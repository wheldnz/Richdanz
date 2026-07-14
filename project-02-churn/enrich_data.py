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

print("--- Enriching Project 02: Telco Customer Churn Dataset ---")

telco_file = os.path.join(base_dir, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
customers = []
usage_logs = []
support_tickets = []

ref_date = datetime(2025, 6, 30)

log_counter = 1
ticket_counter = 1

categories = ['Teknis - Konektivitas', 'Teknis - Lambat', 'Tagihan - Pembayaran', 'Akun - Fitur']

with open(telco_file, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cid = row['customerID'].strip()
        try:
            tenure_months = int(row['tenure'])
        except ValueError:
            tenure_months = 1
            
        signup_dt = ref_date - timedelta(days=tenure_months * 30 + random.randint(0, 15))
        churn = row['Churn'].strip()
        
        customers.append({
            'customer_id': cid,
            'gender': row['gender'],
            'senior_citizen': row['SeniorCitizen'],
            'partner': row['Partner'],
            'dependents': row['Dependents'],
            'tenure_months': tenure_months,
            'signup_date': signup_dt.strftime('%Y-%m-%d'),
            'contract': row['Contract'],
            'payment_method': row['PaymentMethod'],
            'monthly_charges': row['MonthlyCharges'],
            'total_charges': row['TotalCharges'],
            'churn': churn
        })
        
        # Generate Usage Logs over time
        # Monthly snapshots from signup to end
        curr_dt = signup_dt
        active_months = max(1, tenure_months)
        
        for m in range(active_months):
            log_date = signup_dt + timedelta(days=m * 30 + random.randint(1, 25))
            if log_date > ref_date:
                break
                
            # If customer churned, last 2-3 months show declining activity
            if churn == 'Yes' and m >= active_months - 3:
                clicks = random.randint(1, 8) # low engagement
            else:
                clicks = random.randint(15, 60) # healthy engagement
                
            usage_logs.append({
                'log_id': log_counter,
                'customer_id': cid,
                'login_date': log_date.strftime('%Y-%m-%d'),
                'feature_clicks': clicks
            })
            log_counter += 1
            
        # Generate Support Tickets (Higher frequency for Churned customers or Month-to-month)
        num_tickets = 0
        if churn == 'Yes':
            num_tickets = random.choices([1, 2, 3, 4], weights=[20, 35, 30, 15])[0]
        else:
            num_tickets = random.choices([0, 1, 2], weights=[70, 25, 5])[0]
            
        for _ in range(num_tickets):
            t_date = signup_dt + timedelta(days=random.randint(1, active_months * 30))
            if t_date > ref_date:
                t_date = ref_date
                
            category = random.choices(categories, weights=[40, 30, 20, 10])[0]
            resolution_hrs = random.randint(4, 72) if churn == 'Yes' else random.randint(1, 12)
            
            support_tickets.append({
                'ticket_id': ticket_counter,
                'customer_id': cid,
                'ticket_date': t_date.strftime('%Y-%m-%d'),
                'category': category,
                'resolution_time_hours': resolution_hrs
            })
            ticket_counter += 1

# Save enriched raw files
with open(os.path.join(raw_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
    writer.writeheader()
    writer.writerows(customers)

with open(os.path.join(raw_dir, 'usage_logs.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['log_id', 'customer_id', 'login_date', 'feature_clicks'])
    writer.writeheader()
    writer.writerows(usage_logs)

with open(os.path.join(raw_dir, 'support_tickets.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['ticket_id', 'customer_id', 'ticket_date', 'category', 'resolution_time_hours'])
    writer.writeheader()
    writer.writerows(support_tickets)

print(f"SUCCESS: Enriched {len(customers)} customers, {len(usage_logs)} usage logs, and {len(support_tickets)} support tickets!")
