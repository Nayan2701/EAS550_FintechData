-- Query 1: 7-Day Rolling Average Transaction Volume (Window Function)
SELECT 
    account_id,
    transaction_date,
    SUM(amount) OVER (
        PARTITION BY account_id 
        ORDER BY transaction_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7d_volume
FROM fct_transactions
WHERE status = 'Success';

-- Query 2: Fraud Anomaly Detection (CTE + Window Function + Aggregation)
WITH user_stats AS (
    SELECT 
        account_id,
        AVG(amount) as avg_amount,
        STDDEV(amount) as stddev_amount
    FROM fct_transactions
    GROUP BY account_id
)
SELECT 
    t.transaction_id,
    t.account_id,
    t.amount,
    s.avg_amount,
    (t.amount - s.avg_amount) / NULLIF(s.stddev_amount, 0) as z_score
FROM fct_transactions t
JOIN user_stats s ON t.account_id = s.account_id
WHERE (t.amount - s.avg_amount) / NULLIF(s.stddev_amount, 0) > 3;

-- Query 3: Monthly Account Growth & Rank (CTE + Date Truncation + Ranking)
WITH monthly_totals AS (
    SELECT 
        account_id,
        DATE_TRUNC('month', transaction_date) as report_month,
        SUM(amount) as total_volume
    FROM fct_transactions
    GROUP BY 1, 2
)
SELECT 
    account_id,
    report_month,
    total_volume,
    RANK() OVER (PARTITION BY report_month ORDER BY total_volume DESC) as volume_rank
FROM monthly_totals;

-- Strategic Indexing (To be executed by my teammate for the tuning report)
-- CREATE INDEX idx_fct_trans_acct_date ON fct_transactions(account_id, transaction_date);
