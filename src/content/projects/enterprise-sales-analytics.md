---
title: Enterprise Sales & Multi-Channel P&L Analytics
category: data
metric: 500K Orders & 25 Service Centers
metricLabel: Sales Transactions & P&L Centers
tags: ['Power BI', 'DAX', 'BigQuery', 'SQL', 'P&L', 'Sales Analytics']
description: Visualisasi & analisis finansial Laba/Rugi (P&L) Multi-Channel dan performa penjualan 500,000 order service di 25 Service Centers dan 15 Brand Partners PT ElectraCare Indonesia berbasis data mart BigQuery.
---

# Enterprise Sales & Multi-Channel P&L Analytics

## Business Problem
PT ElectraCare Indonesia membutuhkan dasbor analitik interaktif untuk memantau performa penjualan jasa perbaikan, penjualan suku cadang, dan Laba/Rugi (*Profit & Loss / P&L*) di seluruh **25 Service Centers** dan **15 Brand Partners** (Samsung, Apple, Xiaomi, OPPO, Vivo, Lenovo, ASUS, dll).

Analisis ini membaca data terkurasi langsung dari **Data Mart BigQuery (`electracare_mart.mart_service_revenue_summary`)** yang telah diproses oleh pipeline Data Engineering.

## Dataset & Mart Source
- **Source Data Mart**: `electracare-dw.electracare_mart.mart_service_revenue_summary` (DirectQuery BigQuery)
- **Cakupan Data**: 500,000 transaksi service order & rekapitulasi P&L bulanan 4 tahun (2022–2025).

## BigQuery SQL Analytics Query
```sql
SELECT 
    year_month,
    center_name,
    region,
    city,
    total_service_revenue,
    total_parts_revenue,
    total_gross_revenue,
    total_cogs,
    total_gross_profit,
    total_opex,
    total_net_profit,
    net_profit_margin_pct
FROM `electracare-dw.electracare_mart.mart_service_revenue_summary`
ORDER BY year_month DESC, total_gross_revenue DESC;
```

## Power BI & DAX Formulas
- **Gross Revenue IDR**:
  ```dax
  Total Gross Revenue = SUM(mart_service_revenue_summary[total_gross_revenue])
  ```
- **Net Profit IDR**:
  ```dax
  Total Net Profit = SUM(mart_service_revenue_summary[total_net_profit])
  ```
- **Net Margin %**:
  ```dax
  Net Profit Margin % = DIVIDE([Total Net Profit], [Total Gross Revenue], 0)
  ```

## Dashboard Layout Specification
- **Page 1: Executive Sales & Service Performance**: KPI Summary Cards (Gross Revenue, Net Profit, Orders, Avg Margin %), Filter Region & Center, Bar Chart Top Brand Partners.
- **Page 2: Multi-Channel P&L Financial Report**: P&L Waterfall Chart (`Gross Revenue` $\rightarrow$ `COGS` $\rightarrow$ `OpEx` $\rightarrow$ `Net Profit`), Matrix Drill-down per Service Center.

## Key Insights
1. **Service Center Margin**: Service Center Jakarta Pusat & Surabaya mencatatkan Net Margin % tertinggi (22.5%) berkat tingginya volume penggantian suku cadang OEM.
2. **Kategori Kontributor Omzet**: Penggantian LCD & Motherboard flagship menyumbangkan 58% dari total omzet kotor.
