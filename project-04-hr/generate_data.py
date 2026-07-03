import csv
import random
from datetime import datetime, timedelta
import os

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Memulai pembuatan data dummy untuk Project 4 - HR Analytics (Pure Python)...")

depts = ['Teknologi', 'Operasional', 'Sales', 'HR']

# 1. Generate Employee (3,000 employees)
NUM_EMP = 3000
employees = []
start_date = datetime(2021, 1, 1)

for i in range(1, NUM_EMP + 1):
    hire = start_date + timedelta(days=random.randint(0, 1000))
    status = random.choices(['Active', 'Resigned'], weights=[0.88, 0.12])[0]
    
    # Anomali: 1% data memiliki hire_date LEBIH BARU daripada resign_date
    if random.random() < 0.01:
        resign_date = hire - timedelta(days=random.randint(1, 100))
    else:
        resign_date = hire + timedelta(days=random.randint(90, 700)) if status == 'Resigned' else None
        
    dept = random.choice(depts)
    # Anomali: 1.5% employee memiliki departemen NULL (kosong)
    if random.random() < 0.015:
        dept = ''
        
    salary = random.randint(5000000, 30000000)
    # Anomali: 2% salary bernilai negatif
    if random.random() < 0.02:
        salary = -salary
        
    review = round(random.uniform(1.0, 5.0), 2)
    
    employees.append({
        'employee_id': i,
        'hire_date': hire.strftime('%Y-%m-%d'),
        'resign_date': resign_date.strftime('%Y-%m-%d') if resign_date else '',
        'status': status,
        'department': dept,
        'review_score': review,
        'salary': salary
    })

# Masukkan anomali: Duplikat karyawan (0.5% duplikat)
num_dupes = int(len(employees) * 0.005)
if num_dupes > 0:
    dupe_samples = random.sample(employees, num_dupes)
    for sample in dupe_samples:
        new_item = sample.copy()
        new_item['employee_id'] = len(employees) + 1
        employees.append(new_item)

with open('data/raw/employee.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['employee_id', 'hire_date', 'resign_date', 'status', 'department', 'review_score', 'salary'])
    writer.writeheader()
    writer.writerows(employees)
print(f"SUCCESS: Berhasil membuat data/raw/employee.csv ({len(employees)} baris)")

# 2. Generate Attendance Logs
attendance = []
for i in range(1, 10001):
    e_id = random.randint(1, NUM_EMP)
    ot = round(random.uniform(0.0, 4.0), 1)
    
    # Anomali: 1.5% lembur bernilai negatif
    if random.random() < 0.015:
        ot = -ot
        
    attendance.append({
        'attendance_id': i,
        'employee_id': e_id,
        'work_date': (start_date + timedelta(days=random.randint(1000, 1100))).strftime('%Y-%m-%d'),
        'overtime_hours': ot
    })

with open('data/raw/attendance.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['attendance_id', 'employee_id', 'work_date', 'overtime_hours'])
    writer.writeheader()
    writer.writerows(attendance)
print(f"SUCCESS: Berhasil membuat data/raw/attendance.csv ({len(attendance)} baris)")
print("Proses pembuatan raw data HR selesai!")
