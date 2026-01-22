CREATE TABLE Merchants (
    merchant_id INT PRIMARY KEY AUTO_INCREMENT,
    merchant_name VARCHAR(100) NOT NULL,
    merchant_code VARCHAR(20) UNIQUE NOT NULL,
    account_id INT NOT NULL,
    business_type VARCHAR(50),
    address TEXT,
    merchant_status ENUM('Active', 'Suspended', 'Closed') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

    INDEX idx_merchant_code (merchant_code)
);

