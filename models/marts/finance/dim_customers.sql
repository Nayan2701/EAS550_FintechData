WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)
SELECT 
    customer_id,
    full_name,
    email
FROM customers