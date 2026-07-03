# ETL & SQL Analytics Tutorial - Enterprise Sales Analytics

Tutorial ini akan memandu Anda melakukan proses Extract, Transform, Load (ETL) data mentah, menangani anomali data menggunakan Python Pandas, memuatnya ke PostgreSQL, melakukan analisis SQL, dan membangun visualisasi di Power BI.

---

## 1. Tahap ETL: Pembersihan Anomali Data (Python)

Pada data mentah (`data/raw/`), terdapat beberapa anomali sengaja yang disisipkan:
- **`products.csv`**: Beberapa item memiliki `cost_price` negatif.
- **`orders.csv`**: Kolom `store_id` berisi nilai kosong (`NaN`) dan beberapa `order_date` tidak berada dalam rentang logis (tahun 1970 atau 2030).
- **`order_items.csv`**: Kolom `quantity` bernilai negatif dan baris data duplikat penuh.

Buat file baru bernama `etl_process.py` di folder ini dan jalankan kode berikut untuk membersihkan data:

```python
import pandas as pd
import numpy as np

# Load Data Mentah
df_stores = pd.read_csv('data/raw/stores.csv')
df_products = pd.read_csv('data/raw/products.csv')
df_orders = pd.read_csv('data/raw/orders.csv')
df_items = pd.read_csv('data/raw/order_items.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan tabel Products
# Masalah: cost_price negatif
# Solusi: Ubah ke nilai absolut (positif)
bad_costs = df_products[df_products['cost_price'] < 0]
print(f"Menangani {len(bad_costs)} baris cost_price negatif di Products.")
df_products['cost_price'] = df_products['cost_price'].abs()

# 2. Bersihkan tabel Orders
# Masalah A: store_id bernilai NULL/NaN (Melanggar constraint database)
# Solusi A: Drop baris yang tidak memiliki store_id karena transaksi tanpa toko tidak valid
null_stores = df_orders[df_orders['store_id'].isna()]
print(f"Menangani {len(null_stores)} baris store_id kosong (NaN) di Orders (di-drop).")
df_orders = df_orders.dropna(subset=['store_id'])
df_orders['store_id'] = df_orders['store_id'].astype(int) # Pastikan integer

# Masalah B: Tanggal di luar range 2022-2025 (1970 dan 2030)
# Solusi B: Filter transaksi hanya untuk rentang 2022-01-01 s/d 2025-12-31
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
bad_dates = df_orders[(df_orders['order_date'] < '2022-01-01') | (df_orders['order_date'] > '2025-12-31')]
print(f"Menangani {len(bad_dates)} baris tanggal transaksi tidak logis di Orders (di-drop).")
df_orders = df_orders[(df_orders['order_date'] >= '2022-01-01') & (df_orders['order_date'] <= '2025-12-31')]

# 3. Bersihkan tabel Order Items
# Masalah A: quantity bernilai negatif
# Solusi A: Ubah menjadi absolut (positif)
bad_qtys = df_items[df_items['quantity'] <= 0]
print(f"Menangani {len(bad_qtys)} baris quantity negatif di Order Items.")
df_items['quantity'] = df_items['quantity'].abs()

# Masalah B: Duplikat baris
# Solusi B: Hapus duplikat penuh berdasarkan item_id
dupes = df_items[df_items.duplicated(subset=['item_id'])]
print(f"Menghapus {len(dupes)} baris data duplikat di Order Items.")
df_items = df_items.drop_duplicates(subset=['item_id'])

# Simpan Data Bersih ke Folder /data/processed/
df_stores.to_csv('data/processed/stores.csv', index=False)
df_products.to_csv('data/processed/products.csv', index=False)
df_orders.to_csv('data/processed/orders.csv', index=False)
df_items.to_csv('data/processed/order_items.csv', index=False)

print("--- ETL Sukses! Seluruh data bersih disimpan di data/processed/ ---")
```

---

## 2. Tahap Load & SQL Analytics (PostgreSQL)

### A. Load Data Bersih ke Database
1. Buat database `enterprise_sales` di PostgreSQL menggunakan script di `schema.sql`.
2. Gunakan perintah `COPY` atau tool import DBeaver untuk mengunggah CSV bersih dari `data/processed/` ke tabel masing-masing. Urutan impor:
   1. `stores.csv` -> tabel `stores`
   2. `products.csv` -> tabel `products`
   3. `orders.csv` -> tabel `orders`
   4. `order_items.csv` -> tabel `order_items`

### B. Kueri Analisis Utama (SQL)
Jalankan kueri berikut untuk menghitung kontribusi penjualan berdasarkan kategori produk dan mencari *Top 5 Products* per Kategori menggunakan **Window Function**:

```sql
WITH ProductRevenue AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(oi.quantity * p.unit_price) AS total_revenue,
        ROW_NUMBER() OVER(PARTITION BY p.category ORDER BY SUM(oi.quantity * p.unit_price) DESC) as rank_in_category
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT 
    category,
    product_name,
    total_revenue
FROM ProductRevenue
WHERE rank_in_category <= 5
ORDER BY category, total_revenue DESC;
```

---

## 3. Tahap Visualisasi (Power BI)

1. Buka **Power BI Desktop**, pilih **Get Data** -> **PostgreSQL Database** dan hubungkan ke host lokal Anda.
2. Impor keempat tabel: `stores`, `products`, `orders`, dan `order_items`.
3. Di tab **Model View**, buat relasi (Star Schema):
   - `stores[store_id]` $\rightarrow$ `orders[store_id]` ($1:\infty$)
   - `products[product_id]` $\rightarrow$ `order_items[product_id]` ($1:\infty$)
   - `orders[order_id]` $\rightarrow$ `order_items[order_id]` ($1:\infty$)
4. Buat tabel penanggalan dinamis menggunakan DAX:
   ```dax
   Calendar = CALENDARAUTO()
   ```
   Hubungkan `Calendar[Date]` $\rightarrow$ `orders[order_date]` ($1:\infty$).
5. Tulis DAX Measure untuk **YoY Revenue Growth**:
   ```dax
   Total Revenue = SUMX(order_items, order_items[quantity] * RELATED(products[unit_price]))
   
   Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))
   
   YoY Revenue Growth = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)
   ```
6. Susun visualisasi dasbor bertema gelap dengan aksen Neon Blue & Teal sesuai portofolio.
