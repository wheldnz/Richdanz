# Panduan Pembuatan Enterprise Data Warehouse dari Nol (Build From Scratch Tutorial)
**PT ElectraCare Indonesia — Google BigQuery + WSL Airflow + dbt Core**

Tutorial ini menjelaskan **langkah demi langkah bagaimana membangun seluruh sistem Data Warehouse ini dari nol (folder kosong)** hingga menjadi sistem kelas enterprise yang siap pakai.

---

## 📌 Peta Jalan Pembuatan (7 Step Utama)

```
[Step 1: Structuring] ──> [Step 2: Data Modeling] ──> [Step 3: Ingestion Script] ──> [Step 4: Setup GCP]
 Buat struktur folder     Rancang Star Schema SQL    Python Bulk Loader          Project & JSON Key
                                                                                        │
[Step 7: Power BI & SQL] <── [Step 6: WSL Airflow] <── [Step 5: dbt BigQuery] <─────────┘
  Kueri & Dashboard BI        Orkestrasi Pipeline       Model SQL & Quality Tests
```

---

## 📂 STEP 1: Inisialisasi Struktur Folder Proyek

Buka Terminal / Command Prompt di Windows, buat folder proyek dan sub-folder yang dibutuhkan:

```bash
# 1. Buat folder proyek utama
mkdir electracare-dw
cd electracare-dw

# 2. Buat folder Data Lake, dbt, scripts, dags, dan keys
mkdir -p data_lake/raw data_lake/clean data_lake/curated
mkdir -p dbt_project/models/staging dbt_project/models/marts/sales dbt_project/models/marts/operations dbt_project/models/marts/finance
mkdir -p scripts flows dags keys docs
```

---

## 📐 STEP 2: Merancang Data Model (Kimball Star Schema DDL)

Tentukan domain bisnis (Aftersales Elektronik) dan rancang DDL SQL (`scripts/schema_ddl.sql`):

1. **Buat 4 Schema/Dataset**:
   - `stg` (Staging area mentah)
   - `ods` (Cleansed operational store)
   - `dwh` (Star Schema: Dimensions & Facts)
   - `mart` (Agregasi bisnis akhir)

2. **Rancang Conformed Dimensions (Shared)**:
   - `dim_date`: Role-playing date dimension (2022–2025).
   - `dim_geography`: Master lokasi 30 kota di 7 wilayah Indonesia.
   - `dim_customer`: Unified master pelanggan.

3. **Rancang Subject Dimensions & Fact Tables**:
   - Dimensi: `dim_device`, `dim_spare_part`, `dim_service_center`, `dim_employee` (SCD Type 2), `dim_policy`, dll.
   - Fakta: `fact_service_orders`, `fact_parts_usage`, `fact_warranty_claims`, `fact_inventory_snapshot`, `fact_service_pl_monthly`, dll.

---

## 🐍 STEP 3: Membuat Script Data Ingestion & Generator Python

Buat script `scripts/generate_all_data.py` (untuk PostgreSQL) atau `scripts/generate_bigquery_data.py` (untuk BigQuery):

1. **Gunakan Python Memory Buffer Stream (`StringIO`)**:
   - Mencegah memory overflow saat menghasilkan jutaan baris.
2. **Standardize Date Math**:
   - Pastikan tanggal pesanan dan tanggal selesai menggunakan objek `datetime.date` yang valid agar tidak melanggar *Foreign Key*.
3. **Eksekusi Bulk Load (`COPY` / BigQuery API)**:
   - Menggunakan `client.load_table_from_dataframe()` dengan `chunksize=250000` untuk mentransfer data skala juta baris secepat kilat.

---

## ☁️ STEP 4: Setup Google Cloud Platform (BigQuery & Service Account)

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat Project Baru: `electracare-dw`.
3. Aktifkan **BigQuery API**.
4. Buat **Service Account** `airflow-bigquery-sa` dengan Role: **BigQuery Admin** & **Storage Admin**.
5. Unduh Kunci JSON, lalu simpan di folder proyek:
   `electracare-dw/keys/gcp_key.json`

---

## 🔄 STEP 5: Setup Transformasi dbt Core dengan BigQuery

1. **Install dbt BigQuery Adapter**:
   ```bash
   pip install dbt-bigquery
   ```
2. **Konfigurasi `dbt_project/profiles.yml`**:
   Hubungkan dbt ke BigQuery menggunakan Kunci JSON:
   ```yaml
   electracare_dw:
     target: dev_bigquery
     outputs:
       dev_bigquery:
         type: bigquery
         method: service-account
         project: electracare-dw
         dataset: electracare_dwh
         keyfile: ../keys/gcp_key.json
         threads: 4
   ```
3. **Tulis Model SQL**:
   - Staging Model (`models/staging/stg_service_orders.sql`):
     ```sql
     select service_order_key, order_id, total_revenue_idr, turnaround_time_hours
     from electracare_dwh.fact_service_orders
     ```
   - Mart Model (`models/marts/sales/mart_service_revenue_summary.sql`):
     ```sql
     select d.year_month, sc.center_name, sum(f.gross_revenue_idr) as total_gross_revenue
     from electracare_dwh.fact_service_pl_monthly f
     join electracare_dwh.dim_date d on f.month_date_key = d.date_key
     join electracare_dwh.dim_service_center sc on f.center_key = sc.center_key
     group by 1, 2
     ```
4. **Jalankan Command dbt**:
   ```bash
   dbt run --profiles-dir .
   dbt test --profiles-dir .
   ```

---

## ⏰ STEP 6: Setup Automation Pipeline dengan Apache Airflow di WSL

1. **Masuk ke WSL Ubuntu Terminal**:
   ```bash
   wsl
   ```
2. **Install Airflow**:
   ```bash
   python3 -m venv ~/airflow_env
   source ~/airflow_env/bin/activate
   pip install "apache-airflow==2.10.2" apache-airflow-providers-google dbt-bigquery
   ```
3. **Buat Airflow DAG (`dags/electracare_daily_dag.py`)**:
   Menghubungkan skrip Python Ingestion dan dbt run ke dalam alur eksekusi otomatis menggunakan `BashOperator`:
   ```python
   sync_to_bq >> dbt_run_staging >> dbt_run_marts >> dbt_test
   ```
4. **Jalankan Airflow UI**:
   ```bash
   airflow standalone
   ```
   Buka `http://localhost:8080` di browser Windows untuk melihat pipeline visual.

---

## 📊 STEP 7: Kueri Analisis SQL & Power BI Dashboard

1. **Uji Kueri SQL di BigQuery Console**:
   Uji kueri omzet per brand, SLA adherence, atau customer 360 di BigQuery Editor.
2. **Hubungkan Power BI Desktop**:
   Pilih **Get Data $\rightarrow$ Google BigQuery $\rightarrow$ DirectQuery** ke dataset `electracare_mart`.
