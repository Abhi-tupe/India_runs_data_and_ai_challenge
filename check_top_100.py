import csv
import json
import sys

def check_results(csv_path, jsonl_path):
    # 1. Read your top 100 candidate IDs in order of rank
    top_100_ids = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            top_100_ids.append(row['candidate_id'])
            if len(top_100_ids) >= 100:
                break

    # 2. Look up the full profile details from the main dataset
    candidate_lookup = {}
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            cand = json.loads(line)
            cid = cand.get('candidate_id')
            if cid in top_100_ids:
                candidate_lookup[cid] = cand

    # 3. Print out a clean snapshot of the Top 15 to inspect them immediately
    print("\n" + "="*80)
    print(f"   DIAGNOSTIC SNAPSHOT: TOP 15 RANKED CANDIDATES")
    print("="*80)
    
    for rank, cid in enumerate(top_100_ids[:15], 1):
        cand = candidate_lookup.get(cid)
        if not cand:
            print(f"Rank {rank}: {cid} (Profile data missing from JSONL)")
            continue
            
        prof = cand.get('profile', {})
        name = prof.get('anonymized_name', 'Unknown')
        title = prof.get('current_title', 'N/A')
        company = prof.get('current_company', 'N/A')
        exp = prof.get('years_of_experience', 0)
        
        # Grab up to 5 top skills listed
        skills = [s.get('name') for s in cand.get('skills', [])[:5]]
        skills_str = ", ".join(skills) if skills else "None listed"

        print(f"Rank {rank:02d} | Code: {cid} | Name: {name}")
        print(f"        Title: {title} at {company} ({exp} Yrs Exp)")
        print(f"        Top Skills: {skills_str}")
        print("-" * 80)

if __name__ == "__main__":
    check_results("team_abhi.csv", "candidates.jsonl")