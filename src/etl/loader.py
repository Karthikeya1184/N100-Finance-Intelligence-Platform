import pandas as pd

from src.etl.config import RAW_DATA, SUPPORTING_DATA

CORE_FILES = {
    "analysis": "analysis.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "companies": "companies.xlsx",
    "documents": "documents.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "prosandcons": "prosandcons.xlsx",
}

SUPPORT_FILES = {
    "financial_ratios": "financial_ratios.xlsx",
    "market_cap": "market_cap.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
}


def load_excel(path, header):
    """
    Load a single Excel file.
    """
    try:
        df = pd.read_excel(path, header=header)
        print(f"Loaded {path.name}")
        return df

    except Exception as e:
        print(f"Error reading {path.name}")
        print(e)
        return None


def load_all_files():
    """
    Load every dataset into a dictionary.
    """

    datasets = {}

    print("=" * 60)
    print("Loading Core Files")
    print("=" * 60)

    for name, file in CORE_FILES.items():
        file_path = RAW_DATA / file
        datasets[name] = load_excel(file_path, header=1)

        if datasets[name] is not None:
            print(f"{name:<20} {datasets[name].shape}")

    print()
    print("=" * 60)
    print("Loading Supporting Files")
    print("=" * 60)

    for name, file in SUPPORT_FILES.items():
        file_path = SUPPORTING_DATA / file
        datasets[name] = load_excel(file_path, header=0)

        if datasets[name] is not None:
            print(f"{name:<20} {datasets[name].shape}")

    return datasets


if __name__ == "__main__":
    load_all_files()