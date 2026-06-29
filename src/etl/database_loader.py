import sqlite3
from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)

    datasets = load_all_files()

    load_order = [
        "companies",
        "sectors",
        "analysis",
        "documents",
        "prosandcons",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "stock_prices"
    ]

    audit = []

    for table in load_order:

        print(f"Loading {table}...")

        df = datasets[table]

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        audit.append({
            "table": table,
            "rows_loaded": len(df)
        })

        print(f"Loaded {len(df)} rows")

    audit_df = pd.DataFrame(audit)

    output = PROJECT_ROOT / "output"
    output.mkdir(exist_ok=True)

    audit_df.to_csv(
        output / "load_audit.csv",
        index=False
    )

    conn.close()

    print("\nDatabase created successfully.")


if __name__ == "__main__":
    create_database()