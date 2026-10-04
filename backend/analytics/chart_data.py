"""
Chart data preparation service for Chart.js dashboard components.
Generates dynamically calculated arrays and payloads for all frontend visualizations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class ChartDataService:
    """Transforms cleaned survey DataFrames into Chart.js compatible structures."""

    @staticmethod
    def get_route_distribution(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates route usage distribution counts and percentages."""
        if df is None or df.empty:
            return {"labels": [], "counts": [], "percentages": []}

        total = len(df)
        counts_series = df["Primary_Route_Number"].value_counts()

        # Sort with standard corridor routes prioritized
        priority_order = ["364", "383", "363", "A-21", "Other"]
        labels = []
        counts = []
        percentages = []

        # Add priority items in order if present
        for route in priority_order:
            if route in counts_series:
                c = int(counts_series[route])
                labels.append(f"Route {route}" if route != "Other" else "Other Routes")
                counts.append(c)
                percentages.append(round((c / total) * 100, 1))

        # Add any remaining routes not in priority list
        for route, count in counts_series.items():
            route_str = str(route)
            if route_str not in priority_order and route_str != "Other":
                labels.append(f"Route {route_str}")
                counts.append(int(count))
                percentages.append(round((int(count) / total) * 100, 1))

        return {
            "labels": labels,
            "counts": counts,
            "percentages": percentages,
        }

    @staticmethod
    def get_peak_reliability_distribution(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates rating distributions (1-5 stars) for Frequency and Reliability."""
        if df is None or df.empty:
            return {"labels": ["1 (Very Poor)", "2 (Poor)", "3 (Average)", "4 (Good)", "5 (Excellent)"], "frequency": [0]*5, "reliability": [0]*5}

        labels = ["1 (Very Poor)", "2 (Poor)", "3 (Average)", "4 (Good)", "5 (Excellent)"]
        freq_counts = df["Peak_Hour_Frequency_Rating"].value_counts().to_dict()
        rel_counts = df["Schedule_Arrival_Reliability"].value_counts().to_dict()

        freq_data = [int(freq_counts.get(i, 0)) for i in range(1, 6)]
        rel_data = [int(rel_counts.get(i, 0)) for i in range(1, 6)]

        return {
            "labels": labels,
            "frequency": freq_data,
            "reliability": rel_data,
        }

    @staticmethod
    def get_bottleneck_analysis(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates bottleneck location impact, percentages, and severity."""
        if df is None or df.empty:
            return {"labels": [], "counts": [], "percentages": [], "severity": []}

        total = len(df)
        b_series = df["Primary_Bottleneck_Location"].value_counts()

        labels = []
        counts = []
        percentages = []
        severity = []

        for location, count in b_series.items():
            loc_str = str(location)
            c = int(count)
            pct = round((c / total) * 100, 1)
            labels.append(loc_str)
            counts.append(c)
            percentages.append(pct)

            if pct >= 35:
                sev = "Critical Bottleneck"
            elif pct >= 20:
                sev = "High Congestion"
            elif pct >= 10:
                sev = "Moderate Delay"
            else:
                sev = "Low / Minor"
            severity.append(sev)

        return {
            "labels": labels,
            "counts": counts,
            "percentages": percentages,
            "severity": severity,
        }

    @staticmethod
    def get_hourly_analysis(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extracts hourly trends if timestamp data is available.
        If not present or insufficient, explicitly flags data availability.
        """
        if df is None or df.empty:
            return {
                "available": False,
                "message": "No survey data available for hourly analysis.",
                "labels": [],
                "overcrowding_index": [],
                "bus_frequency": [],
            }

        # Check for timestamp or hour columns
        time_col = None
        for col in ["Timestamp", "Time", "Travel_Hour", "Time_Of_Travel"]:
            if col in df.columns:
                time_col = col
                break

        if not time_col:
            return {
                "available": False,
                "message": "Hourly analysis requires a time/hour field in the survey dataset.",
                "labels": [],
                "overcrowding_index": [],
                "bus_frequency": [],
            }

        try:
            # Parse hours from timestamp
            ts = pd.to_datetime(df[time_col], errors="coerce")
            valid_ts = ts.dropna()
            if valid_ts.empty or valid_ts.dt.hour.nunique() < 2:
                return {
                    "available": False,
                    "message": "Insufficient hourly observations in survey timestamps.",
                    "labels": [],
                    "overcrowding_index": [],
                    "bus_frequency": [],
                }

            hours = valid_ts.dt.hour
            hour_counts = hours.value_counts().sort_index()

            standard_hours = [7, 8, 9, 10, 12, 14, 16, 18, 20, 22]
            labels = []
            crowd_trend = []
            freq_trend = []

            for h in standard_hours:
                label = f"{h % 12 or 12} {'AM' if h < 12 else 'PM'}"
                labels.append(label)

                # subset of respondents traveling near this hour
                matching_mask = (hours >= h - 1) & (hours <= h + 1)
                subset = df.loc[valid_ts[matching_mask].index]

                if not subset.empty:
                    severe_pct = round(
                        float(subset["Overcrowding_Level"].isin(["Severe", "High"]).sum()) / len(subset) * 100, 1
                    )
                    avg_freq_score = round(
                        float(subset["Peak_Hour_Frequency_Rating"].mean()) * 20, 1
                    )
                else:
                    severe_pct = 0.0
                    avg_freq_score = 0.0

                crowd_trend.append(severe_pct)
                freq_trend.append(avg_freq_score)

            return {
                "available": True,
                "message": "Hourly distribution derived from commuter response timestamps.",
                "labels": labels,
                "overcrowding_index": crowd_trend,
                "bus_frequency": freq_trend,
            }
        except Exception as e:
            return {
                "available": False,
                "message": f"Unable to parse timestamp for hourly trend: {e}",
                "labels": [],
                "overcrowding_index": [],
                "bus_frequency": [],
            }

    @staticmethod
    def get_transit_health_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates 5-dimensional Transit Health Radar scores (0 to 100).
        Dimensions: Frequency, Timeliness, Capacity, Cleanliness, Digital Adoption.
        """
        if df is None or df.empty:
            return {
                "labels": ["Frequency Adequacy", "Schedule Timeliness", "Capacity & Comfort", "Fleet Cleanliness", "Digital Payment"],
                "scores": [0, 0, 0, 0, 0],
            }

        total = len(df)

        # 1. Frequency Adequacy: mean of Peak_Hour_Frequency_Rating (1-5 mapped to 20-100)
        freq_score = round(float(df["Peak_Hour_Frequency_Rating"].mean()) * 20, 1)

        # 2. Timeliness: mean of Schedule_Arrival_Reliability (1-5 mapped to 20-100)
        time_score = round(float(df["Schedule_Arrival_Reliability"].mean()) * 20, 1)

        # 3. Capacity: % not severely overcrowded
        capacity_score = round(
            float(df["Overcrowding_Level"].isin(["Moderate", "Low"]).sum()) / total * 100, 1
        )

        # 4. Cleanliness: mean of Cleanliness_Rating if available, else Bus_Condition_Rating
        clean_col = "Cleanliness_Rating" if "Cleanliness_Rating" in df.columns else "Bus_Condition_Rating"
        clean_score = round(float(df[clean_col].mean()) * 20, 1)

        # 5. Digital Adoption: % digital ticketing
        digital_score = round(
            float(df["Preferred_Payment_Method"].isin(["Chalo App", "Smart Card", "UPI/QR"]).sum()) / total * 100, 1
        )

        return {
            "labels": [
                "Frequency Adequacy",
                "Schedule Timeliness",
                "Capacity & Comfort",
                "Fleet Cleanliness",
                "Digital Payment",
            ],
            "scores": [freq_score, time_score, capacity_score, clean_score, digital_score],
        }

    @staticmethod
    def get_payment_distribution(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates breakdown of preferred payment methods."""
        if df is None or df.empty:
            return {"labels": [], "counts": [], "percentages": []}

        total = len(df)
        counts_series = df["Preferred_Payment_Method"].value_counts()

        labels = [str(k) for k in counts_series.index]
        counts = [int(v) for v in counts_series.values]
        percentages = [round((int(v) / total) * 100, 1) for v in counts_series.values]

        return {
            "labels": labels,
            "counts": counts,
            "percentages": percentages,
        }

    @staticmethod
    def get_demographics_distribution(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates age group and occupation distributions."""
        if df is None or df.empty:
            return {
                "age_groups": {"labels": [], "counts": []},
                "occupations": {"labels": [], "counts": []},
                "frequencies": {"labels": [], "counts": []},
            }

        age_counts = df["Age_Group"].value_counts()
        occ_counts = df["Occupation"].value_counts()
        freq_counts = df["Travel_Frequency"].value_counts()

        return {
            "age_groups": {
                "labels": [str(k) for k in age_counts.index],
                "counts": [int(v) for v in age_counts.values],
            },
            "occupations": {
                "labels": [str(k) for k in occ_counts.index],
                "counts": [int(v) for v in occ_counts.values],
            },
            "frequencies": {
                "labels": [str(k) for k in freq_counts.index],
                "counts": [int(v) for v in freq_counts.values],
            },
        }

    @staticmethod
    def get_bus_condition_breakdown(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates rating breakdowns for physical bus condition parameters."""
        if df is None or df.empty:
            return {
                "parameters": ["Cleanliness", "Seating Comfort", "Ventilation"],
                "averages": [0.0, 0.0, 0.0],
                "satisfaction_pct": [0.0, 0.0, 0.0],
            }

        total = len(df)
        c_clean = df["Cleanliness_Rating"] if "Cleanliness_Rating" in df.columns else df["Bus_Condition_Rating"]
        c_seat = df["Seating_Comfort_Rating"] if "Seating_Comfort_Rating" in df.columns else df["Bus_Condition_Rating"]
        c_vent = df["Ventilation_Rating"] if "Ventilation_Rating" in df.columns else df["Bus_Condition_Rating"]

        avg_clean = round(float(c_clean.mean()), 2)
        avg_seat = round(float(c_seat.mean()), 2)
        avg_vent = round(float(c_vent.mean()), 2)

        sat_clean = round(float((c_clean >= 3).sum()) / total * 100, 1)
        sat_seat = round(float((c_seat >= 3).sum()) / total * 100, 1)
        sat_vent = round(float((c_vent >= 3).sum()) / total * 100, 1)

        return {
            "parameters": ["Cleanliness", "Seating Comfort", "Ventilation"],
            "averages": [avg_clean, avg_seat, avg_vent],
            "satisfaction_pct": [sat_clean, sat_seat, sat_vent],
        }
