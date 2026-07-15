import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

st.title("🏭 Sector Analysis")

conn = sqlite3.connect("db/nifty100.db")

sector_df = pd.read_sql("""
SELECT DISTINCT
    broad_sector
FROM sectors
ORDER BY broad_sector
""", conn)

sector = st.selectbox(

    "Select Sector",

    sector_df["broad_sector"]

)

query = f"""
SELECT

    c.company_name,

    s.broad_sector,

    s.sub_sector,

    fr.return_on_equity_pct,

    mc.market_cap_crore,

    pl.sales

FROM financial_ratios fr

LEFT JOIN companies c

ON fr.company_id=c.id

LEFT JOIN sectors s

ON fr.company_id=s.company_id

LEFT JOIN market_cap mc

ON fr.company_id=mc.company_id

LEFT JOIN profitandloss pl

ON fr.company_id=pl.company_id

AND fr.year=pl.year

WHERE s.broad_sector='{sector}'

"""

df = pd.read_sql(query, conn)

conn.close()

latest = df.groupby(

    "company_name"

).last().reset_index()

fig = px.scatter(

    latest,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    title="Sector Bubble Chart"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.subheader("Sector Median KPIs")

median = latest.groupby(

    "sub_sector"

)[

    [

        "sales",

        "return_on_equity_pct",

        "market_cap_crore"

    ]

].median().reset_index()

bar = px.bar(

    median,

    x="sub_sector",

    y="return_on_equity_pct",

    color="sub_sector",

    title="Median ROE by Sub Sector"

)

st.plotly_chart(

    bar,

    use_container_width=True

)

st.dataframe(

    latest,

    use_container_width=True,

    hide_index=True

)