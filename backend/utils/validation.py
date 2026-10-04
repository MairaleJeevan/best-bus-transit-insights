"""
Data validation utilities and schema definitions for survey responses.
"""

from typing import Dict, Any, List, Tuple
import os

REQUIRED_COLUMNS = [
    "Response_ID",
    "Age_Group",
    "Occupation",
    "Frequent_User_Status",
    "Primary_Route_Number",
    "Travel_Frequency",
    "Peak_Hour_Frequency_Rating",
    "Schedule_Arrival_Reliability",
    "Bottleneck_Delay_Exposure",
    "Overcrowding_Level",
    "Bus_Condition_Rating",
    "Preferred_Payment_Method",
]

ALLOWED_AGE_GROUPS = {"18-25", "26-35", "36-50", "50+"}
ALLOWED_OCCUPATIONS = {"Student", "Employed", "Government", "Business/Self-Employed", "Retired", "Other"}
ALLOWED_FREQUENCIES = {"Daily", "5-6 days/week", "3-4 days/week", "Occasionally"}
ALLOWED_OVERCROWDING = {"Severe", "High", "Moderate", "Low"}
ALLOWED_PAYMENTS = {"Chalo App", "Smart Card", "Cash", "UPI/QR", "Other"}


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Checks if uploaded file has an allowed extension."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_extensions


def validate_dataframe_schema(columns: List[str]) -> Tuple[bool, List[str]]:
    """Checks whether the dataframe contains all required canonical columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in columns]
    return (len(missing) == 0, missing)
