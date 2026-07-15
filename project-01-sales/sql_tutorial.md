# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 01: Multi-Channel P&L Analytics

Tutorial ini memandu Anda melakukan **ELT & Analisis Profit & Loss (P&L)** murni menggunakan kueri SQL di PostgreSQL.
Fokus analisis: **Memantau performa Laba/Rugi (P&L) Harian, Bulanan, dan Tahunan di 16 Brand Partners, 9 Infinix Service Centers, dan 50 Retail Partners.**

---

## 1. Staging Table: Impor Data Mentah P&L (`pl_multi_channel_raw.csv`)

```sql
DROP TABLE IF EXISTS staging_pl_multi_channel CASCADE;

CREATE TABLE staging_pl_multi_channel (
    partner_id TEXT,
    partner_name TEXT,
    channel_type TEXT,
    month_date TEXT,
    gross_revenue TEXT,       -- Masih string 'Rp 2,500,000,000'
    cogs TEXT,                -- Masih string 'Rp 1,600,000,000'
    gross_profit TEXT,
    operating_expenses TEXT,  -- Masih string 'Rp 300,000,000'
    net_profit TEXT,
    net_profit_margin_pct TEXT
);

-- Impor file data/raw/pl_multi_channel_raw.csv ke staging_pl_multi_channel lewat pgAdmin Import / COPY command
```

---

## 2. Pembersihan & Transformasi Relasional Murni SQL

### A. Dimensi Mitra Usaha (`dim_partners`)
```sql
DROP TABLE IF EXISTS dim_partners CASCADE;

CREATE TABLE dim_partners AS
SELECT DISTINCT
    partner_id,
    partner_name,
    channel_type
FROM staging_pl_multi_channel
WHERE partner_id IS NOT NULL AND partner_id != 'partner_id';

ALTER TABLE dim_partners ADD PRIMARY KEY (partner_id);
```

### B. Tabel Fakta P&L Bulanan (`fact_pl_monthly`)
Membersihkan string mata uang `Rp 2,500,000,000` menjadi angka `NUMERIC` dan menghitung kalkulasi finansial P&L otomatis:

```sql
DROP TABLE IF EXISTS fact_pl_monthly CASCADE;

CREATE TABLE fact_pl_monthly AS
SELECT 
    ROW_NUMBER() OVER() AS pl_id,
    partner_id,
    month_date::DATE AS month_date,
    
    -- Cleaning String Revenue, COGS, OpEx
    COALESCE(NULLIF(REGEXP_REPLACE(gross_revenue, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS gross_revenue_idr,
    COALESCE(NULLIF(REGEXP_REPLACE(cogs, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS cogs_idr,
    
    -- Gross Profit = Revenue - COGS
    (COALESCE(NULLIF(REGEXP_REPLACE(gross_revenue, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) - 
     COALESCE(NULLIF(REGEXP_REPLACE(cogs, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0)) AS gross_profit_idr,
     
    COALESCE(NULLIF(REGEXP_REPLACE(operating_expenses, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) AS operating_expenses_idr,
    
    -- Net Profit = Gross Profit - OpEx
    ((COALESCE(NULLIF(REGEXP_REPLACE(gross_revenue, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) - 
      COALESCE(NULLIF(REGEXP_REPLACE(cogs, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0)) - 
      COALESCE(NULLIF(REGEXP_REPLACE(operating_expenses, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0)) AS net_profit_idr,
      
    -- Net Profit Margin %
    ROUND(
        (((COALESCE(NULLIF(REGEXP_REPLACE(gross_revenue, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0) - 
           COALESCE(NULLIF(REGEXP_REPLACE(cogs, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0)) - 
           COALESCE(NULLIF(REGEXP_REPLACE(operating_expenses, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0)) * 100.0) /
        NULLIF(COALESCE(NULLIF(REGEXP_REPLACE(gross_revenue, '[^\d.]', '', 'g'), '')::NUMERIC, 0.0), 0), 
        2
    ) AS net_profit_margin_pct

FROM staging_pl_multi_channel
WHERE partner_id IS NOT NULL AND partner_id != 'partner_id';

ALTER TABLE fact_pl_monthly ADD PRIMARY KEY (pl_id);
```

---

## 3. Kueri Analisis P&L Multi-Channel SQL

### Query 1: Perbandingan Ringkasan P&L Antar 3 Channel Utama

```sql
SELECT 
    p.channel_type,
    COUNT(DISTINCT p.partner_id) AS total_partners,
    ROUND(SUM(f.gross_revenue_idr) / 1000000000.0, 2) AS total_revenue_miliar_idr,
    ROUND(SUM(f.cogs_idr) / 1000000000.0, 2) AS total_cogs_miliar_idr,
    ROUND(SUM(f.gross_profit_idr) / 1000000000.0, 2) AS total_gross_profit_miliar_idr,
    ROUND(SUM(f.operating_expenses_idr) / 1000000000.0, 2) AS total_opex_miliar_idr,
    ROUND(SUM(f.net_profit_idr) / 1000000000.0, 2) AS total_net_profit_miliar_idr,
    ROUND(SUM(f.net_profit_idr) * 100.0 / NULLIF(SUM(f.gross_revenue_idr), 0), 2) AS net_margin_pct
FROM dim_partners p
JOIN fact_pl_monthly f ON p.partner_id = f.partner_id
GROUP BY p.channel_type
ORDER BY total_net_profit_miliar_idr DESC;
```

### Query 2: Top 5 Brand Partners & Top 3 Infinix Service Centers Berdasarkan Margin Keuntungan Bersih

```sql
SELECT 
    p.partner_name,
    p.channel_type,
    ROUND(SUM(f.gross_revenue_idr) / 1000000.0, 0) AS total_revenue_juta,
    ROUND(SUM(f.net_profit_idr) / 1000000.0, 0) AS net_profit_juta,
    ROUND(SUM(f.net_profit_idr) * 100.0 / NULLIF(SUM(f.gross_revenue_idr), 0), 2) AS net_margin_pct
FROM dim_partners p
JOIN fact_pl_monthly f ON p.partner_id = f.partner_id
GROUP BY p.partner_name, p.channel_type
ORDER BY net_margin_pct DESC
LIMIT 10;
```
