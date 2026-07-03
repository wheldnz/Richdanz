# ETL & SQL Analytics Tutorial - HR Analytics

Tutorial ini menjelaskan proses membersihkan anomali data karir karyawan, mengimpor ke PostgreSQL, dan menyusun kueri analisis jam lembur harian.

---

## 1. ETL & Penanganan Anomali (Python)

Anomali pada dataset ini:
- **`employee.csv`**: Kolom `salary` bernilai negatif, kolom `department` kosong (`NaN`), tanggal resign lebih dahulu dibanding hire, dan baris duplikat.
- **`attendance.csv`**: Kolom `overtime_hours` bernilai negatif.

Buat file `etl_process.py` dan jalankan kode berikut:

```python
import pandas as pd
import numpy as np

# Load
df_emp = pd.read_csv('data/raw/employee.csv')
df_att = pd.read_csv('data/raw/attendance.csv')

print("--- Memulai Proses ETL ---")

# 1. Bersihkan Employee
# Masalah A: Salary bernilai negatif
df_emp['salary'] = df_emp['salary'].abs()

# Masalah B: Department bernilai kosong (NaN)
# Solusi B: Isi dengan kategori default 'Unassigned'
df_emp['department'] = df_emp['department'].fillna('Unassigned')

# Masalah C: Duplikat Karyawan
df_emp = df_emp.drop_duplicates(subset=['employee_id'])

# Masalah D: Tanggal resign < hire date
df_emp['hire_date'] = pd.to_datetime(df_emp['hire_date'])
df_emp['resign_date'] = pd.to_datetime(df_emp['resign_date'])

bad_dates = df_emp[df_emp['resign_date'] < df_emp['hire_date']]
print(f"Menangani {len(bad_dates)} baris tanggal resign mendahului hire_date.")
# Koreksi: Set resign_date menjadi hire_date + 6 bulan
for idx in bad_dates.index:
    df_emp.loc[idx, 'resign_date'] = df_emp.loc[idx, 'hire_date'] + pd.to_timedelta(180, unit='D')

# 2. Bersihkan Attendance
# Masalah: Overtime hours negatif
bad_ot = df_att[df_att['overtime_hours'] < 0]
print(f"Menangani {len(bad_ot)} baris overtime negatif di Attendance.")
df_att['overtime_hours'] = df_att['overtime_hours'].abs()

# Pastikan integritas referensial
valid_emp_ids = df_emp['employee_id'].unique()
df_att = df_att[df_att['employee_id'].isin(valid_emp_ids)]

# Save
df_emp.to_csv('data/processed/employee.csv', index=False)
df_att.to_csv('data/processed/attendance.csv', index=False)

print("--- ETL Sukses! Data bersih disimpan di data/processed/ ---")
```

---

## 2. Load & SQL Analytics (PostgreSQL)

### A. Load Data
Buat tabel dengan `schema.sql`. Impor data dari `data/processed/` ke PostgreSQL:
1. `employee.csv` $\rightarrow$ tabel `employee`
2. `attendance.csv` $\rightarrow$ tabel `attendance`

### B. SQL Overtime Analysis
Gunakan query ini untuk menghitung rata-rata lembur harian per departemen dan hubungannya dengan status kepegawaian (Active vs Resigned):

```sql
SELECT 
    e.department,
    e.status,
    COUNT(DISTINCT e.employee_id) AS total_employees,
    ROUND(AVG(a.overtime_hours), 2) AS avg_overtime_hours
FROM employee e
LEFT JOIN attendance a ON e.employee_id = a.employee_id
GROUP BY e.department, e.status
ORDER BY avg_overtime_hours DESC;
```

---

## 3. Visualisasi (Power BI)

1. Impor data dari PostgreSQL ke Power BI.
2. Buat relasi $1:\infty$ dari `employee[employee_id]` ke `attendance[employee_id]`.
3. Buat tabel tanggal otomatis (Calendar) dan hubungkan ke `employee[hire_date]`.
4. DAX Measure untuk **Active Headcount harian**:
   ```dax
   Active Headcount = 
   CALCULATE(
       COUNT(employee[employee_id]),
       FILTER(
           employee,
           employee[hire_date] <= MAX('Calendar'[Date]) &&
           (ISBLANK(employee[resign_date]) || employee[resign_date] > MAX('Calendar'[Date]))
       )
   )
   ```
5. Buat dashboard visual bertema korporasi navy blue dengan slider what-if parameter dinamis untuk menyimulasikan dampak penyesuaian gaji minimum terhadap pengurangan rasio attrition.
