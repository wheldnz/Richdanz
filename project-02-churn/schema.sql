-- DDL Schema untuk PostgreSQL - Customer Churn

DROP TABLE IF EXISTS support_tickets CASCADE;
DROP TABLE IF EXISTS usage_logs CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- 1. Tabel Dimensi Pelanggan
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    signup_date DATE NOT NULL, -- Di-wajibkan isi setelah ETL
    status VARCHAR(20) NOT NULL,
    payment_method VARCHAR(50) NOT NULL
);

-- 2. Tabel Log Penggunaan
CREATE TABLE usage_logs (
    log_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    login_date DATE NOT NULL,
    feature_clicks INT NOT NULL
);

-- 3. Tabel Support Tickets
CREATE TABLE support_tickets (
    ticket_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    ticket_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    resolution_time_hours INT NOT NULL CHECK (resolution_time_hours >= 0) -- Wajib positif setelah ETL
);

-- Indeks Optimalisasi
CREATE INDEX idx_usage_customer ON usage_logs(customer_id);
CREATE INDEX idx_usage_date ON usage_logs(login_date);
CREATE INDEX idx_tickets_customer ON support_tickets(customer_id);
CREATE INDEX idx_tickets_date ON support_tickets(ticket_date);
