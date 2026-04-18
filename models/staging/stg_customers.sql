SELECT
    customer_id,
    full_name,
    email
FROM {{ source('fintech_raw', 'customers') }}