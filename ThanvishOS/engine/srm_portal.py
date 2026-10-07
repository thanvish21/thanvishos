import datetime
from typing import Dict, Any, List, Optional
from ThanvishOS.engine.db import get_connection

class SRMPortalAdapter:
    """Adapter for interacting with the SRM Academia / Student Portal."""

    def __init__(self):
        self._init_state()

    def _init_state(self):
        """Initializes the sync state record in portal_sync_state if not present."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM portal_sync_state WHERE id = ?", ("srm_portal_main",))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO portal_sync_state (id, status, last_attempt, last_successful_sync, error_message, sync_interval_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("srm_portal_main", "NOT_CONNECTED", None, None, None, 60))
            conn.commit()
        conn.close()

    def _log_sync_attempt(self, event_type: str, details: str, status: str = "NOT_CONNECTED", error_msg: Optional[str] = None):
        """Logs a sync attempt and updates sync state in the database."""
        conn = get_connection()
        cursor = conn.cursor()
        now_iso = datetime.datetime.now().isoformat()

        # Update portal_sync_state
        cursor.execute("""
            UPDATE portal_sync_state
            SET status = ?, last_attempt = ?, error_message = ?
            WHERE id = ?
        """, (status, now_iso, error_msg, "srm_portal_main"))

        # Log to portal_events
        cursor.execute("""
            INSERT INTO portal_events (event_type, title, details, detected_at, acknowledged)
            VALUES (?, ?, ?, ?, ?)
        """, (event_type, f"Sync Attempt: {event_type}", details, now_iso, 0))

        conn.commit()
        conn.close()

    def _default_response(self, query_name: str) -> Dict[str, Any]:
        """Returns standard response for unauthenticated portal queries."""
        self._log_sync_attempt(
            event_type=f"QUERY_{query_name.upper()}",
            details=f"Attempted to fetch {query_name}, but credentials are not configured.",
            status="NOT_CONNECTED"
        )
        return {
            "status": "NOT_CONNECTED",
            "message": "SRM Portal integration awaiting authorized credentials. Zero fake data generated."
        }

    def get_attendance(self) -> Dict[str, Any]:
        """Fetches attendance data from SRM Portal."""
        return self._default_response("attendance")

    def get_marks(self) -> Dict[str, Any]:
        """Fetches internal/CT marks from SRM Portal."""
        return self._default_response("marks")

    def get_exams(self) -> Dict[str, Any]:
        """Fetches exam schedules from SRM Portal."""
        return self._default_response("exams")

    def get_assignments(self) -> Dict[str, Any]:
        """Fetches assignments and due dates from SRM Portal."""
        return self._default_response("assignments")

    def get_announcements(self) -> Dict[str, Any]:
        """Fetches official announcements from SRM Portal."""
        return self._default_response("announcements")

    def get_timetable(self) -> Dict[str, Any]:
        """Fetches timetable mapping from SRM Portal."""
        return self._default_response("timetable")

    def get_credits(self) -> Dict[str, Any]:
        """Fetches registered course credits from SRM Portal."""
        return self._default_response("credits")
