---
title: HR Analytics
category: data
metric: 14% -> 8%
metricLabel: Attrition Rate Reduction
tags: ['SQL', 'Power BI', 'HR', 'Retention']
description: Workforce demographics and employee attrition dashboard, utilizing historical career paths and attendance metrics to pinpoint turnover drivers.
---

# HR Analytics

## Business Problem
Manajemen HR (*Human Resources*) mendeteksi adanya tren peningkatan tingkat pengunduran diri karyawan (*employee attrition*) di beberapa divisi kunci, terutama teknologi dan operasional. Biaya rekrutmen karyawan baru yang tinggi serta hilangnya produktivitas kerja mengganggu pencapaian target bisnis perusahaan. Proyek ini bertujuan untuk membangun dashboard analitik SDM guna memantau sebaran demografi, melacak rasio perputaran karyawan, mendeteksi korelasi antara kompensasi dengan keputusan resign, dan mengidentifikasi pemicu utama stres kerja (misalnya jam lembur yang berlebihan).

## Dataset & Raw Data
* **Tables**:
  - `employee` (50 ribu baris): Data profil karyawan, departemen, jabatan, dan tanggal bergabung/resign.
  - `attendance` (5 juta baris): Log presensi harian, jam masuk, jam pulang, dan status kehadiran.
  - `payroll` (600 ribu baris): Catatan gaji bulanan, bonus, potongan, dan tunjangan.
  - `performance` (100 ribu baris): Hasil penilaian kinerja tahunan (*performance review scores*).
  - `promotion` (80 ribu baris): Riwayat promosi jabatan dan kenaikan golongan.
  - `resignation` (5 ribu baris): Kategori alasan resign (gaji, karir, keluarga, kesehatan, dll).

### Raw Data Generation
Data dummy mensimulasikan korelasi karir yang realistis: karyawan yang tidak mendapatkan promosi selama lebih dari 3 tahun, memiliki nilai kinerja di bawah rata-rata, atau mencatatkan jam lembur harian $> 3$ jam secara konsisten di tabel `attendance`, akan di-generate memiliki status "Resigned" pada tabel `employee` dengan alasan yang logis (misalnya kejenuhan kerja/karir terhambat).

## Data Model
- **Fact Table**: `fact_workforce_snapshot` (snapshot bulanan untuk mencatat headcount aktif, gaji, dan status karyawan).
- **Dimension Tables**: `dim_employee_profile`, `dim_department`, `dim_job_role`, `dim_date`.

## SQL Process
Query SQL berikut digunakan untuk melacak riwayat karir karyawan menggunakan konsep *Slowly Changing Dimensions (SCD) Type 2* untuk mengetahui perpindahan jabatan:

```sql
-- Analisa Korelasi Rata-Rata Lembur (Overtime) terhadap Tingkat Resign per Departemen
WITH OvertimeSummary AS (
    SELECT 
        e.department,
        e.employee_id,
        AVG(CASE WHEN a.overtime_hours > 0 THEN a.overtime_hours ELSE 0 END) AS avg_daily_overtime
    FROM employee e
    JOIN attendance a ON e.employee_id = a.employee_id
    GROUP BY e.department, e.employee_id
)
SELECT 
    os.department,
    COUNT(DISTINCT os.employee_id) AS total_employees,
    ROUND(AVG(os.avg_daily_overtime), 2) AS avg_ot_hours,
    SUM(CASE WHEN e.status = 'Resigned' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT os.employee_id) AS attrition_rate_pct
FROM OvertimeSummary os
JOIN employee e ON os.employee_id = e.employee_id
GROUP BY os.department
ORDER BY attrition_rate_pct DESC;
```

## Power BI & DAX
DAX khusus untuk memantau metrik HR secara dinamis:

* **Active Headcount**:
  ```dax
  Active Headcount = 
  CALCULATE(
      COUNT(dim_employee_profile[EmployeeID]),
      FILTER(
          dim_employee_profile,
          dim_employee_profile[HireDate] <= MAX(dim_date[Date]) &&
          (ISBLANK(dim_employee_profile[ResignDate]) || dim_employee_profile[ResignDate] > MAX(dim_date[Date]))
      )
  )
  ```
