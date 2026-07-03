# ETL & SQL Analytics Tutorial - Repair Service Analytics

Tutorial ini menjelaskan proses perbaikan data teknisi dan tiket, impor skema PostgreSQL, dan penghitungan First Fix Rate untuk mendeteksi repeat repairs.

---

## 1. ETL & Penanganan Anomali (Python)

Anomali pada dataset ini:
- **`technician.csv`**: Beberapa ID bernilai negatif.
- **`ticket.csv`**: Status completed tetapi `completion_date` bernilai kosong (NaN), serta tiket duplikat.
- **`warranty.csv`**: Tanggal klaim garansi mendahului tanggal perbaikan selesai (`completion_date`).

Buat file `etl_process.py` dan jalankan kode berikut:

```python
import pandas as pd
import numpy as np

# Load
df_tech = pd.read_csv('data/raw/technician.csv')
df_tickets = pd.read_csv('data/raw/ticket.csv')
df_warr = pd.read_csv('data/raw/warranty.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan Technician
# Masalah: ID bernilai negatif
# Solusi: Ubah ID menjadi positif (absolut)
bad_ids = df_tech[df_tech['technician_id'] < 0]
print(f"Menangani {len(bad_ids)} baris ID teknisi negatif di Technician.")
df_tech['technician_id'] = df_tech['technician_id'].abs()

# 2. Bersihkan Tickets
# Masalah A: Duplikat tiket
df_tickets = df_tickets.drop_duplicates(subset=['ticket_id'])

# Masalah B: status completed tetapi completion_date kosong (NaN)
# Solusi B: Drop baris karena data selesai wajib memiliki tanggal penyelesaian
bad_comps = df_tickets[(df_tickets['status'] == 'Completed') & (df_tickets['completion_date'].isna())]
print(f"Menghapus {len(bad_comps)} baris tiket selesai tanpa completion_date.")
df_tickets = df_tickets.dropna(subset=['completion_date'])

# Hubungkan IDs teknisi yang sudah dirapikan ke tiket (pastikan foreign key valid)
# Karena ID teknisi negatif telah diubah ke positif, pastikan tiket yang memuat ID negatif juga diubah
df_tickets['technician_id'] = df_tickets['technician_id'].abs()

# 3. Bersihkan Warranty
# Masalah: claim_date mendahului completion_date tiket perbaikan perangkat
# Solusi: Gabungkan data untuk validasi tanggal. Jika claim_date < completion_date,
# set claim_date = completion_date + 7 hari (klaim default seminggu setelah perbaikan)
df_merged = df_warr.merge(df_tickets, on='device_id')
df_merged['claim_date'] = pd.to_datetime(df_merged['claim_date'])
df_merged['completion_date'] = pd.to_datetime(df_merged['completion_date'])

bad_claims = df_merged[df_merged['claim_date'] < df_merged['completion_date']]
print(f"Menangani {len(bad_claims)} baris tanggal klaim garansi mendahului penyelesaian tiket.")

for idx in bad_claims.index:
    df_merged.loc[idx, 'claim_date'] = df_merged.loc[idx, 'completion_date'] + pd.to_timedelta(7, unit='D')

# Kembalikan kolom ke struktur semula
df_warr_cleaned = df_merged[['warranty_id', 'device_id', 'claim_date']].copy()
df_warr_cleaned = df_warr_cleaned.drop_duplicates(subset=['warranty_id'])

# Pastikan data referensial
valid_tech_ids = df_tech['technician_id'].unique()
df_tickets = df_tickets[df_tickets['technician_id'].isin(valid_tech_ids)]

# Save
df_tech.to_csv('data/processed/technician.csv', index=False)
df_tickets.to_csv('data/processed/ticket.csv', index=False)
df_warr_cleaned.to_csv('data/processed/warranty.csv', index=False)

print("--- ETL Sukses! Data bersih disimpan di data/processed/ ---")
```

---

## 2. Load & SQL Analytics (PostgreSQL)

### A. Load Data
Buat tabel menggunakan `schema.sql`. Impor data dari `data/processed/` ke PostgreSQL:
1. `technician.csv` $\rightarrow$ tabel `technician`
2. `ticket.csv` $\rightarrow$ tabel `ticket`
3. `warranty.csv` $\rightarrow$ tabel `warranty`

### B. SQL First Fix Rate (FFR) Query
Jalankan query berikut untuk membandingkan FFR (First Fix Rate) antara teknisi bersertifikasi dan yang tidak bersertifikasi:

```sql
WITH RepetitionAnalysis AS (
    SELECT 
        t.ticket_id,
        t.technician_id,
        t.completion_date,
        COUNT(w.warranty_id) AS repeat_repairs_30d
    FROM ticket t
    LEFT JOIN warranty w ON t.device_id = w.device_id 
        AND w.claim_date BETWEEN t.completion_date AND t.completion_date + INTERVAL '30 days'
    GROUP BY t.ticket_id, t.technician_id, t.completion_date
)
SELECT 
    tn.is_certified,
    COUNT(ra.ticket_id) AS total_repairs,
    SUM(CASE WHEN ra.repeat_repairs_30d = 0 THEN 1 ELSE 0 END) AS first_fix_completed,
    ROUND(SUM(CASE WHEN ra.repeat_repairs_30d = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(ra.ticket_id), 2) AS first_fix_rate_pct
FROM RepetitionAnalysis ra
JOIN technician tn ON ra.technician_id = tn.technician_id
GROUP BY tn.is_certified;
```

---

## 3. Visualisasi (Power BI)

1. Impor data dari PostgreSQL ke Power BI.
2. Buat relasi:
   - `technician[technician_id]` $\rightarrow$ `ticket[technician_id]` ($1:\infty$)
3. Buat tabel kalender dan hubungkan ke `ticket[completion_date]`.
4. DAX Measure untuk **SLA Rate**:
   * *Pastikan Anda merekam total durasi pengerjaan tiket di tabel fakta untuk mengecek apakah durasi $\le 24$ jam.*
5. Susun dasbor bertema gelap oranye dengan corong operasional untuk mengidentifikasi lag/kemandekan pengerjaan antrean di fase diagnosis.
