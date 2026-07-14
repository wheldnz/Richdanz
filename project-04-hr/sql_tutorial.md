# Tutorial SQL Complete (Pure PostgreSQL ELT) - Project 04: HR Analytics

Tutorial ini memandu Anda melakukan **ELT & Analisis Attrition Karyawan** murni menggunakan kueri SQL di PostgreSQL.

---

## 1. Staging Table: Impor Data IBM HR Attrition

```sql
DROP TABLE IF EXISTS staging_hr_attrition CASCADE;

CREATE TABLE staging_hr_attrition (
    Age TEXT,
    Attrition TEXT,
    BusinessTravel TEXT,
    DailyRate TEXT,
    Department TEXT,
    DistanceFromHome TEXT,
    Education TEXT,
    EducationField TEXT,
    EmployeeCount TEXT,
    EmployeeNumber TEXT,
    EnvironmentSatisfaction TEXT,
    Gender TEXT,
    HourlyRate TEXT,
    JobInvolvement TEXT,
    JobLevel TEXT,
    JobRole TEXT,
    JobSatisfaction TEXT,
    MaritalStatus TEXT,
    MonthlyIncome TEXT,
    MonthlyRate TEXT,
    NumCompaniesWorked TEXT,
    Over18 TEXT,
    OverTime TEXT,
    PercentSalaryHike TEXT,
    PerformanceRating TEXT,
    RelationshipSatisfaction TEXT,
    StandardHours TEXT,
    StockOptionLevel TEXT,
    TotalWorkingYears TEXT,
    TrainingTimesLastYear TEXT,
    WorkLifeBalance TEXT,
    YearsAtCompany TEXT,
    YearsInCurrentRole TEXT,
    YearsSinceLastPromotion TEXT,
    YearsWithCurrManager TEXT
);
```

---

## 2. Pembersihan & Kalkulasi Indikator HR (Murni SQL)

### A. Membuat Tabel Dimensi Karyawan (`dim_employee`)
SQL ini menghitung `hire_date` & `resign_date` berdasarkan `YearsAtCompany`, serta membandingkan gaji karyawan terhadap rata-rata pasar (*Market Pay Ratio*):

```sql
DROP TABLE IF EXISTS dim_employee CASCADE;

CREATE TABLE dim_employee AS
SELECT 
    EmployeeNumber AS employee_id,
    Age::INT AS age,
    Gender AS gender,
    COALESCE(NULLIF(Department, ''), 'Unassigned') AS department,
    JobRole AS job_role,
    JobLevel::INT AS job_level,
    ABS(MonthlyIncome::NUMERIC) AS monthly_income,
    -- Hitung Market Pay Ratio vs Standard Benchmark (Level 1=4500, Level 2=7500, dst)
    ROUND(
        ABS(MonthlyIncome::NUMERIC) / 
        CASE JobLevel 
            WHEN '1' THEN 4500 WHEN '2' THEN 7500 WHEN '3' THEN 11500 WHEN '4' THEN 16000 ELSE 22000 
        END, 
        2
    ) AS market_pay_ratio,
    OverTime AS overtime_flag,
    YearsAtCompany::INT AS years_at_company,
    YearsSinceLastPromotion::INT AS years_since_last_promotion,
    -- Hitung Hire Date & Resign Date
    (DATE '2025-06-30' - (YearsAtCompany::INT || ' years')::INTERVAL)::DATE AS hire_date,
    CASE 
        WHEN Attrition = 'Yes' THEN (DATE '2025-06-30' - (RANDOM() * 90)::INT * INTERVAL '1 day')::DATE
        ELSE NULL 
    END AS resign_date,
    CASE WHEN Attrition = 'Yes' THEN 'Resigned' ELSE 'Active' END AS status,
    Attrition AS attrition_flag
FROM staging_hr_attrition;

ALTER TABLE dim_employee ADD PRIMARY KEY (employee_id);
```

### B. Generasi Log Presensi Lembur Bulanan (`fact_attendance`)
Menggunakan `GENERATE_SERIES()` di SQL untuk memproduksi log lembur 12 bulan terakhir:

```sql
DROP TABLE IF EXISTS fact_attendance CASCADE;

CREATE TABLE fact_attendance AS
SELECT 
    ROW_NUMBER() OVER() AS attendance_id,
    e.employee_id,
    (DATE '2025-06-30' - (m.month_idx || ' months')::INTERVAL)::DATE AS work_date,
    CASE 
        WHEN e.overtime_flag = 'Yes' THEN ROUND((RANDOM() * 2.5 + 2.0)::NUMERIC, 1)
        ELSE ROUND((RANDOM() * 1.0)::NUMERIC, 1)
    END AS overtime_hours
FROM dim_employee e
CROSS JOIN LATERAL GENERATE_SERIES(0, 11) AS m(month_idx);

ALTER TABLE fact_attendance ADD PRIMARY KEY (attendance_id);
```

---

## 3. Kueri Analisis HR SQL

### Query 1: Analisis Attrition Rate & Rata-Rata Lembur per Departemen

```sql
SELECT 
    e.department,
    COUNT(e.employee_id) AS total_employees,
    COUNT(CASE WHEN e.attrition_flag = 'Yes' THEN 1 END) AS resigned_employees,
    ROUND(COUNT(CASE WHEN e.attrition_flag = 'Yes' THEN 1 END) * 100.0 / COUNT(e.employee_id), 2) AS attrition_rate_pct,
    ROUND(AVG(e.market_pay_ratio), 2) AS avg_market_pay_ratio,
    ROUND(AVG(a.overtime_hours), 2) AS avg_monthly_overtime_hours
FROM dim_employee e
LEFT JOIN fact_attendance a ON e.employee_id = a.employee_id
GROUP BY e.department
ORDER BY attrition_rate_pct DESC;
```

### Query 2: Identifikasi Karyawan Risiko Attrition Tinggi (Lembur Tinggi + Pay Ratio Rendah)

```sql
SELECT 
    employee_id,
    department,
    job_role,
    monthly_income,
    market_pay_ratio,
    overtime_flag,
    years_since_last_promotion
FROM dim_employee
WHERE status = 'Active' 
  AND overtime_flag = 'Yes' 
  AND market_pay_ratio < 1.0 
  AND years_since_last_promotion >= 3
ORDER BY market_pay_ratio ASC;
```
