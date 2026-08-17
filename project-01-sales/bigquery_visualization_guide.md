# Panduan Integrasi BigQuery & Panduan Visualisasi Sales Analytics Professional

Dokumen ini berisi panduan *end-to-end* pembuatan Dashboard Sales Analytics berstandar enterprise yang terhubung langsung ke **Google BigQuery**, dari tahap persiapan query, pemodelan data visual, desain UI/UX dashboard, formulasi metrik, hingga cara mengekstraksi *actionable business insight*.

---

## 📌 Langkah 1: Data Preparation & View Creation di BigQuery

Untuk memastikan visualisasi cepat, hemat *query cost* BigQuery, dan siap konsumsi BI Tool (Looker Studio / Power BI), buat **Analytical View / Summary Table** di BigQuery.

### 1.1 SQL View: Unified Sales & Financial View (`vw_sales_executive_dashboard`)

```sql
CREATE OR REPLACE VIEW `your_project.sales_dataset.vw_sales_executive_dashboard` AS
WITH base_orders AS (
  SELECT
    o.order_id,
    o.order_date,
    o.store_id,
    s.store_name,
    s.channel_type,
    s.city,
    s.region,
    oi.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    p.unit_price,
    p.cost_price,
    (oi.quantity * p.unit_price) AS gross_revenue,
    (oi.quantity * p.cost_price) AS total_cogs,
    (oi.quantity * (p.unit_price - p.cost_price)) AS gross_profit
  FROM `your_project.sales_dataset.fact_orders` o
  JOIN `your_project.sales_dataset.fact_order_items` oi ON o.order_id = oi.order_id
  JOIN `your_project.sales_dataset.dim_products` p ON oi.product_id = p.product_id
  JOIN `your_project.sales_dataset.dim_stores` s ON o.store_id = s.store_id
)
SELECT
  order_id,
  order_date,
  DATE_TRUNC(order_date, MONTH) AS order_month,
  EXTRACT(YEAR FROM order_date) AS order_year,
  store_id,
  store_name,
  channel_type,
  city,
  region,
  product_id,
  product_name,
  category,
  quantity,
  unit_price,
  cost_price,
  gross_revenue,
  total_cogs,
  gross_profit,
  SAFE_DIVIDE(gross_profit, gross_revenue) AS gross_margin_pct
FROM base_orders;
```

---

## 🔌 Langkah 2: Menghubungkan BigQuery ke BI Tools

