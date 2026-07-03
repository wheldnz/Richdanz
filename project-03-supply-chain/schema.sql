-- DDL Schema untuk PostgreSQL - Supply Chain Analytics

DROP TABLE IF EXISTS shipment CASCADE;
DROP TABLE IF EXISTS purchase_order CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;

-- 1. Tabel Dimensi Gudang
CREATE TABLE warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    capacity_cbm INT NOT NULL CHECK (capacity_cbm >= 0) -- Wajib positif setelah ETL
);

-- 2. Tabel Dimensi Supplier
CREATE TABLE supplier (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contracted_lead_time_days INT NOT NULL
);

-- 3. Tabel Fakta Purchase Order
CREATE TABLE purchase_order (
    po_id INT PRIMARY KEY,
    po_date DATE NOT NULL,
    supplier_id INT NOT NULL REFERENCES supplier(supplier_id),
    warehouse_id INT NOT NULL REFERENCES warehouse(warehouse_id)
);

-- 4. Tabel Fakta Pengiriman (Shipment)
CREATE TABLE shipment (
    shipment_id INT PRIMARY KEY,
    po_id INT NOT NULL REFERENCES purchase_order(po_id) ON DELETE CASCADE,
    estimated_arrival_date DATE NOT NULL,
    actual_arrival_date DATE NOT NULL,
    is_in_full INT NOT NULL CHECK (is_in_full IN (0, 1)),
    CONSTRAINT chk_arrival_date CHECK (actual_arrival_date >= estimated_arrival_date - INTERVAL '30 days') -- Batas toleransi wajar setelah ETL
);

-- Indeks Optimalisasi
CREATE INDEX idx_po_supplier ON purchase_order(supplier_id);
CREATE INDEX idx_po_warehouse ON purchase_order(warehouse_id);
CREATE INDEX idx_po_date ON purchase_order(po_date);
CREATE INDEX idx_shipment_po ON shipment(po_id);
CREATE INDEX idx_shipment_arrival ON shipment(actual_arrival_date);
