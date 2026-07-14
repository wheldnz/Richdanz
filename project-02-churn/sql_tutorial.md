# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 02: Customer Churn Analytics

Tutorial ini memandu Anda melakukan seluruh proses **ELT dan Analisis Churn Pelanggan** murni menggunakan kueri SQL di PostgreSQL.

---

## 1. Staging Table: Impor Data IBM Telco Churn

```sql
DROP TABLE IF EXISTS staging_telco_churn CASCADE;

CREATE TABLE staging_telco_churn (
    customerID VARCHAR(50),
    gender VARCHAR(20),
    SeniorCitizen VARCHAR(10),
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure VARCHAR(10),
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(30),
    InternetService VARCHAR(30),
    OnlineSecurity VARCHAR(30),
    OnlineBackup VARCHAR(30),
    DeviceProtection VARCHAR(30),
    TechSupport VARCHAR(30),
    StreamingTV VARCHAR(30),
    StreamingMovies VARCHAR(30),
    Contract VARCHAR(30),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(50),
    MonthlyCharges VARCHAR(50),
    TotalCharges VARCHAR(50),
    Churn VARCHAR(10)
);
```

> **Impor File:** Impor `WA_Fn-UseC_-Telco-Customer-Churn.csv` ke dalam `staging_telco_churn` melalui pgAdmin GUI.

---

## 2. Pembersihan & Generasi Data Historis (Murni SQL)

### A. Membuat Tabel Dimensi Pelanggan (`dim_customers`)
Kueri ini menghitung `signup_date` secara otomatis dari kolom `tenure` (bulan) dan mengelompokkan pelanggan ke dalam **Tenure Buckets**:

```sql
DROP TABLE IF EXISTS dim_customers CASCADE;

CREATE TABLE dim_customers AS
SELECT 
    customerID AS customer_id,
    gender,
    SeniorCitizen::INT AS is_senior_citizen,
    Partner AS has_partner,
    Dependents AS has_dependents,
    tenure::INT AS tenure_months,
    -- Hitung Tanggal Signup Otomatis dari Tenure
    (DATE '2025-06-30' - (tenure::INT || ' months')::INTERVAL)::DATE AS signup_date,
    -- Tenure Bucket Categorization
    CASE 
        WHEN tenure::INT <= 12 THEN '1. 0 - 12 Bulan'
        WHEN tenure::INT <= 24 THEN '2. 13 - 24 Bulan'
        WHEN tenure::INT <= 48 THEN '3. 25 - 48 Bulan'
        ELSE '4. > 48 Bulan'
    END AS tenure_bucket,
    Contract AS contract_type,
    PaymentMethod AS payment_method,
    COALESCE(NULLIF(REGEXP_REPLACE(MonthlyCharges, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS monthly_charges,
    COALESCE(NULLIF(REGEXP_REPLACE(TotalCharges, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS total_charges,
    Churn AS churn_status
FROM staging_telco_churn
WHERE customerID IS NOT NULL AND customerID != '';

ALTER TABLE dim_customers ADD PRIMARY KEY (customer_id);
```

### B. Generasi Log Historis Penggunaan Otomatis (`fact_usage_logs`)
SQL ini menggunakan `GENERATE_SERIES()` untuk memproduksi log aktivitas login bulanan. Jika pelanggan `Churn = 'Yes'`, aktivitas login akan otomatis menurun drastis di 3 bulan terakhir:

```sql
DROP TABLE IF EXISTS fact_usage_logs CASCADE;

CREATE TABLE fact_usage_logs AS
SELECT 
    ROW_NUMBER() OVER() AS log_id,
    c.customer_id,
    (c.signup_date + (m.month_idx || ' months')::INTERVAL)::DATE AS login_date,
    CASE 
        WHEN c.churn_status = 'Yes' AND m.month_idx >= (c.tenure_months - 3) THEN FLOOR(RANDOM() * 8 + 1)::INT
        ELSE FLOOR(RANDOM() * 45 + 15)::INT
    END AS feature_clicks
FROM dim_customers c
CROSS JOIN LATERAL GENERATE_SERIES(0, GREATEST(c.tenure_months - 1, 0)) AS m(month_idx);

ALTER TABLE fact_usage_logs ADD PRIMARY KEY (log_id);
```

### C. Generasi Log Tiket Keluhan Otomatis (`fact_support_tickets`)

```sql
DROP TABLE IF EXISTS fact_support_tickets CASCADE;

CREATE TABLE fact_support_tickets AS
SELECT 
    ROW_NUMBER() OVER() AS ticket_id,
    c.customer_id,
    (c.signup_date + (RANDOM() * c.tenure_months * 30)::INT * INTERVAL '1 day')::DATE AS ticket_date,
    (ARRAY['Teknis - Konektivitas', 'Teknis - Lambat', 'Tagihan - Pembayaran', 'Akun - Fitur'])[FLOOR(RANDOM()*4 + 1)] AS category,
    CASE WHEN c.churn_status = 'Yes' THEN FLOOR(RANDOM() * 68 + 4)::INT ELSE FLOOR(RANDOM() * 12 + 1)::INT END AS resolution_time_hours
FROM dim_customers c
CROSS JOIN LATERAL (
    SELECT generate_series(1, CASE WHEN c.churn_status = 'Yes' THEN FLOOR(RANDOM() * 3 + 1)::INT ELSE 1 END)
) t;

ALTER TABLE fact_support_tickets ADD PRIMARY KEY (ticket_id);
```

---

## 3. Kueri Analisis Churn SQL

### Query 1: Menghitung Rasio Churn & Hilangnya Pendapatan MRR per Jenis Kontrak

```sql
SELECT 
    contract_type,
    COUNT(customer_id) AS total_customers,
    COUNT(CASE WHEN churn_status = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn_status = 'Yes' THEN 1 END) * 100.0 / COUNT(customer_id), 2) AS churn_rate_percentage,
    ROUND(SUM(CASE WHEN churn_status = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS lost_mrr_revenue
FROM dim_customers
GROUP BY contract_type
ORDER BY churn_rate_percentage DESC;
```

### Query 2: Korelasi Durasi Penanganan Tiket Keluhan terhadap Churn

```sql
SELECT 
    c.churn_status,
    t.category,
    COUNT(t.ticket_id) AS total_tickets,
    ROUND(AVG(t.resolution_time_hours), 1) AS avg_resolution_time_hours
FROM dim_customers c
JOIN fact_support_tickets t ON c.customer_id = t.customer_id
GROUP BY c.churn_status, t.category
ORDER BY c.churn_status, avg_resolution_time_hours DESC;
```
