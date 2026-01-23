ALTER TABLE Users
MODIFY COLUMN momo_pin VARCHAR(255) NOT NULL;

-- Fixed the column name from update_at to updated_at
ALTER TABLE Users
CHANGE COLUMN update_at updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Expanded full_name field length
ALTER TABLE Users
MODIFY COLUMN full_name VARCHAR(100) NOT NULL;

-- Added 'Closed' option to account_status enum
ALTER TABLE Users
MODIFY COLUMN account_status ENUM('Active', 'Suspended', 'Closed') DEFAULT 'Active';

-- Added indexes for performance
ALTER TABLE Users
ADD INDEX idx_phone_number (phone_number);

ALTER TABLE Users
ADD INDEX idx_account_status (account_status);


ALTER TABLE Users ADD COLUMN username varchar(255) UNIQUE NOT NULL ;
ALTER TABLE Users ADD COLUMN email varchar(255) UNIQUE NOT NULL ;
ALTER TABLE momo_erd.Users ADD COLUMN password varchar(255) NOT NULL;