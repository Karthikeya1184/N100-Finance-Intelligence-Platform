import sqlite3


def test_balance():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM balancesheet
    """)

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 1000