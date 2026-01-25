
-- Database: MomoProject
-- This script sets up the database schema for the MomoProject application.
-- It includes tables for the core entities such as Users, Transaction Categories, Transactions, and System logs.
-- Additionaly it also include other entities such as Accounts, Merchants, Fees, Transaction Statements, and Transaction Limits.
-- Each entity has appropriate comments, constraints and indexes.
-- Also it has basic CRUD operations for each table.

-- User Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique internal identifier for the user table',
    full_name VARCHAR(100) NOT NULL COMMENT 'legal name of the customer',
    phone_number VARCHAR(15) NOT NULL UNIQUE COMMENT 'Registred mobile number used as account login',
    momo_pin VARCHAR(255) NOT NULL COMMENT 'Is a security code for transaction authorization',
    national_id VARCHAR(20) NOT NULL UNIQUE COMMENT 'Government issued identification number',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record last update timestamp',

) COMMENT='This table stores personal id info for momo customers';

  CONSTRAINT chk_phone_number_format CHECK (phone_number REGEXP '^[0-9]{10,15}$') COMMENT = 'This stores personal id info for momo customers';

    INDEX idx_phone_number ON Users(phone_number);
    INDEX idx_national_id ON Users(national_id);


-- Transaction Categories Table
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for each transaction category',
    category_name VARCHAR(50) NOT NULL COMMENT 'Name of the transaction category',
    describition TEXT COMMENT 'Description of the transaction category',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Indicates if the category is active',

)COMMENT='This table defines various transaction categories available in the system';

CONSTRAINT chk_category_name_length CHECK (LENGTH(category_name) >= 3) COMMENT = 'Category name must be at least 3 characters long';

    INDEX idx_category_name ON Transaction_Categories(category_name);


-- Accounts Table
CREATE TABLE Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each account',
    user_id INT NOT NULL COMMENT 'ID of the user owning the account',
    account_number VARCHAR(20) UNIQUE NOT NULL COMMENT 'Generated MoMo account number',
    account_type ENUM('Personal', 'Business', 'Agent') DEFAULT 'Personal' COMMENT 'Type of the account',
    balance DECIMAL(15, 2) DEFAULT 0.00 NOT NULL COMMENT 'Current balance of the account',
    currency VARCHAR(3) DEFAULT 'RWF' COMMENT 'Currency of the account',
    account_status ENUM('Active', 'Suspended', 'Closed') DEFAULT 'Active' COMMENT 'Status of the account',
    daily_limit DECIMAL(15, 2) DEFAULT 1000000.00 COMMENT 'Daily transaction limit for the account',
    monthly_limit DECIMAL(15, 2) DEFAULT 30000000.00 COMMENT 'Monthly transaction limit for the account',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',     
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record last update timestamp',

    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE RESTRICT,

)COMMENT='This table stores account information for MoMo users';

    CONSTRAINT chk_positive_balance CHECK (balance >= 0);
    CONSTRAINT chk_limits CHECK (monthly_limit >= daily_limit);

    INDEX idx_user_accounts Users(user_id);
    INDEX idx_account_status (account_status);

-- System Logs Table
CREATE TABLE System_Logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each log entry',
    user_id INT COMMENT 'ID of the user associated with the log entry',
    transaction_id INT COMMENT 'ID of the transaction associated with the log entry',
    action_type VARCHAR(50) NOT NULL COMMENT 'Type of action performed',
    table_name VARCHAR(50) COMMENT 'Name of the table affected',
    record_id INT COMMENT 'ID of the record affected',


    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE SET NULL,


) COMMENT='This table logs system activities for auditing and monitoring purposes';

CONSTRAINT chk_action_not_empty CHECK (LENGTH(action_type) > 0);

    INDEX idx_user_actions (user_id, created_at);
    INDEX idx_transaction_link (transaction_id);

