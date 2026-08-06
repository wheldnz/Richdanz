# Panduan Lengkap Data Engineering di Dunia Bisnis Nyata (Real-World DE Tutorial)
**Studi Kasus: Enterprise Data Warehouse (EDW) PT ElectraCare Indonesia**
*(Aftersales Perangkat Elektronik: HP, Laptop, Tablet, Garansi, & Asuransi)*

---

## 📌 Daftar Isi
1. [Pengantar & Arsitektur Real-World Data Engineering](#1-pengantar--arsitektur-real-world-data-engineering)
2. [Desain Data Model: Kimball Star Schema & Conformed Dimensions](#2-desain-data-model-kimball-star-schema--conformed-dimensions)
3. [Proses Ingestion High-Throughput (Python + PostgreSQL COPY)](#3-proses-ingestion-high-throughput-python--postgresql-copy)
4. [Transformasi SQL Modern dengan dbt Core](#4-transformasi-sql-modern-dengan-dbt-core)
5. [Orkestrasi Pipeline & Automation dengan Prefect](#5-orkestrasi-pipeline--automation-dengan-prefect)
6. [Teknik Lanjutan DE (SCD Type 2 & DuckDB Analytics)](#6-teknik-lanjutan-de-scd-type-2--duckdb-analytics)
7. [Praktik Terbaik (Best Practices) & Pertanyaan Wawancara DE](#7-praktik-terbaik-best-practices--pertanyaan-wawancara-de)

---

## 1. Pengantar & Arsitektur Real-World Data Engineering

Di perusahaan berskala menengah hingga besar, data tidak tersimpan di satu tempat. Data tersebar di sistem POS kasir, CRM Customer Service, ERP pengadaan suku cadang, dan API mitra asuransi.

Sebagai **Data Engineer**, tugas utama Anda adalah menyatukan seluruh sumber data tersebut ke dalam satu **Enterprise Data Warehouse (EDW)** yang bersih, terstruktur, andal, dan siap dianalisis oleh Data Analyst & Executive.

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  DATA SOURCES   │ ──> │   DATA LAKE ZONES    │ ──> │   TRANSFORMATION     │ ──> │     DATA MARTS &     │
│ POS, CRM, ERP   │     │ raw -> clean -> cur  │     │ dbt Core + PostgreSQL│     │ POWER BI DASHBOARDS  │
└─────────────────┘     └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
                                  │                             ▲
                                  └────────── Prefect ──────────┘
                                      (Orchestration Pipeline)
```

### Mengapa ELT (Extract-Load-Transform), Bukan ETL Tradisional?
- **ETL Tradisional**: Data di-transformasi *sebelum* masuk ke database. Lembut jika data sangat besar dan sulit memulihkan kesalahan jika logika transformasi berubah.
- **Modern ELT**: Data mentah di-*extract* dan di-*load* 1:1 ke Data Lake/Staging terlebih dahulu, baru di-*transformasi* di dalam database menggunakan SQL (via dbt). Jika logika bisnis berubah, cukup *re-run* model dbt tanpa merusak data sumber!

---

## 2. Desain Data Model: Kimball Star Schema & Conformed Dimensions

### A. Konsep Kimball Dimensions & Facts
- **Dimension Table (`dim_*`)**: Tabel konteks berisi atribut deskriptif (siapa, apa, di mana). Contoh: `dim_customer`, `dim_device`, `dim_service_center`.
- **Fact Table (`fact_*`)**: Tabel pengukuran kuantitatif numerik (omzet, biaya, durasi jam, jumlah klaim) yang memiliki Foreign Key menuju tabel dimensi. Contoh: `fact_service_orders`, `fact_warranty_claims`.

### B. Conformed Dimensions (Dimensi Terpadu)
Merupakan tabel dimensi yang **digunakan bersama (*shared*)** oleh berbagai proses bisnis yang berbeda. 
- `dim_date`: Digunakan oleh `fact_service_orders`, `fact_warranty_claims`, `fact_inventory_snapshot`, dan `fact_employee_attendance`.
- `dim_geography`: Digunakan oleh penjualan service, lokasi gudang, cabang asuransi, dan domisili pelanggan.

Dengan Conformed Dimensions, Anda bisa melakukan **cross-domain joining** (misalnya membandingkan jumlah tiket pengaduan pelanggan dengan klaim asuransi perangkat mereka).

---

## 3. Proses Ingestion High-Throughput (Python + PostgreSQL COPY)

Ketika menangani data berskala juta baris (misalnya 5.8+ juta baris di proyek ini), metode `INSERT INTO` standar dengan loop sangat lambat dan memakan memori.

### Teknik High-Performance COPY di Python:
```python
import psycopg2
from io import StringIO

def bulk_insert_copy(conn, table_name, columns, buffer_data):
    """
    Menggunakan PostgreSQL COPY command via String Stream (StringIO).
    Mampu meng-insert 100,000+ baris per detik secara langsung ke memory stream.
    """
    cur = conn.cursor()
    cols_str = ",".join(columns)
    sql = f"COPY {table_name} ({cols_str}) FROM STDIN WITH (FORMAT csv, HEADER false, DELIMITER '\t')"
    buffer_data.seek(0)
    cur.copy_expert(sql, buffer_data)
    cur.close()
```

---

## 4. Transformasi SQL Modern dengan dbt Core

**dbt (data build tool)** adalah standar industri #1 untuk transformasi SQL di Data Engineering. dbt mengelola kode SQL seperti *software engineering* (versi terstruktur, pengujian otomatis, dan grafik ketergantungan/lineage).

### Struktur Pembagian Model di dbt:
1. **Staging Layer (`models/staging/`)**: Membaca data dari `dwh` atau `stg`, merapikan nama kolom dan tipe data.
   ```sql
   -- stg_service_orders.sql
   select
       order_id,
       order_date_key,
       service_category,
       total_revenue_idr,
       turnaround_time_hours,
       case 
           when turnaround_time_hours <= 24 then 'Express (<=24h)'
           else 'Standard (>24h)'
       end as speed_category
   from {{ source('dwh', 'fact_service_orders') }}
   ```
2. **Marts Layer (`models/marts/`)**: Tabel agregasi akhir yang dikonsumsi oleh Power BI atau eksekutif.
   ```sql
   -- mart_service_revenue_summary.sql
   select 
       d.year_month,
       sc.center_name,
       sum(f.gross_revenue_idr) as total_gross_revenue,
       sum(f.net_profit_idr) as total_net_profit,
       round(sum(f.net_profit_idr) * 100.0 / nullif(sum(f.gross_revenue_idr), 0), 2) as net_profit_margin_pct
   from {{ ref('stg_service_orders') }} f
   join {{ source('dwh', 'dim_date') }} d on f.order_date_key = d.date_key
   join {{ source('dwh', 'dim_service_center') }} sc on f.center_key = sc.center_key
   group by 1, 2
   ```

### Jalankan dbt Command:
```bash
cd dbt_project
dbt run --profiles-dir .    # Eksekusi seluruh model SQL
dbt test --profiles-dir .   # Jalankan data quality test (not null, unique, FK relation)
```

---

## 5. Orkestrasi Pipeline & Automation dengan Prefect

Di dunia bisnis nyata, pipeline data harus berjalan otomatis setiap malam tanpa campur tangan manusia. **Prefect** mengorkestrasi Python script dan dbt job dengan *retry mechanism* dan penanganan *error*.

### Contoh Code Prefect Flow (`flows/daily_pipeline.py`):
```python
from prefect import flow, task
import subprocess

@task(name="Generator & Ingestion Data")
def task_generate():
    subprocess.run(["python", "scripts/generate_all_data.py"], check=True)

@task(name="dbt Transformation Models")
def task_dbt():
    subprocess.run(["dbt", "run", "--project-dir", "dbt_project", "--profiles-dir", "dbt_project"], check=True)

@flow(name="ElectraCare Daily ETL Pipeline")
def daily_pipeline():
    task_generate()
    task_dbt()

if __name__ == "__main__":
    daily_pipeline.serve(name="daily-cron", cron="0 6 * * *") # Otomatis setiap jam 06:00 WIB
```

---

## 6. Teknik Lanjutan DE (SCD Type 2 & DuckDB Analytics)

### A. Slowly Changing Dimensions Type 2 (SCD Type 2)
Digunakan untuk mencatat **histori perubahan data** (seperti kenaikan gaji teknisi, perpindahan departemen, atau promosi level) tanpa menghapus data lama.

```sql
-- Atribut SCD2 di dim_employee
CREATE TABLE dwh.dim_employee (
    employee_key SERIAL PRIMARY KEY,    -- Surrogate key (berubah saat versi baru)
    employee_id INT NOT NULL,            -- Natural key (tetap)
    employee_name VARCHAR(200),
    department VARCHAR(50),
    salary_idr INT,
    -- Field Histori SCD2:
    scd_effective_date DATE NOT NULL,    -- Tanggal mulai berlaku
    scd_expiry_date DATE DEFAULT '9999-12-31', -- Tanggal kedaluwarsa
    scd_is_current BOOLEAN DEFAULT TRUE  -- Flag record aktif saat ini
);
```

### B. Analytical Querying dengan DuckDB
DuckDB adalah *in-process OLAP database engine* yang sangat cepat untuk membaca data Parquet atau CSV langsung menggunakan SQL tanpa perlu me-load-nya ke database server:

```python
import duckdb

# Analisis instan langsung dari tabel PostgreSQL / DuckDB
res = duckdb.query("""
    SELECT brand, COUNT(*) as total_devices, AVG(msrp_idr) as avg_price
    FROM postgres_scan('dbname=db_electracare_dw host=127.0.0.1 user=postgres password=admin123', 'dwh', 'dim_device')
    GROUP BY brand ORDER BY total_devices DESC
""").df()

print(res)
```

---

## 7. Praktik Terbaik (Best Practices) & Pertanyaan Wawancara DE

### 💡 3 Kunci Utama Portofolio DE yang Memikat Recruiter:
1. **Model Data yang Rapi**: Menunjukkan pemahaman Kimball Star Schema, Conformed Dimensions, dan Normalisasi vs Denormalisasi.
2. **Kualitas Data & Testing**: Adanya pengujian otomatis (`dbt test` / `Great Expectations`) untuk memastikan tidak ada kunci unik duplikat atau *broken Foreign Key*.
3. **Reproducibility & Documented Lineage**: Seluruh proyek memiliki skrip setup mandiri, dokumentasi arsitektur, dan kode yang ter-organisir di Git.

### ❓ Pertanyaan Wawancara DE Yang Bisa Anda Jawab Menggunakan Proyek Ini:
- **"Bagaimana Anda menangani tabel berukuran jutaan baris di PostgreSQL?"**
  *Jawaban*: Menggunakan *COPY command* via stream buffer Python untuk ingestion instan, *partitioning* pada tabel fakta tanggal, serta menambahkan *b-tree indexes* pada Foreign Keys utama (`order_date_key`, `customer_key`, `center_key`).
- **"Bagaimana Anda menangani perubahan histori data seperti gaji atau jabatan karyawan?"**
  *Jawaban*: Menggunakan arsitektur SCD Type 2 pada `dim_employee` dengan melacak `scd_effective_date`, `scd_expiry_date`, dan flag `scd_is_current`.
