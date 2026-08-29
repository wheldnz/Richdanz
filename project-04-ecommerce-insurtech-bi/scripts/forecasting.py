"""
forecasting.py
===============
Forecasting total revenue bulanan (penjualan produk + premi asuransi)
untuk 6 bulan ke depan. Pakai scikit-learn LinearRegression dengan
fitur trend + musiman (bulan), supaya tidak butuh library forecasting
khusus (statsmodels/prophet) yang kadang ribet di-install.

Kalau di komputer kamu ada statsmodels/prophet, ini bisa di-upgrade
jadi SARIMA / Prophet -- lihat catatan di akhir file.

Output: data/monthly_revenue_actual_vs_forecast.csv, forecast_chart.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from db_utils import load_table

# ---------------------------------------------------------------
# 1. Load & agregasi revenue bulanan (produk + premi asuransi)
# ---------------------------------------------------------------
orders = load_table("orders", parse_dates=["order_date"])
items = load_table("order_items")
policies = load_table("insurance_policies", parse_dates=["start_date", "end_date"])

completed = orders[orders.order_status == "Completed"]
order_rev = items.merge(completed[["order_id", "order_date"]], on="order_id")
order_rev["revenue"] = order_rev["quantity"] * order_rev["unit_price"]
product_monthly = order_rev.groupby(order_rev.order_date.dt.to_period("M"))["revenue"].sum()

policy_monthly = policies.groupby(policies.start_date.dt.to_period("M"))["premium"].sum()

monthly = pd.DataFrame({
    "product_revenue": product_monthly,
    "insurance_revenue": policy_monthly
}).fillna(0)
monthly["total_revenue"] = monthly["product_revenue"] + monthly["insurance_revenue"]
monthly = monthly.sort_index()

# ---------------------------------------------------------------
# 2. Feature engineering: trend (index bulan) + musiman (bulan ke berapa)
# ---------------------------------------------------------------
df = monthly.reset_index().rename(columns={"order_date": "month", "index": "month"})
df.columns = ["month", "product_revenue", "insurance_revenue", "total_revenue"]
df["t"] = np.arange(len(df))                 # trend linear
df["month_num"] = df["month"].dt.month        # 1-12, untuk seasonal dummy

seasonal_dummies = pd.get_dummies(df["month_num"], prefix="m", drop_first=True)
X_all = pd.concat([df[["t"]], seasonal_dummies], axis=1)
y_all = df["total_revenue"]

# ---------------------------------------------------------------
# 3. Split train/test (3 bulan terakhir buat validasi akurasi)
# ---------------------------------------------------------------
n_test = 3
X_train, X_test = X_all.iloc[:-n_test], X_all.iloc[-n_test:]
y_train, y_test = y_all.iloc[:-n_test], y_all.iloc[-n_test:]

model = LinearRegression()
model.fit(X_train, y_train)

pred_test = model.predict(X_test)
mape = mean_absolute_percentage_error(y_test, pred_test)
print(f"Validasi model (3 bulan terakhir) - MAPE: {mape:.1%}")
print(pd.DataFrame({"actual": y_test.values, "predicted": pred_test.round(0)},
                    index=df["month"].iloc[-n_test:].astype(str)))

# ---------------------------------------------------------------
# 4. Retrain pakai SEMUA data, lalu forecast 6 bulan ke depan
# ---------------------------------------------------------------
model_full = LinearRegression()
model_full.fit(X_all, y_all)

FORECAST_HORIZON = 6
future_months = pd.period_range(df["month"].max() + 1, periods=FORECAST_HORIZON, freq="M")
future_df = pd.DataFrame({"month": future_months})
future_df["t"] = np.arange(len(df), len(df) + FORECAST_HORIZON)
future_df["month_num"] = future_df["month"].dt.month
future_seasonal = pd.get_dummies(future_df["month_num"], prefix="m", drop_first=True)
# pastikan kolom sama persis dengan waktu training (isi 0 utk kolom bulan yang tidak muncul)
future_seasonal = future_seasonal.reindex(columns=seasonal_dummies.columns, fill_value=0)
X_future = pd.concat([future_df[["t"]], future_seasonal], axis=1)

future_df["forecast_revenue"] = model_full.predict(X_future)

print("\nForecast 6 bulan ke depan:")
print(future_df[["month", "forecast_revenue"]].assign(
    forecast_revenue=lambda d: d.forecast_revenue.round(0)))

# ---------------------------------------------------------------
# 5. Simpan hasil gabungan (actual + forecast) untuk dipakai di Power BI
# ---------------------------------------------------------------
actual_out = df[["month", "total_revenue"]].copy()
actual_out["type"] = "Actual"
actual_out = actual_out.rename(columns={"total_revenue": "revenue"})

forecast_out = future_df[["month", "forecast_revenue"]].copy()
forecast_out["type"] = "Forecast"
forecast_out = forecast_out.rename(columns={"forecast_revenue": "revenue"})

combined = pd.concat([actual_out, forecast_out], ignore_index=True)
combined["month"] = combined["month"].astype(str)
combined.to_csv("../data/monthly_revenue_actual_vs_forecast.csv", index=False)

# ---------------------------------------------------------------
# 6. Chart cepat buat sanity check (opsional, dashboard tetap di Power BI)
# ---------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(actual_out["month"].astype(str), actual_out["revenue"], marker="o", label="Actual")
plt.plot(forecast_out["month"].astype(str), forecast_out["revenue"], marker="o",
         linestyle="--", label="Forecast")
plt.xticks(rotation=60, fontsize=7)
plt.ylabel("Revenue (IDR)")
plt.title("Total Revenue Bulanan: Actual vs Forecast")
plt.legend()
plt.tight_layout()
plt.savefig("../data/forecast_chart.png", dpi=120)
print("\nChart tersimpan: ../data/forecast_chart.png")
print("Data gabungan tersimpan: ../data/monthly_revenue_actual_vs_forecast.csv")

# ---------------------------------------------------------------
# Catatan upgrade (opsional, kalau statsmodels/prophet tersedia):
#   from statsmodels.tsa.statespace.sarimax import SARIMAX
#   model = SARIMAX(y_all, order=(1,1,1), seasonal_order=(1,1,1,12)).fit()
# Prophet biasanya lebih gampang untuk musiman kompleks, tapi versi
# LinearRegression di atas sudah cukup untuk menunjukkan pemahaman
# trend + seasonality ke recruiter, dan tidak butuh dependency berat.
# ---------------------------------------------------------------
