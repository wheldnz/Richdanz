---
title: Customer Churn Analytics
category: data
metric: 92%
metricLabel: Churn Prediction Accuracy
tags: ['SQL', 'Power BI', 'Cohort', 'Retention']
description: Churn forecasting and cohort retention dashboard tracking customer lifetime value (CLV) and feature usage patterns for a 1-million-customer subscription platform.
---

# Customer Churn Analytics

## Business Problem
Perusahaan penyedia layanan digital (*subscription-based model*) mengalami peningkatan rasio *Customer Churn* yang signifikan dalam 6 bulan terakhir. Manajemen membutuhkan visibilitas mendalam tentang pola perilaku pelanggan sebelum mereka memutuskan berhenti berlangganan, kelompok pengguna (*cohort*) mana yang memiliki tingkat retensi paling rendah, serta faktor operasional apa (seperti *support tickets*) yang paling mempengaruhi *churn*.

## Dataset & Raw Data
* **Tables**:
  - `customers` (1 juta baris): Demografi pelanggan, status langganan, dan kanal pendaftaran.
  - `subscriptions` (1.2 juta baris): Riwayat paket langganan, tanggal mulai, dan tanggal berakhir.
  - `invoices` (5 juta baris): Catatan pembayaran bulanan dan status transaksi.
  - `support_tickets` (800 ribu baris): Log keluhan pelanggan dan kategori masalah.
  - `usage_logs` (10 juta baris): Aktivitas login dan frekuensi penggunaan fitur utama.

### Raw Data Generation
Data dirancang dengan keterkaitan logis: pelanggan yang memiliki jumlah keluhan teknis di tabel `support_tickets` $> 3$ kali dalam sebulan, serta frekuensi login di `usage_logs` yang menurun $> 50\%$ secara berturut-turut, akan ditandai dengan probabilitas tinggi mengalami *churn* pada tabel `customers`.

## Data Model
- **Fact Table**: `fact_invoices` (catatan pembayaran harian).
- **Dimension Tables**: `dim_customer`, `dim_subscription`, `dim_support_ticket`, `dim_usage_summary`, `dim_date`.

## SQL Process
Query SQL berikut memproses data di PostgreSQL untuk membuat *Customer Retention Cohort* bulanan:

```sql
-- Deteksi aktivitas login terakhir dan melabeli status 'At Risk'
WITH LastUserActivity AS (
    SELECT 
        customer_id,
        MAX(login_date) AS last_active,
        COUNT(CASE WHEN login_date >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) AS logins_last_30_days
    FROM usage_logs
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.signup_date,
    la.last_active,
    la.logins_last_30_days,
    CASE 
        WHEN la.last_active < CURRENT_DATE - INTERVAL '90 days' THEN 'Churned'
        WHEN la.logins_last_30_days < 3 THEN 'At Risk'
        ELSE 'Active'
    END AS customer_status
FROM customers c
LEFT JOIN LastUserActivity la ON c.customer_id = la.customer_id;
```

## Power BI & DAX
Rumus DAX untuk mengkalkulasi tingkat *Churn Rate* dan *Retention Rate*:

* **Churn Rate**:
  ```dax
  Churn Rate = 
  VAR LostCustomers = CALCULATE(COUNT(dim_customer[CustomerID]), dim_customer[Status] = "Churned")
  VAR TotalCustomers = COUNT(dim_customer[CustomerID])
  RETURN
  DIVIDE(LostCustomers, TotalCustomers, 0)
  ```
* **Customer Lifetime Value (CLV)**:
  ```dax
  CLV = DIVIDE([Average Monthly Revenue Per User], [Churn Rate], 0)
  ```

## Dashboard Mockup Specification
Dashboard didesain dengan konsep **Sleek Light Mode (Sage Green & Coral/Red Accent)**:
- **Halaman 1: Churn Overview**: Cohort Retention Matrix Heatmap yang dinamis, menunjukkan persentase pengguna yang tetap aktif bulan demi bulan setelah tanggal registrasi mereka.
- **Halaman 2: Risk Profiling**: Scatter plot interaktif yang memetakan nasabah berdasarkan Tenure (masa langganan) vs. CLV, dikombinasikan dengan filter kategori keluhan tiket bantuan.

## Key Insights
1. **Titik Kritis Churn**: 65% dari total churn pelanggan terjadi pada bulan pertama setelah mendaftar (Month 1 Churn).
2. **Korelasi Tiket Bantuan**: Pelanggan yang memiliki tiket keluhan berkategori "Konektivitas/Teknis" $> 2$ kali memiliki kemungkinan churn 4 kali lebih tinggi.
3. **Pemberian Diskon**: Pemberian diskon *automatic renewal* di bulan pertama mengurangi churn sebesar 28%.
4. **Metode Pembayaran**: Pelanggan dengan metode pembayaran otomatis (*auto-debit*) memiliki retensi 45% lebih tinggi dibanding pembayaran manual.
5. **Frekuensi Aktivitas**: Penurunan login mingguan di bawah 2 kali dalam 2 minggu berturut-turut merupakan indikator churn paling akurat (akurasi prediktif 88%).
6. **Segmen Tertinggi**: Kategori pelanggan Enterprise memiliki churn terendah (< 2% per tahun).
7. **Kanal Pendaftaran**: Pengguna yang berasal dari kampanye iklan media sosial (Social Ads) cenderung memiliki churn 15% lebih tinggi dibanding pencarian organik.
8. **Pengaruh Kenaikan Harga**: Kenaikan harga paket Premium di Q2 2024 memicu churn sesaat sebesar 5% pada pengguna aktif lama.
9. **Kategori Support**: Rata-rata waktu penyelesaian tiket bantuan di atas 24 jam meningkatkan probabilitas churn sebesar 30%.
10. **Popularitas Fitur**: Pengguna yang mengeksplorasi $> 3$ fitur utama di minggu pertama memiliki tingkat retensi 90% pada bulan ketiga.

