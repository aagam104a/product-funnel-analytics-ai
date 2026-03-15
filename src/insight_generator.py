from src.utils import safe_pct, format_number, format_pct

def generate_funnel_insights(summary_df, brand_df, category_df, daily_df):
    row = summary_df.iloc[0]

    view_users = row["view_users"]
    cart_users = row["cart_users"]
    purchase_users = row["purchase_users"]

    view_to_cart = safe_pct(cart_users, view_users)
    cart_to_purchase = safe_pct(purchase_users, cart_users)
    view_to_purchase = safe_pct(purchase_users, view_users)

    biggest_drop_stage = "view → cart"
    biggest_drop_value = 100 - view_to_cart

    if (100 - cart_to_purchase) > biggest_drop_value:
        biggest_drop_stage = "cart → purchase"
        biggest_drop_value = 100 - cart_to_purchase

    brand_df = brand_df.copy()
    brand_df["view_to_purchase_pct"] = brand_df.apply(
        lambda x: safe_pct(x["purchase_users"], x["view_users"]), axis=1
    )
    brand_df = brand_df[brand_df["view_users"] > 100].sort_values("view_to_purchase_pct", ascending=False)

    category_df = category_df.copy()
    category_df["view_to_purchase_pct"] = category_df.apply(
        lambda x: safe_pct(x["purchase_users"], x["view_users"]), axis=1
    )
    category_df = category_df[category_df["view_users"] > 100].sort_values("view_to_purchase_pct", ascending=False)

    top_brand = brand_df.iloc[0]["brand"] if not brand_df.empty else "N/A"
    weak_brand = brand_df.iloc[-1]["brand"] if not brand_df.empty else "N/A"

    top_category = category_df.iloc[0]["category_code"] if not category_df.empty else "N/A"
    weak_category = category_df.iloc[-1]["category_code"] if not category_df.empty else "N/A"

    insight = f"""
## Executive Summary

This dashboard analyzed a large-scale ecommerce clickstream funnel using the stages **view → cart → purchase**.

### Headline metrics
- Total users who viewed products: **{format_number(view_users)}**
- Total users who added to cart: **{format_number(cart_users)}**
- Total users who purchased: **{format_number(purchase_users)}**

### Conversion performance
- View → Cart conversion: **{format_pct(view_to_cart)}**
- Cart → Purchase conversion: **{format_pct(cart_to_purchase)}**
- Overall View → Purchase conversion: **{format_pct(view_to_purchase)}**

### Main finding
The largest funnel drop-off occurs at **{biggest_drop_stage}**, with an estimated drop-off of **{format_pct(biggest_drop_value)}**.

### Segment highlights
- Strongest brand by purchase conversion: **{top_brand}**
- Weakest brand by purchase conversion: **{weak_brand}**
- Strongest category by purchase conversion: **{top_category}**
- Weakest category by purchase conversion: **{weak_category}**

### Recommendation
Focus first on reducing friction at the **{biggest_drop_stage}** step. In practical terms, that means improving product-page intent capture if the issue is early-stage conversion, or improving checkout and purchase confidence if the issue is late-stage completion.

### Project value
This project demonstrates how a large raw event dataset can be transformed into decision-ready metrics using **DuckDB**, **Parquet**, and **Streamlit**.
"""
    return insight