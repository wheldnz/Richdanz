import csv
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

if not os.path.exists(os.path.join(raw_dir, 'orders.csv')):
    print("Raw data missing. Executing enrich_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'enrich_data.py')], check=True)

print("--- Running ETL Process: Project 03 (Supply Chain) ---")

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

# 2. Clean Products
products = []
with open(os.path.join(raw_dir, 'products.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['price'] = str(abs(float(row['price'])))
        products.append(row)

with open(os.path.join(proc_dir, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
    writer.writeheader()
    writer.writerows(products)
print(f"[OK] Processed {len(products)} products (price anomalies fixed).")

# 3. Clean Orders
orders = []
seen_orders = set()
with open(os.path.join(raw_dir, 'orders.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        oid = (row['order_id'], row['product_id'])
        if oid in seen_orders:
            continue
        seen_orders.add(oid)
        
        real_days = int(float(row['real_shipping_days']))
        sched_days = int(float(row['scheduled_shipping_days']))
        if real_days < 0:
            row['real_shipping_days'] = str(sched_days)
            
        orders.append(row)

with open(os.path.join(proc_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(orders[0].keys()))
    writer.writeheader()
    writer.writerows(orders)
print(f"[OK] Processed {len(orders)} orders (lead_time anomalies fixed & deduplicated).")
print("SUCCESS: Project 03 ETL process complete! Clean data in data/processed/")
