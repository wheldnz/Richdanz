---
title: Enterprise Sales & Multi-Channel P&L Analytics
category: data
metric: 50K Orders & 75 Partners
metricLabel: Sales Transactions & P&L Partners
tags: ['SQL', 'Power BI', 'ETL', 'P&L', 'Python']
description: Integrated Sales & Multi-Channel Financial P&L pipeline, processing 50,000 retail orders and monitoring daily/monthly/yearly P&L across 16 Brand Partners, 9 Infinix Service Centers, and 50 Retail Partners.
---

# Enterprise Sales & Multi-Channel P&L Analytics

## Business Problem
Perusahaan ritel dan jaringan layanan teknologi menghadapi kendala besar dalam menyatukan analisis transaksi penjualan ritel dengan laporan Laba Rugi (*Profit & Loss / P&L*) di berbagai jalur distribusi (*channels*). Data keuangan dan transaksi penjualan tersebar di berbagai unit bisnis terpisah tanpa skema data terpadu (*Conformed Dimensions*). 

Proyek ini bertujuan untuk membangun jalur data analitik terintegrasi (*Unified Data Warehouse Pipeline*) guna memantau **Gross Revenue, COGS, Operating Expenses (OpEx), dan Net Profit Margin %** secara harian, bulanan, dan tahunan (2022–2025) untuk **16 Brand Partners, 9 Infinix Service Centers, dan 50 Retail Partners**.

## Dataset & Unified Data Architecture
* **Star Schema Conformed Dimensions**:
  - `dim_stores` (500 baris): Dimensi jembatan yang menghubungkan 16 Brand Partners (Samsung, Apple, Xiaomi, Infinix, dll), 9 Infinix Service Centers (Jakarta, Surabaya, Bandung, Medan, dll), dan 50 Retail Partners (Erafone, iBox, Digimap, dll).
  - `dim_products` (1,300+ baris): Hirarki katalog produk dan harga modal/jual.
  - `fact_orders` & `fact_order_items` (50,000 order historis 4 tahun 2022–2025).
  - `fact_pl_monthly` (3,600 rekap keuangan P&L bulanan).

## SQL ELT Process
Seluruh data mentah diproses di PostgreSQL menggunakan strategi Pure SQL ELT:

```sql
-- Kueri Analisis Perbandingan P&L Multi-Channel (Brand Partners vs Service Centers vs Retail Partners)
SELECT 
    p.channel_type,
    COUNT(DISTINCT p.store_id) AS total_partners,
    ROUND(SUM(f.gross_revenue_idr) / 1000000000.0, 2) AS total_revenue_miliar_idr,
    ROUND(SUM(f.gross_profit_idr) / 1000000000.0, 2) AS total_gross_profit_miliar_idr,
    ROUND(SUM(f.operating_expenses_idr) / 1000000000.0, 2) AS total_opex_miliar_idr,
    ROUND(SUM(f.net_profit_idr) / 1000000000.0, 2) AS total_net_profit_miliar_idr,
    ROUND(SUM(f.net_profit_idr) * 100.0 / NULLIF(SUM(f.gross_revenue_idr), 0), 2) AS net_margin_pct
FROM dim_stores p
JOIN fact_pl_monthly f ON p.store_id = f.store_id
GROUP BY p.channel_type
ORDER BY total_net_profit_miliar_idr DESC;
```

## Power BI & DAX Financial Formulas
Rumus DAX yang digunakan untuk laporan Laba Rugi P&L:

* **Channel Gross Revenue**:
  ```dax
  Channel Gross Revenue = SUM(fact_pl_monthly[gross_revenue_idr])
  ```
* **Channel Net Profit & Margin %**:
  ```dax
  Channel Net Profit = SUM(fact_pl_monthly[net_profit_idr])
  Channel Net Margin % = DIVIDE([Channel Net Profit], [Channel Gross Revenue], 0)
  ```

## Dashboard Layout Specification
- **Page 1: Executive Sales & Retail Performance**: KPI Summary Card (Revenue, Orders, Top Product), Filter Tanggal & Channel, Bar Chart Top Kategori.
- **Page 2: Multi-Channel P&L Financial Report**: P&L Waterfall Chart (`Gross Revenue` $\rightarrow$ `COGS` $\rightarrow$ `OpEx` $\rightarrow$ `Net Profit`), Matrix Drill-down Table per Mitra Usaha.

## Key Insights
1. **Performa Channel**: *Infinix Service Centers* mencatatkan Net Margin % tertinggi (~24%) berkat kontribusi pendapatan berbasis jasa service, sementara *Brand Partners* mendominasi volume omzet bruto terbanyak.
2. **Tren 4 Tahun (2022–2025)**: Pertumbuhan omzet stabil di angka 14% YoY dengan lonjakan penjualan Q4 rutin di seluruh jaringan Retail Partners.
