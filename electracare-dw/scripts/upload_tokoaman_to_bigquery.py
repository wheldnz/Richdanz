"""
Script Pengunggah Dataset TokoAman.id BI ke Google BigQuery
Project ID: electracare-dw
Dataset Target: tokoaman_bi
"""

import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Set UTF-8 stdout if needed
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(BASE_DIR, "keys", "gcp_key.json")
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "bi_project_claude", "data")

PROJECT_ID = "electracare-dw"
DATASET_ID = "tokoaman_bi"

def get_bq_client():
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(f"GCP Key file not found at: {KEY_PATH}")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)

def create_dataset_if_not_exists(client):
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    try:
        client.create_dataset(dataset, exists_ok=True)
        print(f"[OK] BigQuery Dataset '{dataset_ref}' ready.")
    except Exception as e:
        print(f"Error creating dataset '{dataset_ref}': {e}")

def upload_csv_files_to_bigquery():
    print("=== Uploading TokoAman.id BI Datasets -> Google BigQuery ===")
    client = get_bq_client()
    create_dataset_if_not_exists(client)

    csv_files = [
        ("customers.csv", "customers"),
        ("products.csv", "products"),
        ("campaigns.csv", "campaigns"),
        ("orders.csv", "orders"),
        ("order_items.csv", "order_items"),
        ("insurance_policies.csv", "insurance_policies"),
        ("claims.csv", "claims"),
        ("ab_test_sessions.csv", "ab_test_sessions"),
        ("rfm_segments.csv", "rfm_segments"),
        ("churn_customers.csv", "churn_customers"),
        ("campaign_roi.csv", "campaign_roi"),
        ("channel_roi_summary.csv", "channel_roi_summary"),
        ("monthly_revenue_actual_vs_forecast.csv", "monthly_revenue_actual_vs_forecast")
    ]

    for csv_name, table_name in csv_files:
        csv_path = os.path.join(DATA_DIR, csv_name)
        if not os.path.exists(csv_path):
            print(f"[WARNING] File {csv_name} not found at {csv_path}. Skipping...")
            continue

        print(f"\nReading {csv_name}...")
        df = pd.read_csv(csv_path)

        # Parse date columns if present
        date_cols = [c for c in df.columns if 'date' in c.lower()]
        for col in date_cols:
            try:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            except Exception:
                pass

        destination_table = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            autodetect=True
        )

        print(f"  --> Uploading {len(df):,} rows to BigQuery ({destination_table})...")
        job = client.load_table_from_dataframe(df, destination_table, job_config=job_config)
        job.result() # Wait for job completion
        print(f"[SUCCESS] Table '{table_name}' loaded to BigQuery successfully!")

    print("\n=======================================================")
    print("SUCCESS: All TokoAman.id BI Datasets loaded to BigQuery!")
    print("=======================================================")

if __name__ == "__main__":
    upload_csv_files_to_bigquery()
