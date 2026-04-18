
  create view "neondb"."public"."stg_merchants__dbt_tmp"
    
    
  as (
    SELECT
    merchant_id,
    merchant_name,
    category
FROM "neondb"."public"."merchants"
  );