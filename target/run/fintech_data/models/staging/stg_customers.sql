
  create view "neondb"."public"."stg_customers__dbt_tmp"
    
    
  as (
    SELECT
    customer_id,
    full_name,
    email
FROM "neondb"."public"."customers"
  );