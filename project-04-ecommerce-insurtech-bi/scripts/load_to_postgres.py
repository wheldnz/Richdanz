"""
load_to_postgres.py
====================
Load semua file CSV di /data ke database PostgreSQL yang sudah dibuat
skemanya lewat sql/schema.sql.

Sebelum jalanin:
    1. Buat database, contoh: createdb tokoaman
    2. Jalankan schema:      psql -d tokoaman -f ../sql/schema.sql
    3. Set connection string di bawah (atau lewat env var DATABASE_URL)
    4. pip install sqlalchemy psycopg2-binary
    5. python load_to_postgres.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost:5432/tokoaman"
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Urutan penting! Harus sesuai urutan foreign key (parent dulu baru child)
TABLES_IN_ORDER = [
    "customers",
    "products",
    "campaigns",
    "orders",
    "order_items",
    "insurance_policies",
    "claims",
]

DATE_COLUMNS = {
    "customers": ["signup_date"],
    "campaigns": ["start_date", "end_date"],
    "orders": ["order_date"],
    "insurance_policies": ["start_date", "end_date"],
    "claims": ["claim_date"],
}


def main():
    engine = create_engine(DATABASE_URL)

    for table in TABLES_IN_ORDER:
        csv_path = os.path.join(DATA_DIR, f"{table}.csv")
        df = pd.read_csv(csv_path, parse_dates=DATE_COLUMNS.get(table))
        df.to_sql(table, engine, if_exists="append", index=False, method="multi", chunksize=1000)
        print(f"  loaded {len(df):>6,} baris -> {table}")

    print("\nSelesai! Semua tabel sudah terisi di PostgreSQL.")


if __name__ == "__main__":
    main()
