from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# GET /peers/{group_name}
# ============================================================


@router.get("/{group_name}")
def get_peer_group(group_name: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check whether the peer group exists
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM peer_groups
        WHERE peer_group = ?
        """,
        (group_name,),
    )

    if cursor.fetchone()[0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Peer group not found")

    query = """
    SELECT

        c.id,
        c.company_name,

        pg.peer_group,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score

    FROM peer_groups pg

    JOIN companies c
        ON pg.company_id = c.id

    JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE pg.peer_group = ?

      AND fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = c.id
      )

    ORDER BY fr.composite_quality_score DESC
    """

    cursor.execute(query, (group_name,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ============================================================
# GET /companies/{ticker}/peers/compare
# ============================================================


@router.get("/companies/{ticker}/peers/compare")
def compare_with_peers(ticker: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find the peer group for this company
    cursor.execute(
        """
        SELECT peer_group
        FROM peer_groups
        WHERE company_id = ?
        """,
        (ticker.upper(),),
    )

    peer = cursor.fetchone()

    if peer is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Peer group not found")

    peer_group = peer["peer_group"]

    # Company metrics
    cursor.execute(
        """
        SELECT
            return_on_equity_pct,
            debt_to_equity,
            free_cash_flow_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,
            asset_turnover,
            composite_quality_score
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        (ticker.upper(),),
    )

    company = dict(cursor.fetchone())

    # Peer average
    cursor.execute(
        """
        SELECT
            AVG(fr.return_on_equity_pct) AS return_on_equity_pct,
            AVG(fr.debt_to_equity) AS debt_to_equity,
            AVG(fr.free_cash_flow_cr) AS free_cash_flow_cr,
            AVG(fr.revenue_cagr_5yr) AS revenue_cagr_5yr,
            AVG(fr.pat_cagr_5yr) AS pat_cagr_5yr,
            AVG(fr.eps_cagr_5yr) AS eps_cagr_5yr,
            AVG(fr.asset_turnover) AS asset_turnover,
            AVG(fr.composite_quality_score) AS composite_quality_score
        FROM peer_groups pg
        JOIN financial_ratios fr
            ON pg.company_id = fr.company_id
        WHERE pg.peer_group = ?
          AND fr.year = (
                SELECT MAX(year)
                FROM financial_ratios
                WHERE company_id = fr.company_id
          )
        """,
        (peer_group,),
    )

    peer_average = dict(cursor.fetchone())

    # Benchmark company
    cursor.execute(
        """
        SELECT
            company_id,
            composite_quality_score
        FROM peer_groups pg
        JOIN financial_ratios fr
            ON pg.company_id = fr.company_id
        WHERE pg.peer_group = ?
          AND fr.year = (
                SELECT MAX(year)
                FROM financial_ratios
                WHERE company_id = fr.company_id
          )
        ORDER BY composite_quality_score DESC
        LIMIT 1
        """,
        (peer_group,),
    )

    benchmark = dict(cursor.fetchone())

    conn.close()

    return {
        "peer_group": peer_group,
        "company": company,
        "peer_average": peer_average,
        "benchmark": benchmark,
    }
