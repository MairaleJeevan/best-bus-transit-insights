"""
Tests for Filter Engine (Multi-criteria slicing and pre-analytics filtering).
"""

import pytest
import pandas as pd
from backend.analytics.filters import FilterService


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {"Response_ID": "R1", "Primary_Route_Number": "364", "Age_Group": "18-25", "Occupation": "Student", "Frequent_User_Status": "Yes", "Travel_Frequency": "Daily", "Overcrowding_Level": "Severe", "Peak_Hour_Frequency_Rating": 1, "Schedule_Arrival_Reliability": 2, "Preferred_Payment_Method": "Chalo App"},
        {"Response_ID": "R2", "Primary_Route_Number": "383", "Age_Group": "26-35", "Occupation": "Employed", "Frequent_User_Status": "Yes", "Travel_Frequency": "5-6 days/week", "Overcrowding_Level": "High", "Peak_Hour_Frequency_Rating": 2, "Schedule_Arrival_Reliability": 1, "Preferred_Payment_Method": "Smart Card"},
        {"Response_ID": "R3", "Primary_Route_Number": "A-21", "Age_Group": "18-25", "Occupation": "Student", "Frequent_User_Status": "No", "Travel_Frequency": "Occasionally", "Overcrowding_Level": "Moderate", "Peak_Hour_Frequency_Rating": 4, "Schedule_Arrival_Reliability": 3, "Preferred_Payment_Method": "Chalo App"},
        {"Response_ID": "R4", "Primary_Route_Number": "363", "Age_Group": "50+", "Occupation": "Government", "Frequent_User_Status": "Yes", "Travel_Frequency": "Daily", "Overcrowding_Level": "High", "Peak_Hour_Frequency_Rating": 2, "Schedule_Arrival_Reliability": 2, "Preferred_Payment_Method": "Cash"},
    ])


def test_filter_by_route(sample_df):
    filtered = FilterService.apply_filters(sample_df, {"route": "364"})
    assert len(filtered) == 1
    assert filtered.iloc[0]["Response_ID"] == "R1"


def test_filter_by_age_group(sample_df):
    filtered = FilterService.apply_filters(sample_df, {"age_group": "18-25"})
    assert len(filtered) == 2


def test_filter_by_occupation(sample_df):
    filtered = FilterService.apply_filters(sample_df, {"occupation": "Student"})
    assert len(filtered) == 2


def test_filter_by_multiple_criteria(sample_df):
    filtered = FilterService.apply_filters(sample_df, {
        "age_group": "18-25",
        "route": "364",
        "user_status": "Frequent"
    })
    assert len(filtered) == 1
    assert filtered.iloc[0]["Response_ID"] == "R1"


def test_filter_all_returns_full_dataset(sample_df):
    filtered = FilterService.apply_filters(sample_df, {
        "route": "all",
        "age_group": "all",
        "occupation": "all"
    })
    assert len(filtered) == len(sample_df)
