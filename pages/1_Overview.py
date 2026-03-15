import streamlit as st
from src.utils import load_parquet, safe_pct, format_number, format_pct
from src.charts import funnel_chart

st.title("Overview")
st.caption("Headline conversion metrics from the monthly ecommerce funnel")

summary_df = load_parquet("funnel_summary.parquet")
row = summary_df.iloc[0]

view_sessions = row["view_sessions"]
cart_sessions = row["cart_sessions"]
purchase_sessions = row["purchase_sessions"]

view_to_cart = safe_pct(cart_sessions, view_sessions)
cart_to_purchase = safe_pct(purchase_sessions, cart_sessions)
view_to_purchase = safe_pct(purchase_sessions, view_sessions)

st.markdown("""
<style>
.metric-card {
    background: #f5f5f7;
    border-radius: 22px;
    padding: 1rem 1.1rem;
    border: 1px solid rgba(0,0,0,0.04);
}
.metric-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #111827;
    margin-top: 0.15rem;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(5)
metrics = [
    ("View Sessions", format_number(view_sessions)),
    ("Cart Sessions", format_number(cart_sessions)),
    ("Purchase Sessions", format_number(purchase_sessions)),
    ("View → Cart", format_pct(view_to_cart)),
    ("View → Purchase", format_pct(view_to_purchase)),
]

for col, (label, value) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.plotly_chart(
    funnel_chart(view_sessions, cart_sessions, purchase_sessions),
    use_container_width=True
)

st.markdown("### Interpretation")
st.write(
    f"""
    FunnelSense shows a monthly top-of-funnel base of **{format_number(view_sessions)}** sessions with product views.
    From that base, **{format_number(cart_sessions)}** sessions progressed into cart activity and
    **{format_number(purchase_sessions)}** sessions completed a purchase.

    This translates to:
    - **{format_pct(view_to_cart)}** conversion from view to cart
    - **{format_pct(cart_to_purchase)}** conversion from cart to purchase
    - **{format_pct(view_to_purchase)}** full-funnel conversion from product view to transaction
    """
)