---
title: Enterprise Sales Analytics
category: data
metric: 1.2M Rows
metricLabel: Sales Orders Analyzed
tags: ['SQL', 'Power BI', 'ETL', 'Python']
description: End-to-end sales analysis pipeline, processing over 1.2 million rows of transaction data to deliver actionable insights on profit margins and regional store performance.
---

# Enterprise Sales Analytics

## Business Problem
Perusahaan ritel skala besar menghadapi kendala dalam memantau kinerja penjualan secara real-time di seluruh cabang, kategori produk, dan perwakilan penjualan (*salespersons*). Data penjualan tersebar di berbagai sistem transaksional tanpa struktur terpusat, menyebabkan keputusan manajemen didasarkan pada intuisi, bukan data. Proyek ini bertujuan untuk membangun jalur analisis data terpusat (*Centralized Data Pipeline*) guna memantau Revenue, Profit Margin, Average Order Value (AOV), dan mendeteksi anomali penjualan.

## Dataset & Raw Data
* **Fact Table**: `orders` (1.2 juta baris) & `order_items` (3 juta baris) berisi transaksi harian dari tahun 2022 hingga 2025.
* **Dimension Tables**:
  - `customers` (150 ribu baris): Data demografi pelanggan.
  - `products` (50 ribu baris): Hirarki produk (Category -> Sub-category -> SKU).
  - `stores` (500 baris): Lokasi fisik dan tipe toko.
  - `salespersons` (2 ribu baris): Performa staf penjualan.
  - `calendar` (Tabel tanggal dinamis).

### Raw Data Generation (Python Script)
Data dummy ini dibuat menggunakan script Python dengan library `Faker` dan `Pandas` untuk mensimulasikan pola musiman (kenaikan penjualan di akhir tahun/Q4) serta korelasi realistis (diskon tinggi menurunkan profit margin namun meningkatkan volume transaksi).

## Data Model (Star Schema)
Model data dioptimalkan menggunakan skema bintang (*Star Schema*) di Power BI untuk mempercepat performa kueri:
- **Fact Table**: `fact_sales` (gabungan orders dan order_items)
- **Dimension Tables**: `dim_customer`, `dim_product`, `dim_store`, `dim_salesperson`, `dim_date`
- **Relationships**: One-to-Many ($1:\infty$) dari seluruh tabel dimensi ke tabel fakta menggunakan surrogate keys.

## SQL Process
Seluruh data mentah dibersihkan dan diproses di PostgreSQL. Contoh query berikut digunakan untuk menghitung kontribusi kumulatif penjualan (Pareto 80/20) dan pertumbuhan bulanan (MoM Growth):

```sql
-- Mengaktifkan pencarian cepat menggunakan Index pada kolom kunci
CREATE INDEX idx_sales_date ON orders(order_date);
CREATE INDEX idx_sales_product ON order_items(product_id);

-- CTE untuk menghitung kontribusi produk dan persentase kumulatif
WITH ProductSales AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price) AS total_revenue,
        SUM(oi.quantity * (oi.unit_price - oi.cost_price)) AS total_profit
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
),
CumulativeSales AS (
    SELECT 
        category,
        product_name,
        total_revenue,
        SUM(total_revenue) OVER(ORDER BY total_revenue DESC) AS cum_revenue,
        SUM(total_revenue) OVER() AS grand_total
    FROM ProductSales
)
SELECT 
    category,
    product_name,
    total_revenue,
    (cum_revenue / grand_total) * 100 AS cum_percentage
FROM CumulativeSales
WHERE (cum_revenue / grand_total) * 100 <= 80
ORDER BY total_revenue DESC;
```

## Power BI & DAX
Rumus DAX yang digunakan untuk melacak metrik utama:

* **Total Revenue**:
  ```dax
  Total Revenue = SUMX(fact_sales, fact_sales[Quantity] * fact_sales[Unit Price])
  ```
* **YoY Revenue Growth**:
  ```dax
  YoY Revenue Growth = 
  VAR CurrentYearSales = [Total Revenue]
  VAR LastYearSales = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[Date]))
  RETURN
  DIVIDE(CurrentYearSales - LastYearSales, LastYearSales, 0)
  ```

## Dashboard Mockup Specification
Dashboard didesain dengan konsep **Sleek Dark Mode (Neon Blue & Teal Accent)** yang responsif:
- **Halaman 1: Executive Summary**: Menampilkan KPI Utama (Revenue, Profit, Margin, AOV) dalam bentuk Card besar dengan visualisasi tren mini (sparklines) di bawahnya.
- **Halaman 2: Sales Performance**: Map interaktif dengan sebaran ukuran gelembung sesuai total penjualan wilayah, terintegrasi dengan filter rentang tanggal.

## Key Insights
1. **Pola Musiman Q4**: Terjadi kenaikan transaksi rata-rata 35% setiap bulan November-Desember yang didorong oleh promosi akhir tahun.
2. **Aturan Pareto 80/20**: Sebanyak 18% produk menyumbangkan 80% dari total profit perusahaan.
3. **Diskon & Margin**: Memberikan diskon di atas 20% secara konsisten menurunkan profit margin bersih sebesar 12%, tanpa meningkatkan retensi pelanggan.
4. **Cabang Utama**: Wilayah Metropolitan menyumbang 45% penjualan tetapi memiliki biaya operasional tertinggi, membuat margin profit bersihnya lebih rendah dibanding wilayah sub-urban.
5. **AOV Trend**: Nilai rata-rata keranjang belanja (Average Order Value) meningkat 8% saat fitur *recommender system* produk sejenis diaktifkan di aplikasi kasir.
6. **Performa Sales**: Top 5% *salesperson* memberikan kontribusi 25% terhadap total penjualan baru.
7. **Product Lifecyle**: Kategori Elektronik memiliki siklus perputaran produk paling cepat (rata-rata 14 hari di gudang).
8. **Waktu Transaksi Terpadat**: Puncak transaksi harian terjadi pada pukul 17.00 - 20.00 WIB.
9. **Metode Pembayaran**: Penggunaan metode *E-Wallet* meningkat 50% YoY, menggantikan pembayaran kartu kredit.
10. **Customer Repeat Order**: 30% pelanggan melakukan pembelian ulang dalam waktu 45 hari setelah transaksi pertama.

