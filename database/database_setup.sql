-- Database: MomoProject
-- This script sets up the database schema for the MomoProject application.
-- It includes tables for the core entities such as Users, Transaction Categories, Transactions, and System logs.
-- Additionally, it also includes other entities such as Accounts, Merchants, Fees, Transaction Statements, and Transaction Limits.
-- Each entity has appropriate comments, constraints and indexes.
-- Also, it has basic CRUD operations for each table.
-- Users table

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'unique id',
    full_name VARCHAR(100) NOT NULL COMMENT 'full name',
    --email VARCHAR(100) UNIQUE NOT NULL COMMENT 'email for login',
    --pin INT NOT NULL COMMENT 'Login pin',
    phone_number VARCHAR(15) UNIQUE NOT NULL COMMENT 'MoMo number',
    balance DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Current balance of the account',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record update timestamp',
    CONSTRAINT chk_phone_number_format CHECK (phone_number REGEXP '^[0-9]{10,15}$'),
    INDEX idx_phone_number (phone_number)
) COMMENT 'Table for users';

-- Transaction Categories table
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE, 
    sub_type ENUM('Money Transfer','Cash Management','Payments','Financial Services','Other Services','Unknown') NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE Transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,             
    momo_reference VARCHAR(50) NULL,               
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    recepient_sender VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    fee DECIMAL(10, 2) DEFAULT 0.00,
    new_balance DECIMAL(15, 2) NOT NULL,
    date DATETIME NOT NULL,                         
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
) COMMENT 'Table for transactions';
-- Transaction Statements table
CREATE TABLE Transaction_Statements (
    statement_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique id for requested statements',
    user_id INT NOT NULL COMMENT 'user who requested for the statement',
    start_date DATE NOT NULL COMMENT 'start date for the statement',
    end_date DATE NOT NULL COMMENT 'end date',
    total_transactions INT NOT NULL COMMENT 'number of transactions in that statement',
    total_received DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Total amount received',
    total_sent DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Total amount sent',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When statement was generated',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_date_order CHECK (end_date >= start_date),
    INDEX idx_user_statements (user_id, generated_at),
    INDEX idx_date_range (start_date, end_date)
) COMMENT 'Table for storing statement requests';

-- System Logs table
CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'unique id for logs',
    user_id INT COMMENT 'user who performed the action',
    action VARCHAR(50) NOT NULL COMMENT 'type of action',
    description TEXT COMMENT 'details',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action was performed',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    CONSTRAINT chk_action_not_empty CHECK (LENGTH(action) > 0),
    INDEX idx_user_logs (user_id, created_at),
    INDEX idx_action_type (action)
) COMMENT 'Logs user activities and system events';

-- Populating fixed transaction types
INSERT INTO Transaction_Categories (category_name, sub_type, description, created_at) VALUES
('Sending p2p', 'Money Transfer', 'Person-to-person money sent', NOW()),
('Receiving p2p', 'Money Transfer', 'Person-to-person money received', NOW()),
('Deposit', 'Cash Management', 'Depositing cash at the agent', NOW()),
('Withdrawal', 'Cash Management', 'Withdrawing cash at the agent', NOW()),
('Code Payment', 'Payments', 'Payment to registered merchant', NOW()),
('Airtime', 'Payments', 'Mobile airtime/data purchase', NOW()),
('Water bill', 'Payments', 'Water bill payment', NOW()),
('Electricity bill', 'Payments', 'Electricity bill payment', NOW()),
('Bank to moMo', 'Financial Services', 'Transfer from bank to MoMo', NOW()),
('MoMo to bank', 'Financial Services', 'Transfer from MoMo to bank account', NOW()),
('Loan request', 'Financial Services', 'Loan received', NOW()),
('Loan repayment', 'Financial Services', 'Loan payment made', NOW()),
('Savings transfer', 'Financial Services', 'Transfer to savings account', NOW()),
('Virtual Card Funding', 'Other Services', 'Loading virtual card', NOW()),
('Bulk Payment Received', 'Other Services', 'Bulk payment from organization', NOW()),
('Salary Payment', 'Other Services', 'Salary received', NOW()),
('Reversal', 'Financial Services', 'Transaction reversed', NOW()), 
('Unknown Transaction', 'Unknown', 'Undetermined type', NOW());
