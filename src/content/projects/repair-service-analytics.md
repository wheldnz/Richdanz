---
title: Repair Service Analytics
category: data
metric: 3.2 Hours
metricLabel: Avg Repair Time (MTTR)
tags: ['SQL', 'Power BI', 'SLA', 'Operations']
description: Hardware maintenance operations dashboard monitoring Mean Time to Repair (MTTR), technician SLA achievement rates, and device breakdown patterns.
---

# Repair Service Analytics

## Business Problem
Perusahaan penyedia jasa perbaikan perangkat keras (*hardware service center*) menghadapi peningkatan keluhan pelanggan akibat durasi perbaikan yang lama dan tidak menentu. Selain itu, banyak pelanggan mengeluhkan perangkat mereka kembali rusak dengan gejala yang sama dalam waktu singkat setelah diperbaiki. Proyek ini bertujuan untuk mengukur pencapaian Service Level Agreement (SLA), menganalisa *Mean Time to Repair* (MTTR), mengidentifikasi teknisi berkinerja rendah, dan memantau rasio *Repeat Repair* (perbaikan berulang).

## Dataset & Raw Data
* **Tables**:
  - `customer` (100 ribu baris): Identitas pelanggan dan tingkat keanggotaan (VIP vs Reguler).
  - `device` (200 ribu baris): Detail spesifikasi perangkat (tipe, merk, tahun rilis).
  - `ticket` (800 ribu baris): Tiket perbaikan (tanggal masuk, status, kategori kerusakan, prioritas).
  - `technician` (1 ribu baris): Profil teknisi, sertifikasi, dan spesialisasi.
  - `sparepart` (500 baris): Daftar suku cadang, harga, dan stok yang tersedia.
  - `repair_history` (1.2 juta baris): Log tahapan perbaikan (antre, diagnosis, perbaikan, pengujian, selesai).
  - `warranty` (300 ribu baris): Data klaim garansi pasca-perbaikan.

### Raw Data Generation
Data dummy dirancang untuk mensimulasikan operasional bengkel perbaikan:
- Tiket dengan prioritas "High/VIP" mendapatkan alokasi penanganan lebih cepat secara konsisten di tabel `repair_history`.
- Tiket yang ditangani oleh teknisi yang kurang berpengalaman atau tidak tersertifikasi memiliki probabilitas lebih tinggi mencatatkan rekor *Warranty Claim* baru dalam kurun waktu 30 hari.

## Data Model
- **Fact Table**: `fact_repair_tickets` (data agregasi per tiket perbaikan, mencakup waktu mulai, waktu selesai, biaya suku cadang, dan biaya jasa).
- **Dimension Tables**: `dim_device`, `dim_technician`, `dim_customer`, `dim_date`.

## SQL Process
Query PostgreSQL berikut menghitung durasi perbaikan rata-rata (*Mean Time to Repair*) dan tingkat keberhasilan perbaikan pertama (*First Fix Rate*):

```sql
-- Analisa First Fix Rate per Teknisi (Tiket yang tidak rusak lagi dalam 30 hari)
WITH TicketWarranties AS (
    SELECT 
        t.ticket_id,
        t.technician_id,
        t.completion_date,
        COUNT(w.warranty_id) AS warranty_claims_within_30d
    FROM ticket t
    LEFT JOIN warranty w ON t.device_id = w.device_id 
        AND w.claim_date BETWEEN t.completion_date AND t.completion_date + INTERVAL '30 days'
    WHERE t.status = 'Completed'
    GROUP BY t.ticket_id, t.technician_id, t.completion_date
)
SELECT 
    tn.technician_name,
    COUNT(tw.ticket_id) AS total_repairs,
    SUM(CASE WHEN tw.warranty_claims_within_30d = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(tw.ticket_id) AS first_fix_rate_pct
FROM TicketWarranties tw
JOIN technician tn ON tw.technician_id = tn.technician_id
GROUP BY tn.technician_name
HAVING COUNT(tw.ticket_id) >= 20
ORDER BY first_fix_rate_pct DESC;
```

