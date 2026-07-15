import yaml
import sqlite3
import pandas as pd


class ScreenerEngine:

    def __init__(self):

        with open(
            "src/screener/screener_config.yaml",
            "r"
        ) as f:

            self.config = yaml.safe_load(f)["filters"]

        self.conn = sqlite3.connect("db/nifty100.db")

    def load_data(self):

        ratios = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn
        )

        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn
        )

        market = pd.read_sql(
            """
            SELECT
                company_id,
                market_cap_crore,
                pe_ratio,
                pb_ratio,
                dividend_yield_pct
            FROM market_cap
            """,
            self.conn
        )

        companies = pd.read_sql(
            """
            SELECT
                id,
                company_name
            FROM companies
            """,
            self.conn
        )

        pnl = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                sales,
                net_profit
            FROM profitandloss
            """,
            self.conn
        )

        df = ratios.merge(
            sectors,
            on="company_id",
            how="left"
        )

        df = df.merge(
            market,
            on="company_id",
            how="left"
        )

        df = df.merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        df.drop(
            columns=["id"],
            inplace=True
        )

        df = df.merge(
            pnl[
                [
                    "company_id",
                    "year",
                    "sales",
                    "net_profit"
                ]
            ],
            on=[
                "company_id",
                "year"
            ],
            how="left"
        )

        return df

    def apply_filters(self):

        df = self.load_data()

        c = self.config

        df = df[df["return_on_equity_pct"] >= c["roe_min"]]

        financials = df["broad_sector"] == "Financials"

        df = df[
            financials |
            (df["debt_to_equity"] <= c["debt_to_equity_max"])
        ]

        df = df[df["free_cash_flow_cr"] >= c["free_cash_flow_min"]]

        df = df[df["revenue_cagr_5yr"] >= c["revenue_cagr_5yr_min"]]

        df = df[df["pat_cagr_5yr"] >= c["pat_cagr_5yr_min"]]

        df = df[
            df["operating_profit_margin_pct"]
            >= c["operating_profit_margin_min"]
        ]

        df = df[df["pe_ratio"] <= c["pe_max"]]

        df = df[df["pb_ratio"] <= c["pb_max"]]

        df = df[df["dividend_yield_pct"] >= c["dividend_yield_min"]]

        df["interest_coverage"] = df["interest_coverage"].fillna(float("inf"))

        df = df[df["interest_coverage"] >= c["interest_coverage_min"]]

        df = df[df["market_cap_crore"] >= c["market_cap_min"]]

        df = df[df["net_profit"] >= c["net_profit_min"]]

        df = df[df["eps_cagr_5yr"] >= c["eps_cagr_min"]]

        df = df[df["asset_turnover"] >= c["asset_turnover_min"]]

        df = df[df["sales"] >= c["sales_min"]]

        df = df.sort_values(
            "composite_quality_score",
            ascending=False
        )

        return df


if __name__ == "__main__":

    engine = ScreenerEngine()

    df = engine.apply_filters()

    print(df.head())

    print()

    print("Companies:", len(df))