import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np


class ValuationEngine:

    def __init__(self):

        self.db_path = "db/nifty100.db"

        self.output_path = Path("output")

        self.output_path.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)

    def load_data(self):

        query = """
        SELECT

            mc.company_id,

            c.company_name,

            s.broad_sector,

            mc.year,

            mc.market_cap_crore,

            mc.enterprise_value_crore,

            mc.pe_ratio,

            mc.pb_ratio,

            mc.ev_ebitda,

            mc.dividend_yield_pct,

            fr.free_cash_flow_cr

        FROM market_cap mc

        LEFT JOIN companies c

        ON mc.company_id = c.id

        LEFT JOIN sectors s

        ON mc.company_id = s.company_id

        LEFT JOIN financial_ratios fr

        ON mc.company_id = fr.company_id

        """

        df = pd.read_sql(query, self.conn)

        return df

    def latest_year(self, df):

        return int(df["year"].max())

    def latest_data(self):

        df = self.load_data()

        latest = df[
            df["year"] == self.latest_year(df)
        ].copy()

        return latest

    def five_year_median_pe(self):

        history = self.load_data()

        median = (

            history

            .groupby("company_id")["pe_ratio"]

            .median()

            .reset_index()

            .rename(

                columns={

                    "pe_ratio":"5yr_median_PE"

                }

            )

        )

        return median
    
    def calculate(self):

        latest = self.latest_data()

        latest["FCF_yield_pct"] = np.where(
            latest["market_cap_crore"] > 0,
            (latest["free_cash_flow_cr"] / latest["market_cap_crore"]) * 100,
            np.nan
        )
        sector_median = (
            latest
            .groupby("broad_sector")["pe_ratio"]
            .median()
            .reset_index()
            .rename(
                columns={
                    "pe_ratio": "sector_median_PE"
                }
            )
        )

        latest = latest.merge(
            sector_median,
            on="broad_sector",
            how="left"
        )

        latest["PE_vs_sector_median_pct"] = np.where(
            latest["sector_median_PE"] > 0,
            (
                latest["pe_ratio"]
                /
                latest["sector_median_PE"]
            ) * 100,
            np.nan
        )

        latest["flag"] = "Fair"

        latest.loc[
            latest["pe_ratio"]
            >
            latest["sector_median_PE"] * 1.5,
            "flag"
        ] = "Caution"

        latest.loc[
            latest["pe_ratio"]
            <
            latest["sector_median_PE"] * 0.7,
            "flag"
        ] = "Discount"

        median = self.five_year_median_pe()

        latest = latest.merge(
            median,
            on="company_id",
            how="left"
        )

        latest.rename(
            columns={
                "broad_sector": "sector",
                "pe_ratio": "P/E",
                "pb_ratio": "P/B",
                "ev_ebitda": "EV/EBITDA"
            },
            inplace=True
        )

        summary = latest[
            [
                "company_id",
                "company_name",
                "sector",
                "P/E",
                "P/B",
                "EV/EBITDA",
                "FCF_yield_pct",
                "5yr_median_PE",
                "PE_vs_sector_median_pct",
                "flag"
            ]
        ].copy()

        return summary

    def export(self):

        summary = self.calculate()

        summary.to_excel(
            self.output_path / "valuation_summary.xlsx",
            index=False
        )

        flags = summary[
            summary["flag"].isin(
                ["Caution", "Discount"]
            )
        ].copy()

        flags.to_csv(
            self.output_path / "valuation_flags.csv",
            index=False
        )

        print("=" * 60)
        print("VALUATION MODULE COMPLETED")
        print("=" * 60)

        print(f"Companies Processed : {len(summary)}")
        print(f"Caution Companies  : {(summary['flag']=='Caution').sum()}")
        print(f"Discount Companies : {(summary['flag']=='Discount').sum()}")
        print(f"Fair Companies     : {(summary['flag']=='Fair').sum()}")

        print("\nOutput Files")

        print("✓ output/valuation_summary.xlsx")

        print("✓ output/valuation_flags.csv")

        self.conn.close()

        return summary

       
    
if __name__ == "__main__":

    engine = ValuationEngine()

    engine.export()