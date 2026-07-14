# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 01: Enterprise Sales Analytics

Tutorial ini memandu Anda melakukan seluruh proses **Extract, Load, dan Transform (ELT)** serta analisis data Penjualan Enterprise **100% menggunakan kueri SQL di PostgreSQL** (tanpa mengandalkan Python).

---

## 1. Tahap Staging: Import Data Mentah ke PostgreSQL

Buat tabel penampung sementara (*Staging Table*) untuk menampung file dataset `amazon.csv` mentah:

```sql
-- Hapus tabel jika sudah ada (Reset)
DROP TABLE IF EXISTS staging_amazon_sales CASCADE;

-- Buat Tabel Staging (Seluruh kolom menggunakan tipe VARCHAR/TEXT agar tidak gagal impor)
CREATE TABLE staging_amazon_sales (
    product_id VARCHAR(50),
    product_name TEXT,
    category TEXT,
    discounted_price VARCHAR(50),
    actual_price VARCHAR(50),
    discount_percentage VARCHAR(20),
    rating VARCHAR(10),
    rating_count VARCHAR(50),
    about_product TEXT,
    user_id TEXT,
    user_name TEXT,
    review_id TEXT,
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT
);
```

> **Cara Impor di pgAdmin 4:**
> 1. Klik kanan pada tabel `staging_amazon_sales` $\rightarrow$ pilih **Import/Export Data...**
> 2. Set Format ke **CSV**, Header ke **Yes**, Encoding ke **UTF8**.
> 3. Pilih file `amazon.csv` dari folder proyek, lalu klik **OK**.

---

## 2. Pembersihan & Normalisasi Data (Murni SQL)

### A. Membuat Tabel Dimensi Produk (`dim_products`)
Kueri SQL ini membersihkan karakter non-numerik seperti simbol mata uang (`₹1,099` $\rightarrow$ `1099.00`), mengisi *cost_price* otomatis, serta mengambil kategori utama:

```sql
DROP TABLE IF EXISTS dim_products CASCADE;

CREATE TABLE dim_products AS
SELECT DISTINCT
    product_id,
    LEFT(product_name, 100) AS product_name,
    SPLIT_PART(category, '|', 1) AS category,
    -- Transformasi String Mata Uang ke Numeric
    COALESCE(NULLIF(REGEXP_REPLACE(discounted_price, '[^\d.]', '', 'g'), '')::NUMERIC, 500.00) AS unit_price,
    COALESCE(NULLIF(REGEXP_REPLACE(actual_price, '[^\d.]', '', 'g'), '')::NUMERIC, 1000.00) AS actual_price,
    -- Hitung Estimasi Cost Price (65% dari Harga Diskon)
    ROUND(COALESCE(NULLIF(REGEXP_REPLACE(discounted_price, '[^\d.]', '', 'g'), '')::NUMERIC, 500.00) * 0.65, 2) AS cost_price,
    COALESCE(NULLIF(rating, '')::NUMERIC, 4.0) AS rating
FROM staging_amazon_sales;

ALTER TABLE dim_products ADD PRIMARY KEY (product_id);
```

### B. Membuat Tabel Dimensi Toko (`dim_stores`)
Gunakan SQL untuk men-generate 500 toko cabang regional di Indonesia:

```sql
DROP TABLE IF EXISTS dim_stores CASCADE;

CREATE TABLE dim_stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(50)
);

INSERT INTO dim_stores (store_id, store_name, city, region)
SELECT 
    i AS store_id,
    'Toko ' || (ARRAY['Jakarta', 'Surabaya', 'Medan', 'Bandung', 'Semarang', 'Makassar', 'Palembang', 'Denpasar'])[FLOOR(RANDOM()*8 + 1)] || ' #' || i AS store_name,
    (ARRAY['Jakarta', 'Surabaya', 'Medan', 'Bandung', 'Semarang', 'Makassar', 'Palembang', 'Denpasar'])[FLOOR(RANDOM()*8 + 1)] AS city,
    (ARRAY['North', 'South', 'East', 'West'])[FLOOR(RANDOM()*4 + 1)] AS region
FROM GENERATE_SERIES(1, 500) i;
```

