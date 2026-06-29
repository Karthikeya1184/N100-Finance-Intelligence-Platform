import sqlite3


def test_company_table():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    """)

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 0