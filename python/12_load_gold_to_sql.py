
from pathlib import Path
import pandas as pd
import pyodbc

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "datalake" / "gold" / "gold_sales.csv"

# Read the Gold dataset
df = pd.read_csv(CSV_FILE)
df = df.where(pd.notna(df), None)

print("CSV rows:", len(df))

# SQL Server connection
# Change SERVER if your SSMS uses a different server name.
SERVER = r"localhost"
DATABASE = "retail360dw"
DRIVER = "ODBC Driver 18 for SQL Server"

connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
cursor.fast_executemany = False

columns = list(df.columns)
column_sql = ", ".join(f"[{c}]" for c in columns)
placeholders = ", ".join("?" for _ in columns)

insert_sql = (
    f"INSERT INTO dbo.gold_sales ({column_sql}) "
    f"VALUES ({placeholders})"
)

# Convert pandas/numpy values to Python values for ODBC
rows = [
    tuple(
        None if pd.isna(value) else
        value.item() if hasattr(value, "item") else value
        for value in row
    )
    for row in df.itertuples(index=False, name=None)
]

try:
    cursor.executemany(insert_sql, rows)
    conn.commit()
    print("SUCCESS: Gold data loaded into SQL Server.")
    print("Rows inserted:", len(rows))
except Exception:
    conn.rollback()
    raise
finally:
    cursor.close()
    conn.close()
