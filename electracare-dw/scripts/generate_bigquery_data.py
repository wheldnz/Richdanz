"""
BigQuery Data Loader & Dataset Creator for PT ElectraCare Indonesia EDW
Project ID: electracare-dw
"""

import os
import sys
import psycopg2
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Path Config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(BASE_DIR, "keys", "gcp_key.json")

# BigQuery Config
PROJECT_ID = "electracare-dw"
DATASET_DWH = "electracare_dwh"
DATASET_MART = "electracare_mart"

# Postgres Config
PG_NAME = "db_electracare_dw"
PG_USER = "postgres"
PG_PASS = "admin123"
PG_HOST = "127.0.0.1"

def get_bq_client():
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(f"GCP Key file not found at: {KEY_PATH}")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return client

def create_datasets_if_not_exist(client):
    datasets = [DATASET_DWH, DATASET_MART]
    for ds_name in datasets:
        dataset_id = f"{PROJECT_ID}.{ds_name}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        try:
            client.create_dataset(dataset, exists_ok=True)
            print(f"BigQuery Dataset '{dataset_id}' ready.")
        except Exception as e:
            print(f"Error creating dataset '{dataset_id}': {e}")

def get_pg_connection():
    return psycopg2.connect(dbname=PG_NAME, user=PG_USER, password=PG_PASS, host=PG_HOST, port=5432)

def sync_tables_to_bigquery():
    print("=== Syncing PostgreSQL Data Warehouse -> Google BigQuery ===")
    client = get_bq_client()
    create_datasets_if_not_exist(client)

    conn = get_pg_connection()

    tables = [
        ("dim_date", "dwh"),
        ("dim_geography", "dwh"),
        ("dim_customer", "dwh"),
        ("dim_device", "dwh"),
        ("dim_spare_part", "dwh"),
        ("dim_service_center", "dwh"),
        ("dim_brand_partner", "dwh"),
        ("dim_employee", "dwh"),
        ("dim_supplier", "dwh"),
        ("dim_warehouse", "dwh"),
        ("dim_insurance_partner", "dwh"),
        ("dim_policy", "dwh"),
        ("dim_junk_flags", "dwh"),
        ("fact_service_orders", "dwh"),
        ("fact_parts_usage", "dwh"),
        ("fact_service_pl_monthly", "dwh"),
        ("fact_customer_interactions", "dwh"),
        ("fact_support_tickets", "dwh"),
        ("fact_spare_part_orders", "dwh"),
        ("fact_inventory_snapshot", "dwh"),
        ("fact_employee_attendance", "dwh"),
        ("fact_warranty_claims", "dwh"),
        ("fact_device_protection", "dwh")
    ]

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )

    for table_name, schema in tables:
        print(f"\nFetching dwh.{table_name} from PostgreSQL...")
        query = f"SELECT * FROM {schema}.{table_name}"
        
        # Read in chunks for large fact tables
        chunk_size = 250000
        first_chunk = True
        
        for df_chunk in pd.read_sql_query(query, conn, chunksize=chunk_size):
            destination_table = f"{PROJECT_ID}.{DATASET_DWH}.{table_name}"
            
            chunk_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE" if first_chunk else "WRITE_APPEND",
                autodetect=True
            )
            
            print(f"  --> Uploading chunk of {len(df_chunk):,} rows to BigQuery ({destination_table})...")
            job = client.load_table_from_dataframe(df_chunk, destination_table, job_config=chunk_config)
            job.result() # Wait for job completion
            first_chunk = False

        print(f"Table '{table_name}' successfully loaded to BigQuery!")

    conn.close()
    print("\n=======================================================")
    print("SUCCESS: Enterprise Data Warehouse synced to Google BigQuery!")
    print("=======================================================")

if __name__ == "__main__":
    sync_tables_to_bigquery()
