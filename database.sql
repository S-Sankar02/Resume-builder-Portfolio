CREATE DATABASE resume_builder;

USE resume_builder;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    is_verified BOOLEAN DEFAULT FALSE,

    email_verify_token VARCHAR(255),
    otp_secret VARCHAR(255),

    login_otp VARCHAR(10),
    login_otp_expiry DATETIME,

    reset_token VARCHAR(255),
    reset_expiry DATETIME,

    failed_attempts INT DEFAULT 0,
    account_locked BOOLEAN DEFAULT FALSE,

    last_login DATETIME,
    last_ip VARCHAR(100),
    last_device VARCHAR(255),

    profile_image VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- Resumes Table
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    title VARCHAR(150) NOT NULL,
    summary TEXT,

    template_id VARCHAR(50) DEFAULT 'basic',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_resume_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


