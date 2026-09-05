import spacy
import whois
from datetime import datetime

# 1. spaCy NLP Model Load Karein
nlp = spacy.load("en_core_web_sm")

class CompanyVerifier:
    def extract_company_name(self, job_text: str) -> str:
        """Text mein se Named Entity Recognition (NER) ke zariye Company Name dhoondta hai"""
        doc = nlp(job_text)
        for ent in doc.ents:
            if ent.label_ == "ORG":  # ORG = Organization
                return ent.text
        return "Unknown Company"

    def check_domain_age(self, domain_name: str) -> dict:
        """Domain ki age aur details check karta hai using WHOIS"""
        try:
            domain_info = whois.whois(domain_name)
            creation_date = domain_info.creation_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if creation_date:
                age_days = (datetime.now() - creation_date).days
                return {"success": True, "age_days": age_days, "creation_date": str(creation_date.date())}
            return {"success": False, "reason": "Creation date not found"}
        except Exception as e:
            return {"success": False, "reason": str(e)}

    def calculate_trust_score(self, company_name: str, domain_name: str = None) -> dict:
        """Trust Score (0-100) generate karta hai"""
        score = 50  # Base Score
        flags = []

        # 1. Company Name Presence Check
        if company_name != "Unknown Company":
            score += 20
        else:
            flags.append("Company name not clearly stated in posting.")

        # 2. Domain Age Check (Agar Domain Diya Gaya Ho)
        if domain_name:
            domain_data = self.check_domain_age(domain_name)
            if domain_data["success"]:
                age = domain_data["age_days"]
                if age > 730:  # Older than 2 years
                    score += 30
                elif age > 180:  # Older than 6 months
                    score += 15
                else:  # Very New Domain (< 6 months)
                    score -= 30
                    flags.append("Warning: Domain registered very recently (< 6 months).")
            else:
                flags.append("Could not verify domain registration details.")

        return {
            "company_name": company_name,
            "trust_score": max(0, min(100, score)),
            "flags": flags
        }

# --- Direct Module Testing ---
if __name__ == "__main__":
    verifier = CompanyVerifier()
    
    sample_text = "Google is hiring Senior Software Engineers for remote work."
    extracted_org = verifier.extract_company_name(sample_text)
    
    # Google.com lookup test
    result = verifier.calculate_trust_score(extracted_org, domain_name="google.com")
    
    print("\n--- Company Verification Result ---")
    print(f"Extracted Company: {result['company_name']}")
    print(f"Trust Score: {result['trust_score']} / 100")
    print(f"Flags/Alerts: {result['flags']}")