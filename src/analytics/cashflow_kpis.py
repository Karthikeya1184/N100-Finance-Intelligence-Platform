import sqlite3
from pathlib import Path

import pandas as pd


class CashFlowEngine:
    """
    Cash Flow KPI calculation engine.
    """

    @staticmethod
    def free_cash_flow(cfo, cfi):
        """
        Free Cash Flow = CFO + Investing Activity
        """
        if pd.isna(cfo) or pd.isna(cfi):
            return None
        return cfo + cfi

    @staticmethod
    def cfo_quality_score(cfo_list, pat_list):
        """
        Returns:
            (numeric_score, label)
        """

        ratios = []

        for cfo, pat in zip(cfo_list, pat_list):

            if pd.isna(cfo):
                continue

            if pd.isna(pat):
                continue

            if pat == 0:
                continue

            ratios.append(cfo / pat)

        if not ratios:
            return None, "Unavailable"

        avg = round(sum(ratios) / len(ratios), 2)

        if avg > 1:
            label = "High Quality"

        elif avg >= 0.5:
            label = "Moderate"

        else:
            label = "Accrual Risk"

        return avg, label

    @staticmethod
    def capex_intensity(cfi, sales):

        if pd.isna(cfi):
            return None, "Unavailable"

        if pd.isna(sales):
            return None, "Unavailable"

        if sales == 0:
            return None, "Unavailable"

        value = round(abs(cfi) / sales * 100, 2)

        if value < 3:
            label = "Asset Light"

        elif value <= 8:
            label = "Moderate"

        else:
            label = "Capital Intensive"

        return value, label

    @staticmethod
    def fcf_conversion(fcf, operating_profit):

        if pd.isna(fcf):
            return None

        if pd.isna(operating_profit):
            return None

        if operating_profit == 0:
            return None

        return round((fcf / operating_profit) * 100, 2)

    @staticmethod
    def distress_signal(cfo, cff):

        if pd.isna(cfo):
            return False

        if pd.isna(cff):
            return False

        return cfo < 0 and cff > 0

    @staticmethod
    def deleveraging(cff, latest_borrowings, previous_borrowings):

        if pd.isna(cff):
            return False

        if pd.isna(latest_borrowings):
            return False

        if pd.isna(previous_borrowings):
            return False

        return (
            cff < 0
            and latest_borrowings < previous_borrowings
        )

    @staticmethod
    def fcf_cagr(start_fcf, end_fcf, years=5):

        if start_fcf is None:
            return None

        if end_fcf is None:
            return None

        if start_fcf <= 0:
            return None

        if end_fcf <= 0:
            return None

        return round(
            (((end_fcf / start_fcf) ** (1 / years)) - 1) * 100,
            2,
        )
    

