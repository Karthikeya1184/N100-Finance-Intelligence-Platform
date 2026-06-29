import sqlite3


def test_profitloss():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM profitandloss
    """)

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 1000