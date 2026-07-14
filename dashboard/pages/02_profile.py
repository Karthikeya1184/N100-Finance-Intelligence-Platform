import streamlit as st
import plotly.express as px

from utils.db import *

st.title("🏢 Company Profile")

companies = get_companies()

ticker = st.selectbox(
    "Search Company",
    sorted(companies["id"].tolist())
)

profile = get_company_profile(ticker)

if profile.empty:
    st.warning("Ticker not found — please try another.")
    st.stop()

info = profile.iloc[0]

st.header(info["company_name"])

st.write(info["about_company"])

col1, col2, col3 = st.columns(3)

col1.metric("Sector", info["broad_sector"])
col2.metric("Sub Sector", info["sub_sector"])
col3.metric("Ticker", info["id"])

ratio = get_ratios(ticker)

if ratio.empty:
    st.warning("No ratio data available.")
    st.stop()

latest = ratio.iloc[-1]

k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

k1.metric("ROE", latest["return_on_equity_pct"])
k2.metric("Net Profit Margin", latest["net_profit_margin_pct"])
k3.metric("Debt / Equity", latest["debt_to_equity"])

k4.metric("Revenue CAGR 5Y", latest["revenue_cagr_5yr"])
k5.metric("Free Cash Flow", latest["free_cash_flow_cr"])
k6.metric("Composite Score", latest["composite_quality_score"])

pl = get_pl(ticker)

if not pl.empty:

    fig = px.bar(
        pl,
        x="year",
        y=["sales", "net_profit"],
        barmode="group",
        title="Revenue vs Net Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

fig2 = px.line(
    ratio,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="ROE Trend"
)

st.plotly_chart(fig2, use_container_width=True)

pros = get_pros_cons(ticker)

st.subheader("Pros & Cons")

if pros.empty:
    st.info("No Pros / Cons available.")
else:
    for _, row in pros.iterrows():

        sentiment = str(row.iloc[2]).lower()
        text = row.iloc[3]

        if sentiment == "pro":
            st.success("✔ " + text)
        else:
            st.error("✖ " + text)