## Power BI & DAX
DAX yang digunakan untuk memantau performa operasional:

* **Mean Time to Repair (MTTR) in Hours**:
  ```dax
  MTTR Hours = AVERAGE(fact_repair_tickets[RepairDurationHours])
  ```
* **SLA Achievement Rate**:
  ```dax
  SLA Achievement Rate = 
  DIVIDE(
      CALCULATE(COUNT(fact_repair_tickets[TicketID]), fact_repair_tickets[IsWithinSLA] = 1),
      COUNT(fact_repair_tickets[TicketID]),
      0
  )
  ```

## Dashboard Mockup Specification
Dashboard menggunakan **Operational High-Contrast Theme (Dark Mode with Orange & Grey Accents)**:
- **Halaman 1: Operational SLA**: Grafik corong (*Funnel Chart*) yang menunjukkan alur tiket (Antre -> Diagnosis -> Perbaikan -> QC -> Selesai) beserta waktu tunggu rata-rata di setiap tahapan, serta Gauge Chart untuk target pencapaian SLA.
- **Halaman 2: Technician Performance**: Tabel matriks interaktif membandingkan produktivitas teknisi (jumlah tiket selesai, rata-rata MTTR, dan First Fix Rate), terintegrasi dengan filter pencarian merk perangkat.

## Key Insights
1. **Bottleneck Terbesar**: Waktu tunggu di fase *Diagnosis* memakan waktu rata-rata 36 jam, menyumbang 60% dari total durasi tiket.
2. **Kinerja Teknisi**: Teknisi junior tanpa sertifikasi memiliki First Fix Rate hanya 72% (rata-rata 28% perangkat kembali rusak dalam 30 hari).
3. **Keterlambatan Suku Cadang**: Kelangkaan stok suku cadang *Screen/Display* merk laptop tertentu meningkatkan MTTR sebesar 5 hari kerja.
4. **Prioritas VIP**: Tiket prioritas VIP mencapai SLA rate sebesar 98%, sedangkan tiket reguler hanya mencapai 74%.
5. **Rasio Pengulangan (Repeat Repair)**: Kasus repeat repair didominasi oleh kategori kerusakan *Power/Baterai* (mencapai 15% dari total kasus baterai).
6. **Waktu Puncak Kunjungan**: Tiket masuk mengalami peningkatan signifikan di hari Sabtu (naik 40% dibanding hari kerja).
7. **Usia Perangkat**: Perangkat dengan usia di atas 4 tahun memiliki tingkat kesulitan perbaikan lebih tinggi, meningkatkan rata-rata MTTR sebesar 2.5 jam.
8. **Pengaruh Pengujian QC**: Tiket yang melalui tahap pengujian kualitas (QC) formal memiliki tingkat klaim garansi 80% lebih rendah dibanding yang langsung diserahkan ke pelanggan.
9. **Korelasi Brand**: Brand X memiliki biaya perbaikan rata-rata 30% lebih mahal karena struktur suku cadang yang terintegrasi (tidak bisa diperbaiki per modul).
10. **Tingkat Kepuasan (CSAT)**: Skor CSAT pelanggan menurun drastis dari 4.8 ke 3.1 ketika MTTR melebihi batas psikologis 3 hari (72 jam).

