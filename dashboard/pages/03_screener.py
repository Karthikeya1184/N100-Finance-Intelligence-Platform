import streamlit as st
import pandas as pd
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.screener.engine import ScreenerEngine



st.set_page_config(
    page_title="Financial Screener",
    layout="wide"
)

st.title("📈 Financial Screener")

engine = ScreenerEngine()

df = engine.load_data()

st.sidebar.header("Filter Companies")

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    -50.0,
    100.0,
    15.0,
    0.5
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    10.0,
    2.0,
    0.1
)

fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=0.0
)

rev = st.sidebar.slider(
    "Revenue CAGR 5Y (%)",
    -50.0,
    100.0,
    10.0,
    0.5
)

pat = st.sidebar.slider(
    "PAT CAGR 5Y (%)",
    -50.0,
    100.0,
    10.0,
    0.5
)

opm = st.sidebar.slider(
    "Operating Profit Margin (%)",
    -20.0,
    80.0,
    10.0,
    0.5
)

pe = st.sidebar.slider(
    "Maximum PE",
    0.0,
    150.0,
    25.0,
    1.0
)

pb = st.sidebar.slider(
    "Maximum PB",
    0.0,
    25.0,
    5.0,
    0.1
)

dividend = st.sidebar.slider(
    "Dividend Yield %",
    0.0,
    15.0,
    0.0,
    0.1
)

icr = st.sidebar.slider(
    "Interest Coverage",
    0.0,
    50.0,
    2.0,
    0.5
)

st.sidebar.divider()

st.sidebar.subheader("Preset Screeners")

quality = st.sidebar.button("🏆 Quality")

value = st.sidebar.button("💰 Value")

growth = st.sidebar.button("📈 Growth")

dividend_btn = st.sidebar.button("💵 Dividend")

debtfree = st.sidebar.button("🟢 Debt Free")

turnaround = st.sidebar.button("🚀 Turnaround")


# -----------------------------
# PRESET FILTERS
# -----------------------------

if quality:
    roe = 15
    de = 1
    fcf = 0
    rev = 10
    pat = 10

elif value:
    pe = 20
    pb = 3
    de = 2

elif growth:
    rev = 15
    pat = 20
    de = 2

elif dividend_btn:
    dividend = 2
    fcf = 0

elif debtfree:
    de = 0
    roe = 12

elif turnaround:
    rev = 10
    fcf = 0


# -----------------------------
# LIVE FILTERING
# -----------------------------

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"] >= roe
]

financial = filtered["broad_sector"] == "Financials"

filtered = filtered[
    financial |
    (filtered["debt_to_equity"] <= de)
]

filtered = filtered[
    filtered["free_cash_flow_cr"] >= fcf
]

filtered = filtered[
    filtered["revenue_cagr_5yr"] >= rev
]

filtered = filtered[
    filtered["pat_cagr_5yr"] >= pat
]

filtered = filtered[
    filtered["operating_profit_margin_pct"] >= opm
]

filtered = filtered[
    filtered["pe_ratio"] <= pe
]

filtered = filtered[
    filtered["pb_ratio"] <= pb
]

filtered = filtered[
    filtered["dividend_yield_pct"] >= dividend
]

filtered["interest_coverage"] = filtered[
    "interest_coverage"
].fillna(float("inf"))

filtered = filtered[
    filtered["interest_coverage"] >= icr
]

filtered = filtered.sort_values(
    "composite_quality_score",
    ascending=False
)


# -----------------------------
# RESULT COUNT
# -----------------------------

st.success(
    f"✅ {len(filtered)} companies match your filters."
)


# -----------------------------
# TABLE
# -----------------------------

columns = [

    "company_id",

    "company_name",

    "broad_sector",

    "return_on_equity_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "operating_profit_margin_pct",

    "composite_quality_score"

]

st.dataframe(

    filtered[columns],

    use_container_width=True,

    hide_index=True

)


# -----------------------------
# DOWNLOAD CSV
# -----------------------------

csv = filtered[columns].to_csv(index=False)

st.download_button(

    "⬇ Download CSV",

    csv,

    file_name="screener_output.csv",

    mime="text/csv"

)


# -----------------------------
# SUMMARY
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Companies",

    len(filtered)

)

c2.metric(

    "Average ROE",

    round(

        filtered["return_on_equity_pct"].mean(),

        2

    )

)

c3.metric(

    "Average Composite",

    round(

        filtered["composite_quality_score"].mean(),

        2

    )

)

c4.metric(

    "Average Revenue CAGR",

    round(

        filtered["revenue_cagr_5yr"].mean(),

        2

    )

)

st.divider()

st.caption("Sprint 4 • Day 24 • Financial Screener")