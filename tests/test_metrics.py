"""
Tests for Metrics and KPI Calculations.
Ensures zero hardcoding and accurate dynamic arithmetic.
"""

import pytest
import pandas as pd
from backend.analytics.metrics import MetricsService


def test_metrics_calculation_dynamic():
    """Verify exact dynamic percentage and aggregation computations."""
    df = pd.DataFrame([
        {
            "Response_ID": "R1",
            "Bottleneck_Delay_Exposure": "Yes",
            "Peak_Hour_Frequency_Rating": 2,
            "Overcrowding_Level": "Severe",
            "Preferred_Payment_Method": "Chalo App",
            "Frequent_User_Status": "Yes",
            "Avg_Waiting_Time_Min": 30,
            "Primary_Route_Number": "364",
            "Primary_Bottleneck_Location": "SCLR",
            "Schedule_Arrival_Reliability": 2,
            "Bus_Condition_Rating": 3,
        },
        {
            "Response_ID": "R2",
            "Bottleneck_Delay_Exposure": "No",
            "Peak_Hour_Frequency_Rating": 4,
            "Overcrowding_Level": "Low",
            "Preferred_Payment_Method": "Cash",
            "Frequent_User_Status": "No",
            "Avg_Waiting_Time_Min": 10,
            "Primary_Route_Number": "383",
            "Primary_Bottleneck_Location": "Chembur Station",
            "Schedule_Arrival_Reliability": 4,
            "Bus_Condition_Rating": 4,
        }
    ])

    summary = MetricsService.get_summary_kpis(df)
    assert summary["total_responses"] == 2
    assert summary["peak_delay_pct"] == 50.0  # 1 out of 2 has delay exposure or low freq
    assert summary["overcrowding_pct"] == 50.0  # 1 out of 2
    assert summary["digital_payment_pct"] == 50.0  # 1 out of 2 (Chalo App)
    assert summary["frequent_users_pct"] == 50.0  # 1 out of 2
    assert summary["avg_waiting_time"] == 20.0  # (30 + 10) / 2


def test_metrics_empty_dataframe():
    """Verify that empty DataFrames return zeroed-out structures without crashing."""
    df = pd.DataFrame()
    summary = MetricsService.get_summary_kpis(df)
    assert summary["total_responses"] == 0
    assert summary["peak_delay_pct"] == 0.0
    assert summary["top_route"] == "N/A"
