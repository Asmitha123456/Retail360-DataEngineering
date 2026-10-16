
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SILVER_DIR = PROJECT_ROOT / "datalake" / "silver"
GOLD_DIR = PROJECT_ROOT / "datalake" / "gold"

GOLD_DIR.mkdir(parents=True, exist_ok=True)

# Load Silver datasets
orders = pd.read_csv(SILVER_DIR / "orders.csv")
products = pd.read_csv(SILVER_DIR / "products.csv")

print("Orders loaded:", len(orders))
print("Products loaded:", len(products))

# Avoid duplicate column names from the product table
product_details = products[
    ["product_id", "product_name", "category", "brand", "supplier"]
].drop_duplicates(subset=["product_id"])

# Join order transactions with product information
gold_sales = orders.merge(
    product_details,
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Add useful business metrics
gold_sales["order_date"] = pd.to_datetime(
    gold_sales["order_date"], errors="coerce"
)

gold_sales["order_year"] = gold_sales["order_date"].dt.year
gold_sales["order_month"] = gold_sales["order_date"].dt.month
gold_sales["order_month_name"] = (
    gold_sales["order_date"].dt.strftime("%B")
)

# Check product join quality
unmatched_products = gold_sales["product_name"].isna().sum()

# Save Gold dataset
output_file = GOLD_DIR / "gold_sales.csv"
gold_sales.to_csv(output_file, index=False)

print("\nGOLD SALES DATASET CREATED")
print("Rows:", len(gold_sales))
print("Columns:", len(gold_sales.columns))
print("Unmatched product rows:", unmatched_products)
print("Output:", output_file)

# Create a category-level summary
category_summary = (
    gold_sales.groupby("category", dropna=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        total_sales=("sales_amount", "sum"),
        total_profit=("profit", "sum")
    )
    .reset_index()
)

summary_file = GOLD_DIR / "gold_category_summary.csv"
category_summary.to_csv(summary_file, index=False)

print("\nCATEGORY SUMMARY CREATED")
print(category_summary.to_string(index=False))
print("\nRetail360 Gold transformation finished.")