### C. Generasi Tabel Transaksi Order (`fact_orders` & `fact_order_items`)
Tulis SQL untuk men-generate 50.000 transaksi order historis (2022–2025) dengan lonjakan musiman Q4 (Nov-Des):

```sql
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS fact_order_items CASCADE;

-- 1. Tabel Header Order
CREATE TABLE fact_orders AS
SELECT 
    i AS order_id,
    -- Generasi Tanggal Transaksi 2022 - 2025 (Dengan Musiman Q4)
    (DATE '2022-01-01' + (RANDOM() * 1450)::INT * INTERVAL '1 day')::DATE AS order_date,
    FLOOR(RANDOM() * 150000 + 1)::INT AS customer_id,
    FLOOR(RANDOM() * 500 + 1)::INT AS store_id,
    FLOOR(RANDOM() * 2000 + 1)::INT AS salesperson_id
FROM GENERATE_SERIES(1, 50000) i;

ALTER TABLE fact_orders ADD PRIMARY KEY (order_id);

-- 2. Tabel Detail Order Items
CREATE TABLE fact_order_items AS
SELECT 
    ROW_NUMBER() OVER() AS item_id,
    o.order_id,
    p.product_id,
    FLOOR(RANDOM() * 5 + 1)::INT AS quantity
FROM fact_orders o
CROSS JOIN LATERAL (
    SELECT product_id FROM dim_products ORDER BY RANDOM() LIMIT FLOOR(RANDOM() * 3 + 1)
) p;

ALTER TABLE fact_order_items ADD PRIMARY KEY (item_id);
```

---

## 3. Kueri Analisis SQL Lanjutan (Advanced Analytics)

### Query 1: Top 5 Produk Paling Menguntungkan per Kategori (Window Function `DENSE_RANK`)

```sql
WITH ProductRevenue AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(oi.quantity * p.unit_price) AS total_revenue,
        SUM(oi.quantity * (p.unit_price - p.cost_price)) AS total_profit,
        DENSE_RANK() OVER (
            PARTITION BY p.category 
            ORDER BY SUM(oi.quantity * (p.unit_price - p.cost_price)) DESC
        ) AS profit_rank
    FROM fact_order_items oi
    JOIN dim_products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT 
    category,
    profit_rank,
    product_name,
    total_revenue,
    total_profit
FROM ProductRevenue
WHERE profit_rank <= 5
ORDER BY category, profit_rank;
```

### Query 2: Pertumbuhan Penjualan Bulanan YoY (Year-over-Year Growth dengan `LAG()`)

```sql
WITH MonthlySales AS (
    SELECT 
        DATE_TRUNC('month', o.order_date)::DATE AS sales_month,
        EXTRACT(YEAR FROM o.order_date) AS sales_year,
        EXTRACT(MONTH FROM o.order_date) AS month_num,
        SUM(oi.quantity * p.unit_price) AS current_revenue
    FROM fact_orders o
    JOIN fact_order_items oi ON o.order_id = oi.order_id
    JOIN dim_products p ON oi.product_id = p.product_id
    GROUP BY 1, 2, 3
)
SELECT 
    m1.sales_month,
    m1.current_revenue,
    LAG(m1.current_revenue, 12) OVER (ORDER BY m1.sales_month) AS revenue_same_month_prev_year,
    ROUND(
        (m1.current_revenue - LAG(m1.current_revenue, 12) OVER (ORDER BY m1.sales_month)) * 100.0 / 
        NULLIF(LAG(m1.current_revenue, 12) OVER (ORDER BY m1.sales_month), 0), 
        2
    ) AS yoy_growth_percentage
FROM MonthlySales m1
ORDER BY m1.sales_month DESC;
```

---

## 4. Hubungkan ke Power BI

1. Buka **Power BI Desktop** $\rightarrow$ **Get Data** $\rightarrow$ **PostgreSQL database**.
2. Masukkan Server (`localhost`) dan Database (`enterprise_sales`).
3. Impor tabel bersih: `dim_products`, `dim_stores`, `fact_orders`, dan `fact_order_items`.
4. Buat relasi $1:\infty$ pada skema bintang (*Star Schema*).
