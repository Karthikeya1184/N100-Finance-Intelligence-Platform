import sqlite3


def test_database_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    """)

    count = cursor.fetchone()[0]

    conn.close()

    assert count == 92
    