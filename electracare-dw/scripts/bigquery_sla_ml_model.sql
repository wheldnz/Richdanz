-- ====================================================================
-- BigQuery ML Model & Prediction Table Script
-- Company: PT ElectraCare Indonesia — Enterprise Data Warehouse (EDW)
-- Project ID: electracare-dw
-- Dataset: electracare_mart
-- ====================================================================

-- 1. Create Feature Table / View for Model Training
CREATE OR REPLACE VIEW `electracare-dw.electracare_mart.v_sla_breach_training_data` AS
SELECT 
    wc.claim_key,
    wc.claim_id,
    ip.partner_name AS insurance_partner,
    ip.partner_tier,
    d.category AS device_category,
    d.subcategory AS device_subcategory,
    wc.claim_type,
    wc.damage_type,
    g.region,
    g.is_tier_1_city,
    sc.center_type,
    wc.turnaround_time_days,
    wc.total_claim_cost_idr,
    wc.repair_cost_idr,
    wc.sparepart_cost_idr,
    dt.day_of_week,
    dt.is_weekend,
    -- Target Variable: 1 if Turnaround Time > 7 days (SLA Breach), 0 if <= 7 days (Met SLA)
    IF(wc.turnaround_time_days > 7, 1, 0) AS is_sla_breached_7d
FROM `electracare-dw.electracare_dwh.fact_warranty_claims` wc
JOIN `electracare-dw.electracare_dwh.dim_insurance_partner` ip ON wc.insurance_key = ip.insurance_key
JOIN `electracare-dw.electracare_dwh.dim_device` d ON wc.device_key = d.device_key
JOIN `electracare-dw.electracare_dwh.dim_geography` g ON wc.geo_key = g.geo_key
JOIN `electracare-dw.electracare_dwh.dim_service_center` sc ON wc.center_key = sc.center_key
JOIN `electracare-dw.electracare_dwh.dim_date` dt ON wc.claim_date_key = dt.date_key
WHERE wc.status = 'Resolved';

-- 2. Train Logistic Regression Classifier Model in BigQuery ML
CREATE OR REPLACE MODEL `electracare-dw.electracare_mart.sla_breach_prediction_model`
OPTIONS(
    model_type='LOGISTIC_REG',
    input_label_cols=['is_sla_breached_7d'],
    auto_class_weights=TRUE,
    data_split_method='AUTO_SPLIT'
) AS
SELECT 
    insurance_partner,
    partner_tier,
    device_category,
    device_subcategory,
    claim_type,
    damage_type,
    region,
    is_tier_1_city,
    center_type,
    total_claim_cost_idr,
    day_of_week,
    is_weekend,
    is_sla_breached_7d
FROM `electracare-dw.electracare_mart.v_sla_breach_training_data`;

-- 3. Generate Predictions for Active/Pending Claims
CREATE OR REPLACE TABLE `electracare-dw.electracare_mart.fact_claim_sla_predictions` AS
SELECT 
    claim_key,
    claim_id,
    insurance_partner,
    device_category,
    damage_type,
    total_claim_cost_idr,
    predicted_is_sla_breached_7d AS predicted_breach_flag,
    prob.prob AS probability_breach,
    CASE 
        WHEN prob.prob >= 0.70 THEN 'CRITICAL (High Risk >7D)'
        WHEN prob.prob >= 0.40 THEN 'MEDIUM (Watchlist)'
        ELSE 'LOW RISK (SLA Safe)'
    END AS risk_category,
    CURRENT_TIMESTAMP() AS predicted_at
FROM ML.PREDICT(
    MODEL `electracare-dw.electracare_mart.sla_breach_prediction_model`,
    (SELECT * FROM `electracare-dw.electracare_mart.v_sla_breach_training_data`)
),
UNNEST(predicted_is_sla_breached_7d_probs) AS prob
WHERE prob.label = 1;
