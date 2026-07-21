import sqlite3
import pandas as pd

conn = sqlite3.connect("data/healthcare_claims.db")

query = """
SELECT
    payer_name,
    COUNT(*) AS total_claims,
    SUM(was_denied) AS denied_claims,
    ROUND(
        100.0 * SUM(was_denied) / COUNT(*),
        2
    ) AS denial_rate
FROM claims
GROUP BY payer_name
ORDER BY denial_rate DESC;
"""

df = pd.read_sql_query(query, conn)

print(df)

conn.close()