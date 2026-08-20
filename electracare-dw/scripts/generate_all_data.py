"""
Enterprise Data Warehouse Data Generator & Bulk Loader
Company: PT ElectraCare Indonesia (Aftersales Electronics)
Database: db_electracare_dw
Total Rows Target: ~5.8 Million Rows across 13 Dimensions and 10 Fact Tables
"""

import sys
import os
import random
import datetime
from io import StringIO
import psycopg2

# DB Config
DB_NAME = "db_electracare_dw"
DB_USER = "postgres"
DB_PASS = "admin123"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

DATA_LAKE_RAW = os.path.join(os.path.dirname(__file__), "..", "data_lake", "raw")

BASE_DATE = datetime.date(2022, 1, 1)
MAX_DAYS = (datetime.date(2025, 12, 31) - BASE_DATE).days # 1460 days

def get_random_date_pair(max_duration_days=10):
    start_offset = random.randint(0, MAX_DAYS - max_duration_days)
    duration = random.randint(0, max_duration_days)
    d_start = BASE_DATE + datetime.timedelta(days=start_offset)
    d_end = d_start + datetime.timedelta(days=duration)
    return int(d_start.strftime("%Y%m%d")), int(d_end.strftime("%Y%m%d")), duration

def get_random_date_key():
    offset = random.randint(0, MAX_DAYS)
    d = BASE_DATE + datetime.timedelta(days=offset)
    return int(d.strftime("%Y%m%d"))

