# Panduan Langkah demi Langkah Visualisasi `vw_sales_executive_dashboard` di Power BI

Dokumen ini memandu Anda membangun **Executive Sales Analytics Dashboard** di Power BI Desktop secara detail, dari koneksi BigQuery, pembuatan DAX Measures, penataan skema UI/UX, hingga pengaturan visual interaktif.

---

## 🔌 TAHAP 1: Ingest Data dari BigQuery ke Power BI Desktop

1. Buka **Power BI Desktop**.
2. Di Ribbon Home, klik **Get Data** $\rightarrow$ pilih **Google BigQuery** $\rightarrow$ klik **Connect**.
3. *Sign in* menggunakan akun Google (GCP) yang mengelola BigQuery.
4. Di jendela **Navigator**:
   - Expand project **`electracare-dw`**.
   - Expand dataset **`electracare_dwh`**.
   - Beri centang pada View **`vw_sales_executive_dashboard`**.
5. Pilih **Data Connectivity Mode**:
   - Pilih **Import** (Rekomendasi utama agar responsivitas filter cepat & kalkulasi DAX berjalan optimal).
6. Klik **Transform Data** (Power Query Editor):
   - Verifikasi tipe data:
     - `order_date` $\rightarrow$ **Date**
     - `order_month` $\rightarrow$ **Date**
     - `gross_revenue`, `total_cogs`, `gross_profit` $\rightarrow$ **Fixed Decimal Number** / **Currency**
     - `gross_margin_pct` $\rightarrow$ **Percentage** (`%`)
   - Klik **Close & Apply**.

---

## 🧮 TAHAP 2: Membuat Tabel DAX Measures (`_Measures`)

Agar penulisan rumus rapi dan mudah dipelihara:

1. Di Ribbon Home, klik **Enter Data**.
2. Beri nama tabel: `_Measures` $\rightarrow$ Klik **Load**.
3. Buat rumus DAX berikut di dalam `_Measures`:

```dax
-- 1. Total Revenue
Total Revenue = SUM(vw_sales_executive_dashboard[gross_revenue])

-- 2. Total Profit
Total Profit = SUM(vw_sales_executive_dashboard[gross_profit])

-- 3. Total Orders
Total Orders = DISTINCTCOUNT(vw_sales_executive_dashboard[order_id])

-- 4. Average Order Value (AOV)
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

-- 5. Gross Margin %
Gross Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

-- 6. Revenue Share % (Kalkulasi dinamis untuk filter)
Revenue Share % = 
DIVIDE(
    [Total Revenue], 
    CALCULATE([Total Revenue], ALLSELECTED(vw_sales_executive_dashboard)), 
    0
)
```

---

## 🎨 TAHAP 3: Pengaturan Layout Canvas & Theme

1. **Atur Ukuran Canvas**:
   - Klik di luar canvas $\rightarrow$ **Format Page** $\rightarrow$ **Canvas Settings** $\rightarrow$ Type: **16:9** (1280 x 720).
2. **Atur Background Page**:
   - Canvas Background: Warna Light Gray/Slate (`#F8FAFC`), Transparency: `0%`.
3. **Header Panel**:
   - Tambahkan **Shape (Rectangle)** di bagian paling atas (Height: 70px, Color: Dark Navy `#0F172A`).
   - Tambahkan **Text Box** di atas shape: `"PT ELECTRACARE INDONESIA - EXECUTIVE SALES ANALYTICS"` (Font: Segoe UI / Inter, Bold, White, Size: 18pt).

---

## 📊 TAHAP 4: Langkah demi Langkah Pembuatan Visual

### 1. Global Slicer Bar (Bagian Top Bar / Di bawah Header)
Tambahkan 4 Slicer horizontal agar pengguna bisa memfilter data:
- **Slicer 1 (Date Range)**: Field `vw_sales_executive_dashboard[order_date]` (Style: *Between*).
- **Slicer 2 (Channel Type)**: Field `vw_sales_executive_dashboard[center_type]` (Style: *Dropdown*).
- **Slicer 3 (Brand)**: Field `vw_sales_executive_dashboard[brand]` (Style: *Dropdown*).
- **Slicer 4 (Region)**: Field `vw_sales_executive_dashboard[region]` (Style: *Dropdown*).

