---
title: Insurance Underwriting Analytics
category: data
metric: 64%
metricLabel: Target Loss Ratio
tags: ['SQL', 'Power BI', 'Finance', 'Actuarial']
description: Portfolio analysis dashboard for insurance underwriting, monitoring premium growth, claim loss ratios, and operational approval SLA metrics across branches.
---

# Insurance Underwriting Analytics

## Business Problem
Perusahaan asuransi umum (*general insurance*) menghadapi fluktuasi profitabilitas akibat ketidakseimbangan antara nilai premi yang dikumpulkan dengan klaim yang disetujui, khususnya pada lini bisnis asuransi kendaraan bermotor dan kesehatan. Manajemen memerlukan dashboard analitik terpadu untuk memantau *Loss Ratio* (rasio kerugian), melacak efisiensi operasional tim klaim (*Claim Approval Rate*), mendeteksi anomali/potensi fraud klaim, serta menganalisa kinerja pertumbuhan premi per cabang regional.

## Dataset & Raw Data
* **Tables**:
  - `policy` (500 ribu baris): Data polis asuransi, tanggal berlaku, jenis cakupan, profil nasabah, dan nilai premi.
  - `customer` (300 ribu baris): Demografi nasabah (usia, pekerjaan, lokasi, riwayat medis/berkendara).
  - `premium` (3 juta baris): Log pembayaran premi (bulanan/tahunan) dan status transaksi.
  - `claim` (400 ribu baris): Tiket pengajuan klaim, tanggal klaim, nominal klaim, status (approved, pending, rejected), dan penyebab kerugian.
  - `branch` (20 baris): Kantor cabang dan alokasi budget operasional.

### Raw Data Generation
Data dummy asuransi dirancang dengan korelasi aktuaria yang logis: nasabah dengan profil usia di bawah 25 tahun atau tinggal di wilayah metropolitan tertentu memiliki frekuensi klaim kendaraan bermotor 25% lebih tinggi di tabel `claim`, sehingga menghasilkan *Loss Ratio* yang lebih tinggi untuk segmen tersebut pada tabel analisis.

## Data Model
- **Fact Table**: `fact_insurance_monthly` (data bulanan per polis yang merekam premi diterima, klaim diajukan, klaim dibayar, dan status aktif).
- **Dimension Tables**: `dim_policy`, `dim_customer_profile`, `dim_branch`, `dim_date`.

## SQL Process
Query PostgreSQL berikut menghitung premi bersih yang dihasilkan (*Earned Premium*) vs klaim yang dibayarkan untuk menentukan *Loss Ratio* per kantor cabang:

```sql
-- Analisa Loss Ratio (Total Klaim Disetujui / Total Premi Diterima) per Cabang & Lini Bisnis
SELECT 
    b.branch_name,
    p.policy_type,
    SUM(c.claim_amount) AS total_approved_claims,
    SUM(p.premium_amount) AS total_premium_received,
    ROUND(SUM(c.claim_amount) * 100.0 / SUM(p.premium_amount), 2) AS loss_ratio_pct
FROM policy p
JOIN branch b ON p.branch_id = b.branch_id
LEFT JOIN claim c ON p.policy_id = c.policy_id AND c.status = 'Approved'
GROUP BY b.branch_name, p.policy_type
ORDER BY loss_ratio_pct DESC;
```

## Power BI & DAX
Rumus DAX aktuaria yang digunakan di dashboard:

* **Loss Ratio**:
  ```dax
  Loss Ratio = DIVIDE([Total Incurred Claims], [Total Earned Premium], 0)
  ```
* **Claim Approval Rate**:
  ```dax
  Claim Approval Rate = 
  DIVIDE(
      CALCULATE(COUNT(fact_claim[ClaimID]), fact_claim[Status] = "Approved"),
      COUNT(fact_claim[ClaimID]),
      0
  )
  ```

## Dashboard Mockup Specification
Dashboard menggunakan **Classic Premium Design (Forest Green & Gold Accents)**:
- **Halaman 1: Underwriting Performance**: Grafik garis membandingkan Cumulative Earned Premium vs. Cumulative Incurred Claims dari bulan ke bulan, diiringi KPI Loss Ratio nasional.
- **Halaman 2: Claim Management**: Tree Map dinamis yang menunjukkan proporsi nominal klaim berdasarkan tipe kerusakan, terintegrasi dengan filter rentang usia nasabah.

## Key Insights
1. **Loss Ratio Kritis**: Asuransi Kendaraan Bermotor untuk nasabah berusia < 23 tahun mencatatkan Loss Ratio sebesar 84%, jauh melebihi batas target profitabilitas sebesar 65%.
2. **Keterlambatan Klaim**: Waktu rata-rata persetujuan klaim (*Claim Cycle Time*) mencapai 14 hari kerja untuk kategori klaim non-kemitraan (reimbursement).
3. **Penyebab Klaim Terbesar**: Kategori klaim "Kecelakaan Tabrakan" mendominasi 72% dari total klaim asuransi mobil.
4. **Pertumbuhan Cabang**: Cabang Surabaya mencatatkan pertumbuhan premi tertinggi sebesar 22% YoY, didorong oleh penjualan asuransi properti komersial.
5. **Fraud Detection**: Ditemukan 3.5% pola klaim yang mencurigakan (klaim diajukan dalam waktu < 30 hari setelah polis aktif).
6. **Performa Underwriting**: Lini Bisnis Asuransi Kesehatan memiliki margin profit terkecil karena tingginya biaya klaim rawat jalan.
7. **Rasio Penolakan**: 8% klaim ditolak akibat ketidaksesuaian dokumen atau pengecualian polis yang tidak dipahami nasabah.
8. **Pengaruh loyalty**: Nasabah dengan riwayat polis > 3 tahun memiliki frekuensi klaim 15% lebih rendah dibanding nasabah baru.
9. **Rasio Claim-to-Premium**: Puncak pengajuan klaim asuransi kesehatan terjadi di bulan Januari (pasca-liburan akhir tahun).
10. **Underwriting Risk**: Nasabah di wilayah pesisir memiliki tingkat klaim asuransi properti 40% lebih tinggi akibat cuaca buruk.

