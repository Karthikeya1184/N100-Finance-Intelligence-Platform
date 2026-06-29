import sqlite3
import pytest

DB = "db/nifty100.db"

EXPECTED_TABLES = [
    "companies",
    "sectors",
    "analysis",
    "documents",
    "prosandcons",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "stock_prices"
]


@pytest.mark.parametrize("table", EXPECTED_TABLES)
def test_table_exists(table):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
    """, (table,))

    result = cur.fetchone()

    conn.close()

    assert result is not None