## Recommendations
1. Terapkan SOP wajib *Quality Control* (QC) mandiri selama 30 menit sebelum perangkat dinyatakan selesai.
2. Berikan program pelatihan sertifikasi teknisi junior untuk menaikkan First Fix Rate minimal ke angka 90%.
3. Terapkan strategi *Pre-ordering* suku cadang cepat habis (fast-moving parts seperti baterai dan layar) untuk menghindari downtime operasional.
4. Otomatisasi notifikasi tiket ke WhatsApp teknisi ketika status tiket berada di antrean diagnosis lebih dari 12 jam.
5. Alokasikan teknisi senior khusus untuk menangani kategori kerusakan kompleks seperti sirkuit daya/board level.
6. Buat stasiun kerja diagnosis cepat (*Express Diagnosis*) khusus di hari Sabtu untuk memproses antrean awal.
7. Evaluasi kerja sama dengan Brand yang memiliki ketersediaan suku cadang sulit untuk dinegosiasikan ulang mengenai pasokan.
8. Berikan insentif insidental bagi teknisi yang mampu menyelesaikan tiket di bawah SLA dengan rating bintang 5 dari pelanggan.
9. Informasikan secara transparan estimasi durasi perbaikan di awal tiket dibuat untuk menjaga ekspektasi pelanggan.
10. Lakukan pemeliharaan berkala pada alat ukur dan peralatan kerja teknisi untuk menjaga presisi hasil diagnosa.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
Jalankan script DDL berikut untuk membuat database perbaikan perangkat:

```sql
CREATE DATABASE repair_service;

-- Tabel Teknisi
CREATE TABLE technician (
    technician_id INT PRIMARY KEY,
    technician_name VARCHAR(100),
    is_certified INT -- 1 = Ya, 0 = Tidak
);

-- Tabel Tiket
CREATE TABLE ticket (
    ticket_id INT PRIMARY KEY,
    device_id INT,
    technician_id INT REFERENCES technician(technician_id),
    status VARCHAR(20),
    completion_date DATE
);

-- Tabel Klaim Garansi
CREATE TABLE warranty (
    warranty_id INT PRIMARY KEY,
    device_id INT,
    claim_date DATE
);
```

### Langkah 2: Script Generate Data (Python)
Gunakan script Python berikut untuk membuat log operasional bengkel:

```python
import pandas as pd
import random
from datetime import datetime, timedelta

# Dimensi Teknisi
techs = [{'technician_id': i, 'technician_name': f"Teknisi {i}", 'is_certified': random.choices([1, 0], weights=[0.7, 0.3])[0]} for i in range(1, 101)]
pd.DataFrame(techs).to_csv('technician.csv', index=False)

# 100k Tiket Perbaikan
tickets = []
warranties = []
start_date = datetime(2023, 1, 1)

for i in range(1, 100001):
    t_id = random.randint(1, 100)
    dev_id = random.randint(1, 50000)
    comp_date = start_date + timedelta(days=random.randint(0, 700))
    is_cert = next(item for item in techs if item['technician_id'] == t_id)['is_certified']
    
    tickets.append({
        'ticket_id': i,
        'device_id': dev_id,
        'technician_id': t_id,
        'status': 'Completed',
        'completion_date': comp_date.strftime('%Y-%m-%d')
    })
    
    # Skenario: Teknisi tidak bersertifikat memiliki repeat repair rate (warranty claim) 28%
    rate = 0.28 if is_cert == 0 else 0.08
    if random.random() < rate:
        claim_date = comp_date + timedelta(days=random.randint(1, 29))
        warranties.append({
            'warranty_id': len(warranties) + 1,
            'device_id': dev_id,
            'claim_date': claim_date.strftime('%Y-%m-%d')
        })

pd.DataFrame(tickets).to_csv('ticket.csv', index=False)
pd.DataFrame(warranties).to_csv('warranty.csv', index=False)
print("Data dummy repair berhasil dibuat!")
```

### Langkah 3: Import ke PostgreSQL & Jalankan SQL
1. Import CSV ke PostgreSQL.
2. Jalankan query analisis First Fix Rate per Teknisi di bagian **SQL Process** untuk melacak pemicu garansi perbaikan berulang.

### Langkah 4: Visualisasi di Power BI
1. Tarik seluruh tabel ke Power BI Desktop.
2. Buat relasi One-to-Many dari `technician` ke `ticket`.
3. Gunakan chart operasional bertema gelap dengan aksen orange untuk memetakan bottlenecks waktu tunggu diagnosis dan KPI efisiensi teknisi.

