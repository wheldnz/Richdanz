# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 06: Insurance Underwriting Analytics

Tutorial ini memandu Anda melakukan **ELT & Analisis Loss Ratio Aktuaria Asuransi** murni menggunakan kueri SQL di PostgreSQL.

---

## 1. Staging Table: Impor Data IBM Auto Insurance

```sql
DROP TABLE IF EXISTS staging_auto_insurance CASCADE;

CREATE TABLE staging_auto_insurance (
    Customer TEXT,
    State TEXT,
    "Customer Lifetime Value" TEXT,
    Response TEXT,
    Coverage TEXT,
    Education TEXT,
    "Effective To Date" TEXT,
    EmploymentStatus TEXT,
    Gender TEXT,
    Income TEXT,
    "Location Code" TEXT,
    "Marital Status" TEXT,
    "Monthly Premium Auto" TEXT,
    "Months Since Last Claim" TEXT,
    "Months Since Policy Inception" TEXT,
    "Number of Open Complaints" TEXT,
    "Number of Policies" TEXT,
    "Policy Type" TEXT,
    Policy TEXT,
    "Renew Offer Type" TEXT,
    "Sales Channel" TEXT,
    "Total Claim Amount" TEXT,
    "Vehicle Class" TEXT,
    "Vehicle Size" TEXT
);
```

---

## 2. Pembersihan & Normalisasi Skema Relasional (Murni SQL)

### A. Dimensi Nasabah (`dim_insurance_customers`)
```sql
DROP TABLE IF EXISTS dim_insurance_customers CASCADE;

CREATE TABLE dim_insurance_customers AS
SELECT DISTINCT
    Customer AS customer_id,
    State AS state,
    Gender AS gender,
    Education AS education,
    EmploymentStatus AS employment_status,
    COALESCE(NULLIF(Income, '')::NUMERIC, 0.0) AS income,
    "Marital Status" AS marital_status,
    COALESCE(NULLIF("Customer Lifetime Value", '')::NUMERIC, 0.0) AS customer_lifetime_value
FROM staging_auto_insurance;

ALTER TABLE dim_insurance_customers ADD PRIMARY KEY (customer_id);
```

### B. Dimensi Polis (`dim_policies`)
Menghitung `effective_start_date` dari `Months Since Policy Inception`:

```sql
DROP TABLE IF EXISTS dim_policies CASCADE;

CREATE TABLE dim_policies AS
SELECT DISTINCT
    'POL-' || Customer AS policy_id,
    Customer AS customer_id,
    "Policy Type" AS policy_type,
    Policy AS policy_name,
    Coverage AS coverage_level,
    ABS(COALESCE(NULLIF("Monthly Premium Auto", '')::NUMERIC, 0.0)) AS monthly_premium,
    COALESCE(NULLIF("Months Since Policy Inception", '')::INT, 12) AS months_in_force,
    "Vehicle Class" AS vehicle_class,
    "Vehicle Size" AS vehicle_size,
    (DATE '2025-06-30' - (COALESCE(NULLIF("Months Since Policy Inception", '')::INT, 12) || ' months')::INTERVAL)::DATE AS effective_start_date
FROM staging_auto_insurance;

ALTER TABLE dim_policies ADD PRIMARY KEY (policy_id);
```

### C. Tabel Fakta Klaim (`fact_insurance_claims`)
```sql
DROP TABLE IF EXISTS fact_insurance_claims CASCADE;

CREATE TABLE fact_insurance_claims AS
SELECT 
    'CLM-' || LPAD(ROW_NUMBER() OVER()::TEXT, 6, '0') AS claim_id,
    'POL-' || Customer AS policy_id,
    Customer AS customer_id,
    (DATE '2025-06-30' - (COALESCE(NULLIF("Months Since Last Claim", '')::INT, 3) || ' months')::INTERVAL)::DATE AS claim_date,
    ABS(COALESCE(NULLIF("Total Claim Amount", '')::NUMERIC, 0.0)) AS claim_amount,
    (ARRAY['Approved', 'Pending', 'Rejected'])[FLOOR(RANDOM()*3 + 1)] AS claim_status,
    (ARRAY['Kecelakaan Tabrakan', 'Kerusakan Bodi', 'Kerusakan Kaca', 'Pencurian', 'Bencana Alam'])[FLOOR(RANDOM()*5 + 1)] AS claim_reason
FROM staging_auto_insurance
WHERE COALESCE(NULLIF("Total Claim Amount", '')::NUMERIC, 0.0) > 0;

ALTER TABLE fact_insurance_claims ADD PRIMARY KEY (claim_id);
```

---

## 3. Kueri Analisis Aktuaria Loss Ratio SQL

### Query 1: Menghitung Loss Ratio Aktuaria % per Kelas Kendaraan (*Vehicle Class*)

```sql
SELECT 
    p.vehicle_class,
    COUNT(p.policy_id) AS total_policies,
    ROUND(SUM(p.monthly_premium * p.months_in_force), 2) AS total_earned_premium,
    ROUND(SUM(COALESCE(c.claim_amount, 0)), 2) AS total_claims_paid,
    -- Formula Loss Ratio: (Total Claim / Total Earned Premium) * 100
    ROUND(
        SUM(COALESCE(c.claim_amount, 0)) * 100.0 / 
        NULLIF(SUM(p.monthly_premium * p.months_in_force), 0), 
        2
    ) AS loss_ratio_percentage,
    CASE 
        WHEN SUM(COALESCE(c.claim_amount, 0)) * 100.0 / NULLIF(SUM(p.monthly_premium * p.months_in_force), 0) > 80.0 THEN 'HIGH RISK (Unprofitable)'
        WHEN SUM(COALESCE(c.claim_amount, 0)) * 100.0 / NULLIF(SUM(p.monthly_premium * p.months_in_force), 0) > 50.0 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK (Profitable)'
    END AS underwriting_status
FROM dim_policies p
LEFT JOIN fact_insurance_claims c ON p.policy_id = c.policy_id AND c.claim_status = 'Approved'
GROUP BY p.vehicle_class
ORDER BY loss_ratio_percentage DESC;
```

### Query 2: Analisis Loss Ratio per Negara Bagian (*State*) & Tingkat Proteksi (*Coverage*)

```sql
SELECT 
    cust.state,
    p.coverage_level,
    COUNT(p.policy_id) AS policy_count,
    ROUND(SUM(p.monthly_premium * p.months_in_force), 2) AS earned_premium,
    ROUND(SUM(COALESCE(c.claim_amount, 0)), 2) AS total_claim_amount,
    ROUND(
        SUM(COALESCE(c.claim_amount, 0)) * 100.0 / 
        NULLIF(SUM(p.monthly_premium * p.months_in_force), 0), 
        2
    ) AS loss_ratio_pct
FROM dim_policies p
JOIN dim_insurance_customers cust ON p.customer_id = cust.customer_id
LEFT JOIN fact_insurance_claims c ON p.policy_id = c.policy_id AND c.claim_status = 'Approved'
GROUP BY cust.state, p.coverage_level
ORDER BY cust.state, loss_ratio_pct DESC;
```
