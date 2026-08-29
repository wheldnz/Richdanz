"""
churn_analysis.py
==================
Analisis churn dua lapis untuk TokoAman.id:
1. Churn e-commerce: pelanggan yang tidak lagi belanja (>90 hari sejak
   order terakhir, dan sudah jadi pelanggan >90 hari supaya pelanggan
   baru tidak langsung dicap churn).
2. Churn asuransi (lapse rate): proporsi polis yang tidak diperpanjang
   (status "Expired") dibanding yang "Renewed".

Ditutup dengan model risk-scoring sederhana (Logistic Regression) untuk
memprediksi probabilitas churn e-commerce dari perilaku pelanggan.

Output: data/churn_customers.csv, data/churn_by_policy_type.csv
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from db_utils import load_table

SNAPSHOT_DATE = pd.Timestamp("2026-06-30")
CHURN_WINDOW_DAYS = 90

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
customers = load_table("customers", parse_dates=["signup_date"])
orders = load_table("orders", parse_dates=["order_date"])
items = load_table("order_items")
policies = load_table("insurance_policies", parse_dates=["start_date", "end_date"])

completed = orders[orders.order_status == "Completed"].copy()

# ---------------------------------------------------------------
# 2. CHURN E-COMMERCE
# ---------------------------------------------------------------
last_order = completed.groupby("customer_id")["order_date"].max().reset_index()
last_order.columns = ["customer_id", "last_order_date"]

cust = customers.merge(last_order, on="customer_id", how="left")
cust["tenure_days"] = (SNAPSHOT_DATE - cust["signup_date"]).dt.days
cust["days_since_last_order"] = (SNAPSHOT_DATE - cust["last_order_date"]).dt.days

# Kalau belum pernah order sama sekali, treat sebagai "belum aktif"
cust["days_since_last_order"] = cust["days_since_last_order"].fillna(cust["tenure_days"])

cust["is_churned"] = np.where(
    (cust["tenure_days"] > CHURN_WINDOW_DAYS) & (cust["days_since_last_order"] > CHURN_WINDOW_DAYS),
    1, 0
)

churn_rate = cust["is_churned"].mean()
print(f"Churn rate e-commerce (belum order >{CHURN_WINDOW_DAYS} hari, pelanggan lama): {churn_rate:.1%}")
print(cust.groupby("acquisition_channel")["is_churned"].mean().sort_values(ascending=False).round(3))

# ---------------------------------------------------------------
# 3. CHURN / LAPSE ASURANSI per jenis polis
# ---------------------------------------------------------------
matured = policies[policies.policy_status.isin(["Expired", "Renewed"])]
lapse = (matured.groupby("policy_type")["policy_status"]
         .apply(lambda s: (s == "Expired").mean())
         .reset_index(name="lapse_rate"))
print("\nLapse rate asuransi per jenis polis (tidak diperpanjang):")
print(lapse.sort_values("lapse_rate", ascending=False))

lapse.to_csv("../data/churn_by_policy_type.csv", index=False)

# ---------------------------------------------------------------
# 4. FEATURE ENGINEERING untuk model risk-scoring churn e-commerce
# ---------------------------------------------------------------
freq = completed.groupby("customer_id").size().reset_index(name="frequency")
order_rev = items.merge(completed[["order_id", "customer_id"]], on="order_id")
order_rev["amount"] = order_rev["quantity"] * order_rev["unit_price"]
monetary = order_rev.groupby("customer_id")["amount"].sum().reset_index(name="monetary")

has_insurance = policies.groupby("customer_id").size().reset_index(name="n_policies")

features = cust[["customer_id", "tenure_days", "days_since_last_order",
                  "acquisition_channel", "gender", "is_churned"]]
features = features.merge(freq, on="customer_id", how="left")
features = features.merge(monetary, on="customer_id", how="left")
features = features.merge(has_insurance, on="customer_id", how="left")
features[["frequency", "monetary", "n_policies"]] = features[["frequency", "monetary", "n_policies"]].fillna(0)

# NOTE: days_since_last_order langsung menentukan is_churned by definisi,
# jadi TIDAK dipakai sebagai fitur prediktor (supaya tidak "bocor" / data leakage).
# Model di sini memprediksi risiko churn dari histori PERILAKU pelanggan.
X = pd.get_dummies(features[["tenure_days", "frequency", "monetary", "n_policies",
                              "acquisition_channel", "gender"]], drop_first=True)
y = features["is_churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train, y_train)

pred_proba = model.predict_proba(X_test)[:, 1]
pred = model.predict(X_test)

print("\n=== Evaluasi model risk-scoring churn ===")
print(classification_report(y_test, pred, digits=3))
print(f"ROC-AUC: {roc_auc_score(y_test, pred_proba):.3f}")

coef = pd.Series(model.coef_[0], index=X.columns).sort_values()
print("\nFaktor yang paling menaikkan/menurunkan risiko churn (koefisien logistic regression):")
print(coef)

# Skor risiko untuk SELURUH pelanggan (bukan cuma test set) -> siap dipakai di Power BI
features["churn_risk_score"] = model.predict_proba(X)[:, 1]
features.to_csv("../data/churn_customers.csv", index=False)
print("\nHasil lengkap (skor risiko semua pelanggan) tersimpan di: ../data/churn_customers.csv")
