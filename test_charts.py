from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch data
response = supabase.table("tech_survey").select("*").execute()
data = response.data

print(f"Records found: {len(data)}")

if data:
    df = pd.DataFrame(data)
    print(df.head())
    
    os.makedirs("static", exist_ok=True)
    
    # Generate charts
    plt.figure()
    df['device'].value_counts().plot(kind='bar', color='#8b5cf6')
    plt.title("Device Usage")
    plt.savefig("static/device_chart.png")
    plt.close()
    print("✅ device_chart.png created")
    
    plt.figure()
    df['screen_time'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title("Screen Time")
    plt.savefig("static/screen_chart.png")
    plt.close()
    print("✅ screen_chart.png created")
    
    plt.figure()
    df['anxiety'].value_counts().plot(kind='bar', color='#8b5cf6')
    plt.title("Anxiety")
    plt.savefig("static/anxiety_chart.png")
    plt.close()
    print("✅ anxiety_chart.png created")
else:
    print("❌ No data in database. Submit a survey first!")
