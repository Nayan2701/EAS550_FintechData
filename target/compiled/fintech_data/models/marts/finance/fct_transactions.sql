WITH transactions AS (
    SELECT * FROM "neondb"."public"."stg_transactions"
),
accounts AS (
    SELECT * FROM "neondb"."public"."stg_accounts"
)
SELECT 
    t.transaction_id,
    t.account_id,
    a.customer_id,
    t.transaction_date,
    DATE(t.transaction_date) AS date_key,
    t.amount
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id