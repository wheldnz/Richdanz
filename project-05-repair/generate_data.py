import csv
import random
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 5 - Repair Service Analytics (Pure Python)...")

# 1. Generate Technician (100 technicians)
techs = []
for i in range(1, 101):
    # Anomali: 2% teknisi memiliki ID negatif
    t_id = i
    if random.random() < 0.02:
        t_id = -t_id
        
    techs.append({
        'technician_id': t_id,
        'technician_name': f"Teknisi Spesialis {i}",
        'is_certified': random.choices([1, 0], weights=[0.75, 0.25])[0]
    })

with open('data/raw/technician.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['technician_id', 'technician_name', 'is_certified'])
    writer.writeheader()
    writer.writerows(techs)
print(f"SUCCESS: Berhasil membuat data/raw/technician.csv ({len(df_techs) if 'df_techs' in locals() else 100} baris)")

# 2. Generate Tickets (4,000 tickets)
NUM_TICKETS = 4000
tickets = []
warranties = []
start_date = datetime(2023, 1, 1)

for i in range(1, NUM_TICKETS + 1):
    t_id = random.randint(1, 100)
    dev_id = random.randint(1, 10000)
    comp_date = start_date + timedelta(days=random.randint(0, 500))
    status = 'Completed'
    
    # Anomali: 1% tiket completed tetapi completion_date kosong
    comp_date_str = comp_date.strftime('%Y-%m-%d')
    if random.random() < 0.01:
        comp_date_str = ''
        
    tickets.append({
        'ticket_id': i,
        'device_id': dev_id,
        'technician_id': t_id,
        'status': status,
        'completion_date': comp_date_str
    })
    
    if comp_date_str:
        # Anomali: 1.5% klaim garansi memiliki tanggal sebelum penyelesaian perbaikan (out-of-order)
        is_bad_date = random.random() < 0.015
        
        # Get technician certification status
        is_certified = next(item for item in techs if abs(item['technician_id']) == t_id)['is_certified']
        rate = 0.28 if is_certified == 0 else 0.08
        
        if random.random() < rate:
            if is_bad_date:
                claim_date = comp_date - timedelta(days=random.randint(1, 10))
            else:
                claim_date = comp_date + timedelta(days=random.randint(1, 29))
                
            warranties.append({
                'warranty_id': len(warranties) + 1,
                'device_id': dev_id,
                'claim_date': claim_date.strftime('%Y-%m-%d')
            })

# Masukkan anomali: Duplikat Tiket (0.5% duplikat)
num_dupes = int(len(tickets) * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(tickets, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['ticket_id'] = len(tickets) + 1
        tickets.append(new_item)

with open('data/raw/ticket.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['ticket_id', 'device_id', 'technician_id', 'status', 'completion_date'])
    writer.writeheader()
    writer.writerows(tickets)

with open('data/raw/warranty.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['warranty_id', 'device_id', 'claim_date'])
    writer.writeheader()
    writer.writerows(warranties)

print(f"SUCCESS: Berhasil membuat data/raw/ticket.csv ({len(tickets)} baris - mengandung anomali)")
print(f"SUCCESS: Berhasil membuat data/raw/warranty.csv ({len(warranties)} baris - mengandung anomali)")
print("Proses pembuatan raw data repair selesai!")
