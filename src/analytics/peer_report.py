import sqlite3
import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font


DB = "db/nifty100.db"
OUTPUT = "output/peer_comparison.xlsx"


conn = sqlite3.connect(DB)

peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)

groups = pd.read_sql("SELECT * FROM peer_groups", conn)

companies = pd.read_sql(
    "SELECT id AS company_id, company_name FROM companies",
    conn
)

conn.close()


with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:

    for group in groups["peer_group_name"].dropna().unique():

        group_companies = groups[
            groups["peer_group_name"] == group
        ]["company_id"]

        df = peer[
            peer["company_id"].isin(group_companies)
        ]

        values = df.pivot_table(
            index=["company_id", "year"],
            columns="metric",
            values="value"
        )

        pct = df.pivot_table(
            index=["company_id", "year"],
            columns="metric",
            values="percentile_rank"
        )

        pct.columns = [
            c + "_pct"
            for c in pct.columns
        ]

        final = values.join(pct)

        final.reset_index(inplace=True)

        final = final.merge(
            companies,
            on="company_id",
            how="left"
        )

        cols = ["company_id", "company_name", "year"] + [
            c for c in final.columns
            if c not in [
                "company_id",
                "company_name",
                "year"
            ]
        ]

        final = final[cols]

        # Summary row
        numeric = final.select_dtypes(include="number")
        median = numeric.median()

        summary = {
            col: ""
            for col in final.columns
        }

        summary["company_id"] = "MEDIAN"

        for c in median.index:
            summary[c] = round(median[c], 2)

        final = pd.concat(
            [
                final,
                pd.DataFrame([summary])
            ],
            ignore_index=True
        )

        final.to_excel(
            writer,
            sheet_name=group[:31],
            index=False
        )