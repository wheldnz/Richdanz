# PT ElectraCare Indonesia — Enterprise Data Warehouse (EDW)

Sistem **Enterprise Data Warehouse (EDW)** terpadu untuk perusahaan layanan purna jual (*aftersales*) elektronik (**PT ElectraCare Indonesia**) yang mencakup perbaikan garansi, klaim asuransi perangkat, rantai pasok suku cadang, dan analisis retensi pelanggan.

---

## 🏛️ Architecture Overview

```
                          SOURCES
               (Service, Claims, Parts, HR)
                            │
                            ▼
                    Local Data Lake
                 (data_lake/raw & clean)
                            │
                            ▼
              Modern Data Stack Transformation
                (dbt Core + Python + Prefect)
                            │
                            ▼
                 PostgreSQL Star Schema
                 (dwh: 13 Dims & 10 Facts)
                            │
                            ▼
                   Data Marts & Views
             (mart: Revenue, Ops, Customer 360)
                            │
                            ▼
                 Power BI & DuckDB Analytics
```

---

## 📊 Star Schema Summary

| Type | Table Name | Rows Count | Description |
|---|---|---|---|
| **Conformed Dim** | `dwh.dim_date` | 1,461 | Role-playing date dimension (2022–2025) |
| **Conformed Dim** | `dwh.dim_geography` | 30 | Location master across 7 Indonesian regions |
| **Conformed Dim** | `dwh.dim_customer` | 250,000 | Unified customer records |
| **Subject Dim** | `dwh.dim_device` | 2,500 | Device SKU catalog (Samsung, Apple, Xiaomi, etc.) |
| **Subject Dim** | `dwh.dim_spare_part` | 8,000 | Spare parts catalog (LCD, Battery, IC, etc.) |
| **Subject Dim** | `dwh.dim_service_center` | 25 | Service center network |
| **Subject Dim** | `dwh.dim_brand_partner` | 15 | Principal brand partners |
| **Subject Dim** | `dwh.dim_employee` | 2,000 | Technicians & staff (SCD Type 2) |
| **Subject Dim** | `dwh.dim_supplier` | 20 | Spare part suppliers |
| **Subject Dim** | `dwh.dim_warehouse` | 5 | Spare part regional hubs |
| **Subject Dim** | `dwh.dim_insurance_partner` | 9 | Device protection insurance partners |
| **Subject Dim** | `dwh.dim_policy` | 100,000 | Active device protection policies |
| **Subject Dim** | `dwh.dim_junk_flags` | 128 | Junk dimension flags |
| **Fact** | `dwh.fact_service_orders` | 500,000 | Service order header transactions |
| **Fact** | `dwh.fact_parts_usage` | 750,000 | Spare parts usage line items |
| **Fact** | `dwh.fact_service_pl_monthly` | 3,600 | Monthly P&L per service center |
| **Fact** | `dwh.fact_customer_interactions` | 1,200,000 | Customer engagement logs |
| **Fact** | `dwh.fact_support_tickets` | 180,000 | Support ticket resolution logs |
| **Fact** | `dwh.fact_spare_part_orders` | 60,000 | Supplier purchase orders |
| **Fact** | `dwh.fact_inventory_snapshot` | 2,400,000 | Daily warehouse stock snapshots |
| **Fact** | `dwh.fact_employee_attendance` | 350,000 | Technician daily attendance & output |
| **Fact** | `dwh.fact_warranty_claims` | 200,000 | Warranty & SLA claim logs |
| **Fact** | `dwh.fact_device_protection` | 80,000 | Insurance protection claims |

---

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install psycopg2-binary pandas faker duckdb dbt-postgres prefect
   ```

2. **Generate All Data & Load to PostgreSQL**:
   ```bash
   python scripts/generate_all_data.py
   ```

3. **Run dbt Models & Tests**:
   ```bash
   cd dbt_project
   dbt run --profiles-dir .
   dbt test --profiles-dir .
   ```

4. **Run Prefect Orchestration Flow**:
   ```bash
   python flows/daily_pipeline.py
   ```
