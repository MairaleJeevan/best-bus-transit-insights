"""
BEST Bus Transit Insights - Flask Application Entry Point.
Serves REST API and Frontend Single Page Application.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.config import Config
from backend.routes.data_routes import data_bp
from backend.routes.analytics_routes import analytics_bp
from backend.utils.logger import logger


def create_app(config_class=Config) -> Flask:
    """Application factory for BEST Bus Transit Insights backend."""
    app = Flask(
        __name__,
        static_folder=str(config_class.FRONTEND_PATH),
        static_url_path="",
    )

    # Enable Cross-Origin Resource Sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API blueprints
    app.register_blueprint(data_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")

    # Serve Frontend Shell
    @app.route("/", methods=["GET"])
    def index():
        return send_from_directory(str(config_class.FRONTEND_PATH), "index.html")

    @app.route("/<path:filename>", methods=["GET"])
    def serve_static(filename):
        return send_from_directory(str(config_class.FRONTEND_PATH), filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal server error occurred"
        }), 500

    logger.info(
        f"Initialized BEST Bus Transit Insights App (Source: {config_class.DATA_SOURCE})"
    )
    return app


app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting server on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
