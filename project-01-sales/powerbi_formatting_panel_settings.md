# Panduan Terperinci Pengaturan Panel Format (Power BI Visual Formatting Settings)

Dokumen ini berisi panduan **klik-demi-klik dan nilai spesifik di Panel Format (Format Visual)** di Power BI Desktop untuk setiap visual pada **Executive Sales Analytics Dashboard**.

---

## 📌 1. Pengaturan KPI Scorecard Cards (New Card Visual)

Gunakan visual **Card (New)** dari Visualizations Pane:

### A. Data Fields
- Drag ke zona **Data Fields**: `[Total Revenue]`, `[Total Profit]`, `[Gross Margin %]`, `[Average Order Value]`.

### B. Panel Format Visual $\rightarrow$ Callout Values
- **Apply to**: *Select All* (atau sesuaikan per metrik).
- **Font**: `Segoe UI` (atau `Inter`).
- **Font Size**: `26 pt`.
- **Bold**: `ON`.
- **Color**: `#0F172A` (Dark Slate).
- **Display Units**: `Auto` (atau `Millions` / `Billions` untuk Revenue & Profit).
- **Value Decimal Places**: `2` (contoh: `14.50 M`).

### C. Panel Format Visual $\rightarrow$ Category Label
- **Show Category Label**: `ON`.
- **Position**: `Below Value`.
- **Font**: `Segoe UI`.
- **Font Size**: `10 pt`.
- **Bold/Medium**: `Medium (500)`.
- **Color**: `#64748B` (Muted Gray).
- **Text Transform**: `UPPERCASE`.

### D. Panel Format Visual $\rightarrow$ Cards Container (Kartu Modul)
- **Shape**: `Rounded Rectangle` $\rightarrow$ **Corner Radius**: `8 px`.
- **Padding**: Top `12px`, Bottom `12px`, Left `16px`, Right `16px`.
- **Fill**: `ON` $\rightarrow$ Color: `#FFFFFF` (Pure White).
- **Border**: `OFF` (atau `ON` dengan Color `#E2E8F0`, Width `1px`).
- **Shadow**: `ON` $\rightarrow$ Preset: `Bottom Right`, Color: `#000000`, Blur: `5px`, Transparency: `90%`.

---

## 📌 2. Pengaturan Combo Chart (Monthly Revenue & Margin Trend)

Visual type: **Line and Stacked Column Chart**.

### A. Data Mapping
- **Shared X-Axis**: `vw_sales_executive_dashboard[order_month]`.
- **Column Y-Axis**: `_Measures[Total Revenue]`.
- **Line Y-Axis**: `_Measures[Gross Margin %]`.

### B. X-Axis & Y-Axis Settings
- **X-Axis**: Type `Categorical`, Font Size `9 pt`, Color `#64748B`, Title `OFF`.
- **Column Y-Axis**: Display Units `Billions`, Font Size `9 pt`, Color `#64748B`, Title `OFF`.
  - **Gridlines**: Horizontal `ON`, Line Style `Dotted`, Color `#E2E8F0`, Width `1px`.
- **Line Y-Axis (Secondary Y-Axis)**:
  - **Range**: Minimum `0`, Maximum `0.5` (50%).
  - **Values**: Format `Percentage`, Title `OFF`.

### C. Columns & Lines Color & Style
- **Columns**: Color `#1E3A8A` (Deep Indigo Navy).
- **Lines**: Color `#059669` (Emerald Green), Line Width `3 px`.
  - **Markers**: `ON` $\rightarrow$ Shape: `Circle`, Size: `5`, Marker Fill Color: `#059669`.

### D. Data Labels
- **Series - Total Revenue (Column)**: `ON` $\rightarrow$ Position: `Outside End`, Display Units: `Millions/Billions`, Font Size: `8.5 pt`, Color: `#1E293B`.
- **Series - Gross Margin % (Line)**: `ON` $\rightarrow$ Position: `Above`, Font Size: `8.5 pt`, Bold: `ON`, Color: `#059669`.

### E. General & Container
- **Title**: Text `"Monthly Revenue Trend vs Gross Margin %"`, Font Size `13 pt`, Semi-Bold, Color `#1E293B`.
- **Background Fill**: `#FFFFFF`, Corner Radius: `8 px`, Shadow `ON` (Transparency `90%`).

---

## 📌 3. Pengaturan Horizontal Bar Chart (Top Brand Revenue)

Visual type: **Clustered Bar Chart**.

### A. Data Mapping
- **Y-Axis**: `vw_sales_executive_dashboard[brand]`.
- **X-Axis**: `_Measures[Total Revenue]`.

