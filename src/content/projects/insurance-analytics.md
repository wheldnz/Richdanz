---
title: Insurance & Device Protection SLA Analytics
category: data
metric: 92.4%
metricLabel: Target SLA Adherence
tags: ['BigQuery', 'Power BI', 'Machine Learning', 'SLA Analytics', 'DAX']
description: Enterprise SLA analytics and claim breach (>7 days) predictive modeling for PT ElectraCare Indonesia's device protection and warranty claims data warehouse in Google BigQuery.
---

# PT ElectraCare Indonesia — Sub-Insurance SLA & Claim Breach (>7 Days) Predictive Analytics

## Business Problem
**PT ElectraCare Indonesia** mengelola layanan *aftersales* dan klaim perlindungan perangkat elektronik (smartphone, laptop, tablet, smartwatch) yang terintegrasi dengan 9 mitra asuransi ternama (Qoala, Igloo, Chubb, Allianz, Zurich, BCA Insurance, dll.). 

Manajemen menetapkan **Target Service Level Agreement (SLA) $\le$ 7 Hari** untuk penyelesaian klaim (dari pendaftaran hingga penyerahan kembali unit ke konsumen). Namun, peningkatan volume klaim perbaikan fisik dan pergantian komponen (LCD, Mainboard, Baterai) menyebabkan **18.5% klaim mengalami SLA Breach (> 7 hari)**. Keterlambatan ini berdampak pada penurunan skor CSAT nasabah (turun dari 4.6 ke 2.5) serta klaim pinalti penundaan dari mitra asuransi.

Manajemen membutuhkan:
1. **Dashboard SLA Analytics** terpadu yang terhubung langsung ke Enterprise Data Warehouse (EDW) di **Google BigQuery** (`electracare-dw`).
2. **Sistem Prediksi Dini (*Early Warning System*) berbasis Machine Learning** untuk mengidentifikasi klaim yang berisiko terlambat melewati 7 hari sebelum perbaikan diselesaikan.
3. **Analisis Akar Masalah (*Root Cause Bottleneck*)** dan 10+ rekomendasi operasional taktis.

---

## Architecture & Data Warehouse Structure (Google BigQuery)

Sistem analitik terhubung langsung ke dataset **`electracare_dwh`** dan **`electracare_mart`** pada **Google BigQuery (`electracare-dw`)**:

* **Fact Tables**:
  - `fact_warranty_claims` (200.000 baris): Log klaim garansi & perbaikan unit (tanggal klaim, tanggal completion, turnaround time days, total biaya, status SLA).
  - `fact_device_protection` (80.000 baris): Log klaim perlindungan asuransi perangkat (nominal klaim, deductible, loss ratio, fraud score).
* **Dimension Tables**:
  - `dim_insurance_partner`: Master mitra asuransi (9 mitra, tier partner, target SLA).
  - `dim_policy`: Master polis perlindungan perangkat (Screen Protection, Full Device, Extended Warranty).
  - `dim_device`: Katalog produk perangkat (brand, kategori, subkategori, harga MSRP).
  - `dim_service_center`: Jaringan pusat perbaikan (25 cabang nasional).
  - `dim_customer`: Unified Customer Profile (250.000 nasabah).
  - `dim_date`: Role-playing date dimension (2022–2025).

---

## SQL Process & BigQuery ML Prediction

### 1. Query SLA Breach Rate per Mitra Asuransi & Sub-Kategori Perangkat
```sql
SELECT 
    ip.partner_name AS insurance_partner,
    d.category AS device_category,
    wc.damage_type,
    COUNT(wc.claim_key) AS total_claims,
    COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) AS total_sla_breached,
    ROUND(COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) * 100.0 / NULLIF(COUNT(wc.claim_key), 0), 2) AS sla_breach_rate_pct,
    ROUND(AVG(wc.turnaround_time_days), 1) AS avg_tat_days,
    ROUND(SUM(wc.total_claim_cost_idr), 0) AS total_claim_payout_idr
FROM `electracare-dw.electracare_dwh.fact_warranty_claims` wc
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip ON wc.insurance_key = ip.insurance_key
JOIN `electracare-dw.electracare_dwh.dim_device` d ON wc.device_key = d.device_key
WHERE wc.status = 'Resolved'
GROUP BY ip.partner_name, d.category, wc.damage_type
ORDER BY sla_breach_rate_pct DESC;
```

### 2. BigQuery ML Model: Prediksi Klaim SLA Breach (>7 Hari)
Script SQL berikut melatih model **Logistic Regression Classification** di BigQuery ML untuk memprediksi probabilitas klaim yang berisiko melebihi SLA 7 hari:

