import pandas as pd
import numpy as np
from pathlib import Path

# Create the raw data folder
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# -------------------------
# 1. Customers
# -------------------------
customers = pd.DataFrame({
    "customer_id": range(1, 1001),
    "customer_name": [f"Customer_{i}" for i in range(1, 1001)],
    "gender": np.random.choice(["Male", "Female"], 1000),
    "age": np.random.randint(18, 65, 1000),
    "city": np.random.choice(
        ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"],
        1000
    ),
    "state": np.random.choice(
        ["Telangana", "Karnataka", "Tamil Nadu", "Maharashtra", "Delhi"],
        1000
    ),
    "email": [f"customer{i}@email.com" for i in range(1, 1001)],
    "signup_date": pd.date_range("2023-01-01", periods=1000, freq="D")
})

# -------------------------
# 2. Products
# -------------------------
products = pd.DataFrame({
    "product_id": range(1, 101),
    "product_name": [f"Product_{i}" for i in range(1, 101)],
    "category": np.random.choice(
        ["Electronics", "Clothing", "Home", "Beauty", "Sports"],
        100
    ),
    "brand": np.random.choice(
        ["Brand_A", "Brand_B", "Brand_C", "Brand_D"],
        100
    ),
    "unit_price": np.round(np.random.uniform(100, 5000, 100), 2),
    "cost_price": np.round(np.random.uniform(50, 3000, 100), 2),
    "supplier": np.random.choice(
        ["Supplier_A", "Supplier_B", "Supplier_C"],
        100
    )
})

# -------------------------
# 3. Stores
# -------------------------
stores = pd.DataFrame({
    "store_id": range(1, 21),
    "store_name": [f"Store_{i}" for i in range(1, 21)],
    "city": np.random.choice(
        ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"],
        20
    ),
    "state": np.random.choice(
        ["Telangana", "Karnataka", "Tamil Nadu", "Maharashtra", "Delhi"],
        20
    ),
    "store_type": np.random.choice(
        ["Mall", "High Street", "Standalone"],
        20
    )
})

# -------------------------
# 4. Orders
# -------------------------
n_orders = 10000

orders = pd.DataFrame({
    "order_id": range(1, n_orders + 1),
    "order_date": pd.date_range(
        "2024-01-01",
        periods=n_orders,
        freq="h"
    ),
    "customer_id": np.random.randint(1, 1001, n_orders),
    "product_id": np.random.randint(1, 101, n_orders),
    "store_id": np.random.randint(1, 21, n_orders),
    "quantity": np.random.randint(1, 6, n_orders),
    "discount": np.round(np.random.uniform(0, 0.30, n_orders), 2),
    "payment_method": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Cash"],
        n_orders
    ),
    "order_status": np.random.choice(
        ["Completed", "Cancelled", "Pending"],
        n_orders
    )
})

# Get prices from products
orders = orders.merge(
    products[["product_id", "unit_price", "cost_price"]],
    on="product_id",
    how="left"
)

orders["gross_amount"] = (
    orders["quantity"] * orders["unit_price"]
)

orders["discount_amount"] = (
    orders["gross_amount"] * orders["discount"]
)

orders["sales_amount"] = (
    orders["gross_amount"] - orders["discount_amount"]
)

orders["profit"] = (
    orders["sales_amount"]
    - (orders["quantity"] * orders["cost_price"])
)

# -------------------------
# 5. Returns
# -------------------------
return_orders = np.random.choice(
    orders["order_id"],
    700,
    replace=False
)

returns = pd.DataFrame({
    "return_id": range(1, 701),
    "order_id": return_orders,
    "return_date": pd.date_range(
        "2024-02-01",
        periods=700,
        freq="D"
    ),
    "return_reason": np.random.choice(
        ["Damaged", "Wrong Product", "Customer Changed Mind", "Other"],
        700
    ),
    "refund_amount": np.round(
        np.random.uniform(100, 5000, 700),
        2
    )
})

# -------------------------
# Save CSV files
# -------------------------

customers.to_csv(output_dir / "customers.csv", index=False)
products.to_csv(output_dir / "products.csv", index=False)
stores.to_csv(output_dir / "stores.csv", index=False)
orders.to_csv(output_dir / "orders.csv", index=False)
returns.to_csv(output_dir / "returns.csv", index=False)

print("Retail360 dataset created successfully!")
print()
print("Files created:")
print("customers.csv")
print("products.csv")
print("stores.csv")
print("orders.csv")
print("returns.csv")