from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "healthcare_claims.db"

# Connect to database
conn = sqlite3.connect(DATABASE_PATH)

query = """
SELECT
    payer_name,
    ROUND(
        100.0 * SUM(was_denied) / COUNT(*),
        2
    ) AS denial_rate
FROM claims
GROUP BY payer_name
ORDER BY denial_rate DESC;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df)

# Create a bar chart
plt.figure(figsize=(8, 5))
plt.bar(df["payer_name"], df["denial_rate"])

plt.title("Denial Rate by Payer")
plt.xlabel("Payer")
plt.ylabel("Denial Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.show()