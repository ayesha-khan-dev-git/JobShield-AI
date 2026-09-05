from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import re
import sqlite3
from datetime import datetime

# 1. FastAPI App Initialize
app = FastAPI(
    title="JobShield AI Engine",
    description="Backend API for AI-Powered Job Scam Detection",
    version="1.0"
)

# 2. CORS Middleware (Custom HTML Dashboard Connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ML Model & Vectorizer Load
with open("jobshield_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# 4. Database Setup (SQLite)
def init_db():
    conn = sqlite3.connect("jobshield.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            scam_probability REAL,
            risk_level TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 5. Request Schema
class JobAnalysisRequest(BaseModel):
    title: str
    description: str
    company_name: str = ""

# 6. Helper Function: Text Cleaning
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 7. API Endpoints
@app.get("/")
def home():
    return {"message": "JobShield API is Live & Running!"}

@app.post("/analyze")
def analyze_job(job: JobAnalysisRequest):
    full_text = clean_text(f"{job.title} {job.company_name} {job.description}")
    
    # Vectorize
    vectorized_text = vectorizer.transform([full_text])
    
    # Predict Scam Probability
    probabilities = model.predict_proba(vectorized_text)[0]
    scam_prob = float(probabilities[1])  # Class 1 = Fake/Scam
    
    # High-Risk Scam Keywords Detection (Rules Layer)
    scam_keywords = ['fee', 'whatsapp', 'gmail', 'transfer', 'urgent', 'cash', 'wire', 'typing', 'registration', 'money']
    keyword_matches = [kw for kw in scam_keywords if kw in full_text]
    
    # Upgraded Sensitivity Logic
    if scam_prob >= 0.40 or len(keyword_matches) >= 2:
        risk_level = "High"
        # Boost probability visual if high risk triggered by key flags
        scam_prob = max(scam_prob, 0.78)
    elif scam_prob >= 0.20 or len(keyword_matches) == 1:
        risk_level = "Medium"
        scam_prob = max(scam_prob, 0.45)
    else:
        risk_level = "Low"

    # Save to SQLite Database
    conn = sqlite3.connect("jobshield.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (job_title, scam_probability, risk_level, timestamp) VALUES (?, ?, ?, ?)",
        (job.title, round(scam_prob * 100, 2), risk_level, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return {
        "job_title": job.title,
        "scam_probability_percent": round(scam_prob * 100, 2),
        "risk_level": risk_level,
        "status": "Success"
    }

@app.get("/history")
def get_history():
    conn = sqlite3.connect("jobshield.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "title": row[1],
            "scam_probability": row[2],
            "risk_level": row[3],
            "timestamp": row[4]
        })
    return {"recent_searches": history}