### B. Formatting Settings
- **Y-Axis**: Font Size `10 pt`, Bold `ON`, Color `#1E293B`, Title `OFF`.
- **X-Axis**: Font Size `9 pt`, Color `#64748B`, Title `OFF`.
- **Bars Color**: Color `#2563EB` (Bright Blue).
  - **Corner Radius (Bar End)**: `4 px`.
  - **Inner Padding / Data Gap**: `20%`.
- **Data Labels**: `ON` $\rightarrow$ Position: `Inside End` atau `Outside End`, Font Size `9 pt`, Color `#FFFFFF` / `#1E293B`.
- **Title**: Text `"Revenue by Device Brand"`, Font Size `13 pt`, Color `#1E293B`.
- **Background Fill**: `#FFFFFF`, Corner Radius `8 px`, Shadow `ON`.

---

## 📌 4. Pengaturan Donut Chart (Channel Distribution)

Visual type: **Donut Chart**.

### A. Data Mapping
- **Legend**: `vw_sales_executive_dashboard[center_type]`.
- **Values**: `_Measures[Total Revenue]`.

### B. Formatting Settings
- **Slices Color**:
  - `Main Service Center`: `#1E3A8A` (Deep Indigo).
  - `Authorized Repair Point`: `#60A5FA` (Light Sky Blue).
- **Legend**: Position `Right Center`, Font Size `9.5 pt`, Color `#334155`.
- **Detail Labels**: Label Contents `Category, Percent of total`, Position `Outside`, Font Size `9 pt`.
- **Donut Hole Radius**: `60%`.
- **Title**: Text `"Revenue Contribution by Channel Type"`, Font Size `13 pt`, Color `#1E293B`.
- **Background Fill**: `#FFFFFF`, Corner Radius `8 px`, Shadow `ON`.

---

## 📌 5. Pengaturan Matrix Table (Regional Profitability)

Visual type: **Matrix**.

### A. Data Mapping
- **Rows**: `vw_sales_executive_dashboard[region]`, `city`, `center_name`.
- **Values**: `[Total Orders]`, `[Total Revenue]`, `[Total Profit]`, `[Gross Margin %]`.

### B. Formatting Settings
- **Grid Options**: Vertical Gridlines `OFF`, Horizontal Gridlines `ON` (Color `#E2E8F0`, Width `1px`), Row Padding `6px`.
- **Column Headers**: Font Size `10 pt`, Bold `ON`, Background Color `#F1F5F9`, Text Color `#0F172A`.
- **Row Headers**: Font Size `9.5 pt`, Color `#1E293B`, Stepped Layout `ON` (Indent `10px`).
- **Values**: Font Size `9.5 pt`, Text Color `#334155`.
  - **Alternating Row Color**: Primary `#FFFFFF`, Secondary `#F8FAFC`.
- **Conditional Formatting (`Gross Margin %`)**:
  - Klik kanan `[Gross Margin %]` di Values $\rightarrow$ **Conditional Formatting** $\rightarrow$ **Background Color**.
  - Format Style: `Gradient`.
  - Field: `_Measures[Gross Margin %]`.
  - Minimum (Lowest Value): Color `#FEE2E2` (Soft Light Red).
  - Middle (Custom): Color `#F3F4F6` (Soft Gray).
  - Maximum (Highest Value): Color `#D1FAE5` (Soft Emerald Green).
- **Subtotals & Totals**: Font Size `10 pt`, Bold `ON`, Background `#E2E8F0`, Text `#0F172A`.

---

## 📌 6. Pengaturan Executive Insights Callout Panel (Text Box Container)

### A. Insert & Text Formatting
1. Ribbon Insert $\rightarrow$ **Text Box**.
2. Ketik teks narasi insight bisnis.
3. Highlight Teks $\rightarrow$ Pengaturan Toolbar:
   - **Font**: `Segoe UI` (atau `Inter`).
   - **Font Size**: `10.5 pt`.
   - **Line Spacing**: `1.4 em`.
   - **Teks Header Point**: Bold `ON`, Color `#0F172A`.
   - **Teks Deskripsi**: Regular, Color `#334155`.

### B. Format Text Box Container (Panel Format)
- **Background Fill**: `ON` $\rightarrow$ Color: `#FFFFFF`.
- **Border (Garis Tepi Kartu)**:
  - Custom Border: Top `OFF`, Right `OFF`, Bottom `OFF`.
  - **Left Border ONLY**: `ON` $\rightarrow$ Color `#1E3A8A` (Deep Indigo), Width `4 px`.
- **Shadow**: `ON` $\rightarrow$ Preset `Bottom Right`, Transparency `90%`, Blur `5px`.
- **Visual Corner Radius**: Top-Left `0px`, Bottom-Left `0px`, Top-Right `8px`, Bottom-Right `8px`.
