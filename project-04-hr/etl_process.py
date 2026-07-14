import csv
import os
import subprocess
from datetime import datetime, timedelta

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

if not os.path.exists(os.path.join(raw_dir, 'employee.csv')):
    print("Raw data missing. Executing enrich_data.py first...")
    subprocess.run(['python', os.path.join(base_dir, 'enrich_data.py')], check=True)

print("--- Running ETL Process: Project 04 (HR Analytics) ---")

# 1. Clean Employee
employees = []
valid_emp_ids = set()
seen_emp = set()

with open(os.path.join(raw_dir, 'employee.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        eid = row['employee_id']
        if eid in seen_emp:
            continue
        seen_emp.add(eid)
        
        row['monthly_income'] = str(abs(float(row['monthly_income'])))
        if not row['department']:
            row['department'] = 'Unassigned'
            
        if row['resign_date'] and row['resign_date'] < row['hire_date']:
            h_dt = datetime.strptime(row['hire_date'], '%Y-%m-%d')
            row['resign_date'] = (h_dt + timedelta(days=180)).strftime('%Y-%m-%d')
            
        employees.append(row)
        valid_emp_ids.add(eid)

with open(os.path.join(proc_dir, 'employee.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(employees[0].keys()))
    writer.writeheader()
    writer.writerows(employees)
print(f"[OK] Processed {len(employees)} employees (salary, dept & date anomalies fixed).")

# 2. Clean Attendance
attendance = []
with open(os.path.join(raw_dir, 'attendance.csv'), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['employee_id'] not in valid_emp_ids:
            continue
        row['overtime_hours'] = str(abs(float(row['overtime_hours'])))
        attendance.append(row)

with open(os.path.join(proc_dir, 'attendance.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(attendance[0].keys()))
    writer.writeheader()
    writer.writerows(attendance)
print(f"[OK] Processed {len(attendance)} attendance records (overtime anomalies fixed).")
print("SUCCESS: Project 04 ETL process complete! Clean data in data/processed/")
