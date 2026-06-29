import sqlite3


def test_cashflow():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM cashflow
    """)

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 1000