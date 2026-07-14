import csv
import random
from datetime import datetime, timedelta
import os

random.seed(42)

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(proc_dir, exist_ok=True)

print("--- Enriching Project 04: HR Employee Attrition Dataset ---")

hr_file = os.path.join(base_dir, 'WA_Fn-UseC_-HR-Employee-Attrition.csv')
employees = []
attendance_logs = []

ref_date = datetime(2025, 6, 30)
att_counter = 1

# Industry Benchmark Salary multipliers by JobLevel
benchmarks = {
    '1': 4500,
    '2': 7500,
    '3': 11500,
    '4': 16000,
    '5': 22000
}

with open(hr_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        emp_num = row['EmployeeNumber'].strip()
        yrs_at_co = int(row.get('YearsAtCompany', '1'))
        attrition = row['Attrition'].strip()
        
        # Calculate hire_date
        hire_dt = ref_date - timedelta(days=yrs_at_co * 365 + random.randint(0, 180))
        
        # Calculate resign_date if Attrition == Yes
        resign_dt_str = ''
        if attrition == 'Yes':
            resign_dt = hire_dt + timedelta(days=random.randint(90, max(180, yrs_at_co * 365)))
            if resign_dt > ref_date:
                resign_dt = ref_date - timedelta(days=random.randint(1, 60))
            resign_dt_str = resign_dt.strftime('%Y-%m-%d')
            
        job_lvl = row.get('JobLevel', '1')
        monthly_inc = float(row.get('MonthlyIncome', '5000'))
        benchmark_sal = benchmarks.get(job_lvl, 5000)
        pay_ratio = round(monthly_inc / benchmark_sal, 2)
        
        employees.append({
            'employee_id': emp_num,
            'age': row['Age'],
            'gender': row['Gender'],
            'department': row['Department'],
            'job_role': row['JobRole'],
            'job_level': job_lvl,
            'monthly_income': monthly_inc,
            'market_pay_ratio': pay_ratio,
            'overtime': row['OverTime'],
            'years_at_company': yrs_at_co,
            'years_since_last_promotion': row.get('YearsSinceLastPromotion', '0'),
            'hire_date': hire_dt.strftime('%Y-%m-%d'),
            'resign_date': resign_dt_str,
            'status': 'Resigned' if attrition == 'Yes' else 'Active',
            'attrition': attrition
        })
        
        # Generate Attendance Overtime Logs
        is_ot = row['OverTime'] == 'Yes'
        for month_offset in range(12): # last 12 months logs
            work_dt = ref_date - timedelta(days=month_offset * 30 + random.randint(1, 10))
            if work_dt < hire_dt:
                continue
                
            ot_hours = round(random.uniform(2.5, 5.0), 1) if is_ot else round(random.uniform(0.0, 1.0), 1)
            
            attendance_logs.append({
                'attendance_id': att_counter,
                'employee_id': emp_num,
                'work_date': work_dt.strftime('%Y-%m-%d'),
                'overtime_hours': ot_hours
            })
            att_counter += 1

with open(os.path.join(raw_dir, 'employee.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(employees[0].keys()))
    writer.writeheader()
    writer.writerows(employees)

with open(os.path.join(raw_dir, 'attendance.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['attendance_id', 'employee_id', 'work_date', 'overtime_hours'])
    writer.writeheader()
    writer.writerows(attendance_logs)

print(f"SUCCESS: Enriched {len(employees)} employees and {len(attendance_logs)} attendance logs!")
