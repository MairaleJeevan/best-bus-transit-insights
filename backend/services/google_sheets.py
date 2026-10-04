"""
Google Sheets Integration Service for BEST Bus Transit Insights.
Uses gspread and google-auth to read responses from a connected Google Sheet.
"""

import os
from typing import List, Dict, Any, Optional
from backend.utils.logger import logger

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def fetch_sheet_records(
    sheet_id: str,
    credentials_path: str,
    worksheet_index: int = 0
) -> List[Dict[str, Any]]:
    """
    Fetches records from Google Sheets spreadsheet as list of dictionaries.

    Setup Instructions for Google Sheets API:
    1. Create a project in Google Cloud Console (https://console.cloud.google.com).
    2. Enable the Google Sheets API and Google Drive API.
    3. Create a Service Account, generate a JSON key, and save as `service_account.json`.
    4. Open the Google Sheet where responses are stored, click Share, and invite the
       Service Account email with 'Viewer' permissions.
    5. Put the Google Sheet ID and path in `.env`:
       GOOGLE_SHEET_ID=1abcXYZ...
       GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
    """
    if not GOOGLE_AUTH_AVAILABLE:
        raise RuntimeError("gspread or google-auth package is not installed.")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Google Service Account key not found at: {credentials_path}. "
            "Please follow the setup instructions in docs/05-data-design.md"
        )

    try:
        credentials = Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(worksheet_index)
        records = worksheet.get_all_records()
        logger.info(f"Successfully fetched {len(records)} rows from Google Sheet: {sheet_id}")
        return records
    except Exception as e:
        logger.error(f"Failed to fetch records from Google Sheets: {e}")
        raise e
