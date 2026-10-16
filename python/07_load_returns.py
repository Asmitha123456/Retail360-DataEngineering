import pandas as pd
import pyodbc

csv_path = r"C:\Users\Amulya Komuravelly\Desktop\Retail360\data\processed\returns_cleaned.csv"

df = pd.read_csv(csv_path)

print("Returns found:", len(df))

df["return_date"] = pd.to_datetime(
    df["return_date"],
    errors="coerce"
).dt.date

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Retail360DW;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

sql = """
INSERT INTO fact_returns
    (return_id, order_id, return_date, return_reason, refund_amount)
VALUES (?, ?, ?, ?, ?)
"""

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Returns loaded successfully!")

cursor.close()
conn.close()