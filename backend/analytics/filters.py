"""
Filter service for applying multi-criteria slices on survey Pandas DataFrames.
Ensures filters are executed before analytics and visualization generation.
"""

import pandas as pd
from typing import Dict, Any
from backend.utils.logger import logger


class FilterService:
    """Applies analytical filters to survey DataFrames."""

    @staticmethod
    def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Applies filter dictionary to DataFrame.
        Ignores keys with value 'all', None, or empty string.
        """
        if df is None or df.empty or not filters:
            return df

        filtered_df = df.copy()

        # 1. Route filter
        route = filters.get("route") or filters.get("primary_route_number")
        if route and str(route).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Primary_Route_Number"].str.lower() == str(route).strip().lower()]

        # 2. User Status / Frequent User
        user_status = filters.get("user_status") or filters.get("frequent_user_status")
        if user_status and str(user_status).strip().lower() != "all":
            status_val = str(user_status).strip().lower()
            if status_val in ["frequent", "yes", "regular"]:
                filtered_df = filtered_df[filtered_df["Frequent_User_Status"] == "Yes"]
            elif status_val in ["occasional", "no", "rare"]:
                filtered_df = filtered_df[filtered_df["Frequent_User_Status"] == "No"]

        # 3. Age Group filter
        age_group = filters.get("age_group")
        if age_group and str(age_group).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Age_Group"].str.lower() == str(age_group).strip().lower()]

        # 4. Occupation filter
        occupation = filters.get("occupation")
        if occupation and str(occupation).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Occupation"].str.lower() == str(occupation).strip().lower()]

        # 5. Travel Frequency filter
        frequency = filters.get("frequency") or filters.get("travel_frequency")
        if frequency and str(frequency).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Travel_Frequency"].str.lower() == str(frequency).strip().lower()]

        # 6. Payment Method filter
        payment = filters.get("payment_method") or filters.get("preferred_payment_method")
        if payment and str(payment).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Preferred_Payment_Method"].str.lower() == str(payment).strip().lower()]

        # 7. Overcrowding Level filter
        overcrowding = filters.get("overcrowding") or filters.get("overcrowding_level")
        if overcrowding and str(overcrowding).strip().lower() != "all":
            filtered_df = filtered_df[filtered_df["Overcrowding_Level"].str.lower() == str(overcrowding).strip().lower()]

        # 8. Bus Frequency Rating filter
        bus_freq = filters.get("bus_frequency") or filters.get("peak_hour_frequency_rating")
        if bus_freq and str(bus_freq).strip().lower() != "all":
            try:
                rating_val = int(bus_freq)
                filtered_df = filtered_df[filtered_df["Peak_Hour_Frequency_Rating"] == rating_val]
            except ValueError:
                pass

        # 9. Schedule Reliability filter
        reliability = filters.get("schedule_reliability") or filters.get("schedule_arrival_reliability")
        if reliability and str(reliability).strip().lower() != "all":
            try:
                rel_val = int(reliability)
                filtered_df = filtered_df[filtered_df["Schedule_Arrival_Reliability"] == rel_val]
            except ValueError:
                pass

        logger.debug(f"Filtered DataFrame from {len(df)} to {len(filtered_df)} records.")
        return filtered_df