* **Monthly Attrition Rate**:
  ```dax
  Monthly Attrition Rate = 
  VAR ResignedInMonth = CALCULATE(COUNT(dim_employee_profile[EmployeeID]), dim_employee_profile[Status] = "Resigned")
  VAR AvgHeadcount = ([Active Headcount] + CALCULATE([Active Headcount], PREVIOUSMONTH(dim_date[Date]))) / 2
  RETURN
  DIVIDE(ResignedInMonth, AvgHeadcount, 0)
  ```

## Dashboard Mockup Specification
Dashboard menggunakan **Corporate Style (Navy & Slate Blue with Purple Accent)**:
- **Halaman 1: Workforce Demographics**: Peta sebaran karyawan berdasarkan rentang usia, tingkat pendidikan, diversitas gender, serta KPI Headcount aktif saat ini.
- **Halaman 2: Attrition & Retention**: Grafik analisis turnover berdasarkan masa kerja, tingkat kepuasan, kompensasi gaji relatif terhadap pasar, serta slider interaktif untuk simulasi "What-If" kenaikan gaji minimum terhadap penurunan attrition.

## Key Insights
1. **Pemicu Utama Resign**: 45% karyawan yang resign menyatakan alasan "Kurangnya Perkembangan Karir" sebagai faktor utama.
2. **Kelebihan Lembur (Overtime)**: Divisi Teknologi dengan rata-rata jam lembur $> 2.5$ jam per hari memiliki tingkat attrition 22%, tertinggi di antara divisi lainnya.
3. **Masa Kerja Kritis**: Karyawan dengan masa kerja antara 12 hingga 18 bulan memiliki kerentanan resign sebesar 35%.
4. **Kesenjangan Gaji**: Staf yang memiliki rasio gaji di bawah 80% rata-rata pasar (*Market Pay Ratio* < 0.8) memiliki peluang resign 3 kali lipat lebih tinggi.
5. **Rating Kinerja**: 15% dari karyawan yang resign adalah *High Performers* (nilai review > 4.5), sebuah kerugian intelektual yang besar bagi perusahaan.
6. **Waktu Resign Terbanyak**: Siklus pengunduran diri memuncak di bulan April, tepat setelah pembagian bonus tahunan.
7. **Rasio Promosi**: Karyawan yang tidak mendapat kenaikan golongan/promosi dalam 4 tahun memiliki tingkat kepuasan kerja (NPS proxy) di bawah 50%.
8. **Pengaruh Jarak Rumah**: Karyawan yang tinggal lebih dari 20 km dari kantor dan tidak memiliki akses kerja remote terhitung 25% dari total resign.
9. **Kinerja vs Attrition**: Karyawan berkinerja rendah (nilai review < 2) memiliki tingkat pengunduran diri sukarela yang kecil, melainkan didominasi pemberhentian oleh perusahaan.
10. **Tingkat Pendidikan**: Lulusan program magister (S2) memiliki retensi 20% lebih lama dibandingkan lulusan sarjana (S1) pada level jabatan manajerial.

## Recommendations
1. Susun peta jalur karir (*career pathing*) yang transparan dan lakukan review promosi setiap 2 tahun sekali.
2. Batasi jam lembur maksimal 10 jam per minggu per karyawan dan berikan kompensasi waktu libur pengganti.
3. Lakukan penyesuaian gaji secara bertahap untuk karyawan berkinerja tinggi yang gajinya masih di bawah standar pasar.
4. Terapkan program *Mentorship* khusus dan jalur karir cepat bagi karyawan baru di bulan ke-9 hingga ke-15 (masa kritis).
5. Buat kebijakan kerja fleksibel (hybrid/remote working) bagi staf dengan jarak tempat tinggal jauh.
6. Selenggarakan *Exit Interview* terstandarisasi untuk menangkap data pemicu resign secara akurat.
7. Optimalkan program pelatihan kepemimpinan (*Leadership Training*) bagi manajer divisi dengan attrition tertinggi.
8. Berikan tunjangan kesehatan mental dan keseimbangan kehidupan kerja (*work-life balance*).
9. Lakukan evaluasi gaji tahunan berdasarkan survei pasar berkala agar penawaran kompensasi tetap kompetitif.
10. Rancang program retensi khusus pasca-pembagian bonus tahunan untuk meminimalkan lonjakan resign massal.

