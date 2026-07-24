from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)



# ============================================================
# GET /companies
# ============================================================

@router.get("")
def get_companies(

    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None),

):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT

        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        c.roe_percentage AS roe_pct,
        c.roce_percentage AS roce_pct

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    WHERE 1=1
    """

    params = []

    if sector:

        query += " AND s.broad_sector = ?"

        params.append(sector)

    if market_cap_category:

        query += " AND s.market_cap_category = ?"

        params.append(market_cap_category)

    if search:

        query += """
        AND (
            c.company_name LIKE ?
            OR c.id LIKE ?
        )
        """

        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY c.company_name"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ============================================================
# GET /companies/{ticker}
# ============================================================

@router.get("/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT

        c.*,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score,
        fr.year

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE c.id = ?

    AND fr.year = (
        SELECT MAX(year)
        FROM financial_ratios
        WHERE company_id = c.id
    )
    """

    cursor.execute(query, (ticker.upper(),))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return dict(row)



# ============================================================
# GET /companies/{ticker}/pl
# ============================================================

@router.get("/{ticker}/pl")
def get_profit_and_loss(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    """

    params = [ticker.upper()]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ============================================================
# GET /companies/{ticker}/bs
# ============================================================

@router.get("/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
    """

    params = [ticker.upper()]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ============================================================
# GET /companies/{ticker}/cashflow
# ============================================================

@router.get("/{ticker}/cashflow")
def get_cashflow(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
    """

    params = [ticker.upper()]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ============================================================
# GET /companies/{ticker}/ratios
# ============================================================

@router.get("/{ticker}/ratios")
def get_ratios(
    ticker: str,
    year: str | None = Query(default=None),
):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker.upper()]

    if year:

        query += " AND year = ?"

        params.append(year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ============================================================
# GET /companies/{ticker}/tearsheet
# ============================================================

@router.get("/{ticker}/tearsheet")
def download_tearsheet(ticker: str):

    pdf_path = (
        PROJECT_ROOT
        / "output"
        / "tearsheets"
        / f"{ticker.upper()}_tearsheet.pdf"
    )

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker.upper()}_tearsheet.pdf",
    )