class CashFlowIntelligence:

    DB_PATH = "db/nifty100.db"

    def __init__(self):

        self.conn = sqlite3.connect(self.DB_PATH)

        Path("output").mkdir(exist_ok=True)

        self.engine = CashFlowEngine()

    def close(self):

        if self.conn:
            self.conn.close()

    def load_data(self):

        query = """
        SELECT

            cf.company_id,
            cf.year,

            cf.operating_activity,
            cf.investing_activity,
            cf.financing_activity,
            cf.net_cash_flow,

            pl.sales,
            pl.operating_profit,
            pl.net_profit,

            bs.borrowings,

            c.company_name,

            s.broad_sector

        FROM cashflow cf

        LEFT JOIN profitandloss pl

            ON cf.company_id = pl.company_id
            AND cf.year = pl.year

        LEFT JOIN balancesheet bs

            ON cf.company_id = bs.company_id
            AND cf.year = bs.year

        LEFT JOIN companies c

            ON cf.company_id = c.id

        LEFT JOIN sectors s

            ON cf.company_id = s.company_id

        ORDER BY
            cf.company_id,
            cf.year
        """

        df = pd.read_sql(query, self.conn)

        return df
    

    def prepare_company_data(self):

        df = self.load_data()

        companies = []

        for company_id, group in df.groupby("company_id"):

            group = group.copy()

            latest = group.iloc[-1]

            previous = (
                group.iloc[-2]
                if len(group) > 1
                else latest
            )

            fcf_series = []

            for _, row in group.iterrows():

                fcf = self.engine.free_cash_flow(

                    row["operating_activity"],
                    row["investing_activity"]

                )

                fcf_series.append(fcf)

            quality_score, quality_label = self.engine.cfo_quality_score(

                group["operating_activity"].tolist(),

                group["net_profit"].tolist()

            )

            latest_fcf = fcf_series[-1]

            capex_pct, capex_label = self.engine.capex_intensity(

                latest["investing_activity"],

                latest["sales"]

            )

            if len(fcf_series) >= 6:

                fcf_cagr = self.engine.fcf_cagr(

                    fcf_series[-6],

                    fcf_series[-1],

                    5

                )

            else:

                fcf_cagr = None

            companies.append({

                "company_id": company_id,

                "company_name": latest["company_name"],

                "sector": latest["broad_sector"],

                "quality_score": quality_score,

                "quality_label": quality_label,

                "capex_pct": capex_pct,

                "capex_label": capex_label,

                "latest_cfo": latest["operating_activity"],

                "latest_cfi": latest["investing_activity"],

                "latest_cff": latest["financing_activity"],

                "latest_fcf": latest_fcf,

                "latest_pat": latest["net_profit"],

                "operating_profit": latest["operating_profit"],

                "borrowings": latest["borrowings"],

                "previous_borrowings": previous["borrowings"],

                "fcf_cagr": fcf_cagr

            })

        return pd.DataFrame(companies)
    

    def generate_reports(self):

        df = self.prepare_company_data()

        final_rows = []

        distress_rows = []

        for _, row in df.iterrows():

            distress = self.engine.distress_signal(

                row["latest_cfo"],

                row["latest_cff"]

            )

            deleveraging = self.engine.deleveraging(

                row["latest_cff"],

                row["borrowings"],

                row["previous_borrowings"]

            )

            fcf_conversion = self.engine.fcf_conversion(

                row["latest_fcf"],

                row["operating_profit"]

            )

            if distress:

                capital_label = "Distress"

            elif deleveraging:

                capital_label = "Debt Reduction"

            elif row["quality_label"] == "High Quality":

                capital_label = "Shareholder Returns"

            else:

                capital_label = "Balanced"

            final_rows.append({

                "company_id": row["company_id"],

                "company_name": row["company_name"],

                "sector": row["sector"],

                "cfo_quality_score": row["quality_score"],

                "cfo_quality_label": row["quality_label"],

                "capex_intensity_pct": row["capex_pct"],

                "capex_label": row["capex_label"],

                "fcf_cagr_5yr": row["fcf_cagr"],

                "fcf_conversion_pct": fcf_conversion,

                "distress_flag": distress,

                "deleveraging_flag": deleveraging,

                "capital_allocation_label": capital_label

            })

            if distress:

                distress_rows.append({

                    "company_id": row["company_id"],

                    "company_name": row["company_name"],

                    "CFO": row["latest_cfo"],

                    "CFF": row["latest_cff"],

                    "latest_net_profit": row["latest_pat"]

                })

        final_df = pd.DataFrame(final_rows)

        distress_df = pd.DataFrame(distress_rows)

        final_df.to_excel(

            "output/cashflow_intelligence.xlsx",

            index=False

        )

        distress_df.to_csv(

            "output/distress_alerts.csv",

            index=False

        )

        print("\n" + "=" * 60)
        print("DAY 31 COMPLETED")
        print("=" * 60)

        print(f"Companies Processed : {len(final_df)}")
        print(f"Distress Alerts     : {len(distress_df)}")

        print("\nFiles Generated")

        print("✓ output/cashflow_intelligence.xlsx")

        print("✓ output/distress_alerts.csv")


if __name__ == "__main__":

    app = CashFlowIntelligence()

    try:

        app.generate_reports()

    finally:

        app.close()