-- DDL Schema untuk PostgreSQL

-- Hapus tabel jika sudah ada (untuk keperluan reset)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

-- 1. Tabel Dimensi Toko
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- 2. Tabel Dimensi Produk
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL CHECK (cost_price >= 0), -- Constraint harga tidak boleh negatif setelah ETL
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0)
);

-- 3. Tabel Fakta Transaksi Order (Header)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL, -- Harus valid Date
    customer_id INT NOT NULL,
    store_id INT NOT NULL REFERENCES stores(store_id), -- Foreign key referensi wajib ada
    salesperson_id INT NOT NULL
);

-- 4. Tabel Fakta Transaksi Order (Detail)
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0) -- Qty harus positif setelah ETL
);

-- Optimalisasi Database (Index)
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_store ON orders(store_id);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_items_product ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category);
