
  create view "neondb"."public"."stg_accounts__dbt_tmp"
    
    
  as (
    SELECT
    account_id,
    customer_id,
    account_type,
    balance
FROM "neondb"."public"."accounts"
  );