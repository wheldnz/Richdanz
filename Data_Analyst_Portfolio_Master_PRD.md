# Data Analyst Portfolio Master PRD

## Objective

Bangun **6 proyek portofolio Data Analyst** yang menyerupai implementasi
di perusahaan nyata. Setiap proyek WAJIB menghasilkan: - Dataset dummy
realistis (CSV) - Database SQL - Query SQL lengkap - Power BI (.pbix) -
Dokumentasi - README

## Tech Stack

-   SQL (PostgreSQL/MySQL compatible)
-   Power BI
-   Excel
-   Git/GitHub

------------------------------------------------------------------------

# Global Rules

## Dataset

Untuk setiap proyek AI harus membuat dataset dummy realistis dengan
ukuran:

-   Fact table: 1.000.000+ baris
-   Dimension table: 5.000--100.000 baris
-   Periode: 2022--2025
-   Data harus konsisten antar tabel (foreign key valid)
-   Tidak boleh random murni; distribusi mengikuti kondisi bisnis.

Output:

    /data/raw
    /data/processed
    /schema.sql
    /seed.sql

## SQL

WAJIB mencakup: - CREATE DATABASE - CREATE TABLE - INSERT - VIEW -
INDEX - CTE - Window Function - LAG/LEAD - CASE WHEN - Aggregate -
Stored Procedure (jika DB mendukung)

## Power BI

WAJIB mencakup: - Power Query cleaning - Star Schema - Date Table -
Relationship - DAX: - Revenue - Profit - Margin - MoM - YoY - Running
Total - Top N - Dynamic Ranking - Minimal 5 halaman dashboard: 1.
Executive Summary 2. Sales/Operations 3. Customer 4. Product/Category 5.
Geography

## README setiap proyek

-   Business Problem
-   Dataset
-   Data Model
-   SQL Process
-   Dashboard
-   Insights (\>=10)
-   Recommendations (\>=10)
-   Folder structure

------------------------------------------------------------------------

# Project 1 --- Enterprise Sales Analytics

Business Problem: Analisis revenue, profit, margin, customer, produk,
cabang.

Dummy data: - orders (1.2M) - order_items (3M) - customers (150k) -
products (50k) - stores (500) - salespersons (2k) - calendar

KPI: Revenue, Profit, Margin, AOV, Basket Size, Pareto, MoM, YoY,
Top/Bottom Product.

------------------------------------------------------------------------

# Project 2 --- Customer Churn Analytics

Dummy: - customers - subscriptions - invoices - support_ticket -
usage_log

Target: 1 juta pelanggan.

KPI: Churn, Retention, CLV, Tenure, Cohort, NPS proxy.

------------------------------------------------------------------------

# Project 3 --- Supply Chain Analytics

Dummy: - warehouse - supplier - inventory - purchase_order - shipment -
delivery

KPI: Inventory Turnover, Fill Rate, OTIF, Stockout, Lead Time.

------------------------------------------------------------------------

# Project 4 --- HR Analytics

Dummy: - employee - attendance - payroll - performance - promotion -
resignation

KPI: Attrition, Headcount, Overtime, Promotion, Salary.

------------------------------------------------------------------------

# Project 5 --- Repair Service Analytics

Dummy: - customer - device - ticket - technician - sparepart -
repair_history - warranty

KPI: SLA, Repair Time, First Fix Rate, Repeat Repair.

------------------------------------------------------------------------

# Project 6 --- Insurance Analytics

Dummy: - policy - customer - premium - claim - payment - branch

KPI: Claim Ratio, Approval Rate, Pending, Premium Growth.

------------------------------------------------------------------------

# Folder Structure

    portfolio/
      project-01-sales/
      project-02-churn/
      project-03-supply-chain/
      project-04-hr/
      project-05-repair/
      project-06-insurance/

# Deliverables

Untuk SETIAP proyek AI harus menghasilkan: 1. Dummy dataset CSV 2. SQL
schema 3. SQL seed 4. SQL analysis 5. Power BI data model 6. DAX 7.
Dashboard mockup specification 8. README 9. Business insights 10.
Executive recommendations

Jangan menggunakan dataset publik secara langsung. Bangun dataset dummy
realistis yang menyerupai perusahaan enterprise.
