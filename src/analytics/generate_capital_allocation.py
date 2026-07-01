import pandas as pd

from src.analytics.cashflow_kpis import CashFlowEngine
from src.etl.loader import load_all_files


def generate():

    data = load_all_files()

    cashflow = data["cashflow"]

    rows = []

    for _, row in cashflow.iterrows():

        signs, pattern = CashFlowEngine.capital_pattern(

            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"]

        )

        rows.append({

            "company_id": row["company_id"],

            "year": row["year"],

            "cfo_sign": signs[0],

            "cfi_sign": signs[1],

            "cff_sign": signs[2],

            "pattern_label": pattern

        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "output/capital_allocation.csv",
        index=False
    )

    print(df.head())

    print()

    print("capital_allocation.csv generated")


if __name__ == "__main__":

    generate()