---

### 2. Top Row: 4 KPI Cards (Metrik Utama)
Tambahkan 4 **Card Visual (New)** / Single Value Cards secara berjejer dari kiri ke kanan:

* **Card 1: Total Revenue**
  - Fields: `[Total Revenue]`
  - Category Label: Off
  - Callout Value: Format Currency (Rp), Display Units: **Millions / Billions** (contoh: Rp 14.50 M).
* **Card 2: Total Profit**
  - Fields: `[Total Profit]`
  - Callout Value: Format Currency (Rp), Display Units: **Millions / Billions**.
* **Card 3: Gross Margin %**
  - Fields: `[Gross Margin %]`
  - Callout Value: Format Percentage (`0.0%`).
* **Card 4: Average Order Value (AOV)**
  - Fields: `[Average Order Value]`
  - Callout Value: Format Currency (Rp) utuh.

---

### 3. Middle Left: Trend Sales & Profit Margin Over Time (Combo Chart)
Gunakan **Line and Stacked Column Chart**:
- **Shared X-Axis**: `vw_sales_executive_dashboard[order_month]`
- **Column Y-Axis**: `[Total Revenue]`
- **Line Y-Axis**: `[Gross Margin %]`
- **Colors**: Columns (Navy Blue `#1E3A8A`), Line (Emerald Green `#059669`).
- **Data Labels**: On (Format compact).

---

### 4. Middle Right: Kontribusi Penjualan Per Brand & Channel (Bar & Donut Chart)
1. **Clustered Bar Chart (Top Brand)**:
   - **Y-Axis**: `vw_sales_executive_dashboard[brand]`
   - **X-Axis**: `[Total Revenue]`
   - Data Labels: On.
2. **Donut Chart (Channel Distribution)**:
   - **Legend**: `vw_sales_executive_dashboard[center_type]`
   - **Values**: `[Total Revenue]`

---

### 5. Bottom Row: Matrix Profitabilitas Wilayah & Detail Outlet
Gunakan **Matrix Visual**:
- **Rows**: `vw_sales_executive_dashboard[region]` $\rightarrow$ `city` $\rightarrow$ `center_name` (Hierarchy Drill-down).
- **Values**: `[Total Orders]`, `[Total Revenue]`, `[Total Profit]`, `[Gross Margin %]`.
- **Conditional Formatting**:
  - Klik kanan pada `[Gross Margin %]` di Values field $\rightarrow$ **Conditional Formatting** $\rightarrow$ **Background Color**.
  - Atur Color Scale: Lowest Value (Merah Muda `#FEE2E2`) $\rightarrow$ Highest Value (Hijau Muda `#D1FAE5`).

---

### 6. Side Callout: Executive Business Insight Panel
Tambahkan **Text Box** dengan efek card background putih di sisi kanan bawah:

> 📌 **Executive Summary & Key Takeaways:**
> 1. **Dominasi Perangkat**: Brand Samsung & Apple menyumbang lebih dari 65% total revenue service.
> 2. **Margin Terbaik**: Service Center tipe *Main Service Center* menghasilkan margin 4.2% lebih tinggi dibanding *Authorized Repair Point*.
> 3. **Wilayah Potensial**: Region Jabodetabek & Jawa Barat mendominasi 72% volume order nasional.

---

## 🚀 TAHAP 5: Finishing & Interaktivitas (Cross-Filtering)

1. **Format Visual**: Nonaktifkan border default visual, aktifkan **Drop Shadow** tipis (Color: Dark Gray, Opacity: 10%, Blur: 5px) untuk kesan modern & terangkat (*glassmorphism style*).
2. **Uji Coba Filter**: Klik salah satu Brand di Bar Chart (misal: "Samsung"), pastikan Trend Chart dan Matrix di bawah otomatis memfilter data khusus transaksi Samsung!
