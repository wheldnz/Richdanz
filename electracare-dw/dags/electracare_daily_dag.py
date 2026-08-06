"""
Apache Airflow Daily Pipeline DAG for PT ElectraCare Indonesia EDW (Google BigQuery)
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'electracare_daily_pipeline',
    default_args=default_args,
    description='Daily Ingestion & Transformation pipeline to Google BigQuery',
    schedule_interval='0 6 * * *',  # Every day at 06:00 WIB
    catchup=False,
) as dag:

    # Task 1: Load/Sync Data to Google BigQuery
    sync_to_bigquery = BashOperator(
        task_id='sync_to_bigquery',
        bash_command='python3 /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/scripts/generate_bigquery_data.py',
    )

    # Task 2: Run dbt Staging Models on BigQuery
    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command='dbt run --select staging --project-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project --profiles-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project',
    )

    # Task 3: Run dbt Mart Models on BigQuery
    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command='dbt run --select marts --project-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project --profiles-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project',
    )

    # Task 4: Run dbt Data Quality Tests
    dbt_test = BashOperator(
        task_id='dbt_test_quality',
        bash_command='dbt test --project-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project --profiles-dir /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dbt_project',
    )

    sync_to_bigquery >> dbt_run_staging >> dbt_run_marts >> dbt_test
