from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# GET /market-cap/{ticker}
# ============================================================


@router.get("/{ticker}")
def get_market_cap_history(ticker: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM market_cap
        WHERE company_id = ?
        ORDER BY year
        """,
        (ticker.upper(),),
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Market cap history not found")

    return [dict(row) for row in rows]
