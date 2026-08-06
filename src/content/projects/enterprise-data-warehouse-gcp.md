---
title: Enterprise Data Warehouse & Modern Data Stack Pipeline
category: data
metric: 5.88M Rows & 23 Tables
metricLabel: BigQuery DWH & 10 Fact Tables
tags: ['Data Engineering', 'BigQuery', 'Apache Airflow', 'dbt', 'Python', 'SQL', 'WSL2', 'GCP']
description: Perancangan dan pembangunan Enterprise Data Warehouse (EDW) terpadu PT ElectraCare Indonesia (Aftersales Perangkat Elektronik) mengolah 5.88+ juta baris data di Google BigQuery dengan orkestrasi Apache Airflow di WSL2 Ubuntu dan transformasi dbt Core.
---

# Enterprise Data Warehouse & Modern Data Stack (GCP BigQuery + WSL Airflow + dbt Core)

## Business Context & Engineering Goals
Perusahaan penyedia jasa purna jual (*aftersales*) perangkat elektronik **PT ElectraCare Indonesia** mengelola layanan perbaikan, garansi resmi, proteksi asuransi perangkat, dan distribusi suku cadang untuk 15 produsen elektronik ternama (Samsung, Apple, Xiaomi, OPPO, Vivo, Lenovo, ASUS, HP, Dell, Acer, dll).

Tujuan utama proyek **Data Engineering** ini adalah membangun **Enterprise Data Warehouse (EDW)** terpadu berbasis Kimball Star Schema di **Google BigQuery**, mengotomatiskan alur kerja pengolahan data menggunakan **Apache Airflow di WSL2 Ubuntu**, serta melakukan pembersihan data kotor dan pengujian kualitas data otomatis menggunakan **dbt Core**.

---

## 🏛️ Modern GCP Data Platform Architecture

```
                                 DATA SOURCES
                 (POS Kasir, CRM CS, API Asuransi, ERP Gudang)
                                      │
                                      ▼
                        Python Ingestion & Cleansing Layer
                 (Pandas Regex Cleaning, Deduplication, Type Cast)
                                      │
                                      ▼
                           Google BigQuery (Cloud DWH)
               Dataset: electracare_dwh (13 Dims & 10 Fact Tables)
                                      │
                                      ▼
                          dbt Core SQL Transformation
                Staging (stg) -> Cleansed (ods) -> Data Marts (mart)
                                      │
                                      ▼
                         WSL2 Apache Airflow Pipeline
                     DAG: electracare_daily_pipeline (06:00 WIB)
                                      │
                                      ▼
                           Data Marts for BI Reports
             (mart_service_revenue_summary, mart_customer_360, etc.)
```

---

## 📊 Data Model: Kimball Star Schema (5.88M+ Baris)

Data Warehouse terdiri dari **13 Tabel Dimensi (Conformed & Subject)** dan **10 Tabel Fakta**:

| Tabel / View | Tipe | Jumlah Baris | Deskripsi |
|---|---|---|---|
| `electracare_dwh.dim_date` | Conformed Dim | 1,461 | Role-playing date dimension (2022–2025) |
| `electracare_dwh.dim_geography` | Conformed Dim | 30 | Master lokasi 30 kota di 7 wilayah Indonesia |
| `electracare_dwh.dim_customer` | Conformed Dim | 250,000 | Master pelanggan terpadu |
| `electracare_dwh.dim_device` | Subject Dim | 2,500 | Katalog SKU perangkat (HP, Laptop, Tablet) |
| `electracare_dwh.dim_spare_part` | Subject Dim | 8,000 | Katalog suku cadang (LCD, Baterai, IC, Kamera) |
| `electracare_dwh.dim_service_center` | Subject Dim | 25 | Jaringan 25 service center resmi |
| `electracare_dwh.dim_brand_partner` | Subject Dim | 15 | Mitra brand resmi (Samsung, Apple, Xiaomi, dll) |
| `electracare_dwh.dim_employee` | Subject Dim (SCD2) | 2,000 | Teknisi & staff (Slowly Changing Dimension Type 2) |
| `electracare_dwh.dim_insurance_partner` | Subject Dim | 9 | Mitra asuransi (Qoala, Igloo, PasarPolis, Chubb, dll) |
| `electracare_dwh.dim_policy` | Subject Dim | 100,000 | Polis proteksi perangkat aktif |
| `electracare_dwh.fact_service_orders` | Fact Header | 500,000 | Transaksi jasa perbaikan & revenue |
| `electracare_dwh.fact_parts_usage` | Fact Detail | 750,000 | Penggunaan suku cadang per order |
| `electracare_dwh.fact_service_pl_monthly` | Fact Aggregate | 1,200 | Rekapitulasi Laba Rugi P&L bulanan per cabang |
| `electracare_dwh.fact_customer_interactions` | Fact Log | 1,200,000 | Log interaksi pelanggan (App, WA, Call, Walk-in) |
| `electracare_dwh.fact_inventory_snapshot` | Fact Snapshot | 2,400,000 | Snapshot harian stok suku cadang di 5 gudang |
| `electracare_dwh.fact_warranty_claims` | Fact Transaction | 200,000 | Klaim garansi & pemantauan SLA perbaikan |
| `electracare_dwh.fact_device_protection` | Fact Transaction | 80,000 | Klaim asuransi proteksi layar & perangkat |
| **TOTAL DATA** | | **5,885,272 baris** | **100% Synced ke Google BigQuery** |

