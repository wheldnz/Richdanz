-- Unified Schema PostgreSQL: Enterprise Sales & Multi-Channel P&L (Project 01)
-- Conformed Dimension Model: dim_stores links Amazon Sales & Multi-Channel P&L (16 Brand Partners, 9 Infinix Service Centers, 50 Retail Partners)

DROP TABLE IF EXISTS fact_order_items CASCADE;
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS fact_pl_monthly CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_stores CASCADE;

-- 1. Dimensi Produk Amazon (1,300+ Products)
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    actual_price NUMERIC(12, 2) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    rating NUMERIC(3, 2)
);

-- 2. Dimensi Toko & Mitra Usaha Unified (16 Brand Partners, 9 Infinix Service Centers, 50 Retail Partners, 425 Outlets)
CREATE TABLE dim_stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    channel_type VARCHAR(50) NOT NULL, -- 'Brand Partner', 'Infinix Service Center', 'Retail Partner', 'Retail Outlet'
    city VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- 3. Tabel Fakta Header Transaksi Sales Amazon (50,000 Orders)
CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL,
    store_id INT NOT NULL REFERENCES dim_stores(store_id),
    salesperson_id INT NOT NULL
);

-- 4. Tabel Fakta Detail Item Transaksi Sales Amazon
CREATE TABLE fact_order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES fact_orders(order_id) ON DELETE CASCADE,
    product_id VARCHAR(50) NOT NULL REFERENCES dim_products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0)
);

-- 5. Tabel Fakta P&L Bulanan Multi-Channel (Terhubung ke dim_stores)
CREATE TABLE fact_pl_monthly (
    pl_id SERIAL PRIMARY KEY,
    store_id INT NOT NULL REFERENCES dim_stores(store_id),
    month_date DATE NOT NULL,
    gross_revenue_idr NUMERIC(15, 2) NOT NULL,
    cogs_idr NUMERIC(15, 2) NOT NULL,
    gross_profit_idr NUMERIC(15, 2) NOT NULL,
    operating_expenses_idr NUMERIC(15, 2) NOT NULL,
    net_profit_idr NUMERIC(15, 2) NOT NULL,
    net_profit_margin_pct NUMERIC(5, 2) NOT NULL
);

-- Indeks Performa
CREATE INDEX idx_orders_date ON fact_orders(order_date);
CREATE INDEX idx_orders_store ON fact_orders(store_id);
CREATE INDEX idx_items_order ON fact_order_items(order_id);
CREATE INDEX idx_items_product ON fact_order_items(product_id);
CREATE INDEX idx_pl_store ON fact_pl_monthly(store_id);
CREATE INDEX idx_pl_month ON fact_pl_monthly(month_date);
