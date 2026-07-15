# Master Tutorial Unified: Enterprise Sales & Multi-Channel P&L (PostgreSQL & Power BI)

Tutorial ini memandu Anda membangun **Dashboard Terintegrasi (Enterprise Sales + Multi-Channel P&L)** di mana data transaksi Penjualan Produk Amazon dan Laba-Rugi (P&L) **16 Brand Partners, 9 Infinix Service Centers, dan 50 Retail Partners** saling sinkron secara real-time.

---

## 🐘 BAGIAN 1: Pembuatan Database & Skema Unified di PostgreSQL (pgAdmin)

### Langkah 1: Jalankan Script DDL Skema Unified
Buka **pgAdmin 4** $\rightarrow$ Query Tool pada database `db_enterprise_sales`, lalu jalankan:

```sql
DROP TABLE IF EXISTS fact_order_items CASCADE;
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS fact_pl_monthly CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_stores CASCADE;

-- 1. Dimensi Produk Amazon
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    actual_price NUMERIC(12, 2) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    rating NUMERIC(3, 2)
);

-- 2. Dimensi Toko & Mitra Usaha (Connecting Bridge)
CREATE TABLE dim_stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    channel_type VARCHAR(50) NOT NULL, -- 'Brand Partner', 'Infinix Service Center', 'Retail Partner'
    city VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- 3. Header Transaksi Sales
CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL,
    store_id INT NOT NULL REFERENCES dim_stores(store_id),
    salesperson_id INT NOT NULL
);

-- 4. Detail Item Transaksi Sales
CREATE TABLE fact_order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES fact_orders(order_id) ON DELETE CASCADE,
    product_id VARCHAR(50) NOT NULL REFERENCES dim_products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0)
);

-- 5. Tabel Fakta P&L Bulanan Multi-Channel
CREATE TABLE fact_pl_monthly (
    pl_id SERIAL PRIMARY KEY,
    store_id INT NOT NULL REFERENCES dim_stores(store_id),
    month_date DATE NOT NULL,
    gross_revenue_idr NUMERIC(15, 2) NOT NULL,
    cogs_idr NUMERIC(15, 2) NOT NULL,
    gross_profit_idr NUMERIC(15, 2) NOT NULL,
    operating_expenses_idr NUMERIC(15, 2) NOT NULL,
    net_profit_idr NUMERIC(15, 2) NOT NULL,
    net_profit_margin_pct NUMERIC(5, 2) NOT NULL
);
```

### Langkah 2: Impor Data Toko Unified (`stores_unified.csv`)
Impor file `project-01-sales/data/processed/stores_unified.csv` ke dalam tabel `dim_stores` dan file `pl_multi_channel_clean.csv` ke dalam tabel `fact_pl_monthly`.

---

## 📊 BAGIAN 2: Pengolahan & Model Relasi Terintegrasi di Power BI

### Langkah 1: Tarik Semua Tabel ke Power BI
Buka **Power BI Desktop** $\rightarrow$ `Get Data` $\rightarrow$ `PostgreSQL` $\rightarrow$ Masukkan Server: `localhost:5432`, Database: `db_enterprise_sales`.
Pilih 5 tabel utama:
- ☑️ `dim_products`
- ☑️ `dim_stores`
- ☑️ `fact_orders`
- ☑️ `fact_order_items`
- ☑️ `fact_pl_monthly`

### Langkah 2: Verifikasi Model Skema Bintang Terintegrasi (Model View)
Di ikon **Model View** (kiri), pastikan **`dim_stores`** berada di tengah memfilter kedua tabel fakta sekaligus:

```
                  +-------------------+
                  |   dim_products    |
                  +---------+---------+
                            | (1:*)
                            v
+-----------------+   +-----+-------------+   +-------------------+
|   dim_stores    |-->| fact_order_items  |<--|    fact_orders    |
+--------+--------+   +-------------------+   +-------------------+
         | (1:*)
         v
+--------+--------+
| fact_pl_monthly |
+-----------------+
```

Garis relasi yang terbentuk:
1. `dim_stores (store_id)` (1) $\rightarrow$ (*) `fact_orders (store_id)`
2. `dim_stores (store_id)` (1) $\rightarrow$ (*) `fact_pl_monthly (store_id)`
3. `dim_products (product_id)` (1) $\rightarrow$ (*) `fact_order_items (product_id)`
4. `fact_orders (order_id)` (1) $\rightarrow$ (*) `fact_order_items (order_id)`

---

## 🧮 BAGIAN 3: Rumus DAX Finansial & Interaksi Filter

Buat tabel `_Measures` dan isi rumus DAX sinkron berikut:

```dax
-- 1. Penjualan Retail Amazon
Retail Sales Revenue = SUMX(fact_order_items, fact_order_items[quantity] * RELATED(dim_products[unit_price]))

-- 2. Keuangan P&L Channel
Channel Gross Revenue = SUM(fact_pl_monthly[gross_revenue_idr])
Channel COGS = SUM(fact_pl_monthly[cogs_idr])
Channel Gross Profit = [Channel Gross Revenue] - [Channel COGS]
Channel Operating Expenses = SUM(fact_pl_monthly[operating_expenses_idr])
Channel Net Profit = [Channel Gross Profit] - [Channel Operating Expenses]
Channel Net Margin % = DIVIDE([Channel Net Profit], [Channel Gross Revenue], 0)
```

---

## 🎨 BAGIAN 4: Mendesain Visual Dashboard 2-Halaman Terintegrasi

### Halaman 1 (Page 1): Executive Product & Retail Performance
- **Slicer Utama**: `dim_stores[channel_type]` (Brand Partner, Infinix Service Center, Retail Partner).
- **KPI Cards**: `Retail Sales Revenue`, `Total Orders`, `Top Product Category`.
- **Bar Chart**: Revenue per Produk Kategori.
- **Table**: List Toko/Mitra Teratas beserta Omzet Retail.

### Halaman 2 (Page 2): Multi-Channel P&L Financial Report
- **Waterfall Chart**: P&L Flow (`Channel Gross Revenue` $\rightarrow$ `COGS` $\rightarrow$ `OpEx` $\rightarrow$ `Channel Net Profit`).
- **Matrix Table P&L**: Baris `dim_stores[channel_type]` $\rightarrow$ `dim_stores[store_name]` (Klik tombol **+** untuk mengekspansi 16 Brand Partners, 9 Infinix Service Centers, dan 50 Retail Partners).
- **Donut Chart**: Distribusi Net Profit per Channel Type.

---

### 🌟 Efek Ajaib Sinkronisasi:
Ketika Anda memilih filter **`"16 Brand Partners"`** di Slicer atas:
- **Page 1** akan menampilkan total penjualan produk retail yang terjadi di 16 Brand Partners tersebut.
- **Page 2** akan langsung menampilkan laporan Laba Rugi (Net Profit & Margin %) khusus untuk 16 Brand Partners tersebut!
