
from pathlib import Path
import shutil

# Retail360 project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
BRONZE_DIR = PROJECT_ROOT / "datalake" / "bronze"

BRONZE_DIR.mkdir(parents=True, exist_ok=True)

# Copy source CSV files into Bronze, preserving originals
csv_files = list(RAW_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in {RAW_DIR}"
    )

for csv_file in csv_files:
    destination = BRONZE_DIR / csv_file.name
    shutil.copy2(csv_file, destination)
    print(f"Bronze copied: {csv_file.name}")

print(f"\nBronze ingestion completed: {len(csv_files)} files")