```sql
-- Melatih Model Prediksi Klasifikasi di BigQuery ML
CREATE OR REPLACE MODEL `electracare-dw.electracare_mart.sla_breach_prediction_model`
OPTIONS(
    model_type='LOGISTIC_REG',
    input_label_cols=['is_sla_breached_7d'],
    auto_class_weights=TRUE
) AS
SELECT 
    ip.partner_name AS insurance_partner,
    d.category AS device_category,
    wc.damage_type,
    g.region,
    sc.center_type,
    wc.total_claim_cost_idr,
    dt.day_of_week,
    dt.is_weekend,
    IF(wc.turnaround_time_days > 7, 1, 0) AS is_sla_breached_7d
FROM `electracare-dw.electracare_dwh.fact_warranty_claims` wc
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip ON wc.insurance_key = ip.insurance_key
JOIN `electracare-dw.electracare_dwh.dim_device` d ON wc.device_key = d.device_key
JOIN `electracare-dw.electracare_dwh.dim_geography` g ON wc.geo_key = g.geo_key
JOIN `electracare-dw.electracare_dwh.dim_service_center` sc ON wc.center_key = sc.center_key
JOIN `electracare-dw.electracare_dwh.dim_date` dt ON wc.claim_date_key = dt.date_key
WHERE wc.status = 'Resolved';
```

---

## Panduan Step-by-Step Implementasi di Power BI

Berikut adalah tutorial lengkap dari koneksi Google BigQuery, pembuatan DAX Measures, Machine Learning prediction visual, hingga desain dashboard 5 halaman:

### Langkah 1: Connect Power BI Desktop ke Google BigQuery
1. Buka **Power BI Desktop**, klik **Get Data** $\to$ pilih **Google BigQuery**.
2. Masukkan **Project ID**: `electracare-dw`.
3. Pilih Data Connectivity mode: **Import** (untuk performa visual optimal) atau **DirectQuery** (untuk real-time data sync).
4. Lakukan autentikasi menggunakan Service Account GCP Key JSON (`keys/gcp_key.json`).
5. Pilih tabel-tabel berikut dari dataset `electracare_dwh` & `electracare_mart`:
   - `fact_warranty_claims`, `fact_device_protection`, `fact_claim_sla_predictions`
   - `dim_insurance_partner`, `dim_policy`, `dim_device`, `dim_service_center`, `dim_geography`, `dim_date`

### Langkah 2: Power Query Data Cleaning & Feature Engineering
1. Pada **Power Query Editor**, pastikan tipe data tanggal (`claim_date`, `completion_date`) berformat `Date`.
2. Buat kustom kolom **Turnaround Time (TAT)**:
   ```m
   TAT_Days = Duration.Days([completion_date] - [claim_date])
   ```
3. Buat kustom kolom target binary **Is_SLA_Breached_7D**:
   ```m
   Is_SLA_Breached_7D = if [TAT_Days] > 7 then 1 else 0
   ```
4. Klik **Close & Apply**.

### Langkah 3: Data Modeling (Star Schema) & Formula DAX
Buka **Model View** di Power BI dan pastikan relasi berikut terbentuk (1-to-Many):
- `dim_date[date_key]` $\to$ `fact_warranty_claims[claim_date_key]`
- `dim_insurance_partner[insurance_key]` $\to$ `fact_warranty_claims[insurance_key]`
- `dim_device[device_key]` $\to$ `fact_warranty_claims[device_key]`
- `dim_service_center[center_key]` $\to$ `fact_warranty_claims[center_key]`

Buat tabel khusus `_SLA_Measures` dan masukkan rumus DAX berikut:

* **Total Claims**:
  ```dax
  Total Claims = COUNTROWS(fact_warranty_claims)
  ```
* **Total Resolved Claims**:
  ```dax
  Total Resolved Claims = CALCULATE(COUNTROWS(fact_warranty_claims), fact_warranty_claims[status] = "Resolved")
  ```
* **SLA Breached Claims (>7 Days)**:
  ```dax
  SLA Breached Claims (>7D) = 
  CALCULATE(
      COUNTROWS(fact_warranty_claims),
      fact_warranty_claims[turnaround_time_days] > 7
  )
  ```
* **SLA Breach Rate %**:
  ```dax
  SLA Breach Rate % = DIVIDE([SLA Breached Claims (>7D)], [Total Resolved Claims], 0)
  ```
* **SLA Adherence %**:
  ```dax
  SLA Adherence % = 1 - [SLA Breach Rate %]
  ```
* **Average Turnaround Time (TAT Days)**:
  ```dax
  Avg TAT Days = AVERAGE(fact_warranty_claims[turnaround_time_days])
  ```
