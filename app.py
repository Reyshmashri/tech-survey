from flask import Flask, render_template, request, redirect
from supabase import create_client
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Missing Supabase environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Home page
@app.route('/')
def home():
    return render_template("index.html")


# Submit form
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "age_group": request.form.get("age_group"),
            "occupation": request.form.get("occupation"),
            "screen_time": request.form.get("screen_time"),
            "device": request.form.get("device"),
            "morning_check": request.form.get("morning_check"),
            "anxiety": request.form.get("anxiety"),
            "communication": int(request.form.get("communication")),
            "ease": int(request.form.get("ease")),
            "dependence": request.form.get("dependence"),
            "screen_limit": request.form.get("screen_limit")
        }

        print("📌 DATA:", data)

        response = supabase.table("tech_survey").insert(data).execute()

        print("✅ INSERT SUCCESS:", response)

        return redirect("/charts")

    except Exception as e:
        print("❌ ERROR:", e)
        return "Error occurred"


# Success page
@app.route('/success')
def success():
    return render_template("success.html")


@app.route("/charts")
def charts():
    try:
        # Fetch data from Supabase
        response = supabase.table("tech_survey").select("*").execute()
        data = response.data

        if not data:
            return "No data available. Please submit the survey first."

        df = pd.DataFrame(data)
        print(f"✅ Loaded {len(df)} records")

        # Create static folder if not exists
        os.makedirs("static", exist_ok=True)

        # -------- Chart 1: Device Usage --------
        plt.figure(figsize=(8, 6))
        df['device'].value_counts().plot(kind='bar', color='#8b5cf6')
        plt.title("Device Usage")
        plt.xlabel("Device")
        plt.ylabel("Count")
        plt.tight_layout()
        chart1_path = os.path.join("static", "device_chart.png")
        plt.savefig(chart1_path, dpi=100, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {chart1_path}")

        # -------- Chart 2: Screen Time --------
        plt.figure(figsize=(8, 6))
        df['screen_time'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe'])
        plt.title("Screen Time Distribution")
        plt.ylabel('')
        plt.tight_layout()
        chart2_path = os.path.join("static", "screen_chart.png")
        plt.savefig(chart2_path, dpi=100, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {chart2_path}")

        # -------- Chart 3: Anxiety --------
        plt.figure(figsize=(8, 6))
        df['anxiety'].value_counts().plot(kind='bar', color='#8b5cf6')
        plt.title("Anxiety Without Internet")
        plt.xlabel("Response")
        plt.ylabel("Count")
        plt.tight_layout()
        chart3_path = os.path.join("static", "anxiety_chart.png")
        plt.savefig(chart3_path, dpi=100, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {chart3_path}")

        return render_template("charts.html")
    
    except Exception as e:
        print("❌ CHART ERROR:", e)
        import traceback
        traceback.print_exc()
        return f"Error generating charts: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
