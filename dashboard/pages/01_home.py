import streamlit as st
import plotly.express as px

from utils.db import *

st.title("🏠 Nifty 100 Analytics")

year = st.sidebar.selectbox(

    "Select Year",

    [

        "Mar 2019",

        "Mar 2020",

        "Mar 2021",

        "Mar 2022",

        "Mar 2023",

        "Mar 2024"

    ]

)

df = get_latest_ratios(year)

companies = get_companies()

sector = get_sectors()

col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric(

    "Average ROE",

    round(df["return_on_equity_pct"].mean(),2)

)

col2.metric(

    "Median D/E",

    round(df["debt_to_equity"].median(),2)

)

col3.metric(

    "Companies",

    len(companies)

)

col4.metric(

    "Median Revenue CAGR",

    round(df["revenue_cagr_5yr"].median(),2)

)

col5.metric(

    "Debt Free",

    len(df[df["debt_to_equity"]==0])

)

col6.metric(

    "Composite Avg",

    round(df["composite_quality_score"].mean(),2)

)

sector_count = sector.groupby(

    "broad_sector"

).size().reset_index(name="Count")

fig = px.pie(

    sector_count,

    names="broad_sector",

    values="Count",

    hole=.6,

    title="Sector Breakdown"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.subheader("Top Quality Companies")

top=df.sort_values(

    "composite_quality_score",

    ascending=False

).head(5)

st.dataframe(top)

st.divider()

st.caption(
    "N100 Finance Intelligence Platform | Sprint 4"
)