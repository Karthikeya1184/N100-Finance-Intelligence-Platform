import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


class Validator:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def run(self):

        print("=" * 60)
        print("Running Validation")
        print("=" * 60)

        tables = [
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

        summary = []

        for table in tables:

            query = f"SELECT COUNT(*) FROM {table}"

            rows = pd.read_sql(query, self.conn)

            count = rows.iloc[0, 0]

            print(f"{table:<20} {count}")

            summary.append({
                "table": table,
                "rows": count
            })

        output = PROJECT_ROOT / "output"

        output.mkdir(exist_ok=True)

        pd.DataFrame(summary).to_csv(
            output / "validation_summary.csv",
            index=False
        )

        self.conn.close()

        print("\nValidation Completed Successfully")


if __name__ == "__main__":
    Validator().run()