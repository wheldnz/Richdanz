# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 05: Repair Service Analytics

Tutorial ini memandu Anda melakukan **ELT & Analisis Performa Perbaikan Perangkat & Garansi Ulang** murni menggunakan SQL di PostgreSQL.

---

## 1. Staging Table: Impor Data Tiket & Teknisi

```sql
DROP TABLE IF EXISTS staging_technician CASCADE;
DROP TABLE IF EXISTS staging_ticket CASCADE;
DROP TABLE IF EXISTS staging_warranty CASCADE;

CREATE TABLE staging_technician (
    technician_id TEXT,
    technician_name TEXT,
    is_certified TEXT
);

CREATE TABLE staging_ticket (
    ticket_id TEXT,
    device_id TEXT,
    technician_id TEXT,
    status TEXT,
    completion_date TEXT
);

CREATE TABLE staging_warranty (
    warranty_id TEXT,
    device_id TEXT,
    claim_date TEXT
);
```

---

## 2. Pembersihan & Perbaikan Anomali Data (Murni SQL)

### A. Dimensi Teknisi (`dim_technician`)
Memperbaiki anomali ID negatif menggunakan `ABS()`:

```sql
DROP TABLE IF EXISTS dim_technician CASCADE;

CREATE TABLE dim_technician AS
SELECT DISTINCT
    ABS(technician_id::INT) AS technician_id,
    technician_name,
    is_certified::INT AS is_certified
FROM staging_technician;

ALTER TABLE dim_technician ADD PRIMARY KEY (technician_id);
```

### B. Tabel Fakta Tiket Perbaikan (`fact_tickets`)
Menghapus duplikat dan menyaring tiket completed tanpa tanggal penyelesaian:

```sql
DROP TABLE IF EXISTS fact_tickets CASCADE;

CREATE TABLE fact_tickets AS
SELECT DISTINCT
    ticket_id::INT AS ticket_id,
    device_id::INT AS device_id,
    ABS(technician_id::INT) AS technician_id,
    status,
    completion_date::DATE AS completion_date
FROM staging_ticket
WHERE status = 'Completed' AND completion_date IS NOT NULL AND completion_date != '';

ALTER TABLE fact_tickets ADD PRIMARY KEY (ticket_id);
```

### C. Tabel Fakta Klaim Garansi Ulang (`fact_warranties`)
Mengkoreksi anomali di mana `claim_date` mendahului `completion_date` tiket perbaikan:

```sql
DROP TABLE IF EXISTS fact_warranties CASCADE;

CREATE TABLE fact_warranties AS
SELECT 
    w.warranty_id::INT AS warranty_id,
    w.device_id::INT AS device_id,
    CASE 
        WHEN w.claim_date::DATE < t.completion_date THEN (t.completion_date + INTERVAL '7 days')::DATE
        ELSE w.claim_date::DATE
    END AS claim_date
FROM staging_warranty w
JOIN fact_tickets t ON w.device_id = t.device_id;

ALTER TABLE fact_warranties ADD PRIMARY KEY (warranty_id);
```

---

## 3. Kueri Analisis First Fix Rate (FFR) SQL

### Query: Perbandingan First Fix Rate % Antara Teknisi Bersertifikasi vs Non-Sertifikasi

```sql
WITH RepeatRepairAnalysis AS (
    SELECT 
        t.ticket_id,
        t.technician_id,
        t.completion_date,
        COUNT(w.warranty_id) AS repeat_claims_30d
    FROM fact_tickets t
    LEFT JOIN fact_warranties w 
        ON t.device_id = w.device_id 
       AND w.claim_date BETWEEN t.completion_date AND (t.completion_date + INTERVAL '30 days')
    GROUP BY t.ticket_id, t.technician_id, t.completion_date
)
SELECT 
    tn.is_certified,
    CASE WHEN tn.is_certified = 1 THEN 'Bersertifikasi' ELSE 'Belum Sertifikasi' END AS cert_status,
    COUNT(ra.ticket_id) AS total_repairs,
    SUM(CASE WHEN ra.repeat_claims_30d = 0 THEN 1 ELSE 0 END) AS first_fix_completed,
    ROUND(SUM(CASE WHEN ra.repeat_claims_30d = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(ra.ticket_id), 2) AS first_fix_rate_pct,
    ROUND(SUM(CASE WHEN ra.repeat_claims_30d > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(ra.ticket_id), 2) AS repeat_repair_rate_pct
FROM RepeatRepairAnalysis ra
JOIN dim_technician tn ON ra.technician_id = tn.technician_id
GROUP BY tn.is_certified;
```
