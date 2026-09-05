# 🛡️ JobShield AI — Enterprise Job Scam Detection System

JobShield AI is an intelligent threat detection system designed to identify fraudulent job postings in real time. It utilizes a hybrid evaluation pipeline combining Machine Learning models with automated rule-based overrides to achieve high sensitivity against employment scams.

---

## 🌟 Key Features
* **Hybrid Detection Engine:** Scikit-Learn Random Forest Classifier + TF-IDF Vectorizer coupled with a high-risk Keyword Override Engine.
* **FastAPI Backend:** Lightweight, high-speed REST API featuring dynamic CORS integration.
* **SQLite Audit Database:** Automatically records scan history with precise risk classification and timestamps.
* **Modern Glassmorphic UI:** Responsive dark-mode dashboard equipped with live score gauge visualizations.
* **Automated Launcher:** Includes a 1-click execution script (`start_jobshield.bat`) for easy local deployment.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Machine Learning:** Scikit-Learn, Pickle, Regex
* **Database:** SQLite3
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)

---

## 🚀 How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/ayesha-khan-dev-git/JobShield-AI.git](https://github.com/ayesha-khan-dev-git/JobShield-AI.git)
   cd JobShield-AI

   Install Dependencies:
   pip install fastapi uvicorn scikit-learn pydantic

   Launch the Application:
Double-click start_jobshield.bat OR run:

uvicorn app:app --reload


