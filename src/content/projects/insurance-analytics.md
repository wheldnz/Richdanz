---
title: ElectraCare — Insurance Partner Performance & Risk Monitoring
category: data
metric: 70.5%
metricLabel: Flagged Claims Terkonsentrasi di 2 dari 9 Mitra
tags: ['BigQuery', 'Tableau', 'Data Warehouse', 'Fraud Detection', 'Risk Monitoring']
description: Dashboard Tableau untuk memonitor performa 9 mitra asuransi device-protection ElectraCare — approval rate, loss ratio, dan pola klaim yang di-flag sebagai indikasi fraud, lintas 100.000 polis aktif dan 80.000 klaim.
---

# ElectraCare — Insurance Partner Performance & Risk Monitoring

**Catatan konteks**: ini proyek portofolio pribadi berbasis data sintetis, terinspirasi bentuk bisnis after-sales/device-protection multi-brand — bukan data resmi perusahaan tempat penulis bekerja. Nama 9 mitra asuransi di dashboard ini (Proteka, Naungan, Sentra Polis, Bastion Assurance, Lindap, Meridian Marine, Cakra Assurance, Garda Sentosa, Nusantara Bank Insurance) seluruhnya fiktif — tidak merujuk ke perusahaan asuransi sungguhan mana pun.

## Masalah yang Ingin Dijawab

ElectraCare menawarkan layanan *device protection* (garansi tambahan, proteksi perangkat penuh, proteksi layar) lewat **9 mitra asuransi** eksternal. Tiap mitra memproses klaim kerusakan atau kehilangan perangkat secara mandiri, dengan target SLA dan tier kontrak yang sama untuk semua mitra.

Selama ini belum ada satu tempat untuk membandingkan performa ke-9 mitra ini secara adil dalam satu tampilan — approval rate, loss ratio, dan klaim yang ditandai berpotensi fraud. Tanpa dashboard ini, tim operasional hanya melihat laporan per-mitra secara terpisah, sehingga pola seperti "2 mitra dengan loss ratio dua kali lipat mitra lain" tidak pernah terlihat sampai dibandingkan langsung.

Dashboard ini dibangun untuk menjawab tiga hal:

1. **Mitra mana yang performanya menyimpang** dari mitra-mitra lain yang sehat?
2. **Apakah pola penyimpangan itu konsisten** di semua wilayah operasional, atau hanya terjadi di lokasi tertentu?
3. **Bagaimana portofolio polis terdistribusi**, untuk memastikan gap performa itu bukan sekadar akibat salah harga produk?

## Cara Dashboard Ini Bekerja

Data klaim dan polis diambil dari data warehouse perusahaan (Google BigQuery), lalu divisualisasikan di **Tableau**. Dashboard menampilkan scorecard perbandingan 9 mitra, peta panas (heatmap) pola klaim mencurigakan per wilayah, dan sebaran jenis polis — semuanya dalam satu tampilan supaya perbandingan antar mitra langsung terlihat. Detail teknis soal query, struktur data, dan cara build-nya ada di bagian paling bawah halaman ini, untuk yang tertarik dari sisi data.

## Lihat Dashboard-nya

Dashboard lengkap tersedia sebagai file Tableau (`.twbx`) yang bisa didownload dan dibuka langsung — lihat link download di bagian bawah halaman ini.

## Temuan Utama

