WITH accounts AS (
    SELECT * FROM {{ ref('stg_accounts') }}
)
SELECT 
    account_id,
    customer_id,
    account_type,
    balance AS current_balance
FROM accounts
