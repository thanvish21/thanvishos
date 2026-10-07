"""ThanvishOS Attendance Engine & What-If Projection Simulator.

Implements:
- Strict personal requirement of >= 90% in every subject.
- Mathematical attendance risk modeling:
    Projected % after N missed = (attended) / (conducted + N) * 100
    Projected % after N attended = (attended + N) / (conducted + N) * 100
    Classes needed to reach 90% = ceil((0.90 * conducted - attended) / 0.10)
    Classes allowed to miss = floor((attended - 0.90 * conducted) / 0.90)
- Day Order correlated attendance warnings:
    Checks if classes for high-risk subjects are scheduled today and flags warnings.
- NSS 2-period limit: NSS is strictly 2 periods, never 4.
"""

import math
from typing import Dict, Any, List, Optional
from ThanvishOS.engine.db import get_connection
from ThanvishOS.engine.srm_schedule import get_day_order, build_do_periods

def get_attendance_summary() -> Dict[str, Any]:
    """Returns attendance records, risk status, and today's schedule warnings."""
    today_schedule = get_day_order()
    today_do = today_schedule.get("day_order", "DO1")
    today_periods = build_do_periods(today_do)
    today_course_codes = {p["course_code"] for p in today_periods if p["type"] == "CLASS"}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.course_code, c.title, ar.classes_conducted, ar.classes_attended,
               ar.classes_missed, ar.percentage, ar.risk_status, ar.source
        FROM attendance_records ar
        JOIN courses c ON ar.course_code = c.code
        ORDER BY ar.course_code
    """)
    rows = cursor.fetchall()

    summary = []
    for r in rows:
        code = r["course_code"]
        conducted = r["classes_conducted"]
        attended = r["classes_attended"]
        pct = round(r["percentage"], 2)
        status = r["risk_status"]

        # Recalculate risk status dynamically based on current numbers
        if status != "NOT_CONNECTED":
            if conducted == 0:
                status = "NOT_CONNECTED"
            elif pct >= 90.0:
                status = "SAFE"
            elif pct >= 89.0:
                status = "WATCH"
            elif pct >= 75.0:
                status = "RISK"
            else:
                status = "CRITICAL"

        scheduled_today = code in today_course_codes
        flag_warning = (status in ["RISK", "CRITICAL", "WATCH"]) and scheduled_today

        summary.append({
            "code": code,
            "title": r["title"],
            "classes_conducted": conducted,
            "classes_attended": attended,
            "classes_missed": r["classes_missed"],
            "percentage": pct,
            "risk_status": status,
            "scheduled_today": scheduled_today,
            "flag_warning": flag_warning,
            "source": r["source"],
            "message": "Attendance data unavailable / AWAITING SYNC" if status == "NOT_CONNECTED" else f"Status: {status}"
        })

    conn.close()
    return {"records": summary, "date": today_schedule.get("date"), "day_order": today_do}

def simulate_what_if(course_code: str, miss_count: int = 0, attend_count: int = 0) -> Dict[str, Any]:
    """Simulates attendance percentage based on hypothetical attended and missed classes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT classes_conducted, classes_attended FROM attendance_records WHERE course_code = ?", (course_code,))
    row = cursor.fetchone()
    conn.close()

    if not row or row["classes_conducted"] == 0:
        return {
            "course_code": course_code,
            "current_conducted": 0,
            "current_attended": 0,
            "current_percentage": 0.0,
            "projected_percentage": 0.0,
            "classes_needed_for_90": 0,
            "classes_allowed_to_miss_for_90": 0,
            "status": "AWAITING_SYNC",
            "message": "Attendance data unlinked / Awaiting SRM Portal sync"
        }

    conducted = row["classes_conducted"]
    attended = row["classes_attended"]
    current_pct = round((attended / conducted) * 100, 2)

    total_new_conducted = conducted + miss_count + attend_count
    total_new_attended = attended + attend_count

    projected_pct = round((total_new_attended / total_new_conducted) * 100, 2) if total_new_conducted > 0 else 0.0

    # Classes needed to reach 90%: ceil((0.90 * conducted - attended) / 0.10)
    needed_raw = (0.90 * conducted - attended) / 0.10
    needed_to_90 = max(0, math.ceil(round(needed_raw, 8)))

    # Classes allowed to miss while staying >= 90%: floor((attended - 0.90 * conducted) / 0.90)
    allowed_raw = (attended - 0.90 * conducted) / 0.90
    allowed_to_miss = max(0, math.floor(round(allowed_raw, 8)))

    return {
        "course_code": course_code,
        "current_conducted": conducted,
        "current_attended": attended,
        "current_percentage": current_pct,
        "projected_percentage": projected_pct,
        "miss_scenario": {
            "miss_count": miss_count,
            "projected_percentage": round((attended / (conducted + miss_count)) * 100, 2) if (conducted + miss_count) > 0 else 0.0
        },
        "attend_scenario": {
            "attend_count": attend_count,
            "projected_percentage": round(((attended + attend_count) / (conducted + attend_count)) * 100, 2) if (conducted + attend_count) > 0 else 0.0
        },
        "classes_needed_for_90": needed_to_90,
        "classes_allowed_to_miss_for_90": allowed_to_miss,
        "status": "COMPUTED"
    }

def record_attendance_update(course_code: str, attended: int, conducted: int, source: str = "MANUAL") -> Dict[str, Any]:
    """Records real attendance numbers into the database and updates history."""
    if conducted < 0 or attended < 0 or attended > conducted:
        return {"error": "Invalid attendance numbers: attended must be between 0 and conducted."}

    percentage = round((attended / conducted) * 100, 2) if conducted > 0 else 0.0
    missed = conducted - attended

    if percentage >= 90.0:
        status = "SAFE"
    elif percentage >= 89.0:
        status = "WATCH"
    elif percentage >= 75.0:
        status = "RISK"
    else:
        status = "CRITICAL"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE attendance_records
        SET classes_conducted = ?, classes_attended = ?, classes_missed = ?,
            percentage = ?, risk_status = ?, source = ?, updated_at = datetime('now')
        WHERE course_code = ?
    """, (conducted, attended, missed, percentage, status, source, course_code))

    cursor.execute("""
        INSERT INTO attendance_history (course_code, date, classes_conducted, classes_attended, percentage, change_reason)
        VALUES (?, date('now'), ?, ?, ?, ?)
    """, (course_code, conducted, attended, percentage, f"Updated via {source}"))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "course_code": course_code,
        "conducted": conducted,
        "attended": attended,
        "percentage": percentage,
        "risk_status": status
    }