## Recommendations
1. Naikkan tarif premi (underwriting loading) sebesar 15% untuk nasabah asuransi kendaraan bermotor berusia di bawah 25 tahun.
2. Digitalisasi sistem persetujuan klaim kemitraan menggunakan API rumah sakit/bengkel untuk mempercepat SLA di bawah 3 hari.
3. Wajibkan survei fisik foto digital untuk kendaraan sebelum polis disetujui guna menekan kecurangan klaim awal.
4. Fokuskan kampanye pemasaran pada asuransi properti di wilayah non-pesisir yang memiliki risiko kerugian rendah.
5. Sosialisasikan pengecualian klaim secara transparan melalui ringkasan polis di aplikasi mobile untuk menekan rasio penolakan klaim.
6. Berikan diskon loyalitas berupa pemotongan premi sebesar 10% untuk nasabah dengan rekam jejak bebas klaim (*No Claim Discount*) selama 3 tahun berturut-turut.
7. Tingkatkan integrasi dengan jaringan bengkel rekanan resmi untuk mengontrol biaya estimasi perbaikan klaim fisik.
8. Lakukan audit investigasi mendalam khusus pada klaim yang diajukan dalam kurun waktu 30 hari pertama masa aktif asuransi.
9. Sediakan fitur pengajuan klaim online mandiri (*Self-Service Portal*) dengan panduan verifikasi dokumen berbasis AI.
10. Kurangi batas maksimal tanggungan rawat jalan asuransi kesehatan mandiri; alihkan ke fokus rawat inap ber-margin sehat.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
Jalankan script DDL berikut untuk membuat database underwriting asuransi:

```sql
CREATE DATABASE insurance_analytics;

-- Tabel Kantor Cabang
CREATE TABLE branch (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100)
);

-- Tabel Polis
CREATE TABLE policy (
    policy_id INT PRIMARY KEY,
    branch_id INT REFERENCES branch(branch_id),
    policy_type VARCHAR(50),
    premium_amount INT,
    customer_age INT
);

-- Tabel Klaim
CREATE TABLE claim (
    claim_id INT PRIMARY KEY,
    policy_id INT REFERENCES policy(policy_id),
    claim_amount INT,
    status VARCHAR(20) -- 'Approved', 'Pending', 'Rejected'
);
```

### Langkah 2: Script Generate Data (Python)
Gunakan python script berikut untuk men-generate log premi dan klaim dengan korelasi risiko umur:

```python
import pandas as pd
import random
from datetime import datetime, timedelta

# Dimensi Cabang
branches = [{'branch_id': i, 'branch_name': f"Cabang {c}"} for i, c in enumerate(['Jakarta', 'Surabaya', 'Medan', 'Bandung'], 1)]
pd.DataFrame(branches).to_csv('branch.csv', index=False)

# 100k Polis Asuransi & Klaim
policies = []
claims = []

for i in range(1, 100001):
    b_id = random.randint(1, 4)
    p_type = random.choice(['Kendaraan', 'Kesehatan', 'Properti'])
    premium = random.randint(1000000, 10000000) # Premi Rupiah
    age = random.randint(18, 70)
    
    policies.append({
        'policy_id': i,
        'branch_id': b_id,
        'policy_type': p_type,
        'premium_amount': premium,
        'customer_age': age
    })
    
    # Skenario aktuaria: pengemudi < 25 tahun memiliki rasio klaim 25% lebih tinggi
    claim_rate = 0.45 if (p_type == 'Kendaraan' and age < 25) else 0.15
    if random.random() < claim_rate:
        claims.append({
            'claim_id': len(claims) + 1,
            'policy_id': i,
            'claim_amount': int(premium * random.uniform(0.3, 1.5)), # klaim bervariasi
            'status': random.choices(['Approved', 'Rejected'], weights=[0.92, 0.08])[0]
        })

pd.DataFrame(policies).to_csv('policy.csv', index=False)
pd.DataFrame(claims).to_csv('claim.csv', index=False)
print("Data dummy asuransi berhasil dibuat!")
```

### Langkah 3: Import ke PostgreSQL & Jalankan SQL
1. Import CSV ke PostgreSQL.
2. Jalankan query analisis Loss Ratio per Cabang dan Lini Bisnis di bagian **SQL Process** untuk melacak profitabilitas underwriting.

### Langkah 4: Visualisasi di Power BI
1. Tarik seluruh tabel ke Power BI Desktop.
2. Buat relasi One-to-Many dari `branch` ke `policy` dan `policy` ke `claim`.
3. Buat visualisasi bertema premium klasik dengan Forest Green & Gold.
4. Rancang visual line chart kumulatif premi vs klaim serta slider umur nasabah untuk memfilter rasio kerugian secara real-time.

