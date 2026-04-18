SELECT
    transaction_id,
    account_id,
    transaction_amount AS amount,
    transaction_date
FROM "neondb"."public"."transactions"