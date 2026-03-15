import pandas as pd
import streamlit as st
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

@st.cache_data
def load_parquet(file_name: str) -> pd.DataFrame:
    path = PROCESSED_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_parquet(path)

def safe_pct(numerator, denominator):
    if denominator in [0, None]:
        return 0.0
    return (numerator / denominator) * 100

def format_number(x):
    try:
        return f"{int(x):,}"
    except Exception:
        return str(x)

def format_pct(x):
    return f"{x:.2f}%"