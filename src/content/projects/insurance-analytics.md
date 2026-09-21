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

## Business Problem

ElectraCare mengintegrasikan layanan *device protection* (Extended Warranty, Full Device Protection, Screen Protection) untuk pelanggan elektroniknya lewat **9 mitra asuransi** eksternal. Setiap mitra menangani approval dan pembayaran klaim kerusakan/kehilangan perangkat secara mandiri, dengan target SLA dan tier kontrak (Platinum/Gold) yang seragam di seluruh mitra.

Yang belum ada sebelumnya: **visibilitas terpusat** untuk membandingkan performa ke-9 mitra ini secara apple-to-apple — approval rate, loss ratio, dan pola klaim yang di-flag sebagai indikasi fraud (`Under Investigation`). Tanpa dashboard ini, tim operasional hanya melihat laporan per-mitra secara terpisah, sehingga pola yang baru terlihat jelas ketika dibandingkan lintas mitra — seperti 2 mitra dengan loss ratio dua kali lipat mitra lain — tidak pernah terdeteksi.

Dashboard ini dibangun untuk menjawab tiga pertanyaan operasional:
1. **Mitra mana yang performanya menyimpang** dari baseline 7 mitra sehat lainnya?
2. **Apakah pola penyimpangan itu konsisten** di semua wilayah operasional, atau terkonsentrasi di lokasi tertentu (yang mengarah ke akar masalah berbeda: proses internal mitra vs faktor lapangan lokal)?
3. **Bagaimana portofolio polis** (jenis produk, volume) terdistribusi, untuk memastikan gap performa itu bukan sekadar akibat mispricing produk?

---

## Architecture & Data Warehouse (Google BigQuery)

