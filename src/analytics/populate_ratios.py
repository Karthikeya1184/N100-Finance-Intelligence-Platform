import sqlite3
import pandas as pd

from src.etl.loader import load_all_files
from src.analytics.ratios import RatioEngine
from src.analytics.cashflow_kpis import CashFlowEngine
from src.analytics.cagr import (
    revenue_cagr_5yr,
    pat_cagr_5yr,
    eps_cagr_5yr
)


DB_PATH = "db/nifty100.db"


def populate():

    data = load_all_files()

    pnl = data["profitandloss"]
    bs = data["balancesheet"]
    cf = data["cashflow"]

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    rows = []

    merged = pnl.merge(
        bs,
        on=["company_id", "year"],
        how="left"
    )

    merged = merged.merge(
        cf,
        on=["company_id", "year"],
        how="left"
    )

    merged = merged.sort_values(
        ["company_id", "year"]
    )

    for company in merged["company_id"].unique():

        company_df = merged[
            merged["company_id"] == company
        ].copy()

        company_df = company_df.sort_values("year")

        for _, row in company_df.iterrows():

            npm = RatioEngine.net_profit_margin(
                row["net_profit"],
                row["sales"]
            )

            opm = RatioEngine.operating_profit_margin(
                row["operating_profit"],
                row["sales"]
            )

            roe = RatioEngine.roe(
                row["net_profit"],
                row["equity_capital"],
                row["reserves"]
            )

            debt_equity = RatioEngine.debt_to_equity(
                row["borrowings"],
                row["equity_capital"],
                row["reserves"]
            )

            interest_cov = RatioEngine.interest_coverage(
                row["operating_profit"],
                row["other_income"],
                row["interest"]
            )

            asset_turnover = RatioEngine.asset_turnover(
                row["sales"],
                row["total_assets"]
            )

            fcf = CashFlowEngine.free_cash_flow(
                row["operating_activity"],
                row["investing_activity"]
            )

            capex = CashFlowEngine.capex_intensity(
                row["investing_activity"],
                row["sales"]
            )[0]

            revenue5, _ = revenue_cagr_5yr(
                company_df["sales"].tolist()
            )

            pat5, _ = pat_cagr_5yr(
                company_df["net_profit"].tolist()
            )

            eps5, _ = eps_cagr_5yr(
                company_df["eps"].tolist()
            )

            score = 0

            if roe is not None and roe > 15:
                score += 1

            if debt_equity is not None and debt_equity < 1:
                score += 1

            if interest_cov is not None and interest_cov > 3:
                score += 1

            rows.append({

                "company_id": row["company_id"],

                "year": row["year"],

                "net_profit_margin_pct": npm,

                "operating_profit_margin_pct": opm,

                "return_on_equity_pct": roe,

                "debt_to_equity": debt_equity,

                "interest_coverage": interest_cov,

                "asset_turnover": asset_turnover,

                "free_cash_flow_cr": fcf,

                "capex_cr": capex,

                "earnings_per_share": row["eps"],

                "book_value_per_share":
                    row["book_value"] if "book_value" in row else None,

                "dividend_payout_ratio_pct":
                    row["dividend_payout"],

                "total_debt_cr":
                    row["borrowings"],

                "cash_from_operations_cr":
                    row["operating_activity"],

                "revenue_cagr_5yr":
                    revenue5,

                "pat_cagr_5yr":
                    pat5,

                "eps_cagr_5yr":
                    eps5,

                "composite_quality_score":
                    score

            })