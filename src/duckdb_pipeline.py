import duckdb
import os

RAW_FILE = "data/raw/2019-Nov.csv"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

con = duckdb.connect()

print("Creating canonical events table...")

con.execute(f"""
CREATE OR REPLACE TABLE events AS
SELECT
    CAST(event_time AS TIMESTAMP) AS event_time,
    DATE(CAST(event_time AS TIMESTAMP)) AS event_date,
    event_type,
    product_id,
    category_id,
    category_code,
    brand,
    price,
    user_id,
    user_session
FROM read_csv_auto('{RAW_FILE}')
WHERE event_type IN ('view', 'cart', 'purchase')
""")

print("Total rows:")
print(con.execute("SELECT COUNT(*) FROM events").fetchall())

print("Creating session-level funnel base...")

con.execute("""
CREATE OR REPLACE TABLE session_funnel AS
WITH session_events AS (
    SELECT
        user_session,
        MIN(CASE WHEN event_type = 'view' THEN event_time END) AS first_view_time,
        MIN(CASE WHEN event_type = 'cart' THEN event_time END) AS first_cart_time,
        MIN(CASE WHEN event_type = 'purchase' THEN event_time END) AS first_purchase_time
    FROM events
    GROUP BY user_session
)
SELECT
    user_session,
    first_view_time,
    first_cart_time,
    first_purchase_time,
    CASE WHEN first_view_time IS NOT NULL THEN 1 ELSE 0 END AS has_view,
    CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_cart_time >= first_view_time
        THEN 1 ELSE 0
    END AS has_cart_after_view,
    CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_purchase_time IS NOT NULL
         AND first_cart_time >= first_view_time
         AND first_purchase_time >= first_cart_time
        THEN 1 ELSE 0
    END AS has_purchase_after_cart
FROM session_events
""")

print("Computing funnel summary...")

con.execute("""
CREATE OR REPLACE TABLE funnel_summary AS
SELECT
    SUM(has_view) AS view_sessions,
    SUM(has_cart_after_view) AS cart_sessions,
    SUM(has_purchase_after_cart) AS purchase_sessions
FROM session_funnel
""")

con.execute(f"""
COPY funnel_summary TO '{PROCESSED_DIR}/funnel_summary.parquet'
(FORMAT PARQUET)
""")

print("Computing funnel by brand...")

con.execute("""
CREATE OR REPLACE TABLE funnel_by_brand AS
WITH brand_session_base AS (
    SELECT
        brand,
        user_session,
        MIN(CASE WHEN event_type = 'view' THEN event_time END) AS first_view_time,
        MIN(CASE WHEN event_type = 'cart' THEN event_time END) AS first_cart_time,
        MIN(CASE WHEN event_type = 'purchase' THEN event_time END) AS first_purchase_time
    FROM events
    GROUP BY brand, user_session
)
SELECT
    COALESCE(brand, 'Unknown') AS brand,
    SUM(CASE WHEN first_view_time IS NOT NULL THEN 1 ELSE 0 END) AS view_sessions,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_cart_time >= first_view_time
        THEN 1 ELSE 0 END) AS cart_sessions,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_purchase_time IS NOT NULL
         AND first_cart_time >= first_view_time
         AND first_purchase_time >= first_cart_time
        THEN 1 ELSE 0 END) AS purchase_sessions
FROM brand_session_base
GROUP BY brand
""")

con.execute(f"""
COPY funnel_by_brand TO '{PROCESSED_DIR}/funnel_by_brand.parquet'
(FORMAT PARQUET)
""")

print("Computing funnel by category...")

con.execute("""
CREATE OR REPLACE TABLE funnel_by_category AS
WITH category_session_base AS (
    SELECT
        category_code,
        user_session,
        MIN(CASE WHEN event_type = 'view' THEN event_time END) AS first_view_time,
        MIN(CASE WHEN event_type = 'cart' THEN event_time END) AS first_cart_time,
        MIN(CASE WHEN event_type = 'purchase' THEN event_time END) AS first_purchase_time
    FROM events
    GROUP BY category_code, user_session
)
SELECT
    COALESCE(category_code, 'Unknown') AS category_code,
    SUM(CASE WHEN first_view_time IS NOT NULL THEN 1 ELSE 0 END) AS view_sessions,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_cart_time >= first_view_time
        THEN 1 ELSE 0 END) AS cart_sessions,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_purchase_time IS NOT NULL
         AND first_cart_time >= first_view_time
         AND first_purchase_time >= first_cart_time
        THEN 1 ELSE 0 END) AS purchase_sessions
FROM category_session_base
GROUP BY category_code
""")

con.execute(f"""
COPY funnel_by_category TO '{PROCESSED_DIR}/funnel_by_category.parquet'
(FORMAT PARQUET)
""")

print("Computing daily conversion...")

con.execute("""
CREATE OR REPLACE TABLE daily_conversion AS
WITH daily_session_events AS (
    SELECT
        event_date,
        user_session,
        MIN(CASE WHEN event_type = 'view' THEN event_time END) AS first_view_time,
        MIN(CASE WHEN event_type = 'cart' THEN event_time END) AS first_cart_time,
        MIN(CASE WHEN event_type = 'purchase' THEN event_time END) AS first_purchase_time
    FROM events
    GROUP BY event_date, user_session
)
SELECT
    event_date,
    SUM(CASE WHEN first_view_time IS NOT NULL THEN 1 ELSE 0 END) AS views,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_cart_time >= first_view_time
        THEN 1 ELSE 0 END) AS carts,
    SUM(CASE
        WHEN first_view_time IS NOT NULL
         AND first_cart_time IS NOT NULL
         AND first_purchase_time IS NOT NULL
         AND first_cart_time >= first_view_time
         AND first_purchase_time >= first_cart_time
        THEN 1 ELSE 0 END) AS purchases
FROM daily_session_events
GROUP BY event_date
ORDER BY event_date
""")

con.execute(f"""
COPY daily_conversion TO '{PROCESSED_DIR}/daily_conversion.parquet'
(FORMAT PARQUET)
""")

print("Pipeline completed successfully.")