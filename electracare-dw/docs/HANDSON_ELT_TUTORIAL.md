# Panduan Praktik Langsung (Hands-On Step-by-Step ELT & Data Cleaning Tutorial)
**PT ElectraCare Indonesia — Enterprise Data Warehouse (Google BigQuery + WSL Airflow)**

---

## 🧼 BAB KHUSUS: Cara Membersihkan Data Kotor (Data Cleaning di Dunia Nyata)

Di dunia industri nyata, data mentah yang datang dari berbagai sumber (POS, CSV Excel kasir, API Mitra, CRM) hampir selalu **kotor**:
- Ada format mata uang string: `'Rp 2.500.000,00'`
- Nomor telepon berformat berantakan: `'+62 812-3456-7890'` atau `'0812 3456 7890'`
- Penulisan kategori tidak konsisten: `'samsung'`, `'SAMSUNG ELECTRONICS'`, `'Samsung Inc.'`
- Data duplikat akibat jaringan terputus atau *double click* kasir.
- Data hilang (*missing values / NULL*).

Dalam arsitektur Modern Data Stack, pembersihan data dilakukan di **2 tempat**:
1. **Python Ingestion Layer (Pandas)**: Untuk konversi format mentah & pembacaan file.
2. **dbt SQL Layer (`stg` & `ods`)**: Untuk pembersihan logika bisnis, deduping, dan standarisasi.

---

### 1. Data Cleaning di Python (Pandas Ingestion Layer)

Misalkan kita menerima file CSV mentah yang kotor `raw_sales_dirty.csv`:

```python
import pandas as pd
import numpy as np
import re

# 1. Baca CSV Mentah
df = pd.read_csv("data_lake/raw/raw_sales_dirty.csv")

# ----------------------------------------------------
# A. Membersihkan String Mata Uang -> Integer/Float
# Contoh: 'Rp 1.500.000' -> 1500000
# ----------------------------------------------------
df['clean_price'] = (
    df['raw_price']
    .astype(str)
    .str.replace(r'[Rp.,\s]', '', regex=True) # Hapus 'Rp', titik, koma, spasi
    .pipe(pd.to_numeric, errors='coerce')     # Ubah ke angka, jika gagal jadi NaN
    .fillna(0)                                 # Isi NaN dengan 0
)

# ----------------------------------------------------
# B. Standarisasi Nomor Telepon Indonesia
# Contoh: '+62-812 3456 7890' -> '081234567890'
# ----------------------------------------------------
def clean_phone(phone_str):
    if pd.isna(phone_str):
        return None
    # Ambil hanya digit angka
    digits = re.sub(r'\D', '', str(phone_str))
    if digits.startswith('62'):
        digits = '0' + digits[2:]
    return digits

df['clean_phone'] = df['raw_phone'].apply(clean_phone)

# ----------------------------------------------------
# C. Menghapus Data Duplikat (Deduplication)
# ----------------------------------------------------
df = df.drop_duplicates(subset=['transaction_id'], keep='last')

# ----------------------------------------------------
# D. Handling Missing Values (NULL)
# ----------------------------------------------------
df['customer_name'] = df['customer_name'].fillna('UNKNOWN CUSTOMER').str.strip().str.title()
df['brand'] = df['brand'].fillna('Generic Brand').str.strip().str.upper()

# Simpan hasil bersih ke format Parquet
df.to_parquet("data_lake/clean/sales_cleaned.parquet")
print("Data berhasil dibersihkan di Python Layer!")
```

---

### 2. Data Cleaning di dbt SQL Layer (Staging & ODS)

Di layer dbt, kita membersihkan data menggunakan kueri SQL murni sebelum dimasukkan ke Star Schema DWH.

#### A. Standarisasi Kategori & Teks dengan `CASE WHEN` & `REGEXP`
```sql
-- models/staging/stg_dirty_customers.sql
with source_data as (
    select * from {{ source('electracare_stg', 'raw_customers') }}
)

select
    customer_id,
    
    -- Cleaning Nama (Hapus spasi ganda & Capitalize)
    initcap(trim(customer_name)) as clean_customer_name,
    
    -- Standarisasi Jenis Kelamin (Gender)
    case 
        when lower(gender) in ('m', 'male', 'pria', 'laki-laki') then 'Male'
        when lower(gender) in ('f', 'female', 'wanita', 'perempuan') then 'Female'
        else 'Unspecified'
    end as clean_gender,
    
    -- Standarisasi Brand Elektronik
    case
        when lower(brand) like '%samsung%' then 'Samsung'
        when lower(brand) like '%apple%' or lower(brand) like '%iphone%' then 'Apple'
        when lower(brand) like '%xiaomi%' or lower(brand) like '%redmi%' or lower(brand) like '%poco%' then 'Xiaomi'
        else coalesce(initcap(trim(brand)), 'Other Brand')
    end as clean_brand,
    
    -- Pembersihan Format Tanggal yang Salah
    safe_cast(registration_date as DATE) as clean_reg_date

from source_data
```

#### B. Menghapus Duplikat dengan SQL Window Function (`QUALIFY ROW_NUMBER`)
Jika ada data transaksi ganda akibat *system glitch*, kita ambil baris transaksi yang paling baru (*latest record*):

```sql
-- models/intermediate/int_dedup_service_orders.sql
select
    service_order_id,
    customer_id,
    order_timestamp,
    total_amount_idr,
    order_status
from {{ ref('stg_service_orders') }}

-- Ambil hanya 1 record terbaru per service_order_id
qualify row_number() over (
    partition by service_order_id 
    order by order_timestamp desc, updated_at desc
) = 1
```

---

### 3. Otomatisasi Test Data Quality di dbt

Untuk memastikan data yang kotor **tidak pernah lolos ke Dashboard Power BI**, kita menambahkan validasi otomatis di file `models/schema.yml`:

```yaml
version: 2

models:
  - name: stg_service_orders
    description: "Tabel staging service orders yang sudah dibersihkan"
    columns:
      - name: service_order_id
        tests:
          - unique       # Pastikan tidak ada ID duplikat
          - not_null     # Pastikan ID tidak pernah kosong/NULL

      - name: total_revenue_idr
        tests:
          - not_null
          # Custom Test: Revenue tidak boleh bernilai negatif
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0

      - name: customer_key
        tests:
          - relationships:
              to: ref('dim_customer')
              field: customer_key # Pastikan Foreign Key valid dan terhubung
```

Saat Anda menjalankan command `dbt test`, dbt akan memberi peringatan **`ERROR`** jika menemukan data kotor yang melanggar aturan di atas!

---

## 📌 Ringkasan Strategi Cleaning di Real Business:
1. **Raw Layer (`stg`)**: Terima data apa adanya dari sumber.
2. **Cleansing Layer (`ods` / `int`)**: Lakukan cast tipe data, *trim text*, *regex cleaning*, dan *case-when standardization*.
3. **Deduplication Layer**: Gunakan `ROW_NUMBER() OVER (...) = 1` untuk menghapus duplikat.
4. **Data Quality Layer**: Jalankan `dbt test` untuk mencegah data cacat masuk ke laporan eksekutif.
