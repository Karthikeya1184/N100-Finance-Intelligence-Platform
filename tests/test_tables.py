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
    ("financial_ratios", 1184),
    ("market_cap", 552),
    ("peer_groups", 56),
    ("stock_prices", 5520),
]


@pytest.mark.parametrize("table,expected", TABLES)
def test_table_row_count(table, expected):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table}")

    rows = cur.fetchone()[0]

    conn.close()

    assert rows == expected