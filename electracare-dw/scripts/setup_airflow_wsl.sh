#!/bin/bash
# Script Setup Apache Airflow 2.x di WSL2 Ubuntu
# PT ElectraCare Indonesia — EDW Project

set -e

echo "=== 1. Updating Ubuntu Packages & Installing Prerequisites ==="
sudo apt-get update && sudo apt-get install -y python3-pip python3-venv libpq-dev build-essential

echo "=== 2. Creating Virtual Environment for Airflow ==="
mkdir -p ~/airflow_env
cd ~/airflow_env
python3 -m venv venv
source venv/bin/activate

echo "=== 3. Installing Apache Airflow & GCP/dbt Providers ==="
pip install --upgrade pip
pip install "apache-airflow==2.10.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.10.txt"
pip install apache-airflow-providers-google dbt-bigquery google-cloud-bigquery pandas pyarrow

echo "=== 4. Setting Up Airflow Folders & DAGs ==="
mkdir -p ~/airflow/dags ~/airflow/keys
cp /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/keys/gcp_key.json ~/airflow/keys/gcp_key.json 2>/dev/null || true
cp /mnt/c/Users/USER/Documents/present/potrfolio/electracare-dw/dags/electracare_daily_dag.py ~/airflow/dags/ 2>/dev/null || true

export AIRFLOW_HOME=~/airflow

echo "=== 5. Initializing Airflow Standalone Database ==="
airflow db init

echo "=== 6. Creating Airflow Admin User ==="
airflow users create \
    --username admin \
    --firstname Electra \
    --lastname Care \
    --role Admin \
    --email admin@electracare.id \
    --password admin123 || true

echo "======================================================="
echo "SUCCESS: Apache Airflow is installed & configured in WSL!"
echo "To start Airflow UI (http://localhost:8080):"
echo "  source ~/airflow_env/venv/bin/activate"
echo "  airflow standalone"
echo "======================================================="
