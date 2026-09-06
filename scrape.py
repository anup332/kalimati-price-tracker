import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta   # NEW

# ======================================================
# CONFIGURATION
# ======================================================

URL = "https://kalimatimarket.gov.np/price"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ======================================================
# NEW: DATE RANGE TO SCRAPE
# ======================================================

START_DATE = "2026-07-01"
END_DATE = "2026-07-31"

start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.strptime(END_DATE, "%Y-%m-%d")


# ======================================================
# START SESSION
# ======================================================

session = requests.Session()


# ======================================================
# GET PAGE ONCE TO OBTAIN CSRF TOKEN
# ======================================================

response = session.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

token = soup.find("input", {"name": "_token"})["value"]

print("CSRF Token:", token)


# ======================================================
# NEW: LOOP THROUGH EVERY DATE
# ======================================================

current_date = start_date

while current_date <= end_date:

    # NEW: Convert date object back to string
    selected_date = current_date.strftime("%Y-%m-%d")

    print(f"\nScraping {selected_date}...")

    payload = {
        "_token": token,
        "datePricing": selected_date
    }

    response = session.post(
        URL,
        headers=HEADERS,
        data=payload
    )

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    data = []

    for row in rows[1:]:

        cells = row.find_all("td")

        if len(cells) != 5:
            continue

        item = {
            "commodity": cells[0].get_text(strip=True),
            "unit": cells[1].get_text(strip=True),
            "min": cells[2].get_text(strip=True),
            "max": cells[3].get_text(strip=True),
            "avg": cells[4].get_text(strip=True),
        }

        data.append(item)

    # NEW: Filename changes every iteration
    filename = f"data/{selected_date}.csv"

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "commodity",
                "unit",
                "min",
                "max",
                "avg"
            ]
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"✓ Saved {filename}")

    # NEW: Move to the next day
    current_date += timedelta(days=1)


print("\nAll dates scraped successfully!")