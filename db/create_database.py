from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"


def create_database():
    print("Creating database...")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()