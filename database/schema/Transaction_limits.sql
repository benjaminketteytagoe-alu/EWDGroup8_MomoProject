CREATE TABLE Transaction_Limits (
    limit_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    limit_date DATE NOT NULL,
    daily_sent DECIMAL(15, 2) DEFAULT 0.00,
    monthly_sent DECIMAL(15, 2) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,

    UNIQUE KEY unique_account_date (account_id, limit_date),
    INDEX idx_account_limit (account_id, limit_date)
);

