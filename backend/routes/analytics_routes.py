"""
Analytics endpoints for the BEST Bus Transit Insights API.
Calculates and serves dynamic analytical summaries and chart data.
"""

from flask import Blueprint, jsonify, request, Response
from datetime import datetime
from backend.services.analytics_service import analytics_service
from backend.utils.logger import logger

analytics_bp = Blueprint("analytics", __name__)


def _extract_filter_args(req) -> dict:
    """Extracts analytical query filters from request arguments."""
    filters = {}
    for key in [
        "route",
        "user_status",
        "age_group",
        "occupation",
        "frequency",
        "payment_method",
        "overcrowding",
        "bus_frequency",
        "schedule_reliability",
    ]:
        val = req.args.get(key)
        if val and val.strip().lower() != "all":
            filters[key] = val.strip()
    return filters


@analytics_bp.route("/analytics", methods=["GET"])
def get_full_analytics():
    """Returns complete analytics payload including KPIs, diagnostics, and charts."""
    try:
        filters = _extract_filter_args(request)
        payload = analytics_service.get_analytics(filters)
        return jsonify({
            "status": "success",
            "filters_applied": filters,
            "data": payload,
        }), 200
    except Exception as e:
        logger.error(f"Error generating analytics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@analytics_bp.route("/summary", methods=["GET"])
def get_summary():
    """Summary KPI metrics with optional query filtering."""
    try:
        filters = _extract_filter_args(request)
        payload = analytics_service.get_analytics(filters)
        return jsonify({
            "status": "success",
            "summary": payload["summary"],
            "validation": payload["validation"],
            "active_records": payload["active_record_count"],
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@analytics_bp.route("/routes", methods=["GET"])
def get_available_routes():
    """Returns unique route numbers found in the survey dataset."""
    options = analytics_service.get_filter_options()
    return jsonify({"status": "success", "routes": options["routes"]}), 200


@analytics_bp.route("/occupations", methods=["GET"])
def get_available_occupations():
    """Returns unique occupations found in the survey dataset."""
    options = analytics_service.get_filter_options()
    return jsonify({"status": "success", "occupations": options["occupations"]}), 200


@analytics_bp.route("/age-groups", methods=["GET"])
def get_available_age_groups():
    """Returns standard age group options."""
    options = analytics_service.get_filter_options()
    return jsonify({"status": "success", "age_groups": options["age_groups"]}), 200


@analytics_bp.route("/analytics/routes", methods=["GET"])
def get_route_analytics():
    """Returns Route Usage Distribution chart data."""
    filters = _extract_filter_args(request)
    payload = analytics_service.get_analytics(filters)
    return jsonify({"status": "success", "data": payload["charts"]["route_usage"]}), 200


@analytics_bp.route("/analytics/bottlenecks", methods=["GET"])
def get_bottleneck_analytics():
    """Returns Operational Bottlenecks chart data."""
    filters = _extract_filter_args(request)
    payload = analytics_service.get_analytics(filters)
    return jsonify({"status": "success", "data": payload["charts"]["bottlenecks"]}), 200


@analytics_bp.route("/analytics/overcrowding", methods=["GET"])
def get_overcrowding_analytics():
    """Returns Overcrowding and peak reliability chart data."""
    filters = _extract_filter_args(request)
    payload = analytics_service.get_analytics(filters)
    return jsonify({
        "status": "success",
        "data": {
            "peak_reliability": payload["charts"]["peak_reliability"],
            "overcrowding_pct": payload["summary"]["overcrowding_pct"],
        }
    }), 200


@analytics_bp.route("/analytics/payments", methods=["GET"])
def get_payment_analytics():
    """Returns Payment method distribution chart data."""
    filters = _extract_filter_args(request)
    payload = analytics_service.get_analytics(filters)
    return jsonify({"status": "success", "data": payload["charts"]["payments"]}), 200


@analytics_bp.route("/analytics/hourly", methods=["GET"])
def get_hourly_analytics():
    """Returns Hourly overcrowding vs bus frequency trend."""
    filters = _extract_filter_args(request)
    payload = analytics_service.get_analytics(filters)
    return jsonify({"status": "success", "data": payload["charts"]["hourly_trend"]}), 200


@analytics_bp.route("/export-csv", methods=["GET"])
def export_filtered_csv():
    """Exports current filtered survey records as a downloadable CSV file."""
    try:
        filters = _extract_filter_args(request)
        csv_content = analytics_service.export_filtered_csv(filters)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"best_bus_filtered_data_{today}.csv"

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Error exporting filtered CSV: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
