"""
push_analytics_to_postgres.py
==============================
Setelah rfm_segmentation.py, churn_analysis.py, forecasting.py, dan
marketing_roi.py dijalankan, hasilnya (CSV) di-push balik ke
PostgreSQL sebagai tabel "analytics layer".

Tujuannya: Power BI cukup connect ke SATU sumber (PostgreSQL) untuk
data mentah MAUPUN hasil analisis Python -- ini pola arsitektur BI
yang lebih rapi untuk ditunjukkan ke recruiter (single source of truth).

Jalankan setelah keempat script analisis di atas selesai:
    python push_analytics_to_postgres.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost:5432/tokoaman"
)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

ANALYTICS_TABLES = [
    "rfm_segments",
    "churn_customers",
    "churn_by_policy_type",
    "campaign_roi",
    "channel_roi_summary",
    "monthly_revenue_actual_vs_forecast",
    "ab_test_sessions",
]


def main():
    engine = create_engine(DATABASE_URL)
    for name in ANALYTICS_TABLES:
        path = os.path.join(DATA_DIR, f"{name}.csv")
        df = pd.read_csv(path)
        df.to_sql(name, engine, if_exists="replace", index=False)
        print(f"  pushed {len(df):>6,} baris -> {name}")
    print("\nSelesai! Power BI sekarang bisa connect ke PostgreSQL saja untuk semua data.")


if __name__ == "__main__":
    main()
