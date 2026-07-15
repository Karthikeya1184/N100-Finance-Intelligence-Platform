import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("👥 Peer Comparison Dashboard")

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

peer_groups = pd.read_sql("""
SELECT DISTINCT peer_group_name
FROM peer_groups
ORDER BY peer_group_name
""", conn)

group = st.sidebar.selectbox(
    "Select Peer Group",
    peer_groups["peer_group_name"]
)

companies = pd.read_sql(f"""
SELECT
    p.company_id,
    c.company_name,
    p.is_benchmark
FROM peer_groups p
LEFT JOIN companies c
ON p.company_id=c.id
WHERE p.peer_group_name='{group}'
ORDER BY c.company_name
""", conn)

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies[
    companies["company_name"] == company
]["company_id"].iloc[0]

benchmark = companies[
    companies["is_benchmark"] == 1
]

if benchmark.empty:
    benchmark_company = None
else:
    benchmark_company = benchmark.iloc[0]["company_id"]

metrics = [

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "asset_turnover",

    "composite_quality_score"

]

latest = pd.read_sql(f"""
SELECT *
FROM financial_ratios
WHERE company_id='{company_id}'
ORDER BY year DESC
LIMIT 1
""", conn)

peer_ids = tuple(companies["company_id"])

peer = pd.read_sql(f"""
SELECT *
FROM financial_ratios
WHERE company_id IN {peer_ids}
""", conn)

peer_avg = peer.groupby(
    "company_id"
).last()

peer_mean = peer_avg[
    metrics
].mean()




# --------------------------------------------------------
# RADAR CHART
# --------------------------------------------------------

if latest.empty:
    st.warning("No financial ratio data available.")
    st.stop()

company_values = latest.iloc[0][metrics].fillna(0).tolist()
peer_values = peer_mean.fillna(0).tolist()

labels = [
    "ROE",
    "NPM",
    "D/E",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
    "Asset Turnover",
    "Composite"
]

company_values.append(company_values[0])
peer_values.append(peer_values[0])
labels.append(labels[0])

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=company_values,

        theta=labels,

        fill="toself",

        name=company

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=peer_values,

        theta=labels,

        line=dict(dash="dash"),

        name="Peer Average"

    )

)

fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True

        )

    ),

    showlegend=True,

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# --------------------------------------------------------
# BENCHMARK COMPANY
# --------------------------------------------------------

st.divider()

st.subheader("Benchmark Company")

if benchmark_company is None:

    st.info("No benchmark company assigned.")

else:

    benchmark_name = companies[
        companies["company_id"] == benchmark_company
    ]["company_name"].iloc[0]

    st.success(

        f"🏆 Benchmark : {benchmark_name}"

    )

# --------------------------------------------------------
# KPI TABLE
# --------------------------------------------------------

peer_latest = peer.sort_values(

    "year"

).groupby(

    "company_id"

).last().reset_index()

peer_latest = peer_latest.merge(

    companies[[
        "company_id",
        "company_name",
        "is_benchmark"
    ]],

    on="company_id",

    how="left"

)

display = peer_latest[[
    "company_name",
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "asset_turnover",
    "composite_quality_score",
    "is_benchmark"
]]

def highlight(row):

    if row["is_benchmark"] == 1:

        return [

            "background-color:#FFD54F"

        ] * len(row)

    return [

        ""

    ] * len(row)

st.subheader("Peer KPI Comparison")

st.dataframe(

    display.style.apply(

        highlight,

        axis=1

    ),

    use_container_width=True

)

# --------------------------------------------------------
# SUMMARY
# --------------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(

    "Peer Companies",

    len(display)

)

c2.metric(

    "Average Composite",

    round(

        display["composite_quality_score"].mean(),

        2

    )

)

c3.metric(

    "Average ROE",

    round(

        display["return_on_equity_pct"].mean(),

        2

    )

)

st.divider()

st.caption(

    "Sprint 4 • Day 24 • Peer Comparison Dashboard"

)

conn.close()