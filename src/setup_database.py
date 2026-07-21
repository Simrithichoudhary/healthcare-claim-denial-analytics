from pathlib import Path
import sqlite3
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "healthcare_claims.csv"
DB_PATH = PROJECT_ROOT / "data" / "healthcare_claims.db"

# Read CSV
claims = pd.read_csv(CSV_PATH)

# Create SQLite database
conn = sqlite3.connect(DB_PATH)

# Load data into a table called 'claims'
claims.to_sql("claims", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")
print(f"Rows loaded: {len(claims)}")
print(f"Database location: {DB_PATH}")