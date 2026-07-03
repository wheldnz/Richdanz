import csv
import random
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 2 - Customer Churn Analytics (Pure Python)...")

pay_methods = ['Auto-Debit Credit Card', 'Auto-Debit Bank Transfer', 'Manual E-Wallet']

# 1. Generate Customers (5,000 customers)
NUM_CUST = 5000
customers = []
start_date = datetime(2023, 1, 1)

for i in range(1, NUM_CUST + 1):
    signup = start_date + timedelta(days=random.randint(0, 500))
    status = random.choices(['Active', 'Churned'], weights=[0.85, 0.15])[0]
    pay = random.choice(pay_methods)
    
    signup_str = signup.strftime('%Y-%m-%d')
    # Anomali: 1% data signup_date adalah kosong
    if random.random() < 0.01:
        signup_str = ''
        
    customers.append({
        'customer_id': i,
        'signup_date': signup_str,
        'status': status,
        'payment_method': pay
    })

with open('data/raw/customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'signup_date', 'status', 'payment_method'])
    writer.writeheader()
    writer.writerows(customers)
print("SUCCESS: Berhasil membuat data/raw/customers.csv (5000 baris)")

# 2. Generate Usage Logs
logs = []
for i in range(1, 15001):
    c_id = random.randint(1, NUM_CUST)
    login = start_date + timedelta(days=random.randint(500, 600))
    
    logs.append({
        'log_id': i,
        'customer_id': c_id,
        'login_date': login.strftime('%Y-%m-%d'),
        'feature_clicks': random.randint(1, 50)
    })

# Anomali duplikat (0.5% duplikat)
num_dupes = int(len(logs) * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(logs, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['log_id'] = len(logs) + 1
        logs.append(new_item)

with open('data/raw/usage_logs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['log_id', 'customer_id', 'login_date', 'feature_clicks'])
    writer.writeheader()
    writer.writerows(logs)
print(f"SUCCESS: Berhasil membuat data/raw/usage_logs.csv ({len(logs)} baris - mengandung anomali)")

# 3. Generate Support Tickets
tickets = []
categories = ['Teknis', 'Tagihan', 'Akun']
for i in range(1, 2001):
    c_id = random.randint(1, NUM_CUST)
    t_date = start_date + timedelta(days=random.randint(200, 600))
    res_time = random.randint(1, 72)
    
    # Anomali: 2% support ticket memiliki resolution_time negatif
    if random.random() < 0.02:
        res_time = -res_time
        
    tickets.append({
        'ticket_id': i,
        'customer_id': c_id,
        'ticket_date': t_date.strftime('%Y-%m-%d'),
        'category': random.choice(categories),
        'resolution_time_hours': res_time
    })

with open('data/raw/support_tickets.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['ticket_id', 'customer_id', 'ticket_date', 'category', 'resolution_time_hours'])
    writer.writeheader()
    writer.writerows(tickets)
print(f"SUCCESS: Berhasil membuat data/raw/support_tickets.csv ({len(tickets)} baris - mengandung anomali)")
print("Proses pembuatan raw data churn selesai!")
