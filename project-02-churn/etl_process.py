import csv
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

if not os.path.exists(os.path.join(raw_dir, 'customers.csv')):
    print("Raw data missing. Executing enrich_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'enrich_data.py')], check=True)

print("--- Running ETL Process: Project 02 (Customer Churn) ---")

# 1. Clean Customers
customers = []
valid_cust_ids = set()
with open(os.path.join(raw_dir, 'customers.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['signup_date']:
            continue
        customers.append(row)
        valid_cust_ids.add(row['customer_id'])

with open(os.path.join(proc_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
    writer.writeheader()
    writer.writerows(customers)
print(f"[OK] Processed {len(customers)} customers (dropped signup_date missing anomalies).")

# 2. Clean Support Tickets
tickets = []
with open(os.path.join(raw_dir, 'support_tickets.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['customer_id'] not in valid_cust_ids:
            continue
        row['resolution_time_hours'] = str(abs(int(row['resolution_time_hours'])))
        tickets.append(row)

with open(os.path.join(proc_dir, 'support_tickets.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(tickets[0].keys()))
    writer.writeheader()
    writer.writerows(tickets)
print(f"[OK] Processed {len(tickets)} support tickets (resolution_time anomalies fixed).")

# 3. Clean Usage Logs
logs = []
seen_logs = set()
with open(os.path.join(raw_dir, 'usage_logs.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lid = row['log_id']
        if lid in seen_logs:
            continue
        if row['customer_id'] not in valid_cust_ids:
            continue
        seen_logs.add(lid)
        logs.append(row)

with open(os.path.join(proc_dir, 'usage_logs.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(logs[0].keys()))
    writer.writeheader()
    writer.writerows(logs)
print(f"[OK] Processed {len(logs)} usage logs (deduplicated & referential integrity checked).")
print("SUCCESS: Project 02 ETL process complete! Clean data in data/processed/")
