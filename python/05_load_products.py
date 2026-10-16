import pandas as pd
import pyodbc

csv_path = r"C:\Users\Amulya Komuravelly\Desktop\Retail360\data\processed\products_cleaned.csv"

df = pd.read_csv(csv_path)

print("Products found:", len(df))

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Retail360DW;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

sql = """
INSERT INTO dim_product
    (product_id, product_name, category, brand, unit_price, cost_price, supplier)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Products loaded successfully!")

cursor.close()
conn.close()