1. **Dua dari 9 mitra tampil berbeda secara konsisten**: Meridian Marine (approval rate 97,1%, avg loss ratio 4,43) dan Nusantara Bank Insurance (97,3%, avg loss ratio 4,38) — dibanding 7 mitra lain yang seragam di kisaran 99,6–99,8% approval rate dan loss ratio 2,08–2,17. Gap loss ratio-nya sekitar **2 kali lipat**, bukan selisih kecil.
2. Dari total 80.000 klaim, **709 klaim (0,89%) ditandai sebagai berpotensi fraud** — dan 500 dari 709 klaim itu (70,5%) berasal dari 2 mitra bermasalah di atas, padahal keduanya cuma menyumbang sekitar 22,6% dari total volume klaim. Konsentrasi klaim mencurigakan di 2 mitra ini jauh di atas proporsi volume mereka.
3. **Pola ini konsisten di ke-7 wilayah operasional**, bukan terkonsentrasi di satu daerah tertentu — dicek langsung per wilayah (Jabodetabek, Jawa, Kalimantan, Sumatera, Bali & Nusa Tenggara, Papua & Maluku, Sulawesi), Meridian Marine dan Nusantara Bank Insurance selalu jadi 2 mitra dengan angka mencurigakan tertinggi, dengan margin yang serupa di semua wilayah. Ini artinya **akar masalahnya ada di proses internal mitra itu sendiri**, bukan faktor geografis tertentu.
4. **Komisi mitra sama rata 12% untuk seluruh 9 mitra**, tanpa membedakan tier atau performa aktual — belum ada mekanisme yang mengaitkan komisi dengan approval rate atau loss ratio, jadi tidak ada disinsentif finansial otomatis untuk mitra yang berperforma buruk.
5. **Target SLA juga sama rata, 7 hari untuk semua mitra**, tanpa dibedakan berdasarkan tier atau riwayat performa — sejalan dengan temuan di atas, belum ada kebijakan yang memperlakukan mitra secara berbeda berdasarkan rekam jejak.
6. **Total 100.000 polis aktif** terbagi rata di 3 jenis produk (garansi tambahan, proteksi perangkat penuh, proteksi layar — masing-masing sekitar 33.300 polis) dengan premi bulanan rata-rata yang mirip. Tidak ada satu produk yang timpang volumenya, jadi kemungkinan besar mispricing produk bukan penyebab gap performa 2 mitra tersebut.
7. **Tier kontrak tidak berkaitan dengan performa aktual**: Meridian Marine dan Nusantara Bank Insurance sama-sama berstatus "Gold" — tapi begitu juga 4 dari 7 mitra yang sehat. Tier saat ini murni administratif, belum mencerminkan risiko aktual mitra.
8. **Selisih approval rate terlihat kecil dalam persentase (97% vs 99,7%) tapi berdampak besar dalam angka nyata**: pada skala 9.000+ klaim per mitra, selisih 2,5 poin persentase berarti ratusan klaim tambahan yang butuh proses manual atau investigasi ekstra per tahun — beban operasional yang tidak proporsional dibanding 7 mitra lain.

## Rekomendasi

1. **Audit kontrak dan proses klaim Meridian Marine serta Nusantara Bank Insurance secara khusus** — karena polanya seragam di semua wilayah, akar masalahnya kemungkinan besar ada di kebijakan underwriting atau proses verifikasi klaim internal kedua mitra ini sendiri, bukan faktor lapangan yang bisa diperbaiki dari sisi ElectraCare.
2. **Terapkan review tambahan khusus untuk klaim dari 2 mitra ini**, bukan kebijakan investigasi tambahan yang sama rata untuk semua — 7 mitra lain sudah menunjukkan performa yang konsisten baik dan tidak butuh proses ekstra yang sama.
3. **Jadikan approval rate dan loss ratio sebagai syarat perpanjangan tier kontrak tahunan**, bukan hanya volume atau lama kemitraan — tier saat ini tidak berkaitan dengan performa aktual, sehingga 2 mitra bermasalah masih berstatus "Gold" sama seperti mitra sehat lainnya.
4. **Kaitkan struktur komisi dengan performa**, bukan flat 12% untuk semua mitra — beri insentif komisi lebih tinggi untuk mitra dengan loss ratio dan klaim mencurigakan yang rendah, dan turunkan untuk mitra yang konsisten bermasalah.
5. **Bangun monitoring bulanan otomatis** untuk approval rate dan loss ratio per mitra, dengan peringatan dini kalau ada mitra baru yang mulai menyimpang dari baseline mitra-mitra sehat.
6. **Alokasikan staf verifikasi klaim sesuai beban investigasi riil**, bukan merata per mitra — dengan 70% klaim mencurigakan berasal dari 2 mitra saja, tim verifikasi idealnya mengikuti beban ini.
7. **Evaluasi apakah target SLA 7 hari yang seragam masih relevan** setelah profil risiko tiap mitra terlihat jelas — mitra dengan proses klaim lebih rumit mungkin butuh SLA berbeda dari mitra yang sudah efisien.
8. **Jadikan dashboard ini bagian dari proses onboarding mitra baru** — pola loss ratio 2 kali lipat pada 2 dari 9 mitra baru benar-benar terlihat setelah dibandingkan lintas mitra dalam satu tampilan; proses onboarding ke depan sebaiknya menyertakan baseline metrik serupa sejak awal kontrak.

<details>
<summary>Detail Teknis (untuk Tim Data)</summary>

### Architecture & Data Warehouse (Google BigQuery)

Sumber data: dataset `electracare_dwh` dan `electracare_dwh_mart` pada **Google BigQuery (`electracare-dw`)**.

* **View agregat**: `mart_insurance_partner_performance` — 1 baris per mitra (approval rate, avg loss ratio, flagged claims, total klaim/polis). Sumber utama untuk scorecard & dual-bar chart.
* **Fact table**: `fact_device_protection` (80.000 baris) — klaim device protection per polis, termasuk `fraud_score` dan `loss_ratio` per klaim. Dipakai untuk breakdown per region × mitra.
* **Dimension tables**: `dim_insurance_partner` (9 mitra: nama, tier, target SLA, komisi), `dim_policy` (100.000 polis: jenis produk, status, premi), `dim_geography` (7 region operasional nasional).

