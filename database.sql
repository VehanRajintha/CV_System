-- Create the database
CREATE DATABASE IF NOT EXISTS cv_system;
USE cv_system;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    INDEX email_idx (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create cvs table
CREATE TABLE IF NOT EXISTS cvs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    industry VARCHAR(255) NOT NULL,
    cv_file_path VARCHAR(255) NOT NULL,
    encrypted_key VARCHAR(255) NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX user_id_idx (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create admin user (password is 'admin123')
-- The hashed_password below is the bcrypt hash of 'admin123'
INSERT INTO users (email, name, hashed_password, is_admin)
VALUES (
    'admin@example.com',
    'Admin User',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGRl3Ob/oNK',
    TRUE
); 