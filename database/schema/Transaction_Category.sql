CREATE TABLE Transaction_Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL, -- e.g., 'sending p2p'
    category_code VARCHAR(50) UNIQUE NOT NULL, -- e.g., 'SEND_P2P'
    parent_group VARCHAR(50) NOT NULL, -- e.g., 'MONEY_TRANSFER'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

