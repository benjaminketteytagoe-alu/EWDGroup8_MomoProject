CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_reference VARCHAR(50) UNIQUE NOT NULL,  -- e.g., "MOMO2026012212345"
    category_id INT NOT NULL,

    -- Sender information
    sender_account_id INT,
    sender_phone VARCHAR(15),

    -- Receiver information
    receiver_account_id INT,
    receiver_phone VARCHAR(15),

    -- Transaction details
    transaction_type ENUM('Debit', 'Credit') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    fee_charged DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(15, 2) NOT NULL,  -- amount + fee

    -- Balance tracking
    sender_balance_before DECIMAL(15, 2),
    sender_balance_after DECIMAL(15, 2),
    receiver_balance_before DECIMAL(15, 2),
    receiver_balance_after DECIMAL(15, 2),

    -- Status and metadata
    transaction_status ENUM('Pending', 'Success', 'Failed', 'Reversed') DEFAULT 'Pending',
    failure_reason TEXT,
    description VARCHAR(255),

    -- Timestamps
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys
    FOREIGN KEY (category_id) REFERENCES Transaction_Category(category_id) ON DELETE RESTRICT,
    FOREIGN KEY (sender_account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (receiver_account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

    -- Indexes for performance
    INDEX idx_transaction_reference (transaction_reference),
    INDEX idx_sender_account (sender_account_id, transaction_date),
    INDEX idx_receiver_account (receiver_account_id, transaction_date),
    INDEX idx_sender_phone (sender_phone, transaction_date),
    INDEX idx_receiver_phone (receiver_phone, transaction_date),
    INDEX idx_transaction_status (transaction_status),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_category (category_id)
);