Tableau connect ke BigQuery lewat 2 Data Source terpisah sesuai grain-nya: satu langsung ke view agregat untuk scorecard, satu lagi ke tabel mentah (via Tableau Relationships, bukan Join fisik) untuk breakdown region.

#### Query dasar — Approval Rate & Loss Ratio per Mitra

```sql
SELECT
    ip.partner_name,
    ip.partner_tier,
    COUNT(fdp.claim_key) AS total_claims,
    COUNTIF(fdp.claim_status = 'Approved') AS approved_claims,
    ROUND(COUNTIF(fdp.claim_status = 'Approved') * 100.0 / NULLIF(COUNT(fdp.claim_key), 0), 1) AS approval_rate_pct,
    COUNTIF(fdp.claim_status = 'Under Investigation') AS flagged_claims,
    ROUND(AVG(fdp.loss_ratio), 3) AS avg_loss_ratio,
    ROUND(AVG(fdp.fraud_score), 3) AS avg_fraud_score
FROM `electracare-dw.electracare_dwh.fact_device_protection` fdp
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip
    ON fdp.insurance_key = ip.insurance_key
GROUP BY ip.partner_name, ip.partner_tier
ORDER BY avg_loss_ratio DESC;
```

#### Query pendukung — konsistensi anomali lintas region

```sql
SELECT
    g.region,
    ip.partner_name,
    COUNT(fdp.claim_key) AS total_claims,
    COUNTIF(fdp.claim_status = 'Under Investigation') AS flagged_claims,
    ROUND(AVG(fdp.fraud_score), 3) AS avg_fraud_score,
    ROUND(AVG(fdp.loss_ratio), 3) AS avg_loss_ratio
FROM `electracare-dw.electracare_dwh.fact_device_protection` fdp
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip ON fdp.insurance_key = ip.insurance_key
JOIN `electracare-dw.electracare_dwh.dim_geography` g ON fdp.geo_key = g.geo_key
GROUP BY g.region, ip.partner_name
ORDER BY g.region, avg_loss_ratio DESC;
```

Hasil lengkap kedua query ini (di-export sebagai CSV) tersedia untuk didownload — lihat `project-06-insurance-partner-analytics/dataset/` di repo GitHub.

### Cara Dashboard Ini Dibangun (Tableau)

Dashboard-nya Tableau, bukan Power BI — koneksi & strategi refresh-nya beda dari proyek lain. Ringkasan langkahnya (detail lengkap ada di `tableau-connection-tutorial.md` dan `insurance-partner-github-deploy-guide.md` pada dokumentasi proyek):

1. **Dua Data Source terpisah**, sesuai grain: (a) connect langsung ke view `mart_insurance_partner_performance` untuk scorecard 9 mitra + dual-bar Approval Rate vs Loss Ratio; (b) model **Tableau Relationships** (bukan Join fisik, supaya tidak fan-out) yang menghubungkan `fact_device_protection` ↔ `dim_insurance_partner` ↔ `dim_geography` ↔ `dim_policy`, untuk heatmap fraud per region dan donut distribusi polis.
2. **Extract, bukan Live** — semua interaksi (filter, sort, drill) berjalan di engine `.hyper` lokal Tableau, tidak re-query BigQuery tiap klik. Data historis/batch, jadi Live tidak memberi manfaat, hanya menambah lambat dan biaya query.
3. **Heatmap Fraud Score by Region × Partner** dibangun dengan Marks type **Square** (2 dimensi di Rows/Columns, measure di Color) — bukan tipe chart bawaan "Show Me", perlu disusun manual.
4. **Donut Policy Distribution** dibangun dari Pie chart yang di-dual-axis-kan dengan lingkaran putih di tengah (Tableau tidak punya tipe donut native).
5. Layout **Tiled** (bukan Floating) dengan **Fixed Size** 1300×900, supaya posisi tiap visual presisi di berbagai ukuran layar.

### Data & File

| File | Isi |
|---|---|
| `Insurance_ServicePartner.twbx` | File dashboard Tableau lengkap, siap dibuka |
| `mart_insurance_partner_performance.csv` | Scorecard 9 mitra |
| `dim_insurance_partner.csv` | Data mitra (tier, target SLA, komisi) |
| `fraud_pattern_by_region_partner.csv` | Pola klaim mencurigakan per region × mitra |
| `policy_distribution_by_type.csv` | Sebaran jenis polis |

Semua file di atas beserta README berisi insight dan metodologi lengkap tersedia di folder `project-06-insurance-partner-analytics/` pada repo GitHub — lihat link di bagian paling bawah halaman ini.

</details>

## Download Dataset & Dashboard Lengkap
Data source (CSV hasil query langsung ke BigQuery `electracare-dw`) dan file dashboard tersedia untuk didownload di repo terpisah: **[github.com/wheldnz/electracare-insurance-partner-analytics](https://github.com/wheldnz/electracare-insurance-partner-analytics)**.
