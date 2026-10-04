"""
Configuration module for BEST Bus Transit Insights application.
Handles environment variables and application-wide settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"

# Load .env if present
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration parameters."""

    # Server settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    PORT = int(os.getenv("PORT", "5000"))
    HOST = os.getenv("HOST", "127.0.0.1")

    # Data Source ("csv" or "google_sheets")
    DATA_SOURCE = os.getenv("DATA_SOURCE", "csv").lower()

    # CSV File Settings
    CSV_DATA_PATH = os.getenv("CSV_DATA_PATH", str(DATA_DIR / "sample_data.csv"))
    if not os.path.isabs(CSV_DATA_PATH):
        CSV_DATA_PATH = str(BASE_DIR / CSV_DATA_PATH)

    # Google Sheets Settings
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
    GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON", str(BASE_DIR / "service_account.json")
    )
    if not os.path.isabs(GOOGLE_SERVICE_ACCOUNT_JSON):
        GOOGLE_SERVICE_ACCOUNT_JSON = str(BASE_DIR / GOOGLE_SERVICE_ACCOUNT_JSON)
    GOOGLE_SHEET_RANGE = os.getenv("GOOGLE_SHEET_RANGE", "Form Responses 1!A:Z")

    # Auto-Refresh Settings (seconds; 0 = off)
    AUTO_REFRESH_INTERVAL = int(os.getenv("AUTO_REFRESH_INTERVAL", "0"))

    # Paths
    BASE_PATH = BASE_DIR
    FRONTEND_PATH = FRONTEND_DIR
    DATA_PATH = DATA_DIR

    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {"csv"}
