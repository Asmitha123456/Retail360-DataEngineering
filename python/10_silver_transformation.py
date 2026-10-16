
from pathlib import Path
import shutil

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BRONZE_DIR = PROJECT_ROOT / "datalake" / "bronze"
SILVER_DIR = PROJECT_ROOT / "datalake" / "silver"

SILVER_DIR.mkdir(parents=True, exist_ok=True)

# Start Spark
spark = (
    SparkSession.builder
    .appName("Retail360-Silver")
    .master("local[1]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    datasets = [
        "customers",
        "orders",
        "products",
        "returns",
        "stores",
    ]

    for name in datasets:
        source = BRONZE_DIR / f"{name}.csv"

        if not source.exists():
            print(f"SKIPPED: {source} not found")
            continue

        # Read Bronze CSV with PySpark
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(source))
        )

        # Remove exact duplicate rows
        df = df.dropDuplicates()

        # Remove completely empty rows
        if df.columns:
            non_empty = None

            for column_name in df.columns:
                condition = col(column_name).isNotNull()
                non_empty = (
                    condition if non_empty is None
                    else non_empty | condition
                )

            df = df.filter(non_empty)

        # Count rows after cleaning
        row_count = df.count()

        # Collect transformed results to the local machine
        pdf = df.toPandas()

        # Write a regular CSV file using Python
        destination = SILVER_DIR / f"{name}.csv"
        pdf.to_csv(destination, index=False, encoding="utf-8")

        print(
            f"SILVER COMPLETE: {name} | "
            f"Rows: {row_count} | File: {destination.name}"
        )

finally:
    spark.stop()

print("Retail360 Silver transformation finished.")
