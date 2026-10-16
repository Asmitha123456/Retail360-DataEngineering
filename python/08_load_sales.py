import pandas as pd
import pyodbc

csv_path = r"C:\Users\Amulya Komuravelly\Desktop\Retail360\data\processed\orders_cleaned.csv"

df = pd.read_csv(csv_path)

print("Orders found:", len(df))

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Retail360DW;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

sql = """
INSERT INTO fact_sales
(
    order_id,
    date_key,
    customer_key,
    product_key,
    store_key,
    quantity,
    discount,
    payment_method,
    order_status,
    unit_price,
    gross_amount,
    discount_amount,
    sales_amount,
    profit
)
SELECT
    ?,
    CONVERT(INT, CONVERT(VARCHAR(8), ?, 112)),
    c.customer_key,
    p.product_key,
    s.store_key,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
FROM dim_customer c
CROSS JOIN dim_product p
CROSS JOIN dim_store s
WHERE c.customer_id = ?
  AND p.product_id = ?
  AND s.store_id = ?
"""

for row in df.itertuples(index=False, name=None):
    (
        order_id,
        order_date,
        customer_id,
        product_id,
        store_id,
        quantity,
        discount,
        payment_method,
        order_status,
        unit_price,
        cost_price,
        gross_amount,
        discount_amount,
        sales_amount,
        profit
    ) = row

    cursor.execute(
        sql,
        order_id,
        order_date,
        quantity,
        discount,
        payment_method,
        order_status,
        unit_price,
        gross_amount,
        discount_amount,
        sales_amount,
        profit,
        customer_id,
        product_id,
        store_id
    )

conn.commit()

print("Sales loaded successfully!")

cursor.close()
conn.close()