
  create view "neondb"."public"."stg_transactions__dbt_tmp"
    
    
  as (
    SELECT
    transaction_id,
    account_id,
    transaction_amount AS amount,
    transaction_date
FROM "neondb"."public"."transactions"
  );