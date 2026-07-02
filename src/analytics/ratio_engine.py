import pandas as pd

from src.etl.loader import load_all_files
from src.analytics.ratio_calculator import RatioCalculator
from src.analytics.db_writer import DatabaseWriter


class RatioEngineRunner:

    def __init__(self):

        self.data = load_all_files()

        self.pnl = self.data["profitandloss"]

        self.bs = self.data["balancesheet"]

        self.cf = self.data["cashflow"]

        self.company = self.data["companies"]

    def merge_data(self):

        merged = self.pnl.merge(

            self.bs,

            on=["company_id", "year"],

            how="left"

        )

        merged = merged.merge(

            self.cf,

            on=["company_id", "year"],

            how="left"

        )

        merged = merged.rename(

            columns={

                "id_x": "id"

            }

        )

        return merged

    def build_ratio_table(self):

        merged = self.merge_data()

        merged = merged.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

        final_rows = []

        companies = merged["company_id"].unique()

        print()

        print("=" * 60)

        print("Building Ratio Table")

        print("=" * 60)

        for company in companies:

            company_df = merged[
                merged["company_id"] == company
            ].copy()

            company_df = company_df.sort_values("year")

            company_master = self.company[
                self.company["id"] == company
            ]

            if len(company_master) == 0:
                continue

            company_master = company_master.iloc[0]

            for _, row in company_df.iterrows():

                ratios = RatioCalculator.calculate(

                    row,

                    company_df,

                    company_master

                )

                ratios["company_id"] = row["company_id"]

                ratios["year"] = row["year"]

                final_rows.append(ratios)

        df = pd.DataFrame(final_rows)

        print()

        print(df.head())

        print()

        print(f"Rows Created : {len(df)}")

        return df
    


if __name__ == "__main__":

    engine = RatioEngineRunner()

    df = engine.build_ratio_table()

    DatabaseWriter.write(df)

    print(df.shape)