"""
Refresh service for managing manual and scheduled survey dataset refreshes.
"""

from typing import Dict, Any
from backend.services.analytics_service import analytics_service
from backend.utils.logger import logger


class RefreshService:
    """Handles dataset synchronization and refresh events."""

    @staticmethod
    def trigger_refresh() -> Dict[str, Any]:
        """Triggers a complete refresh of the analytics service cache."""
        logger.info("Manual/scheduled dataset refresh requested.")
        return analytics_service.refresh()


refresh_service = RefreshService()
