import csv
import random
from datetime import datetime, timedelta
import os

random.seed(42)

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(proc_dir, exist_ok=True)

print("--- Enriching Project 06: Auto Insurance Underwriting Dataset ---")

auto_file = os.path.join(base_dir, 'AutoInsurance.csv')

customers = []
policies = []
claims = []

ref_date = datetime(2025, 6, 30)

claim_counter = 1
reasons = ['Kecelakaan Tabrakan', 'Kerusakan Bodi', 'Kerusakan Kaca', 'Pencurian', 'Bencana Alam']

with open(auto_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        cid = row['Customer'].strip()
        policy_id = f"POL-{cid}"
        
        try:
            m_inception = int(row['Months Since Policy Inception'])
        except ValueError:
            m_inception = 12
            
        start_dt = ref_date - timedelta(days=m_inception * 30 + random.randint(0, 15))
        
        try:
            prem = float(row['Monthly Premium Auto'])
        except ValueError:
            prem = 100.0
            
        try:
            tot_claim_val = float(row['Total Claim Amount'])
        except ValueError:
            tot_claim_val = 0.0
            
        customers.append({
            'customer_id': cid,
            'state': row['State'],
            'gender': row['Gender'],
            'education': row['Education'],
            'employment_status': row['EmploymentStatus'],
            'income': row['Income'],
            'marital_status': row['Marital Status'],
            'customer_lifetime_value': row['Customer Lifetime Value']
        })
        
        policies.append({
            'policy_id': policy_id,
            'customer_id': cid,
            'policy_type': row['Policy Type'],
            'policy_name': row['Policy'],
            'coverage': row['Coverage'],
            'monthly_premium': prem,
            'vehicle_class': row['Vehicle Class'],
            'vehicle_size': row['Vehicle Size'],
            'effective_start_date': start_dt.strftime('%Y-%m-%d')
        })
        
        # Generate Claim records if Total Claim Amount > 0
        if tot_claim_val > 0:
            try:
                m_last_claim = int(row['Months Since Last Claim'])
            except ValueError:
                m_last_claim = 3
                
            claim_dt = ref_date - timedelta(days=m_last_claim * 30 + random.randint(1, 10))
            if claim_dt < start_dt:
                claim_dt = start_dt + timedelta(days=5)
                
            status = random.choices(['Approved', 'Pending', 'Rejected'], weights=[85, 7, 8])[0]
            reason = random.choices(reasons, weights=[45, 25, 15, 10, 5])[0]
            
            claims.append({
                'claim_id': f"CLM-{claim_counter:06d}",
                'policy_id': policy_id,
                'customer_id': cid,
                'claim_date': claim_dt.strftime('%Y-%m-%d'),
                'claim_amount': round(tot_claim_val, 2),
                'claim_status': status,
                'claim_reason': reason
            })
            claim_counter += 1

with open(os.path.join(raw_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
    writer.writeheader()
    writer.writerows(customers)

with open(os.path.join(raw_dir, 'policies.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(policies[0].keys()))
    writer.writeheader()
    writer.writerows(policies)

with open(os.path.join(raw_dir, 'claims.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
    writer.writeheader()
    writer.writerows(claims)

print(f"SUCCESS: Enriched {len(customers)} customers, {len(policies)} policies, and {len(claims)} insurance claim records!")
