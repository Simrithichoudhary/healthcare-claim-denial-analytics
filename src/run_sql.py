from pathlib import Path
import sqlite3
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "healthcare_claims.db"
SQL_FOLDER = PROJECT_ROOT / "sql"

# Read SQL file
sql_file = SQL_FOLDER / "02_payer_analysis.sql"

with open(sql_file, "r") as file:
    query = file.read()

# Execute query
conn = sqlite3.connect(DATABASE_PATH)

df = pd.read_sql_query(query, conn)

print(df)

conn.close()