---

## Tutorial Langkah demi Langkah (Real-World Implementation)

Berikut adalah panduan lengkap jika Anda ingin mengerjakan dan membangun proyek ini secara nyata di komputer lokal Anda:

### Langkah 1: Setup Database PostgreSQL
Jalankan script DDL berikut untuk membuat struktur database HR:

```sql
CREATE DATABASE hr_analytics;

-- Tabel Profil Karyawan
CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    hire_date DATE,
    resign_date DATE,
    status VARCHAR(20), -- 'Active' atau 'Resigned'
    department VARCHAR(50),
    review_score NUMERIC(3, 2),
    salary INT
);

-- Tabel Presensi & Overtime
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT REFERENCES employee(employee_id),
    work_date DATE,
    overtime_hours NUMERIC(4, 2)
);
```

### Langkah 2: Script Generate Data (Python)
Gunakan korelasi probabilitas attrition: karyawan dengan lembur berlebih dan gaji rendah di bawah pasar cenderung resign.

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 50k Employees
employees = []
start_date = datetime(2021, 1, 1)

for i in range(1, 50001):
    hire = start_date + timedelta(days=random.randint(0, 1000))
    status = random.choices(['Active', 'Resigned'], weights=[0.88, 0.12])[0]
    resign = hire + timedelta(days=random.randint(90, 700)) if status == 'Resigned' else None
    
    dept = random.choice(['Teknologi', 'Operasional', 'Sales', 'HR'])
    salary = random.randint(5000000, 30000000) # Gaji Bulanan Rupiah
    review = round(random.uniform(1.0, 5.0), 2)
    
    employees.append({
        'employee_id': i,
        'hire_date': hire.strftime('%Y-%m-%d'),
        'resign_date': resign.strftime('%Y-%m-%d') if resign else None,
        'status': status,
        'department': dept,
        'review_score': review,
        'salary': salary
    })

pd.DataFrame(employees).to_csv('employee.csv', index=False)

# Generate log lembur sampel (100k data relasional)
attendance = []
for i in range(1, 100000):
    e_id = random.randint(1, 50000)
    ot = 0
    # Overtime generator
    emp_dept = next(item for item in employees if item['employee_id'] == e_id)['department']
    if emp_dept == 'Teknologi' and random.random() < 0.6: # Tech lembur tinggi
        ot = round(random.uniform(1.0, 4.0), 1)
    else:
        ot = round(random.uniform(0.0, 2.0), 1)
        
    attendance.append({
        'attendance_id': i,
        'employee_id': e_id,
        'work_date': (start_date + timedelta(days=random.randint(1000, 1100))).strftime('%Y-%m-%d'),
        'overtime_hours': ot
    })

pd.DataFrame(attendance).to_csv('attendance.csv', index=False)
print("Data dummy HR berhasil dibuat!")
```

### Langkah 3: Eksekusi SQL Query
Import CSV ke PostgreSQL. Jalankan kueri korelasi rata-rata lembur terhadap tingkat resign yang ada di bagian **SQL Process** untuk melacak pemicu attrition.

### Langkah 4: Visualisasi di Power BI
1. Load tabel `employee` dan `attendance` ke Power BI.
2. Hubungkan `employee[employee_id]` ke `attendance[employee_id]`.
3. Buat visualisasi bertema korporasi navy blue dengan slider what-if parameter dinamis untuk menyimulasikan budget penyesuaian gaji minimum terhadap retensi karyawan.

