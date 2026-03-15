import streamlit as st

st.title("About FunnelSense")
st.caption("How the project works end to end")

st.markdown("""
## Project summary

**FunnelSense AI** is a product analytics portfolio project built to analyze large-scale ecommerce clickstream data and convert raw behavioral events into clear business decisions.

The project starts with a **9 GB CSV** containing more than **67 million events** from an online retail environment.  
Instead of loading that raw file directly into a dashboard, the data is first transformed through a lightweight analytics pipeline and then served as compact, app-ready summary tables.

## Core business question

Where are users dropping off in the ecommerce funnel, and which segments are performing best or worst?

## Funnel used

The funnel modeled in this project is:

**view → cart → purchase**

That means the analysis focuses on:
- product discovery intent
- add-to-cart behavior
- completed purchases

## Architecture

### 1. Raw event data
The original source file lives in:

`data/raw/2019-Nov.csv`

Each row is a user-product event.

### 2. DuckDB processing layer
The raw CSV is processed using **DuckDB**, which is ideal for fast analytical queries over large local files.

This stage:
- parses timestamps
- standardizes the event table
- computes funnel-level aggregates
- computes segment-level performance tables

### 3. Parquet output layer
The pipeline writes compact summary files into:

`data/processed/`

Including:
- `funnel_summary.parquet`
- `funnel_by_brand.parquet`
- `funnel_by_category.parquet`
- `daily_conversion.parquet`

### 4. Streamlit presentation layer
The web app reads only the processed summary files, which keeps the user experience fast and deployment-friendly.

## Why this design matters

This project demonstrates a realistic analytics workflow:

- ingest high-volume clickstream data
- transform it into decision-ready metrics
- expose those metrics through a business-facing application
- generate plain-English insight summaries on top of the analysis

## Tech stack

- **Python**
- **DuckDB**
- **Parquet**
- **Streamlit**
- **Plotly**

## What this project demonstrates

- product analytics thinking
- funnel design and conversion analysis
- scalable data processing for large files
- segment-level performance analysis
- stakeholder-friendly narrative reporting
- deployable analytics app architecture

## Portfolio positioning

This project is best positioned as:

**Scalable Funnel Analytics App with AI Insight Layer**

A clean way to describe it on a resume:

> Built FunnelSense AI, a portfolio-ready ecommerce analytics application that processed 67M+ clickstream events with DuckDB, transformed raw data into Parquet-based summary tables, and delivered funnel insights, segment comparisons, and AI-style executive summaries through a live Streamlit dashboard.
""")