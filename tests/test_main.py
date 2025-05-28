import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# --- Fixtures ---

@pytest.fixture
def valid_token():
    # Replace with a real token from your DB if needed
    return "128d8249e357b82f7e3e68ab65eca6c3"

@pytest.fixture
def test_image_path():
    return "app/static/test.jpg"  # ensure this file exists in your repo

# --- Tests ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_usage_requires_auth():
    response = client.get("/usage")
    assert response.status_code == 422 or response.status_code == 401


def test_invalid_token_rejected():
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/usage", headers=headers)
    assert response.status_code == 403


def test_moderate_requires_token(test_image_path):
    with open(test_image_path, "rb") as img:
        response = client.post("/moderate", files={"file": img})
    assert response.status_code in [401, 422]


@patch("app.api.moderate.requests.post")
def test_moderate_with_mocked_api(mock_post, valid_token, test_image_path):
    # Mock Sightengine response
    mock_post.return_value.json.return_value = {
        "nudity": {"safe": 0.99, "raw": 0.01, "partial": 0.01},
        "gore": {"prob": 0.01},
        "weapon": 0.01,
        "summary": {"action": "accept"}
    }

    headers = {"Authorization": f"Bearer {valid_token}"}
    with open(test_image_path, "rb") as img:
        response = client.post("/moderate", headers=headers, files={"file": img})

    assert response.status_code == 200
    result = response.json()
    assert "filename" in result
    assert "safe" in result
    assert "categories" in result