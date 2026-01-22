CREATE TABLE Transaction_Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    category_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    fee_percentage DECIMAL(5, 2) DEFAULT 0.00,
    fixed_fee DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_category_code (category_code)
);

