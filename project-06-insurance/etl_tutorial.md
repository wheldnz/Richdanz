# ETL & SQL Analytics Tutorial - Insurance Underwriting Analytics

Tutorial ini menjelaskan proses perbaikan data nasabah, premi, dan klaim asuransi, impor ke PostgreSQL, serta penghitungan Loss Ratio aktuaria.

---

## 1. ETL & Penanganan Anomali (Python)

Anomali pada dataset ini:
- **`policy.csv`**: Kolom `premium_amount` bernilai negatif, `customer_age` di luar batas (negatif atau $> 100$ tahun), dan polis duplikat.
- **`claim.csv`**: Kolom `claim_amount` bernilai negatif.

Buat file `etl_process.py` dan jalankan kode berikut:

```python
import pandas as pd
import numpy as np

# Load
df_branch = pd.read_csv('data/raw/branch.csv')
df_policy = pd.read_csv('data/raw/policy.csv')
df_claim = pd.read_csv('data/raw/claim.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan Policy
# Masalah A: Duplikat polis
df_policy = df_policy.drop_duplicates(subset=['policy_id'])

# Masalah B: premium_amount bernilai negatif
df_policy['premium_amount'] = df_policy['premium_amount'].abs()

# Masalah C: customer_age tidak valid (< 17 atau > 100)
# Solusi C: Set ke nilai default median umur (misal: 40 tahun)
bad_ages = df_policy[(df_policy['customer_age'] < 17) | (df_policy['customer_age'] > 100)]
print(f"Menangani {len(bad_ages)} baris umur nasabah tidak logis di Policy.")
for idx in bad_ages.index:
    df_policy.loc[idx, 'customer_age'] = 40

# 2. Bersihkan Claim
# Masalah: claim_amount bernilai negatif
bad_claims = df_claim[df_claim['claim_amount'] < 0]
print(f"Menangani {len(bad_claims)} baris nominal klaim negatif di Claim.")
df_claim['claim_amount'] = df_claim['claim_amount'].abs()

# Pastikan konsistensi data referensi
valid_policy_ids = df_policy['policy_id'].unique()
df_claim = df_claim[df_claim['policy_id'].isin(valid_policy_ids)]

# Save
df_branch.to_csv('data/processed/branch.csv', index=False)
df_policy.to_csv('data/processed/policy.csv', index=False)
df_claim.to_csv('data/processed/claim.csv', index=False)

print("--- ETL Sukses! Data bersih disimpan di data/processed/ ---")
```

---

## 2. Load & SQL Analytics (PostgreSQL)

### A. Load Data
Buat database dan tabel menggunakan `schema.sql`. Impor data dari `data/processed/` ke PostgreSQL:
1. `branch.csv` $\rightarrow$ tabel `branch`
2. `policy.csv` $\rightarrow$ tabel `policy`
3. `claim.csv` $\rightarrow$ tabel `claim`

### B. SQL Loss Ratio Actuarial Query
Jalankan query berikut untuk mencari rasio kerugian (*Loss Ratio*) per cabang dan lini bisnis asuransi kendaraan bermotor:

```sql
SELECT 
    b.branch_name,
    p.policy_type,
    SUM(c.claim_amount) AS total_claims,
    SUM(p.premium_amount) AS total_premiums,
    ROUND(SUM(c.claim_amount) * 100.0 / SUM(p.premium_amount), 2) AS loss_ratio_pct
FROM policy p
JOIN branch b ON p.branch_id = b.branch_id
LEFT JOIN claim c ON p.policy_id = c.policy_id AND c.status = 'Approved'
WHERE p.policy_type = 'Kendaraan'
GROUP BY b.branch_name, p.policy_type
ORDER BY loss_ratio_pct DESC;
```

---

## 3. Visualisasi (Power BI)

1. Impor data dari PostgreSQL ke Power BI.
2. Hubungkan relasi:
   - `branch[branch_id]` $\rightarrow$ `policy[branch_id]` ($1:\infty$)
   - `policy[policy_id]` $\rightarrow$ `claim[policy_id]` ($1:\infty$)
3. Tulis DAX Measure untuk **Loss Ratio**:
   ```dax
   Total Premi = SUM(policy[premium_amount])
   
   Total Klaim Disetujui = CALCULATE(SUM(claim[claim_amount]), claim[status] = "Approved")
   
   Loss Ratio = DIVIDE([Total Klaim Disetujui], [Total Premi], 0)
   ```
4. Buat dasbor visual klasik premium (Forest Green & Gold) dengan line chart membandingkan Earned Premiums vs Incurred Claims.
5. Gunakan slicer umur nasabah untuk menyaring Loss Ratio di bawah target aktuaria (< 65%).
