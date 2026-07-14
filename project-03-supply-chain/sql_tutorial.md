# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 03: Supply Chain Analytics

Tutorial ini memandu Anda melakukan **ELT & Normalisasi Skema Bintang (Star Schema)** pada dataset raksasa DataCo Supply Chain murni menggunakan SQL di PostgreSQL.

---

## 1. Staging Table: Impor Data Mentah DataCo

```sql
DROP TABLE IF EXISTS staging_dataco CASCADE;

CREATE TABLE staging_dataco (
    "Type" TEXT,
    "Days for shipping (real)" TEXT,
    "Days for shipment (scheduled)" TEXT,
    "Benefit per order" TEXT,
    "Sales per customer" TEXT,
    "Delivery Status" TEXT,
    "Late_delivery_risk" TEXT,
    "Category Id" TEXT,
    "Category Name" TEXT,
    "Customer City" TEXT,
    "Customer Country" TEXT,
    "Customer Fname" TEXT,
    "Customer Id" TEXT,
    "Customer Lname" TEXT,
    "Customer Segment" TEXT,
    "Order City" TEXT,
    "Order Country" TEXT,
    "order date (DateOrders)" TEXT,
    "Order Id" TEXT,
    "Order Region" TEXT,
    "Order Status" TEXT,
    "Product Card Id" TEXT,
    "Product Name" TEXT,
    "Product Price" TEXT,
    "Shipping Mode" TEXT
);
```

---

## 2. Normalisasi Skema Bintang (Star Schema) Murni SQL

### A. Dimensi Pelanggan (`dim_customers`)
```sql
DROP TABLE IF EXISTS dim_customers CASCADE;

CREATE TABLE dim_customers AS
SELECT DISTINCT
    "Customer Id" AS customer_id,
    "Customer Fname" AS first_name,
    "Customer Lname" AS last_name,
    "Customer City" AS city,
    "Customer Country" AS country,
    "Customer Segment" AS segment
FROM staging_dataco
WHERE "Customer Id" IS NOT NULL AND "Customer Id" != '';

ALTER TABLE dim_customers ADD PRIMARY KEY (customer_id);
```

### B. Dimensi Produk (`dim_products`)
```sql
DROP TABLE IF EXISTS dim_products CASCADE;

CREATE TABLE dim_products AS
SELECT DISTINCT
    "Product Card Id" AS product_id,
    "Category Id" AS category_id,
    "Category Name" AS category_name,
    "Product Name" AS product_name,
    ABS(COALESCE(NULLIF("Product Price", '')::NUMERIC, 0.0)) AS unit_price
FROM staging_dataco
WHERE "Product Card Id" IS NOT NULL AND "Product Card Id" != '';

ALTER TABLE dim_products ADD PRIMARY KEY (product_id);
```

### C. Tabel Fakta Pengiriman & Order (`fact_supply_chain_orders`)
SQL ini menghitung variansi lead time (`real_shipping_days - scheduled_shipping_days`) dan menentukan flag **OTIF (On-Time In-Full)**:

```sql
DROP TABLE IF EXISTS fact_supply_chain_orders CASCADE;

CREATE TABLE fact_supply_chain_orders AS
SELECT 
    ROW_NUMBER() OVER() AS fact_id,
    "Order Id" AS order_id,
    SPLIT_PART("order date (DateOrders)", ' ', 1)::DATE AS order_date,
    "Customer Id" AS customer_id,
    "Product Card Id" AS product_id,
    "Order Region" AS order_region,
    "Shipping Mode" AS shipping_mode,
    COALESCE(NULLIF("Sales per customer", '')::NUMERIC, 0.0) AS sales_amount,
    COALESCE(NULLIF("Benefit per order", '')::NUMERIC, 0.0) AS profit_amount,
    GREATEST("Days for shipping (real)"::INT, 0) AS real_shipping_days,
    "Days for shipment (scheduled)"::INT AS scheduled_shipping_days,
    -- Hitung Variansi Keterlambatan Hari
    ("Days for shipping (real)"::INT - "Days for shipment (scheduled)"::INT) AS lead_time_variance_days,
    "Late_delivery_risk"::INT AS late_delivery_risk,
    "Delivery Status" AS delivery_status,
    -- Penentuan Flag OTIF Murni di SQL
    CASE 
        WHEN "Delivery Status" = 'Shipping on time' AND "Late_delivery_risk"::INT = 0 THEN 1 
        ELSE 0 
    END AS is_otif
FROM staging_dataco
WHERE "Order Id" IS NOT NULL AND "Order Id" != '';

ALTER TABLE fact_supply_chain_orders ADD PRIMARY KEY (fact_id);
```

---

## 3. Kueri Analisis OTIF & Performa Logistik

### Query 1: Analisis Rasio OTIF % per Wilayah Pengiriman (*Order Region*)

```sql
SELECT 
    order_region,
    COUNT(fact_id) AS total_orders,
    SUM(is_otif) AS otif_orders,
    ROUND(SUM(is_otif) * 100.0 / COUNT(fact_id), 2) AS otif_rate_percentage,
    ROUND(AVG(lead_time_variance_days), 1) AS avg_delay_days,
    ROUND(SUM(CASE WHEN is_otif = 0 THEN profit_amount ELSE 0 END), 2) AS profit_at_risk_due_to_delays
FROM fact_supply_chain_orders
GROUP BY order_region
ORDER BY otif_rate_percentage ASC;
```

### Query 2: Evaluasi Kinerja Mode Pengiriman (*Shipping Mode*)

```sql
SELECT 
    shipping_mode,
    COUNT(fact_id) AS total_shipments,
    SUM(late_delivery_risk) AS late_deliveries,
    ROUND(SUM(late_delivery_risk) * 100.0 / COUNT(fact_id), 2) AS late_risk_percentage,
    ROUND(AVG(real_shipping_days), 1) AS avg_actual_days,
    ROUND(AVG(scheduled_shipping_days), 1) AS avg_target_days
FROM fact_supply_chain_orders
GROUP BY shipping_mode
ORDER BY late_risk_percentage DESC;
```
