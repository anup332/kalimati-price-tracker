import pandas as pd
import os

from load import load_all_data


# ======================================================
# MARKET SUMMARY
# ======================================================

def market_summary(df):
    """
    Return a summary of the entire Kalimati dataset.
    """

    # Total number of rows
    total_records = len(df)

    # Number of different commodities
    total_commodities = df["commodity"].nunique()

    # Dataset start and end dates
    start_date = df["date"].min().date()
    end_date = df["date"].max().date()

    # Overall average market price
    overall_average = df["avg"].mean()

    # Average price of every commodity
    commodity_average = (
        df.groupby("commodity")["avg"]
        .mean()
        .sort_values(ascending=False)
    )

    # Most expensive commodity
    most_expensive = commodity_average.idxmax()
    highest_price = commodity_average.max()

    # Cheapest commodity
    cheapest = commodity_average.idxmin()
    lowest_price = commodity_average.min()

    # Return everything as a dictionary
    return {
        "Total Records": total_records,
        "Unique Commodities": total_commodities,
        "Date Range": f"{start_date} to {end_date}",
        "Overall Average Price": round(overall_average, 2),
        "Most Expensive Commodity": most_expensive,
        "Highest Average Price": round(highest_price, 2),
        "Cheapest Commodity": cheapest,
        "Lowest Average Price": round(lowest_price, 2)
    }


# ======================================================
# COMMODITY SUMMARY
# ======================================================

def commodity_summary(df):
    """
    Create summary statistics for every commodity.
    """

    summary = (
        df.groupby("commodity")
        .agg(
            Average_Price=("avg", "mean"),
            Minimum_Price=("avg", "min"),
            Maximum_Price=("avg", "max"),
            Price_Volatility=("avg", "std"),
            Days_Available=("avg", "count")
        )
        .round(2)
        .sort_values(by="Average_Price", ascending=False)
    )
    summary = summary.reset_index()

    return summary

# ======================================================
# DAILY MARKET TREND
# ======================================================

def daily_market_trend(df):
    """
    Calculate the average market price for each day.
    """

    trend = (
        df.groupby("date")
        .agg(
            Average_Market_Price=("avg", "mean"),
            Total_Commodities=("commodity", "count")
        )
        .round(2)
        .reset_index()
    )

    return trend


# ======================================================
# PRICE CHANGE ANALYSIS
# ======================================================

def price_change_report(df):
    """
    Calculate how much each commodity's average price
    changed from its first recorded day to its last
    recorded day.
    """

    # --------------------------------------------------
    # Sort by commodity and date
    # --------------------------------------------------
    # This guarantees that "first" and "last" really mean
    # earliest and latest dates.
    df = df.sort_values(by=["commodity", "date"])

    # --------------------------------------------------
    # Get the FIRST price of every commodity
    # --------------------------------------------------
    first_price = (
        df.groupby("commodity")
        .first()[["avg"]]
        .rename(columns={"avg": "First_Price"})
    )

    # --------------------------------------------------
    # Get the LAST price of every commodity
    # --------------------------------------------------
    last_price = (
        df.groupby("commodity")
        .last()[["avg"]]
        .rename(columns={"avg": "Last_Price"})
    )

    # --------------------------------------------------
    # Combine both tables
    # --------------------------------------------------
    report = first_price.join(last_price)

    # --------------------------------------------------
    # Calculate percentage change
    # --------------------------------------------------
    report["Percent_Change"] = (
        (report["Last_Price"] - report["First_Price"])
        / report["First_Price"]
    ) * 100

    # Round numbers
    report = report.round(2)

    # Commodity becomes a normal column again
    report = report.reset_index()

    return report


# ======================================================
# VOLATILITY REPORT
# ======================================================

def volatility_report(df):
    """
    Rank commodities by how much their prices fluctuate.

    Higher standard deviation = more unstable prices.
    """

    volatility = (
        df.groupby("commodity")
        .agg(
            Average_Price=("avg", "mean"),
            Price_Volatility=("avg", "std"),
            Minimum_Price=("avg", "min"),
            Maximum_Price=("avg", "max"),
            Days_Available=("avg", "count")
        )
        .round(2)
        .reset_index()
        .sort_values(
            by="Price_Volatility",
            ascending=False
        )
    )

    return volatility


