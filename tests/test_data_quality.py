import sqlite3

DB = "db/nifty100.db"


def get_value(query):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(query)

    value = cur.fetchone()[0]

    conn.close()

    return value


def test_positive_sales():

    assert get_value(
        """
        SELECT COUNT(*)
        FROM profitandloss
        WHERE sales < 0
        """
    ) == 0


def test_market_cap_positive():

    assert get_value(
        """
        SELECT COUNT(*)
        FROM market_cap
        WHERE market_cap_crore < 0
        """
    ) == 0


def test_stock_prices_positive():

    assert get_value(
        """
        SELECT COUNT(*)
        FROM stock_prices
        WHERE close_price < 0
        """
    ) == 0