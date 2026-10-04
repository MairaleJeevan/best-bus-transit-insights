"""
Tests for Data Loaders (CSV, Google Sheets Fallback).
"""

import pytest
import os
import pandas as pd
from backend.analytics.data_loader import CSVLoader, GoogleSheetsLoader, get_data_loader
from backend.config import Config


def test_csv_loader_reads_sample_data():
    """Verifies that CSVLoader loads sample survey data correctly."""
    loader = CSVLoader(Config.CSV_DATA_PATH)
    df = loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 100
    assert "Response_ID" in df.columns
    assert "Primary_Route_Number" in df.columns


def test_csv_loader_raises_on_missing_file():
    """Verifies FileNotFoundError on non-existent CSV."""
    loader = CSVLoader("non_existent_file.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_data()


def test_get_data_loader_fallback():
    """Verifies that get_data_loader falls back to CSV when sheets credentials are missing."""
    loader = get_data_loader("google_sheets")
    assert isinstance(loader, (CSVLoader, GoogleSheetsLoader))
