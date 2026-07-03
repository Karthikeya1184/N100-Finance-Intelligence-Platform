import sqlite3
import pytest

DB = "db/nifty100.db"

TABLES = [
    ("companies", 92),
    ("sectors", 92),
    ("analysis", 20),
    ("documents", 1585),
    ("prosandcons", 16),
    ("profitandloss", 1276),
    ("balancesheet", 1312),
    ("cashflow", 1187),
    ("market_cap", 552),
    ("peer_groups", 56),
    ("stock_prices", 5520),
]


@pytest.mark.parametrize("table, expected", TABLES)
def test_table_row_count(table, expected):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table}")
    rows = cur.fetchone()[0]

    conn.close()

    assert rows == expected


def test_financial_ratios_row_count():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM financial_ratios")
    rows = cur.fetchone()[0]

    conn.close()

    # Sprint 2 requirement
    assert rows >= 1100