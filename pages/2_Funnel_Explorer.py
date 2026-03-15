import streamlit as st
import pandas as pd
from src.utils import load_parquet, safe_pct, format_pct
from src.charts import line_chart

st.title("Funnel Explorer")

summary_df = load_parquet("funnel_summary.parquet")
daily_df = load_parquet("daily_conversion.parquet")

row = summary_df.iloc[0]

view_sessions = row["view_sessions"]
cart_sessions = row["cart_sessions"]
purchase_sessions = row["purchase_sessions"]

funnel_steps = pd.DataFrame({
    "stage": ["view", "cart", "purchase"],
    "sessions": [view_sessions, cart_sessions, purchase_sessions]
})

funnel_steps["conversion_from_previous"] = [
    100.0,
    safe_pct(cart_sessions, view_sessions),
    safe_pct(purchase_sessions, cart_sessions)
]

funnel_steps["drop_off_from_previous"] = [
    0.0,
    100 - safe_pct(cart_sessions, view_sessions),
    100 - safe_pct(purchase_sessions, cart_sessions)
]

st.markdown("### Funnel Stage Table")
display_df = funnel_steps.copy()
display_df["conversion_from_previous"] = display_df["conversion_from_previous"].map(format_pct)
display_df["drop_off_from_previous"] = display_df["drop_off_from_previous"].map(format_pct)
st.dataframe(display_df, use_container_width=True)

st.markdown("### Daily Funnel Activity")
daily_df = daily_df.sort_values("event_date")
st.plotly_chart(
    line_chart(
        daily_df,
        x_col="event_date",
        y_cols=["views", "carts", "purchases"],
        title="Daily Views, Carts, and Purchases"
    ),
    use_container_width=True
)