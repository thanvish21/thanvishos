"""SRM Mess Menu Engine.

Handles tracking and syncing of the hostel mess menu.
Supports setting menus, checking current meals, and integrating with constraints (e.g. exams).
"""

import datetime
import re
from typing import Dict, Any, Optional

from ThanvishOS.engine.db import get_connection

def parse_time_to_minutes(t_str: str) -> int:
    """Parses a time string like '12:30 PM' or '14:10' into minutes since midnight."""
    t_str = t_str.strip().upper()
    is_pm = 'PM' in t_str
    is_am = 'AM' in t_str
    clean = re.sub(r'[^\d:]', '', t_str)
    parts = clean.split(':')
    if not parts or not parts[0]:
        raise ValueError("Invalid time string")
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if is_pm and hours < 12:
        hours += 12
    elif is_am and hours == 12:
        hours = 0
    return hours * 60 + minutes

def check_lunch_overlap(start_str: str, end_str: Optional[str] = None) -> bool:
    """Checks if a given time range overlaps with standard lunch window (12:30 to 14:00)."""
    if "-" in start_str and not end_str:
        parts = start_str.split("-")
        start_str = parts[0]
        end_str = parts[1] if len(parts) > 1 else None

    if not start_str:
        return False

    try:
        start_min = parse_time_to_minutes(start_str)
        end_min = parse_time_to_minutes(end_str) if end_str else start_min + 60
    except Exception:
        return False

    lunch_start = 12 * 60 + 30 # 750
    lunch_end = 14 * 60 # 840

    # Overlaps if start is before lunch_end AND end is after lunch_start
    return start_min < lunch_end and end_min > lunch_start

class SRMMessAdapter:
    def __init__(self):
        self._ensure_sync_state()

    def _ensure_sync_state(self):
        """Ensures that the initial sync state exists in the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM mess_sync_state WHERE id = 'current'")
        row = cursor.fetchone()
        if not row:
            cursor.execute(
                "INSERT INTO mess_sync_state (id, status, last_sync, source_type) VALUES (?, ?, ?, ?)",
                ("current", "NOT_CONNECTED", None, "NOT_PROVIDED")
            )
            conn.commit()
        conn.close()

    def get_sync_state(self) -> str:
        """Returns the current mess sync state."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM mess_sync_state WHERE id = 'current'")
        row = cursor.fetchone()
        conn.close()
        return row["status"] if row else "NOT_CONNECTED"

    def set_sync_state(self, status: str, source_type: Optional[str] = None):
        """Sets the sync state status (NOT_CONNECTED, AWAITING_MENU, SYNCED)."""
        now = datetime.datetime.now().isoformat()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE mess_sync_state
            SET status = ?, last_sync = ?, source_type = COALESCE(?, source_type)
            WHERE id = 'current'
        """, (status, now, source_type))
        conn.commit()
        conn.close()

    def _get_exams_for_date(self, date_str: str) -> list:
        """Returns a list of exams scheduled for a given date from the database and fallback."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT subject_name, start_time, end_time FROM exams WHERE exam_date = ?", (date_str,))
        rows = cursor.fetchall()
        conn.close()

        exams = [dict(row) for row in rows]

        # Fallback to schedule CT1_EXAMS if db is empty for that date
        if not exams:
            try:
                from ThanvishOS.engine.srm_schedule import CT1_EXAMS
                for ex in CT1_EXAMS:
                    if ex.get("date") == date_str:
                        # Extract start/end from "time"
                        t_str = ex.get("time", "")
                        parts = t_str.split("-") if "-" in t_str else [t_str]
                        exams.append({
                            "subject_name": ex.get("subject"),
                            "start_time": parts[0].strip() if parts else "",
                            "end_time": parts[1].strip() if len(parts) > 1 else ""
                        })
            except ImportError:
                pass

        return exams

    def get_today_mess(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        """Returns the mess menu for the specified date, adjusting for constraints."""
        if date_str is None:
            date_str = datetime.date.today().isoformat()

        status = self.get_sync_state()

        default_timings = {
            "breakfast": "07:30–09:00",
            "lunch": "12:30–14:00",
            "snacks": "16:30–17:30",
            "dinner": "19:30–21:00"
        }

        # Initialize the baseline result for missing/un-synced menu
        result_missing = {
            "status": "AWAITING_MENU",
            "message": "Mess menu unavailable — upload hostel menu PDF/text in Brain Dump",
            "menu": None,
            "timings": default_timings
        }

        exams = self._get_exams_for_date(date_str)
        has_lunch_overlap = False
        for exam in exams:
            if check_lunch_overlap(exam["start_time"], exam.get("end_time")):
                has_lunch_overlap = True
                break

        if has_lunch_overlap:
            result_missing["constraint_note"] = "Exam overlaps standard lunch window — plan meal before 12:00 or after 14:15"

        if status != "SYNCED":
            return result_missing

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mess_menu WHERE date = ?", (date_str,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return result_missing

        timings = {
            "breakfast": row["breakfast_timings"] or default_timings["breakfast"],
            "lunch": row["lunch_timings"] or default_timings["lunch"],
            "snacks": row["snacks_timings"] or default_timings["snacks"],
            "dinner": row["dinner_timings"] or default_timings["dinner"]
        }

        menu = {
            "breakfast": row["breakfast"],
            "lunch": row["lunch"],
            "snacks": row["snacks"],
            "dinner": row["dinner"],
            "special_notes": row["special_notes"]
        }

        result = {
            "status": "SYNCED",
            "message": "Mess menu loaded.",
            "menu": menu,
            "timings": timings
        }

        if has_lunch_overlap:
            result["constraint_note"] = "Exam overlaps standard lunch window — plan meal before 12:00 or after 14:15"

        return result

    def save_mess_menu(
        self,
        date: str,
        breakfast: Optional[str],
        lunch: Optional[str],
        snacks: Optional[str],
        dinner: Optional[str],
        timings: Optional[Dict[str, str]] = None,
        source: str = "MANUAL",
        special_notes: Optional[str] = None
    ):
        """Saves a day's mess menu."""
        if timings is None:
            timings = {}

        b_time = timings.get("breakfast")
        l_time = timings.get("lunch")
        s_time = timings.get("snacks")
        d_time = timings.get("dinner")

        now = datetime.datetime.now().isoformat()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mess_menu (date, breakfast, breakfast_timings, lunch, lunch_timings, snacks, snacks_timings, dinner, dinner_timings, special_notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                breakfast=excluded.breakfast,
                breakfast_timings=excluded.breakfast_timings,
                lunch=excluded.lunch,
                lunch_timings=excluded.lunch_timings,
                snacks=excluded.snacks,
                snacks_timings=excluded.snacks_timings,
                dinner=excluded.dinner,
                dinner_timings=excluded.dinner_timings,
                special_notes=excluded.special_notes,
                updated_at=excluded.updated_at
        """, (date, breakfast, b_time, lunch, l_time, snacks, s_time, dinner, d_time, special_notes, now))

        # Update sync state to SYNCED
        cursor.execute("""
            UPDATE mess_sync_state
            SET status = 'SYNCED', last_sync = ?, source_type = ?
            WHERE id = 'current'
        """, (now, source))

        conn.commit()
        conn.close()
