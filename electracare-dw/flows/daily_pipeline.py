"""
Prefect Orchestration Flow for PT ElectraCare Indonesia EDW
Replaces Airflow with a lightweight, native Windows Python flow.
"""

from prefect import flow, task
import subprocess
import sys
import os

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
DBT_DIR = os.path.join(os.path.dirname(__file__), "..", "dbt_project")

@task(name="Generate EDW Data & Load Postgres", retries=1)
def generate_data_task():
    script_path = os.path.join(SCRIPTS_DIR, "generate_all_data.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Data generation failed:\n{result.stderr}")
    print(result.stdout)
    return "Data generated and loaded successfully!"

@task(name="Run dbt Staging Models")
def run_dbt_staging():
    result = subprocess.run(["dbt", "run", "--select", "staging", "--project-dir", DBT_DIR, "--profiles-dir", DBT_DIR], capture_output=True, text=True)
    print(result.stdout)

@task(name="Run dbt Mart Models")
def run_dbt_marts():
    result = subprocess.run(["dbt", "run", "--select", "marts", "--project-dir", DBT_DIR, "--profiles-dir", DBT_DIR], capture_output=True, text=True)
    print(result.stdout)

@task(name="Run dbt Data Quality Tests")
def run_dbt_tests():
    result = subprocess.run(["dbt", "test", "--project-dir", DBT_DIR, "--profiles-dir", DBT_DIR], capture_output=True, text=True)
    print(result.stdout)

@flow(name="ElectraCare EDW Daily Pipeline")
def electracare_daily_pipeline():
    print("Starting ElectraCare EDW Daily Pipeline...")
    gen_status = generate_data_task()
    run_dbt_staging()
    run_dbt_marts()
    run_dbt_tests()
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    electracare_daily_pipeline()
