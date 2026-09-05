import pandas as pd
import numpy as np

print("⚙️ Dataset local system par create ho raha hai...")

# Standard Kaggle dataset schema
n_samples = 2000

data = {
    'job_id': range(1, n_samples + 1),
    'title': np.random.choice([
        'Software Engineer', 'Data Entry Clerk', 'Customer Service Rep', 
        'Work From Home Specialist', 'Marketing Manager', 'Urgent Hiring Admin'
    ], size=n_samples),
    'location': np.random.choice(['US, NY, New York', 'US, CA, Los Angeles', 'PK, LHR, Lahore', 'IN, DEL, Delhi'], size=n_samples),
    'department': np.random.choice(['IT', 'Sales', 'Admin', 'Customer Care', None], size=n_samples),
    'salary_range': np.random.choice(['50000-70000', '100000-120000', '1000-2000', None], size=n_samples),
    'company_profile': np.random.choice([
        'We are a leading tech firm establishing global remote teams.',
        'Earn $500 daily working 2 hours from home. No experience needed!',
        'Established multi-national logistics company.',
        'Immediate opening! Send bank details for equipment processing.'
    ], size=n_samples),
    'description': np.random.choice([
        'Looking for experienced Python developer with FastAPI and SQL skills.',
        'Urgent requirement! High payout daily. Contact personal gmail address immediately.',
        'Manage customer queries via ticket portal and phone support.',
        'Simple copy paste job. High commission guaranteed.'
    ], size=n_samples),
    'requirements': np.random.choice([
        'Bachelor degree in CS, 2+ years Python experience required.',
        'Must have laptop and active internet. No qualifications needed.',
        'Strong communication skills and team management experience.'
    ], size=n_samples),
    'benefits': np.random.choice(['Health insurance, 401k, paid leaves.', 'Weekly cash bonuses.', None], size=n_samples),
    'telecommuting': np.random.choice([0, 1], size=n_samples),
    'has_company_logo': np.random.choice([0, 1], size=n_samples),
    'has_questions': np.random.choice([0, 1], size=n_samples),
    'employment_type': np.random.choice(['Full-time', 'Part-time', 'Contract', None], size=n_samples),
    'required_experience': np.random.choice(['Entry level', 'Mid-Senior level', 'Associate', None], size=n_samples),
    'required_education': np.random.choice(["Bachelor's Degree", "High School or equivalent", None], size=n_samples),
    'industry': np.random.choice(['Information Technology', 'Financial Services', 'Marketing', None], size=n_samples),
    'function': np.random.choice(['Engineering', 'Administrative', 'Sales', None], size=n_samples),
    'fraudulent': np.random.choice([0, 1], size=n_samples, p=[0.93, 0.07])
}

df = pd.DataFrame(data)
df.to_csv("fake_job_postings.csv", index=False)

print("\n✅ Dataset successfully ban gaya hai!")
print(f"📊 Saved File: fake_job_postings.csv ({df.shape[0]} rows, {df.shape[1]} columns)")