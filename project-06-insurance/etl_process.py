import csv
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

if not os.path.exists(os.path.join(raw_dir, 'claims.csv')):
    print("Raw data missing. Executing enrich_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'enrich_data.py')], check=True)

print("--- Running ETL Process: Project 06 (Insurance Analytics) ---")

# 1. Clean Customers
customers = []
with open(os.path.join(raw_dir, 'customers.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    customers = list(reader)

with open(os.path.join(proc_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
    writer.writeheader()
    writer.writerows(customers)
print(f"[OK] Processed {len(customers)} customers.")

# 2. Clean Policies
policies = []
seen_pol = set()
with open(os.path.join(raw_dir, 'policies.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['policy_id']
        if pid in seen_pol:
            continue
        seen_pol.add(pid)
        
        row['monthly_premium'] = str(abs(float(row['monthly_premium'])))
        policies.append(row)

with open(os.path.join(proc_dir, 'policies.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(policies[0].keys()))
    writer.writeheader()
    writer.writerows(policies)
print(f"[OK] Processed {len(policies)} policies (premium anomalies fixed & deduplicated).")

# 3. Clean Claims
claims = []
with open(os.path.join(raw_dir, 'claims.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['claim_amount'] = str(abs(float(row['claim_amount'])))
        claims.append(row)

with open(os.path.join(proc_dir, 'claims.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
    writer.writeheader()
    writer.writerows(claims)
print(f"[OK] Processed {len(claims)} claims (claim_amount anomalies fixed).")
print("SUCCESS: Project 06 ETL process complete! Clean data in data/processed/")
