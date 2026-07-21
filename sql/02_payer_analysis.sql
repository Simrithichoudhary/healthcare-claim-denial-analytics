SELECT
    payer_name,
    plan_type,
    COUNT(*) AS total_claims,
    SUM(was_denied) AS denied_claims,
    ROUND(
        100.0 * SUM(was_denied) / COUNT(*),
        2
    ) AS denial_rate_pct,
    ROUND(SUM(claim_amount), 2) AS total_billed,
    ROUND(SUM(revenue_leakage), 2) AS revenue_leakage
FROM claims
GROUP BY payer_name, plan_type
ORDER BY denial_rate_pct DESC;