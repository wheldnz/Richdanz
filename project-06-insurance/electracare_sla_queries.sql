-- ====================================================================
-- BigQuery Analytics Queries: Sub-Insurance SLA & Claim Performance
-- Company: PT ElectraCare Indonesia — Enterprise Data Warehouse (EDW)
-- Database: BigQuery dataset `electracare_dwh` & `electracare_mart`
-- ====================================================================

-- 1. SLA Breach Rate & TAT Summary per Insurance Partner & Sub-Category
SELECT 
    ip.partner_name AS insurance_partner,
    d.category AS device_category,
    wc.damage_type,
    COUNT(wc.claim_key) AS total_claims,
    COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) AS total_sla_breached,
    ROUND(COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) * 100.0 / NULLIF(COUNT(wc.claim_key), 0), 2) AS sla_breach_rate_pct,
    ROUND(AVG(wc.turnaround_time_days), 1) AS avg_tat_days,
    ROUND(SUM(wc.total_claim_cost_idr), 0) AS total_claim_payout_idr
FROM `electracare-dw.electracare_dwh.fact_warranty_claims` wc
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip ON wc.insurance_key = ip.insurance_key
JOIN `electracare-dw.electracare_dwh.dim_device` d ON wc.device_key = d.device_key
WHERE wc.status = 'Resolved'
GROUP BY ip.partner_name, d.category, wc.damage_type
ORDER BY sla_breach_rate_pct DESC;

-- 2. Monthly Trend & Window Function (MoM Change of SLA Breach Rate)
WITH monthly_sla AS (
    SELECT 
        dt.year_month,
        COUNT(wc.claim_key) AS total_resolved_claims,
        COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) AS breach_claims,
        ROUND(COUNT(CASE WHEN wc.turnaround_time_days > 7 THEN 1 END) * 100.0 / NULLIF(COUNT(wc.claim_key), 0), 2) AS breach_rate_pct
    FROM `electracare-dw.electracare_dwh.fact_warranty_claims` wc
    JOIN `electracare-dw.electracare_dwh.dim_date` dt ON wc.claim_date_key = dt.date_key
    WHERE wc.status = 'Resolved'
    GROUP BY dt.year_month
)
SELECT 
    year_month,
    total_resolved_claims,
    breach_claims,
    breach_rate_pct,
    LAG(breach_rate_pct, 1) OVER (ORDER BY year_month) AS prev_month_breach_rate,
    ROUND(breach_rate_pct - LAG(breach_rate_pct, 1) OVER (ORDER BY year_month), 2) AS mom_breach_change_pts
FROM monthly_sla
ORDER BY year_month;

-- 3. High Risk Pending Claims (Early Warning System from BigQuery ML Model)
SELECT 
    p.claim_id,
    p.insurance_partner,
    p.device_category,
    p.damage_type,
    p.total_claim_cost_idr,
    ROUND(p.probability_breach * 100, 1) AS breach_risk_pct,
    p.risk_category
FROM `electracare-dw.electracare_mart.fact_claim_sla_predictions` p
WHERE p.risk_category = 'CRITICAL (High Risk >7D)'
ORDER BY p.probability_breach DESC
LIMIT 50;
