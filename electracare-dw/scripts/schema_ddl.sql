-- ====================================================================
-- Enterprise Data Warehouse (EDW) DDL Schema Script
-- Company: PT ElectraCare Indonesia (Aftersales Electronics)
-- Database: db_electracare_dw
-- ====================================================================

-- 1. CREATE SCHEMAS
CREATE SCHEMA IF NOT EXISTS stg;  -- Raw staging tables
CREATE SCHEMA IF NOT EXISTS ods;  -- Operational Data Store / Cleansed
CREATE SCHEMA IF NOT EXISTS dwh;  -- Star Schema (Kimball Dimensions & Facts)
CREATE SCHEMA IF NOT EXISTS mart; -- Data Marts / Aggregates

-- Set search path
SET search_path TO dwh, public;

-- --------------------------------------------------------------------
-- 2. CONFORMED DIMENSIONS
-- --------------------------------------------------------------------

-- 2.1 Role-Playing Date Dimension
DROP TABLE IF EXISTS dwh.dim_date CASCADE;
CREATE TABLE dwh.dim_date (
    date_key INT PRIMARY KEY, -- YYYYMMDD
    full_date DATE NOT NULL,
    day_of_week SMALLINT NOT NULL, -- 1=Monday, 7=Sunday
    day_name VARCHAR(10) NOT NULL,
    day_of_month SMALLINT NOT NULL,
    day_of_year SMALLINT NOT NULL,
    week_of_year SMALLINT NOT NULL,
    month_number SMALLINT NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    month_short CHAR(3) NOT NULL,
    quarter SMALLINT NOT NULL,
    quarter_name VARCHAR(6) NOT NULL,
    year SMALLINT NOT NULL,
    fiscal_year SMALLINT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday_id BOOLEAN NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    year_quarter VARCHAR(7) NOT NULL
);

-- 2.2 Conformed Location Dimension
DROP TABLE IF EXISTS dwh.dim_geography CASCADE;
CREATE TABLE dwh.dim_geography (
    geo_key SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL, -- Jabodetabek, Jawa, Sumatera, etc.
    country VARCHAR(50) DEFAULT 'Indonesia',
    timezone VARCHAR(10) DEFAULT 'WIB',
    is_tier_1_city BOOLEAN DEFAULT FALSE
);

-- 2.3 Unified Customer Dimension
DROP TABLE IF EXISTS dwh.dim_customer CASCADE;
CREATE TABLE dwh.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(30) NOT NULL UNIQUE,
    source_system VARCHAR(20) NOT NULL, -- SERVICE, WARRANTY, INSURANCE, RETAIL
    customer_name VARCHAR(200) NOT NULL,
    phone_number VARCHAR(30),
    email VARCHAR(100),
    gender VARCHAR(10),
    age_group VARCHAR(20),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    customer_segment VARCHAR(30) DEFAULT 'Individual',
    registration_date_key INT REFERENCES dwh.dim_date(date_key),
    loyalty_tier VARCHAR(20) DEFAULT 'Bronze',
    total_lifetime_visits INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Active'
);

-- --------------------------------------------------------------------
-- 3. SUBJECT-AREA DIMENSIONS
-- --------------------------------------------------------------------

