import sqlite3

DB = "db/nifty100.db"


def test_database_exists():

    conn = sqlite3.connect(DB)

    assert conn is not None

    conn.close()


def test_total_tables():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM sqlite_master
    WHERE type='table'
    """)

    total = cur.fetchone()[0]

    conn.close()

    assert total == 12


def test_companies_primary_key():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(DISTINCT id)
    FROM companies
    """)

    distinct = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)
    FROM companies
    """)

    total = cur.fetchone()[0]

    conn.close()

    assert distinct == total