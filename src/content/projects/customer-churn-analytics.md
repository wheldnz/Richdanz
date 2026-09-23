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

## Business Problem

ElectraCare punya basis 250.000 pelanggan aktif yang bertransaksi lintas kanal (retail, servis garansi, device protection) selama 4 tahun (2022–2025). Yang belum ada sebelumnya: **visibilitas terpusat** untuk menjawab pertanyaan dasar retensi — pelanggan mana yang berisiko berhenti, seberapa besar populasi masing-masing tingkat risiko, dan apakah faktor operasional (kepuasan layanan, SLA servis) benar-benar mendorong churn atau tidak.

Dashboard ini dibangun untuk menjawab tiga pertanyaan operasional:
1. **Berapa besar dan di mana** populasi pelanggan berisiko tinggi (High Risk) terkonsentrasi — apakah di region, segmen, atau tier tertentu?
2. **Apakah kepuasan pelanggan (CSAT/interaction satisfaction) benar-benar memprediksi churn**, atau sinyal lain yang lebih kuat?
3. **Seberapa cepat pelanggan baru drop-off** setelah akuisisi (cohort retention), dan di titik mana intervensi paling berdampak?

---

## Architecture & Data Warehouse (Google BigQuery)

Sumber data: view `mart_customer_churn` dan `mart_operations_kpi` pada dataset `electracare_dwh_mart`, Google BigQuery project `electracare-dw`.

* **View utama**: `mart_customer_churn` — 250.000 baris, 1 baris per pelanggan, sudah pre-agregat RFM (`days_since_last_order`, `frequency_orders`, `monetary_total`) plus `churn_risk_segment` turunan.
* **View pendukung**: `mart_operations_kpi` (1.200 baris, grain center × year_month) — dipakai untuk root-cause chart yang menghubungkan churn regional dengan SLA breach rate operasional servis, lewat `dim_service_center` → `dim_geography`.

### Query dasar — ringkasan RFM per churn risk segment

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

### Query pendukung — churn risk per region dijoin SLA breach operasional

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

---

## Cara dashboard ini dibangun (Tableau Public)

1. **Data source**: koneksi ke export CSV dari `mart_customer_churn` (250.000 baris) sebagai sumber utama, di-extract ke engine `.hyper` lokal Tableau — bukan Live connection, karena datanya historis/batch (2022–2025), bukan real-time.
2. **Cohort Retention Matrix** dibangun manual dari agregasi bulanan (bukan tipe chart bawaan "Show Me") — 12 cohort akuisisi bulanan × hingga 12 period_month, ditampilkan sebagai matrix/heatmap dengan skala warna berdasarkan `retention_pct`.
3. **Monthly Churn Rate** dipecah per tier gabungan (Premium = Platinum+Gold, Base = Bronze+Silver) untuk melihat apakah pola musiman berbeda antar tier pelanggan.
4. **KPI cards** (Active Users, High Risk Users, Avg Churn Rate, Total Customers) dilengkapi filter Period Selector (Quarter/Month) dan Month-Year, jadi angka yang tampil bisa berubah sesuai filter yang aktif — screenshot di bawah adalah satu snapshot filter tertentu, bukan angka agregat penuh.

Dashboard dipublikasikan di Tableau Public (bukan file `.twbx` lokal) supaya bisa langsung dibuka di browser tanpa install Tableau Desktop.

## Lihat dashboard-nya

