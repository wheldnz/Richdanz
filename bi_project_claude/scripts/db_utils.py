"""
db_utils.py
===========
Helper supaya semua script analisis bisa jalan dengan dua mode:
1. Kalau environment variable DATABASE_URL di-set dan PostgreSQL bisa
   diakses -> baca langsung dari database (sesuai tech stack aslinya).
2. Kalau tidak -> otomatis fallback baca dari file CSV di folder ../data
   (supaya tetap bisa latihan tanpa perlu install PostgreSQL dulu).

Contoh DATABASE_URL:
    postgresql+psycopg2://postgres:password@localhost:5432/tokoaman
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return None
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        with engine.connect():
            pass
        return engine
    except Exception as e:
        print(f"[info] Tidak bisa konek ke PostgreSQL ({e}). Fallback ke CSV lokal di /data.")
        return None


def load_table(name, parse_dates=None):
    engine = get_engine()
    if engine is not None:
        query = f"SELECT * FROM {name}"
        return pd.read_sql_query(query, engine, parse_dates=parse_dates)
    path = os.path.join(DATA_DIR, f"{name}.csv")
    return pd.read_csv(path, parse_dates=parse_dates)
