# Kalimati Food Price & Inflation Tracker

An end-to-end data analytics project that collects, cleans, stores, analyzes, and visualizes wholesale food-price data published by Kalimati Fruits and Vegetable Market, Nepal.

The project uses Python, Pandas, NumPy, SQLite, SQL, Matplotlib, Seaborn, and Power BI to explore food-price patterns from January 1 to July 31, 2026.

> **Important:** The selected-basket index in this project is an analytical indicator based on selected commodities. It is not Nepal's official Consumer Price Index (CPI) or an official inflation rate.

## Project Objectives

- Collect historical wholesale food-price data from the Kalimati Market website.
- Clean and prepare data for analysis.
- Explore price distributions, data quality, and commodity-level patterns.
- Compare monthly average prices and selected-basket price movements.
- Identify commodities with notable observed price changes.
- Present findings through Python visualizations, CSV reports, and a Power BI dashboard.

## Dataset Overview

| Metric | Value |
|---|---:|
| Data period | Jan 1 – Jul 31, 2026 |
| Price records | 21,095 |
| Unique commodities | 136 |
| Overall mean recorded average price | Rs. 142.97 |

The mean is calculated from the recorded `avg` prices across the dataset. Since commodities can use different units, it should not be interpreted as the average cost of a standard food basket.

## Technology Stack

- **Programming:** Python
- **Data manipulation:** Pandas, NumPy
- **Data collection:** Requests, BeautifulSoup
- **Database:** SQLite, SQL
- **Visualization:** Matplotlib, Seaborn
- **Dashboard:** Microsoft Power BI
- **Development tools:** Jupyter Notebook, VS Code, Git, GitHub

## Workflow

1. **Data collection:** Retrieve historical price data from the Kalimati Market website.
2. **Data cleaning:** Standardize data types, parse dates, inspect missing values, check duplicates, and investigate inconsistent or unusual price records.
3. **Database storage:** Store structured price records in SQLite.
4. **Exploratory data analysis:** Examine descriptive statistics, commodity coverage, and price distributions.
5. **Feature engineering:** Derive monthly summaries and a selected-basket price index.
6. **Trend analysis:** Compare monthly commodity prices and identify observed price increases and decreases.
7. **Reporting:** Export summary tables and analytical reports.
8. **Visualization:** Present results in Python charts and a three-page Power BI dashboard.

## Key Analysis

The final notebook, `mainanalysis.ipynb`, contains the data-quality checks, exploratory analysis, monthly summaries, selected-basket index, and price-trend visualizations.

The analysis explores:

- Dataset structure, descriptive statistics, and missing values
- Duplicate records and potentially inconsistent prices
- Commodity coverage over time
- Daily selected-basket price movements
- Monthly average prices and highest-priced commodities
- Monthly price patterns for selected commodities
- Potential outliers for further investigation
- Percentage changes between the first and last available monthly average prices for each commodity

## Power BI Dashboard

The Power BI dashboard contains three pages:

1. **Market Overview** — high-level market metrics and price trends
2. **Commodity Price Analysis** — comparisons across commodities
3. **Seasonal & Market Insights** — monthly patterns and market observations

The dashboard file is available in the `dashboard/` directory, if included in the repository.

## Repository Structure

```text
kalimati-price-tracker/
├── dashboard/
├── data/
├── reports/
├── mainanalysis.ipynb
├── analysis.ipynb
├── scrape.py
├── load.py
├── database.py
├── analyze.py
├── report.py
├── utils.py
├── sql_queries.sql
├── requirements.txt
├── .gitignore
└── README.md
```

Remove any filenames from this tree that are not actually present in the repository. If `mainanalysis.ipynb` replaces `analysis.ipynb`, you can remove the old notebook and its entry from this list.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/anup332/kalimati-price-tracker.git
cd kalimati-price-tracker
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the analysis

Open `mainanalysis.ipynb` in VS Code or Jupyter Notebook and run the cells in order.

The notebook expects the SQLite database and its `prices` table to be available at the configured path. Follow the project's data-collection and database-loading scripts if the database has not been created locally.

## Reports and Outputs

The `reports/` directory may contain outputs such as:

- `basket_index.csv`
- `commodity_summary.csv`
- `daily_market_trend.csv`
- `market_summary.csv`
- `price_change_report.csv`
- `volatility_report.csv`

Check the actual filenames in your repository and update this list if necessary.

## Limitations

- The analysis covers only January–July 2026 and does not establish year-over-year trends.
- Published wholesale prices may differ from retail prices and prices in other markets.
- The selected-basket index is not an official CPI or inflation measure.
- Raw prices across commodities may use different units and are not always directly comparable.
- Missing observations and unusual prices can affect the analysis.
- Observed price movements do not establish their causes.

## Future Improvements

- Automate regular data collection.
- Extend the dataset to multiple years.
- Add month-over-month and year-over-year comparisons when enough data is available.
- Investigate relationships with rainfall, fuel prices, and other relevant factors.
- Add anomaly detection and a web-based reporting interface.

## Author

**Anup Aryal**  
BSc CSIT | Data Analytics

GitHub: [anup332](https://github.com/anup332)

---

*This project was developed for learning and portfolio purposes using publicly available market-price data.*