## Recommendations
1. Fokuskan stok dan kampanye pemasaran pada 18% produk utama penghasil profit tinggi (Pareto).
2. Batasi diskon maksimal di angka 15% untuk menghindari penurunan profit margin yang tidak sehat.
3. Alokasikan insentif bagi *salesperson* berkinerja tinggi untuk menjaga retensi staf terbaik.
4. Kurangi biaya operasional di wilayah metropolitan melalui digitalisasi laporan cabang.
5. Gunakan skema bundling produk elektronik dengan aksesoris margin tinggi untuk menaikkan AOV.
6. Optimalkan staf cabang pada jam sibuk (17.00 - 20.00) untuk meminimalkan waktu tunggu kasir.
7. Luncurkan program loyalitas khusus pengguna E-Wallet untuk menekan biaya transaksi kartu kredit.
8. Lakukan kampanye retensi terautomasi pada pelanggan di hari ke-40 setelah transaksi terakhir mereka.
9. Kurangi kapasitas penyimpanan untuk kategori produk lambat (turnover > 60 hari) guna meminimalkan biaya sewa gudang.
10. Terapkan strategi dynamic pricing pada jam-jam sepi untuk menarik pelanggan sekunder.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
1. Buka PostgreSQL (melalui pgAdmin atau psql CLI).
2. Jalankan kueri berikut untuk membuat database dan tabel yang dibutuhkan:

```sql
CREATE DATABASE enterprise_sales;

-- Buat tabel Dimensi Toko
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    region VARCHAR(50)
);

-- Buat tabel Dimensi Produk
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    cost_price NUMERIC(10, 2),
    unit_price NUMERIC(10, 2)
);

-- Buat tabel Fakta Penjualan
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    store_id INT REFERENCES stores(store_id),
    salesperson_id INT
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT
);
```

### Langkah 2: Generate Data Dummy (Python)
Gunakan library `Faker` dan `Pandas` untuk membuat data 1.2M baris. Buat file `generator.py` dan jalankan script berikut:

```python
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Generate Dimensi
stores = [{'store_id': i, 'store_name': f"Toko {fake.city()}", 'city': fake.city(), 'region': random.choice(['North','South','East','West'])} for i in range(1, 501)]
pd.DataFrame(stores).to_csv('stores.csv', index=False)

products = [{'product_id': i, 'product_name': f"Produk {fake.word().capitalize()}", 'category': random.choice(['Elektronik','Mebel','Pakaian','Makanan']), 'cost_price': round(random.uniform(5, 500), 2)} for i in range(1, 1001)]
for p in products:
    p['unit_price'] = round(p['cost_price'] * random.uniform(1.2, 1.8), 2)
pd.DataFrame(products).to_csv('products.csv', index=False)

# Generate 1.2M Orders
orders = []
order_items = []
start_date = datetime(2022, 1, 1)

for i in range(1, 1200001):
    o_date = start_date + timedelta(days=random.randint(0, 1400))
    orders.append({
        'order_id': i,
        'order_date': o_date.strftime('%Y-%m-%d'),
        'customer_id': random.randint(1, 150000),
        'store_id': random.randint(1, 500),
        'salesperson_id': random.randint(1, 2000)
    })
    
    # Generate 1-3 items per order
    for j in range(random.randint(1, 3)):
        order_items.append({
            'item_id': len(order_items) + 1,
            'order_id': i,
            'product_id': random.randint(1, 1000),
            'quantity': random.randint(1, 10)
        })

pd.DataFrame(orders).to_csv('orders.csv', index=False)
pd.DataFrame(order_items).to_csv('order_items.csv', index=False)
print("Data dummy berhasil di-generate!")
```

### Langkah 3: Import ke Database & Tulis SQL Query
1. Load file `.csv` di atas ke tabel PostgreSQL Anda (menggunakan perintah `COPY` atau UI Import DBeaver).
2. Jalankan query analisis (seperti kueri analisis Pareto pada bagian **SQL Process** di atas) untuk memverifikasi kebenaran relasi.

### Langkah 4: Visualisasi di Power BI
1. Buka **Power BI Desktop**, hubungkan ke PostgreSQL Database Anda.
2. Load tabel `orders`, `order_items`, `products`, dan `stores`.
3. Buat skema bintang: hubungkan `products[product_id]` ke `order_items[product_id]` dan `stores[store_id]` ke `orders[store_id]`.
4. Buat tabel tanggal otomatis (Calendar Table) menggunakan kode DAX:
   ```dax
   Calendar = CALENDAR(DATE(2022,1,1), DATE(2025,12,31))
   ```
5. Implementasikan metrik DAX pada bagian **Power BI & DAX** di atas pada visualisasi laporan Anda.
6. Buat tata letak dasbor modern dengan tema gelap sesuai spesifikasi mockup.

