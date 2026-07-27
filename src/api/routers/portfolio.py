from pathlib import Path
import sqlite3

from fastapi import APIRouter

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

@router.get("/stats")
def portfolio_stats():

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            AVG(return_on_equity_pct) AS avg_roe,
            AVG(debt_to_equity) AS avg_de,
            AVG(free_cash_flow_cr) AS avg_fcf,
            AVG(revenue_cagr_5yr) AS avg_rev_cagr,
            AVG(pat_cagr_5yr) AS avg_pat_cagr,
            AVG(eps_cagr_5yr) AS avg_eps_cagr,
            AVG(asset_turnover) AS avg_asset_turnover,
            AVG(composite_quality_score) AS avg_quality

        FROM financial_ratios

        WHERE year = (
            SELECT MAX(year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = financial_ratios.company_id
        )
        """
    )

    stats = dict(cursor.fetchone())

    conn.close()

    return stats