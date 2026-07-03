import csv
import random
import math
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 3 - Supply Chain Analytics (Pure Python)...")

regions = ['Pusat', 'Utara', 'Selatan', 'Barat', 'Timur']

# 1. Generate Warehouse (50 rows)
warehouses = []
for i in range(1, 51):
    cap = random.randint(10000, 50000)
    # Anomali: 4% kapasitas gudang bernilai negatif
    if random.random() < 0.04:
        cap = -cap
        
    warehouses.append({
        'warehouse_id': i,
        'warehouse_name': f"Gudang {random.choice(regions)} {i}",
        'capacity_cbm': cap
    })

with open('data/raw/warehouse.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['warehouse_id', 'warehouse_name', 'capacity_cbm'])
    writer.writeheader()
    writer.writerows(warehouses)
print("SUCCESS: Berhasil membuat data/raw/warehouse.csv (50 baris)")

# 2. Generate Supplier (50 rows)
suppliers = []
for i in range(1, 51):
    suppliers.append({
        'supplier_id': i,
        'supplier_name': f"Supplier Utama {i}",
        'contracted_lead_time_days': random.randint(3, 15)
    })

with open('data/raw/supplier.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['supplier_id', 'supplier_name', 'contracted_lead_time_days'])
    writer.writeheader()
    writer.writerows(suppliers)
print("SUCCESS: Berhasil membuat data/raw/supplier.csv (50 baris)")

# 3. Generate POs & Shipments (4,000 baris)
NUM_POS = 4000
pos = []
shipments = []
start_date = datetime(2023, 1, 1)

# Helper function to generate log-normal random numbers
def lognormal_random(mean, sigma):
    u1 = random.random()
    u2 = random.random()
    # Box-Muller transform
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return math.exp(mean + sigma * z0)

for i in range(1, NUM_POS + 1):
    po_date = start_date + timedelta(days=random.randint(0, 600))
    s_id = random.randint(1, 50)
    w_id = random.randint(1, 50)
    
    pos.append({
        'po_id': i,
        'po_date': po_date.strftime('%Y-%m-%d'),
        'supplier_id': s_id,
        'warehouse_id': w_id
    })
    
    contracted = next(item for item in suppliers if item['supplier_id'] == s_id)['contracted_lead_time_days']
    
    # Anomali: 1.5% shipment memiliki tanggal kedatangan LEBIH DULU daripada PO date
    if random.random() < 0.015:
        actual_lead = -random.randint(1, 10)
    else:
        # Lead time normal (log-normal)
        actual_lead = int(contracted + lognormal_random(mean=0.5, sigma=0.5))
        
    est_arrival = po_date + timedelta(days=contracted)
    act_arrival = po_date + timedelta(days=actual_lead)
    
    shipments.append({
        'shipment_id': i,
        'po_id': i,
        'estimated_arrival_date': est_arrival.strftime('%Y-%m-%d'),
        'actual_arrival_date': act_arrival.strftime('%Y-%m-%d'),
        'is_in_full': random.choices([1, 0], weights=[0.88, 0.12])[0]
    })

# Masukkan anomali: Duplikat PO (0.5% duplikat)
num_dupes = int(len(pos) * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(pos, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['po_id'] = len(pos) + 1
        pos.append(new_item)

with open('data/raw/purchase_order.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['po_id', 'po_date', 'supplier_id', 'warehouse_id'])
    writer.writeheader()
    writer.writerows(pos)

with open('data/raw/shipment.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['shipment_id', 'po_id', 'estimated_arrival_date', 'actual_arrival_date', 'is_in_full'])
    writer.writeheader()
    writer.writerows(shipments)

print(f"SUCCESS: Berhasil membuat data/raw/purchase_order.csv ({len(pos)} baris - mengandung anomali)")
print(f"SUCCESS: Berhasil membuat data/raw/shipment.csv ({len(shipments)} baris - mengandung anomali)")
print("Proses pembuatan raw data supply chain selesai!")
