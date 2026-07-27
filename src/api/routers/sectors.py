from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@router.get("")
def get_sectors():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT

        s.broad_sector,

        COUNT(DISTINCT c.id) AS company_count,

        AVG(fr.return_on_equity_pct) AS median_roe,

        NULL AS median_pe,

        AVG(fr.debt_to_equity) AS median_de

    FROM sectors s

    JOIN companies c
        ON s.company_id = c.id

    JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE fr.year = (
        SELECT MAX(year)
        FROM financial_ratios
        WHERE company_id = c.id
    )

    GROUP BY s.broad_sector

    ORDER BY s.broad_sector
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ============================================================
# GET /sectors/{sector}/companies
# ============================================================


@router.get("/{sector}/companies")
def get_sector_companies(sector: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if the sector exists
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sectors
        WHERE broad_sector = ?
        """,
        (sector,),
    )

    if cursor.fetchone()[0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Sector not found")

    query = """
    SELECT

        c.id,
        c.company_name,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.composite_quality_score

    FROM companies c

    JOIN sectors s
        ON c.id = s.company_id

    JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE s.broad_sector = ?

      AND fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = c.id
      )

    ORDER BY fr.composite_quality_score DESC
    """

    cursor.execute(query, (sector,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
