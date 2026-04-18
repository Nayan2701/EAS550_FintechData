SELECT
    account_id,
    customer_id,
    account_type,
    balance
FROM {{ source('fintech_raw', 'accounts') }}