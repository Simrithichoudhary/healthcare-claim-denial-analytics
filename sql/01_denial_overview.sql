SELECT
    COUNT(*) AS total_claims,
    SUM(was_denied) AS denied_claims,
    ROUND(
        100.0 * SUM(was_denied) / COUNT(*),
        2
    ) AS denial_rate_pct,
    ROUND(SUM(claim_amount), 2) AS total_billed,
    ROUND(SUM(amount_paid), 2) AS total_paid,
    ROUND(SUM(revenue_leakage), 2) AS total_revenue_leakage
FROM claims;