-- Transactions Table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction',
    transaction_refrence VARCHAR(50) NOT NULL UNIQUE COMMENT 'Unique reference code for the transaction',
    category_id INT NOT NULL COMMENT 'ID of the transaction category',
    sender_account_id INT COMMENT 'Account ID of the sender',
    sender_phone VARCHAR(15) COMMENT 'Phone number of the sender',
    receiver_account_id INT COMMENT 'Account ID of the receiver',
    receiver_phone VARCHAR(15) COMMENT 'Phone number of the receiver',
    transaction_type ENUM('Debit', 'Credit') NOT NULL COMMENT 'Type of the transaction',
    amount DECIMAL(10, 2) NOT NULL COMMENT 'Amount involved in the transaction',
    fee_charged DECIMAL(10, 2) DEFAULT 0.00 COMMENT 'Fee charged for the transaction',
    total_amount DECIMAL(15, 2) NOT NULL COMMENT 'Total amount (amount + fee)',
    sender_balance_after DECIMAL(15, 2) COMMENT 'Sender new balance after transaction',
    transaction_status ENUM('Pending', 'Success', 'Failed', 'Reversed') DEFAULT 'Pending' COMMENT 'Current status of the transaction',
    description VARCHAR(255) COMMENT 'Description or notes about the transaction',
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time of the transaction',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',

    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT,
    FOREIGN KEY (sender_account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (receiver_account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,


) COMMENT = 'This table records all transactions made within the MomoProject system';

    CONSTRAINT chk_positive_amonut CHECK (amount > 0);
    CONSTRAINT chk_total_consistency CHEK (total_amount >= amount );
    CONSTRAINR chk_fee_positive CHECK (fee_charged >= 0);


    INDEX idx_transaction_date (transaction_date);
    INDEX idx_sender_search (sender_phone);
    INDEX idx_status_lookup (transaction_status);


-- Trnansaction Statement Table
CREATE TABLE Transaction_Statements (
    statement_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each statement entry',
    account_id INT NOT NULL COMMENT 'ID of the account associated with the statement',
    start_date DATETIME NOT NULL COMMENT 'Start date of the statement period',
    end_date DATETIME NOT NULL COMMENT 'End date of the statement period',
    openging_balance DECIMAL(15, 2) NOT NULL COMMENT 'Account balance at the start of the period',
    closing_balance DECIMAL(15, 2) NOT NULL COMMENT 'Account balance at the end of the period',
    transaction_count INT NOT NULL COMMENT 'Number of transactions in the statement period',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the statement was generated',

    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

)COMMENT='This table stores transaction statements for accounts';


    CONSTRAINT chk_date_consistency CHECK (end_date >= start_date);

    INDEX idx_account_statements (account_id, start_date);


-- Transaction limit Table
CREATE TABLE Transaction_Limits (
    limit_id INT PRIMARY KEY AUTO_INCREMENT  COMMENT 'Unique identifier for each limit entry',
    account_id INT NOT NULL COMMENT 'ID of the account associated with the limit',
    limit_date DATE NOT NULL COMMENT 'Date for which the limit is set',
    daily_sent_total DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Total amount sent on the given date',
    monthly_sent_total DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Total amount sent in the month of the given date',

    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

    UNIQUE KEY unique_account_date (account_id, limit_date),


) COMMENT='This table tracks daily and monthly transaction limits for accounts';

    CONSTRAINT chk_sent_positive CHECK (daily_sent_total >= 0);

    INDEX idx_limit_lookup (account_id, limit_date);


-- he merchants Table
CREATE TABLE Merchants (
    merchants_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each merchant',
    merchant_name VARCHAR(100) NOT NULL COMMENT 'Name of the merchant',
    merchant_code VARCHAR(20) UNIQUE NOT NULL COMMENT 'Unique code assigned to the merchant',
    account_id INT NOT NULL COMMENT 'Account ID associated with the merchant',
    business_type VARCHAR(50) COMMENT 'Type of business the merchant operates',
    address TEXT COMMENT 'Physical address of the merchant',
    merchant_status ENUM('Active', 'Suspended', 'Closed') DEFAULT 'Active' COMMENT 'Current status of the merchant',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',


    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT,

)COMMENT='This table stores information about merchants registered in the MoMo system';

    CONSTRAINT chk_merchant_name_val CHEK (LENGTH(merchant_name) >= 1);

    INDEX idx_merchant_lookup (merchant_code, merchant_status);



-- Fee Table
CREATE TABLE Fees (
    fee_id INT PRIMARY KEY AUTO_INCREMENT COMMENT  'Unique identifier for each fee entry',
    category_id INT NOT NULL COMMENT 'ID of the transaction category',
    min_amount DECIMAL(15, 2) NOT NULL COMMENT 'Minimum transaction amount for the fee',
    max_amount DECIMAL(15, 2) NOT NULL COMMENT 'Maximum transaction amount for the fee',
    fee_value DECIMAL(10, 2) NOT NULL COMMENT 'Fee amount or percentage',
    fee_type ENUM('Fixed', 'Percentage') NOT NULL COMMENT 'Type of fee: fixed amount or percentage',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',

    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT,

)COMMENT='This table defines fees associated with different transaction categories';

    CONSTRAINT chk_fee_range CHECK (max_amount > min_amount);
    CONSTRAINT chk_fee_positive CHECK (fee_value >= 0);

    INDEX idx_fee_search  (category_id, min_amount, max_amount);



-- Sample data DML, 5 records per main table

-- Insert sample Transaction Categories 
INSERT INTO Transaction_Categories (category_name, description) VALUES
('Transfer', 'Direct P2P money transfer'),
('Merchants Payment,' 'Payment for goods or services'),
('Withdrawal', 'Cash out at an authorized agent'),
('Deposite', 'Cash in at an authorized agent'),
('Airtime', 'Purchase of mobile credit');

-- Insert sample Users
INSERT INTO Users (full_name, phone_number, momo_pin, national_id) VALUES
('Jane Smith', '0788111001', '1234', '1199012345678001'),
('Samuel Carter', '0788111002', '2233', '1199012345678002'),
('Alice Mukana', '0788111003', '1111', '1199012345678003'),
('Bob Gasana', '0788111004', '4444', '1199012345678004'),
('Kigali Bakery', '0788111005', '0000', '1199012345678005');

-- Insert sample Accounts 
INSERT INTO Accounts ( user_id, account_number, balance, account_type) VALUES
(1, '0788111001', 50000.00, 'Personal'),
(2, '0788111002', 15500.00, 'Personal'),
(3, '0788111003', 2500.00, 'Personal'),
(4, '0788111004', 850000.00, 'Agent'),
(5, '0788111005', 120000.00, 'Business');


-- Insert Sample Transcation 
INSERT INTO Transactions (transaction_refrence, category_id, sender_account_id, receiver_account_id, amount, fee_charged, total_amount, transaction_status) VALUES
('TXN76662021', 1, 1, 2, 2000.00, 20.00, 2020.00, 'Success'),
('TXN73214484', 2, 2, 5, 1000.00, 0.00, 1000.00, 'Success'),
('TXN51732411', 5, 3, NULL, 500.00, 0.00, 500.00, 'Success'),
('TXN17818959', 3, 4, 1, 10000.00, 100.00, 10100.00, 'Success'),
('TXN36521838', 4, NULL, 4, 5000.00, 0.00, 5000.00, 'Success');

-- Insert sample Fees
INSERT INTO Fees ( category_id, min_amount, max_amount, fee_values, fee_type) VALUES
(1, 0.00, 1000.00, 10.00, 'Fixed'),
(1, 1001.00, 5000.00, 20.00, 'Fixed'),
(3, 0.00, 100000.00, 1.00, 'Percentage'),
(5, 0.00, 10000.00, 0.00, 'Fixed'),
(2, 0.00, 1000000.00, 0.00, 'Fixed');

-- Insert sample Ssystem Logs
INSERT INTO System_Logs (user_id, table_name, record_id) VALUES
(1, 'LOGIN', 'Users', 1),
(NULL, 'SMS_PARSED', 'Transactions', 1),
(NULL, 'SMS_PARSED', 'Transactions', 2),
(1, 'PIN_CHANGE', 'Users', 1),
(2, 'ACCOUNT_SUSPENDED', 'Accounts', 2);


-- Basic CRUD Operations to test the database implmentation 

-- Users Table CRUD
-- Create
INSERT INTO Users (full_name, phone_number, momo_pin, national_id) VALUES ('Didier Ishimwe', '0788999888', '5566', '1200180098765432');

-- Accounts Table CRUD
-- Create
INSERT INTO Accounts (user_id, account_number, balance, account_type, balance) VALUES (LAST_INSERT_ID(), '0788999888', 'Personal', 15000.00);

-- Read
SELECT u.full_name, a.account_number, a.balance
FROM Users u
JOIN Accounts a ON u.user_id = a.user_id
WHERE u.phone_number = '0788111001';

-- Update
UPDATE Accounts
SET balance = balance + 5000 
WHERE account_number = '0788111001';

--Delete
DELETE FROM System_Logs WHERE log_id = 1;






