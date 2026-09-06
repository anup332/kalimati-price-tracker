import os
import pandas as pd

# ======================================================
# CONFIGURATION
# ======================================================

# Folder where all daily CSV files are stored
DATA_FOLDER = "data"


# ======================================================
# HELPER FUNCTION
# ======================================================

def clean_price(price):
    """
    Convert Nepali price strings into float.

    Examples:
        'रू ४५.००'   -> 45.0
        'रू 1,250.00' -> 1250.0
        '-', '', None -> None
    """

    # Handle missing values
    if pd.isna(price):
        return None

    # Convert to string
    price = str(price).strip()

    # Handle invalid values
    if price in ["", "-", "--", "N/A"]:
        return None

    # Remove Nepali currency symbol
    price = price.replace("रू", "")

    # Remove commas from numbers
    price = price.replace(",", "")

    # Remove leading/trailing spaces
    price = price.strip()

    # Convert to float
    try:
        return float(price)

    except ValueError:
        return None


# ======================================================
# LOAD ALL DATA
# ======================================================

def load_all_data():
    """
    Read every CSV from the data folder,
    clean the data,
    and combine everything into one DataFrame.
    """

    # Store every day's DataFrame here
    dataframes = []

    # Get all CSV files and sort them by filename (date)
    files = sorted(
        file for file in os.listdir(DATA_FOLDER)
        if file.endswith(".csv")
    )

    # Read every CSV file
    for file in files:

        # Full path to the file
        file_path = os.path.join(DATA_FOLDER, file)

        # Extract date from filename
        # Example:
        # 2026-06-15.csv -> 2026-06-15
        file_date = file.replace(".csv", "")

        # Read CSV into a DataFrame
        df = pd.read_csv(file_path)

        # --------------------------------------------------
        # CLEAN PRICE COLUMNS
        # --------------------------------------------------

        # These columns should contain numbers
        price_columns = ["min", "max", "avg"]

        # Clean each price column
        for column in price_columns:
            df[column] = df[column].apply(clean_price)

        # --------------------------------------------------
        # CLEAN TEXT COLUMNS
        # --------------------------------------------------

        # Remove unwanted spaces
        df["commodity"] = df["commodity"].str.strip()
        df["unit"] = df["unit"].str.strip()

        # --------------------------------------------------
        # ADD DATE COLUMN
        # --------------------------------------------------

        df["date"] = pd.to_datetime(file_date)

        # Save today's cleaned DataFrame
        dataframes.append(df)

    # ------------------------------------------------------
    # COMBINE ALL DATAFRAMES
    # ------------------------------------------------------

    combined_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    # ------------------------------------------------------
    # SORT DATA
    # ------------------------------------------------------

    # Arrange by date first, then commodity
    combined_df = combined_df.sort_values(
        by=["date", "commodity"]
    )

    # Reset index after sorting
    combined_df = combined_df.reset_index(drop=True)

    return combined_df


# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    # Load the complete dataset
    df = load_all_data()

    print("=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)
    print(df.head())

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    print(df.isna().sum())

    print("\n" + "=" * 60)
    print("DATAFRAME INFO")
    print("=" * 60)
    df.info()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(df.describe(include="all"))

# Export cleaned SQLite data for Power BI
import sqlite3
import pandas as pd

conn = sqlite3.connect("kalimati.db")

df = pd.read_sql_query("SELECT * FROM prices", conn)

df.to_csv(
    "data/kalimati_prices.csv",
    index=False,
    encoding="utf-8-sig"
)

conn.close()

print("Exported:", df.shape)