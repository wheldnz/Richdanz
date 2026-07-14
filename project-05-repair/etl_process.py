import csv
import os
import subprocess
from datetime import datetime, timedelta

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

if not os.path.exists(os.path.join(raw_dir, 'ticket.csv')):
    print("Raw data missing. Executing generate_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'generate_data.py')], check=True)

print("--- Running ETL Process: Project 05 (Repair Service) ---")

# 1. Clean Technician
techs = []
valid_tech_ids = set()
with open(os.path.join(raw_dir, 'technician.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tid = str(abs(int(row['technician_id'])))
        row['technician_id'] = tid
        techs.append(row)
        valid_tech_ids.add(tid)

with open(os.path.join(proc_dir, 'technician.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(techs[0].keys()))
    writer.writeheader()
    writer.writerows(techs)
print(f"[OK] Processed {len(techs)} technicians (ID anomalies fixed).")

# 2. Clean Tickets
tickets = []
device_comp_dates = {}
seen_tickets = set()

with open(os.path.join(raw_dir, 'ticket.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tid = row['ticket_id']
        if tid in seen_tickets:
            continue
        seen_tickets.add(tid)
        
        row['technician_id'] = str(abs(int(row['technician_id'])))
        if row['technician_id'] not in valid_tech_ids:
            continue
            
        if row['status'] == 'Completed' and not row['completion_date']:
            continue
            
        tickets.append(row)
        if row['completion_date']:
            device_comp_dates[row['device_id']] = row['completion_date']

with open(os.path.join(proc_dir, 'ticket.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(tickets[0].keys()))
    writer.writeheader()
    writer.writerows(tickets)
print(f"[OK] Processed {len(tickets)} tickets (missing completion dates & deduplicated).")

# 3. Clean Warranty Claims
warranties = []
seen_warr = set()
with open(os.path.join(raw_dir, 'warranty.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        wid = row['warranty_id']
        if wid in seen_warr:
            continue
        seen_warr.add(wid)
        
        dev_id = row['device_id']
        if dev_id in device_comp_dates:
            comp_dt_str = device_comp_dates[dev_id]
            if row['claim_date'] < comp_dt_str:
                comp_dt = datetime.strptime(comp_dt_str, '%Y-%m-%d')
                row['claim_date'] = (comp_dt + timedelta(days=7)).strftime('%Y-%m-%d')
                
        warranties.append(row)

with open(os.path.join(proc_dir, 'warranty.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(warranties[0].keys()))
    writer.writeheader()
    writer.writerows(warranties)
print(f"[OK] Processed {len(warranties)} warranty claims (out-of-order date anomalies fixed).")
print("SUCCESS: Project 05 ETL process complete! Clean data in data/processed/")
