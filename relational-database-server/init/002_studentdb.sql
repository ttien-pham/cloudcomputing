-- Tạo database studentdb
CREATE DATABASE IF NOT EXISTS studentdb;

USE studentdb;

-- Tạo bảng students
CREATE TABLE IF NOT EXISTS students (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(10)  NOT NULL,
    fullname   VARCHAR(100) NOT NULL,
    dob        DATE,
    major      VARCHAR(50)
);

-- Chèn 3 bản ghi mẫu
INSERT INTO students (student_id, fullname, dob, major) VALUES
    ('SV001', 'Nguyen Van An',  '2003-05-15', 'Cong nghe Thong tin'),
    ('SV002', 'Tran Thi Bich',  '2003-08-22', 'Ky thuat Phan mem'),
    ('SV003', 'Le Hoang Minh',  '2002-11-01', 'An toan Thong tin');

-- Kiểm tra
SELECT * FROM students;
