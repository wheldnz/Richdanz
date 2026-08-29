"""
marketing_roi.py
=================
Menghitung ROI/ROAS tiap campaign marketing, dengan revenue yang
diatribusikan dari DUA sumber: penjualan produk (orders) dan
pendaftaran polis asuransi (insurance_policies) yang tertaut ke
campaign_id yang sama (last-touch attribution sederhana).

Output: data/campaign_roi.csv, data/channel_roi_summary.csv
"""

import pandas as pd
from db_utils import load_table

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
campaigns = load_table("campaigns", parse_dates=["start_date", "end_date"])
orders = load_table("orders", parse_dates=["order_date"])
items = load_table("order_items")
policies = load_table("insurance_policies", parse_dates=["start_date", "end_date"])

completed = orders[orders.order_status == "Completed"].copy()

# ---------------------------------------------------------------
# 2. Revenue dari e-commerce per campaign
# ---------------------------------------------------------------
order_rev = items.merge(completed[["order_id", "campaign_id"]], on="order_id")
order_rev["revenue"] = order_rev["quantity"] * order_rev["unit_price"]
rev_ecommerce = (order_rev.dropna(subset=["campaign_id"])
                  .groupby("campaign_id")["revenue"].sum()
                  .reset_index(name="product_revenue"))

# ---------------------------------------------------------------
# 3. Revenue dari asuransi per campaign
# ---------------------------------------------------------------
rev_insurance = (policies.dropna(subset=["campaign_id"])
                  .groupby("campaign_id")["premium"].sum()
                  .reset_index(name="insurance_revenue"))

# ---------------------------------------------------------------
# 4. Gabungkan ke tabel campaign
# ---------------------------------------------------------------
roi = campaigns.merge(rev_ecommerce, on="campaign_id", how="left")
roi = roi.merge(rev_insurance, on="campaign_id", how="left")
roi[["product_revenue", "insurance_revenue"]] = roi[["product_revenue", "insurance_revenue"]].fillna(0)
roi["total_attributed_revenue"] = roi["product_revenue"] + roi["insurance_revenue"]

roi["roas"] = roi["total_attributed_revenue"] / roi["budget"]                  # Revenue / Spend
roi["roi_pct"] = (roi["total_attributed_revenue"] - roi["budget"]) / roi["budget"] * 100

roi_sorted = roi.sort_values("roas", ascending=False)

print("Top 10 campaign dengan ROAS tertinggi:")
print(roi_sorted[["campaign_name", "channel", "objective", "budget",
                   "total_attributed_revenue", "roas", "roi_pct"]].head(10).round(2))

print("\nBottom 10 campaign dengan ROAS terendah (kandidat dihentikan/dievaluasi ulang):")
print(roi_sorted[["campaign_name", "channel", "objective", "budget",
                   "total_attributed_revenue", "roas", "roi_pct"]].tail(10).round(2))

# ---------------------------------------------------------------
# 5. Ringkasan per channel & objective
# ---------------------------------------------------------------
channel_summary = roi.groupby("channel").agg(
    total_budget=("budget", "sum"),
    total_revenue=("total_attributed_revenue", "sum"),
    n_campaigns=("campaign_id", "count"),
).reset_index()
channel_summary["roas"] = channel_summary["total_revenue"] / channel_summary["total_budget"]
channel_summary = channel_summary.sort_values("roas", ascending=False)

print("\nRingkasan ROAS per channel:")
print(channel_summary.round(2))

# ---------------------------------------------------------------
# 6. Simpan
# ---------------------------------------------------------------
roi.to_csv("../data/campaign_roi.csv", index=False)
channel_summary.to_csv("../data/channel_roi_summary.csv", index=False)
print("\nHasil tersimpan: ../data/campaign_roi.csv dan ../data/channel_roi_summary.csv")

# Catatan: attribution di sini "last-touch sederhana" (1 campaign per
# transaksi, sesuai kolom campaign_id). Kalau mau lebih advanced, ini
# tempatnya menjelaskan konsep multi-touch attribution di laporan kamu.
