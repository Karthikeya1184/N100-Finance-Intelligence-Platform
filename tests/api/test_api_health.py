from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_status():

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_health_has_db_row_counts():

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert "db_row_counts" in data

    row_counts = data["db_row_counts"]

    expected_tables = [
        "companies",
        "sectors",
        "analysis",
        "documents",
        "prosandcons",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "stock_prices",
    ]

    for table in expected_tables:
        assert table in row_counts
