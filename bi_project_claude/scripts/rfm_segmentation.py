"""
rfm_segmentation.py
====================
Segmentasi pelanggan TokoAman.id berdasarkan RFM (Recency, Frequency,
Monetary), menggabungkan transaksi e-commerce (orders) DAN pembelian
polis asuransi (insurance_policies) sebagai satu customer value.

Output: data/rfm_segments.csv
"""

import pandas as pd
from db_utils import load_table

SNAPSHOT_DATE = pd.Timestamp("2026-06-30")  # "hari ini" di simulasi kita

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
orders = load_table("orders", parse_dates=["order_date"])
items = load_table("order_items")
policies = load_table("insurance_policies", parse_dates=["start_date", "end_date"])

orders = orders[orders.order_status == "Completed"].copy()

# ---------------------------------------------------------------
# 2. Gabungkan dua sumber transaksi jadi satu tabel "transactions"
#    supaya RFM mencerminkan total value pelanggan (belanja + asuransi)
# ---------------------------------------------------------------
order_rev = items.merge(orders[["order_id", "customer_id", "order_date"]], on="order_id")
order_rev["amount"] = order_rev["quantity"] * order_rev["unit_price"]
order_txn = (order_rev.groupby(["customer_id", "order_id"])
             .agg(txn_date=("order_date", "first"), amount=("amount", "sum"))
             .reset_index()[["customer_id", "txn_date", "amount"]])

policy_txn = policies.rename(columns={"start_date": "txn_date", "premium": "amount"})[
    ["customer_id", "txn_date", "amount"]]

transactions = pd.concat([order_txn, policy_txn], ignore_index=True)

# ---------------------------------------------------------------
# 3. Hitung Recency, Frequency, Monetary per pelanggan
# ---------------------------------------------------------------
rfm = transactions.groupby("customer_id").agg(
    recency_days=("txn_date", lambda x: (SNAPSHOT_DATE - x.max()).days),
    frequency=("txn_date", "count"),
    monetary=("amount", "sum"),
).reset_index()

# ---------------------------------------------------------------
# 4. Skoring 1-4 per kuartil (Recency dibalik: makin baru makin tinggi skor)
# ---------------------------------------------------------------
rfm["R_score"] = pd.qcut(rfm["recency_days"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
rfm["RFM_score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)


# ---------------------------------------------------------------
# 5. Mapping ke label segmen yang gampang dibaca stakeholder
# ---------------------------------------------------------------
def label_segment(row):
    r, f, m = row["R_score"], row["F_score"], row["M_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "New Customers"
    if r <= 2 and f >= 3 and m >= 3:
        return "At Risk (Nilai Tinggi, Mulai Sepi)"
    if r <= 2 and f <= 2 and m <= 2:
        return "Hibernating / Lost"
    return "Need Attention"


rfm["segment"] = rfm.apply(label_segment, axis=1)

# ---------------------------------------------------------------
# 6. Simpan hasil
# ---------------------------------------------------------------
out_path = "../data/rfm_segments.csv"
rfm.to_csv(out_path, index=False)

print("Distribusi segmen pelanggan:")
print(rfm["segment"].value_counts())
print()
print("Rata-rata monetary per segmen:")
print(rfm.groupby("segment")["monetary"].mean().sort_values(ascending=False).round(0))
print(f"\nHasil lengkap tersimpan di: {out_path}")
