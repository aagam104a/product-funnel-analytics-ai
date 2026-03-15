import streamlit as st
import pandas as pd
from src.utils import load_parquet

st.set_page_config(
    page_title="FunnelSense",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 3.2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.05;
    margin-top: 0.2rem;
    margin-bottom: 0.7rem;
    color: #111827;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #6b7280;
    max-width: 820px;
    line-height: 1.7;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #111827;
    margin-top: 2rem;
    margin-bottom: 0.8rem;
}
.soft-card {
    background: #f5f5f7;
    padding: 1.2rem 1.3rem;
    border-radius: 22px;
    border: 1px solid rgba(0,0,0,0.04);
    min-height: 150px;
}
.soft-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.05rem;
    color: #111827;
}
.soft-card p {
    margin: 0;
    color: #6b7280;
    line-height: 1.6;
    font-size: 0.96rem;
}
.mini-label {
    font-size: 0.82rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.4rem;
    margin-bottom: 0.65rem;
}
.feature-pill {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    margin: 0.2rem 0.35rem 0.2rem 0;
    background: #f3f4f6;
    border-radius: 999px;
    font-size: 0.86rem;
    color: #374151;
    border: 1px solid rgba(0,0,0,0.05);
}
.data-card {
    background: #ffffff;
    border-radius: 22px;
    padding: 1rem 1rem 0.6rem 1rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="mini-label">Portfolio Project · Product Analytics · Funnel Intelligence</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="hero-title">FunnelSense</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">A polished ecommerce funnel intelligence app built on top of large-scale clickstream data. FunnelSense transforms 67M+ raw events into valid session-based conversion metrics, segment-level performance insights, and executive-ready summaries.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<span class="feature-pill">DuckDB pipeline</span>
<span class="feature-pill">67M+ events analyzed</span>
<span class="feature-pill">Session-based funnel</span>
<span class="feature-pill">Parquet-powered app</span>
<span class="feature-pill">Streamlit dashboard</span>
<span class="feature-pill">Portfolio-ready analytics</span>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">What this app shows</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="soft-card">
        <h4>Overview</h4>
        <p>Headline conversion KPIs, funnel scale, and purchase performance across the month.</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="soft-card">
        <h4>Funnel Explorer</h4>
        <p>Valid session-based progression across the customer journey: <strong>view → cart → purchase</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="soft-card">
        <h4>Segment Comparison</h4>
        <p>Compare conversion across brands and product categories to surface top and weak performers.</p>
    </div>
    """, unsafe_allow_html=True)

c4, c5 = st.columns(2)
with c4:
    st.markdown("""
    <div class="soft-card">
        <h4>Insights</h4>
        <p>Auto-generated business summaries turn raw conversion metrics into stakeholder-ready takeaways.</p>
    </div>
    """, unsafe_allow_html=True)
with c5:
    st.markdown("""
    <div class="soft-card">
        <h4>Architecture</h4>
        <p>See how a 9 GB CSV is processed with DuckDB and served as lightweight Parquet outputs for the web app.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Dataset snapshot</div>', unsafe_allow_html=True)

snippet = pd.DataFrame({
    "event_time": ["2019-11-01 00:00:00", "2019-11-01 00:00:00", "2019-11-01 00:00:01"],
    "event_type": ["view", "view", "view"],
    "product_id": [1003461, 5000088, 17302664],
    "category_code": ["electronics.smartphone", "appliances.sewing_machine", "Unknown"],
    "brand": ["xiaomi", "janome", "creed"],
    "price": [489.07, 293.65, 28.31],
    "user_session": ["4d3b30da...", "8e5f4f83...", "755422e7..."]
})

st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.dataframe(snippet, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Dataset and funnel</div>', unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown("""
    **Source schema**
    - `event_time`
    - `event_type`
    - `product_id`
    - `category_id`
    - `category_code`
    - `brand`
    - `price`
    - `user_id`
    - `user_session`

    **Funnel modeled**
    - `view`
    - `cart`
    - `purchase`
    """)

with right:
    st.info(
        "This landing page is designed as the cover frame for portfolio screenshots. "
        "Use the sidebar to explore the rest of the analysis."
    )