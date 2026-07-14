import csv
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

# Ensure raw data is enriched first
if not os.path.exists(os.path.join(raw_dir, 'orders.csv')):
    print("Raw data missing. Executing enrich_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'enrich_data.py')], check=True)

print("--- Running ETL Process: Project 01 (Sales Analytics) ---")

# 1. Clean Products
products = []
with open(os.path.join(raw_dir, 'products.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['cost_price'] = str(abs(float(row['cost_price'])))
        row['unit_price'] = str(abs(float(row['unit_price'])))
        products.append(row)

with open(os.path.join(proc_dir, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
    writer.writeheader()
    writer.writerows(products)
print(f"[OK] Processed {len(products)} products (cost_price anomaly fixed).")

# 2. Clean Stores
stores = []
with open(os.path.join(raw_dir, 'stores.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stores = list(reader)

with open(os.path.join(proc_dir, 'stores.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(stores[0].keys()))
    writer.writeheader()
    writer.writerows(stores)
print(f"[OK] Processed {len(stores)} stores.")

# 3. Clean Orders
orders = []
valid_order_ids = set()
with open(os.path.join(raw_dir, 'orders.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['store_id']:
            continue
        odate = row['order_date']
        if odate < '2022-01-01' or odate > '2025-12-31':
            continue
        orders.append(row)
        valid_order_ids.add(row['order_id'])

with open(os.path.join(proc_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(orders[0].keys()))
    writer.writeheader()
    writer.writerows(orders)
print(f"[OK] Processed {len(orders)} valid orders (dropped store_id missing & invalid date anomalies).")

# 4. Clean Order Items
order_items = []
seen_items = set()
with open(os.path.join(raw_dir, 'order_items.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        item_id = row['item_id']
        if item_id in seen_items:
            continue
        if row['order_id'] not in valid_order_ids:
            continue
        seen_items.add(item_id)
        row['quantity'] = str(abs(int(row['quantity'])))
        order_items.append(row)

with open(os.path.join(proc_dir, 'order_items.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(order_items[0].keys()))
    writer.writeheader()
    writer.writerows(order_items)
print(f"[OK] Processed {len(order_items)} order items (deduplicated & quantity anomalies fixed).")
print("SUCCESS: Project 01 ETL process complete! Clean data in data/processed/")
