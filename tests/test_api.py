"""Tests for API endpoints."""
from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint_validation_empty_message():
    """Test that empty message returns 422 validation error."""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any(
        error.get("type") == "string_too_short"
        for error in response.json()["detail"]
    )

def test_chat_endpoint_validation_missing_message():
    """Test that missing message field returns 422."""
    response = client.post("/api/chat", json={})
    assert response.status_code == 422

def test_chat_endpoint_validation_message_too_long():
    """Test that message exceeding max_length returns 422."""
    long_message = "x" * 1001
    response = client.post("/api/chat", json={"message": long_message})
    assert response.status_code == 422