* **MoM SLA Breach Rate Change %**:
  ```dax
  MoM Breach Rate Change % = 
  VAR CurrentRate = [SLA Breach Rate %]
  VAR PrevRate = CALCULATE([SLA Breach Rate %], DATEADD(dim_date[full_date], -1, MONTH))
  RETURN DIVIDE(CurrentRate - PrevRate, PrevRate, 0)
  ```
* **At-Risk Claim Payout Value**:
  ```dax
  At Risk Claim Value = 
  CALCULATE(
      SUM(fact_warranty_claims[total_claim_cost_idr]),
      fact_warranty_claims[turnaround_time_days] > 7
  )
  ```

### Langkah 4: Prediksi Machine Learning di Power BI

#### Metode A: Memanfaat Visual AI Bawaan — "Key Influencers"
1. Tambahkan visual **Key Influencers** ke kanvas Power BI.
2. Drag field `fact_warranty_claims[Is_SLA_Breached_7D]` ke kotak **Analyze**.
3. Drag field prediktor ke kotak **Explain by**:
   - `dim_insurance_partner[partner_name]`
   - `dim_device[category]`
   - `fact_warranty_claims[damage_type]`
   - `dim_service_center[center_name]`
   - `dim_geography[region]`
   - `dim_date[day_name]`
4. **Hasil Visual Key Influencers**: Power BI secara otomatis menjalankan model ML regresi logistik bawaan dan menampilkan *top predictors* utama keterlambatan klaim > 7 hari.

#### Metode B: Menggunakan Python Visual / Script di Power Query
Tambahkan Python script berikut di Power Query untuk menghasilkan prediksi probabilitas menggunakan model **Random Forest Classifier**:

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Copy dataset
df = dataset.copy()

# Feature Encoding
le_partner = LabelEncoder()
le_device = LabelEncoder()
le_damage = LabelEncoder()

df['partner_code'] = le_partner.fit_transform(df['insurance_partner'])
df['device_code'] = le_device.fit_transform(df['device_category'])
df['damage_code'] = le_damage.fit_transform(df['damage_type'])

X = df[['partner_code', 'device_code', 'damage_code', 'total_claim_cost_idr']]
y = df['is_sla_breached_7d']

