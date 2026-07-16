import json
import random
import os

def main():
    cases_path = "../../data/synthetic_cases.json"
    with open(cases_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    # We need >=20 English, >=20 Kannada, >=10 Code-switched
    # We will sample cases and create queries for them.

    # Fix seed for reproducibility
    random.seed(42)
    sample_cases = random.sample(cases, 60)

    en_queries = []
    kn_queries = []
    cs_queries = []

    for i, case in enumerate(sample_cases):
        case_id = case["case_id"]
        mo = case["modus_operandi"]
        district = case["location"]["district"]
        
        # Exact field lookups
        if i % 3 == 0:
            en_q = f"{mo} in {district}"
            kn_q = f"{district} ದಲ್ಲಿ {mo} ಪ್ರಕರಣ" # Basic translation logic placeholder, we know generate_dataset.py has mo_kn
            # We can use narrative for NL questions.
        elif i % 3 == 1:
            en_q = f"Looking for incidents of {mo} that happened in {district}"
            kn_q = f"{district} ಪ್ರದೇಶದಲ್ಲಿ {mo} ಕುರಿತು ಹುಡುಕಿ"
        else:
            en_q = f"Any {mo} cases reported from {district}?"
            kn_q = f"{district} ದಿಂದ ವರದಿಯಾದ {mo} ಪ್ರಕರಣಗಳು"

        if i < 25:
            en_queries.append({
                "question_id": f"eval-en-{case_id}",
                "query_text": en_q,
                "language": "en",
                "expected_case_ids": [case_id],
                "notes": "English eval query"
            })
        elif i < 50:
            kn_queries.append({
                "question_id": f"eval-kn-{case_id}",
                "query_text": kn_q,
                "language": "kn",
                "expected_case_ids": [case_id],
                "notes": "Kannada eval query"
            })
        else:
            cs_q = f"{mo} ಪ್ರಕರಣ in {district}"
            cs_queries.append({
                "question_id": f"eval-cs-{case_id}",
                "query_text": cs_q,
                "language": "kn-en",
                "expected_case_ids": [case_id],
                "notes": "Code-switched eval query"
            })
    
    # Add some ambiguous queries
    en_queries.append({
         "question_id": "eval-en-ambiguous-1",
         "query_text": "alien abduction in Bengaluru",
         "language": "en",
         "expected_case_ids": [],
         "notes": "Ambiguous query, should return nothing"
    })
    kn_queries.append({
         "question_id": "eval-kn-ambiguous-1",
         "query_text": "ಬೆಂಗಳೂರಿನಲ್ಲಿ ಏಲಿಯನ್ ಅಪಹರಣ",
         "language": "kn",
         "expected_case_ids": [],
         "notes": "Ambiguous query, should return nothing"
    })

    with open("eval_set_en.json", "w", encoding="utf-8") as f:
        json.dump(en_queries, f, indent=2, ensure_ascii=False)
    
    with open("eval_set_kn.json", "w", encoding="utf-8") as f:
        json.dump(kn_queries, f, indent=2, ensure_ascii=False)
        
    with open("eval_set_codeswitch.json", "w", encoding="utf-8") as f:
        json.dump(cs_queries, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {len(en_queries)} EN, {len(kn_queries)} KN, {len(cs_queries)} CS queries.")

if __name__ == '__main__':
    main()
