"""
Tests for Data Cleaner (Deduplication, Imputation, Route Normalization, Boolean Normalization).
"""

import pytest
import pandas as pd
import numpy as np
from backend.analytics.data_cleaner import DataCleaner


def test_cleaner_deduplication():
    """Verify that duplicate Response_IDs are properly removed."""
    raw_df = pd.DataFrame([
        {"Response_ID": "RESP001", "Primary_Route_Number": "364", "Age_Group": "18-25"},
        {"Response_ID": "RESP001", "Primary_Route_Number": "364", "Age_Group": "18-25"},
        {"Response_ID": "RESP002", "Primary_Route_Number": "383", "Age_Group": "26-35"},
    ])
    cleaner = DataCleaner()
    df, report = cleaner.clean(raw_df)
    assert len(df) == 2
    assert report["duplicates_removed"] == 1
    assert report["valid_records"] == 2


def test_cleaner_route_normalization():
    """Verify route normalization for variations like 'Route 364', 'A21', 'Bus 383'."""
    raw_df = pd.DataFrame([
        {"Response_ID": "R1", "Primary_Route_Number": "Route 364"},
        {"Response_ID": "R2", "Primary_Route_Number": "A21"},
        {"Response_ID": "R3", "Primary_Route_Number": "Bus 383"},
        {"Response_ID": "R4", "Primary_Route_Number": "999"},
    ])
    cleaner = DataCleaner()
    df, _ = cleaner.clean(raw_df)
    routes = df["Primary_Route_Number"].tolist()
    assert routes[0] == "364"
    assert routes[1] == "A-21"
    assert routes[2] == "383"
    assert routes[3] == "Other"


def test_cleaner_boolean_normalization():
    """Verify boolean normalization of strings, numbers, etc."""
    raw_df = pd.DataFrame([
        {"Response_ID": "R1", "Frequent_User_Status": "Yes", "Bottleneck_Delay_Exposure": "1"},
        {"Response_ID": "R2", "Frequent_User_Status": "No", "Bottleneck_Delay_Exposure": "0"},
        {"Response_ID": "R3", "Frequent_User_Status": "frequent", "Bottleneck_Delay_Exposure": "true"},
        {"Response_ID": "R4", "Frequent_User_Status": "rare", "Bottleneck_Delay_Exposure": "false"},
    ])
    cleaner = DataCleaner()
    df, _ = cleaner.clean(raw_df)
    assert df.loc[df["Response_ID"] == "R1", "Frequent_User_Status"].values[0] == "Yes"
    assert df.loc[df["Response_ID"] == "R2", "Frequent_User_Status"].values[0] == "No"
    assert df.loc[df["Response_ID"] == "R3", "Frequent_User_Status"].values[0] == "Yes"
    assert df.loc[df["Response_ID"] == "R4", "Frequent_User_Status"].values[0] == "No"


def test_cleaner_missing_value_imputation():
    """Verify that missing ratings and values are gracefully imputed."""
    raw_df = pd.DataFrame([
        {"Response_ID": "R1", "Peak_Hour_Frequency_Rating": None, "Avg_Waiting_Time_Min": None}
    ])
    cleaner = DataCleaner()
    df, report = cleaner.clean(raw_df)
    assert df["Peak_Hour_Frequency_Rating"].values[0] == 3
    assert df["Avg_Waiting_Time_Min"].values[0] == 20
    assert report["missing_values_handled"] > 0
