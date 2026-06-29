import pandas as pd

from pathlib import Path

from src.etl.config import RAW_DATA, SUPPORTING_DATA

CORE_FILES = {

    "analysis": "analysis.xlsx",

    "balancesheet": "balancesheet.xlsx",

    "cashflow": "cashflow.xlsx",

    "companies": "companies.xlsx",

    "documents": "documents.xlsx",

    "profitandloss": "profitandloss.xlsx",

    "prosandcons": "prosandcons.xlsx"

}

SUPPORT_FILES = {

    "financial_ratios": "financial_ratios.xlsx",

    "market_cap": "market_cap.xlsx",

    "peer_groups": "peer_groups.xlsx",

    "sectors": "sectors.xlsx",

    "stock_prices": "stock_prices.xlsx"

}

def load_excel(path, header):

    try:

        df = pd.read_excel(path, header=header)

        print(f"Loaded {path.name}")

        return df

    except Exception as e:

        print(f"Error reading {path.name}")

        print(e)

        return None