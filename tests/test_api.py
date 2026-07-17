from unittest.mock import patch
from fastapi.testclient import TestClient
from app.schemas.extraction import ExtractedEntities
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_extract_returns_200_with_valid_input():
    mock_entities = ExtractedEntities(
        people=["João Silva"],
        organizations=["Tech Ltda"],
        dates=["15/03/2024"],
        values=["R$ 50.000"],
        locations=["São Paulo"],
        key_terms=["contrato"],
    )

    with patch("app.api.routes.extractor.extract", return_value=mock_entities):
        response = client.post(
            "/api/v1/extract",
            json={
                "text": "João Silva firmou contrato com Tech Ltda em São Paulo.",
                "document_type": "contract",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["document_type"] == "contract"
    assert "João Silva" in data["entities"]["people"]
    assert data["confidence"] > 0.0


def test_extract_returns_422_with_short_text():
    response = client.post(
        "/api/v1/extract",
        json={"text": "Curto"},
    )
    assert response.status_code == 422


def test_extract_returns_422_with_missing_text():
    response = client.post(
        "/api/v1/extract",
        json={},
    )
    assert response.status_code == 422