def get_db_connection(dbname=DB_NAME):
    conn = psycopg2.connect(
        dbname=dbname,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    return conn

def create_database_if_not_exists():
    print(f"Checking database '{DB_NAME}'...")
    conn = get_db_connection(dbname="postgres")
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cur.fetchone()
    if not exists:
        print(f"Creating database '{DB_NAME}'...")
        cur.execute(f"CREATE DATABASE {DB_NAME}")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()

def execute_sql_file(filepath):
    print(f"Executing DDL script: {filepath}...")
    conn = get_db_connection()
    cur = conn.cursor()
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
    cur.execute(sql)
    cur.close()
    conn.close()
    print("DDL script executed successfully.")

def bulk_insert_copy(conn, table_name, columns, buffer_data):
    cur = conn.cursor()
    cols_str = ",".join(columns)
    sql = f"COPY {table_name} ({cols_str}) FROM STDIN WITH (FORMAT csv, HEADER false, DELIMITER '\t')"
    buffer_data.seek(0)
    cur.copy_expert(sql, buffer_data)
    cur.close()

# --------------------------------------------------------------------
# 1. GENERATE DIMENSIONS
# --------------------------------------------------------------------

def generate_dim_date(conn):
    print("Generating dwh.dim_date (1,461 rows)...")
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    
    holidays = {
        (1, 1): "Tahun Baru Masehi", (5, 1): "Hari Buruh", (6, 1): "Hari Lahir Pancasila",
        (8, 17): "Hari Kemerdekaan RI", (12, 25): "Hari Natal"
    }

    buf = StringIO()
    cols = [
        "date_key", "full_date", "day_of_week", "day_name", "day_of_month",
        "day_of_year", "week_of_year", "month_number", "month_name", "month_short",
        "quarter", "quarter_name", "year", "fiscal_year", "is_weekend",
        "is_holiday_id", "year_month", "year_quarter"
    ]
    
    curr = start_date
    count = 0
    while curr <= end_date:
        date_key = int(f"{curr.year}{curr.month:02d}{curr.day:02d}")
        day_of_week = curr.isoweekday() # 1=Mon, 7=Sun
        day_name = curr.strftime("%A")
        day_of_month = curr.day
        day_of_year = curr.timetuple().tm_yday
        week_of_year = curr.isocalendar()[1]
        month_number = curr.month
        month_name = curr.strftime("%B")
        month_short = curr.strftime("%b")
        quarter = (month_number - 1) // 3 + 1
        quarter_name = f"Q{quarter}"
        year = curr.year
        fiscal_year = year
        is_weekend = day_of_week in (6, 7)
        is_holiday = (curr.month, curr.day) in holidays
        year_month = f"{year}-{month_number:02d}"
        year_quarter = f"{year}-Q{quarter}"

        row = [
            str(date_key), str(curr), str(day_of_week), day_name, str(day_of_month),
            str(day_of_year), str(week_of_year), str(month_number), month_name, month_short,
            str(quarter), quarter_name, str(year), str(fiscal_year), str(is_weekend).upper(),
            str(is_holiday).upper(), year_month, year_quarter
        ]
        buf.write("\t".join(row) + "\n")
        curr += datetime.timedelta(days=1)
        count += 1

    bulk_insert_copy(conn, "dwh.dim_date", cols, buf)
    print(f"dwh.dim_date inserted: {count} rows.")

def generate_dim_geography(conn):
    print("Generating dwh.dim_geography (30 rows)...")
    cities = [
        ("Jakarta Pusat", "DKI Jakarta", "Jabodetabek", True),
        ("Jakarta Selatan", "DKI Jakarta", "Jabodetabek", True),
        ("Jakarta Barat", "DKI Jakarta", "Jabodetabek", True),
        ("Jakarta Timur", "DKI Jakarta", "Jabodetabek", True),
        ("Jakarta Utara", "DKI Jakarta", "Jabodetabek", True),
        ("Tangerang", "Banten", "Jabodetabek", True),
        ("Bekasi", "Jawa Barat", "Jabodetabek", True),
        ("Depok", "Jawa Barat", "Jabodetabek", True),
        ("Bogor", "Jawa Barat", "Jabodetabek", False),
        ("Surabaya", "Jawa Timur", "Jawa", True),
        ("Bandung", "Jawa Barat", "Jawa", True),
        ("Medan", "Sumatera Utara", "Sumatera", True),
        ("Semarang", "Jawa Tengah", "Jawa", False),
        ("Makassar", "Sulawesi Selatan", "Sulawesi", False),
        ("Palembang", "Sumatera Selatan", "Sumatera", False),
        ("Batam", "Kepulauan Riau", "Sumatera", False),
        ("Pekanbaru", "Riau", "Sumatera", False),
        ("Denpasar", "Bali", "Bali & Nusa Tenggara", False),
        ("Yogyakarta", "DI Yogyakarta", "Jawa", False),
        ("Malang", "Jawa Timur", "Jawa", False),
        ("Solo", "Jawa Tengah", "Jawa", False),
        ("Balikpapan", "Kalimantan Timur", "Kalimantan", False),
        ("Samarinda", "Kalimantan Timur", "Kalimantan", False),
        ("Banjarmasin", "Kalimantan Selatan", "Kalimantan", False),
        ("Pontianak", "Kalimantan Barat", "Kalimantan", False),
        ("Manado", "Sulawesi Utara", "Sulawesi", False),
        ("Mataram", "Nusa Tenggara Barat", "Bali & Nusa Tenggara", False),
        ("Kupang", "Nusa Tenggara Timur", "Bali & Nusa Tenggara", False),
        ("Ambon", "Maluku", "Papua & Maluku", False),
        ("Jayapura", "Papua", "Papua & Maluku", False),
    ]
    buf = StringIO()
    cols = ["city", "province", "region", "country", "timezone", "is_tier_1_city"]
    for city, prov, reg, t1 in cities:
        tz = "WITA" if reg in ("Sulawesi", "Bali & Nusa Tenggara") else "WIT" if reg == "Papua & Maluku" else "WIB"
        buf.write("\t".join([city, prov, reg, "Indonesia", tz, str(t1).upper()]) + "\n")

    bulk_insert_copy(conn, "dwh.dim_geography", cols, buf)
    print("dwh.dim_geography inserted: 30 rows.")

def generate_dim_customer(conn):
    print("Generating dwh.dim_customer (250,000 rows)...")
    first_names = ["Budi", "Siti", "Agus", "Dewi", "Eko", "Rina", "Rudi", "Nur", "Bambang", "Sri", "Andi", "Maya", "Dedi", "Indah", "Hendra", "Novi", "Ahmad", "Lilis", "Taufik", "Rini"]
    last_names = ["Santoso", "Wijaya", "Kusuma", "Saputra", "Pratama", "Hidayat", "Nugroho", "Utami", "Laksana", "Permana", "Setiawan", "Wibowo", "Suryadi", "Rahayu", "Firmansyah"]
    
    source_systems = ["SERVICE", "WARRANTY", "INSURANCE", "RETAIL"]
    segments = ["Individual", "Individual", "Individual", "Corporate", "Reseller"]
    tiers = ["Bronze", "Bronze", "Bronze", "Silver", "Silver", "Gold", "Platinum"]
    genders = ["Male", "Female"]
    age_groups = ["18-25", "26-35", "36-45", "46-55", "56+"]

    buf = StringIO()
    cols = [
        "customer_id", "source_system", "customer_name", "phone_number", "email",
        "gender", "age_group", "geo_key", "customer_segment", "registration_date_key",
        "loyalty_tier", "total_lifetime_visits", "status"
    ]

    for i in range(1, 250001):
        cid = f"CUST-{i:06d}"
        src = random.choice(source_systems)
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"0812{random.randint(10000000, 99999999)}"
        email = f"user_{i}@electracare-demo.id"
        gender = random.choice(genders)
        age = random.choice(age_groups)
        geo_key = random.randint(1, 30)
        seg = random.choice(segments)
        reg_date_key = get_random_date_key()
        tier = random.choice(tiers)
        visits = random.randint(1, 15)
        status = "Active" if random.random() > 0.1 else "Churned"

        row = [cid, src, name, phone, email, gender, age, str(geo_key), seg, str(reg_date_key), tier, str(visits), status]
        buf.write("\t".join(row) + "\n")
        
        if i % 50000 == 0:
            bulk_insert_copy(conn, "dwh.dim_customer", cols, buf)
            buf = StringIO()
            print(f"  ... inserted {i}/250,000 customers")

    if buf.getvalue():
        bulk_insert_copy(conn, "dwh.dim_customer", cols, buf)
    print("dwh.dim_customer inserted: 250,000 rows.")

def generate_dim_device(conn):
    print("Generating dwh.dim_device (2,500 rows)...")
    brands = [
        ("Samsung", ["Galaxy S24 Ultra", "Galaxy S23 FE", "Galaxy Z Fold5", "Galaxy A55", "Galaxy Tab S9", "Galaxy Book4"]),
        ("Apple", ["iPhone 15 Pro Max", "iPhone 14", "iPhone 13", "iPad Air M2", "MacBook Pro M3", "MacBook Air M2"]),
        ("Xiaomi", ["Xiaomi 14", "Redmi Note 13 Pro", "Poco F6", "Pad 6 Pro"]),
        ("OPPO", ["Find N3 Flip", "Reno11 Pro", "A79 5G"]),
        ("Vivo", ["X100 Pro", "V30 5G", "Y100"]),
        ("Realme", ["Realme GT5", "Realme 12 Pro+"]),
        ("Infinix", ["Zero 30 5G", "Note 40 Pro", "GT 20 Pro"]),
        ("ASUS", ["ROG Phone 8", "Zenbook 14 OLED", "TUF Gaming F15"]),
        ("Lenovo", ["Legion Slim 5", "IdeaPad Slim 3", "Yoga Slim 7i"]),
        ("HP", ["Spectre x360", "Pavilion Plus 14", "Omen 16"]),
        ("Dell", ["XPS 13 Plus", "Inspiron 15", "Alienware m16"]),
        ("Acer", ["Predator Helios 16", "Swift Go 14", "Aspire 5"]),
        ("Huawei", ["P60 Pro", "MatePad Pro 13.2"]),
        ("OnePlus", ["OnePlus 12", "OnePlus Nord 3"]),
        ("Nothing", ["Phone (2)", "Phone (2a)"])
    ]
    subcategories = ["Flagship", "Mid-Range", "Entry-Level", "Gaming", "Business"]

    buf = StringIO()
    cols = ["device_id", "device_name", "brand", "category", "subcategory", "launch_year", "msrp_idr", "warranty_months", "is_active"]
    
    count = 0
    for i in range(1, 2501):
        brand, models = random.choice(brands)
        model = random.choice(models)
        cat = "Laptop" if "Book" in model or "MacBook" in model or "Legion" in model or "Zenbook" in model or "XPS" in model or "Predator" in model or "Pavilion" in model else "Tablet" if "Tab" in model or "iPad" in model or "Pad" in model else "Smartphone"
        subcat = "Gaming" if "ROG" in model or "Legion" in model or "Predator" in model or "Poco" in model or "GT" in model else "Flagship" if "Ultra" in model or "Pro Max" in model or "Fold" in model or "S24" in model or "15 Pro" in model else random.choice(subcategories)
        yr = random.randint(2021, 2024)
        msrp = random.choice([2999000, 4999000, 7999000, 12999000, 18999000, 24999000, 32999000])
        w_months = random.choice([12, 12, 12, 24])

        dev_id = f"DEV-{i:05d}"
        dev_name = f"{brand} {model} Spec-{i}"
        row = [dev_id, dev_name, brand, cat, subcat, str(yr), str(msrp), str(w_months), "TRUE"]
        buf.write("\t".join(row) + "\n")
        count += 1

    bulk_insert_copy(conn, "dwh.dim_device", cols, buf)
    print(f"dwh.dim_device inserted: {count} rows.")

def generate_dim_spare_part(conn):
    print("Generating dwh.dim_spare_part (8,000 rows)...")
    categories = [
        ("LCD/Screen", 800000, 1500000),
        ("Battery", 250000, 600000),
        ("IC/Chipset", 450000, 950000),
        ("Casing/Frame", 150000, 400000),
        ("Camera Module", 350000, 850000),
        ("Flex Cable", 80000, 200000),
        ("Charging Port", 70000, 180000)
    ]
    brands = ["Samsung", "Apple", "Xiaomi", "OPPO", "Vivo", "Realme", "Infinix", "ASUS", "Lenovo", "HP", "Dell", "Acer", "Huawei", "OnePlus", "Nothing"]

    buf = StringIO()
    cols = ["part_id", "part_name", "part_category", "compatible_brand", "unit_cost_idr", "unit_price_idr", "lead_time_days", "is_original"]

    for i in range(1, 8001):
        cat, min_cost, max_cost = random.choice(categories)
        brand = random.choice(brands)
        cost = random.randint(min_cost, max_cost)
        price = int(cost * random.uniform(1.3, 1.8))
        part_id = f"PART-{i:05d}"
        part_name = f"{cat} Original {brand} Variant-{i}"
        lead = random.randint(2, 10)
        is_orig = "TRUE" if random.random() > 0.15 else "FALSE"

        row = [part_id, part_name, cat, brand, str(cost), str(price), str(lead), is_orig]
        buf.write("\t".join(row) + "\n")

    bulk_insert_copy(conn, "dwh.dim_spare_part", cols, buf)
    print("dwh.dim_spare_part inserted: 8,000 rows.")

def generate_other_dims(conn):
    print("Generating remaining dimensions (Service Centers, Brand Partners, Employees, Suppliers, Warehouses, Insurance Partners, Policies, Junk Flags)...")

    # 1. Service Centers (25)
    buf = StringIO()
    cols = ["center_id", "center_name", "center_type", "geo_key", "capacity_slots_per_day", "opening_date", "is_active"]
    types = ["Main Service Center", "Authorized Repair Point", "Retail Spare Parts"]
    for i in range(1, 26):
        cname = f"ElectraCare Center #{i}"
        ctype = types[0] if i <= 10 else types[1] if i <= 20 else types[2]
        gkey = i
        cap = random.randint(40, 120)
        odate = "2021-01-15"
        buf.write("\t".join([str(i), cname, ctype, str(gkey), str(cap), odate, "TRUE"]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_service_center", cols, buf)

    # 2. Brand Partners (15)
    buf = StringIO()
    cols = ["partner_id", "partner_name", "brand", "contract_type", "sla_target_days", "commission_pct"]
    brands = ["Samsung", "Apple", "Xiaomi", "OPPO", "Vivo", "Realme", "Infinix", "ASUS", "Lenovo", "HP", "Dell", "Acer", "Huawei", "OnePlus", "Nothing"]
    for i, b in enumerate(brands, 1):
        pname = f"{b} Indonesia Official"
        ctype = "Exclusive" if b in ("Samsung", "Apple") else "Authorized"
        sla = 5 if b in ("Samsung", "Apple") else 7
        comm = 12.5 if b in ("Samsung", "Apple") else 15.0
        buf.write("\t".join([str(i), pname, b, ctype, str(sla), str(comm)]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_brand_partner", cols, buf)

    # 3. Employees (2,000)
    buf = StringIO()
    cols = ["employee_id", "employee_name", "department", "job_role", "job_level", "certification", "center_key", "salary_idr", "hire_date", "status", "scd_effective_date", "scd_expiry_date", "scd_is_current"]
    roles = [
        ("Technical", "Senior Technician", 3, 12000000),
        ("Technical", "Junior Technician", 1, 6000000),
        ("Technical", "Field Engineer", 2, 8500000),
        ("Customer Service", "CS Representative", 1, 5500000),
        ("Logistics", "Warehouse Inspector", 2, 7000000)
    ]
    for i in range(1, 2001):
        ename = f"Emp_{i}"
        dept, role, lvl, base_sal = random.choice(roles)
        cert = "Multi-brand Certified" if lvl >= 2 else "Basic Trained"
        ckey = random.randint(1, 25)
        sal = base_sal + random.randint(0, 2000000)
        hdate = "2022-01-01"
        buf.write("\t".join([str(i), ename, dept, role, str(lvl), cert, str(ckey), str(sal), hdate, "Active", "2022-01-01", "9999-12-31", "TRUE"]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_employee", cols, buf)

    # 4. Suppliers (20)
    buf = StringIO()
    cols = ["supplier_id", "supplier_name", "geo_key", "supplier_type", "contracted_lead_time_days", "payment_terms_days", "is_active"]
    for i in range(1, 21):
        sname = f"Global Spare Parts Supplier #{i}"
        gkey = random.randint(1, 30)
        stype = "OEM Manufacturer" if i <= 10 else "Authorized Distributor"
        lead = random.randint(5, 14)
        pay = 30
        buf.write("\t".join([str(i), sname, str(gkey), stype, str(lead), str(pay), "TRUE"]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_supplier", cols, buf)

    # 5. Warehouses (5)
    buf = StringIO()
    cols = ["warehouse_id", "warehouse_name", "warehouse_type", "geo_key", "capacity_cbm", "cold_storage"]
    whs = [
        ("Central Hub Jakarta", "Central Hub", 1, 5000, "TRUE"),
        ("Regional Hub Surabaya", "Regional Hub", 10, 3000, "TRUE"),
        ("Regional Hub Medan", "Regional Hub", 12, 2500, "FALSE"),
        ("Satellite Makassar", "Satellite", 14, 1500, "FALSE"),
        ("Satellite Balikpapan", "Satellite", 22, 1200, "FALSE")
    ]
    for i, (wname, wtype, gkey, cap, cold) in enumerate(whs, 1):
        buf.write("\t".join([str(i), wname, wtype, str(gkey), str(cap), cold]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_warehouse", cols, buf)

    # 6. Insurance Partners (9)
    buf = StringIO()
    cols = ["partner_id", "partner_name", "sla_target_days", "partner_tier", "commission_pct"]
    ip_list = ["Qoala", "Igloo", "PasarPolis", "Chubb", "ACA", "Tokio Marine", "Zurich", "Allianz", "BCA Insurance"]
    for i, ip in enumerate(ip_list, 1):
        tier = "Platinum" if ip in ("Qoala", "Chubb", "Allianz") else "Gold"
        buf.write("\t".join([str(i), f"{ip} Device Protection", "7", tier, "12.00"]) + "\n")
    bulk_insert_copy(conn, "dwh.dim_insurance_partner", cols, buf)

    # 7. Policies (100,000)
    print("  ... generating 100,000 insurance policies ...")
    buf = StringIO()
    cols = ["policy_id", "customer_key", "device_key", "insurance_key", "policy_type", "coverage_level", "premium_monthly_idr", "deductible_idr", "effective_date_key", "expiry_date_key", "status"]
    ptypes = ["Screen Protection", "Full Device Protection", "Extended Warranty"]
    for i in range(1, 100001):
        ckey = random.randint(1, 250000)
        dkey = random.randint(1, 2500)
        ikey = random.randint(1, 9)
        ptype = random.choice(ptypes)
        prem = random.choice([25000, 49000, 79000, 129000])
        ded = 100000
        eff = get_random_date_key()
        exp = get_random_date_key()
        buf.write("\t".join([str(i), str(ckey), str(dkey), str(ikey), ptype, "Standard", str(prem), str(ded), str(eff), str(exp), "Active"]) + "\n")
        if i % 50000 == 0:
            bulk_insert_copy(conn, "dwh.dim_policy", cols, buf)
            buf = StringIO()
    if buf.getvalue():
        bulk_insert_copy(conn, "dwh.dim_policy", cols, buf)

    # 8. Junk Flags (128)
    buf = StringIO()
    cols = ["is_weekend_service", "is_repeat_customer", "is_warranty_covered", "is_insurance_covered", "is_sla_breach", "is_escalated", "is_original_part_used", "priority_level", "service_type"]
    for b1 in [False, True]:
        for b2 in [False, True]:
            for b3 in [False, True]:
                for b4 in [False, True]:
                    for b5 in [False, True]:
                        plevel = random.choice(["Low", "Medium", "High", "Critical"])
                        stype = random.choice(["Walk-in", "Pick-up", "On-site", "Mail-in"])
                        row = [str(b1).upper(), str(b2).upper(), str(b3).upper(), str(b4).upper(), str(b5).upper(), "FALSE", "TRUE", plevel, stype]
                        buf.write("\t".join(row) + "\n")
    bulk_insert_copy(conn, "dwh.dim_junk_flags", cols, buf)
    print("Other dimensions inserted successfully.")

# --------------------------------------------------------------------
# 2. GENERATE FACT TABLES
# --------------------------------------------------------------------

def generate_fact_service_orders_and_parts(conn):
    print("Generating dwh.fact_service_orders (500,000 rows) & dwh.fact_parts_usage (750,000 rows)...")
    
    buf_so = StringIO()
    cols_so = [
        "order_id", "order_date_key", "completion_date_key", "customer_key", "device_key",
        "center_key", "technician_key", "brand_partner_key", "geo_key", "junk_key",
        "service_category", "service_fee_idr", "parts_revenue_idr", "total_revenue_idr",
        "total_cost_idr", "profit_idr", "turnaround_time_hours"
    ]
    
    categories = ["Warranty Repair", "Paid Repair", "Screen Replace", "Battery Replace", "Trade-In", "Diagnosis Only"]
    
    so_count = 500000
    batch_size = 50000

    for b in range(0, so_count, batch_size):
        buf_so = StringIO()
        for i in range(b + 1, b + batch_size + 1):
            oid = f"SO-{i:07d}"
            odate_key, cdate_key, _ = get_random_date_pair(max_duration_days=5)
            
            ckey = random.randint(1, 250000)
            dkey = random.randint(1, 2500)
            center_key = random.randint(1, 25)
            tech_key = random.randint(1, 2000)
            bp_key = random.randint(1, 15)
            gkey = random.randint(1, 30)
            jkey = random.randint(1, 32)
            
            scat = random.choice(categories)
            sfee = random.choice([150000, 250000, 350000, 500000]) if scat != "Warranty Repair" else 0
            prevenue = random.randint(200000, 2500000) if "Replace" in scat or "Paid" in scat else 0
            tot_rev = sfee + prevenue
            
            # --- ANOMALY INJECTION 1: Harbolnas Spikes & Outage Drops ---
            odate_str = str(odate_key)
            if odate_str.endswith("1111") or odate_str.endswith("1212"):
                tot_rev = int(tot_rev * random.uniform(3.5, 5.0))
                sfee = int(sfee * random.uniform(3.5, 5.0))
                prevenue = int(prevenue * random.uniform(3.5, 5.0))
            elif 20240810 <= odate_key <= 20240817:
                tot_rev = int(tot_rev * 0.20)
                sfee = int(sfee * 0.20)
                prevenue = int(prevenue * 0.20)

            # --- ANOMALY INJECTION 2: Data Quality Noise (0.5% Negative Refund, 0.2% Fat-Finger Error) ---
            rand_noise = random.random()
            if rand_noise < 0.005:
                tot_rev = -abs(tot_rev)
            elif rand_noise < 0.007:
                tot_rev = tot_rev * 100

            tot_cost = int(abs(tot_rev) * random.uniform(0.55, 0.75))
            profit = tot_rev - tot_cost

            # --- ANOMALY INJECTION 3: Operational SLA Bottleneck in ISC Jakarta Selatan (center_key == 3) ---
            tat_hrs = random.randint(4, 96)
            if center_key == 3 and 20240601 <= odate_key <= 20240930:
                if random.random() < 0.38:
                    tat_hrs = random.randint(14 * 24, 21 * 24) # 14-21 Days Severe Delay

            row = [
                oid, str(odate_key), str(cdate_key), str(ckey), str(dkey),
                str(center_key), str(tech_key), str(bp_key), str(gkey), str(jkey),
                scat, str(sfee), str(prevenue), str(tot_rev), str(tot_cost), str(profit), str(tat_hrs)
            ]
            buf_so.write("\t".join(row) + "\n")

        bulk_insert_copy(conn, "dwh.fact_service_orders", cols_so, buf_so)
        print(f"  ... inserted {b + batch_size}/500,000 fact_service_orders")

    # Generate fact_parts_usage (750,000 rows)
    print("  ... generating 750,000 rows for dwh.fact_parts_usage ...")
    cols_pu = ["service_order_key", "part_key", "order_date_key", "quantity", "unit_cost_idr", "unit_price_idr", "line_revenue_idr", "line_cost_idr", "line_margin_idr"]
    
    pu_count = 750000
    for b in range(0, pu_count, 100000):
        buf_pu = StringIO()
        for _ in range(100000):
            so_key = random.randint(1, 500000)
            part_key = random.randint(1, 8000)
            odate_key = get_random_date_key()
            qty = random.choice([1, 1, 1, 2])
            cost = random.randint(200000, 1000000)
            price = int(cost * 1.4)
            lrev = qty * price
            lcost = qty * cost
            lmargin = lrev - lcost
            buf_pu.write("\t".join([str(so_key), str(part_key), str(odate_key), str(qty), str(cost), str(price), str(lrev), str(lcost), str(lmargin)]) + "\n")

        bulk_insert_copy(conn, "dwh.fact_parts_usage", cols_pu, buf_pu)
        print(f"  ... inserted {b + 100000}/750,000 fact_parts_usage")

def generate_fact_inventory_and_others(conn):
    print("Generating dwh.fact_inventory_snapshot (2,400,000 rows)...")
    cols_inv = ["snapshot_date_key", "warehouse_key", "part_key", "quantity_on_hand", "quantity_reserved", "quantity_in_transit", "reorder_point", "days_of_supply"]
    
    total_inv = 2400000
    for b in range(0, total_inv, 200000):
        buf_inv = StringIO()
        for _ in range(200000):
            sdate = get_random_date_key()
            wh = random.randint(1, 5)
            part = random.randint(1, 8000)
            
            # --- ANOMALY INJECTION 4: Regional Stockout Alert in Surabaya Hub (wh == 2) ---
            if wh == 2 and part <= 1200 and random.random() < 0.35:
                qoh = random.randint(0, 5) # Stockout below ROP (20)
            else:
                qoh = random.randint(15, 300)

            qres = random.randint(0, 20)
            qtrans = random.randint(0, 50)
            rop = 20
            dos = random.randint(15, 60)
            buf_inv.write("\t".join([str(sdate), str(wh), str(part), str(qoh), str(qres), str(qtrans), str(rop), str(dos)]) + "\n")

        bulk_insert_copy(conn, "dwh.fact_inventory_snapshot", cols_inv, buf_inv)
        print(f"  ... inserted {b + 200000}/2,400,000 fact_inventory_snapshot")

    print("Generating dwh.fact_customer_interactions (1,200,000 rows)...")
    cols_ci = ["interaction_date_key", "customer_key", "junk_key", "channel", "interaction_type", "satisfaction_score"]
    channels = ["App", "Website", "WhatsApp", "Call Center", "Walk-in"]
    itypes = ["Status Check", "Booking", "Complaint", "Inquiry", "Review"]
    
    total_ci = 1200000
    for b in range(0, total_ci, 200000):
        buf_ci = StringIO()
        for _ in range(200000):
            idate = get_random_date_key()
            ckey = random.randint(1, 250000)
            jkey = random.randint(1, 32)
            ch = random.choice(channels)
            itype = random.choice(itypes)
            score = random.randint(5, 10)
            buf_ci.write("\t".join([str(idate), str(ckey), str(jkey), ch, itype, str(score)]) + "\n")

        bulk_insert_copy(conn, "dwh.fact_customer_interactions", cols_ci, buf_ci)
        print(f"  ... inserted {b + 200000}/1,200,000 fact_customer_interactions")

    print("Generating dwh.fact_employee_attendance (350,000 rows)...")
    cols_att = ["work_date_key", "employee_key", "center_key", "junk_key", "overtime_hours", "devices_repaired", "is_present"]
    buf_att = StringIO()
    for i in range(1, 350001):
        wdate = get_random_date_key()
        emp = random.randint(1, 2000)
        center = random.randint(1, 25)
        jkey = random.randint(1, 32)
        ot = random.choice([0, 0, 0, 1.5, 2.0, 3.0])
        devs = random.randint(3, 12)
        buf_att.write("\t".join([str(wdate), str(emp), str(center), str(jkey), str(ot), str(devs), "TRUE"]) + "\n")
        if i % 100000 == 0:
            bulk_insert_copy(conn, "dwh.fact_employee_attendance", cols_att, buf_att)
            buf_att = StringIO()
    if buf_att.getvalue():
        bulk_insert_copy(conn, "dwh.fact_employee_attendance", cols_att, buf_att)

    print("Generating dwh.fact_warranty_claims (200,000 rows)...")
    cols_wc = [
        "claim_id", "claim_date_key", "approval_date_key", "completion_date_key", "customer_key",
        "device_key", "insurance_key", "center_key", "brand_partner_key", "geo_key", "junk_key",
        "claim_type", "damage_type", "turnaround_time_days", "sla_target_days", "repair_cost_idr",
        "sparepart_cost_idr", "total_claim_cost_idr", "status", "sla_status", "csat_rating"
    ]
    ctypes = ["Warranty", "Insurance", "Extended Warranty"]
    dtypes = ["Screen Crack", "Water Damage", "Battery Swell", "Motherboard Failure", "Software Issue"]
    
    for b in range(0, 200000, 50000):
        buf_wc = StringIO()
        for i in range(b + 1, b + 50001):
            cid = f"CLM-{i:06d}"
            cdate, compdate, tat = get_random_date_pair(max_duration_days=10)
            adate = cdate
            ckey = random.randint(1, 250000)
            dkey = random.randint(1, 2500)
            inskey = random.randint(1, 9)
            centerkey = random.randint(1, 25)
            bpkey = random.randint(1, 15)
            gkey = random.randint(1, 30)
            jkey = random.randint(1, 32)
            ctype = random.choice(ctypes)
            dtype = random.choice(dtypes)
            sla_target = 7
            rcost = random.randint(200000, 800000)
            scost = random.randint(300000, 1500000)
            totcost = rcost + scost
            status = "Resolved" if random.random() > 0.08 else "Pending"
            
            # --- ANOMALY INJECTION 5: SLA Breach Bottleneck in ISC Jaksel (centerkey == 3) ---
            if centerkey == 3 and 20240601 <= cdate <= 20240930 and random.random() < 0.38:
                tat = random.randint(14, 22)
                csat = random.randint(1, 2)
            else:
                csat = random.randint(3, 5)

            sla_status = "Met SLA" if tat <= sla_target else "SLA Breached"

            row = [
                cid, str(cdate), str(adate), str(compdate), str(ckey), str(dkey),
                str(inskey), str(centerkey), str(bpkey), str(gkey), str(jkey),
                ctype, dtype, str(tat), str(sla_target), str(rcost), str(scost),
                str(totcost), status, sla_status, str(csat)
            ]
            buf_wc.write("\t".join(row) + "\n")

        bulk_insert_copy(conn, "dwh.fact_warranty_claims", cols_wc, buf_wc)
        print(f"  ... inserted {b + 50000}/200,000 fact_warranty_claims")

    print("Generating dwh.fact_device_protection (80,000 rows)...")
    cols_dp = ["claim_date_key", "policy_key", "customer_key", "device_key", "insurance_key", "geo_key", "junk_key", "claim_amount_idr", "premium_snapshot_idr", "deductible_paid_idr", "claim_status", "loss_ratio", "fraud_score"]
    buf_dp = StringIO()

    # Fraud suspicious customers
    fraud_customers = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]

    for i in range(1, 80001):
        cdate = get_random_date_key()
        polkey = random.randint(1, 100000)
        
        # --- ANOMALY INJECTION 6: High Risk Insurance Fraud Claims ---
        if i <= 300: # First 300 claims targeted for rapid multi-claim fraud testing
            ckey = random.choice(fraud_customers)
            camt = random.randint(25000000, 45000000) # Extremely high claim amount
            status = "Under Investigation"
            fscore = round(random.uniform(0.78, 0.96), 2)
        else:
            ckey = random.randint(1, 250000)
            camt = random.randint(500000, 3000000)
            status = "Approved"
            fscore = round(random.uniform(0.01, 0.25), 2)

        dkey = random.randint(1, 2500)
        inskey = random.randint(1, 9)
        gkey = random.randint(1, 30)
        jkey = random.randint(1, 32)
        prem = 79000 * 12
        ded = 100000
        lratio = round(camt / prem, 2)
        buf_dp.write("\t".join([str(cdate), str(polkey), str(ckey), str(dkey), str(inskey), str(gkey), str(jkey), str(camt), str(prem), str(ded), status, str(lratio), str(fscore)]) + "\n")
        if i % 40000 == 0:
            bulk_insert_copy(conn, "dwh.fact_device_protection", cols_dp, buf_dp)
            buf_dp = StringIO()
    if buf_dp.getvalue():
        bulk_insert_copy(conn, "dwh.fact_device_protection", cols_dp, buf_dp)

    print("Generating dwh.fact_service_pl_monthly (3,600 rows)...")
    cols_pl = ["month_date_key", "center_key", "geo_key", "service_revenue_idr", "parts_revenue_idr", "gross_revenue_idr", "cogs_idr", "gross_profit_idr", "operating_expenses_idr", "net_profit_idr", "net_profit_margin_pct"]
    buf_pl = StringIO()
    for yr in (2022, 2023, 2024, 2025):
        for mo in range(1, 13):
            mkey = int(f"{yr}{mo:02d}01")
            for ckey in range(1, 26):
                gkey = ckey
                srev = random.randint(150000000, 450000000)
                prev = random.randint(200000000, 600000000)
                grev = srev + prev
                cogs = int(grev * random.uniform(0.55, 0.65))
                gprof = grev - cogs
                opex = int(grev * random.uniform(0.15, 0.22))
                nprof = gprof - opex
                npm = round(nprof * 100.0 / grev, 2)
                buf_pl.write("\t".join([str(mkey), str(ckey), str(gkey), str(srev), str(prev), str(grev), str(cogs), str(gprof), str(opex), str(nprof), str(npm)]) + "\n")
    bulk_insert_copy(conn, "dwh.fact_service_pl_monthly", cols_pl, buf_pl)

    print("Generating dwh.fact_support_tickets (180,000 rows)...")
    cols_st = ["ticket_id", "ticket_date_key", "resolution_date_key", "customer_key", "center_key", "junk_key", "ticket_category", "resolution_time_hours", "is_resolved", "is_escalated"]
    st_cats = ["Repair Status", "Billing", "Warranty Inquiry", "Complaint", "Parts Availability"]
    buf_st = StringIO()
    for i in range(1, 180001):
        tdate, rdate, rhrs_days = get_random_date_pair(max_duration_days=3)
        ckey = random.randint(1, 250000)
        centerkey = random.randint(1, 25)
        jkey = random.randint(1, 32)
        cat = random.choice(st_cats)
        rhrs = rhrs_days * 24 + random.randint(1, 12)
        buf_st.write("\t".join([str(i), str(tdate), str(rdate), str(ckey), str(centerkey), str(jkey), cat, str(rhrs), "TRUE", "FALSE"]) + "\n")
        if i % 60000 == 0:
            bulk_insert_copy(conn, "dwh.fact_support_tickets", cols_st, buf_st)
            buf_st = StringIO()
    if buf_st.getvalue():
        bulk_insert_copy(conn, "dwh.fact_support_tickets", cols_st, buf_st)

    print("Generating dwh.fact_spare_part_orders (60,000 rows)...")
    cols_po = ["po_id", "po_date_key", "supplier_key", "warehouse_key", "part_key", "geo_key", "order_quantity", "received_quantity", "unit_cost_idr", "total_po_amount_idr", "estimated_arrival_key", "actual_arrival_key", "is_on_time", "is_in_full", "delay_days"]
    buf_po = StringIO()
    for i in range(1, 60001):
        poid = f"PO-{i:06d}"
        pdate, actarr, delay_days = get_random_date_pair(max_duration_days=10)
        estarr = pdate
        supkey = random.randint(1, 20)
        
        # --- ANOMALY INJECTION 7: Severe Supplier Lead Time Delay (OEM Display Tech - supkey == 4) ---
        if supkey == 4:
            delay_days = random.randint(20, 45) # 20 to 45 Days Delay
            ontime = "FALSE"
            is_in_full = "FALSE"
        else:
            ontime = "TRUE" if actarr <= estarr else "FALSE"
            is_in_full = "TRUE"

        whkey = random.randint(1, 5)
        partkey = random.randint(1, 8000)
        gkey = random.randint(1, 30)
        oqty = random.randint(50, 500)
        rqty = oqty
        ucost = random.randint(100000, 800000)
        totpo = oqty * ucost
        buf_po.write("\t".join([poid, str(pdate), str(supkey), str(whkey), str(partkey), str(gkey), str(oqty), str(rqty), str(ucost), str(totpo), str(estarr), str(actarr), ontime, is_in_full, str(delay_days)]) + "\n")
        if i % 30000 == 0:
            bulk_insert_copy(conn, "dwh.fact_spare_part_orders", cols_po, buf_po)
            buf_po = StringIO()
    if buf_po.getvalue():
        bulk_insert_copy(conn, "dwh.fact_spare_part_orders", cols_po, buf_po)
        if i % 30000 == 0:
            bulk_insert_copy(conn, "dwh.fact_spare_part_orders", cols_po, buf_po)
            buf_po = StringIO()
    if buf_po.getvalue():
        bulk_insert_copy(conn, "dwh.fact_spare_part_orders", cols_po, buf_po)

def main():
    print("=== PT ElectraCare Indonesia EDW Generator ===")
    create_database_if_not_exists()
    
    script_dir = os.path.dirname(__file__)
    ddl_path = os.path.join(script_dir, "schema_ddl.sql")
    execute_sql_file(ddl_path)

    conn = get_db_connection()
    
    print("\n--- Phase 1: Generating Dimensions ---")
    generate_dim_date(conn)
    generate_dim_geography(conn)
    generate_dim_customer(conn)
    generate_dim_device(conn)
    generate_dim_spare_part(conn)
    generate_other_dims(conn)

    print("\n--- Phase 2: Generating Fact Tables (~5.8M rows) ---")
    generate_fact_service_orders_and_parts(conn)
    generate_fact_inventory_and_others(conn)

    conn.close()
    print("\n=======================================================")
    print("SUCCESS: Full Enterprise Data Warehouse (~5.8M rows) generated & loaded!")
    print("=======================================================")

if __name__ == "__main__":
    main()
