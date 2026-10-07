import pytest
import sqlite3
import math
from ThanvishOS.engine.db import init_db, get_connection
from ThanvishOS.engine.attendance import (
    get_risk_status,
    get_attendance_summary,
    simulate_what_if,
    record_attendance_update
)
from ThanvishOS.engine.srm_portal import SRMPortalAdapter
from ThanvishOS.engine.srm_schedule import get_day_order

@pytest.fixture(autouse=True)
def setup_test_db():
    """Ensure clean database state before each test."""
    init_db()
    yield

def test_risk_status_classifications():
    # NOT_CONNECTED
    assert get_risk_status(95.0, 0, "NOT_CONNECTED") == "NOT_CONNECTED"
    assert get_risk_status(0.0, 0, "PORTAL_SYNC") == "NOT_CONNECTED"
    assert get_risk_status(95.0, 10, "NOT_CONNECTED") == "NOT_CONNECTED"

    # SAFE >= 90.0%
    assert get_risk_status(90.0, 10, "PORTAL_SYNC") == "SAFE"
    assert get_risk_status(95.5, 20, "PORTAL_SYNC") == "SAFE"
    assert get_risk_status(100.0, 5, "PORTAL_SYNC") == "SAFE"

    # WATCH: 89.0% - 89.9%
    assert get_risk_status(89.0, 100, "PORTAL_SYNC") == "WATCH"
    assert get_risk_status(89.5, 100, "PORTAL_SYNC") == "WATCH"
    assert get_risk_status(89.9, 100, "PORTAL_SYNC") == "WATCH"

    # RISK: 75.0% - 88.9%
    assert get_risk_status(75.0, 100, "PORTAL_SYNC") == "RISK"
    assert get_risk_status(80.0, 20, "PORTAL_SYNC") == "RISK"
    assert get_risk_status(88.9, 100, "PORTAL_SYNC") == "RISK"

    # CRITICAL: < 75.0%
    assert get_risk_status(74.9, 100, "PORTAL_SYNC") == "CRITICAL"
    assert get_risk_status(50.0, 10, "PORTAL_SYNC") == "CRITICAL"
    assert get_risk_status(0.0, 1, "PORTAL_SYNC") == "CRITICAL"

def test_simulate_what_if_and_record_attendance():
    course_code = "26CYB1002J" # Chemistry

    # Record attendance update: 18 attended out of 20 conducted (90%)
    res = record_attendance_update(course_code, attended=18, conducted=20)
    assert res["status"] == "success"
    assert res["percentage"] == 90.0
    assert res["risk_status"] == "SAFE"

    # Simulate: If misses 2 classes -> attended=18, conducted=22 -> 18/22 = 81.818%
    sim = simulate_what_if(course_code, miss_count=2, attend_count=0)
    assert pytest.approx(sim["miss_scenario"]["projected_percentage"], 0.01) == 81.818
    assert sim["classes_needed_for_90"] == 0
    assert sim["classes_allowed_to_miss_for_90"] == 0

    # Simulate when attendance is 80% (16/20)
    record_attendance_update(course_code, attended=16, conducted=20)
    sim = simulate_what_if(course_code, miss_count=0, attend_count=5)
    # 21/25 = 84%
    assert pytest.approx(sim["attend_scenario"]["projected_percentage"], 0.01) == 84.0
    # Classes needed to reach 90%: ceil((0.90*20 - 16)/0.10) = ceil(2/0.10) = 20
    assert sim["classes_needed_for_90"] == 20
    assert sim["classes_allowed_to_miss_for_90"] == 0

    # Simulate when attendance is 100% (20/20)
    record_attendance_update(course_code, attended=20, conducted=20)
    sim = simulate_what_if(course_code, miss_count=0, attend_count=0)
    # Allowed to miss: floor((20 - 0.90*20)/0.90) = floor(2/0.90) = 2
    assert sim["classes_allowed_to_miss_for_90"] == 2
    assert sim["classes_needed_for_90"] == 0

def test_nss_attendance_rule():
    course_code = "26GNN1004L"
    # First reset NSS
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE attendance_records SET classes_conducted=0, classes_attended=0 WHERE course_code=?", (course_code,))
    conn.commit()
    conn.close()

    # If an update attempts to increment conducted by 4 periods, it should cap to 2 periods max
    res = record_attendance_update(course_code, attended=4, conducted=4)
    assert res["status"] == "success"
    assert res["conducted"] == 2
    assert res["attended"] == 2

def test_get_attendance_summary():
    # Set one course to RISK that is scheduled today or not
    record_attendance_update("26MAB1001T", attended=15, conducted=20) # 75% -> RISK
    summary = get_attendance_summary()
    assert "records" in summary
    assert "date" in summary
    assert "day_order" in summary

    math_record = next(r for r in summary["records"] if r["course_code"] == "26MAB1001T")
    assert math_record["status"] == "RISK"
    if math_record["scheduled_today"]:
        assert math_record["flag_warning"] is True

def test_srm_portal_adapter():
    adapter = SRMPortalAdapter()

    # Test all 7 required methods
    for method_name in ["get_attendance", "get_marks", "get_exams", "get_assignments", "get_announcements", "get_timetable", "get_credits"]:
        method = getattr(adapter, method_name)
        res = method()
        assert res["status"] == "NOT_CONNECTED"
        assert res["message"] == "SRM Portal integration awaiting authorized credentials. Zero fake data generated."

    # Verify portal_sync_state in DB
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM portal_sync_state WHERE id = 'srm_portal_main'")
    sync_state = dict(c.fetchone())
    assert sync_state["status"] == "NOT_CONNECTED"
    assert sync_state["last_attempt"] is not None

    # Verify portal_events logged
    c.execute("SELECT * FROM portal_events WHERE event_type LIKE 'QUERY_%'")
    events = c.fetchall()
    assert len(events) >= 7
    conn.close()
