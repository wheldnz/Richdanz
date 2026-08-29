"""
generate_dummy_data.py
=======================
Membuat data dummy realistis untuk studi kasus "TokoAman.id":
marketplace e-commerce yang juga menjual produk asuransi mikro
(embedded insurance) di checkout — gabungan tema retail & insurtech,
salah satu model bisnis yang sedang naik daun.

Hanya pakai numpy + pandas (tidak butuh Faker/internet), supaya bisa
dijalankan di mana saja. Output: 7 file CSV di folder ./data/

Cara pakai:
    python generate_dummy_data.py
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import os

SEED = 42
rng = np.random.default_rng(SEED)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

START_DATE = date(2024, 1, 1)
END_DATE   = date(2026, 6, 30)
ALL_DATES  = pd.date_range(START_DATE, END_DATE, freq="D")
N_DAYS     = len(ALL_DATES)

# ------------------------------------------------------------------
# 1. CUSTOMERS
# ------------------------------------------------------------------
N_CUSTOMERS = 3000

FIRST_NAMES = ["Ahmad", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hadi",
               "Indah", "Joko", "Kartika", "Lestari", "Made", "Nurul", "Oki",
               "Putri", "Rian", "Sari", "Tono", "Umi", "Vina", "Wawan", "Yuni",
               "Zaki", "Agus", "Bella", "Cahyo", "Dian", "Erlangga", "Fitri"]
LAST_NAMES  = ["Saputra", "Wijaya", "Kusuma", "Pratama", "Santoso", "Hidayat",
               "Ramadhan", "Setiawan", "Nugroho", "Permata", "Anggraini",
               "Firmansyah", "Maulana", "Handoko", "Susanti", "Rahayu",
               "Gunawan", "Puspita", "Halim", "Wibowo"]

CITY_PROVINCE = [
    ("Jakarta", "DKI Jakarta"), ("Surabaya", "Jawa Timur"),
    ("Bandung", "Jawa Barat"), ("Medan", "Sumatera Utara"),
    ("Semarang", "Jawa Tengah"), ("Makassar", "Sulawesi Selatan"),
    ("Palembang", "Sumatera Selatan"), ("Depok", "Jawa Barat"),
    ("Denpasar", "Bali"), ("Yogyakarta", "DI Yogyakarta"),
    ("Malang", "Jawa Timur"), ("Balikpapan", "Kalimantan Timur"),
    ("Batam", "Kepulauan Riau"), ("Bekasi", "Jawa Barat"),
    ("Tangerang", "Banten"),
]

CHANNELS = ["Instagram Ads", "TikTok Ads", "Google Ads", "Referral", "Organic", "Email"]
CHANNEL_WEIGHTS = [0.22, 0.20, 0.18, 0.12, 0.20, 0.08]

def random_dates_growth(n, start, end, growth=True):
    """Sample n dates between start/end with a mild upward growth trend
    so later months have a higher chance of being picked (mimics user growth)."""
    days = (end - start).days
    idx = np.arange(days + 1)
    if growth:
        weights = 1 + (idx / days) * 2.2         # later days weigh up to ~3.2x more
    else:
        weights = np.ones(days + 1)
    weights = weights / weights.sum()
    picked = rng.choice(idx, size=n, p=weights)
    return [start + timedelta(days=int(d)) for d in picked]

customer_ids = np.arange(1, N_CUSTOMERS + 1)
signup_dates = random_dates_growth(N_CUSTOMERS, START_DATE, END_DATE, growth=True)

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "full_name": [f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}" for _ in range(N_CUSTOMERS)],
    "gender": rng.choice(["M", "F"], size=N_CUSTOMERS, p=[0.48, 0.52]),
    "signup_date": signup_dates,
})
city_choice_idx = rng.integers(0, len(CITY_PROVINCE), size=N_CUSTOMERS)
customers["city"] = [CITY_PROVINCE[i][0] for i in city_choice_idx]
customers["province"] = [CITY_PROVINCE[i][1] for i in city_choice_idx]
customers["acquisition_channel"] = rng.choice(CHANNELS, size=N_CUSTOMERS, p=CHANNEL_WEIGHTS)
customers = customers[["customer_id", "full_name", "gender", "city", "province",
                        "signup_date", "acquisition_channel"]]

# ------------------------------------------------------------------
# 2. PRODUCTS
# ------------------------------------------------------------------
CATEGORY_PRODUCTS = {
    "Elektronik": [("Smartphone X10", 3200000, 2400000), ("Earbuds Pro", 450000, 280000),
                   ("Power Bank 20000mAh", 250000, 150000), ("Smartwatch Fit", 899000, 550000),
                   ("Laptop Ultraslim 14", 7500000, 6100000), ("Kamera Aksi 4K", 1200000, 850000),
                   ("Speaker Bluetooth Mini", 175000, 95000), ("Charger Fast 65W", 129000, 70000)],
    "Fashion": [("Kemeja Katun Pria", 149000, 80000), ("Dress Wanita Casual", 199000, 110000),
                ("Sepatu Sneakers", 329000, 190000), ("Tas Ransel Harian", 259000, 140000),
                ("Jaket Hoodie", 219000, 120000), ("Celana Jeans Slim", 189000, 100000)],
    "Rumah Tangga": [("Rice Cooker 1.8L", 349000, 230000), ("Blender Portable", 159000, 90000),
                      ("Setrika Uap", 229000, 140000), ("Air Fryer 4L", 599000, 380000),
                      ("Vacuum Cleaner Mini", 449000, 290000)],
    "Kesehatan": [("Vitamin C 1000mg (30 tab)", 65000, 35000), ("Masker Medis (50pcs)", 35000, 18000),
                   ("Hand Sanitizer 500ml", 28000, 14000), ("Timbangan Badan Digital", 119000, 65000),
                   ("Alat Tensimeter Digital", 259000, 160000)],
    "Olahraga": [("Matras Yoga", 99000, 55000), ("Dumbbell Set 5kg", 279000, 170000),
                  ("Botol Minum Olahraga", 45000, 22000), ("Sepatu Lari", 359000, 210000)],
    "Perjalanan": [("Koper Cabin 20 inch", 449000, 270000), ("Tas Travel Organizer", 89000, 45000),
                    ("Bantal Leher Travel", 39000, 18000)],
}

rows = []
pid = 1
for cat, items in CATEGORY_PRODUCTS.items():
    for name, price, cost in items:
        rows.append((pid, name, cat, price, cost))
        pid += 1
products = pd.DataFrame(rows, columns=["product_id", "product_name", "category", "unit_price", "cost_price"])

# ------------------------------------------------------------------
# 3. CAMPAIGNS
# ------------------------------------------------------------------
N_CAMPAIGNS = 42
CAMPAIGN_THEMES = ["Harbolnas", "Gajian Sale", "Ramadan Sale", "Back to School",
                   "Flash Sale Elektronik", "Fashion Week Deal", "Proteksi Gadget Gratis Ongkir",
                   "Travel Ready Bundle", "New Customer Promo", "Loyalty Reward"]
OBJECTIVES = ["Product Sales", "Insurance Signup", "Brand Awareness"]

camp_rows = []
for cid in range(1, N_CAMPAIGNS + 1):
    channel = rng.choice(CHANNELS[:5], p=[0.24, 0.22, 0.20, 0.14, 0.20])  # exclude Email-only weight tweak
    objective = rng.choice(OBJECTIVES, p=[0.55, 0.30, 0.15])
    theme = rng.choice(CAMPAIGN_THEMES)
    start = START_DATE + timedelta(days=int(rng.integers(0, N_DAYS - 20)))
    duration = int(rng.integers(5, 21))
    end = start + timedelta(days=duration)
    budget = float(rng.integers(5, 80)) * 1_000_000  # 5jt - 80jt
    camp_rows.append((cid, f"{theme} #{cid}", channel, objective, start, end, budget))

campaigns = pd.DataFrame(camp_rows, columns=["campaign_id", "campaign_name", "channel",
                                              "objective", "start_date", "end_date", "budget"])
campaigns["start_date"] = pd.to_datetime(campaigns["start_date"])
campaigns["end_date"] = pd.to_datetime(campaigns["end_date"])

def campaign_active_on(d, objective_filter=None):
    d = pd.Timestamp(d)
    mask = (campaigns["start_date"] <= d) & (campaigns["end_date"] >= d)
    if objective_filter:
        mask &= campaigns["objective"].isin(objective_filter)
    active = campaigns[mask]
    if len(active) == 0:
        return None
    return int(active.sample(1, random_state=rng.integers(0, 1_000_000)).iloc[0]["campaign_id"])

# ------------------------------------------------------------------
# 4. ORDERS + ORDER_ITEMS  (dengan trend pertumbuhan + musiman)
# ------------------------------------------------------------------
# Bobot harian: naik seiring waktu + lonjakan Harbolnas (11/11,12/12), gajian (25-31),
# dan periode Ramadan/Lebaran (perkiraan kasar per tahun)
RAMADAN_WINDOWS = [
    (date(2024, 3, 11), date(2024, 4, 13)),
    (date(2025, 3, 1),  date(2025, 4, 1)),
    (date(2026, 2, 18), date(2026, 3, 22)),
]

def is_in_windows(d, windows):
    return any(w[0] <= d <= w[1] for w in windows)

day_weights = []
for i, d in enumerate(ALL_DATES):
    dd = d.date()
    w = 1.0 + (i / N_DAYS) * 2.5          # trend pertumbuhan jangka panjang
    if dd.day >= 25 or dd.day <= 2:       # musim gajian
        w *= 1.35
    if (dd.month == 11 and dd.day == 11) or (dd.month == 12 and dd.day == 12):
        w *= 4.0                           # Harbolnas
    if dd.month == 12 and dd.day >= 20:
        w *= 1.4                           # akhir tahun
    if is_in_windows(dd, RAMADAN_WINDOWS):
        w *= 1.5                           # Ramadan/Lebaran
    if d.weekday() >= 5:
        w *= 1.15                          # weekend sedikit lebih ramai
    day_weights.append(w)
day_weights = np.array(day_weights)
day_probs = day_weights / day_weights.sum()

N_ORDERS = 15000
order_dates_idx = rng.choice(np.arange(N_DAYS), size=N_ORDERS, p=day_probs)
order_dates = [ALL_DATES[i].date() for i in order_dates_idx]
order_dates_sorted = sorted(order_dates)  # order_id sequential roughly follows time

# customer harus sudah signup sebelum order -> pilih customer yang eligible per tanggal
customers_sorted = customers.sort_values("signup_date").reset_index(drop=True)
signup_arr = customers_sorted["signup_date"].values
cust_id_arr = customers_sorted["customer_id"].values

order_rows = []
item_rows = []
order_id = 1
item_id = 1

# precompute product pool per category for quick sampling
product_ids_by_cat = {cat: products.loc[products.category == cat, "product_id"].tolist()
                       for cat in CATEGORY_PRODUCTS}
all_product_ids = products["product_id"].tolist()
product_price_map = dict(zip(products.product_id, products.unit_price))

STATUS_CHOICES = ["Completed", "Cancelled", "Returned"]
STATUS_PROBS = [0.88, 0.07, 0.05]
DEVICE_CHOICES = ["App", "Web"]

for od in order_dates_sorted:
    eligible_count = np.searchsorted(signup_arr, np.datetime64(od), side="right")
    if eligible_count < 5:
        continue
    cust = int(cust_id_arr[rng.integers(0, eligible_count)])

    channel = rng.choice(DEVICE_CHOICES, p=[0.7, 0.3])
    status = rng.choice(STATUS_CHOICES, p=STATUS_PROBS)
    camp_id = campaign_active_on(pd.Timestamp(od), objective_filter=["Product Sales", "Brand Awareness"])

    order_rows.append((order_id, cust, od, camp_id, channel, status))

    n_items = int(rng.choice([1, 2, 3], p=[0.55, 0.30, 0.15]))
    chosen_products = rng.choice(all_product_ids, size=n_items, replace=False)
    for p in chosen_products:
        qty = int(rng.choice([1, 2, 3], p=[0.7, 0.22, 0.08]))
        price = product_price_map[p]
        item_rows.append((item_id, order_id, int(p), qty, price))
        item_id += 1

    order_id += 1

orders = pd.DataFrame(order_rows, columns=["order_id", "customer_id", "order_date",
                                            "campaign_id", "channel", "order_status"])
order_items = pd.DataFrame(item_rows, columns=["order_item_id", "order_id", "product_id",
                                                "quantity", "unit_price"])

# ------------------------------------------------------------------
# 5. INSURANCE POLICIES (embedded di checkout + standalone travel)
# ------------------------------------------------------------------
POLICY_TYPES = ["Gadget Protection", "Shipping Insurance", "Travel Insurance"]
PREMIUM_RANGE = {"Gadget Protection": (29000, 89000),
                  "Shipping Insurance": (5000, 15000),
                  "Travel Insurance": (39000, 150000)}
COVERAGE_DAYS = {"Gadget Protection": 365, "Shipping Insurance": 14, "Travel Insurance": 30}

completed_orders = orders[orders.order_status == "Completed"].copy()
elektronik_ids = set(product_ids_by_cat["Elektronik"])
orders_with_elektronik = set(
    order_items.loc[order_items.product_id.isin(elektronik_ids), "order_id"]
)

policy_rows = []
policy_id = 1

# 5a. Embedded: attach ke order (gadget protection utk order elektronik, shipping utk order lain)
for _, o in completed_orders.iterrows():
    attach_prob = 0.35 if o.order_id in orders_with_elektronik else 0.15
    if rng.random() < attach_prob:
        ptype = "Gadget Protection" if o.order_id in orders_with_elektronik and rng.random() < 0.7 else "Shipping Insurance"
        lo, hi = PREMIUM_RANGE[ptype]
        premium = float(rng.integers(lo, hi))
        start = pd.Timestamp(o.order_date)
        end = start + timedelta(days=COVERAGE_DAYS[ptype])
        camp = campaign_active_on(start, objective_filter=["Insurance Signup"])
        policy_rows.append((policy_id, o.customer_id, o.order_id, camp, ptype, premium,
                             start.date(), end.date()))
        policy_id += 1

# 5b. Standalone: travel insurance (tidak terikat order)
N_TRAVEL_POLICIES = 900
for _ in range(N_TRAVEL_POLICIES):
    d_idx = rng.integers(0, N_DAYS)
    start_dt = ALL_DATES[d_idx]
    eligible_count = np.searchsorted(signup_arr, np.datetime64(start_dt.date()), side="right")
    if eligible_count < 5:
        continue
    cust = int(cust_id_arr[rng.integers(0, eligible_count)])
    lo, hi = PREMIUM_RANGE["Travel Insurance"]
    premium = float(rng.integers(lo, hi))
    end = start_dt + timedelta(days=COVERAGE_DAYS["Travel Insurance"])
    camp = campaign_active_on(start_dt, objective_filter=["Insurance Signup"])
    policy_rows.append((policy_id, cust, None, camp, "Travel Insurance", premium,
                         start_dt.date(), end.date()))
    policy_id += 1

insurance_policies = pd.DataFrame(policy_rows, columns=[
    "policy_id", "customer_id", "order_id", "campaign_id", "policy_type",
    "premium", "start_date", "end_date"])

# Tentukan status polis relatif terhadap "hari ini" simulasi = END_DATE
TODAY = pd.Timestamp(END_DATE)
def determine_status(row):
    end = pd.Timestamp(row.end_date)
    if end >= TODAY:
        return "Active"
    # sudah lewat masa berlaku -> sebagian renew, sebagian lapse/cancelled
    r = rng.random()
    if r < 0.55:
        return "Expired"      # habis begitu saja / tidak renew (churn asuransi)
    elif r < 0.85:
        return "Renewed"
    else:
        return "Cancelled"

insurance_policies["policy_status"] = insurance_policies.apply(determine_status, axis=1)
insurance_policies = insurance_policies[[
    "policy_id", "customer_id", "order_id", "campaign_id", "policy_type",
    "premium", "start_date", "end_date", "policy_status"]]

# ------------------------------------------------------------------
# 6. CLAIMS
# ------------------------------------------------------------------
CLAIM_TYPE_MAP = {
    "Gadget Protection": ["Layar Retak", "Kerusakan Air", "Kehilangan", "Baterai Rusak"],
    "Shipping Insurance": ["Barang Rusak saat Kirim", "Paket Hilang", "Salah Kirim"],
    "Travel Insurance": ["Pembatalan Perjalanan", "Bagasi Hilang", "Keterlambatan Penerbangan", "Medis Darurat"],
}
CLAIM_RATE = 0.10  # ~10% polis mengajukan klaim

claim_rows = []
claim_id = 1
claimable = insurance_policies[insurance_policies.policy_status.isin(
    ["Expired", "Renewed", "Cancelled", "Active"])]
claim_sample = claimable.sample(frac=CLAIM_RATE, random_state=SEED)

for _, p in claim_sample.iterrows():
    start = pd.Timestamp(p.start_date)
    end = pd.Timestamp(p.end_date)
    span = max((end - start).days, 1)
    claim_date = (start + timedelta(days=int(rng.integers(1, span)))).date()
    ctype = rng.choice(CLAIM_TYPE_MAP[p.policy_type])
    claim_amount = float(rng.integers(int(p.premium * 2), int(p.premium * 15)))
    status = rng.choice(["Approved", "Rejected", "Pending"], p=[0.68, 0.22, 0.10])
    claim_rows.append((claim_id, p.policy_id, claim_date, ctype, claim_amount, status))
    claim_id += 1

claims = pd.DataFrame(claim_rows, columns=["claim_id", "policy_id", "claim_date",
                                            "claim_type", "claim_amount", "claim_status"])

# ------------------------------------------------------------------
# SIMPAN KE CSV
# ------------------------------------------------------------------
customers.to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)
products.to_csv(os.path.join(OUT_DIR, "products.csv"), index=False)
campaigns.to_csv(os.path.join(OUT_DIR, "campaigns.csv"), index=False)
orders.to_csv(os.path.join(OUT_DIR, "orders.csv"), index=False)
order_items.to_csv(os.path.join(OUT_DIR, "order_items.csv"), index=False)
insurance_policies.to_csv(os.path.join(OUT_DIR, "insurance_policies.csv"), index=False)
claims.to_csv(os.path.join(OUT_DIR, "claims.csv"), index=False)

print("Selesai! Ringkasan data yang dibuat:")
print(f"  customers           : {len(customers):,}")
print(f"  products             : {len(products):,}")
print(f"  campaigns             : {len(campaigns):,}")
print(f"  orders                : {len(orders):,}")
print(f"  order_items            : {len(order_items):,}")
print(f"  insurance_policies      : {len(insurance_policies):,}")
print(f"  claims                    : {len(claims):,}")
print(f"\nFile CSV tersimpan di: {os.path.abspath(OUT_DIR)}")
