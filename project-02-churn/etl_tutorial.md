# ETL & SQL Analytics Tutorial - Customer Churn Analytics

Tutorial ini memandu Anda memproses data, membersihkan anomali log, mengimpor ke PostgreSQL, dan menyusun korelasi keluhan pelanggan terhadap rasio Churn.

---

## 1. ETL & Penanganan Anomali (Python)

Anomali pada dataset ini:
- **`customers.csv`**: Kolom `signup_date` mengandung `NULL` / `NaN`.
- **`support_tickets.csv`**: Kolom `resolution_time_hours` bernilai negatif.
- **`usage_logs.csv`**: Beberapa baris berisi log duplikat.

Buat file `etl_process.py` dan jalankan kode berikut:

```python
import pandas as pd
import numpy as np

# Load
df_cust = pd.read_csv('data/raw/customers.csv')
df_logs = pd.read_csv('data/raw/usage_logs.csv')
df_tickets = pd.read_csv('data/raw/support_tickets.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan Customers
# Masalah: signup_date kosong (NaN)
# Solusi: Karena signup_date penting untuk Cohort, drop baris yang kosong
null_signups = df_cust[df_cust['signup_date'].isna()]
print(f"Menghapus {len(null_signups)} baris signup_date kosong di Customers.")
df_cust = df_cust.dropna(subset=['signup_date'])

# 2. Bersihkan Support Tickets
# Masalah: resolution_time_hours bernilai negatif
# Solusi: Ubah ke nilai absolut (positif)
bad_times = df_tickets[df_tickets['resolution_time_hours'] < 0]
print(f"Menangani {len(bad_times)} baris resolution_time negatif di Support Tickets.")
df_tickets['resolution_time_hours'] = df_tickets['resolution_time_hours'].abs()

# 3. Bersihkan Usage Logs
# Masalah: Log id duplikat
# Solusi: Hapus baris duplikat berdasarkan log_id
dupes = df_logs[df_logs.duplicated(subset=['log_id'])]
print(f"Menghapus {len(dupes)} baris log duplikat di Usage Logs.")
df_logs = df_logs.drop_duplicates(subset=['log_id'])

# Pastikan data referensial konsisten (foreign key valid)
# Hapus log dan tiket yang customer_id-nya tidak ada lagi di tabel customers yang telah dibersihkan
valid_cust_ids = df_cust['customer_id'].unique()
df_logs = df_logs[df_logs['customer_id'].isin(valid_cust_ids)]
df_tickets = df_tickets[df_tickets['customer_id'].isin(valid_cust_ids)]

# Save
df_cust.to_csv('data/processed/customers.csv', index=False)
df_logs.to_csv('data/processed/usage_logs.csv', index=False)
df_tickets.to_csv('data/processed/support_tickets.csv', index=False)

print("--- ETL Sukses! Data bersih disimpan di data/processed/ ---")
```

---

## 2. Load & SQL Analytics (PostgreSQL)

### A. Load Data
Buat tabel menggunakan `schema.sql`. Kemudian impor file CSV bersih dari `data/processed/` dengan urutan:
1. `customers.csv` $\rightarrow$ tabel `customers`
2. `usage_logs.csv` $\rightarrow$ tabel `usage_logs`
3. `support_tickets.csv` $\rightarrow$ tabel `support_tickets`

### B. SQL Cohort & Churn Query
Gunakan query ini untuk menghitung rata-rata penyelesaian tiket keluhan per kategori dan hubungannya dengan status Churn pelanggan:

```sql
SELECT 
    c.status,
    st.category,
    COUNT(st.ticket_id) AS total_tickets,
    ROUND(AVG(st.resolution_time_hours), 1) AS avg_resolution_hours
FROM customers c
JOIN support_tickets st ON c.customer_id = st.customer_id
GROUP BY c.status, st.category
ORDER BY c.status, avg_resolution_hours DESC;
```

---

## 3. Visualisasi (Power BI)

1. Impor data dari PostgreSQL ke Power BI.
2. Buat relasi $1:\infty$ dari `customers[customer_id]` ke `usage_logs[customer_id]` dan `support_tickets[customer_id]`.
3. Buat tabel kalender DAX dan hubungkan ke `customers[signup_date]`.
4. DAX Measure untuk **Churn Rate**:
   ```dax
   Total Customers = COUNT(customers[customer_id])
   
   Churned Customers = CALCULATE([Total Customers], customers[status] = "Churned")
   
   Churn Rate = DIVIDE([Churned Customers], [Total Customers], 0)
   ```
5. Buat visualisasi Cohort Heatmap berdasarkan Tanggal Registrasi untuk mendeteksi kapan pelanggan paling rentan keluar (*Month-1 Churn*).