---

## 🛠️ Step-by-Step Pembuatan Sistem Data Warehouse dari Nol

### 1. Inisialisasi Proyek & Folder Structure
```bash
mkdir electracare-dw && cd electracare-dw
mkdir -p data_lake/raw data_lake/clean data_lake/curated
mkdir -p dbt_project/models/staging dbt_project/models/marts
mkdir -p scripts flows dags keys docs
```

### 2. Penanganan Data Kotor dari Berbagai Sumber (Data Cleaning & Ingestion)
Di dunia nyata, data datang dari berbagai sumber (POS Kasir, CSV Gudang, API Asuransi) dengan format yang berantakan. Pembersihan dilakukan menggunakan **Python Pandas & Regex**:

```python
import pandas as pd
import re

# A. Cleaning Mata Uang ('Rp 1.500.000,00' -> 1500000)
df['clean_price'] = (
    df['raw_price'].astype(str)
    .str.replace(r'[Rp.,\s]', '', regex=True)
    .pipe(pd.to_numeric, errors='coerce').fillna(0)
)

# B. Standarisasi Nomor Telepon Indonesia ('+62-812 345' -> '081234567890')
def clean_phone(p):
    digits = re.sub(r'\D', '', str(p))
    return '0' + digits[2:] if digits.startswith('62') else digits

df['clean_phone'] = df['raw_phone'].apply(clean_phone)

# C. Deduplikasi Transaksi Ganda (Window Deduplication)
df = df.drop_duplicates(subset=['transaction_id'], keep='last')
```

### 3. Upload Data ke Cloud BigQuery (Google Cloud Platform)
Data yang sudah dibersihkan diunggah ke dataset Google BigQuery menggunakan Python SDK:
```python
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("keys/gcp_key.json")
client = bigquery.Client(credentials=credentials, project="electracare-dw")

job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND", autodetect=True)
client.load_table_from_dataframe(df_clean, "electracare-dw.electracare_dwh.fact_service_orders", job_config=job_config)
```

### 4. Transformasi & Data Quality Testing dengan dbt Core
Mengompilasi model SQL staging & marts serta menjalankan pengujian kualitas data otomatis:

```sql
-- models/marts/sales/mart_service_revenue_summary.sql
SELECT 
    d.year_month,
    sc.center_name,
    g.region,
    SUM(f.gross_revenue_idr) AS total_gross_revenue,
    SUM(f.net_profit_idr) AS total_net_profit,
    ROUND(SUM(f.net_profit_idr) * 100.0 / NULLIF(SUM(f.gross_revenue_idr), 0), 2) AS net_profit_margin_pct
FROM `electracare-dw.electracare_dwh.fact_service_pl_monthly` f
JOIN `electracare-dw.electracare_dwh.dim_date` d ON f.month_date_key = d.date_key
JOIN `electracare-dw.electracare_dwh.dim_service_center` sc ON f.center_key = sc.center_key
JOIN `electracare-dw.electracare_dwh.dim_geography` g ON f.geo_key = g.geo_key
GROUP BY 1, 2, 3
```

**Hasil dbt Execution**:
```bash
dbt run  --> PASS=4 WARN=0 ERROR=0 TOTAL=4 (Views Created in BigQuery)
dbt test --> PASS=5 WARN=0 ERROR=0 TOTAL=5 (Data Quality Validated)
```

### 5. Penambahan Data Baru (*Incremental Data Ingestion*)
Ketika ada penambahan data baru harian dari POS kasir atau mitra asuransi:
1. File CSV baru masuk ke `data_lake/raw/YYYYMMDD_new_orders.csv`.
2. Python Script melakukan pembersihan & pengecekan duplikasi terhadap data lama di BigQuery.
3. Menggunakan mode `WRITE_APPEND` di BigQuery untuk menyisipkan baris baru tanpa menghapus data historis.
4. dbt menyegarkan (*refresh*) view `mart_service_revenue_summary` dan `mart_operations_kpi` secara otomatis.

### 6. Otomatisasi Pipeline Harian dengan Apache Airflow di WSL2 Ubuntu
Airflow berjalan di WSL2 Ubuntu (`http://localhost:8080`) dan mengeksekusi DAG `electracare_daily_pipeline` otomatis setiap jam 06:00 WIB:

```python
# electracare_daily_dag.py
sync_to_bigquery >> dbt_run_staging >> dbt_run_marts >> dbt_test
```