-- 3.1 Device Master Dimension
DROP TABLE IF EXISTS dwh.dim_device CASCADE;
CREATE TABLE dwh.dim_device (
    device_key SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL UNIQUE,
    device_name VARCHAR(200) NOT NULL,
    brand VARCHAR(50) NOT NULL, -- Samsung, Apple, Xiaomi, OPPO, Vivo, Lenovo, ASUS, etc.
    category VARCHAR(50) NOT NULL, -- Smartphone, Laptop, Tablet, Smartwatch, TWS
    subcategory VARCHAR(50) NOT NULL, -- Flagship, Mid-Range, Entry-Level, Gaming
    launch_year SMALLINT NOT NULL,
    msrp_idr NUMERIC(12, 2) NOT NULL,
    warranty_months SMALLINT DEFAULT 12,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3.2 Spare Parts Master Dimension
DROP TABLE IF EXISTS dwh.dim_spare_part CASCADE;
CREATE TABLE dwh.dim_spare_part (
    part_key SERIAL PRIMARY KEY,
    part_id VARCHAR(50) NOT NULL UNIQUE,
    part_name VARCHAR(200) NOT NULL,
    part_category VARCHAR(50) NOT NULL, -- LCD/Screen, Battery, IC/Chipset, Casing, Camera
    compatible_brand VARCHAR(50) NOT NULL,
    unit_cost_idr NUMERIC(12, 2) NOT NULL,
    unit_price_idr NUMERIC(12, 2) NOT NULL,
    lead_time_days INT DEFAULT 3,
    is_original BOOLEAN DEFAULT TRUE
);

-- 3.3 Service Center Dimension
DROP TABLE IF EXISTS dwh.dim_service_center CASCADE;
CREATE TABLE dwh.dim_service_center (
    center_key SERIAL PRIMARY KEY,
    center_id INT NOT NULL UNIQUE,
    center_name VARCHAR(100) NOT NULL,
    center_type VARCHAR(50) NOT NULL, -- Main Service Center, Authorized Repair Point
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    capacity_slots_per_day INT DEFAULT 50,
    opening_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3.4 Brand Partner Dimension
DROP TABLE IF EXISTS dwh.dim_brand_partner CASCADE;
CREATE TABLE dwh.dim_brand_partner (
    brand_partner_key SERIAL PRIMARY KEY,
    partner_id INT NOT NULL UNIQUE,
    partner_name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    contract_type VARCHAR(30) DEFAULT 'Authorized',
    sla_target_days INT DEFAULT 7,
    commission_pct NUMERIC(5, 2) DEFAULT 15.00
);

-- 3.5 Employee Dimension (SCD Type 2)
DROP TABLE IF EXISTS dwh.dim_employee CASCADE;
CREATE TABLE dwh.dim_employee (
    employee_key SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    employee_name VARCHAR(200) NOT NULL,
    department VARCHAR(50) NOT NULL,
    job_role VARCHAR(100) NOT NULL,
    job_level SMALLINT NOT NULL DEFAULT 1,
    certification VARCHAR(100),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    salary_idr INT NOT NULL,
    hire_date DATE NOT NULL,
    resign_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    -- SCD2 Metadata
    scd_effective_date DATE NOT NULL,
    scd_expiry_date DATE NOT NULL DEFAULT '9999-12-31',
    scd_is_current BOOLEAN NOT NULL DEFAULT TRUE
);

-- 3.6 Supplier Dimension
DROP TABLE IF EXISTS dwh.dim_supplier CASCADE;
CREATE TABLE dwh.dim_supplier (
    supplier_key SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL UNIQUE,
    supplier_name VARCHAR(100) NOT NULL,
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    supplier_type VARCHAR(30) DEFAULT 'OEM Manufacturer',
    contracted_lead_time_days INT DEFAULT 7,
    payment_terms_days INT DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3.7 Warehouse Dimension
DROP TABLE IF EXISTS dwh.dim_warehouse CASCADE;
CREATE TABLE dwh.dim_warehouse (
    warehouse_key SERIAL PRIMARY KEY,
    warehouse_id INT NOT NULL UNIQUE,
    warehouse_name VARCHAR(100) NOT NULL,
    warehouse_type VARCHAR(30) DEFAULT 'Regional Hub',
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    capacity_cbm INT DEFAULT 1000,
    cold_storage BOOLEAN DEFAULT FALSE
);

-- 3.8 Insurance Partner Dimension
DROP TABLE IF EXISTS dwh.dim_insurance_partner CASCADE;
CREATE TABLE dwh.dim_insurance_partner (
    insurance_key SERIAL PRIMARY KEY,
    partner_id INT NOT NULL UNIQUE,
    partner_name VARCHAR(100) NOT NULL,
    sla_target_days INT DEFAULT 7,
    partner_tier VARCHAR(20) DEFAULT 'Gold',
    commission_pct NUMERIC(5, 2) DEFAULT 10.00
);

-- 3.9 Insurance Policy Master Dimension
DROP TABLE IF EXISTS dwh.dim_policy CASCADE;
CREATE TABLE dwh.dim_policy (
    policy_key SERIAL PRIMARY KEY,
    policy_id INT NOT NULL UNIQUE,
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    device_key INT REFERENCES dwh.dim_device(device_key),
    insurance_key INT REFERENCES dwh.dim_insurance_partner(insurance_key),
    policy_type VARCHAR(50) NOT NULL, -- Screen Protection, Full Device, Extended Warranty
    coverage_level VARCHAR(30) DEFAULT 'Standard',
    premium_monthly_idr INT NOT NULL,
    deductible_idr INT DEFAULT 100000,
    effective_date_key INT REFERENCES dwh.dim_date(date_key),
    expiry_date_key INT REFERENCES dwh.dim_date(date_key),
    status VARCHAR(20) DEFAULT 'Active'
);

-- 3.10 Junk Dimension (Flags & Indicators)
DROP TABLE IF EXISTS dwh.dim_junk_flags CASCADE;
CREATE TABLE dwh.dim_junk_flags (
    junk_key SERIAL PRIMARY KEY,
    is_weekend_service BOOLEAN DEFAULT FALSE,
    is_repeat_customer BOOLEAN DEFAULT FALSE,
    is_warranty_covered BOOLEAN DEFAULT FALSE,
    is_insurance_covered BOOLEAN DEFAULT FALSE,
    is_sla_breach BOOLEAN DEFAULT FALSE,
    is_escalated BOOLEAN DEFAULT FALSE,
    is_original_part_used BOOLEAN DEFAULT TRUE,
    priority_level VARCHAR(10) DEFAULT 'Medium',
    service_type VARCHAR(30) DEFAULT 'Walk-in'
);

-- --------------------------------------------------------------------
-- 4. FACT TABLES
-- --------------------------------------------------------------------

-- 4.1 Fact Service Orders (Header)
DROP TABLE IF EXISTS dwh.fact_service_orders CASCADE;
CREATE TABLE dwh.fact_service_orders (
    service_order_key BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date_key INT REFERENCES dwh.dim_date(date_key),
    completion_date_key INT REFERENCES dwh.dim_date(date_key),
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    device_key INT REFERENCES dwh.dim_device(device_key),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    technician_key INT REFERENCES dwh.dim_employee(employee_key),
    brand_partner_key INT REFERENCES dwh.dim_brand_partner(brand_partner_key),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    service_category VARCHAR(50) NOT NULL,
    service_fee_idr NUMERIC(12, 2) NOT NULL DEFAULT 0,
    parts_revenue_idr NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total_revenue_idr NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total_cost_idr NUMERIC(12, 2) NOT NULL DEFAULT 0,
    profit_idr NUMERIC(12, 2) NOT NULL DEFAULT 0,
    turnaround_time_hours INT DEFAULT 0
);

-- 4.2 Fact Parts Usage (Detail Line Items)
DROP TABLE IF EXISTS dwh.fact_parts_usage CASCADE;
CREATE TABLE dwh.fact_parts_usage (
    parts_usage_key BIGSERIAL PRIMARY KEY,
    service_order_key BIGINT REFERENCES dwh.fact_service_orders(service_order_key) ON DELETE CASCADE,
    part_key INT REFERENCES dwh.dim_spare_part(part_key),
    order_date_key INT REFERENCES dwh.dim_date(date_key),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_cost_idr NUMERIC(12, 2) NOT NULL,
    unit_price_idr NUMERIC(12, 2) NOT NULL,
    line_revenue_idr NUMERIC(12, 2) NOT NULL,
    line_cost_idr NUMERIC(12, 2) NOT NULL,
    line_margin_idr NUMERIC(12, 2) NOT NULL
);

-- 4.3 Fact Monthly P&L
DROP TABLE IF EXISTS dwh.fact_service_pl_monthly CASCADE;
CREATE TABLE dwh.fact_service_pl_monthly (
    pl_key BIGSERIAL PRIMARY KEY,
    month_date_key INT REFERENCES dwh.dim_date(date_key),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    service_revenue_idr NUMERIC(15, 2) NOT NULL,
    parts_revenue_idr NUMERIC(15, 2) NOT NULL,
    gross_revenue_idr NUMERIC(15, 2) NOT NULL,
    cogs_idr NUMERIC(15, 2) NOT NULL,
    gross_profit_idr NUMERIC(15, 2) NOT NULL,
    operating_expenses_idr NUMERIC(15, 2) NOT NULL,
    net_profit_idr NUMERIC(15, 2) NOT NULL,
    net_profit_margin_pct NUMERIC(5, 2) NOT NULL
);

-- 4.4 Fact Customer Interactions
DROP TABLE IF EXISTS dwh.fact_customer_interactions CASCADE;
CREATE TABLE dwh.fact_customer_interactions (
    interaction_key BIGSERIAL PRIMARY KEY,
    interaction_date_key INT REFERENCES dwh.dim_date(date_key),
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    channel VARCHAR(30) NOT NULL,
    interaction_type VARCHAR(30) NOT NULL,
    satisfaction_score SMALLINT CHECK (satisfaction_score BETWEEN 1 AND 10)
);

-- 4.5 Fact Support Tickets
DROP TABLE IF EXISTS dwh.fact_support_tickets CASCADE;
CREATE TABLE dwh.fact_support_tickets (
    ticket_key BIGSERIAL PRIMARY KEY,
    ticket_id INT NOT NULL UNIQUE,
    ticket_date_key INT REFERENCES dwh.dim_date(date_key),
    resolution_date_key INT REFERENCES dwh.dim_date(date_key),
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    ticket_category VARCHAR(50) NOT NULL,
    resolution_time_hours INT NOT NULL DEFAULT 0,
    is_resolved BOOLEAN DEFAULT TRUE,
    is_escalated BOOLEAN DEFAULT FALSE
);

-- 4.6 Fact Spare Part Purchase Orders
DROP TABLE IF EXISTS dwh.fact_spare_part_orders CASCADE;
CREATE TABLE dwh.fact_spare_part_orders (
    po_key BIGSERIAL PRIMARY KEY,
    po_id VARCHAR(50) NOT NULL,
    po_date_key INT REFERENCES dwh.dim_date(date_key),
    supplier_key INT REFERENCES dwh.dim_supplier(supplier_key),
    warehouse_key INT REFERENCES dwh.dim_warehouse(warehouse_key),
    part_key INT REFERENCES dwh.dim_spare_part(part_key),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    order_quantity INT NOT NULL,
    received_quantity INT NOT NULL,
    unit_cost_idr NUMERIC(12, 2) NOT NULL,
    total_po_amount_idr NUMERIC(15, 2) NOT NULL,
    estimated_arrival_key INT REFERENCES dwh.dim_date(date_key),
    actual_arrival_key INT REFERENCES dwh.dim_date(date_key),
    is_on_time BOOLEAN DEFAULT TRUE,
    is_in_full BOOLEAN DEFAULT TRUE,
    delay_days INT DEFAULT 0
);

-- 4.7 Fact Inventory Snapshot
DROP TABLE IF EXISTS dwh.fact_inventory_snapshot CASCADE;
CREATE TABLE dwh.fact_inventory_snapshot (
    snapshot_key BIGSERIAL PRIMARY KEY,
    snapshot_date_key INT REFERENCES dwh.dim_date(date_key),
    warehouse_key INT REFERENCES dwh.dim_warehouse(warehouse_key),
    part_key INT REFERENCES dwh.dim_spare_part(part_key),
    quantity_on_hand INT NOT NULL DEFAULT 0,
    quantity_reserved INT NOT NULL DEFAULT 0,
    quantity_in_transit INT NOT NULL DEFAULT 0,
    reorder_point INT NOT NULL DEFAULT 10,
    days_of_supply INT NOT NULL DEFAULT 30
);

-- 4.8 Fact Employee Attendance
DROP TABLE IF EXISTS dwh.fact_employee_attendance CASCADE;
CREATE TABLE dwh.fact_employee_attendance (
    attendance_key BIGSERIAL PRIMARY KEY,
    work_date_key INT REFERENCES dwh.dim_date(date_key),
    employee_key INT REFERENCES dwh.dim_employee(employee_key),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    overtime_hours NUMERIC(4, 2) DEFAULT 0,
    devices_repaired INT DEFAULT 0,
    is_present BOOLEAN DEFAULT TRUE
);

-- 4.9 Fact Warranty Claims & SLA
DROP TABLE IF EXISTS dwh.fact_warranty_claims CASCADE;
CREATE TABLE dwh.fact_warranty_claims (
    claim_key BIGSERIAL PRIMARY KEY,
    claim_id VARCHAR(50) NOT NULL UNIQUE,
    claim_date_key INT REFERENCES dwh.dim_date(date_key),
    approval_date_key INT REFERENCES dwh.dim_date(date_key),
    completion_date_key INT REFERENCES dwh.dim_date(date_key),
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    device_key INT REFERENCES dwh.dim_device(device_key),
    insurance_key INT REFERENCES dwh.dim_insurance_partner(insurance_key),
    center_key INT REFERENCES dwh.dim_service_center(center_key),
    brand_partner_key INT REFERENCES dwh.dim_brand_partner(brand_partner_key),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    claim_type VARCHAR(30) NOT NULL,
    damage_type VARCHAR(50) NOT NULL,
    turnaround_time_days INT NOT NULL,
    sla_target_days INT DEFAULT 7,
    repair_cost_idr NUMERIC(12, 2) NOT NULL,
    sparepart_cost_idr NUMERIC(12, 2) NOT NULL,
    total_claim_cost_idr NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Resolved',
    sla_status VARCHAR(30) DEFAULT 'Met SLA',
    csat_rating SMALLINT CHECK (csat_rating BETWEEN 1 AND 5)
);

-- 4.10 Fact Device Protection Insurance
DROP TABLE IF EXISTS dwh.fact_device_protection CASCADE;
CREATE TABLE dwh.fact_device_protection (
    protection_claim_key BIGSERIAL PRIMARY KEY,
    claim_date_key INT REFERENCES dwh.dim_date(date_key),
    policy_key INT REFERENCES dwh.dim_policy(policy_key),
    customer_key INT REFERENCES dwh.dim_customer(customer_key),
    device_key INT REFERENCES dwh.dim_device(device_key),
    insurance_key INT REFERENCES dwh.dim_insurance_partner(insurance_key),
    geo_key INT REFERENCES dwh.dim_geography(geo_key),
    junk_key INT REFERENCES dwh.dim_junk_flags(junk_key),
    claim_amount_idr NUMERIC(15, 2) NOT NULL,
    premium_snapshot_idr INT NOT NULL,
    deductible_paid_idr INT DEFAULT 0,
    claim_status VARCHAR(20) DEFAULT 'Approved',
    loss_ratio NUMERIC(5, 2) NOT NULL,
    fraud_score NUMERIC(3, 2) DEFAULT 0.05
);

-- --------------------------------------------------------------------
-- 5. PERFORMANCE INDEXES
-- --------------------------------------------------------------------

CREATE INDEX idx_service_orders_date ON dwh.fact_service_orders(order_date_key);
CREATE INDEX idx_service_orders_cust ON dwh.fact_service_orders(customer_key);
CREATE INDEX idx_service_orders_center ON dwh.fact_service_orders(center_key);

CREATE INDEX idx_parts_usage_so ON dwh.fact_parts_usage(service_order_key);
CREATE INDEX idx_parts_usage_part ON dwh.fact_parts_usage(part_key);

CREATE INDEX idx_pl_monthly_date ON dwh.fact_service_pl_monthly(month_date_key);
CREATE INDEX idx_pl_monthly_center ON dwh.fact_service_pl_monthly(center_key);

CREATE INDEX idx_inventory_date ON dwh.fact_inventory_snapshot(snapshot_date_key);
CREATE INDEX idx_inventory_wh ON dwh.fact_inventory_snapshot(warehouse_key);

CREATE INDEX idx_claims_date ON dwh.fact_warranty_claims(claim_date_key);
CREATE INDEX idx_claims_partner ON dwh.fact_warranty_claims(insurance_key);
CREATE INDEX idx_claims_center ON dwh.fact_warranty_claims(center_key);

-- --------------------------------------------------------------------
-- 6. DATA MARTS (SUMMARY VIEWS)
-- --------------------------------------------------------------------

-- Mart 1: Service Revenue & P&L Monthly Summary
CREATE OR REPLACE VIEW mart.service_revenue_summary AS
SELECT 
    d.year,
    d.month_name,
    d.year_month,
    sc.center_name,
    g.region,
    g.city,
    SUM(f.service_revenue_idr) AS total_service_revenue,
    SUM(f.parts_revenue_idr) AS total_parts_revenue,
    SUM(f.gross_revenue_idr) AS total_gross_revenue,
    SUM(f.cogs_idr) AS total_cogs,
    SUM(f.gross_profit_idr) AS total_gross_profit,
    SUM(f.operating_expenses_idr) AS total_opex,
    SUM(f.net_profit_idr) AS total_net_profit,
    ROUND(SUM(f.net_profit_idr) * 100.0 / NULLIF(SUM(f.gross_revenue_idr), 0), 2) AS net_profit_margin_pct
FROM dwh.fact_service_pl_monthly f
JOIN dwh.dim_date d ON f.month_date_key = d.date_key
JOIN dwh.dim_service_center sc ON f.center_key = sc.center_key
JOIN dwh.dim_geography g ON f.geo_key = g.geo_key
GROUP BY d.year, d.month_name, d.year_month, sc.center_name, g.region, g.city;

-- Mart 2: Customer 360 View
CREATE OR REPLACE VIEW mart.customer_360 AS
SELECT 
    c.customer_key,
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.loyalty_tier,
    g.city,
    g.region,
    COUNT(DISTINCT so.service_order_key) AS total_service_orders,
    COALESCE(SUM(so.total_revenue_idr), 0) AS total_service_spend,
    COUNT(DISTINCT wc.claim_key) AS total_claims_filed,
    COALESCE(SUM(wc.total_claim_cost_idr), 0) AS total_claim_value,
    COUNT(DISTINCT st.ticket_key) AS total_support_tickets,
    AVG(wc.csat_rating) AS avg_csat_rating
FROM dwh.dim_customer c
LEFT JOIN dwh.dim_geography g ON c.geo_key = g.geo_key
LEFT JOIN dwh.fact_service_orders so ON c.customer_key = so.customer_key
LEFT JOIN dwh.fact_warranty_claims wc ON c.customer_key = wc.customer_key
LEFT JOIN dwh.fact_support_tickets st ON c.customer_key = st.customer_key
GROUP BY c.customer_key, c.customer_id, c.customer_name, c.customer_segment, c.loyalty_tier, g.city, g.region;

-- Mart 3: Operations & SLA KPI
CREATE OR REPLACE VIEW mart.operations_kpi AS
SELECT 
    d.year_month,
    sc.center_name,
    COUNT(wc.claim_key) AS total_claims,
    COUNT(CASE WHEN wc.status = 'Resolved' THEN 1 END) AS resolved_claims,
    ROUND(COUNT(CASE WHEN wc.status = 'Resolved' THEN 1 END) * 100.0 / NULLIF(COUNT(wc.claim_key), 0), 1) AS resolution_rate_pct,
    ROUND(AVG(wc.turnaround_time_days), 2) AS avg_tat_days,
    ROUND(COUNT(CASE WHEN wc.sla_status = 'Met SLA' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN wc.status = 'Resolved' THEN 1 END), 0), 1) AS sla_adherence_pct,
    ROUND(AVG(wc.csat_rating), 2) AS avg_csat
FROM dwh.fact_warranty_claims wc
JOIN dwh.dim_date d ON wc.claim_date_key = d.date_key
JOIN dwh.dim_service_center sc ON wc.center_key = sc.center_key
GROUP BY d.year_month, sc.center_name;
