SELECT
    transaction_id,
    account_id,
    transaction_amount AS amount,
    transaction_date
FROM {{ source('fintech_raw', 'transactions') }}