"""
Analytics service orchestrating data ingestion, cleaning, caching, filtering,
and analytical calculations for the BEST Bus Transit Insights backend.
"""

import pandas as pd
import threading
from typing import Dict, Any, Optional, List, Tuple
from backend.config import Config
from backend.utils.logger import logger
from backend.analytics.data_loader import get_data_loader, CSVLoader
from backend.analytics.data_cleaner import DataCleaner
from backend.analytics.filters import FilterService
from backend.analytics.metrics import MetricsService
from backend.analytics.chart_data import ChartDataService
from backend.utils.validation import SUPPORTED_ROUTES


class AnalyticsService:
    """Singleton service for managing dataset lifecycle and analytical payloads."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AnalyticsService, cls).__new__(cls)
                cls._instance._init_service()
            return cls._instance

    def _init_service(self):
        self.cleaner = DataCleaner()
        self.cached_df: Optional[pd.DataFrame] = None
        self.cached_validation: Dict[str, Any] = {}
        self.custom_df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self, source_override: Optional[str] = None):
        """Loads and cleans dataset from source."""
        try:
            if self.custom_df is not None:
                raw_df = self.custom_df
                logger.info("Using uploaded custom survey DataFrame.")
            else:
                loader = get_data_loader(source_override or Config.DATA_SOURCE)
                raw_df = loader.load_data()

            cleaned_df, validation = self.cleaner.clean(raw_df)
            self.cached_df = cleaned_df
            self.cached_validation = validation
            logger.info("AnalyticsService data cache refreshed successfully.")
        except Exception as e:
            logger.error(f"Error loading dataset in AnalyticsService: {e}")
            if self.cached_df is None:
                # Fallback to local CSV if possible
                try:
                    raw_df = CSVLoader().load_data()
                    self.cached_df, self.cached_validation = self.cleaner.clean(raw_df)
                    logger.info("Fell back successfully to default local CSV dataset.")
                except Exception as ex:
                    logger.error(f"Fallback CSV also failed: {ex}")
                    self.cached_df = pd.DataFrame()
                    self.cached_validation = {
                        "total_records": 0,
                        "valid_records": 0,
                        "duplicates_removed": 0,
                        "missing_values_handled": 0,
                        "status": "Failed to load data",
                    }

    def refresh(self, source_override: Optional[str] = None) -> Dict[str, Any]:
        """Forces cache refresh from data source."""
        self._load_data(source_override)
        return {
            "status": "success",
            "message": "Dataset refreshed successfully",
            "validation": self.cached_validation,
        }

    def set_custom_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Sets an in-memory custom uploaded survey DataFrame."""
        self.custom_df = df
        return self.refresh()

    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """Returns the full cached cleaned DataFrame."""
        if self.cached_df is None:
            self._load_data()
        return self.cached_df.copy() if self.cached_df is not None else pd.DataFrame()

    def get_analytics(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes filtering and generates the complete analytics response.
        Filters are applied before KPI, parameter, and chart calculations.
        """
        df = self.get_cleaned_dataframe()

        # Apply filters
        if filters:
            df = FilterService.apply_filters(df, filters)

        summary_kpis = MetricsService.get_summary_kpis(df)
        parameter_matrix = MetricsService.get_parameter_diagnostics(df)

        # Charts payloads
        route_data = ChartDataService.get_route_distribution(df)
        peak_reliability_data = ChartDataService.get_peak_reliability_distribution(df)
        bottleneck_data = ChartDataService.get_bottleneck_analysis(df)
        hourly_data = ChartDataService.get_hourly_analysis(df)
        radar_data = ChartDataService.get_transit_health_profile(df)
        payment_data = ChartDataService.get_payment_distribution(df)
        demographics_data = ChartDataService.get_demographics_distribution(df)
        condition_data = ChartDataService.get_bus_condition_breakdown(df)

        return {
            "summary": summary_kpis,
            "parameters": parameter_matrix,
            "charts": {
                "route_usage": route_data,
                "peak_reliability": peak_reliability_data,
                "bottlenecks": bottleneck_data,
                "hourly_trend": hourly_data,
                "transit_health": radar_data,
                "payments": payment_data,
                "demographics": demographics_data,
                "bus_condition": condition_data,
            },
            "validation": self.cached_validation,
            "active_record_count": len(df),
            "data_source": Config.DATA_SOURCE,
        }

    def get_filter_options(self) -> Dict[str, List[str]]:
        """Returns supported routes plus category options available in the dataset."""
        df = self.get_cleaned_dataframe()
        if df.empty:
            return {"routes": list(SUPPORTED_ROUTES), "occupations": [], "age_groups": []}

        routes = list(SUPPORTED_ROUTES)
        if "Other" in df["Primary_Route_Number"].values:
            routes.append("Other")

        occupations = sorted([str(o) for o in df["Occupation"].dropna().unique()])
        age_groups = ["18-25", "26-35", "36-50", "50+"]

        return {
            "routes": routes,
            "occupations": occupations,
            "age_groups": age_groups,
        }

    def export_filtered_csv(self, filters: Optional[Dict[str, Any]] = None) -> str:
        """Returns CSV string of the filtered dataset."""
        df = self.get_cleaned_dataframe()
        if filters:
            df = FilterService.apply_filters(df, filters)
        return df.to_csv(index=False)


# Global analytics service instance
analytics_service = AnalyticsService()
