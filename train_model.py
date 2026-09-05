import pandas as pd
import numpy as np
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import shap

# 1. Dataset Load Karein
print("⏳ Dataset load ho raha hai...")
df = pd.read_csv("fake_job_postings.csv")

# Missing values ko empty string se replace karein
text_columns = ['title', 'company_profile', 'description', 'requirements']
for col in text_columns:
    df[col] = df[col].fillna('')

# 2. Text Preprocessing & Cleaning
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Links remove
    text = re.sub(r'\W', ' ', text) # Special characters remove
    text = re.sub(r'\s+', ' ', text).strip() # Extra spaces remove
    return text

print("🧹 Text clean kar rahe hain...")
# Sub text columns ko combine kar ke ek master text feature banayein
df['full_text'] = (
    df['title'] + " " + 
    df['company_profile'] + " " + 
    df['description'] + " " + 
    df['requirements']
).apply(clean_text)

# Target Variable (0 = Real, 1 = Scam)
X = df['full_text']
y = df['fraudulent']

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Feature Engineering (TF-IDF Vectorization)
print("🔤 TF-IDF Features extract ho rahe hain...")
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. Model Training (Random Forest)
print("🤖 Machine Learning Model (Random Forest) train ho raha hai...")
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train_vec, y_train)

# 6. Evaluation
y_pred = model.predict(X_test_vec)
print("\n--- Model Evaluation Results ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(f"F1 Score: {f1_score(y_test, y_pred):.2f}")
print("\nDetailed Report:\n", classification_report(y_test, y_pred))

# 7. Model & Vectorizer Ko Save Karein
with open("jobshield_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("💾 Trained Model ('jobshield_model.pkl') aur Vectorizer save ho gaye hain!")

# 8. SHAP Explainability Test
print("\n🔍 Testing SHAP Explainability...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test_vec.toarray())

print("✅ SHAP Explainer ready hai dashboard integration ke liye!")