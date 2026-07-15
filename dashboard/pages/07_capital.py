import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(
    page_title="Capital Allocation",
    layout="wide"
)

st.title("💰 Capital Allocation Map")

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT

    c.company_name,

    fr.company_id,

    fr.free_cash_flow_cr,

    fr.capex_cr,

    fr.cash_from_operations_cr,

    fr.composite_quality_score,

    CASE

        WHEN fr.free_cash_flow_cr > 0
             AND fr.capex_cr > 0
             THEN 'Growth Reinvestment'

        WHEN fr.free_cash_flow_cr > 0
             AND fr.capex_cr <= 0
             THEN 'Cash Generator'

        WHEN fr.free_cash_flow_cr < 0
             AND fr.capex_cr > 0
             THEN 'Expansion Phase'

        WHEN fr.free_cash_flow_cr < 0
             AND fr.capex_cr <= 0
             THEN 'Weak Capital Allocation'

        ELSE 'Other'

    END AS capital_pattern

FROM financial_ratios fr

LEFT JOIN companies c

ON fr.company_id = c.id
"""

df = pd.read_sql(query, conn)

conn.close()

latest = df.groupby("company_id").last().reset_index()

fig = px.treemap(

    latest,

    path=["capital_pattern", "company_name"],

    values="composite_quality_score",

    color="free_cash_flow_cr",

    title="Capital Allocation Treemap"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

patterns = sorted(latest["capital_pattern"].unique())

selected = st.selectbox(

    "Select Capital Allocation Pattern",

    patterns

)

filtered = latest[

    latest["capital_pattern"] == selected

]

st.subheader(

    f"{selected} Companies"

)

st.dataframe(

    filtered[

        [

            "company_name",

            "free_cash_flow_cr",

            "capex_cr",

            "cash_from_operations_cr",

            "composite_quality_score"

        ]

    ],

    use_container_width=True,

    hide_index=True

)

c1, c2, c3 = st.columns(3)

c1.metric(

    "Companies",

    len(filtered)

)

c2.metric(

    "Average FCF",

    round(

        filtered["free_cash_flow_cr"].mean(),

        2

    )

)

c3.metric(

    "Average Score",

    round(

        filtered["composite_quality_score"].mean(),

        2

    )

)