CREATE TABLE Transaction_Statements (
    statement_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_id INT NOT NULL,
    statement_period ENUM('Daily', 'Weekly', 'Monthly', 'Custom') DEFAULT 'Monthly',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    opening_balance DECIMAL(15, 2) NOT NULL,
    closing_balance DECIMAL(15, 2) NOT NULL,
    total_credits DECIMAL(15, 2) DEFAULT 0.00,
    total_debits DECIMAL(15, 2) DEFAULT 0.00,
    total_fees DECIMAL(10, 2) DEFAULT 0.00,
    transaction_count INT DEFAULT 0,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

    INDEX idx_user_statements (user_id, start_date, end_date),
    INDEX idx_account_statements (account_id, start_date, end_date)
);

