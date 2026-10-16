import pandas as pd
from pathlib import Path


def clean_csv(file_name):
    input_file = Path("data/raw") / file_name
    output_file = Path("data/processed") / file_name.replace(".csv", "_cleaned.csv")

    df = pd.read_csv(input_file)

    print(f"\n===== {file_name} =====")
    print("Raw shape:", df.shape)

    # Remove duplicate rows
    df = df.drop_duplicates()

    print("After duplicates:", df.shape)

    # Remove completely empty rows
    df = df.dropna(how="all")

    print("After empty rows:", df.shape)

    # Save cleaned data
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print("Saved to:", output_file)


clean_csv("customers.csv")
clean_csv("products.csv")
clean_csv("stores.csv")
clean_csv("returns.csv")

print("\nAll datasets cleaned successfully!")