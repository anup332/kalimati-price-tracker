import sqlite3
import pandas as pd

from load import load_all_data


# ======================================================
# CONFIGURATION
# ======================================================

DATABASE = "kalimati.db"


# ======================================================
# CREATE DATABASE TABLE
# ======================================================

def create_table():
    """
    Create the prices table if it does not already exist.
    """

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT NOT NULL,

            commodity TEXT NOT NULL,

            unit TEXT,

            min REAL,

            max REAL,

            avg REAL,

            UNIQUE(date, commodity)
        )
    """)

    connection.commit()
    connection.close()

    print("Prices table created successfully!")


# ======================================================
# LOAD DATA INTO DATABASE
# ======================================================

def load_data_to_database(df):
    """
    Insert the cleaned DataFrame into the SQLite database.
    """

    # --------------------------------------------------
    # Connect to SQLite database
    # --------------------------------------------------

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    # --------------------------------------------------
    # Insert records one by one
    #
    # INSERT OR IGNORE means:
    # if the same date + commodity already exists,
    # SQLite will skip that record.
    # --------------------------------------------------

    inserted = 0

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT OR IGNORE INTO prices
            (date, commodity, unit, min, max, avg)

            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["date"].strftime("%Y-%m-%d"),
            row["commodity"],
            row["unit"],
            row["min"],
            row["max"],
            row["avg"]
        ))

        # Check whether a row was actually inserted
        if cursor.rowcount == 1:
            inserted += 1

    # Save all changes
    connection.commit()

    connection.close()

    print(f"Records inserted: {inserted}")


# ======================================================
# CHECK DATABASE
# ======================================================

def check_database():
    """
    Display basic information about the database.
    """

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    # Count records
    cursor.execute("""
        SELECT COUNT(*)
        FROM prices
    """)

    total_records = cursor.fetchone()[0]

    print(f"Total records in database: {total_records}")

    # Show first five records
    cursor.execute("""
        SELECT date, commodity, unit, min, max, avg
        FROM prices
        LIMIT 5
    """)

    rows = cursor.fetchall()

    print("\nFirst 5 records:")

    for row in rows:
        print(row)

    connection.close()


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    # 1. Create table
    create_table()

    # 2. Load cleaned data from load.py
    df = load_all_data()

    print(f"\nDataFrame records: {len(df)}")

    # 3. Insert data into database
    load_data_to_database(df)

    # 4. Verify database
    print("\n" + "=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)

    check_database()