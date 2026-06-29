import sqlite3

DB = "db/nifty100.db"


def get_columns(table):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table})")

    cols = [row[1] for row in cur.fetchall()]

    conn.close()

    return cols


def test_company_columns():

    cols = get_columns("companies")

    assert "id" in cols
    assert "company_name" in cols
    assert "website" in cols


def test_profitloss_columns():

    cols = get_columns("profitandloss")

    assert "sales" in cols
    assert "net_profit" in cols
    assert "eps" in cols


def test_balance_columns():

    cols = get_columns("balancesheet")

    assert "total_assets" in cols
    assert "borrowings" in cols


def test_cashflow_columns():

    cols = get_columns("cashflow")

    assert "operating_activity" in cols
    assert "net_cash_flow" in cols