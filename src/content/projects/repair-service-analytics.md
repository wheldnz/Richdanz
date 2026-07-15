---
title: Insurance Claims & SLA Analytics
category: data
metric: 5.4 Days TAT vs 7d SLA
metricLabel: 3.8K Claims Monitored (9 Partners)
tags: ['SQL', 'Power BI', 'SLA', 'Operations']
description: Insurance claims resolution & SLA performance monitoring pipeline, tracking 3,800+ monthly service claims across 9 insurance partners with a 5.4-day average turnaround time against a 7-day SLA target.
---

# Insurance Claims & SLA Analytics

## Business Problem
Operasional klaim perbaikan garansi asuransi perangkat keras (*hardware insurance claims*) membutuhkan pemantauan ketat terhadap batas waktu layanan (*Service Level Agreement / SLA*). Keterlambatan klaim meningkatkan angka pembatalan dan ketidakpuasan pelanggan. 

Proyek ini bertujuan untuk mengukur **Resolution Rate**, memantau **Turnaround Time (TAT)** harian (target rata-rata 5–6 hari terhadap SLA 7 hari), serta mengevaluasi tingkat *SLA Breach* di **9 Mitra Asuransi** (*Qoala, Igloo, PasarPolis, Chubb, ACA, Tokio Marine, Zurich, Allianz, BCA Insurance*) dan jaringan **9 Infinix Service Centers**.

## Dataset & Raw Data
* **Fact Table**: `fact_claims_sla` (3,840 baris klaim historis 2024–2025).
* **Dimension Tables**:
  - `dim_insurance_partners` (9 Mitra Asuransi).
  - `dim_service_centers` (9 Infinix Care & Service Partners).

## SQL ELT Process
Pemrosesan dan pembersihan string `Rp ` serta kalkulasi durasi pengerjaan dilakukan di PostgreSQL:

```sql
-- Analisis SLA Adherence % dan Rata-rata Turnaround Time (TAT) per Mitra Asuransi
SELECT 
    p.partner_name,
    COUNT(f.claim_id) AS total_claims,
    COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END) AS resolved_claims,
    ROUND(COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END) * 100.0 / COUNT(f.claim_id), 1) AS resolution_rate_pct,
    ROUND(AVG(f.turnaround_time_days), 2) AS avg_tat_days,
    ROUND(
        COUNT(CASE WHEN f.sla_status = 'Met SLA' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN f.status = 'Resolved' THEN 1 END), 0), 
        1
    ) AS sla_adherence_pct
FROM dim_insurance_partners p
JOIN fact_claims_sla f ON p.partner_id = f.partner_id
GROUP BY p.partner_name
ORDER BY avg_tat_days ASC;
```

## Dashboard Specification
- **KPI Summary**: Total Claims, Resolution Rate (90.2%), Avg Turnaround Time (5.4 Days), SLA Adherence % (92.4%).
- **SLA Breach Matrix**: Pemetaan tingkat kelambatan klaim per kota service center.
- **Partner CSAT Breakdown**: Skor kepuasan pelanggan per mitra asuransi.

## Key Insights
1. **Performa SLA**: Rata-rata *Turnaround Time (TAT)* berhasil dijaga pada angka **5.4 hari**, secara konsisten memenuhi batas SLA 7 hari.
2. **Resolution Rate**: Sebesar 90.2% klaim terselesaikan dengan tingkat kepuasan pelanggan (CSAT) rata-rata 4.4/5.0.
