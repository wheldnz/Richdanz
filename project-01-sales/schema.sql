-- Schema PostgreSQL: Multi-Channel P&L Dashboard (Project 01)
-- Managing Daily/Monthly/Yearly P&L across 16 Brand Partners, 9 Infinix Service Centers, and 50 Retail Partners

DROP TABLE IF EXISTS fact_pl_monthly CASCADE;
DROP TABLE IF EXISTS dim_partners CASCADE;

-- 1. Dimensi Mitra Usaha (75 Partners across 3 Channels)
CREATE TABLE dim_partners (
    partner_id VARCHAR(50) PRIMARY KEY,
    partner_name VARCHAR(100) NOT NULL,
    channel_type VARCHAR(50) NOT NULL CHECK (channel_type IN ('Brand Partner', 'Infinix Service Center', 'Retail Partner'))
);

-- 2. Tabel Fakta P&L Bulanan (1,800 Records for 2024-2025)
CREATE TABLE fact_pl_monthly (
    pl_id SERIAL PRIMARY KEY,
    partner_id VARCHAR(50) REFERENCES dim_partners(partner_id),
    month_date DATE NOT NULL,
    gross_revenue_idr NUMERIC(15, 2) NOT NULL,
    cogs_idr NUMERIC(15, 2) NOT NULL,
    gross_profit_idr NUMERIC(15, 2) NOT NULL,
    operating_expenses_idr NUMERIC(15, 2) NOT NULL,
    net_profit_idr NUMERIC(15, 2) NOT NULL,
    net_profit_margin_pct NUMERIC(5, 2) NOT NULL
);

-- Indeks Performa
CREATE INDEX idx_pl_partner ON fact_pl_monthly(partner_id);
CREATE INDEX idx_pl_month ON fact_pl_monthly(month_date);
