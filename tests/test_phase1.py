"""
Phase 1 Test Suite - Application Structure, Configuration, and Server Health.
"""

import pytest
from backend.app import create_app
from backend.config import Config


@pytest.fixture
def client():
    app = create_app(Config)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Verify that the /api/health endpoint responds with 200 OK and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "data_source" in data
    assert "version" in data


def test_index_page_serving(client):
    """Verify that the frontend index.html is served at root /."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Transit Insights" in response.data
    assert b"Chembur" in response.data


def test_static_css_serving(client):
    """Verify that static CSS files are accessible."""
    response = client.get("/css/styles.css")
    assert response.status_code == 200
    assert b"BEST BUS TRANSIT INSIGHTS" in response.data


def test_static_js_serving(client):
    """Verify that static JS files are accessible."""
    response = client.get("/js/app.js")
    assert response.status_code == 200
    assert b"BEST Bus Transit Insights Dashboard Initializing" in response.data


def test_404_error_handling(client):
    """Verify that non-existent API routes return structured 404 JSON."""
    response = client.get("/api/non-existent-route")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
    assert data["code"] == 404
