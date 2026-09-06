-- =====================================================
-- 1. TOTAL NUMBER OF RECORDS
-- =====================================================

SELECT COUNT(*) AS total_records
FROM prices;

-- =====================================================
-- 2. UNIQUE COMMODITIES
-- =====================================================

SELECT COUNT(DISTINCT commodity) AS unique_commodities
FROM prices;

-- =====================================================
-- 3. DATASET DATE RANGE
-- =====================================================

SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM prices;

-- =====================================================
-- 4. AVERAGE PRICE BY COMMODITY
-- =====================================================

SELECT
    commodity,
    ROUND(AVG(avg), 2) AS average_price
FROM prices
GROUP BY commodity
ORDER BY average_price DESC;

-- =====================================================
-- 5. TOP 10 MOST EXPENSIVE COMMODITIES
-- =====================================================

SELECT
    commodity,
    ROUND(AVG(avg), 2) AS average_price
FROM prices
GROUP BY commodity
ORDER BY average_price DESC
LIMIT 10;

-- =====================================================
-- 6. DAILY MARKET TREND
-- =====================================================

SELECT
    date,
    ROUND(AVG(avg), 2) AS average_market_price,
    COUNT(DISTINCT commodity) AS commodities_available
FROM prices
GROUP BY date
ORDER BY date;

-- =====================================================
-- 7. DAY-OVER-DAY PRICE CHANGE
-- =====================================================

SELECT
    date,
    commodity,
    avg AS current_price,

    -- Previous recorded price for the same commodity
    LAG(avg) OVER (
        PARTITION BY commodity
        ORDER BY date
    ) AS previous_price,

    -- Percentage change from previous price
    ROUND(
        (
            (avg - LAG(avg) OVER (
                PARTITION BY commodity
                ORDER BY date
            ))
            /
            LAG(avg) OVER (
                PARTITION BY commodity
                ORDER BY date
            )
        ) * 100,
        2
    ) AS percent_change

FROM prices

ORDER BY commodity, date;

-- =====================================================
-- 8. MONTHLY AVERAGE PRICE
-- =====================================================

SELECT
    strftime('%Y-%m', date) AS month,
    commodity,
    ROUND(AVG(avg), 2) AS monthly_average_price

FROM prices

GROUP BY
    month,
    commodity

ORDER BY
    month,
    commodity;

-- =====================================================
-- 9. MOST VOLATILE COMMODITIES
-- =====================================================

SELECT
    commodity,
    ROUND(AVG(avg), 2) AS average_price,
    ROUND(
        SQRT(
            AVG(avg * avg) -
            AVG(avg) * AVG(avg)
        ),
        2
    ) AS price_volatility

FROM prices

GROUP BY commodity

ORDER BY price_volatility DESC

LIMIT 10;

-- =====================================================
-- 10. BIGGEST PRICE INCREASES
-- =====================================================

WITH price_changes AS (

    SELECT
        commodity,
        date,
        avg,

        LAG(avg) OVER (
            PARTITION BY commodity
            ORDER BY date
        ) AS previous_price

    FROM prices
)

SELECT
    commodity,
    date,
    ROUND(previous_price, 2) AS previous_price,
    ROUND(avg, 2) AS current_price,

    ROUND(
        ((avg - previous_price) / previous_price) * 100,
        2
    ) AS percent_change

FROM price_changes

WHERE previous_price IS NOT NULL
  AND previous_price > 0

ORDER BY percent_change DESC

LIMIT 10;

-- =====================================================
-- 11. BIGGEST PRICE DECREASES
-- =====================================================

WITH price_changes AS (

    SELECT
        commodity,
        date,
        avg,

        LAG(avg) OVER (
            PARTITION BY commodity
            ORDER BY date
        ) AS previous_price

    FROM prices
)

SELECT
    commodity,
    date,
    ROUND(previous_price, 2) AS previous_price,
    ROUND(avg, 2) AS current_price,

    ROUND(
        ((avg - previous_price) / previous_price) * 100,
        2
    ) AS percent_change

FROM price_changes

WHERE previous_price IS NOT NULL
  AND previous_price > 0

ORDER BY percent_change ASC

LIMIT 10;