# Design System & UI/UX Style Guide: Enterprise Sales Analytics Dashboard

Dokumen ini menjelaskan secara terperinci seluruh **sistem desain, filosofi estetik, skema warna, tipografi, grid layout, dan standar data visualisasi** yang digunakan dalam membangun **Power BI / Web Executive Sales Analytics Dashboard**.

---

## 🏛️ 1. Filosofi Desain & Estetika (Executive Clean & Modern Card UI)

Dashboard ini mengusung pendekatan **Executive Minimalist & Modern Soft-Card UI**:
- **Bebas Visual Noise**: Menghilangkan garis kisi (*gridlines*) yang terlalu kontras dan border tebal yang mengganggu mata.
- **Kognisi 5-Detik (5-Second Rule)**: Desain disusun agar level C-Suite / Eksekutif dapat menangkap kesehatan bisnis (Revenue, Profit, Margin) dalam kurun waktu kurang dari 5 detik saat pertama kali membuka dashboard.
- **Card-Container Hierarchy**: Setiap kelompok informasi dibungkus dalam wadah karton (*card container*) putih ber-corner radius lembut dengan bayangan tipis (*subtle elevation*).

---

## 🎨 2. Sistem Skema Warna (Color Palette System & HSL Values)

Pemilihan warna tidak dilakukan secara acak, melainkan menggunakan skema warna psikologi finansial & *corporate trust*:

| Fungsi Warna | Nama Warna | Kode Hex | Kode HSL | Penggunaan di Visual |
| :--- | :--- | :--- | :--- | :--- |
| **Canvas Background** | Slate White | `#F8FAFC` | `hsl(210, 40%, 98%)` | Background utama seluruh halaman dashboard |
| **Header Bar** | Deep Slate Navy | `#0F172A` | `hsl(222, 47%, 11%)` | Top Navigation & Header Bar utama |
| **Card Container** | Pure Crisp White | `#FFFFFF` | `hsl(0, 0%, 100%)` | Modul latar belakang setiap visual chart |
| **Primary Metric Bar** | Deep Royal Indigo | `#1E3A8A` | `hsl(224, 64%, 33%)` | Batang utama pada Combo Chart & Bar Chart |
| **Secondary Accent** | Bright Blue | `#2563EB` | `hsl(217, 91%, 60%)` | Donut Chart slice & Highlight elemen aktif |
| **Profit & Growth** | Emerald Green | `#059669` | `hsl(160, 84%, 39%)` | Line Margin %, Indikator positif, Heatmap max |
| **Alert / Warning** | Crimson Rose | `#DC2626` | `hsl(0, 72%, 51%)` | Indikator margin rendah / Heatmap min |
| **Secondary Text** | Slate Muted Gray | `#64748B` | `hsl(215, 16%, 47%)` | Subtitle, label kategori, dan keterangan axis |

---

## ✍️ 3. Skala Tipografi & Hirarki Teks (Typography System)

Menggunakan tipe huruf **Sans-Serif Modern** (*Inter*, *Segoe UI*, atau *Roboto*) yang memiliki *x-height* tinggi untuk memastikan angka-angka keuangan mudah dibaca tanpa salah interpretasi:

1. **Header Title (Judul Utama Dashboard)**:
   - Font Weight: `Bold (700)` | Size: `18pt - 20pt` | Color: `#FFFFFF`
   - Letter Spacing: `+0.5px` (Wide uppercase style)

2. **KPI Scorecard Main Value (Angka Metrik Kunci)**:
   - Font Weight: `Extra Bold (800)` | Size: `26pt - 28pt` | Color: `#0F172A`
   - Format Angka: Compact (`Rp 14.50 B` / `26.2%`), tidak menampilkan desimal panjang di angka triliun/miliar.

3. **KPI Scorecard Sub-Label (Keterangan Metrik)**:
   - Font Weight: `Medium (500)` | Size: `10pt` | Color: `#64748B`
   - Transform: `UPPERCASE` dengan letter spacing `+1px`.

4. **Chart Titles (Judul Modul Visual)**:
   - Font Weight: `Semi-Bold (600)` | Size: `13pt - 14pt` | Color: `#1E293B`
   - Posisi: Align Left di pojok kiri atas *card container*.

5. **Table / Data Labels & Axis Text**:
   - Font Weight: `Regular (400)` | Size: `10pt` | Color: `#334155`

---

## 📐 4. Sistem Layout Grid & Hirarki Mata (F-Pattern Layout)

Dashboard dibagi menjadi 4 tingkatan horizontal berdasar pola gerakan mata pembaca (*F-Pattern Eye Movement*):

```
+-------------------------------------------------------------------------------+
| ZONA 1: Top Navigation Bar (Header Title + Global Slicers)                   |
+-------------------------------------------------------------------------------+
| ZONA 2: Executive Summary Row (4 KPI Scorecards berjejer 1x4 Grid)             |
+-------------------------------------------------------------------------------+
| ZONA 3: Main Visual Split (Left 60%: Combo Chart | Right 40%: Bar & Donut)    |
+-------------------------------------------------------------------------------+
| ZONA 4: Operational Deep-Dive (Left 65%: Matrix Table | Right 35%: Insights)  |
+-------------------------------------------------------------------------------+
```

### Aturan Spacing & Radius:
- **Outer Margin**: 16px dari tepi canvas.
- **Card Gutter (Jarak Antar Card)**: 12px.
- **Card Border Radius**: 8px - 10px (menciptakan bentuk visual modern & bersahabat).
- **Subtle Drop Shadow**: `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)`.

---

## 📊 5. Detail Teknikal Spesifikasi Visualisasi Data

### A. Combo Chart (Monthly Revenue & Margin)
- **Primary Axis (Column)**: Menampilkan omzet kotor bulanan dengan *bar width* 65% (jarak antar batang 35%), tanpa garis bingkai batang.
- **Secondary Axis (Line)**: Menampilkan *Gross Margin %* dengan ketebalan garis 3px, menggunakan *circular data markers* di setiap titik bulan.
- **Background Grid**: Garis horizontal (*Y-axis gridlines*) diset ke *Dotted Soft Gray* (`#E2E8F0`) dengan transparansi 60%.

### B. Matrix Table & Conditional Formatting
- **Alternating Row Color**: Baris genap menggunakan *Pure White* (`#FFFFFF`), baris ganjil menggunakan *Very Soft Slate* (`#F1F5F9`).
- **Data Bar / Heatmap Margin %**:
  - Soft Red Tint (`#FEE2E2`) untuk margin di bawah 15%.
  - Neutral Gray (`#F3F4F6`) untuk margin 15% - 25%.
  - Soft Emerald Tint (`#D1FAE5`) untuk margin di atas 25%.

### C. Executive Narrative Box (Callout Panel)
- **Background**: White dengan *Left Border Accent Strip* setebal 4px berwarna Deep Indigo (`#1E3A8A`).
- **Typography**: Bullet points dengan spasi antar baris 1.4em untuk keterbacaan tinggi.

---

## ♿ 6. Standar Aksesibilitas (WCAG 2.1 AA Compliance)

1. **Rasio Kontras Warna**: Seluruh teks memiliki rasio kontras minimal **4.5:1** terhadap warna latar belakangnya (contoh: Teks `#0F172A` di atas `#FFFFFF` memiliki rasio kontras 15:1).
2. **Penggunaan Warna Bukan Satu-satunya Indikator**: Selain warna merah/hijau di heatmap, angka desimal/persentase dan panah tren tetap disertakan agar pengguna dengan keterbatasan penglihatan warna (*color blindness*) tetap dapat membaca data dengan akurat.
