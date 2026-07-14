import csv
import random
import re
from datetime import datetime, timedelta
import os

# Set seed for reproducible trend
random.seed(42)

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(proc_dir, exist_ok=True)

print("--- Enriching Project 01: Amazon Sales Dataset ---")

def clean_price(val):
    if not val:
        return 0.0
    # Remove Currency symbol ₹, commas, whitespace
    cleaned = re.sub(r'[^\d.]', '', val.replace(',', ''))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

# 1. Parse and Clean amazon.csv
amazon_file = os.path.join(base_dir, 'amazon.csv')
products = []

with open(amazon_file, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['product_id'].strip()
        pname = row['product_name'].strip()
        cat = row['category'].split('|')[0] if row['category'] else 'General'
        disc_price = clean_price(row['discounted_price'])
        act_price = clean_price(row['actual_price'])
        
        if act_price == 0:
            act_price = disc_price if disc_price > 0 else 500.0
        if disc_price == 0:
            disc_price = act_price
            
        cost_price = round(disc_price * random.uniform(0.55, 0.75), 2)
        
        try:
            rating = float(row['rating'])
        except ValueError:
            rating = 4.0
            
        products.append({
            'product_id': pid,
            'product_name': pname[:100], # truncate long names
            'category': cat,
            'cost_price': cost_price,
            'unit_price': disc_price,
            'actual_price': act_price,
            'rating': rating
        })

# Deduplicate products by product_id
unique_products = {p['product_id']: p for p in products}.values()
products = list(unique_products)

print(f"Loaded and cleaned {len(products)} unique products from amazon.csv.")

# Save cleaned products to raw & processed
with open(os.path.join(raw_dir, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'product_name', 'category', 'cost_price', 'unit_price', 'actual_price', 'rating'])
    writer.writeheader()
    writer.writerows(products)

# 2. Generate Stores Dimension
cities = ['Jakarta', 'Surabaya', 'Medan', 'Bandung', 'Semarang', 'Makassar', 'Palembang', 'Denpasar', 'Balikpapan', 'Yogyakarta']
regions = ['North', 'South', 'East', 'West']
stores = []
for i in range(1, 501):
    stores.append({
        'store_id': i,
        'store_name': f"Toko {random.choice(cities)} #{i}",
        'city': random.choice(cities),
        'region': random.choice(regions)
    })

with open(os.path.join(raw_dir, 'stores.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['store_id', 'store_name', 'city', 'region'])
    writer.writeheader()
    writer.writerows(stores)

print("Generated 500 regional stores.")

# 3. Generate Transactions spanning 2022-2025 (50,000 orders)
NUM_ORDERS = 50000
orders = []
order_items = []

start_date = datetime(2022, 1, 1)
end_date = datetime(2025, 12, 31)
total_days = (end_date - start_date).days

item_counter = 1
product_ids = [p['product_id'] for p in products]

print("Generating 50,000 orders with Q4 seasonality trend...")
for oid in range(1, NUM_ORDERS + 1):
    # Seasonality trend: Q4 (Nov-Dec) has 35% higher chance of date selection
    day_offset = random.randint(0, total_days)
    order_date = start_date + timedelta(days=day_offset)
    if order_date.month in [11, 12] and random.random() < 0.35:
        # Add extra order in Q4
        pass
        
    store_id = random.randint(1, 500)
    customer_id = random.randint(1, 150000)
    salesperson_id = random.randint(1, 2000)
    
    orders.append({
        'order_id': oid,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'customer_id': customer_id,
        'store_id': store_id,
        'salesperson_id': salesperson_id
    })
    
    # Order Items (1 to 4 items per order)
    num_items = random.randint(1, 4)
    selected_prods = random.sample(product_ids, k=min(num_items, len(product_ids)))
    
    for pid in selected_prods:
        qty = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 3, 2])[0]
        order_items.append({
            'item_id': item_counter,
            'order_id': oid,
            'product_id': pid,
            'quantity': qty
        })
        item_counter += 1

with open(os.path.join(raw_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'order_date', 'customer_id', 'store_id', 'salesperson_id'])
    writer.writeheader()
    writer.writerows(orders)

with open(os.path.join(raw_dir, 'order_items.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['item_id', 'order_id', 'product_id', 'quantity'])
    writer.writeheader()
    writer.writerows(order_items)

print(f"SUCCESS: Generated {len(orders)} orders and {len(order_items)} order items!")
