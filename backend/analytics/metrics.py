"""
Metrics and KPI computation engine for BEST Bus Transit Insights.
All metrics are dynamically calculated using Pandas and NumPy.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class MetricsService:
    """Calculates summary KPIs and diagnostic matrix from DataFrame."""

    @staticmethod
    def get_summary_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates top-level KPI metrics."""
        if df is None or df.empty:
            return {
                "total_responses": 0,
                "peak_delay_pct": 0.0,
                "overcrowding_pct": 0.0,
                "digital_payment_pct": 0.0,
                "frequent_users_pct": 0.0,
                "avg_waiting_time": 0.0,
                "top_route": "N/A",
                "top_bottleneck": "N/A",
            }

        total = len(df)

        # 1. Peak Delay Exposure (% affected by bottleneck delays or poor frequency rating <= 2)
        delay_count = int(
            (
                (df["Bottleneck_Delay_Exposure"] == "Yes")
                | (df["Peak_Hour_Frequency_Rating"] <= 2)
            ).sum()
        )
        peak_delay_pct = round((delay_count / total) * 100, 1)

        # 2. Overcrowding Index (% reporting Severe or High)
        crowd_count = int(df["Overcrowding_Level"].isin(["Severe", "High"]).sum())
        overcrowding_pct = round((crowd_count / total) * 100, 1)

        # 3. Digital Payment Share (% Chalo App, Smart Card, UPI/QR)
        digital_count = int(
            df["Preferred_Payment_Method"].isin(["Chalo App", "Smart Card", "UPI/QR"]).sum()
        )
        digital_payment_pct = round((digital_count / total) * 100, 1)

        # 4. Frequent BEST Users (% Yes)
        frequent_count = int((df["Frequent_User_Status"] == "Yes").sum())
        frequent_users_pct = round((frequent_count / total) * 100, 1)

        # 5. Average Waiting Time (mins)
        if "Avg_Waiting_Time_Min" in df.columns and not df["Avg_Waiting_Time_Min"].dropna().empty:
            avg_wait = round(float(df["Avg_Waiting_Time_Min"].mean()), 1)
        else:
            avg_wait = 20.0

        # 6. Top Route
        route_counts = df["Primary_Route_Number"].value_counts()
        top_route = str(route_counts.index[0]) if not route_counts.empty else "N/A"

        # 7. Top Bottleneck
        bottleneck_counts = df["Primary_Bottleneck_Location"].value_counts()
        # filter out None if other bottlenecks exist
        valid_b_counts = bottleneck_counts[~bottleneck_counts.index.isin(["None", "None / Smooth"])]
        if not valid_b_counts.empty:
            top_bottleneck = str(valid_b_counts.index[0])
        elif not bottleneck_counts.empty:
            top_bottleneck = str(bottleneck_counts.index[0])
        else:
            top_bottleneck = "N/A"

        return {
            "total_responses": total,
            "peak_delay_pct": peak_delay_pct,
            "overcrowding_pct": overcrowding_pct,
            "digital_payment_pct": digital_payment_pct,
            "frequent_users_pct": frequent_users_pct,
            "avg_waiting_time": avg_wait,
            "top_route": top_route,
            "top_bottleneck": top_bottleneck,
        }

    @staticmethod
    def get_parameter_diagnostics(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generates the detailed parameter diagnostic analysis table.
        Applies configurable operational health rules to categorize indicators.
        """
        if df is None or df.empty:
            return []

        total = len(df)
        params = []

        # Parameter 1: Digital Payment Adoption
        digital_pct = round(
            float(df["Preferred_Payment_Method"].isin(["Chalo App", "Smart Card", "UPI/QR"]).sum()) / total * 100, 1
        )
        params.append({
            "parameter": "Digital Payment Adoption",
            "positive_label": "Chalo / Smart Card",
            "negative_label": "Cash / Manual",
            "positive_pct": digital_pct,
            "negative_pct": round(100 - digital_pct, 1),
            "status": "High Adoption" if digital_pct >= 60 else "Acceptable" if digital_pct >= 40 else "Operational Concern",
            "recommendation": "Expand Chalo card reload kiosks at Chembur Station & Nehru Nagar stops.",
        })

        # Parameter 2: Peak Hour Bus Frequency
        freq_good_pct = round(
            float((df["Peak_Hour_Frequency_Rating"] >= 3).sum()) / total * 100, 1
        )
        freq_bad_pct = round(100 - freq_good_pct, 1)
        params.append({
            "parameter": "Peak-Hour Frequency Adequacy",
            "positive_label": "Adequate (>=3)",
            "negative_label": "Inadequate (1-2)",
            "positive_pct": freq_good_pct,
            "negative_pct": freq_bad_pct,
            "status": "Critical Deficit" if freq_bad_pct >= 60 else "Operational Concern" if freq_bad_pct >= 35 else "Acceptable",
            "recommendation": "Deploy supplementary feeder buses on Route 364 & 383 between 8-11 AM & 6-9 PM.",
        })

        # Parameter 3: Schedule Arrival Reliability
        rel_good_pct = round(
            float((df["Schedule_Arrival_Reliability"] >= 3).sum()) / total * 100, 1
        )
        rel_bad_pct = round(100 - rel_good_pct, 1)
        params.append({
            "parameter": "Schedule Arrival Reliability",
            "positive_label": "Reliable (>=3)",
            "negative_label": "Unreliable (1-2)",
            "positive_pct": rel_good_pct,
            "negative_pct": rel_bad_pct,
            "status": "Critical Deficit" if rel_bad_pct >= 60 else "Operational Concern" if rel_bad_pct >= 35 else "Acceptable",
            "recommendation": "Integrate transit signal priority (TSP) at SCLR and Chembur Station intersections.",
        })

        # Parameter 4: Overcrowding Management
        crowd_safe_pct = round(
            float(df["Overcrowding_Level"].isin(["Moderate", "Low"]).sum()) / total * 100, 1
        )
        crowd_bad_pct = round(100 - crowd_safe_pct, 1)
        params.append({
            "parameter": "Cabin Capacity & Crowd Control",
            "positive_label": "Comfortable/Moderate",
            "negative_label": "Severe/High Crowd",
            "positive_pct": crowd_safe_pct,
            "negative_pct": crowd_bad_pct,
            "status": "Critical Deficit" if crowd_bad_pct >= 70 else "Operational Concern" if crowd_bad_pct >= 40 else "Acceptable",
            "recommendation": "Introduce Double Decker electric buses or articulated buses along high-demand corridors.",
        })

        # Parameter 5: Fleet Physical Condition
        cond_good_pct = round(
            float((df["Bus_Condition_Rating"] >= 3).sum()) / total * 100, 1
        )
        cond_bad_pct = round(100 - cond_good_pct, 1)
        params.append({
            "parameter": "Bus Physical Condition & Fleet Quality",
            "positive_label": "Good / Fair (>=3)",
            "negative_label": "Poor (1-2)",
            "positive_pct": cond_good_pct,
            "negative_pct": cond_bad_pct,
            "status": "Acceptable" if cond_good_pct >= 70 else "Operational Concern" if cond_good_pct >= 50 else "Critical Deficit",
            "recommendation": "Maintain daily depot inspection schedule at Kurla & Anik depots.",
        })

        # Parameter 6: Commuter Loyalty / User Retention
        frequent_pct = round(
            float((df["Frequent_User_Status"] == "Yes").sum()) / total * 100, 1
        )
        params.append({
            "parameter": "Commuter Dependency & Loyalty",
            "positive_label": "Regular Daily Riders",
            "negative_label": "Occasional Commuters",
            "positive_pct": frequent_pct,
            "negative_pct": round(100 - frequent_pct, 1),
            "status": "High Adoption" if frequent_pct >= 70 else "Acceptable",
            "recommendation": "Introduce student & monthly corridor subscription passes on Chalo App.",
        })

        return params
