import sqlite3
from pathlib import Path

import pandas as pd


class ProsConsGenerator:

    DB = "db/nifty100.db"

    def __init__(self):

        self.conn = sqlite3.connect(self.DB)

        Path("output").mkdir(exist_ok=True)

    def load_data(self):

        query = """
        SELECT

            fr.company_id,

            c.company_name,

            c.roce_percentage,

            c.roe_percentage,

            fr.return_on_equity_pct,

            fr.net_profit_margin_pct,

            fr.operating_profit_margin_pct,

            fr.debt_to_equity,

            fr.interest_coverage,

            fr.asset_turnover,

            fr.free_cash_flow_cr,

            fr.dividend_payout_ratio_pct,

            fr.total_debt_cr,

            fr.revenue_cagr_5yr,

            fr.pat_cagr_5yr,

            fr.eps_cagr_5yr,

            fr.composite_quality_score,

            mc.dividend_yield_pct

        FROM financial_ratios fr

        LEFT JOIN companies c
            ON fr.company_id = c.id

        LEFT JOIN market_cap mc
            ON fr.company_id = mc.company_id
            AND fr.year = mc.year
        """

        return pd.read_sql(query, self.conn)

    def confidence(self, value, threshold):

        if pd.isna(value):

            return 0

        if value >= threshold * 2:

            return 100

        score = int(

            60 +

            ((value - threshold) / threshold) * 40

        )

        return max(60, min(score, 100))
    

    def generate(self):

        df = self.load_data()

        print(f"Rows Loaded : {len(df)}")

        output = []

        for _, row in df.iterrows():

            company = row["company_id"]

            # -------------------------
            # PRO 1
            # -------------------------

            if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] > 20:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P1",

                    "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

                    "confidence_pct": self.confidence(
                        row["return_on_equity_pct"],
                        20
                    )

                })

            # -------------------------
            # PRO 2
            # -------------------------

            if pd.notna(row["free_cash_flow_cr"]) and row["free_cash_flow_cr"] > 0:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P2",

                    "text": "Strong positive free cash flow indicates healthy business fundamentals.",

                    "confidence_pct": 85

                })

            # -------------------------
            # PRO 3
            # -------------------------

            if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] == 0:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P3",

                    "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",

                    "confidence_pct": 95

                })

            # -------------------------
            # PRO 4
            # -------------------------

            if pd.notna(row["revenue_cagr_5yr"]) and row["revenue_cagr_5yr"] > 15:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P4",

                    "text": "Revenue growing above 15% CAGR over five years reflects strong business momentum.",

                    "confidence_pct": self.confidence(
                        row["revenue_cagr_5yr"],
                        15
                    )

                })

            # -------------------------
            # PRO 5
            # -------------------------

            if pd.notna(row["operating_profit_margin_pct"]) and row["operating_profit_margin_pct"] > 25:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P5",

                    "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline.",

                    "confidence_pct": self.confidence(
                        row["operating_profit_margin_pct"],
                        25
                    )

                })

            # -------------------------
            # PRO 6
            # -------------------------

            if pd.notna(row["pat_cagr_5yr"]) and row["pat_cagr_5yr"] > 20:

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P6",

                    "text": "Net profit compounding above 20% over five years creates significant shareholder value.",

                    "confidence_pct": self.confidence(
                        row["pat_cagr_5yr"],
                        20
                    )

                })

        return output
    

            # -------------------------
            # PRO 7
            # -------------------------

            
        if (
                pd.notna(row["interest_coverage"])
                and row["interest_coverage"] > 10
            ) or (
                pd.notna(row["debt_to_equity"])
                and row["debt_to_equity"] == 0
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P7",

                    "text": "Very high interest coverage reflects minimal financial stress from debt servicing.",

                    "confidence_pct": 90

                })

            # -------------------------
            # PRO 8
            # -------------------------

        if (
                pd.notna(row["dividend_yield_pct"])
                and pd.notna(row["free_cash_flow_cr"])
                and row["dividend_yield_pct"] > 2
                and row["free_cash_flow_cr"] > 0
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P8",

                    "text": "Healthy dividend yield supported by positive free cash flow.",

                    "confidence_pct": 88

                })

            # -------------------------
            # PRO 9
            # -------------------------

        if (
                pd.notna(row["eps_cagr_5yr"])
                and row["eps_cagr_5yr"] > 15
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P9",

                    "text": "Strong EPS growth indicates improving earnings quality.",

                    "confidence_pct": self.confidence(
                        row["eps_cagr_5yr"],
                        15
                    )

                })

            # -------------------------
            # PRO 10
            # -------------------------

        if (
                pd.notna(row["asset_turnover"])
                and row["asset_turnover"] > 1
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P10",

                    "text": "Efficient asset utilisation supports healthy operational performance.",

                    "confidence_pct": 82

                })

            # -------------------------
            # PRO 11
            # -------------------------

        if (
                pd.notna(row["pat_cagr_5yr"])
                and pd.notna(row["revenue_cagr_5yr"])
                and row["pat_cagr_5yr"] > row["revenue_cagr_5yr"]
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P11",

                    "text": "Profit growth exceeding revenue growth indicates improving operating leverage.",

                    "confidence_pct": 86

                })

            # -------------------------
            # PRO 12
            # -------------------------

        if (
                pd.notna(row["debt_to_equity"])
                and pd.notna(row["free_cash_flow_cr"])
                and row["debt_to_equity"] < 0.5
                and row["free_cash_flow_cr"] > 0
            ):

                output.append({

                    "company_id": company,

                    "type": "Pro",

                    "rule_id": "P12",

                    "text": "Low leverage combined with positive free cash flow reflects strong financial quality.",

                    "confidence_pct": 87

                }) 



            # -------------------------
            # CON 1
            # -------------------------

        if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] > 2:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C1",

                    "text": f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated and warrants monitoring.",

                    "confidence_pct": self.confidence(
                        row["debt_to_equity"],
                        2
                    )

                })

            # -------------------------
            # CON 2
            # -------------------------

        if pd.notna(row["free_cash_flow_cr"]) and row["free_cash_flow_cr"] < 0:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C2",

                    "text": "Negative free cash flow raises concern about cash generation quality.",

                    "confidence_pct": 85

                })

            # -------------------------
            # CON 3
            # -------------------------

        if pd.notna(row["operating_profit_margin_pct"]) and row["operating_profit_margin_pct"] < 10:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C3",

                    "text": "Operating profit margin is low, indicating pricing pressure or weak cost efficiency.",

                    "confidence_pct": 78

                })

            # -------------------------
            # CON 4
            # -------------------------

        if pd.notna(row["net_profit_margin_pct"]) and row["net_profit_margin_pct"] < 0:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C4",

                    "text": "Company reported a negative net profit margin in the latest financial year.",

                    "confidence_pct": 95

                })

            # -------------------------
            # CON 5
            # -------------------------

        if pd.notna(row["revenue_cagr_5yr"]) and row["revenue_cagr_5yr"] < 5:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C5",

                    "text": "Revenue growth below 5% over five years suggests limited business momentum.",

                    "confidence_pct": 80

                })

            # -------------------------
            # CON 6
            # -------------------------

        if pd.notna(row["interest_coverage"]) and row["interest_coverage"] < 1.5:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C6",

                    "text": "Interest coverage below 1.5x indicates elevated debt servicing risk.",

                    "confidence_pct": 95

                })

            # -------------------------
            # CON 7
            # -------------------------

        if pd.notna(row["dividend_payout_ratio_pct"]) and row["dividend_payout_ratio_pct"] > 100:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C7",

                    "text": "Dividend payout ratio above 100% may not be sustainable.",

                    "confidence_pct": 92

                })

            # -------------------------
            # CON 8
            # -------------------------

        if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] > 1:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C8",

                    "text": "High debt-to-equity ratio suggests increasing financial leverage risk.",

                    "confidence_pct": 78

                })

            # -------------------------
            # CON 9
            # -------------------------

        if pd.notna(row["eps_cagr_5yr"]) and row["eps_cagr_5yr"] < 5:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C9",

                    "text": "Weak EPS growth indicates limited earnings momentum.",

                    "confidence_pct": 82

                })

            # -------------------------
            # CON 10
            # -------------------------

        if pd.notna(row["roce_percentage"]) and row["roce_percentage"] < 10:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C10",

                    "text": "Return on capital employed below 10% suggests inefficient capital utilisation.",

                    "confidence_pct": 90

                })

            # -------------------------
            # CON 11
            # -------------------------

        if pd.notna(row["total_debt_cr"]) and row["total_debt_cr"] > 10000:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C11",

                    "text": "High debt level may reduce financial flexibility and increase refinancing risk.",

                    "confidence_pct": 76

                })

            # -------------------------
            # CON 12
            # -------------------------

        if pd.notna(row["composite_quality_score"]) and row["composite_quality_score"] < 50:

                output.append({

                    "company_id": company,

                    "type": "Con",

                    "rule_id": "C12",

                    "text": "Low composite quality score indicates below-average overall business quality.",

                    "confidence_pct": 80

                })

        print(f"Generated Records : {len(output)}")

        return output


    def export(self):

        output = self.generate()

        columns = [
            "company_id",
            "type",
            "rule_id",
            "text",
            "confidence_pct"
        ]

        df = pd.DataFrame(output, columns=columns)

        companies = self.load_data()["company_id"].unique()

        for company in companies:

            company_rows = df[df["company_id"] == company]

            # Ensure at least one Pro
            if not (company_rows["type"] == "Pro").any():

                df.loc[len(df)] = {
                    "company_id": company,
                    "type": "Pro",
                    "rule_id": "P_DEFAULT",
                    "text": "Company demonstrates stable business fundamentals.",
                    "confidence_pct": 65
                }

            # Ensure at least one Con
            if not (company_rows["type"] == "Con").any():

                df.loc[len(df)] = {
                    "company_id": company,
                    "type": "Con",
                    "rule_id": "C_DEFAULT",
                    "text": "Business performance should continue to be monitored.",
                    "confidence_pct": 65
                }

        df = df[df["confidence_pct"] >= 60]

        df = df.sort_values(
            ["company_id", "type", "rule_id"]
        ).reset_index(drop=True)

        output_file = "output/pros_cons_generated.csv"

        df.to_csv(
            output_file,
            index=False
        )

        print()
        print("=" * 60)
        print("Pros & Cons Generation Completed")
        print("=" * 60)
        print(f"Companies Covered : {df['company_id'].nunique()}")
        print(f"Rows Generated    : {len(df)}")
        print(f"Output File       : {output_file}")
        print("=" * 60)

        return df

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    generator = ProsConsGenerator()

    try:

        df = generator.export()

        print()
        print("=" * 60)
        print("DAY 30 COMPLETED SUCCESSFULLY")
        print("=" * 60)

    finally:

        generator.close()                       