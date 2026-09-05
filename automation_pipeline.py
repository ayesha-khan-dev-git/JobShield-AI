import time
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# Track processed jobs to avoid duplicates
processed_jobs_hash = set()

def send_telegram_alert(job_title, risk_score):
    """High Risk Jobs ke liye Telegram Bot Alert bhejta hai (Optional Token Integration)"""
    print(f"\n🚨 [HIGH RISK ALERT]: '{job_title}' identified as potential scam! (Probability: {risk_score}%)")
    
    # Telegram Integration Schema (Optional: Fill Bot Token & Chat ID)
    # BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    # CHAT_ID = "YOUR_CHAT_ID"
    # message = f"🚨 *Scam Alert!*\nJob: {job_title}\nRisk Score: {risk_score}%"
    # requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown")

def scheduled_job_scanner():
    """Background task jo periodically job postings process karta hai"""
    print(f"\n⏰ [{time.strftime('%Y-%m-%d %H:%M:%S')}] Background Job Scanner Running...")
    
    # Simulated Incoming Scraped Jobs Queue
    incoming_jobs = [
        {"id": "JOB101", "title": "Data Analyst", "description": "SQL and Python required at established fintech."},
        {"id": "JOB102", "title": "Urgent Cash Handler", "description": "Earn $500/day working 1 hr. Send registration fee immediately."},
        {"id": "JOB101", "title": "Data Analyst", "description": "SQL and Python required at established fintech."} # Duplicate
    ]

    for job in incoming_jobs:
        job_id = job["id"]
        
        # 1. Duplicate Detection Check
        if job_id in processed_jobs_hash:
            print(f"⏭️ Skipping Duplicate Job ID: {job_id}")
            continue
            
        processed_jobs_hash.add(job_id)
        
        # 2. Analyze via Phase 2 FastAPI Service
        try:
            response = requests.post("http://127.0.0.1:8000/analyze", json={
                "title": job["title"],
                "description": job["description"],
                "company_name": "Unknown"
            })
            
            if response.status_code == 200:
                result = response.json()
                scam_prob = result["scam_probability_percent"]
                print(f"✅ Processed '{job['title']}': Risk Level = {result['risk_level']} ({scam_prob}%)")
                
                # 3. High Risk Trigger Alert
                if result["risk_level"] == "High":
                    send_telegram_alert(job["title"], scam_prob)
        except Exception as e:
            print(f"⚠️ Could not connect to FastAPI server. Ensure 'uvicorn app:app' is running! ({e})")

# --- Scheduler Setup ---
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # Har 15 Seconds baad background job run karega (Testing Interval)
    scheduler.add_job(scheduled_job_scanner, 'interval', seconds=15)
    scheduler.start()
    
    print("🚀 Automation Pipeline Active! Running background scanner every 15 seconds. Press Ctrl+C to exit.")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\n🛑 Scheduler Stopped.")