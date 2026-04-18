WITH customers AS (
    SELECT * FROM "neondb"."public"."stg_customers"
)
SELECT 
    customer_id,
    full_name,
    email
FROM customers