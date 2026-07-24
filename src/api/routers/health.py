from pathlib import Path
import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

START_TIME = time.time()


@router.get("/health")
def health():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

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
        "stock_prices",
    ]

    row_counts = {}

    for table in tables:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        row_counts[table] = cursor.fetchone()[0]

    conn.close()

    return {
        "status": "ok",
        "db_row_counts": row_counts,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "version": "1.0.0"
    }