
import sqlite3
import getpass

import pandas as pd
from sqlalchemy import create_engine, URL

# Update this path if kalimati.db is stored elsewhere.
SQLITE_DB = "kalimati.db"

# PostgreSQL connection details.
# Change the username, host, port, or database if necessary.
pg_user = input("PostgreSQL username [postgres]: ").strip() or "postgres"
pg_password = getpass.getpass("PostgreSQL password: ")

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=pg_user,
    password=pg_password,
    host="localhost",
    port=5432,
    database="kalimati_analytics",
)

# Read the SQLite table.
with sqlite3.connect(SQLITE_DB) as conn:
    df = pd.read_sql_query(
        'SELECT date, commodity, unit, "min", "max", avg FROM prices',
        conn,
    )

# Convert columns to appropriate data types.
df["date"] = pd.to_datetime(df["date"], errors="coerce")

for column in ["min", "max", "avg"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Use descriptive column names in PostgreSQL.
df = df.rename(
    columns={
        "min": "min_price",
        "max": "max_price",
        "avg": "avg_price",
    }
)

# Remove rows with invalid dates before loading.
df = df.dropna(subset=["date"])

# Connect to PostgreSQL and load the table.
engine = create_engine(connection_url)

try:
    df.to_sql(
        name="prices",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    print(f"Successfully migrated {len(df):,} rows.")
    print("PostgreSQL table: kalimati_analytics.public.prices")

finally:
    engine.dispose()