Dashboard interaktif: **[Churn Customers Dashboard — Tableau Public](https://public.tableau.com/views/Churn_Customers/Dashboard1?:language=en-GB&:display_count=n&:origin=viz_share_link)**

![Dashboard preview](/images/projects/customer-churn.png)

---

## Key Insights (berdasarkan query langsung ke data, bukan estimasi)

1. Dari 250.000 pelanggan, **62,99% (157.483 pelanggan) berada di High Risk** churn, 9,33% (23.315) **Already Churned**, sisanya Medium Risk (11,30%) dan Low Risk (16,38%).
2. `churn_risk_segment` murni digerakkan oleh **recency** (`days_since_last_order`), bukan kombinasi RFM penuh: Low Risk = 6–150 hari sejak order terakhir, Medium Risk = 151–270 hari, High Risk = 271–1.461 hari (masih Active), Already Churned = flag `status = 'Churned'` terpisah.
3. Rata-rata frequency order justru **lebih tinggi** pada segmen Low Risk (2,91 order) dan Medium Risk (2,72 order) dibanding High Risk (1,64 order) — konsisten dengan logika RFM: pelanggan yang lebih sering transaksi cenderung baru saja bertransaksi juga.
4. **Tidak ada korelasi antara kepuasan interaksi dan risiko churn** — korelasi `avg_interaction_satisfaction` terhadap `days_since_last_order` hanya 0,0043 dan terhadap status churned hanya 0,0030 (skala -1 s/d 1). Rata-rata satisfaction nyaris identik di semua churn_risk_segment: 7,49–7,51 (skala 0–10).
5. Saat dikelompokkan per band satisfaction, proporsi High Risk + Already Churned tetap flat di kisaran 71,9%–72,8% di semua band — pelanggan dengan satisfaction rendah (<6) **tidak** menunjukkan churn rate lebih tinggi dibanding satisfaction tinggi (9-10).
6. Pola churn risk hampir seragam lintas `customer_segment` (Individual 72,26%, Reseller 72,60%, Corporate 72,23%) dan `loyalty_tier` (Bronze 72,29%, Silver 72,39%, Platinum 72,47%, Gold 72,14%) — tidak ada segmen/tier yang menonjol.
7. Antar region juga relatif seragam: High Risk + Already Churned berkisar **71,49% (Papua & Maluku) hingga 73,54% (Sumatera)** — rentang hanya ~2 poin persentase, tidak ada region outlier ekstrem.
8. Join churn regional terhadap SLA breach operasional (6 dari 7 region punya data ops) menunjukkan breach rate 6,92%–7,49% — **tidak selaras** dengan urutan churn risk per region (Sumatera churn risk tertinggi tapi SLA breach-nya bukan yang tertinggi).
9. Cohort retention drop-off tajam dan konsisten antar bulan akuisisi: dari 100% di bulan ke-0, turun ke rata-rata **90,4% di bulan ke-1**, lalu **72,5% di bulan ke-2**, terus menyusut ke kisaran 15-20% di sekitar bulan ke-10/11 — kurva peluruhannya seragam antar cohort.
10. Churn rate bulanan (dipecah tier Premium vs Base) menunjukkan pola musiman ringan: cenderung naik di November, turun di Desember-Februari — arah berkebalikan dari lonjakan volume transaksi musiman yang ditemukan di proyek Enterprise Sales.

---

## Actionable Recommendations

1. Karena `churn_risk_segment` murni berbasis recency, pertimbangkan menambah bobot frequency & monetary ke formula churn score — pelanggan frequency tinggi justru terkonsentrasi di Low/Medium Risk, sehingga model recency-only berisiko mengabaikan pelanggan bernilai tinggi yang baru mulai jarang bertransaksi.
2. Karena satisfaction interaksi tidak berkorelasi dengan churn risk, **jangan** jadikan CSAT sebagai leading indicator churn di dashboard utama — gunakan `days_since_last_order` sebagai sinyal utama, cari variabel lain (kategori device, channel akuisisi) untuk driver yang lebih prediktif.
3. Fokuskan program reaktivasi pada 157.483 pelanggan High Risk (271-1.461 hari, masih Active) — populasi terbesar dan masih bisa direaktivasi sebelum berpindah ke Already Churned.
4. Karena tidak ada segmen/tier/region yang menonjol, program retensi sebaiknya nasional/lintas tier, bukan dipusatkan ke satu wilayah — anggaran retensi terpusat berisiko tidak efisien.
5. Region **Papua & Maluku** punya 16.617 pelanggan tapi nol service center fisik — data quality gap sekaligus celah operasional nyata; perlu ditentukan apakah dilayani lintas-region atau butuh coverage baru.
6. Karena SLA breach rate tidak selaras dengan urutan churn risk regional, root-cause churn kemungkinan bukan kualitas layanan center — eksplorasi variabel lain (device lifecycle, kompetitor, harga) sebelum investasi ke operasional center.
7. Karena drop-off retensi paling tajam di bulan ke-1 dan ke-2 pasca akuisisi, intervensi onboarding/re-engagement di 60 hari pertama berpotensi memberi dampak terbesar per pelanggan dibanding intervensi belakangan.
8. Manfaatkan pola musiman churn (naik di November) untuk menjadwalkan kampanye retensi proaktif sebelum periode tersebut, bukan reaktif setelah angka bulanan sudah naik.
9. Karena Already Churned (9,33%) recency rata-ratanya 505 hari — jauh di atas ambang High Risk (271 hari) — evaluasi apakah ambang "declared churned" bisa dipercepat agar early-warning ke tim retensi lebih cepat.

---

## Data & File

Dataset (export `mart_customer_churn` + agregat regional, cohort retention, dan monthly trend) tersedia untuk didownload di repo GitHub terpisah, lengkap dengan README berisi insight & rekomendasi di atas beserta metodologinya.

---

## Download Dataset & Dashboard Lengkap
Data source (CSV hasil query langsung ke BigQuery `electracare-dw`) dan link dashboard Tableau Public tersedia di repo terpisah: **[github.com/wheldnz/electracare-customer-churn-analytics](https://github.com/wheldnz/electracare-customer-churn-analytics)**.
