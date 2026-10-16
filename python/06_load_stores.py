import pandas as pd
import pyodbc

csv_path = r"C:\Users\Amulya Komuravelly\Desktop\Retail360\data\processed\stores_cleaned.csv"

df = pd.read_csv(csv_path)

print("Stores found:", len(df))

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Retail360DW;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

sql = """
INSERT INTO dim_store
    (store_id, store_name, city, state, store_type)
VALUES (?, ?, ?, ?, ?)
"""

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Stores loaded successfully!")

cursor.close()
conn.close()