# ======================================================
# KALIMATI BASKET PRICE
# ======================================================

def basket_price(df):
    """
    Calculate the average daily price of a basket
    of staple vegetables.
    """

    # --------------------------------------------------
    # Staple vegetable basket
    # --------------------------------------------------

    basket = [
        "आलु रातो(लाम्चो)",
        "प्याज सुकेको (भारतीय)",
        "गोलभेडा ठूलो(नेपाली)",
        "बन्दा(लोकल)",
        "काउली स्थानिय",
        "गाजर(लोकल)",
        "मूला सेतो(लोकल)"
    ]

    # --------------------------------------------------
    # Keep only basket commodities
    # --------------------------------------------------

    basket_df = df[df["commodity"].isin(basket)]

    # --------------------------------------------------
    # Average basket price for each day
    # --------------------------------------------------

    basket_daily = (
        basket_df
        .groupby("date")
        .agg(
            Basket_Price=("avg", "mean")
        )
        .round(2)
        .reset_index()
    )

    # --------------------------------------------------
    # Convert Basket Price into an Index
    # --------------------------------------------------

    # Price on the first day becomes the base (100)
    base_price = basket_daily.loc[0, "Basket_Price"]

    # Calculate the Kalimati Basket Price Index (KBPI)
    basket_daily["KBPI"] = (
        basket_daily["Basket_Price"] / base_price
    ) * 100

    # Round the index to 2 decimal places
    basket_daily["KBPI"] = basket_daily["KBPI"].round(2)

    return basket_daily


# ======================================================
# SAVE REPORT
# ======================================================

def save_report(df, filename):
    """
    Save a DataFrame into the reports folder.
    """

    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Full path of the output file
    filepath = os.path.join("reports", filename)

    # Save DataFrame as CSV
    df.to_csv(
        filepath,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved: {filepath}")

# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    # Load cleaned dataset
    df = load_all_data()

    # Generate market summary
    summary = market_summary(df)

    # Convert dictionary into a DataFrame
    summary_df = pd.DataFrame(
        summary.items(),
        columns=["Metric", "Value"]
    )

    # Save market summary
    save_report(
        summary_df,
        "market_summary.csv"
    )

    print("=" * 60)
    print("KALIMATI MARKET SUMMARY")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key:<28}: {value}")

    print("\n" + "=" * 60)
    print("TOP 10 MOST EXPENSIVE COMMODITIES")
    print("=" * 60)

    commodity_df = commodity_summary(df)

    print(commodity_df.head(10))
    save_report(
    commodity_df,
    "commodity_summary.csv"
    )

    print("\n" + "=" * 60)
    print("DAILY MARKET TREND")
    print("=" * 60)

    trend_df = daily_market_trend(df)

    print(trend_df.head(10))
    save_report(
    trend_df,
    "daily_market_trend.csv"
    )

    print("\n" + "=" * 60)
    print("TOP 10 PRICE INCREASES")
    print("=" * 60)

    price_report = price_change_report(df)

    print(
        price_report
        .sort_values("Percent_Change", ascending=False)
        .head(10)
    )
    save_report(
    price_report,
    "price_change_report.csv"
    )

    print("\n" + "=" * 60)
    print("TOP 10 PRICE DECREASES")
    print("=" * 60)

    print(
        price_report
        .sort_values("Percent_Change")
        .head(10)
    )

    print("\n" + "=" * 60)
    print("TOP 10 MOST VOLATILE COMMODITIES")
    print("=" * 60)

    volatility_df = volatility_report(df)

    print(volatility_df.head(10))
    save_report(
    volatility_df,
    "volatility_report.csv"
    )

    print("\n" + "=" * 60)
    print("KALIMATI BASKET PRICE")
    print("=" * 60)

    basket_df = basket_price(df)

    print(basket_df.head(10))
    save_report(
    basket_df,
    "basket_index.csv"
    )
