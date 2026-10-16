# Retail360 — Data Engineering & Sales Analytics

## Project Overview

Retail360 is an end-to-end retail data engineering and business intelligence project. It processes retail CSV datasets through Bronze, Silver, and Gold layers, loads analytics-ready sales data into SQL Server, and visualizes business performance in Power BI.

## Architecture

CSV Source Files → Bronze Layer → Silver Layer → Gold Layer → SQL Server (`Retail360DW`) → Power BI

> This implementation runs locally. Azure cloud services are not part of the current version.

## Technologies Used

- Python
- Pandas
- PySpark
- SQL Server and SQL
- Power BI Desktop
- Git and GitHub

## Project Structure

```text
Retail360/
├── data/                       # Source and processed datasets
├── datalake/
│   ├── bronze/                 # Raw ingested datasets
│   ├── silver/                 # Cleaned and transformed datasets
│   └── gold/                   # Analytics-ready datasets
├── python/                     # Python ingestion, cleaning, transformation,
│                               # and SQL-loading scripts
├── .gitignore                  # Files and folders excluded from Git
├── README.md                   # Project documentation
└── Retail360_Sales_Dashboard.pbix  # Power BI report (if included)
```

The exact locations of SQL scripts and the Power BI report may vary according to the local project folder structure.

## Pipeline Steps

1. **Ingestion:** Ingested retail CSV files into the local Bronze layer.
2. **Cleaning and Silver transformation:** Cleaned and deduplicated datasets using Python/Pandas and PySpark.
3. **Gold transformation:** Combined sales/order data with product details and added date attributes for analysis.
4. **SQL Server loading:** Loaded the Gold sales dataset into `dbo.gold_sales` in the `Retail360DW` database.
5. **Power BI reporting:** Built KPI cards and charts for sales, profit, monthly sales trends, category performance, and top products.

## Dataset and Results

- Gold sales dataset: **10,000 rows**
- Distinct order IDs: **10,000**
- Unmatched product rows during Gold transformation: **0**
- Gold table: `dbo.gold_sales`
- Database: `Retail360DW`

The Power BI report includes:
- Total Sales
- Total Profit
- Total Orders
- Monthly Sales Trend
- Sales by Category
- Top 10 Products by Sales

## How to Run

1. Install a compatible Python version and the packages required by the scripts.
2. Open the `Retail360` folder in VS Code.
3. Run the Python ingestion, cleaning, Silver, and Gold scripts in the order required by the project.
4. Configure the SQL Server connection in the loading script for your own environment.
5. Run the Gold-to-SQL loading script.
6. Open the `.pbix` report in Power BI Desktop and update the data-source settings if needed.

## Notes

- The SQL Server connection is configured for a local development environment; update it before running on another computer.
- Do not commit passwords, access tokens, `.env` files, or private customer information.
- Do not upload the `.venv` folder. Use a dependency file such as `requirements.txt` if you want others to recreate the Python environment.
- If the datasets are not permitted for public distribution, exclude them from a public repository and document how to obtain or generate them.

## Future Improvements

- Add automated data-quality checks and pipeline logging.
- Add a `requirements.txt` file for reproducible setup.
- Add dashboard screenshots.
- Add automated pipeline execution and refresh documentation.
- Consider cloud storage and orchestration in a future version.
