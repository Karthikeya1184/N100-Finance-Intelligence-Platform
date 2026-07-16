import sqlite3
import pandas as pd
import re
from pathlib import Path


class AnalysisParser:

    DB = "db/nifty100.db"

    def __init__(self):

        self.conn = sqlite3.connect(self.DB)

        self.output = Path("output")

        self.output.mkdir(exist_ok=True)

        self.pattern = re.compile(
            r"(\d+)\s*Years?:?\s*([\d.]+)%"
        )

    def load_data(self):

        query = """
        SELECT
            company_id,
            compounded_sales_growth,
            compounded_profit_growth,
            stock_price_cagr,
            roe
        FROM analysis
        """

        return pd.read_sql(query, self.conn)

    def parse_metric(
        self,
        company_id,
        metric_name,
        text
    ):

        if pd.isna(text):

            return [], False

        text = str(text).strip()

        matches = self.pattern.findall(text)

        if not matches:

            return [], False

        parsed = []

        for period, value in matches:

            parsed.append({

                "company_id": company_id,

                "metric_type": metric_name,

                "period_years": int(period),

                "value_pct": float(value)

            })

        return parsed, True
    



    def parse(self):

        df = self.load_data()

        parsed_rows = []

        failed_rows = []

        metrics = [
            "compounded_sales_growth",
            "compounded_profit_growth",
            "stock_price_cagr",
            "roe"
        ]

        for _, row in df.iterrows():

            company = row["company_id"]

            for metric in metrics:

                text = row[metric]

                values, success = self.parse_metric(
                    company,
                    metric,
                    text
                )

                if success:

                    parsed_rows.extend(values)

                else:

                    failed_rows.append({

                        "company_id": company,

                        "metric_type": metric,

                        "raw_text": text

                    })

        # ---------------------------------
        # Parsed DataFrame
        # ---------------------------------

        parsed_df = pd.DataFrame(
            parsed_rows,
            columns=[
                "company_id",
                "metric_type",
                "period_years",
                "value_pct"
            ]
        )

        # ---------------------------------
        # Failure DataFrame
        # ---------------------------------

        failure_df = pd.DataFrame(
            failed_rows,
            columns=[
                "company_id",
                "metric_type",
                "raw_text"
            ]
        )

        parsed_df.to_csv(

            self.output / "analysis_parsed.csv",

            index=False

        )

        failure_df.to_csv(

            self.output / "parse_failures.csv",

            index=False

        )

        print()

        print("=" * 60)

        print("Analysis Parsing Completed")

        print("=" * 60)

        print(f"Companies Processed : {len(df)}")

        print(f"Parsed Rows         : {len(parsed_df)}")

        print(f"Failed Rows         : {len(failure_df)}")

        print()

        return parsed_df
    


    def validate(self, parsed_df):

        if parsed_df.empty:

            print("No parsed rows available for validation.")

            review = pd.DataFrame(
                columns=[
                    "company_id",
                    "metric_type",
                    "value_pct",
                    "expected_value",
                    "difference_pct"
                ]
            )

            review.to_csv(
                self.output / "manual_review.csv",
                index=False
            )

            return review

        ratios = pd.read_sql(
            """
            SELECT
                company_id,
                revenue_cagr_5yr,
                pat_cagr_5yr,
                return_on_equity_pct
            FROM financial_ratios
            """,
            self.conn
        )

        compare = parsed_df.merge(
            ratios,
            on="company_id",
            how="left"
        )

        compare["expected_value"] = None

        compare.loc[
            compare["metric_type"] == "compounded_sales_growth",
            "expected_value"
        ] = compare["revenue_cagr_5yr"]

        compare.loc[
            compare["metric_type"] == "compounded_profit_growth",
            "expected_value"
        ] = compare["pat_cagr_5yr"]

        compare.loc[
            compare["metric_type"] == "roe",
            "expected_value"
        ] = compare["return_on_equity_pct"]

        compare["difference_pct"] = (
            compare["value_pct"] -
            compare["expected_value"]
        ).abs()

        review = compare[
            compare["difference_pct"] > 5
        ].copy()

        review.to_csv(
            self.output / "manual_review.csv",
            index=False
        )

        print("=" * 60)
        print("Validation Completed")
        print("=" * 60)
        print(f"Rows Checked : {len(compare)}")
        print(f"Manual Review: {len(review)}")
        print()

        return review

    def close(self):

        self.conn.close()




if __name__ == "__main__":

    parser = AnalysisParser()

    parsed = parser.parse()

    review = parser.validate(parsed)

    parser.close()

    print("=" * 60)
    print("DAY 29 NLP PARSER COMPLETED")
    print("=" * 60)
    print()

    print(f"Parsed Rows        : {len(parsed)}")
    print(f"Manual Review Rows : {len(review)}")
    print()

    print("Generated Files")
    print("✓ output/analysis_parsed.csv")
    print("✓ output/parse_failures.csv")
    print("✓ output/manual_review.csv")