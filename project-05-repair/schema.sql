-- Schema PostgreSQL: Claims & SLA Analytics (Project 05)
-- Monitoring 300+ monthly service claims across 9 insurance partners (Target SLA 7 Days)

DROP TABLE IF EXISTS fact_claims_sla CASCADE;
DROP TABLE IF EXISTS dim_insurance_partners CASCADE;
DROP TABLE IF EXISTS dim_service_centers CASCADE;

-- 1. Dimensi Mitra Asuransi (9 Insurance Partners)
CREATE TABLE dim_insurance_partners (
    partner_id INT PRIMARY KEY,
    partner_name VARCHAR(100) NOT NULL,
    sla_target_days INT DEFAULT 7
);

-- 2. Dimensi Jaringan Service Center (9 Service Centers)
CREATE TABLE dim_service_centers (
    center_id INT PRIMARY KEY,
    center_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- 3. Tabel Fakta Klaim & SLA (3,800+ Claims Records)
CREATE TABLE fact_claims_sla (
    claim_id VARCHAR(50) PRIMARY KEY,
    partner_id INT REFERENCES dim_insurance_partners(partner_id),
    center_id INT REFERENCES dim_service_centers(center_id),
    device_brand VARCHAR(50),
    device_model VARCHAR(50),
    claim_date DATE NOT NULL,
    approval_date DATE,
    completion_date DATE,
    turnaround_time_days INT,
    sla_target_days INT DEFAULT 7,
    repair_cost_idr NUMERIC(12, 2),
    sparepart_cost_idr NUMERIC(12, 2),
    status VARCHAR(20) CHECK (status IN ('Resolved', 'Pending', 'Rejected')),
    sla_status VARCHAR(30),
    csat_rating INT CHECK (csat_rating BETWEEN 1 AND 5)
);

-- Indeks Performa
CREATE INDEX idx_claims_partner ON fact_claims_sla(partner_id);
CREATE INDEX idx_claims_center ON fact_claims_sla(center_id);
CREATE INDEX idx_claims_date ON fact_claims_sla(claim_date);
CREATE INDEX idx_claims_status ON fact_claims_sla(status);
