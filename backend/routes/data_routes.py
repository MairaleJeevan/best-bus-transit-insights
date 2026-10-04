"""
Data management and health check endpoints for BEST Bus Transit Insights API.
"""

from flask import Blueprint, jsonify, request
import pandas as pd
import io
from backend.config import Config
from backend.services.analytics_service import analytics_service
from backend.services.refresh_service import refresh_service
from backend.utils.validation import validate_file_extension
from backend.utils.logger import logger

data_bp = Blueprint("data", __name__)


@data_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend status."""
    return jsonify({
        "status": "healthy",
        "service": "BEST Bus Transit Insights API",
        "version": "1.0.0",
        "data_source": Config.DATA_SOURCE,
    }), 200


@data_bp.route("/data", methods=["GET"])
def get_raw_data():
    """Returns sample records from the cleaned survey DataFrame."""
    try:
        limit = int(request.args.get("limit", 100))
        df = analytics_service.get_cleaned_dataframe()
        records = df.head(limit).to_dict(orient="records")
        return jsonify({
            "status": "success",
            "total_records": len(df),
            "returned_records": len(records),
            "data_source": Config.DATA_SOURCE,
            "records": records,
        }), 200
    except Exception as e:
        logger.error(f"Error fetching raw data records: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@data_bp.route("/refresh", methods=["POST"])
def refresh_data():
    """Forces synchronization from Google Sheets or CSV."""
    try:
        source_override = request.json.get("data_source") if request.is_json and request.json else None
        result = analytics_service.refresh(source_override)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error refreshing dataset: {e}")
        return jsonify({"status": "error", "message": f"Unable to refresh survey data: {e}"}), 500


@data_bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    """Accepts CSV file upload, validates schema, and updates active analytics."""
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"}), 400

        file = request.files["file"]
        if not file or file.filename == "":
            return jsonify({"status": "error", "message": "No file selected"}), 400

        if not validate_file_extension(file.filename, Config.ALLOWED_EXTENSIONS):
            return jsonify({
                "status": "error",
                "message": "Invalid file format. Only CSV files are supported."
            }), 400

        # Read CSV into DataFrame
        content = file.stream.read().decode("utf-8", errors="ignore")
        if not content.strip():
            return jsonify({"status": "error", "message": "Uploaded CSV file is empty"}), 400

        df = pd.read_csv(io.StringIO(content))
        if df.empty:
            return jsonify({"status": "error", "message": "Uploaded CSV contains no records"}), 400

        analytics_service.set_custom_dataset(df)
        logger.info(f"Custom CSV uploaded successfully with {len(df)} records.")

        return jsonify({
            "status": "success",
            "message": f"Successfully uploaded and analyzed {len(df)} survey responses!",
            "filename": file.filename,
            "validation": analytics_service.cached_validation,
        }), 200
    except Exception as e:
        logger.error(f"Error handling CSV upload: {e}")
        return jsonify({"status": "error", "message": f"CSV processing error: {e}"}), 500
