import pandas as pd
from pathlib import Path

input_file = Path("data/raw/orders.csv")
output_file = Path("data/processed/orders_cleaned.csv")

orders = pd.read_csv(input_file)

print("Raw orders:", orders.shape)

print("\nMissing values before cleaning:")
print(orders.isnull().sum())

orders = orders.drop_duplicates()

print("\nOrders after removing duplicates:", orders.shape)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

print("\nInvalid dates:", orders["order_date"].isnull().sum())

orders = orders[orders["quantity"] > 0]

print("\nOrders after quantity validation:", orders.shape)

orders = orders[
    (orders["discount"] >= 0) &
    (orders["discount"] <= 1)
]

print("\nOrders after discount validation:", orders.shape)

output_file.parent.mkdir(parents=True, exist_ok=True)

orders.to_csv(output_file, index=False)

print("\nCleaning completed!")
print("Cleaned orders:", orders.shape)
print("Saved to:", output_file)