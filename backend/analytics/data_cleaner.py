"""
Data cleaner and normalization pipeline for BEST Bus Transit survey responses.
"""

import pandas as pd
import numpy as np
import re
from typing import Tuple, Dict, Any, List
from backend.utils.logger import logger
from backend.utils.validation import (
    REQUIRED_COLUMNS,
    ALLOWED_AGE_GROUPS,
    ALLOWED_OCCUPATIONS,
    ALLOWED_FREQUENCIES,
    ALLOWED_OVERCROWDING,
    ALLOWED_PAYMENTS,
)


class DataCleaner:
    """Performs validation, deduplication, imputation, and normalization on survey DataFrames."""

    def __init__(self):
        self.column_aliases = {
            "response_id": "Response_ID",
            "id": "Response_ID",
            "timestamp": "Timestamp",
            "time": "Timestamp",
            "age": "Age_Group",
            "age_group": "Age_Group",
            "age group": "Age_Group",
            "occupation": "Occupation",
            "frequent_user_status": "Frequent_User_Status",
            "frequent_user": "Frequent_User_Status",
            "are you a frequent best user": "Frequent_User_Status",
            "primary_route_number": "Primary_Route_Number",
            "primary_route": "Primary_Route_Number",
            "route": "Primary_Route_Number",
            "route_number": "Primary_Route_Number",
            "bus route": "Primary_Route_Number",
            "travel_frequency": "Travel_Frequency",
            "frequency": "Travel_Frequency",
            "how often do you travel": "Travel_Frequency",
            "peak_hour_frequency_rating": "Peak_Hour_Frequency_Rating",
            "bus_frequency_rating": "Peak_Hour_Frequency_Rating",
            "frequency_rating": "Peak_Hour_Frequency_Rating",
            "schedule_arrival_reliability": "Schedule_Arrival_Reliability",
            "reliability_rating": "Schedule_Arrival_Reliability",
            "punctuality": "Schedule_Arrival_Reliability",
            "bottleneck_delay_exposure": "Bottleneck_Delay_Exposure",
            "delay_exposure": "Bottleneck_Delay_Exposure",
            "primary_bottleneck_location": "Primary_Bottleneck_Location",
            "bottleneck_location": "Primary_Bottleneck_Location",
            "bottleneck": "Primary_Bottleneck_Location",
            "overcrowding_level": "Overcrowding_Level",
            "overcrowding": "Overcrowding_Level",
            "crowd_level": "Overcrowding_Level",
            "bus_condition_rating": "Bus_Condition_Rating",
            "bus_condition": "Bus_Condition_Rating",
            "condition_rating": "Bus_Condition_Rating",
            "cleanliness_rating": "Cleanliness_Rating",
            "cleanliness": "Cleanliness_Rating",
            "seating_comfort_rating": "Seating_Comfort_Rating",
            "seating_comfort": "Seating_Comfort_Rating",
            "ventilation_rating": "Ventilation_Rating",
            "ventilation": "Ventilation_Rating",
            "preferred_payment_method": "Preferred_Payment_Method",
            "payment_method": "Preferred_Payment_Method",
            "ticketing_method": "Preferred_Payment_Method",
            "avg_waiting_time_min": "Avg_Waiting_Time_Min",
            "waiting_time": "Avg_Waiting_Time_Min",
            "waiting_time_minutes": "Avg_Waiting_Time_Min",
        }

    def clean(self, raw_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Cleans and normalizes raw DataFrame.
        Returns: (cleaned_df, validation_report)
        """
        if raw_df is None or raw_df.empty:
            return pd.DataFrame(), {
                "total_records": 0,
                "valid_records": 0,
                "duplicates_removed": 0,
                "missing_values_handled": 0,
                "status": "Empty Dataset",
            }

        df = raw_df.copy()
        total_initial = len(df)

        # 1. Rename column aliases to canonical names
        renamed_cols = {}
        for col in df.columns:
            normalized_key = str(col).strip().lower().replace("-", "_")
            if normalized_key in self.column_aliases:
                renamed_cols[col] = self.column_aliases[normalized_key]
        df.rename(columns=renamed_cols, inplace=True)

        # Ensure required columns exist with sensible defaults if completely missing
        missing_handled_count = 0
        for req_col in REQUIRED_COLUMNS:
            if req_col not in df.columns:
                df[req_col] = np.nan
                missing_handled_count += len(df)

        # Count NaN cells before imputation
        missing_handled_count += int(df.isna().sum().sum())

        # 2. Response_ID validation & deduplication
        if "Response_ID" in df.columns:
            # fill missing IDs
            mask_missing_id = df["Response_ID"].isna() | (df["Response_ID"].astype(str).str.strip() == "")
            df.loc[mask_missing_id, "Response_ID"] = [f"GEN_{i+1:04d}" for i in range(mask_missing_id.sum())]
            df["Response_ID"] = df["Response_ID"].astype(str).str.strip()
            
            duplicates_count = int(df.duplicated(subset=["Response_ID"]).sum())
            df.drop_duplicates(subset=["Response_ID"], keep="first", inplace=True)
        else:
            df["Response_ID"] = [f"RESP{i+1:03d}" for i in range(len(df))]
            duplicates_count = 0

        # 3. Text Normalization
        str_columns = df.select_dtypes(include=["object", "string"]).columns
        for col in str_columns:
            df[col] = df[col].astype(str).str.strip()
            df.loc[df[col].isin(["nan", "None", "NULL", "null", ""]), col] = np.nan

        # 4. Route Number Normalization
        df["Primary_Route_Number"] = df["Primary_Route_Number"].apply(self._normalize_route)

        # 5. Boolean Field Normalization (Frequent_User_Status, Bottleneck_Delay_Exposure)
        df["Frequent_User_Status"] = df["Frequent_User_Status"].apply(self._normalize_boolean)
        df["Bottleneck_Delay_Exposure"] = df["Bottleneck_Delay_Exposure"].apply(self._normalize_boolean)

        # 6. Categorical Normalization (Age, Occupation, Travel Frequency, Overcrowding, Payment)
        df["Age_Group"] = df["Age_Group"].apply(self._normalize_age_group)
        df["Occupation"] = df["Occupation"].apply(self._normalize_occupation)
        df["Travel_Frequency"] = df["Travel_Frequency"].apply(self._normalize_travel_frequency)
        df["Overcrowding_Level"] = df["Overcrowding_Level"].apply(self._normalize_overcrowding)
        df["Preferred_Payment_Method"] = df["Preferred_Payment_Method"].apply(self._normalize_payment)

        # 7. Bottleneck Location Normalization
        if "Primary_Bottleneck_Location" not in df.columns:
            df["Primary_Bottleneck_Location"] = "SCLR"
        df["Primary_Bottleneck_Location"] = df["Primary_Bottleneck_Location"].apply(self._normalize_bottleneck)

        # 8. Rating Values Normalization (1 to 5 numeric scale)
        rating_cols = [
            "Peak_Hour_Frequency_Rating",
            "Schedule_Arrival_Reliability",
            "Bus_Condition_Rating",
            "Cleanliness_Rating",
            "Seating_Comfort_Rating",
            "Ventilation_Rating",
        ]
        for r_col in rating_cols:
            if r_col not in df.columns:
                df[r_col] = 3
            df[r_col] = pd.to_numeric(df[r_col], errors="coerce").fillna(3).clip(1, 5).astype(int)

        # 9. Numeric Waiting Time Normalization
        if "Avg_Waiting_Time_Min" not in df.columns:
            df["Avg_Waiting_Time_Min"] = 20
        df["Avg_Waiting_Time_Min"] = pd.to_numeric(df["Avg_Waiting_Time_Min"], errors="coerce").fillna(20).clip(1, 120).astype(int)

        # Build validation report
        valid_records = len(df)
        validation_report = {
            "total_records": total_initial,
            "valid_records": valid_records,
            "duplicates_removed": duplicates_count,
            "missing_values_handled": missing_handled_count,
            "status": "Healthy / Validated",
        }

        logger.info(
            f"Data cleaning complete. Total: {total_initial}, Valid: {valid_records}, "
            f"Dups: {duplicates_count}, Missing Handled: {missing_handled_count}"
        )
        return df, validation_report

    @staticmethod
    def _normalize_route(val: Any) -> str:
        if pd.isna(val) or str(val).strip().lower() in ["", "nan", "none"]:
            return "Other"
        s = str(val).strip().upper()
        s = re.sub(r"^ROUTE\s*", "", s, flags=re.IGNORECASE)
        s = re.sub(r"^BUS\s*", "", s, flags=re.IGNORECASE)
        if "A" in s and "21" in s:
            return "A-21"
        if "364" in s:
            return "364"
        if "383" in s:
            return "383"
        if "363" in s:
            return "363"
        return s if s in ["364", "383", "363", "A-21"] else "Other"

    @staticmethod
    def _normalize_boolean(val: Any) -> str:
        if pd.isna(val):
            return "Yes"
        s = str(val).strip().lower()
        if s in ["1", "true", "yes", "y", "frequent", "regular"]:
            return "Yes"
        if s in ["0", "false", "no", "n", "occasional", "rare"]:
            return "No"
        return "Yes"

    @staticmethod
    def _normalize_age_group(val: Any) -> str:
        if pd.isna(val):
            return "18-25"
        s = str(val).strip()
        if "18" in s or "20" in s or "25" in s:
            return "18-25"
        if "26" in s or "30" in s or "35" in s:
            return "26-35"
        if "36" in s or "40" in s or "50" in s:
            return "36-50"
        if "50" in s or "60" in s or "+" in s or "senior" in s.lower():
            return "50+"
        return "18-25"

    @staticmethod
    def _normalize_occupation(val: Any) -> str:
        if pd.isna(val):
            return "Employed"
        s = str(val).strip().lower()
        if "student" in s or "college" in s:
            return "Student"
        if "gov" in s or "public" in s:
            return "Government"
        if "bus" in s or "self" in s or "own" in s:
            return "Business/Self-Employed"
        if "retir" in s:
            return "Retired"
        if "emp" in s or "priv" in s or "corp" in s or "job" in s or "work" in s:
            return "Employed"
        return "Other"

    @staticmethod
    def _normalize_travel_frequency(val: Any) -> str:
        if pd.isna(val):
            return "Daily"
        s = str(val).strip().lower()
        if "daily" in s or "7" in s or "every" in s:
            return "Daily"
        if "5" in s or "6" in s:
            return "5-6 days/week"
        if "3" in s or "4" in s:
            return "3-4 days/week"
        if "occ" in s or "rare" in s or "1" in s or "2" in s:
            return "Occasionally"
        return "Daily"

    @staticmethod
    def _normalize_overcrowding(val: Any) -> str:
        if pd.isna(val):
            return "High"
        s = str(val).strip().capitalize()
        if s in ALLOWED_OVERCROWDING:
            return s
        s_lower = str(val).strip().lower()
        if "sev" in s_lower or "extreme" in s_lower:
            return "Severe"
        if "high" in s_lower or "crowd" in s_lower:
            return "High"
        if "mod" in s_lower or "medium" in s_lower:
            return "Moderate"
        if "low" in s_lower or "empty" in s_lower:
            return "Low"
        return "High"

    @staticmethod
    def _normalize_payment(val: Any) -> str:
        if pd.isna(val):
            return "Chalo App"
        s = str(val).strip()
        s_lower = s.lower()
        if "chalo" in s_lower:
            return "Chalo App"
        if "card" in s_lower or "smart" in s_lower:
            return "Smart Card"
        if "cash" in s_lower:
            return "Cash"
        if "upi" in s_lower or "qr" in s_lower or "gpay" in s_lower or "phonepe" in s_lower:
            return "UPI/QR"
        return "Other"

    @staticmethod
    def _normalize_bottleneck(val: Any) -> str:
        if pd.isna(val):
            return "SCLR"
        s = str(val).strip()
        s_lower = s.lower()
        if "sclr" in s_lower or "santacruz" in s_lower or "link road" in s_lower:
            return "SCLR"
        if "station" in s_lower or "chembur stn" in s_lower:
            return "Chembur Station"
        if "diamond" in s_lower or "garden" in s_lower:
            return "Diamond Garden"
        if "nehru" in s_lower:
            return "Nehru Nagar"
        if "kurla" in s_lower:
            return "Kurla Signal"
        if "none" in s_lower or "no" in s_lower:
            return "None / Smooth"
        return s
