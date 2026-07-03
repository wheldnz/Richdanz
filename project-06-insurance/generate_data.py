import csv
import random
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 6 - Insurance Underwriting Analytics (Pure Python)...")

cities = ['Jakarta', 'Surabaya', 'Medan', 'Bandung', 'Semarang', 'Makassar', 'Palembang', 'Denpasar', 'Balikpapan', 'Yogyakarta']

# 1. Generate Branch (10 branches)
branches = [{'branch_id': i, 'branch_name': f"Cabang {city}"} for i, city in enumerate(cities, 1)]

with open('data/raw/branch.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['branch_id', 'branch_name'])
    writer.writeheader()
    writer.writerows(branches)
print("SUCCESS: Berhasil membuat data/raw/branch.csv (10 baris)")

# 2. Generate Policies (4,000 policies)
NUM_POL = 4000
policies = []
claims = []
start_date = datetime(2023, 1, 1)

for i in range(1, NUM_POL + 1):
    b_id = random.randint(1, 10)
    p_type = random.choice(['Kendaraan', 'Kesehatan', 'Properti'])
    premium = random.randint(1500000, 15000000)
    age = random.randint(18, 75)
    
    # Anomali: 1.5% premium bernilai negatif
    if random.random() < 0.015:
        premium = -premium
        
    # Anomali: 1% umur nasabah bernilai negatif atau di luar batas (150 tahun)
    if random.random() < 0.01:
        age = random.choice([-5, 150])
        
    policies.append({
        'policy_id': i,
        'branch_id': b_id,
        'policy_type': p_type,
        'premium_amount': premium,
        'customer_age': age
    })
    
    # Skenario: pengemudi < 25 tahun memiliki rasio klaim kendaraan bermotor 45% (tinggi)
    claim_rate = 0.45 if (p_type == 'Kendaraan' and age < 25) else 0.15
    if random.random() < claim_rate:
        claim_val = int(abs(premium) * random.uniform(0.3, 2.5))
        
        # Anomali: 2% klaim memiliki nominal negatif
        if random.random() < 0.02:
            claim_val = -claim_val
            
        claims.append({
            'claim_id': len(claims) + 1,
            'policy_id': i,
            'claim_amount': claim_val,
            'status': random.choices(['Approved', 'Rejected'], weights=[0.92, 0.08])[0]
        })

# Masukkan anomali: Duplikat polis (0.5% duplikat)
num_dupes = int(len(policies) * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(policies, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['policy_id'] = len(policies) + 1
        policies.append(new_item)

with open('data/raw/policy.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['policy_id', 'branch_id', 'policy_type', 'premium_amount', 'customer_age'])
    writer.writeheader()
    writer.writerows(policies)

with open('data/raw/claim.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['claim_id', 'policy_id', 'claim_amount', 'status'])
    writer.writeheader()
    writer.writerows(claims)

print(f"SUCCESS: Berhasil membuat data/raw/policy.csv ({len(policies)} baris - mengandung anomali)")
print(f"SUCCESS: Berhasil membuat data/raw/claim.csv ({len(claims)} baris - mengandung anomali)")
print("Proses pembuatan raw data asuransi selesai!")
