CREATE DATABASE IF NOT EXISTS secure_mysql_db;
USE secure_mysql_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL
);

INSERT INTO employees (name, role)
SELECT 'Demo Employee', 'Developer'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE name='Demo Employee');
