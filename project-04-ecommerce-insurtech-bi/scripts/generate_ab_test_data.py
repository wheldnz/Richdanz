"""
generate_ab_test_data.py
=========================
Simulasi data eksperimen A/B test 4 minggu untuk TokoAman.id.

Hipotesis bisnis: mengubah checkbox "Proteksi Gadget" di checkout dari
opt-in manual (kosong, harus dicentang sendiri) jadi PRE-CHECKED
(opt-out, sudah tercentang default) akan meningkatkan attach rate
polis asuransi.

Populasi eksperimen: sesi checkout yang berisi minimal 1 produk
kategori Elektronik (satu-satunya kategori yang ditawari Gadget
Protection). Setiap sesi diacak 50/50 ke Control atau Treatment.

Guardrail metric: completion rate checkout -- desain "dipaksa" seperti
pre-checked bisa saja menurunkan kepercayaan/kenyamanan pengguna dan
membuat lebih banyak yang batal checkout.

Ground truth yang disimulasikan (di dunia nyata inilah yang justru
ingin kita TEMUKAN lewat eksperimen, bukan diketahui di awal):
    Control (opt-in manual) : attach rate 24%, completion rate 93%
    Treatment (pre-checked)  : attach rate 37%, completion rate 90%

Output: data/ab_test_sessions.csv
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import os

SEED = 7
rng = np.random.default_rng(SEED)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

EXPERIMENT_START = date(2026, 7, 1)
EXPERIMENT_END = date(2026, 7, 28)          # 4 minggu, langsung setelah data historis (s.d. 30 Jun 2026)
N_SESSIONS = 6000

PRODUCT_VALUE_RANGE = (500000, 8000000)      # nilai barang elektronik di sesi ini
PREMIUM_RANGE = (29000, 89000)

# "Ground truth" tersembunyi -- dipakai untuk simulasi, BUKAN dipakai di script analisis
TRUE_RATES = {
    "Control":   {"attach": 0.24, "completion": 0.93},
    "Treatment": {"attach": 0.37, "completion": 0.90},
}

days_span = (EXPERIMENT_END - EXPERIMENT_START).days
session_dates = [EXPERIMENT_START + timedelta(days=int(d))
                  for d in rng.integers(0, days_span + 1, size=N_SESSIONS)]
groups = rng.choice(["Control", "Treatment"], size=N_SESSIONS, p=[0.5, 0.5])

rows = []
for i in range(N_SESSIONS):
    grp = groups[i]
    rates = TRUE_RATES[grp]
    product_value = float(rng.integers(*PRODUCT_VALUE_RANGE))

    completed = rng.random() < rates["completion"]
    # attach hanya mungkin terjadi kalau checkout selesai
    attached = bool(completed and (rng.random() < rates["attach"]))
    premium = float(rng.integers(*PREMIUM_RANGE)) if attached else 0.0
    order_value = (product_value + premium) if completed else 0.0

    rows.append((i + 1, session_dates[i], grp, product_value,
                 completed, attached, premium, order_value))

df = pd.DataFrame(rows, columns=[
    "session_id", "session_date", "group", "product_value",
    "completed_checkout", "attached_insurance", "premium", "order_value"])

df.to_csv(os.path.join(OUT_DIR, "ab_test_sessions.csv"), index=False)

summary = df.groupby("group").agg(
    n_sessions=("session_id", "count"),
    completion_rate=("completed_checkout", "mean"),
    attach_rate_all=("attached_insurance", "mean"),
    avg_order_value=("order_value", "mean"),
).round(4)
print("Ringkasan mentah per grup (sebelum uji statistik):")
print(summary)
print(f"\nData tersimpan: {os.path.join(OUT_DIR, 'ab_test_sessions.csv')}")
print("\nCatatan: 'attach_rate_all' di atas dihitung dari SEMUA sesi (termasuk yang")
print("batal checkout, otomatis attached=False). Attach rate yang benar untuk diuji")
print("adalah attach rate DI ANTARA sesi yang checkout-nya selesai -- lihat ab_test_analysis.py")
