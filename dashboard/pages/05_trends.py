import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("📈 Trend Analysis")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("""
SELECT
    id,
    company_name
FROM companies
ORDER BY company_name
""", conn)

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

df = pd.read_sql(f"""
SELECT
    year,
    return_on_equity_pct,
    net_profit_margin_pct,
    revenue_cagr_5yr,
    pat_cagr_5yr,
    asset_turnover,
    free_cash_flow_cr
FROM financial_ratios
WHERE company_id='{company_id}'
ORDER BY year
""", conn)

metrics = st.multiselect(
    "Select up to 3 Metrics",
    [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "asset_turnover",
        "free_cash_flow_cr"
    ],
    default=["return_on_equity_pct"]
)

if len(metrics) > 3:

    st.warning("Select a maximum of 3 metrics.")

    st.stop()

plot_df = df[["year"] + metrics]

fig = px.line(
    plot_df,
    x="year",
    y=metrics,
    markers=True,
    title="10-Year Trend Analysis"
)

for metric in metrics:

    yoy = df[metric].pct_change() * 100

    for x, y, p in zip(df["year"], df[metric], yoy):

        if pd.notna(p):

            fig.add_annotation(
                x=x,
                y=y,
                text=f"{p:.1f}%",
                showarrow=False,
                font=dict(size=9)
            )

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    plot_df,
    use_container_width=True
)

conn.close()