""" Test the routes of the Flask app """
import json
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_page_not_found(client):
    """Test the 404 error handler"""
    response = client.get("/invalid_route")
    assert response.status_code == 404
    assert response.json == {
        "error": "Page not found",
        "message": "The requested page does not exist.",
    }


def test_get_data(client):
    """Test the get_data route"""
    response = client.get("/allBerryStats")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.get_data(as_text=True))
    assert "berries_names" in data


if __name__ == "__main__":
    pytest.main()
