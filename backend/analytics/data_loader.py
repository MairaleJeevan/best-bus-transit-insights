"""
Data loader module for BEST Bus Transit Insights.
Supports loading from local CSV and Google Sheets API.
"""

from abc import ABC, abstractmethod
import os
import pandas as pd
from typing import Optional, Tuple
from backend.config import Config
from backend.utils.logger import logger


class AbstractDataLoader(ABC):
    """Abstract base class for survey data loaders."""

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads data into a pandas DataFrame."""
        pass


class CSVLoader(AbstractDataLoader):
    """Loads survey responses from a local CSV file."""

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or Config.CSV_DATA_PATH

    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            logger.error(f"CSV dataset not found at path: {self.file_path}")
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        try:
            df = pd.read_csv(self.file_path, encoding="utf-8")
            logger.info(f"Loaded {len(df)} records from CSV: {self.file_path}")
            return df
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise e


class GoogleSheetsLoader(AbstractDataLoader):
    """Loads survey responses from Google Sheets API using gspread/google-auth."""

    def __init__(self, sheet_id: Optional[str] = None, credentials_path: Optional[str] = None):
        self.sheet_id = sheet_id or Config.GOOGLE_SHEET_ID
        self.credentials_path = credentials_path or Config.GOOGLE_SERVICE_ACCOUNT_JSON

    def load_data(self) -> pd.DataFrame:
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEET_ID is not configured.")

        from backend.services.google_sheets import fetch_sheet_records
        records = fetch_sheet_records(self.sheet_id, self.credentials_path)
        if not records:
            raise ValueError("No records returned from Google Sheet.")

        df = pd.DataFrame(records)
        logger.info(f"Loaded {len(df)} records from Google Sheet ID: {self.sheet_id}")
        return df


def get_data_loader(source_type: Optional[str] = None) -> AbstractDataLoader:
    """Factory function returning the configured data loader instance with fallback."""
    source = (source_type or Config.DATA_SOURCE).lower()

    if source == "google_sheets":
        try:
            if Config.GOOGLE_SHEET_ID and os.path.exists(Config.GOOGLE_SERVICE_ACCOUNT_JSON):
                return GoogleSheetsLoader()
            else:
                logger.warning(
                    "Google Sheets credentials or Sheet ID missing. Falling back to CSVLoader."
                )
                return CSVLoader()
        except Exception as e:
            logger.warning(f"Failed to initialize GoogleSheetsLoader ({e}). Using CSVLoader.")
            return CSVLoader()

    return CSVLoader()