Sumber data: dataset `electracare_dwh` dan `electracare_dwh_mart` pada **Google BigQuery (`electracare-dw`)`**.

* **View agregat**: `mart_insurance_partner_performance` — 1 baris per mitra (approval rate, avg loss ratio, flagged claims, total klaim/polis). Sumber utama untuk scorecard & dual-bar chart.
* **Fact table**: `fact_device_protection` (80.000 baris) — klaim device protection per polis, termasuk `fraud_score` dan `loss_ratio` per klaim. Dipakai untuk breakdown per region × mitra.
* **Dimension tables**: `dim_insurance_partner` (9 mitra: nama, tier, target SLA, komisi), `dim_policy` (100.000 polis: jenis produk, status, premi), `dim_geography` (7 region operasional nasional).

Tableau connect ke BigQuery lewat 2 Data Source terpisah sesuai grain-nya (lihat bagian "Cara dashboard ini dibangun" di bawah): satu langsung ke view agregat untuk scorecard, satu lagi ke tabel mentah (via Tableau Relationships, bukan Join fisik) untuk breakdown region.

### Query dasar — Approval Rate & Loss Ratio per Mitra

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

### Query pendukung insight #3 — konsistensi anomali lintas region

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

---

## Cara dashboard ini dibangun (Tableau)

Dashboard-nya Tableau, bukan Power BI — koneksi & strategi refresh-nya beda dari proyek lain. Ringkasan langkahnya (detail lengkap ada di `tableau-connection-tutorial.md` dan `insurance-partner-github-deploy-guide.md` pada dokumentasi proyek):

1. **Dua Data Source terpisah**, sesuai grain: (a) connect langsung ke view `mart_insurance_partner_performance` untuk scorecard 9 mitra + dual-bar Approval Rate vs Loss Ratio — tidak perlu relationship apa pun; (b) model **Tableau Relationships** (bukan Join fisik, supaya tidak fan-out) yang menghubungkan `fact_device_protection` ↔ `dim_insurance_partner` ↔ `dim_geography` ↔ `dim_policy`, untuk heatmap fraud per region dan donut distribusi polis.
2. **Extract, bukan Live** — semua interaksi (filter, sort, drill) berjalan di engine `.hyper` lokal Tableau, tidak re-query BigQuery tiap klik. Data historis/batch (bukan real-time), jadi Live tidak memberi manfaat, hanya menambah lambat dan biaya query.
3. **Heatmap Fraud Score by Region × Partner** dibangun dengan Marks type **Square** (2 dimensi di Rows/Columns, measure di Color) — bukan tipe chart bawaan "Show Me", perlu disusun manual.
4. **Donut Policy Distribution** dibangun dari Pie chart yang di-dual-axis-kan dengan lingkaran putih di tengah (Tableau tidak punya tipe donut native).
5. Layout **Tiled** (bukan Floating) dengan **Fixed Size** 1300×900, supaya posisi tiap visual presisi di berbagai ukuran layar.

---

## Key Insights (berdasarkan query langsung ke data, bukan estimasi)

1. **Dua dari 9 mitra tampil berbeda secara konsisten**: Meridian Marine (approval rate 97,1%, avg loss ratio 4,43) dan Nusantara Bank Insurance (97,3%, avg loss ratio 4,38) — dibanding 7 mitra lain yang seragam di kisaran 99,6–99,8% approval rate dan loss ratio 2,08–2,17. Gap loss ratio-nya sekitar **2x lipat**, bukan selisih kecil.
2. **709 klaim berstatus "Under Investigation" (flagged) dari total 80.000 klaim (0,89%)** — dan 500 dari 709 flagged claims itu (70,5%) berasal dari 2 mitra bermasalah di atas (259 dari Meridian Marine, 241 dari Nusantara Bank Insurance), padahal keduanya cuma menyumbang ~22,6% dari total volume klaim (9.075 + 8.908 dari 80.000). Konsentrasi flagged claims di 2 mitra ini jauh di atas proporsi volume mereka.
3. **Pola anomali ini konsisten di ke-7 region operasional**, bukan terkonsentrasi di wilayah tertentu — dicek langsung per region (Jabodetabek, Jawa, Kalimantan, Sumatera, Bali & Nusa Tenggara, Papua & Maluku, Sulawesi): di setiap satu region, Meridian Marine dan Nusantara Bank Insurance selalu jadi 2 mitra dengan avg fraud score dan avg loss ratio tertinggi, dengan margin yang serupa di semua wilayah. Ini mengindikasikan **akar masalah ada di level proses/kontrak mitra itu sendiri**, bukan faktor geografis/operasional lokal tertentu.
4. **Komisi mitra seragam 12% untuk seluruh 9 mitra**, tanpa membedakan tier (Platinum vs Gold) atau performa aktual — struktur insentif saat ini tidak punya mekanisme yang menghubungkan komisi dengan approval rate/loss ratio, jadi tidak ada disinsentif finansial otomatis untuk mitra yang berperforma buruk.
5. **Target SLA juga seragam 7 hari untuk semua mitra**, tanpa diferensiasi berbasis tier atau riwayat performa — konsisten dengan temuan #4, belum ada kebijakan yang memperlakukan mitra secara berbeda berdasarkan track record.
6. **Total 100.000 polis aktif** terbagi rata di 3 jenis produk (Extended Warranty 33.336, Full Device Protection 33.262, Screen Protection 33.402) dengan avg premi bulanan Rp 70.220–70.585 — tidak ada satu produk yang timpang secara volume, jadi mispricing produk kemungkinan bukan penyebab gap performa 2 mitra tersebut (karena distribusi produknya merata di semua mitra).
7. **Tier kontrak tidak berkorelasi dengan performa aktual**: Meridian Marine dan Nusantara Bank Insurance sama-sama berstatus "Gold" — tapi begitu juga 4 dari 7 mitra sehat (Naungan, Sentra Polis, Lindap, Cakra Assurance). Tier saat ini murni administratif, belum mencerminkan risiko aktual mitra.
8. **Ketimpangan approval rate terlihat kecil dalam persentase (97% vs 99,7%) tapi berdampak besar dalam angka absolut**: pada skala 9.000+ klaim per mitra, selisih 2,5 poin persentase approval rate berarti ratusan klaim tambahan yang butuh proses manual/investigasi ekstra per tahun untuk 2 mitra itu saja — beban operasional yang tidak proporsional dibanding 7 mitra lain.

---

## Actionable Recommendations

1. **Audit kontrak & proses klaim Meridian Marine dan Nusantara Bank Insurance secara spesifik** — karena pola anomalinya seragam di semua wilayah (bukan hanya 1-2 region), akar masalahnya kemungkinan besar ada di kebijakan underwriting atau proses verifikasi klaim internal kedua mitra itu sendiri, bukan faktor lapangan yang bisa diperbaiki dari sisi ElectraCare saja.
2. **Terapkan threshold review tambahan khusus untuk klaim dari 2 mitra ini** (misal: semua klaim di atas rata-rata fraud_score mitra tersebut otomatis masuk antrean review manual), alih-alih menerapkan kebijakan investigasi tambahan yang sama rata ke semua mitra — 7 mitra lain sudah menunjukkan performa yang konsisten baik dan tidak butuh proses tambahan yang sama.
3. **Jadikan approval rate + loss ratio sebagai syarat renewal tier kontrak tahunan** (bukan cuma volume/lama kemitraan) — tier saat ini (Gold/Platinum) tidak berkorelasi dengan performa aktual, sehingga 2 mitra bermasalah tetap berstatus "Gold" yang sama dengan mitra sehat lainnya.
4. **Kaitkan struktur komisi dengan performa**, bukan flat 12% untuk semua mitra — beri insentif komisi lebih tinggi untuk mitra dengan loss ratio & flagged-claim rate rendah, dan turunkan untuk mitra yang konsisten di atas baseline, supaya ada disinsentif finansial otomatis.
5. **Bangun monitoring bulanan otomatis** (bukan tinjauan tahunan) dari `mart_insurance_partner_performance` untuk approval rate & loss ratio per mitra, dengan alert kalau ada mitra baru yang mulai menyimpang dari baseline ~99,6% approval / ~2,1 loss ratio yang ditunjukkan 7 mitra sehat.
6. **Alokasikan staf verifikasi klaim proporsional ke beban investigasi riil**, bukan merata per mitra — dengan 500 dari 709 flagged claims (70%) berasal dari 2 mitra saja, tim fraud/verifikasi idealnya dialokasikan mengikuti beban ini, bukan dibagi rata ke 9 mitra.
7. **Evaluasi apakah SLA target 7 hari yang seragam masih relevan** setelah profil risiko per mitra terlihat jelas — mitra dengan proses klaim lebih rumit (yang tercermin dari avg fraud score & loss ratio tinggi) mungkin butuh SLA berbeda dari mitra dengan proses klaim yang sudah efisien, alih-alih satu target yang sama untuk semua.
8. **Jadikan dashboard ini bagian dari proses due-diligence mitra baru** — pola loss ratio 2x lipat pada 2 dari 9 mitra baru benar-benar terlihat setelah dibandingkan lintas mitra dalam satu tampilan; proses onboarding mitra ke depan sebaiknya menyertakan baseline metrik serupa sejak awal kontrak, bukan baru dievaluasi belakangan.

---

## Data & File

File dashboard (`.twbx`) dan 4 CSV data source (`mart_insurance_partner_performance`, `dim_insurance_partner`, `fraud_pattern_by_region_partner`, `policy_distribution_by_type`) tersedia untuk didownload di folder `project-06-insurance-partner-analytics/` pada repo GitHub — lengkap dengan README berisi insight & rekomendasi di atas beserta metodologinya.

---

## Download Dataset & Dashboard Lengkap
Data source (CSV hasil query langsung ke BigQuery `electracare-dw`) dan file dashboard tersedia untuk didownload di repo terpisah: **[github.com/wheldnz/electracare-insurance-partner-analytics](https://github.com/wheldnz/electracare-insurance-partner-analytics)**.
