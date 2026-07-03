---
title: Supply Chain Analytics
category: data
metric: 96%
metricLabel: On-Time In-Full (OTIF)
tags: ['SQL', 'Power BI', 'Inventory', 'Logistics']
description: Inventory optimization and supply chain logistics dashboard monitoring stock turnover, warehouse capacity, and supplier SLA performance across global operations.
---

# Supply Chain Analytics

## Business Problem
Perusahaan manufaktur global mengalami inefisiensi biaya operasional akibat tingginya tingkat *stockout* (kehabisan stok) untuk produk populer, dan di sisi lain terdapat penumpukan stok (*overstock*) untuk produk yang kurang diminati di beberapa gudang regional. Selain itu, keterlambatan pengiriman dari supplier utama sering mengganggu jadwal produksi. Proyek ini bertujuan untuk mengoptimalkan *Inventory Turnover*, memantau kapasitas gudang secara real-time, dan mengukur performa pengiriman supplier (OTIF).

## Dataset & Raw Data
* **Tables**:
  - `warehouse` (50 baris): Lokasi, kapasitas maksimum (CBM), dan biaya sewa gudang.
  - `supplier` (500 baris): Informasi supplier, lead time kontrak, dan rating.
  - `inventory` (5 juta baris): Catatan harian tingkat stok per SKU di setiap gudang.
  - `purchase_order` (500 ribu baris): Detail pesanan barang ke supplier.
  - `shipment` (800 ribu baris): Log pengiriman barang dari supplier (estimasi vs aktual).
  - `delivery` (800 ribu baris): Data pengiriman produk akhir ke distributor/ritel.

### Raw Data Generation
Data dummy mensimulasikan kondisi logistik riil: *Lead Time* pengiriman dari supplier memiliki distribusi log-normal (memiliki ekor panjang yang mencerminkan delay tidak terduga akibat cuaca/bea cukai), dan kapasitas gudang terisi secara dinamis berdasarkan laju *inventory inbound* dan *outbound*.

## Data Model
- **Fact Table**: `fact_inventory_daily` (snapshot harian jumlah stok dan pergerakan barang).
- **Dimension Tables**: `dim_product`, `dim_warehouse`, `dim_supplier`, `dim_date`.

## SQL Process
Query PostgreSQL ini digunakan untuk mendeteksi *Reorder Point* (titik pemesanan ulang) serta menghitung keterlambatan pengiriman supplier:

```sql
-- Analisa Lead Time Aktual vs Kontrak per Supplier
SELECT 
    s.supplier_name,
    COUNT(po.po_id) AS total_orders,
    AVG(EXTRACT(DAY FROM (sh.actual_arrival_date - po.po_date))) AS avg_lead_time_days,
    AVG(s.contracted_lead_time_days) AS contracted_lead_time,
    SUM(CASE WHEN sh.actual_arrival_date <= sh.estimated_arrival_date THEN 1 ELSE 0 END) * 100.0 / COUNT(po.po_id) AS on_time_rate_pct
FROM purchase_order po
JOIN supplier s ON po.supplier_id = s.supplier_id
JOIN shipment sh ON po.po_id = sh.po_id
GROUP BY s.supplier_name
HAVING COUNT(po.po_id) > 10
ORDER BY on_time_rate_pct ASC;
```

## Power BI & DAX
Metrik DAX untuk melacak performa rantai pasok:

* **On-Time In-Full (OTIF) Rate**:
  ```dax
  OTIF Rate = 
  DIVIDE(
      CALCULATE(COUNT(fact_shipment[ShipmentID]), fact_shipment[IsOnTime] = 1 && fact_shipment[IsInFull] = 1),
      COUNT(fact_shipment[ShipmentID]),
      0
  )
  ```
* **Inventory Turnover Ratio (ITR)**:
  ```dax
  Inventory Turnover Ratio = DIVIDE([Total Cost of Goods Sold], [Average Inventory Value], 0)
  ```

## Dashboard Mockup Specification
Dashboard menggunakan **Industrial Theme (Dark Slate with Amber & Emerald Accents)**:
- **Halaman 1: Inventory Health**: Visualisasi tingkat keterisian gudang (Gauge Chart) dan indikator sisa hari stok sebelum habis (Days of Supply Outstanding).
- **Halaman 2: Supplier SLA & OTIF**: Peta rute pengiriman (Route Map) yang dinamis dengan visualisasi warna rute berdasarkan status keterlambatan, terintegrasi dengan filter pencarian nama supplier.

## Key Insights
1. **Rendahnya OTIF**: Rata-rata OTIF nasional hanya mencapai 82%, di bawah target korporat sebesar 95%.
2. **Keterlambatan Supplier Utama**: Supplier kategori *Packaging* mengalami rata-rata keterlambatan 4.5 hari selama Q3 akibat kelangkaan bahan baku lokal.
3. **Bottleneck Gudang**: Gudang Regional Barat melebihi 90% kapasitas maksimumnya, menyebabkan biaya penyimpanan ekstra (*holding cost*) naik 25%.
4. **Stockout Produk Hero**: SKU kategori *High-Demand Electronics* mengalami kehabisan stok rata-rata 6 hari per bulan, menyebabkan estimasi kehilangan potensi revenue sebesar Rp 1.2M.
5. **Slow-Moving Inventory**: Produk kategori *Fashion Accessories* memiliki ITR terendah (hanya 1.8 kali per tahun), terendap rata-rata 180 hari di gudang.
6. **Akurasi Estimasi (ETA)**: Algoritma estimasi pengiriman pihak ketiga memiliki margin kesalahan (bias) rata-rata +2 hari pada musim hujan.
7. **Korelasi Jarak**: Rute pengiriman darat di atas 500 km memiliki risiko keterlambatan 30% lebih tinggi dibanding rute kombinasi kereta api.
8. **Efisiensi Batch**: Pengiriman dengan kontainer penuh (FCL - *Full Container Load*) memiliki tingkat OTIF 12% lebih stabil dibanding eceran (LCL).
9. **Ketergantungan Supplier tunggal**: 70% komponen kritis dipasok dari satu supplier tunggal (Single-sourcing risk).
10. **Penghematan Reorder Point**: Penerapan formula Safety Stock dinamis berhasil mengurangi insiden stockout sebesar 40% pada simulasi data historis.

