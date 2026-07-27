from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_all_sectors():

    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    print(data)
    assert len(data) == 10


def test_get_it_sector():

    response = client.get(
        "/api/v1/sectors/Information Technology/companies"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for company in data:
        assert "id" in company
        assert "company_name" in company