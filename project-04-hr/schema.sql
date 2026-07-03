-- DDL Schema untuk PostgreSQL - HR Analytics

DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS employee CASCADE;

-- 1. Tabel Dimensi/Fakta Karyawan
CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    hire_date DATE NOT NULL,
    resign_date DATE,
    status VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL, -- Wajib diisi setelah ETL
    review_score NUMERIC(3, 2) NOT NULL,
    salary INT NOT NULL CHECK (salary > 0), -- Gaji harus positif setelah ETL
    CONSTRAINT chk_dates CHECK (resign_date IS NULL OR resign_date >= hire_date) -- Validasi tanggal setelah ETL
);

-- 2. Tabel Log Presensi (Overtime)
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employee(employee_id) ON DELETE CASCADE,
    work_date DATE NOT NULL,
    overtime_hours NUMERIC(4, 2) NOT NULL CHECK (overtime_hours >= 0) -- Lembur harus positif setelah ETL
);

-- Indeks Optimalisasi
CREATE INDEX idx_employee_dept ON employee(department);
CREATE INDEX idx_employee_status ON employee(status);
CREATE INDEX idx_attendance_emp ON attendance(employee_id);
CREATE INDEX idx_attendance_date ON attendance(work_date);
