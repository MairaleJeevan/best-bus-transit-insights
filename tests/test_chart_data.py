"""
Tests for ChartDataService (Chart.js transformations, Radar, Bottlenecks, Hourly conditional logic).
"""

import pytest
import pandas as pd
from backend.analytics.chart_data import ChartDataService


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "Response_ID": "R1",
            "Primary_Route_Number": "364",
            "Peak_Hour_Frequency_Rating": 2,
            "Schedule_Arrival_Reliability": 2,
            "Primary_Bottleneck_Location": "SCLR",
            "Overcrowding_Level": "Severe",
            "Cleanliness_Rating": 3,
            "Preferred_Payment_Method": "Chalo App",
            "Age_Group": "18-25",
            "Occupation": "Student",
            "Travel_Frequency": "Daily",
            "Timestamp": "2026-09-10 08:30:00",
        },
        {
            "Response_ID": "R2",
            "Primary_Route_Number": "383",
            "Peak_Hour_Frequency_Rating": 4,
            "Schedule_Arrival_Reliability": 4,
            "Primary_Bottleneck_Location": "Chembur Station",
            "Overcrowding_Level": "Moderate",
            "Cleanliness_Rating": 4,
            "Preferred_Payment_Method": "Smart Card",
            "Age_Group": "26-35",
            "Occupation": "Employed",
            "Travel_Frequency": "5-6 days/week",
            "Timestamp": "2026-09-10 18:30:00",
        }
    ])


def test_route_distribution(sample_df):
    data = ChartDataService.get_route_distribution(sample_df)
    assert "labels" in data
    assert "counts" in data
    assert len(data["labels"]) == 2
    assert 1 in data["counts"]


def test_transit_health_radar(sample_df):
    data = ChartDataService.get_transit_health_profile(sample_df)
    assert len(data["labels"]) == 5
    assert len(data["scores"]) == 5
    assert data["scores"][0] > 0  # Frequency


def test_hourly_analysis_with_timestamps(sample_df):
    data = ChartDataService.get_hourly_analysis(sample_df)
    assert data["available"] is True
    assert len(data["labels"]) == 10
    assert len(data["overcrowding_index"]) == 10


def test_hourly_analysis_without_timestamps():
    df_no_time = pd.DataFrame([{"Response_ID": "R1", "Primary_Route_Number": "364"}])
    data = ChartDataService.get_hourly_analysis(df_no_time)
    assert data["available"] is False
    assert "Hourly analysis requires a time/hour field" in data["message"]
