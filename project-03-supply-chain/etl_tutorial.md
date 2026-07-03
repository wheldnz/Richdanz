# ETL & SQL Analytics Tutorial - Supply Chain Analytics

Tutorial ini menjelaskan cara mendeteksi dan memperbaiki anomali logistik, mengimpor skema ke PostgreSQL, dan menyusun dashboard metrik OTIF (On-Time In-Full).

---

## 1. ETL & Penanganan Anomali (Python)

Anomali pada dataset ini:
- **`warehouse.csv`**: Kolom `capacity_cbm` bernilai negatif.
- **`purchase_order.csv`**: Beberapa baris berisi log PO duplikat.
- **`shipment.csv`**: Kolom `actual_arrival_date` lebih dahulu dibanding `po_date` (lead time negatif).

Buat file `etl_process.py` dan jalankan kode berikut:

```python
import pandas as pd
import numpy as np

# Load
df_wh = pd.read_csv('data/raw/warehouse.csv')
df_sup = pd.read_csv('data/raw/supplier.csv')
df_pos = pd.read_csv('data/raw/purchase_order.csv')
df_ship = pd.read_csv('data/raw/shipment.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan Warehouse
# Masalah: capacity_cbm bernilai negatif
# Solusi: Ubah ke nilai absolut (positif)
bad_caps = df_wh[df_wh['capacity_cbm'] < 0]
print(f"Menangani {len(bad_caps)} baris kapasitas gudang negatif di Warehouse.")
df_wh['capacity_cbm'] = df_wh['capacity_cbm'].abs()

# 2. Bersihkan Purchase Order
# Masalah: PO duplikat
# Solusi: Hapus duplikat berdasarkan po_id
dupes = df_pos[df_pos.duplicated(subset=['po_id'])]
print(f"Menghapus {len(dupes)} baris PO duplikat di Purchase Order.")
df_pos = df_pos.drop_duplicates(subset=['po_id'])

# 3. Bersihkan Shipment
# Masalah: actual_arrival_date lebih dahulu daripada po_date
# Solusi: Join tabel PO untuk mendapatkan po_date. Jika actual_arrival_date < po_date, 
# set actual_arrival_date = po_date + contracted_lead_time_days (SLA kontrak default)
df_merged = df_ship.merge(df_pos, on='po_id').merge(df_sup, on='supplier_id')

df_merged['actual_arrival_date'] = pd.to_datetime(df_merged['actual_arrival_date'])
df_merged['po_date'] = pd.to_datetime(df_merged['po_date'])

bad_ship_dates = df_merged[df_merged['actual_arrival_date'] < df_merged['po_date']]
print(f"Menangani {len(bad_ship_dates)} baris tanggal kirim tidak logis (lebih awal dari tanggal pesan) di Shipment.")

# Koreksi tanggal yang salah
for idx in bad_ship_dates.index:
    lead_time_target = int(df_merged.loc[idx, 'contracted_lead_time_days'])
    df_merged.loc[idx, 'actual_arrival_date'] = df_merged.loc[idx, 'po_date'] + pd.to_timedelta(lead_time_target, unit='D')

# Kembalikan kolom ke struktur semula
df_ship_cleaned = df_merged[['shipment_id', 'po_id', 'estimated_arrival_date', 'actual_arrival_date', 'is_in_full']].copy()

# Pastikan data referensial konsisten
valid_po_ids = df_pos['po_id'].unique()
df_ship_cleaned = df_ship_cleaned[df_ship_cleaned['po_id'].isin(valid_po_ids)]

# Save
df_wh.to_csv('data/processed/warehouse.csv', index=False)
df_sup.to_csv('data/processed/supplier.csv', index=False)
df_pos.to_csv('data/processed/purchase_order.csv', index=False)
df_ship_cleaned.to_csv('data/processed/shipment.csv', index=False)

print("--- ETL Sukses! Data bersih disimpan di data/processed/ ---")
```

---

## 2. Load & SQL Analytics (PostgreSQL)

### A. Load Data
Buat database dan tabel menggunakan `schema.sql`. Impor file CSV bersih dari `data/processed/` dengan urutan:
1. `warehouse.csv` $\rightarrow$ tabel `warehouse`
2. `supplier.csv` $\rightarrow$ tabel `supplier`
3. `purchase_order.csv` $\rightarrow$ tabel `purchase_order`
4. `shipment.csv` $\rightarrow$ tabel `shipment`

### B. SQL OTIF Calculation Query
Jalankan query berikut untuk mencari persentase OTIF (On-Time In-Full) dan jumlah keterlambatan pengiriman per supplier:

```sql
SELECT 
    s.supplier_name,
    COUNT(sh.shipment_id) AS total_shipments,
    SUM(CASE WHEN sh.actual_arrival_date <= sh.estimated_arrival_date AND sh.is_in_full = 1 THEN 1 ELSE 0 END) AS otif_orders,
    ROUND(SUM(CASE WHEN sh.actual_arrival_date <= sh.estimated_arrival_date AND sh.is_in_full = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(sh.shipment_id), 2) AS otif_rate_pct
FROM shipment sh
JOIN purchase_order po ON sh.po_id = po.po_id
JOIN supplier s ON po.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY otif_rate_pct DESC;
```

---

## 3. Visualisasi (Power BI)

1. Impor data dari PostgreSQL ke Power BI.
2. Buat relasi:
   - `warehouse[warehouse_id]` $\rightarrow$ `purchase_order[warehouse_id]` ($1:\infty$)
   - `supplier[supplier_id]` $\rightarrow$ `purchase_order[supplier_id]` ($1:\infty$)
   - `purchase_order[po_id]` $\rightarrow$ `shipment[po_id]` ($1:\infty$)
3. Buat tabel kalender dan hubungkan ke `purchase_order[po_date]`.
4. DAX Measure untuk **OTIF Rate**:
   ```dax
   On Time Orders = CALCULATE(COUNT(shipment[shipment_id]), FILTER(shipment, shipment[actual_arrival_date] <= shipment[estimated_arrival_date]))
   
   In Full Orders = CALCULATE(COUNT(shipment[shipment_id]), shipment[is_in_full] = 1)
   
   OTIF Rate = DIVIDE(
       CALCULATE(COUNT(shipment[shipment_id]), shipment[actual_arrival_date] <= shipment[estimated_arrival_date] && shipment[is_in_full] = 1),
       COUNT(shipment[shipment_id]),
       0
   )
   ```
5. Susun dasbor visual dengan Gauge visual untuk memantau kapasitas penyimpanan gudang dan peta rute jalur logistik.
