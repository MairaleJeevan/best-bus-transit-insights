"""
Vercel Serverless Function entry point for BEST Bus Transit Insights.
"""

import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app import app

# Vercel WSGI entry point
# Exports the Flask 'app' instance
