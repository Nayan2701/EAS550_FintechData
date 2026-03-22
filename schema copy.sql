
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(50) CHECK (account_type IN ('Checking', 'Savings', 'Credit')),
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE Merchants (
    merchant_id SERIAL PRIMARY KEY,
    merchant_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Transactions (
    transaction_id UUID PRIMARY KEY,
    account_id INT NOT NULL,
    merchant_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id),
    FOREIGN KEY (merchant_id) REFERENCES Merchants(merchant_id)
);