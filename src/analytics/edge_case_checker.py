import pandas as pd

from src.etl.loader import load_all_files


class EdgeCaseChecker:

    def __init__(self):

        data = load_all_files()

        self.pnl = data["profitandloss"]
        self.bs = data["balancesheet"]
        self.company = data["companies"]
        self.sector = data["sectors"]

    def run(self):

        df = self.pnl.merge(
            self.bs,
            on=["company_id", "year"],
            how="inner"
        )

        df = df.merge(
            self.company,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        df = df.merge(
            self.sector[["company_id", "broad_sector"]],
            on="company_id",
            how="left"
        )

        log = []

        for _, row in df.iterrows():

            capital = row["equity_capital"] + row["reserves"]

            if capital <= 0:
                continue

            roe = (row["net_profit"] / capital) * 100

            employed = capital + row["borrowings"]

            if employed <= 0:
                continue

            ebit = row["operating_profit"] + row["other_income"]

            roce = (ebit / employed) * 100

            source_roce = row["roce_percentage"]
            source_roe = row["roe_percentage"]

            category = ""

            if pd.notna(source_roce):

                diff = abs(roce - source_roce)

                if diff > 5:

                    category = "Formula Discrepancy"

                    if row["company_name"] == "TCS":
                        category = "Data Source Issue"

                    log.append([
                        row["company_id"],
                        row["year"],
                        "ROCE",
                        round(roce,2),
                        source_roce,
                        round(diff,2),
                        category
                    ])

            if pd.notna(source_roe):

                diff = abs(roe - source_roe)

                if diff > 5:

                    category = "Formula Discrepancy"

                    if row["company_name"] == "TCS":
                        category = "Data Source Issue"

                    log.append([
                        row["company_id"],
                        row["year"],
                        "ROE",
                        round(roe,2),
                        source_roe,
                        round(diff,2),
                        category
                    ])

        log_df = pd.DataFrame(
            log,
            columns=[
                "company_id",
                "year",
                "ratio",
                "computed",
                "source",
                "difference",
                "category"
            ]
        )

        log_df.to_csv(
            "output/ratio_edge_cases.log",
            index=False
        )

        print(log_df.head())

        print()

        print("ratio_edge_cases.log generated")


if __name__ == "__main__":

    EdgeCaseChecker().run()