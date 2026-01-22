CREATE TABLE Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,  -- Generated MoMo account number
    account_type ENUM('Personal', 'Business', 'Agent') DEFAULT 'Personal',
    balance DECIMAL(15, 2) DEFAULT 0.00 NOT NULL,
    currency VARCHAR(3) DEFAULT 'RWF',
    account_status ENUM('Active', 'Suspended', 'Closed') DEFAULT 'Active',
    daily_limit DECIMAL(15, 2) DEFAULT 1000000.00,
    monthly_limit DECIMAL(15, 2) DEFAULT 30000000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE RESTRICT,

    INDEX idx_user_accounts (user_id),
    INDEX idx_account_number (account_number),
    INDEX idx_account_status (account_status)
);