## Recommendations
1. Diversifikasi supplier untuk komponen kritis guna menghindari risiko kegagalan pasokan dari satu sumber.
2. Terapkan formula Reorder Point (ROP) otomatis yang disesuaikan dengan fluktuasi lead time aktual supplier.
3. Negosiasikan ulang kontrak SLA dengan supplier packaging yang memiliki performa OTIF di bawah 80%.
4. Alihkan kelebihan stok dari Gudang Barat ke Gudang Timur yang kapasitasnya baru terisi 55%.
5. Hentikan produksi produk aksesoris fashion yang lambat terjual dan lakukan cuci gudang (diskon besar) untuk mengosongkan tempat.
6. Gunakan transportasi kereta api untuk rute antar-kota jarak jauh guna meningkatkan konsistensi ketepatan waktu pengiriman.
7. Terapkan sistem *Cross-docking* di gudang utama untuk mempercepat distribusi barang tanpa perlu menyimpannya di rak.
8. Berikan insentif finansial (bonus) kepada pihak ekspedisi yang berhasil mempertahankan OTIF harian di atas 98%.
9. Integrasikan sistem inventory gudang secara langsung ke dashboard supplier untuk transparansi stok bahan baku.
10. Lakukan audit triwulanan pada akurasi pencatatan stok fisik vs sistem untuk menghindari kesalahan pelaporan.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
Jalankan script DDL berikut di PostgreSQL:

```sql
CREATE DATABASE supply_chain;

-- Tabel Gudang
CREATE TABLE warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR(50),
    capacity_cbm INT
);

-- Tabel Supplier
CREATE TABLE supplier (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100),
    contracted_lead_time_days INT
);

-- Tabel Purchase Order (PO)
CREATE TABLE purchase_order (
    po_id INT PRIMARY KEY,
    po_date DATE,
    supplier_id INT REFERENCES supplier(supplier_id),
    warehouse_id INT REFERENCES warehouse(warehouse_id)
);

-- Tabel Pengiriman (Shipment)
CREATE TABLE shipment (
    shipment_id INT PRIMARY KEY,
    po_id INT REFERENCES purchase_order(po_id),
    estimated_arrival_date DATE,
    actual_arrival_date DATE,
    is_in_full INT
);
```

### Langkah 2: Script Generate Data (Python)
Gunakan python script untuk membuat log pengiriman dengan variasi lead time log-normal:

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Dimensi
warehouses = [{'warehouse_id': i, 'warehouse_name': f"Gudang {r}", 'capacity_cbm': random.randint(10000, 50000)} for i, r in enumerate(['Pusat', 'Utara', 'Selatan'], 1)]
pd.DataFrame(warehouses).to_csv('warehouse.csv', index=False)

suppliers = [{'supplier_id': i, 'supplier_name': f"Supplier {i}", 'contracted_lead_time_days': random.randint(3, 10)} for i in range(1, 51)]
pd.DataFrame(suppliers).to_csv('supplier.csv', index=False)

# 500k POs & Shipments
pos = []
shipments = []
start_date = datetime(2023, 1, 1)

for i in range(1, 500001):
    po_date = start_date + timedelta(days=random.randint(0, 700))
    s_id = random.randint(1, 50)
    w_id = random.randint(1, 3)
    pos.append({'po_id': i, 'po_date': po_date.strftime('%Y-%m-%d'), 'supplier_id': s_id, 'warehouse_id': w_id})
    
    # Lead time log-normal distribution
    contracted = next(item for item in suppliers if item['supplier_id'] == s_id)['contracted_lead_time_days']
    actual_lead = int(contracted + np.random.lognormal(mean=0.5, sigma=0.5))
    
    est_arrival = po_date + timedelta(days=contracted)
    act_arrival = po_date + timedelta(days=actual_lead)
    
    shipments.append({
        'shipment_id': i,
        'po_id': i,
        'estimated_arrival_date': est_arrival.strftime('%Y-%m-%d'),
        'actual_arrival_date': act_arrival.strftime('%Y-%m-%d'),
        'is_in_full': random.choices([1, 0], weights=[0.88, 0.12])[0]
    })

pd.DataFrame(pos).to_csv('purchase_order.csv', index=False)
pd.DataFrame(shipments).to_csv('shipment.csv', index=False)
print("Data supply chain berhasil dibuat!")
```

### Langkah 3: Import ke PostgreSQL & Jalankan SQL
1. Pindahkan CSV ke PostgreSQL.
2. Hitung performa OTIF menggunakan SQL query di bagian **SQL Process** untuk melacak delay supplier.

### Langkah 4: Visualisasi di Power BI
1. Impor seluruh tabel relasi ke Power BI.
2. Buat visualisasi bertema industrial gelap (dark slate) dengan gauge chart untuk melacak kapasitas gudang.
3. Rancang tombol parameter what-if dinamis untuk menguji keefektifan Safety Stock ROP yang telah Anda buat.

