import streamlit as st
from src.utils import load_parquet, safe_pct, format_number, format_pct

st.title("Insights")
st.caption("Executive-ready interpretation layer for the funnel analysis")

summary_df = load_parquet("funnel_summary.parquet")
brand_df = load_parquet("funnel_by_brand.parquet").copy()
category_df = load_parquet("funnel_by_category.parquet").copy()
daily_df = load_parquet("daily_conversion.parquet").copy()

row = summary_df.iloc[0]

view_sessions = row["view_sessions"]
cart_sessions = row["cart_sessions"]
purchase_sessions = row["purchase_sessions"]

view_to_cart = safe_pct(cart_sessions, view_sessions)
cart_to_purchase = safe_pct(purchase_sessions, cart_sessions)
view_to_purchase = safe_pct(purchase_sessions, view_sessions)

drop_view_cart = 100 - view_to_cart
drop_cart_purchase = 100 - cart_to_purchase

biggest_drop_stage = "View → Cart"
biggest_drop_value = drop_view_cart
if drop_cart_purchase > drop_view_cart:
    biggest_drop_stage = "Cart → Purchase"
    biggest_drop_value = drop_cart_purchase

brand_df["brand"] = brand_df["brand"].fillna("Unknown")
brand_df = brand_df[brand_df["view_sessions"] > 100].copy()
brand_df["view_to_purchase_pct"] = brand_df.apply(
    lambda x: safe_pct(x["purchase_sessions"], x["view_sessions"]), axis=1
)
brand_df = brand_df.sort_values("view_to_purchase_pct", ascending=False)

category_df["category_code"] = category_df["category_code"].fillna("Unknown")
category_df = category_df[category_df["view_sessions"] > 100].copy()
category_df["view_to_purchase_pct"] = category_df.apply(
    lambda x: safe_pct(x["purchase_sessions"], x["view_sessions"]), axis=1
)
category_df = category_df.sort_values("view_to_purchase_pct", ascending=False)

top_brand = brand_df.iloc[0] if not brand_df.empty else None
bottom_brand = brand_df.iloc[-1] if not brand_df.empty else None
top_category = category_df.iloc[0] if not category_df.empty else None
bottom_category = category_df.iloc[-1] if not category_df.empty else None

st.markdown("""
<style>
.ai-card {
    background: #f5f5f7;
    border-radius: 22px;
    padding: 1.25rem 1.3rem;
    border: 1px solid rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.ai-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.5rem;
}
.ai-body {
    color: #4b5563;
    line-height: 1.7;
    font-size: 0.97rem;
}
.big-kpi {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: 22px;
    padding: 1rem 1.2rem;
}
.big-kpi-label {
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
}
.big-kpi-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #111827;
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="big-kpi">
        <div class="big-kpi-label">View to Cart</div>
        <div class="big-kpi-value">{format_pct(view_to_cart)}</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="big-kpi">
        <div class="big-kpi-label">Cart to Purchase</div>
        <div class="big-kpi-value">{format_pct(cart_to_purchase)}</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="big-kpi">
        <div class="big-kpi-label">View to Purchase</div>
        <div class="big-kpi-value">{format_pct(view_to_purchase)}</div>
    </div>
    """, unsafe_allow_html=True)

summary_text = f"""
FunnelSense analyzed **{format_number(view_sessions)}** sessions with product views, **{format_number(cart_sessions)}** sessions with cart activity,
and **{format_number(purchase_sessions)}** sessions that completed a purchase.

The funnel shows that **{format_pct(view_to_cart)}** of view sessions progressed to cart,
while **{format_pct(cart_to_purchase)}** of cart sessions completed purchase.
The full-funnel conversion from **view to purchase** is **{format_pct(view_to_purchase)}**.

The largest source of friction appears at **{biggest_drop_stage}**, where the estimated drop-off is **{format_pct(biggest_drop_value)}**.
"""

st.markdown(f"""
<div class="ai-card">
    <div class="ai-title">Executive Summary</div>
    <div class="ai-body">{summary_text}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    strength_text = "Not enough qualifying brand/category data to compute highlights."
    if top_brand is not None and top_category is not None:
        strength_text = f"""
        The strongest brand in the benchmark set is **{top_brand['brand']}**, with a view-to-purchase conversion of
        **{format_pct(top_brand['view_to_purchase_pct'])}**.

        The strongest category is **{top_category['category_code']}**, converting at
        **{format_pct(top_category['view_to_purchase_pct'])}**.

        These segments can serve as benchmarks for strong product intent and stronger merchandising performance.
        """
    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-title">What is working well</div>
        <div class="ai-body">{strength_text}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    risk_text = "Not enough qualifying brand/category data to compute risk segments."
    if bottom_brand is not None and bottom_category is not None:
        risk_text = f"""
        The weakest brand in the benchmark set is **{bottom_brand['brand']}**, with a view-to-purchase conversion of
        **{format_pct(bottom_brand['view_to_purchase_pct'])}**.

        The weakest category is **{bottom_category['category_code']}**, converting at
        **{format_pct(bottom_category['view_to_purchase_pct'])}**.

        These segments may indicate weaker merchandising, lower purchase intent, pricing friction, or lower-quality traffic.
        """
    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-title">Where the risk is</div>
        <div class="ai-body">{risk_text}</div>
    </div>
    """, unsafe_allow_html=True)

rec_text = f"""
1. Prioritize the **{biggest_drop_stage}** step because it accounts for the largest loss of sessions.  
2. Benchmark weaker segments against top-performing brands and categories.  
3. Focus on product page quality, cart confidence, and purchase friction reduction.  
4. A next production upgrade would be source-level segmentation and experiment analysis.
"""
st.markdown(f"""
<div class="ai-card">
    <div class="ai-title">Recommended next actions</div>
    <div class="ai-body">{rec_text}</div>
</div>
""", unsafe_allow_html=True)

with st.expander("How these insights were generated"):
    st.write("""
    These insights are generated from the processed funnel summary tables created by the DuckDB pipeline.
    The app currently uses deterministic business logic on top of:
    - session-based funnel conversion
    - drop-off analysis
    - segment-level performance
    - trend summaries

    This can later be upgraded to a full LLM-powered narrative layer.
    """)