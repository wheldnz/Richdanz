# Panduan Lengkap Power BI: Multi-Channel P&L Executive Dashboard

Tutorial ini memandu Anda membuat **Multi-Channel Profit & Loss (P&L) Dashboard** profesional di Power BI Desktop, mencakup **16 Brand Partners, 9 Infinix Service Centers, dan 50 Retail Partners**.

---

## 🛠️ LANGKAH 1: Rumus DAX Keuangan P&L (P&L Measures)

Buat tabel `_PL_Measures` di Power BI dan tambahkan rumus-rumus DAX finansial berikut:

### 1. Total Pendapatan Kotor (Gross Revenue)
```dax
Total Gross Revenue = SUM(fact_pl_monthly[gross_revenue_idr])
```

### 2. Total Harga Pokok Penjualan (COGS / Modal Produk)
```dax
Total COGS = SUM(fact_pl_monthly[cogs_idr])
```

### 3. Laba Kotor (Gross Profit)
```dax
Total Gross Profit = [Total Gross Revenue] - [Total COGS]
```

### 4. Beban Operasional (Operating Expenses / OpEx)
```dax
Total OpEx = SUM(fact_pl_monthly[operating_expenses_idr])
```

### 5. Laba Bersih (Net Profit)
```dax
Total Net Profit = [Total Gross Profit] - [Total OpEx]
```

### 6. Persentase Marjin Laba Bersih (Net Margin %)
```dax
Net Profit Margin % = DIVIDE([Total Net Profit], [Total Gross Revenue], 0)
```

---

## 📐 LANGKAH 2: Tata Letak & Struktur Visual Dashboard P&L

### 1. Panel Atas (Executive Summary Cards)
Gunakan visual **Card (New)** atau **Multi-row Card**:
- **Gross Revenue**: `Rp XXX Miliar`
- **Gross Profit**: `Rp XXX Miliar`
- **Operating Expenses**: `Rp XXX Miliar`
- **Net Profit**: `Rp XXX Miliar` (Warna Aksen Hijau Emerald jika Positif)
- **Net Margin %**: `XX.X%`

---

### 2. Visual Utama 1: P&L Waterfall Chart (Laporan Arus Laba Rugi)
*Fungsi: Memvisualisasikan pengurangan dari Pendapatan Kotor $\rightarrow$ COGS $\rightarrow$ OpEx $\rightarrow$ Laba Bersih.*

- Pilih visual **Waterfall Chart**.
- **Category**: Masukkan nama struktur P&L.
- **Y-Axis**: Masukkan `[Total Gross Revenue]`, `- [Total COGS]`, dan `- [Total OpEx]`.
- **Hasil**: Direksi dapat melihat dengan sangat jelas bagaimana pendapatan kotor terkikis oleh modal dan operasional hingga menjadi Laba Bersih.

---

### 3. Visual Utama 2: Matrix Table P&L per Channel & Partner
*Fungsi: Menampilkan laporan P&L lengkap dengan fitur Hierarki Drill-Down (Channel $\rightarrow$ Partner Name).*

- Pilih visual **Matrix**.
- **Rows**: 
  1. `dim_partners[channel_type]` (Brand Partner, Infinix Service Center, Retail Partner)
  2. `dim_partners[partner_name]`
- **Columns**: `fact_pl_monthly[month_date]` (Year & Month)
- **Values**:
  - `[Total Gross Revenue]`
  - `[Total Gross Profit]`
  - `[Total Net Profit]`
  - `[Net Profit Margin %]`
- **Formatting Sentuhan Emas**: Aktifkan ikon **(+) Expand** pada baris Matrix untuk memungkinkan pengguna men-drill-down dari tipe channel ke nama mitra spesifik!

---

### 4. Visual Utama 3: Perbandingan Marjin Keuntungan Antar Channel (Clustered Bar Chart)
- **Y-Axis**: `dim_partners[channel_type]`
- **X-Axis**: `[Net Profit Margin %]`
- **Formatting**: Beri warna kontras:
  - **Infinix Service Center**: Warna Cyan/Teal (Margin jasa tinggi ~25%)
  - **Brand Partner**: Warna Indigo Blue (Volume besar ~15%)
  - **Retail Partner**: Warna Amber Orange (Margin retail ~8%)

---

## 🚀 Fitur Interaktif Tambahan (Level Expert)

### 1. Top Partner Performance Slicer
Tambahkan Slicer `dim_partners[channel_type]` dalam bentuk **Tile / Button Horizontal** di bagian header. Pengguna bisa mengklik tombol:
`[ ALL CHANNELS ]` | `[ 16 BRAND PARTNERS ]` | `[ 9 INFINIX SERVICE CENTERS ]` | `[ 50 RETAIL PARTNERS ]`

Seluruh grafik dan angka P&L di layar akan otomatis memfilter sesuai channel yang dipilih!
