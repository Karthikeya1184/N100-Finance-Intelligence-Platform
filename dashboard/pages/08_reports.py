import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Annual Reports",
    layout="wide"
)

st.title("📄 Annual Reports")

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

reports = pd.read_sql(f"""
SELECT
    Year,
    Annual_Report
FROM documents
WHERE company_id='{company_id}'
ORDER BY Year DESC
""", conn)

conn.close()

if reports.empty:

    st.error("No reports available.")

else:

    st.subheader(company)
for _, row in reports.iterrows():

    year = row["Year"]

    link = row["Annual_Report"]

    col1, col2 = st.columns([2, 6])

    col1.write(year)

    if pd.isna(link) or str(link).strip() == "":

        col2.error("🔴 Report unavailable")

    else:

        col2.link_button(
            f"📄 Annual Report {year}",
            link
        )

st.divider()

st.caption("Sprint 4 • Day 25 • Annual Reports")