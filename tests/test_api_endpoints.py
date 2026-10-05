"""
Integration tests for Flask API Endpoints.
"""

import pytest
import io
from backend.app import create_app
from backend.config import Config


@pytest.fixture
def client():
    app = create_app(Config)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_analytics_endpoint(client):
    """Test full analytics JSON endpoint."""
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "summary" in data["data"]
    assert "charts" in data["data"]
    assert "parameters" in data["data"]
    assert data["data"]["summary"]["total_responses"] >= 100


def test_api_analytics_with_filters(client):
    """Test filtered analytics endpoint."""
    response = client.get("/api/analytics?route=364&age_group=18-25")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["filters_applied"]["route"] == "364"
    assert data["filters_applied"]["age_group"] == "18-25"


def test_api_routes_endpoint(client):
    """Test dynamic route options endpoint."""
    response = client.get("/api/routes")
    assert response.status_code == 200
    data = response.get_json()
    assert "routes" in data
    assert {"364", "501", "430", "663", "399", "367"}.issubset(data["routes"])


def test_api_export_csv(client):
    """Test CSV export endpoint."""
    response = client.get("/api/export-csv?route=364")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Response_ID" in response.data
    assert b"Primary_Route_Number" in response.data


def test_api_refresh_endpoint(client):
    """Test POST /api/refresh endpoint."""
    response = client.post("/api/refresh")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"


def test_api_upload_csv_valid(client):
    """Test valid CSV upload endpoint."""
    csv_data = "Response_ID,Primary_Route_Number,Age_Group,Occupation,Frequent_User_Status,Travel_Frequency,Peak_Hour_Frequency_Rating,Schedule_Arrival_Reliability,Bottleneck_Delay_Exposure,Overcrowding_Level,Bus_Condition_Rating,Preferred_Payment_Method\nTEST01,364,18-25,Student,Yes,Daily,2,2,Yes,Severe,3,Chalo App"
    data = {
        "file": (io.BytesIO(csv_data.encode("utf-8")), "survey_upload.csv")
    }
    response = client.post("/api/upload-csv", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_json = response.get_json()
    assert res_json["status"] == "success"
    assert "validation" in res_json


def test_api_upload_csv_invalid_extension(client):
    """Test rejection of non-CSV file upload."""
    data = {
        "file": (io.BytesIO(b"malicious script"), "script.exe")
    }
    response = client.post("/api/upload-csv", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "Only CSV files are supported" in response.get_json()["message"]
