import streamlit as st
from src.utils import load_parquet, safe_pct, format_pct
from src.charts import bar_chart

st.title("Segment Comparison")

segment_option = st.selectbox(
    "Choose segment",
    ["Brand", "Category"]
)

if segment_option == "Brand":
    df = load_parquet("funnel_by_brand.parquet").copy()
    segment_col = "brand"
else:
    df = load_parquet("funnel_by_category.parquet").copy()
    segment_col = "category_code"

df[segment_col] = df[segment_col].fillna("Unknown")
df = df[df["view_sessions"] > 100].copy()

df["view_to_cart_pct"] = df.apply(lambda x: safe_pct(x["cart_sessions"], x["view_sessions"]), axis=1)
df["cart_to_purchase_pct"] = df.apply(lambda x: safe_pct(x["purchase_sessions"], x["cart_sessions"]), axis=1)
df["view_to_purchase_pct"] = df.apply(lambda x: safe_pct(x["purchase_sessions"], x["view_sessions"]), axis=1)

top_n = st.slider("Top segments to display", min_value=5, max_value=25, value=10)

sort_metric = st.selectbox(
    "Sort by",
    ["view_to_purchase_pct", "view_to_cart_pct", "cart_to_purchase_pct", "view_sessions"]
)

top_df = df.sort_values(sort_metric, ascending=False).head(top_n)

st.plotly_chart(
    bar_chart(top_df, segment_col, sort_metric, f"Top {top_n} {segment_option}s by {sort_metric}"),
    use_container_width=True
)

display_df = top_df[[segment_col, "view_sessions", "cart_sessions", "purchase_sessions", "view_to_cart_pct", "cart_to_purchase_pct", "view_to_purchase_pct"]].copy()
display_df["view_to_cart_pct"] = display_df["view_to_cart_pct"].map(format_pct)
display_df["cart_to_purchase_pct"] = display_df["cart_to_purchase_pct"].map(format_pct)
display_df["view_to_purchase_pct"] = display_df["view_to_purchase_pct"].map(format_pct)

st.markdown("### Segment Performance Table")
st.dataframe(display_df, use_container_width=True)