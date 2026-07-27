from pathlib import Path
import sqlite3

from fastapi import APIRouter

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@router.get("/companies/{ticker}/documents")
def get_documents(ticker: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            document_name,
            document_url
        FROM documents
        WHERE company_id = ?
        ORDER BY document_name
        """,
        (ticker.upper(),)
    )

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:
        item = dict(row)
        url = item.get("document_url")
        item["is_url_valid"] = (
            isinstance(url, str)
            and url.startswith(("http://", "https://"))
        )
        results.append(item)

    return results