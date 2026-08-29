-- =========================================================
-- TokoAman.id — Skema Database (PostgreSQL)
-- Studi kasus: marketplace e-commerce yang juga menjual
-- produk asuransi mikro (embedded insurance) di checkout
-- =========================================================

DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS insurance_policies CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Master pelanggan
CREATE TABLE customers (
    customer_id         INT PRIMARY KEY,
    full_name           VARCHAR(100) NOT NULL,
    gender              VARCHAR(1),
    city                VARCHAR(50),
    province            VARCHAR(50),
    signup_date         DATE NOT NULL,
    acquisition_channel VARCHAR(50)
);

-- Master produk e-commerce
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    unit_price   NUMERIC(12,2) NOT NULL,
    cost_price   NUMERIC(12,2) NOT NULL
);

-- Master campaign marketing (dipakai lintas e-commerce & asuransi)
CREATE TABLE campaigns (
    campaign_id   INT PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    channel       VARCHAR(50) NOT NULL,       -- Instagram Ads, TikTok Ads, Google Ads, Email, Referral, Organic
    objective     VARCHAR(50) NOT NULL,       -- Product Sales, Insurance Signup, Brand Awareness
    start_date    DATE NOT NULL,
    end_date      DATE NOT NULL,
    budget        NUMERIC(14,2) NOT NULL
);

-- Transaksi order e-commerce (header)
CREATE TABLE orders (
    order_id     INT PRIMARY KEY,
    customer_id  INT NOT NULL REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    campaign_id  INT REFERENCES campaigns(campaign_id),
    channel      VARCHAR(20),                 -- App / Web
    order_status VARCHAR(20) NOT NULL          -- Completed / Cancelled / Returned
);

-- Detail item per order
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT NOT NULL REFERENCES orders(order_id),
    product_id    INT NOT NULL REFERENCES products(product_id),
    quantity      INT NOT NULL,
    unit_price    NUMERIC(12,2) NOT NULL       -- harga saat transaksi (bisa beda dari master jika promo)
);

-- Polis asuransi mikro (embedded di checkout atau standalone)
CREATE TABLE insurance_policies (
    policy_id     INT PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customers(customer_id),
    order_id      INT REFERENCES orders(order_id),   -- NULL jika standalone (mis. asuransi perjalanan)
    campaign_id   INT REFERENCES campaigns(campaign_id),
    policy_type   VARCHAR(50) NOT NULL,        -- Gadget Protection, Shipping Insurance, Travel Insurance
    premium       NUMERIC(12,2) NOT NULL,
    start_date    DATE NOT NULL,
    end_date      DATE NOT NULL,
    policy_status VARCHAR(20) NOT NULL         -- Active, Expired, Renewed, Cancelled, Lapsed
);

-- Klaim asuransi
CREATE TABLE claims (
    claim_id     INT PRIMARY KEY,
    policy_id    INT NOT NULL REFERENCES insurance_policies(policy_id),
    claim_date   DATE NOT NULL,
    claim_type   VARCHAR(50),
    claim_amount NUMERIC(12,2) NOT NULL,
    claim_status VARCHAR(20) NOT NULL          -- Approved, Rejected, Pending
);

-- Index untuk mempercepat query analitik
CREATE INDEX idx_orders_customer   ON orders(customer_id);
CREATE INDEX idx_orders_date       ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_policies_customer ON insurance_policies(customer_id);
CREATE INDEX idx_policies_status   ON insurance_policies(policy_status);
CREATE INDEX idx_claims_policy     ON claims(policy_id);
