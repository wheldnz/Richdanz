import csv
import random
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 1 - Enterprise Sales Analytics (Pure Python)...")

cities = ['Jakarta', 'Surabaya', 'Medan', 'Bandung', 'Semarang', 'Makassar', 'Palembang', 'Denpasar', 'Balikpapan', 'Yogyakarta']
regions = ['North', 'South', 'East', 'West']
categories = ['Elektronik', 'Mebel', 'Pakaian', 'Makanan']
product_adjectives = ['Mewah', 'Premium', 'Eco', 'Super', 'Classic', 'Modern', 'Smart', 'Elite']
product_nouns = ['Kipas', 'Lampu', 'Kursi', 'Meja', 'Baju', 'Celana', 'Kopi', 'Biskuit', 'Tv', 'Kulkas']

# 1. Generate Stores (500 stores)
stores = []
for i in range(1, 501):
    stores.append({
        'store_id': i,
        'store_name': f"Toko {random.choice(cities)} {i}",
        'city': random.choice(cities),
        'region': random.choice(regions)
    })

with open('data/raw/stores.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['store_id', 'store_name', 'city', 'region'])
    writer.writeheader()
    writer.writerows(stores)
print("SUCCESS: Berhasil membuat data/raw/stores.csv (500 baris)")

# 2. Generate Products (1,000 products)
products = []
for i in range(1, 1001):
    cost = round(random.uniform(5.0, 500.0), 2)
    # Masukkan anomali: 2% produk memiliki cost_price negatif
    if random.random() < 0.02:
        cost = -cost
        
    products.append({
        'product_id': i,
        'product_name': f"{random.choice(product_adjectives)} {random.choice(product_nouns)} Model-{i}",
        'category': random.choice(categories),
        'cost_price': cost,
        'unit_price': round(abs(cost) * random.uniform(1.2, 1.8), 2)
    })

with open('data/raw/products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'product_name', 'category', 'cost_price', 'unit_price'])
    writer.writeheader()
    writer.writerows(products)
print("SUCCESS: Berhasil membuat data/raw/products.csv (1.000 baris - mengandung anomali)")

# 3. Generate Orders & Order Items (5,000 baris)
NUM_ORDERS = 5000
orders = []
order_items = []
start_date = datetime(2022, 1, 1)

for i in range(1, NUM_ORDERS + 1):
    o_date = start_date + timedelta(days=random.randint(0, 1400))
    # Pola Musiman: Volume belanja naik di Q4 (Nov-Des)
    if o_date.month in [11, 12] and random.random() < 0.3:
        o_date = o_date - timedelta(days=random.randint(1, 30))
            
    # Masukkan anomali: 1% tanggal order di luar range (tahun 1970 atau 2030)
    order_date_str = o_date.strftime('%Y-%m-%d')
    if random.random() < 0.01:
        order_date_str = random.choice(['1970-01-01', '2030-12-31'])
        
    # Masukkan anomali: 1.5% order tidak memiliki store_id (kosong)
    s_id = str(random.randint(1, 500))
    if random.random() < 0.015:
        s_id = ''

    orders.append({
        'order_id': i,
        'order_date': order_date_str,
        'customer_id': random.randint(1, 150000),
        'store_id': s_id,
        'salesperson_id': random.randint(1, 2000)
    })
    
    num_items = random.randint(1, 3)
    for j in range(num_items):
        qty = random.randint(1, 10)
        # Masukkan anomali: 1% qty adalah negatif
        if random.random() < 0.01:
            qty = -qty
            
        order_items.append({
            'item_id': len(order_items) + 1,
            'order_id': i,
            'product_id': random.randint(1, 1000),
            'quantity': qty
        })

# Masukkan anomali: Duplikat order items (0.5% duplikat penuh)
df_len = len(order_items)
num_dupes = int(df_len * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(order_items, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['item_id'] = len(order_items) + 1
        order_items.append(new_item)

with open('data/raw/orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'order_date', 'customer_id', 'store_id', 'salesperson_id'])
    writer.writeheader()
    writer.writerows(orders)

with open('data/raw/order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['item_id', 'order_id', 'product_id', 'quantity'])
    writer.writeheader()
    writer.writerows(order_items)

print(f"SUCCESS: Berhasil membuat data/raw/orders.csv ({len(orders)} baris - mengandung anomali)")
print(f"SUCCESS: Berhasil membuat data/raw/order_items.csv ({len(order_items)} baris - mengandung anomali)")
print("Proses pembuatan raw data selesai!")
