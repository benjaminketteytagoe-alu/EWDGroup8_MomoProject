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
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'UNIQUE id for the category types',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'name of category type', 
    sub_type ENUM('Money Transfer','Cash Management','Payments','Financial Services','Other Services','Unknown') NOT NULL COMMENT 'sub transaction types'
    -- parent_group ENUM('Money Transfer','Cash Management','Payments','Financial Services','Other Services','Unknown') NOT NULL COMMENT 'major transaction types',
    description TEXT COMMENT 'category description',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'date create',
    CONSTRAINT chk_category_name_length CHECK (LENGTH(category_name) >= 3),
    INDEX idx_category_name (category_name),
    INDEX idx_parent_group (parent_group)
) COMMENT 'Table for all category types and parent groups';

-- Transactions table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'unique ids for each transaction',
    user_id INT NOT NULL COMMENT 'User ID from Users table',
    category_id INT NOT NULL COMMENT 'transaction category',
    transaction_type VARCHAR(50) NOT NULL COMMENT 'type of transaction',
    -- transaction_reference VARCHAR(50) NOT NULL COMMENT 'reference fetched from momo',
    recepient_sender VARCHAR(100) NOT NULL COMMENT 'Party involved in the transaction',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Transaction amount',
    fee DECIMAL(10, 2) DEFAULT 0.00 COMMENT 'fee charged',
    new_balance DECIMAL(15, 2) NOT NULL COMMENT 'balance after transaction',
    -- balance_before DECIMAL(15, 2) COMMENT 'balance before the transaction',
    -- balance_after DECIMAL(15, 2) NOT NULL COMMENT 'balance after transaction',
    -- transaction_date DATETIME NOT NULL COMMENT 'When transaction occurred',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When record was created',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT,
    CONSTRAINT chk_amount CHECK (amount > 0),
    CONSTRAINT chk_fee CHECK (fee >= 0),
    INDEX idx_user_transactions (user_id, transaction_date),
    INDEX idx_category (category_id),
    INDEX idx_recepient_sender (recepient_sender),
    -- INDEX idx_reference (transaction_reference),
    -- INDEX idx_date (transaction_date)
) COMMENT 'Table for all transaction records';

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
INSERT INTO Transaction_Categories (category_name, parent_group, description), created_at) VALUES
('Sending p2p', 'Money Transfer', 'Person-to-person money sent', NOW()),
('Receiving p2p', 'Money Transfer', 'Person-to-person money received', NOW()),
('Deposit', 'Cash Management', 'Depositing cash at the agent', NOW()),
('Withdrawal', 'Cash Management', 'Withdrawing cash at the agent', NOW()),
('Code Payment', 'Payments', 'Payment to registered merchant', NOW()),
('Merchant Payment', 'Payments', 'Payment to unregistered merchant', NOW()),
('Airtime', 'Payments', 'Mobile airtime/data purchase', NOW()),
('Water bill', 'Payments', 'Water bill payment', NOW()),
('Electricity bill', 'Payments', 'Electricity bill payment', NOW()),
('Other bills', 'Payments', 'Other utility bills payment', NOW()),  
('MoMo to bank', 'Financial Services', 'Transfer from MoMo to bank account', NOW()),
('Bank to moMo', 'Financial Services', 'Transfer from bank to MoMo'),
('Loan request', 'Financial Services', 'Loan received'),
('Loan repayment', 'Financial Services', 'Loan payment made'),
('Savings transfer', 'Financial Services', 'Transfer to savings account'),
('Virtual Card Funding', 'Other Services', 'Loading virtual card'),
('Bulk Payment Received', 'Other Services', 'Bulk payment from organization'),
('Salary Payment', 'Other Services', 'Salary received'),
('Unknown Transaction', 'Unknown', 'Transaction type could not be determined');
