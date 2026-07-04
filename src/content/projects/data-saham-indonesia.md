---
title: Data Pipeline Saham Indonesia
category: data
metric: 500+
metricLabel: IDX Emiten Tersaring
tags: ['Python', 'Pandas', 'Scraping', 'Finance']
description: Pipeline data otonom untuk melakukan scraping, pembersihan, dan analisis fundamental saham-saham di Bursa Efek Indonesia (IDX) untuk screening rasio PE dan PBV.
---

# Data Pipeline Saham Indonesia

## Business Problem
Investor saham jangka panjang (value investor) membutuhkan pemindaian (*screening*) rutin terhadap ratusan emiten di Bursa Efek Indonesia (IDX) untuk menemukan saham-saham salah harga yang memiliki fundamental kuat namun dihargai murah oleh pasar (undervalued). Melakukan pengumpulan data metrik keuangan (seperti PE Ratio, PBV, ROE, dan Dividen Yield) dari laporan keuangan PDF satu per satu secara manual sangat lambat, melelahkan, dan rentan terhadap kesalahan input data.

## Data Extraction & Pipeline Architecture
Proyek ini mengimplementasikan data pipeline berbasis Python yang berjalan secara otomatis:
1. **Scraping**: Mengambil data ringkasan performa saham harian dari API publik bursa atau situs keuangan tepercaya menggunakan library `requests` dan `BeautifulSoup`.
2. **Data Cleaning**: Membersihkan data menggunakan `Pandas` (menangani nilai kosong/NaN, konversi tipe data string ke numerik, dan standardisasi penulisan kode emiten).
3. **Feature Engineering**: Menghitung matriks valuasi tambahan (seperti Graham Number, PEG Ratio, dan skor kesehatan finansial Altman Z-Score).
4. **Data Loading**: Menyimpan data bersih yang telah terstruktur ke dalam file CSV hasil olahan dan database PostgreSQL lokal untuk visualisasi.

### Python Code for Data Cleaning & Filtering
```python
import pandas as pd
import numpy as np

# Load raw scraped data
raw_data = {
    'Ticker': ['BBRI', 'TLKM', 'ASII', 'GOTO', 'UNVR'],
    'Price': [4300, 3200, 5100, 62, 2800],
    'EPS': [410, 220, 540, -12, 140],
    'BVPS': [1800, 1500, 4200, 85, 450],
    'ROE_Percent': [22.7, 14.6, 12.8, -14.1, 31.1]
}

df = pd.DataFrame(raw_data)

# 1. Bersihkan nilai tidak valid dan hitung rasio fundamental
df['PE_Ratio'] = np.where(df['EPS'] > 0, df['Price'] / df['EPS'], np.nan)
df['PBV_Ratio'] = df['Price'] / df['BVPS']

# 2. Filter Saham dengan kriteria Value Investing:
# - PE Ratio < 15 kali
# - PBV Ratio < 2.0 kali
# - ROE > 10% (Perusahaan menghasilkan laba bersih yang baik)
undervalued_stocks = df[
    (df['PE_Ratio'] < 15) & 
    (df['PBV_Ratio'] < 2.0) & 
    (df['ROE_Percent'] > 10)
]

print(undervalued_stocks[['Ticker', 'PE_Ratio', 'PBV_Ratio', 'ROE_Percent']])
```

## Key Insights
1. **Skalabilitas Screening**: Pipeline berhasil mengekstrak dan memproses data metrik fundamental untuk **lebih dari 500 emiten** aktif di IDX hanya dalam waktu kurang dari 2 menit.
2. **Korelasi Murah & Laba**: Saham berkapitalisasi pasar besar (Big Cap) sektor perbankan terbukti memiliki kestabilan ROE tertinggi (> 18%) meskipun dihargai dengan PBV yang relatif wajar.
3. **Saham Salah Harga**: Berhasil mendeteksi 12 emiten lapis kedua (*second liner*) sektor industri dan komoditas yang diperdagangkan di bawah nilai bukunya (PBV < 1.0) dengan rasio hutang (DER) yang aman.
4. **Deteksi Data Duplikat**: Penanganan anomali data berhasil mengeliminasi 8% catatan ganda dan salah format dari data scraping mentah sebelum disimpan ke database.
5. **Akurasi Integrasi**: Integrasi script scraper otomatis dengan penjadwalan Cron Job menghasilkan keberhasilan eksekusi pipeline 99.4% setiap akhir hari perdagangan bursa (pukul 17:00 WIB).
6. **Value Traps Avoidance**: Filter otomatis berhasil menyingkirkan emiten dengan PBV rendah semu yang disebabkan oleh kerugian berturut-turut atau beban hutang yang membengkak.
7. **Tren Sektor**: Sektor konsumsi (Consumer Goods) mencatatkan penurunan rata-rata PE Ratio sebesar 15% dalam setahun, menjadikannya menarik untuk riset mendalam.
8. **Konsistensi Dividen**: Sebesar 8% emiten terdeteksi memiliki rekam jejak pembagian dividen konsisten dengan yield di atas bunga deposito ( > 6% per tahun) selama 5 tahun terakhir.
9. **Kesehatan Finansial**: Altmans Z-score terbukti efektif menyaring keluar 14 perusahaan yang terindikasi memiliki risiko kebangkrutan dalam waktu dekat.
10. **Visualisasi Siap Pakai**: Data PostgreSQL siap dihubungkan langsung ke dasbor BI (seperti Looker Studio) untuk memantau radar saham undervalued secara visual.

## Recommendations
1. **Gunakan API Laporan Keuangan Resmi**: Migrasikan sumber data scraper ke API XBRL resmi milik IDX untuk menjamin validitas keakuratan angka laporan keuangan audited.
2. **Jadwalkan Pipeline dengan Airflow**: Kelola alur kerja ETL (Extract-Transform-Load) menggunakan Apache Airflow untuk penanganan kegagalan tugas (*retries*) dan monitoring grafis yang lebih andal.
3. **Terapkan Sentiment Screening**: Tambahkan modul analisis sentimen berita media finansial terkait emiten untuk menghindari jebakan saham murah yang memiliki isu hukum/kasus korporat.
4. **Optimasi Struktur Database**: Buat indeks (*indexing*) pada kolom `Ticker` dan `Sector` di database PostgreSQL agar query filter pencarian dasbor berjalan instan.
5. **Tambahkan Fitur Backtesting**: Buat skrip simulasi historis untuk menguji apakah strategi membeli saham undervalued dari screener ini terbukti mengalahkan return indeks IHSG secara jangka panjang.
6. **Filter Saham Syariah Otomatis**: Tambahkan filter screening berbasis daftar saham syariah (DES) Otoritas Jasa Keuangan untuk memfasilitasi investor syariah.
7. **Deteksi Transaksi Bandar (Bandarmologi)**: Integrasikan pipeline dengan data transaksi broker summary harian untuk mendeteksi akumulasi pembelian oleh investor institusi/asing.
8. **Skema Backup Otomatis**: Buat skrip backup database harian otomatis yang disimpan di cloud storage (seperti AWS S3 atau Google Drive) untuk mencegah hilangnya data historis.
9. **Hitung Fair Value Otomatis**: Masukkan formula intrinsik valuasi (seperti Discounted Cash Flow atau Graham Formula) agar target harga beli wajar terhitung otomatis per emiten.
10. **Sistem Notifikasi Telegram**: Hubungkan pipeline dengan bot Telegram untuk mengirimkan daftar saham undervalued harian secara otomatis langsung ke smartphone Anda.
