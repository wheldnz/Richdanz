-- DDL Schema untuk PostgreSQL - Insurance Underwriting

DROP TABLE IF EXISTS claim CASCADE;
DROP TABLE IF EXISTS policy CASCADE;
DROP TABLE IF EXISTS branch CASCADE;

-- 1. Tabel Dimensi Kantor Cabang
CREATE TABLE branch (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL
);

-- 2. Tabel Dimensi Polis
CREATE TABLE policy (
    policy_id INT PRIMARY KEY,
    branch_id INT NOT NULL REFERENCES branch(branch_id),
    policy_type VARCHAR(50) NOT NULL,
    premium_amount INT NOT NULL CHECK (premium_amount > 0), -- Premi harus positif setelah ETL
    customer_age INT NOT NULL CHECK (customer_age BETWEEN 17 AND 100) -- Umur harus logis setelah ETL
);

-- 3. Tabel Fakta Klaim
CREATE TABLE claim (
    claim_id INT PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policy(policy_id) ON DELETE CASCADE,
    claim_amount INT NOT NULL CHECK (claim_amount >= 0), -- Klaim harus positif setelah ETL
    status VARCHAR(20) NOT NULL
);

-- Indeks
CREATE INDEX idx_policy_branch ON policy(branch_id);
CREATE INDEX idx_policy_type ON policy(policy_type);
CREATE INDEX idx_claim_policy ON claim(policy_id);
CREATE INDEX idx_claim_status ON claim(status);
