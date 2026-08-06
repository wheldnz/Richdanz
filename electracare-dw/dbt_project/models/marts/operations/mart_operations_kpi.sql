select 
    d.year_month,
    sc.center_name,
    count(wc.claim_key) as total_claims,
    count(case when wc.status = 'Resolved' then 1 end) as resolved_claims,
    round(count(case when wc.status = 'Resolved' then 1 end) * 100.0 / nullif(count(wc.claim_key), 0), 1) as resolution_rate_pct,
    round(avg(wc.turnaround_time_days), 2) as avg_tat_days,
    round(count(case when wc.sla_status = 'Met SLA' then 1 end) * 100.0 / nullif(count(case when wc.status = 'Resolved' then 1 end), 0), 1) as sla_adherence_pct,
    round(avg(wc.csat_rating), 2) as avg_csat
from electracare_dwh.fact_warranty_claims wc
join electracare_dwh.dim_date d on wc.claim_date_key = d.date_key
join electracare_dwh.dim_service_center sc on wc.center_key = sc.center_key
group by d.year_month, sc.center_name