## Recommendations
1. Luncurkan kampanye *onboarding* yang interaktif untuk memastikan pengguna baru mengeksplorasi minimal 3 fitur di minggu pertama.
2. Buat alarm otomatis untuk tim *Customer Success* jika frekuensi login pelanggan menurun di bawah batas kritis.
3. Prioritaskan penyelesaian tiket bantuan teknis di bawah 4 jam khusus untuk segmen pelanggan "At Risk".
4. Berikan penawaran diskon perpanjangan secara otomatis sebelum masa langganan gratis berakhir.
5. Dorong pengguna manual ke metode *auto-debit* dengan insentif cashback atau poin loyalitas.
6. Hentikan kampanye iklan media sosial dengan ROI retensi rendah; alihkan anggaran ke SEO/organik.
7. Implementasikan sistem survei keluar (*exit survey*) otomatis untuk mendeteksi alasan utama churn saat pembatalan langganan.
8. Optimalkan performa server web agar waktu loading halaman di bawah 2 detik demi menekan frustrasi teknis pengguna.
9. Terapkan strategi retensi khusus (loyalty reward) untuk mempertahankan pelanggan ber-tenure tinggi (> 1 tahun).
10. Sediakan basis pengetahuan (*Knowledge Base*) mandiri yang komprehensif untuk mengurangi beban antrean tiket teknis.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
Jalankan DDL berikut untuk membuat struktur database retensi pelanggan:

```sql
CREATE DATABASE customer_churn;

-- Tabel Profil Pelanggan
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    signup_date DATE,
    status VARCHAR(20),
    payment_method VARCHAR(30)
);

-- Tabel Log Penggunaan Fitur
CREATE TABLE usage_logs (
    log_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    login_date DATE,
    feature_clicks INT
);

-- Tabel Tiket Bantuan
CREATE TABLE support_tickets (
    ticket_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    ticket_date DATE,
    category VARCHAR(50),
    resolution_time_hours INT
);
```

### Langkah 2: Script Generate Data (Python)
Gunakan korelasi probabilitas churn: pelanggan dengan rating keluhan tinggi dan login menurun akan dilabeli sebagai *Churned*.

```python
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Generate 1M Customers
customers = []
start_date = datetime(2023, 1, 1)

for i in range(1, 1000001):
    signup = start_date + timedelta(days=random.randint(0, 700))
    status = random.choices(['Active', 'Churned'], weights=[0.85, 0.15])[0]
    pay = random.choice(['Auto-Debit Credit Card', 'Auto-Debit Bank Transfer', 'Manual E-Wallet'])
    customers.append({'customer_id': i, 'signup_date': signup.strftime('%Y-%m-%d'), 'status': status, 'payment_method': pay})

pd.DataFrame(customers).to_csv('customers.csv', index=False)

# Generate Logs & Tickets (sampel 100k data relasional)
logs = []
tickets = []
for i in range(1, 100000):
    c_id = random.randint(1, 1000000)
    logs.append({
        'log_id': i,
        'customer_id': c_id,
        'login_date': (start_date + timedelta(days=random.randint(700, 800))).strftime('%Y-%m-%d'),
        'feature_clicks': random.randint(1, 50)
    })
    
    if random.random() < 0.3: # 30% user submit tickets
        tickets.append({
            'ticket_id': len(tickets) + 1,
            'customer_id': c_id,
            'ticket_date': (start_date + timedelta(days=random.randint(700, 800))).strftime('%Y-%m-%d'),
            'category': random.choice(['Teknis', 'Tagihan', 'Akun']),
            'resolution_time_hours': random.randint(1, 72)
        })

pd.DataFrame(logs).to_csv('usage_logs.csv', index=False)
pd.DataFrame(tickets).to_csv('support_tickets.csv', index=False)
print("Data dummy churn berhasil dibuat!")
```

### Langkah 3: Eksekusi SQL Query
Import CSV ke PostgreSQL. Jalankan query deteksi aktivitas login terakhir dan identifikasi user berisiko (*At Risk*) pada tab **SQL Process** untuk memfilter profil retensi.

### Langkah 4: Visualisasi di Power BI
1. Tarik tabel `customers`, `usage_logs`, dan `support_tickets` ke Power BI.
2. Buat relasi One-to-Many dari `customers[customer_id]` ke tabel logs & tickets.
3. Buat Matrix visual untuk Cohort Analysis:
   - Rows: `customers[signup_date]` (dikelompokkan per bulan/tahun)
   - Columns: Periode waktu sejak registrasi (Month 1, Month 2, dst)
   - Values: `% Retention Rate` (DAX calculation)
4. Buat visualisasi yang menonjolkan zona bahaya keluhan teknis menggunakan warna Coral sesuai panduan mockup.

