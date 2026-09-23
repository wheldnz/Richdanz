---
title: ElectraCare — Customer Churn Risk & Retention Analytics
category: data
metric: 62,99%
metricLabel: Pelanggan Aktif Berstatus High-Risk Churn (dari 250K)
tags: ['BigQuery', 'Tableau', 'RFM', 'Cohort Retention', 'Customer Analytics']
description: Dashboard Tableau untuk memonitor risiko churn 250.000 pelanggan ElectraCare — segmentasi RFM, churn risk segment, cohort retention, dan korelasinya (atau ketiadaannya) dengan kepuasan layanan.
---

# ElectraCare — Customer Churn Risk & Retention Analytics

**Catatan konteks**: ini proyek portofolio pribadi berbasis data sintetis, terinspirasi bentuk bisnis after-sales/loyalty pelanggan elektronik — bukan data resmi perusahaan tempat penulis bekerja.

## Masalah yang Ingin Dijawab

ElectraCare punya 250.000 pelanggan aktif yang bertransaksi lewat beberapa kanal (retail, servis garansi, device protection) selama 4 tahun terakhir. Selama ini belum ada satu tempat yang bisa menjawab pertanyaan paling dasar soal retensi pelanggan: siapa yang berisiko berhenti, seberapa besar jumlahnya, dan apakah kepuasan pelanggan benar-benar jadi penyebabnya atau bukan.

Dashboard ini dibangun untuk menjawab tiga hal:

1. **Berapa banyak, dan siapa saja**, pelanggan yang berisiko tinggi berhenti — apakah terkonsentrasi di region, segmen, atau tingkat loyalitas tertentu?
2. **Apakah kepuasan pelanggan benar-benar memprediksi churn**, atau justru ada sinyal lain yang lebih kuat?
3. **Seberapa cepat pelanggan baru berhenti** setelah pertama kali bergabung, dan di titik mana perusahaan paling perlu turun tangan?

## Cara Dashboard Ini Bekerja

Data pelanggan diambil dari data warehouse perusahaan (Google BigQuery), lalu divisualisasikan di **Tableau Public** supaya bisa langsung dibuka lewat browser tanpa perlu install aplikasi apa pun. Dashboard menampilkan status risiko tiap pelanggan, kurva retensi pelanggan baru dari bulan ke bulan, dan perbandingan langsung antara skor kepuasan pelanggan dengan risiko churn-nya. Detail teknis soal query dan cara build-nya ada di bagian paling bawah halaman ini, untuk yang tertarik dari sisi data.

## Lihat Dashboard-nya