### Opsi A: Google Looker Studio (Rekomendasi Native GCP)
1. Buka [Looker Studio](https://lookerstudio.google.com).
2. Klik **Create** $\rightarrow$ **Data Source** $\rightarrow$ Pilih **BigQuery**.
3. Pilih **Project Name** $\rightarrow$ **Dataset** $\rightarrow$ **Custom Query** atau pilih View `vw_sales_executive_dashboard`.
4. Untuk performa maksimal & biaya efisien:
   - Gunakan **DirectQuery** dengan parameter tanggal `@DS_START_DATE` & `@DS_END_DATE`.
   - Atau aktifkan **Extract Data** / Scheduled Refresh jika dataset sangat besar (>10 juta baris).

### Opsi B: Power BI Desktop
1. Buka Power BI $\rightarrow$ `Get Data` $\rightarrow$ `More...` $\rightarrow$ Pilih **Google BigQuery**.
2. Sign in dengan akun GCP yang memiliki akses *BigQuery Data Viewer*.
3. Pilih opsi **Import** (untuk responsivitas cepat & kalkulasi DAX komplek) atau **DirectQuery** (untuk real-time data tanpa menyimpan lokal).
4. Load tabel View `vw_sales_executive_dashboard`.

---

## 🎨 Langkah 3: Menentukan Arsitektur & Layout Dashboard (3-Page Structure)

Dashboard profesional menggunakan hirarki informasi **F-Pattern / Z-Pattern** (Informasi penting berada di kiri atas):

```
+-------------------------------------------------------------------------------+
| TOP BAR: Filters (Date Range Selector | Channel Slicer | Region | Category)  |
+-------------------------------------------------------------------------------+
| KPI SCORECARDS (4 Metric Utama):                                              |
| [ Total Revenue ]  [ Gross Profit ]  [ Net Profit Margin % ]  [ AOV ]          |
+-------------------------------------------------------------------------------+
| MAIN VISUALS (2 Column Layout):                                               |
| Left (60% width): Revenue & Profit Trend Over Time (Combo Bar & Line)         |
| Right (40% width): Channel / Region Sales Distribution (Donut / Horizontal)   |
+-------------------------------------------------------------------------------+
| DETAILED BREAKDOWN (Full Width Table / Matrix):                               |
| Top N Products / Stores with Sparklines & Conditional Formatting             |
+-------------------------------------------------------------------------------+
```

### Struktur Halaman Dashboard:
1. **Page 1: Executive Sales Overview**
   - KPI Scorecards: Revenue, Profit, Order Volume, AOV.
   - Monthly Revenue & Gross Margin Trend (Line + Bar Chart).
   - Sales Breakdown by Channel & Region.
   - Top 10 Best Selling Products.
2. **Page 2: Product & Pareto Performance**
   - Pareto Analysis Chart (80/20 Rule: Produk penyumbang 80% revenue).
   - Category Profitability Matrix (Bubble chart: Margin % vs Revenue).
   - Slow Moving & Low Margin Product Table.
3. **Page 3: Store & Regional Deep-Dive (P&L Level)**
   - Regional Sales & Profitability Map / Heatmap.
   - P&L Waterfall Chart (Gross Revenue $\rightarrow$ COGS $\rightarrow$ OpEx $\rightarrow$ Net Profit).
   - Store Profitability Matrix dengan Conditional Formatting.

---

## 📐 Langkah 4: Panduan Standar UI/UX Visualisasi Profesional

1. **Color Palette Standard**:
   - **Primary Neutral**: Dark Slate (`#0F172A`) atau Pure White background (`#F8FAFC`).
   - **Accent / Primary Bar**: Indigo Navy (`#1E3A8A` / `#2563EB`).
   - **Positive / Growth**: Emerald Green (`#059669`).
   - **Negative / Alert**: Crimson Rose (`#DC2626`).
   - **Secondary / Comparison**: Slate Gray (`#64748B`).
   *Aturan*: Maksimal 3 warna utama dalam 1 visual agar tidak *cluttered*.

2. **Typography & Formatting**:
   - Font Family: *Inter*, *Roboto*, atau *Segoe UI*.
   - Format Angka ringkas: Gunakan *Compact Number* (contoh: Rp 1,45 Miliar atau $ 1.45M), bukan Rp 1.450.321.000 di Scorecard.

3. **Interactive Elements**:
   - Sertakan Global Date Slicer di bagian header atas.
   - Aktifkan **Cross-filtering & Drill-down** (misal klik Kategori Produk langsung memfilter Trend Chart).

---

## 🧮 Langkah 5: Formulasi Metrik Kunci (Calculated Fields / DAX)

| Nama Metrik | Formulasi (Looker Studio / DAX) | Fungsi Bisnis |
| :--- | :--- | :--- |
| **Total Revenue** | `SUM(gross_revenue)` | Mengukur total nilai penjualan kotor |
| **Gross Profit** | `SUM(gross_profit)` | Mengukur margin laba sebelum opEx |
| **Gross Margin %** | `SUM(gross_profit) / SUM(gross_revenue)` | Mengukur efisiensi HPP / COGS |
| **AOV (Avg Order Value)** | `SUM(gross_revenue) / COUNT_DISTINCT(order_id)` | Mengukur rerata pembelanjaan per transaksi |
| **MoM Growth %** | `(Revenue Current Month - Revenue Previous Month) / Revenue Previous Month` | Mengukur laju pertumbuhan bulanan |

---

## 💡 Langkah 6: Ekstraksi Business Insight & Rekomendasi Aksionabel

Visualisasi profesional harus disertai dengan ringkasan **Data Storytelling & Business Insight** di bagian atas/sisi dashboard. Contoh insight dari data sales:

1. **Insight Dominasi Produk (Pareto 80/20)**:
   - *Temuan*: 15% dari total SKU Produk menghasilkan 78% total gross revenue enterprise.
   - *Rekomendasi*: Amankan *stock buffer* untuk Top 15% SKU ini dan optimalkan strategi pembalakan stok (vendor negotiation).

2. **Insight Channel Margin Anomaly**:
   - *Temuan*: Penjualan di channel *Retail Partners* memiliki omzet tertinggi ($62%), namun memiliki *Gross Margin %* terendah (18%) dibanding *Brand Partners* (35%).
   - *Rekomendasi*: Tinjau ulang struktur komisi/diskon ke Retail Partners dan tingkatkan direct-to-consumer lewat Brand Partner stores.

3. **Insight Musim & Trajektori Pertumbuhan (MoM)**:
   - *Temuan*: Terjadi penurunan MoM 12% pada Q3 di wilayah Jawa Barat akibat penurunan volume transaksi produk kategori Electronics.
   - *Rekomendasi*: Jalankan promosi bundling produk aksesoris di wilayah Jawa Barat untuk meningkatkan AOV dan memulihkan margin Q4.

---

## 🚀 Check-List Kesiapan Dashboard Sebelum Publish
- [ ] Apakah angka di Scorecard sudah cocok dengan query rujukan SQL BigQuery?
- [ ] Apakah warna visual konsisten di seluruh halaman?
- [ ] Apakah filter tanggal dan Slicer Channel berfungsi tanpa membingungkan relasi data?
- [ ] Apakah angka uang disajikan dalam format ringkas (K, M, B / Ribu, Juta, Miliar)?
- [ ] Apakah terdapat Executive Summary / Key Takeaways di halaman depan?
