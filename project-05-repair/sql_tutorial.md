# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 05: Claims & SLA Analytics

Tutorial ini memandu Anda melakukan **ELT & Analisis SLA Klaim Asuransi Perbaikan** murni menggunakan kueri SQL di PostgreSQL.
Fokus analisis: **Memantau 300+ klaim bulanan di 9 Mitra Asuransi, mengukur Resolution Rate, serta mengevaluasi Turnaround Time (TAT rata-rata 5-6 hari vs Target SLA 7 Hari).**

---

## 1. Staging Table: Impor Data Mentah Klaim (`claims_sla_raw.csv`)

```sql
DROP TABLE IF EXISTS staging_claims_sla CASCADE;

CREATE TABLE staging_claims_sla (
    claim_id TEXT,
    insurance_partner TEXT,
    service_center TEXT,
    brand TEXT,
    model TEXT,
    claim_date TEXT,
    approval_date TEXT,
    completion_date TEXT,
    turnaround_time_days TEXT,
    repair_cost TEXT, -- String masih ada 'Rp '
    status TEXT,
    sla_status TEXT,
    csat_rating TEXT
);

-- Impor file data/raw/claims_sla_raw.csv ke staging_claims_sla lewat pgAdmin Import / COPY command
```

---

## 2. Pembersihan & Transformasi Relasional Murni SQL

### A. Dimensi Mitra Asuransi (`dim_insurance_partners`)
```sql
DROP TABLE IF EXISTS dim_insurance_partners CASCADE;

CREATE TABLE dim_insurance_partners AS
SELECT 
    ROW_NUMBER() OVER(ORDER BY insurance_partner) AS partner_id,
    insurance_partner AS partner_name,
    7 AS sla_target_days
FROM (SELECT DISTINCT insurance_partner FROM staging_claims_sla WHERE insurance_partner IS NOT NULL AND insurance_partner != 'insurance_partner') sub;

ALTER TABLE dim_insurance_partners ADD PRIMARY KEY (partner_id);
```

### B. Dimensi Service Center (`dim_service_centers`)
```sql
DROP TABLE IF EXISTS dim_service_centers CASCADE;

CREATE TABLE dim_service_centers AS
SELECT 
    ROW_NUMBER() OVER(ORDER BY service_center) AS center_id,
    service_center AS center_name,
    SPLIT_PART(service_center, '- ', 2) AS city
FROM (SELECT DISTINCT service_center FROM staging_claims_sla WHERE service_center IS NOT NULL AND service_center != 'service_center') sub;

ALTER TABLE dim_service_centers ADD PRIMARY KEY (center_id);
```

### C. Tabel Fakta Klaim & SLA (`fact_claims_sla`)
Pembersihan string `Rp 1,500,000`, safe cast tanggal, dan penghitungan ulang otomatis TAT & SLA Adherence:

```sql
DROP TABLE IF EXISTS fact_claims_sla CASCADE;

CREATE TABLE fact_claims_sla AS
SELECT 
    s.claim_id,
    p.partner_id,
    c.center_id,
    s.brand AS device_brand,
    s.model AS device_model,
    s.claim_date::DATE AS claim_date,
    NULLIF(s.approval_date, '')::DATE AS approval_date,
    NULLIF(s.completion_date, '')::DATE AS completion_date,
    
    -- Hitung Ulang Turnaround Time (TAT) dalam Hari
    CASE 
        WHEN NULLIF(s.completion_date, '') IS NOT NULL THEN (NULLIF(s.completion_date, '')::DATE - s.claim_date::DATE)
        ELSE NULL 
    END AS turnaround_time_days,
    
    7 AS sla_target_days,
    
    -- Cleaning String Mata Uang 'Rp 1,250,000' -> 1250000.00
    COALESCE(NULLIF(REGEXP_REPLACE(s.repair_cost, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS repair_cost_idr,
    ROUND(COALESCE(NULLIF(REGEXP_REPLACE(s.repair_cost, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) * 0.65, 2) AS sparepart_cost_idr,
    
    s.status,
    
    -- Penentuan Status SLA (Met SLA vs Breached SLA)
    CASE 
        WHEN s.status = 'Pending' THEN 'In Progress'
        WHEN s.status = 'Rejected' THEN 'Rejected Claim'
        WHEN (NULLIF(s.completion_date, '')::DATE - s.claim_date::DATE) <= 7 THEN 'Met SLA'
        ELSE 'Breached SLA'
    END AS sla_status,
    
    COALESCE(NULLIF(s.csat_rating, '')::INT, 4) AS csat_rating

FROM staging_claims_sla s
JOIN dim_insurance_partners p ON s.insurance_partner = p.partner_name
JOIN dim_service_centers c ON s.service_center = c.center_name
WHERE s.claim_id IS NOT NULL AND s.claim_id != 'claim_id';

ALTER TABLE fact_claims_sla ADD PRIMARY KEY (claim_id);
```

---

## 3. Kueri Analisis Performa SLA & Turnaround Time (TAT)

### Query 1: Analisis Ringkasan SLA per Mitra Asuransi (Rata-Rata TAT 5-6 Hari)

```sql
SELECT 
    p.partner_name,
    COUNT(f.claim_id) AS total_claims,
    COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END) AS resolved_claims,
    
    -- Resolution Rate %
    ROUND(COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END) * 100.0 / COUNT(f.claim_id), 1) AS resolution_rate_pct,
    
    -- Rata-rata Turnaround Time (TAT)
    ROUND(AVG(f.turnaround_time_days), 2) AS avg_tat_days,
    
    -- SLA Adherence % (Persentase Klaim Selesai <= 7 Hari)
    ROUND(
        COUNT(CASE WHEN f.sla_status = 'Met SLA' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END), 0), 
        1
    ) AS sla_adherence_pct,
    
    -- Total Nilai Perbaikan Klaim
    ROUND(SUM(f.repair_cost_idr), 0) AS total_repair_payout_idr
FROM dim_insurance_partners p
JOIN fact_claims_sla f ON p.partner_id = f.partner_id
GROUP BY p.partner_name
ORDER BY avg_tat_days ASC;
```

### Query 2: Evaluasi Bulanan SLA Breach & Kepuasan Pelanggan (CSAT)

```sql
SELECT 
    TO_CHAR(f.claim_date, 'YYYY-MM') AS claim_month,
    COUNT(f.claim_id) AS monthly_claim_volume,
    ROUND(AVG(f.turnaround_time_days), 2) AS avg_monthly_tat_days,
    COUNT(CASE WHEN f.sla_status = 'Breached SLA' THEN 1 END) AS breached_claims_count,
    ROUND(AVG(f.csat_rating), 2) AS avg_csat_score
FROM fact_claims_sla f
GROUP BY TO_CHAR(f.claim_date, 'YYYY-MM')
ORDER BY claim_month ASC;
```