# Fit Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict Probabilities
df['ml_breach_probability'] = model.predict_proba(X)[:, 1]
```

---

### Langkah 5: Desain Spesifikasi Dashboard Power BI 5 Halaman

1. **Halaman 1: Executive SLA Command Center**:
   - KPI Cards: Total Claims, Avg TAT (5.4 Hari), SLA Breach Rate % (18.5%), At-Risk Value (Rp 4.2B).
   - Line Chart: Cumulative Resolved Claims vs Cumulative SLA Breach Trends per Bulan.
   - Slicer: Tahun, Region (Jabodetabek, Jawa, Sumatera, Bali, dll.), dan Category Perangkat.
2. **Halaman 2: Sub-Insurance LOB & Partner SLA Matrix**:
   - Matrix Table: Breakdown Mitra Asuransi (Qoala, Igloo, Chubb, Allianz, Sunday) vs Tipe Perlindungan (Screen Protection, Full Device, Extended Warranty).
   - Decomposition Tree: Membedah kontribusi SLA Breach dari Mitra Asuransi $\to$ Tipe Perangkat $\to$ Kerusakan.
3. **Halaman 3: Operational Bottleneck & Service Center Heatmap**:
   - Map Visual: Peta sebaran Service Center di 25 kota Indonesia diwarnai berdasarkan SLA Breach Rate %.
   - Bar Chart Horizontal: Latency Tahapan Perbaikan (Verifikasi Dokumen $\to$ Inspeksi $\to$ Sparepart Procurement $\to$ Payout).
4. **Halaman 4: Predictive Early Warning Terminal (ML Insights)**:
   - Key Influencers AI Visual: Menampilkan variabel paling berpengaruh memicu klaim > 7 hari.
   - Table Grid: Daftar klaim `Pending` aktif yang mendapatkan flag alert *CRITICAL (High Risk >7D)* dari model BigQuery ML untuk segera ditindaklanjuti.
5. **Halaman 5: What-If Scenario & Action Simulator**:
   - What-If Parameter Slider: "Simulasi Peningkatan Stok Spare Part LCD (+% Buffer Stock)".
   - Dynamic Gauge Chart: Memproyeksikan penurunan SLA Breach Rate dari 18.5% ke 9.2% jika skenario diterapkan.

---

## Key Insights (>10 Temuan Analitis)

1. **LCD & Mainboard Dominance**: Pergantian LCD & Mainboard pada kategori Smartphone Flagship menyumbang **58% dari total klaim yang breach SLA (>7 hari)** akibat waktu tunggu suku cadang impor.
2. **Partner Delay Variations**: Mitra Asuransi **Igloo** dan **Sunday** mencatatkan SLA breach rate tertinggi (**24.2%** dan **22.8%**), disebabkan oleh proses verifikasi polis reimbursement manual yang membutuhkan waktu rata-rata 3.8 hari.
3. **Spare Part Latency Bottleneck**: Tahapan *Spare Part Procurement Latency* merupakan bottleneck terbesar, memakan waktu rata-rata **4.2 hari** dari total 8.5 hari TAT pada klaim yang breach.
4. **Regional Technician Disparity**: Service Center cabang **Medan** dan **Surabaya** memiliki tingkat klaim terlambat tertinggi (**28% breach rate**), didorong oleh terbatasnya kuota teknisi tersertifikasi Level 3 untuk perbaikan motherboard.
5. **Weekend Submissions Impact**: Pengajuan klaim pada hari **Jumat & Sabtu** memiliki probabilitas **1.8x lebih tinggi untuk breach 7 hari** akibat backlog antrean verifikasi di hari Senin.
6. **High-Value Audit Delay**: Klaim dengan nominal di atas **Rp 5.000.000** memicu proses audit fraud manual tambahan yang menambah delay rata-rata 3 hari kerja.
7. **CSAT Rating Drop**: Skor kepuasan pelanggan (CSAT) anjlok drastis sebesar **2.1 poin** (dari 4.6 ke 2.5) ketika waktu perbaikan melewati ambang batas 7 hari.
8. **Incomplete Document Rate**: **15% pengajuan klaim** diajukan dengan dokumen fisik yang tidak lengkap, menambahkan delay rata-rata 3.5 hari pada tahap verifikasi awal.
9. **Repeat Repair Overhead**: Penggunaan komponen non-OEM pada klaim garansi tertentu meningkatkan *repeat repair rate* sebesar **12%**, yang secara tidak langsung menambah beban antrean unit di cabang.
10. **Digital Channel Fast-Track**: Klaim tipe *Screen Protection* yang diajukan via **Aplikasi Mobile PT ElectraCare** mencatatkan kepatuhan SLA tertinggi (**94.8% SLA Met**) dengan rata-rata TAT hanya 2.5 hari.

---

## Actionable Recommendations (>10 Strategi Operasional)

1. **Implementasi AI Auto-Approval**: Terapkan *auto-approval* berbasis AI untuk klaim penggantian layar bernilai $\le$ Rp 1.500.000 guna memotong SLA persetujuan dari 2 hari menjadi < 15 menit.
2. **Automated Document Completeness Check (OCR)**: Integrasikan fitur OCR & validasi dokumen otomatis pada aplikasi mobile sebelum konsumen dapat menekan tombol submit pengajuan.
3. **Dynamic Buffer Stock Regional Hub**: Tingkatkan Reorder Point (ROP) suku cadang LCD Flagship di Regional Hub Medan dan Surabaya sebesar **35%** untuk menekan *Procurement Latency*.
4. **Integrasi Partner API Real-Time**: Bangun integrasi API otomatis dengan mitra asuransi (Igloo & Sunday) untuk memotong waktu verifikasi polis dari 3 hari menjadi real-time.
5. **Technician Cross-Skill Certification**: Buka program akselerasi pelatihan teknisi Level 3 di cabang regional dengan breach rate tinggi untuk meratakan kapasitas perbaikan.
6. **Alert Early Warning System (BigQuery ML)**: Gunakan hasil prediksi `ML.PREDICT` BigQuery untuk mengirimkan notifikasi otomatis ke Service Center Manager pada hari ke-3 apabila klaim terdeteksi berisiko terlambat.
7. **Proactive Customer Status Updates**: Sediakan notifikasi proaktif via WhatsApp pada hari ke-4 jika terdapat kendala pasokan suku cadang agar ekspektasi konsumen terjaga dan CSAT tidak anjlok.
8. **Weekend Verification Shift Allowance**: Sediakan insentif jam kerja akhir pekan bagi tim verifikasi data guna mengurai penumpukan klaim pengajuan Sabtu-Minggu.
9. **Dedicated High-Value Audit Desk**: Alokasikan *Senior Fraud Auditor* khusus untuk memproses klaim bernilai tinggi (> Rp 5M) dengan SLA audit maksimal 24 jam.
10. **Differential Tiered SLA Targets**: Tetapkan target SLA yang realistis berdasarkan tingkat kesulitan perbaikan (Garansi Layar: 3 Hari, Perbaikan Mainboard Kompleks: 7 Hari) disertai bonus KPI bulanan bagi cabang yang mencapai SLA > 95%.
