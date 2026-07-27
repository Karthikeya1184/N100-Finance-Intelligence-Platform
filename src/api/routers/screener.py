from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@router.get("")
def screener(
    min_roe: float | None = Query(default=None),
    max_de: float | None = Query(default=None),
    min_fcf: float | None = Query(default=None),
    sector: str | None = Query(default=None),
    min_rev_cagr_5yr: float | None = Query(default=None),
    min_pat_cagr_5yr: float | None = Query(default=None),
    max_pe: float | None = Query(default=None),
):

    if min_roe is not None and min_roe < 0:
        raise HTTPException(status_code=400, detail="Invalid min_roe")

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT

        c.id,
        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr

    FROM companies c

    LEFT JOIN sectors s
        ON c.id=s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id

    WHERE fr.year=(
        SELECT MAX(year)
        FROM financial_ratios
        WHERE company_id=c.id
    )
    """

    params = []

    if sector:
        query += " AND s.broad_sector=?"
        params.append(sector)

    if min_roe is not None:
        query += " AND fr.return_on_equity_pct>=?"
        params.append(min_roe)

    if max_de is not None:
        query += " AND fr.debt_to_equity<=?"
        params.append(max_de)

    if min_fcf is not None:
        query += " AND fr.free_cash_flow_cr>=?"
        params.append(min_fcf)

    if min_rev_cagr_5yr is not None:
        query += " AND fr.revenue_cagr_5yr>=?"
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query += " AND fr.pat_cagr_5yr>=?"
        params.append(min_pat_cagr_5yr)

    query += " ORDER BY fr.return_on_equity_pct DESC"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(r) for r in rows]
