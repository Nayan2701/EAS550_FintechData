
  
    

  create  table "neondb"."public"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    WITH customers AS (
    SELECT * FROM "neondb"."public"."stg_customers"
)
SELECT 
    customer_id,
    full_name,
    email
FROM customers
  );
  