Dashboard interaktif: **[Churn Customers Dashboard — Tableau Public](https://public.tableau.com/views/Churn_Customers/Dashboard1?:language=en-GB&:display_count=n&:origin=viz_share_link)**

![Dashboard preview](/images/projects/customer-churn.png)

## Temuan Utama

1. Dari 250.000 pelanggan, **62,99% (157.483 orang) masuk kategori risiko tinggi** untuk berhenti, dan **9,33% (23.315 orang) sudah resmi berhenti**. Sisanya terbagi antara risiko sedang (11,30%) dan risiko rendah (16,38%).
2. Status risiko ini murni ditentukan dari **seberapa lama pelanggan tidak bertransaksi**: 6–150 hari tanpa transaksi = risiko rendah, 151–270 hari = risiko sedang, 271 hari ke atas = risiko tinggi.
3. Pelanggan yang paling sering bertransaksi justru lebih banyak berada di kategori risiko rendah dan sedang, bukan risiko tinggi — masuk akal, karena pelanggan yang aktif belanja otomatis baru saja bertransaksi juga.
4. **Kepuasan pelanggan (CSAT) ternyata hampir tidak berkaitan dengan risiko churn** — secara statistik, hubungan keduanya nyaris nol. Skor kepuasan rata-rata hampir sama persis di semua kategori risiko (7,49–7,51 dari skala 10), artinya pelanggan puas maupun tidak puas punya peluang berhenti yang kurang lebih sama.
5. Ini konsisten walau dilihat per kelompok skor kepuasan: pelanggan dengan skor kepuasan rendah (di bawah 6) **tidak** lebih berisiko churn dibanding pelanggan dengan skor kepuasan tinggi (9–10). Proporsinya tetap di kisaran 72% di semua kelompok.
6. Pola risiko churn juga rata di semua jenis pelanggan (Individual, Reseller, Corporate) dan semua tingkat loyalitas (Bronze sampai Platinum) — tidak ada satu segmen yang menonjol jauh dari yang lain.
7. Begitu juga antar wilayah: dari 7 region, gap-nya hanya sekitar 2 poin persentase — dari 71,49% (Papua & Maluku) sampai 73,54% (Sumatera). Tidak ada satu wilayah yang jadi "biang keladi".
8. Saat dibandingkan dengan data pelanggaran SLA servis di lapangan, polanya juga tidak nyambung — wilayah dengan risiko churn tertinggi (Sumatera) bukan wilayah dengan pelanggaran SLA servis tertinggi.
9. Pelanggan baru paling banyak berhenti di 1–2 bulan pertama setelah bergabung: dari 100% aktif di bulan ke-0, tersisa rata-rata 90,4% di bulan ke-1, lalu turun tajam ke 72,5% di bulan ke-2, dan terus menyusut sampai 15–20% di sekitar bulan ke-10/11.
10. Ada pola musiman ringan: churn cenderung naik di bulan November, lalu turun lagi di Desember–Februari.

## Rekomendasi

1. Karena status risiko saat ini hanya dihitung dari lama tidaknya pelanggan bertransaksi, pertimbangkan menambah bobot dari frekuensi dan nilai transaksi ke formula churn score — pelanggan bernilai tinggi yang baru mulai jarang bertransaksi bisa terlewat kalau hanya mengandalkan satu variabel ini.
2. Karena kepuasan pelanggan terbukti tidak berkaitan dengan churn, **jangan** jadikan skor kepuasan sebagai indikator utama churn di dashboard — pakai lama tidaknya transaksi sebagai sinyal utama, dan cari variabel lain (misalnya kategori device atau channel akuisisi) untuk prediktor yang lebih kuat.
3. Fokuskan program reaktivasi pada 157.483 pelanggan risiko tinggi yang masih aktif — ini populasi terbesar dan masih bisa diselamatkan sebelum benar-benar berhenti.
4. Karena tidak ada satu segmen, tingkat loyalitas, atau wilayah yang menonjol, program retensi sebaiknya diterapkan merata secara nasional, bukan dipusatkan ke satu wilayah — anggaran yang dipusatkan berisiko tidak efisien.
5. Region **Papua & Maluku** punya 16.617 pelanggan tapi nol pusat servis fisik di sana — ini celah operasional nyata yang perlu ditentukan: apakah dilayani lintas wilayah, atau memang butuh coverage baru.
6. Karena pelanggaran SLA servis tidak selaras dengan tingginya churn per wilayah, penyebab churn kemungkinan besar bukan soal kualitas layanan servis — perlu ditelusuri faktor lain seperti siklus hidup perangkat, kompetitor, atau harga, sebelum berinvestasi memperbaiki operasional servis.
7. Karena penurunan retensi paling tajam terjadi di bulan pertama dan kedua setelah bergabung, program onboarding atau re-engagement di 60 hari pertama berpotensi memberi dampak paling besar dibanding intervensi belakangan.
8. Manfaatkan pola musiman (churn naik di November) untuk menjadwalkan kampanye retensi sebelum periode tersebut, bukan setelah angkanya sudah naik.
9. Pelanggan yang sudah resmi berhenti rata-rata baru "ditandai berhenti" setelah 505 hari tidak bertransaksi — jauh di atas ambang risiko tinggi (271 hari). Ada baiknya dievaluasi apakah ambang ini bisa dipercepat, supaya tim retensi bisa bergerak lebih awal.

<details>
<summary>Detail Teknis (untuk Tim Data)</summary>

### Architecture & Data Warehouse (Google BigQuery)

Sumber data: view `mart_customer_churn` dan `mart_operations_kpi` pada dataset `electracare_dwh_mart`, Google BigQuery project `electracare-dw`.

* **View utama**: `mart_customer_churn` — 250.000 baris, 1 baris per pelanggan, sudah pre-agregat RFM (`days_since_last_order`, `frequency_orders`, `monetary_total`) plus `churn_risk_segment` turunan.
* **View pendukung**: `mart_operations_kpi` (1.200 baris, grain center × year_month) — dipakai untuk root-cause chart yang menghubungkan churn regional dengan SLA breach rate operasional servis, lewat `dim_service_center` → `dim_geography`.

#### Query dasar — ringkasan RFM per churn risk segment

```sql
SELECT
    churn_risk_segment,
    COUNT(*) AS n_customers,
    ROUND(AVG(days_since_last_order), 1) AS avg_recency_days,
    ROUND(AVG(frequency_orders), 2) AS avg_frequency,
    ROUND(AVG(monetary_total), 0) AS avg_monetary,
    ROUND(AVG(avg_interaction_satisfaction), 2) AS avg_satisfaction
FROM `electracare-dw.electracare_dwh_mart.mart_customer_churn`
GROUP BY churn_risk_segment
ORDER BY avg_recency_days;
```

#### Query pendukung — churn risk per region dijoin SLA breach operasional

```sql
WITH churn_by_region AS (
  SELECT region,
         COUNT(*) AS n_customers,
         ROUND(COUNTIF(churn_risk_segment IN ('High Risk','Already Churned')) * 100.0 / COUNT(*), 2) AS pct_high_risk_or_churned
  FROM `electracare-dw.electracare_dwh_mart.mart_customer_churn`
  GROUP BY region
),
ops_by_region AS (
  SELECT g.region,
         SUM(k.total_claims) AS total_claims,
         ROUND(100 - AVG(k.sla_adherence_pct), 2) AS avg_sla_breach_pct,
         ROUND(AVG(k.avg_csat), 2) AS avg_csat,
         COUNT(DISTINCT k.center_name) AS n_service_centers
  FROM `electracare-dw.electracare_dwh_mart.mart_operations_kpi` k
  JOIN `electracare-dw.electracare_dwh.dim_service_center` sc ON k.center_name = sc.center_name
  JOIN `electracare-dw.electracare_dwh.dim_geography` g ON sc.geo_key = g.geo_key
  GROUP BY g.region
)
SELECT c.*, o.total_claims, o.avg_sla_breach_pct, o.avg_csat, o.n_service_centers
FROM churn_by_region c
LEFT JOIN ops_by_region o USING (region)
ORDER BY c.pct_high_risk_or_churned DESC;
```

Hasil lengkap kedua query ini (di-export sebagai CSV, plus export penuh `mart_customer_churn`) tersedia untuk didownload — lihat repo GitHub terpisah di bagian bawah halaman ini.

### Cara Dashboard Ini Dibangun (Tableau Public)

1. **Data source**: koneksi ke export CSV dari `mart_customer_churn` (250.000 baris) sebagai sumber utama, di-extract ke engine `.hyper` lokal Tableau — bukan Live connection, karena datanya historis/batch (2022–2025), bukan real-time.
2. **Cohort Retention Matrix** dibangun manual dari agregasi bulanan (bukan tipe chart bawaan "Show Me") — 12 cohort akuisisi bulanan × hingga 12 period_month, ditampilkan sebagai matrix/heatmap dengan skala warna berdasarkan `retention_pct`.
3. **Monthly Churn Rate** dipecah per tier gabungan (Premium = Platinum+Gold, Base = Bronze+Silver) untuk melihat apakah pola musiman berbeda antar tier pelanggan.
4. **KPI cards** (Active Users, High Risk Users, Avg Churn Rate, Total Customers) dilengkapi filter Period Selector (Quarter/Month) dan Month-Year, jadi angka yang tampil bisa berubah sesuai filter yang aktif — screenshot di atas adalah satu snapshot filter tertentu, bukan angka agregat penuh.

Dashboard dipublikasikan di Tableau Public (bukan file `.twbx` lokal) supaya bisa langsung dibuka di browser tanpa install Tableau Desktop.

### Data & File

| File | Isi | Grain | Status verifikasi |
|---|---|---|---|
| `mart_customer_churn.csv` | Export penuh dari view `mart_customer_churn` — 1 baris per pelanggan, seluruh kolom RFM, region, segment, tier, churn_risk_segment | 1 baris = 1 pelanggan (250.000 baris) | Query langsung ke BigQuery `electracare-dw` |
| `04_region_churn_vs_sla_breach.csv` | Churn risk per region dijoin dengan SLA breach rate operasional | 1 baris per region (7 baris) | Query langsung ke BigQuery `electracare-dw` |
| `06_cohort_retention_matrix.csv` | Retention % per cohort bulan akuisisi × period_month (0–11 bulan sejak akuisisi) | 79 baris | Diolah dari `mart_customer_churn.csv`, bukan query BigQuery terpisah yang diverifikasi ulang |
| `07_monthly_churn_trend.csv` | Churn rate bulanan, dipecah per tier Premium vs Base | 12 baris | Sama seperti di atas — diolah untuk kebutuhan visual dashboard |

Semua dataset lengkap dan README metodologinya tersedia di repo GitHub terpisah, lihat link di bagian paling bawah halaman ini.

### Metodologi Singkat

* **Sumber data**: `electracare-dw.electracare_dwh_mart.mart_customer_churn` (250.000 baris, 1 baris per pelanggan) dan `mart_operations_kpi` (1.200 baris, grain center × year_month, periode 2022-01 s/d 2025-12).
* **RFM**: kolom yang tersedia adalah `days_since_last_order` (Recency), `frequency_orders` (Frequency), dan `monetary_total` (Monetary) — sudah pre-agregat per customer di view mart.
* **churn_risk_segment**: murni berbasis ambang recency (lihat Temuan #2); `Already Churned` adalah flag terpisah mengikuti kolom `status = 'Churned'`, bukan turunan dari threshold recency yang sama.
* **Join region untuk root-cause chart**: `mart_operations_kpi` tidak punya kolom `region` langsung — didapat lewat `dim_service_center.geo_key` → `dim_geography.region`. Join berhasil 100% (25/25 center cocok). Papua & Maluku tidak punya service center fisik sehingga barisnya kosong di data SLA.
* **Cohort retention**: cohort didefinisikan dari bulan `last_order_date` pada saat data diolah — definisi cohort yang lebih presisi (akuisisi vs order terakhir) sebaiknya dikonfirmasi ulang, karena export mentah yang tersedia tidak punya kolom tanggal order pertama secara eksplisit.

</details>

## Download Dataset & Dashboard Lengkap

Data source (CSV hasil query langsung ke BigQuery `electracare-dw`) dan link dashboard Tableau Public tersedia di repo terpisah: **[github.com/wheldnz/electracare-customer-churn-analytics](https://github.com/wheldnz/electracare-customer-churn-analytics)**.
