-- DDL Schema untuk PostgreSQL - Repair Service

DROP TABLE IF EXISTS warranty CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS technician CASCADE;

-- 1. Tabel Dimensi Teknisi
CREATE TABLE technician (
    technician_id INT PRIMARY KEY,
    technician_name VARCHAR(100) NOT NULL,
    is_certified INT NOT NULL CHECK (is_certified IN (0, 1))
);

-- 2. Tabel Fakta Tiket
CREATE TABLE ticket (
    ticket_id INT PRIMARY KEY,
    device_id INT NOT NULL,
    technician_id INT NOT NULL REFERENCES technician(technician_id),
    status VARCHAR(20) NOT NULL,
    completion_date DATE NOT NULL -- Wajib diisi setelah ETL
);

-- 3. Tabel Fakta Klaim Garansi (Repeat Repair)
CREATE TABLE warranty (
    warranty_id INT PRIMARY KEY,
    device_id INT NOT NULL,
    claim_date DATE NOT NULL
);

-- Indeks
CREATE INDEX idx_ticket_tech ON ticket(technician_id);
CREATE INDEX idx_ticket_device ON ticket(device_id);
CREATE INDEX idx_ticket_comp_date ON ticket(completion_date);
CREATE INDEX idx_warranty_device ON warranty(device_id);
CREATE INDEX idx_warranty_date ON warranty(claim_date);
