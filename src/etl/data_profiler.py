from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW = PROJECT_ROOT / "data" / "raw"
SUPPORT = PROJECT_ROOT / "data" / "supporting"


def profile_excel(file_path, header=0):

    print("=" * 80)
    print(file_path.name)
    print("=" * 80)

    df = pd.read_excel(file_path, header=header)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nCOLUMN INFORMATION\n")

    summary = pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str),
        "Missing": df.isna().sum().values,
        "Unique": df.nunique().values
    })

    print(summary)

    print("\nFIRST FIVE ROWS\n")

    print(df.head())

    return summary


def profile_all():

    print("\nCORE FILES\n")

    core_files = [
        ("analysis.xlsx", 1),
        ("balancesheet.xlsx", 1),
        ("cashflow.xlsx", 1),
        ("companies.xlsx", 1),
        ("documents.xlsx", 1),
        ("profitandloss.xlsx", 1),
        ("prosandcons.xlsx", 1),
    ]

    for file_name, header in core_files:
        profile_excel(RAW / file_name, header)

    print("\nSUPPORT FILES\n")

    support_files = [
        ("financial_ratios.xlsx", 0),
        ("market_cap.xlsx", 0),
        ("peer_groups.xlsx", 0),
        ("sectors.xlsx", 0),
        ("stock_prices.xlsx", 0),
    ]

    for file_name, header in support_files:
        profile_excel(SUPPORT / file_name, header)


if __name__ == "__main__":
    profile_all()