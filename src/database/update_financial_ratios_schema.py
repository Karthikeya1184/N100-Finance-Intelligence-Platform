import sqlite3

DB_PATH = "db/nifty100.db"

NEW_COLUMNS = [
    ("revenue_cagr_5yr", "REAL"),
    ("pat_cagr_5yr", "REAL"),
    ("eps_cagr_5yr", "REAL"),
    ("composite_quality_score", "INTEGER")
]


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols


def main():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    for column, datatype in NEW_COLUMNS:

        if not column_exists(cursor, "financial_ratios", column):

            cursor.execute(
                f"""
                ALTER TABLE financial_ratios
                ADD COLUMN {column} {datatype}
                """
            )

            print(f"Added {column}")

        else:

            print(f"{column} already exists")

    conn.commit()

    conn.close()

    print("\nSchema Updated Successfully")


if __name__ == "__main__":
    main()