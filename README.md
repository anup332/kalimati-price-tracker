# Kalimati Food Price & Inflation Tracker

An end-to-end **food price analytics and inflation tracking platform** built using wholesale market data from the **Kalimati Fruits and Vegetable Market Development Board, Nepal**.

The project collects daily commodity prices, stores and processes the data, performs SQL and Python-based analysis, calculates price indices, identifies commodity-level trends and volatility, and presents insights through an interactive **Power BI dashboard**.

---

## Project Overview

Food prices can change significantly over time due to seasonality, supply conditions, demand, weather, transportation costs, and market conditions.

This project transforms daily wholesale market price data into an analytical dataset that can be used to answer questions such as:

* How are food prices changing over time?
* Which commodities are consistently expensive or inexpensive?
* Which commodities experience the highest price volatility?
* Which commodities are driving changes in the overall price index?
* How does the market-level food price index change over time?
* Which commodities have experienced the largest price increases or decreases?

---

## Key Results

Analysis of the collected dataset produced:

| Metric                                    |                    Result |
| ----------------------------------------- | ------------------------: |
| Data period                               | January 1 – July 31, 2026 |
| Total records                             |                    21,095 |
| Unique commodities                        |                       136 |
| Overall average price                     |                    142.97 |
| Most expensive commodity by average price |              सिताके च्याउ |
| Average price of most expensive commodity |                    899.42 |
| Lowest average-price commodity            |           मूला सेतो(लोकल) |
| Lowest average price                      |                     15.54 |

The project also generates analytical reports covering:

* Daily market trends
* Commodity-level summaries
* Price changes
* Commodity volatility
* Market-level price index
* Basket/index calculations

---

## Data Pipeline

```text
Kalimati Market Website
          │
          ▼
    Web Scraping
  Requests + BeautifulSoup
          │
          ▼
     Raw CSV Data
          │
          ▼
     Data Cleaning
   Python / Pandas
          │
          ▼
      SQLite Database
          │
          ▼
     SQL Analysis
          │
          ▼
  Python Analytics Layer
 Pandas / NumPy / Statistics
          │
          ▼
 Price Index & Inflation Analysis
          │
          ▼
   Analytical CSV Reports
          │
          ▼
      Power BI Dashboard
```

---

## Features

### 1. Automated Web Scraping

The scraper collects daily wholesale commodity prices from the Kalimati market website.

Technologies:

* Python
* Requests
* BeautifulSoup
* HTTP POST requests
* CSRF token handling

The scraper handles the website's CSRF protection by first retrieving the required token before submitting the data request.

---

### 2. Data Cleaning & Transformation

Raw price data is cleaned and transformed into analysis-ready datasets.

Processing includes:

* Converting Nepali numeric characters into usable numerical values
* Cleaning currency-formatted price strings
* Handling missing values
* Standardizing commodity records
* Combining daily datasets
* Preparing data for database storage and analysis

---

### 3. SQLite Database

The project uses SQLite to store structured market data.

The database layer separates data storage from the analytical workflow and allows SQL queries to be performed directly on the collected market data.

The SQLite database itself is excluded from the GitHub repository because the underlying CSV datasets already provide reproducible source data.

---

### 4. SQL Analytics

The project includes a dedicated `sql_queries.sql` file containing analytical queries.

The SQL analysis covers areas such as:

* Aggregations
* Commodity-level statistics
* Price comparisons
* Grouping and filtering
* Market trends
* Ranking commodities
* Price changes
* Analytical summaries

---

### 5. Price & Inflation Analysis

A market basket/index approach is used to track changes in overall food prices.

The analysis produces:

* Basket index
* Market-level price index
* Daily market trends
* Commodity-level price changes
* Price volatility
* Summary statistics

The index allows the project to represent changes in the overall price level rather than focusing only on individual commodities.

---

### 6. Analytical Reports

The `reports/` directory contains processed analytical outputs:

```text
reports/
├── basket_index.csv
├── commodity_summary.csv
├── daily_market_trend.csv
├── market_summary.csv
├── price_change_report.csv
└── volatility_report.csv
```

These outputs can be consumed directly by visualization and business intelligence tools.

---

### 7. Power BI Dashboard

The processed data is used to build an interactive Power BI dashboard for exploring:

* Market price trends
* Food price index
* Commodity prices
* Price changes
* Commodity comparisons
* Market-level indicators

The dashboard is designed to provide a business-friendly view of the underlying analytical pipeline.

---

## Project Structure

```text
kalimati-price-tracker/
│
├── data/
│   ├── 2026-01-01.csv
│   ├── 2026-01-02.csv
│   ├── ...
│   ├── 2026-07-31.csv
│   └── kalimati_prices.csv
│
├── reports/
│   ├── basket_index.csv
│   ├── commodity_summary.csv
│   ├── daily_market_trend.csv
│   ├── market_summary.csv
│   ├── price_change_report.csv
│   └── volatility_report.csv
│
├── analysis.ipynb
├── analyze.py
├── database.py
├── load.py
├── report.py
├── scrape.py
├── sql_queries.sql
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

### Programming & Analysis

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn

### Database

* SQLite
* SQL

### Web Scraping

* Requests
* BeautifulSoup

### Visualization & BI

* Power BI
* Matplotlib
* Seaborn

### Development

* Jupyter Notebook
* VS Code
* Git & GitHub

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/anup332/kalimati-price-tracker.git
cd kalimati-price-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the analysis

The main analysis can be explored through:

```text
analysis.ipynb
```

Individual Python scripts are also provided for the different stages of the pipeline.

---

## Data Source

The project uses publicly available wholesale market price information published by the **Kalimati Fruits and Vegetable Market Development Board, Nepal**.

The collected dataset covers:

**January 1, 2026 – July 31, 2026**

---

## Future Improvements

Potential extensions include:

* Automating daily data collection
* Scheduling the pipeline using a workflow orchestrator
* Adding a cloud database
* Building an automated ETL pipeline
* Adding month-over-month and year-over-year inflation measures
* Incorporating external factors such as rainfall and fuel prices
* Adding anomaly detection for unusual commodity price movements
* Deploying the dashboard as a web application
* Expanding the dataset to multiple years for stronger inflation analysis

---

## Author

**Anup Aryal**

BSc CSIT | Data Analytics | Python | SQL | Power BI

GitHub: [@anup332](https://github.com/anup332)
