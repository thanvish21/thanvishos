"""ThanvishOS Verification Agent (Agent 10) & Automated System Auditor.

Implements automated system integrity audits:
- Verifies SQLite database tables exist and have rows.
- Verifies SRM Day Order calculation against calendar.
- Verifies NSS 2-period rule (P1+P2 or P3+P4, never 4).
- Verifies exam dates and countdown calculation.
- Verifies that no fake attendance or fake portal data is shown.
- Verifies test evaluation rubric dimensions.
- Records check results to `system_verifications` table.
- Returns structured {"overall_status": "VERIFIED", "checks": [...]}.
"""

import datetime
import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Ensure project paths are in sys.path
_parent_dir = str(Path(__file__).resolve().parent.parent)
_grandparent_dir = str(Path(__file__).resolve().parent.parent.parent)
for p in [_parent_dir, _grandparent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from ThanvishOS.engine.db import get_connection, init_db
    from ThanvishOS.engine.srm_schedule import get_day_order, build_do_periods, SRM_DO_CALENDAR, CT1_EXAMS
    from ThanvishOS.engine.daily_test import QUESTION_BANK, evaluate_test_submission
    from ThanvishOS.engine.agents_runner import log_agent_execution
except ImportError:
    from engine.db import get_connection, init_db
    from engine.srm_schedule import get_day_order, build_do_periods, SRM_DO_CALENDAR, CT1_EXAMS
    from engine.daily_test import QUESTION_BANK, evaluate_test_submission
    from engine.agents_runner import log_agent_execution

def _save_verification_record(cursor, component: str, check_name: str, status: str, evidence: str):
    """Inserts a verification result into the system_verifications table."""
    now = datetime.datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO system_verifications (component, check_name, status, evidence, verified_at)
        VALUES (?, ?, ?, ?, ?)
    """, (component, check_name, status, evidence, now))

def run_system_verification() -> Dict[str, Any]:
    """Runs a full suite of automated system integrity checks and logs to database."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    checks = []
    has_failure = False
    has_warning = False

    def add_check(component: str, check_name: str, status: str, evidence: str):
        nonlocal has_failure, has_warning
        _save_verification_record(cursor, component, check_name, status, evidence)
        checks.append({
            "component": component,
            "check_name": check_name,
            "status": status,
            "evidence": evidence
        })
        if status == "FAIL":
            has_failure = True
        elif status == "WARNING":
            has_warning = True

    # -------------------------------------------------------------
    # Check 1: SQLite Database Tables & Row Integrity
    # -------------------------------------------------------------
    expected_tables = [
        'users', 'courses', 'course_schedule', 'academic_calendar', 'nss_occurrences',
        'attendance_targets', 'attendance_records', 'attendance_history', 'exams',
        'portal_sync_state', 'portal_events', 'mess_sync_state', 'mess_menu',
        'daily_plans', 'tasks', 'skills', 'test_questions', 'test_attempts',
        'weaknesses', 'brain_dumps', 'agent_telemetry', 'agent_runs', 'system_verifications'
    ]
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {row[0] for row in cursor.fetchall()}
    missing_tables = [t for t in expected_tables if t not in existing_tables]

    if missing_tables:
        add_check(
            component="database",
            check_name="table_existence",
            status="FAIL",
            evidence=f"Missing expected SQLite tables: {', '.join(missing_tables)}"
        )
    else:
        cursor.execute("SELECT COUNT(*) FROM academic_calendar")
        calendar_rows = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM courses")
        courses_rows = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM exams")
        exams_rows = cursor.fetchone()[0]

        if calendar_rows > 0 and courses_rows > 0 and exams_rows > 0:
            add_check(
                component="database",
                check_name="table_existence_and_data",
                status="PASS",
                evidence=f"All {len(expected_tables)} tables present. Rows: academic_calendar={calendar_rows}, courses={courses_rows}, exams={exams_rows}."
            )
        else:
            add_check(
                component="database",
                check_name="table_existence_and_data",
                status="WARNING",
                evidence=f"All tables exist, but some core tables have 0 rows (calendar={calendar_rows}, courses={courses_rows}, exams={exams_rows})."
            )

    # -------------------------------------------------------------
    # Check 2: SRM Day Order Calculation against Calendar
    # -------------------------------------------------------------
    test_dates = [
        ("2026-09-01", "DO4"),
        ("2026-09-03", "DO1"),
        ("2026-10-02", "HOLIDAY"),
        ("2026-10-08", "DO3")
    ]
    mismatches = []
    for dt, expected_do in test_dates:
        actual_result = get_day_order(dt)
        actual_do = actual_result.get("day_order")
        if actual_do != expected_do:
            mismatches.append(f"{dt}: expected {expected_do}, got {actual_do}")

    if mismatches:
        add_check(
            component="srm_schedule",
            check_name="day_order_calendar_mapping",
            status="FAIL",
            evidence=f"Day Order computation failed on: {'; '.join(mismatches)}"
        )
    else:
        add_check(
            component="srm_schedule",
            check_name="day_order_calendar_mapping",
            status="PASS",
            evidence="Rotating Day Order matches authoritative calendar without weekday assumptions (verified DO1, DO3, DO4, and HOLIDAY)."
        )

    # -------------------------------------------------------------
    # Check 3: NSS 2-Period Rule (P1+P2 or P3+P4, never 4)
    # -------------------------------------------------------------
    periods_a = build_do_periods("DO2", "A")
    periods_b = build_do_periods("DO2", "B")

    nss_a_periods = [p["period"] for p in periods_a if p["type"] == "NSS" or "NSS Active Block" in p.get("subject", "")]
    nss_b_periods = [p["period"] for p in periods_b if p["type"] == "NSS" or "NSS Active Block" in p.get("subject", "")]

    batch_a_valid = (set(nss_a_periods) == {"P1", "P2"} and len(nss_a_periods) == 2)
    batch_b_valid = (set(nss_b_periods) == {"P3", "P4"} and len(nss_b_periods) == 2)

    if batch_a_valid and batch_b_valid:
        add_check(
            component="srm_schedule",
            check_name="nss_2_period_rule",
            status="PASS",
            evidence="NSS block rule strictly enforced: Batch A gets P1+P2 (2 periods), Batch B gets P3+P4 (2 periods). Never all 4."
        )
    else:
        add_check(
            component="srm_schedule",
            check_name="nss_2_period_rule",
            status="FAIL",
            evidence=f"NSS block rule violation! Batch A: {nss_a_periods}, Batch B: {nss_b_periods}"
        )

    # -------------------------------------------------------------
    # Check 4: Exam Dates and Countdown Calculation
    # -------------------------------------------------------------
    # Verify CT1 schedule and alert generation
    try:
        # Check tomorrow alert for 2026-10-08 (Math exam is 2026-10-09)
        oct_08_res = get_day_order("2026-10-08")
        alert = oct_08_res.get("exam_alert")
        has_correct_alert = alert is not None and "Calculus" in alert.get("subject", "")

        # Check today alert for 2026-10-09
        oct_09_res = get_day_order("2026-10-09")
        today_alert = oct_09_res.get("exam_alert")
        has_today_alert = today_alert is not None and today_alert.get("urgency") == "TODAY"

        if has_correct_alert and has_today_alert and len(CT1_EXAMS) >= 6:
            add_check(
                component="exams",
                check_name="exam_countdown_and_alerts",
                status="PASS",
                evidence=f"Verified {len(CT1_EXAMS)} CT1 exams. Tomorrow and Today countdown alerts trigger accurately."
            )
        else:
            add_check(
                component="exams",
                check_name="exam_countdown_and_alerts",
                status="FAIL",
                evidence=f"Exam alert failure: Oct 8 alert={alert}, Oct 9 alert={today_alert}"
            )
    except Exception as e:
        add_check(
            component="exams",
            check_name="exam_countdown_and_alerts",
            status="FAIL",
            evidence=f"Exception during exam countdown evaluation: {str(e)}"
        )

    # -------------------------------------------------------------
    # Check 5: No Fake Attendance or Fake Portal Data
    # -------------------------------------------------------------
    cursor.execute("""
        SELECT course_code, classes_conducted, classes_attended, percentage, risk_status, source
        FROM attendance_records
    """)
    att_rows = cursor.fetchall()

    fake_data_detected = False
    fake_reasons = []

    for row in att_rows:
        source = row["source"]
        percentage = row["percentage"]
        conducted = row["classes_conducted"]
        risk_status = row["risk_status"]

        if source == "NOT_CONNECTED":
            if percentage != 0.0 or conducted != 0 or risk_status != "NOT_CONNECTED":
                fake_data_detected = True
                fake_reasons.append(f"{row['course_code']} has {percentage}% despite NOT_CONNECTED source")

    if not fake_data_detected and len(att_rows) > 0:
        add_check(
            component="portal_attendance",
            check_name="no_fake_portal_data",
            status="PASS",
            evidence=f"All {len(att_rows)} attendance records adhere to the zero-fake-data policy. Unconnected courses show NOT_CONNECTED with 0%."
        )
    elif fake_data_detected:
        add_check(
            component="portal_attendance",
            check_name="no_fake_portal_data",
            status="FAIL",
            evidence=f"Fake attendance data detected: {'; '.join(fake_reasons)}"
        )
    else:
        add_check(
            component="portal_attendance",
            check_name="no_fake_portal_data",
            status="WARNING",
            evidence="Attendance table is empty; zero fake data present by default."
        )

    # -------------------------------------------------------------
    # Check 6: Test Evaluation Rubric Dimensions
    # -------------------------------------------------------------
    required_dimensions = {"conceptual", "coding", "debugging", "critical_thinking"}
    found_dimensions = set()

    for topic_key, questions in QUESTION_BANK.items():
        for q in questions:
            if "rubric_dimension" in q:
                found_dimensions.add(q["rubric_dimension"])

    eval_result = evaluate_test_submission({"calc-l1-02": "C", "py-l1-01": "Prints [1, 2, 3, 4]"}, "calculus_maths")
    eval_scores = eval_result.get("scores", {})

    has_all_dims = required_dimensions.issubset(found_dimensions)
    eval_valid = len(eval_scores) >= 4 and "overall_score" in eval_result

    if has_all_dims and eval_valid:
        add_check(
            component="testing_engine",
            check_name="rubric_dimensions_integrity",
            status="PASS",
            evidence=f"All {len(required_dimensions)} rubric dimensions ({', '.join(sorted(required_dimensions))}) present in question bank and evaluation returns {len(eval_scores)} scoring dimensions."
        )
    else:
        add_check(
            component="testing_engine",
            check_name="rubric_dimensions_integrity",
            status="FAIL",
            evidence=f"Missing rubric dimensions. Found in bank: {found_dimensions}, returned scores: {list(eval_scores.keys())}"
        )

    # -------------------------------------------------------------
    # Finalize Overall Status & Telemetry Update
    # -------------------------------------------------------------
    if has_failure:
        overall_status = "FAILED"
    elif has_warning:
        overall_status = "WARNING"
    else:
        overall_status = "VERIFIED"

    now_iso = datetime.datetime.now().isoformat()

    # Update agent_telemetry last_verified
    cursor.execute("""
        UPDATE agent_telemetry
        SET last_verified = ?,
            verified_by = 'agent-verification-auditor'
    """, (now_iso,))

    conn.commit()
    conn.close()

    # Log execution for Agent 10
    log_agent_execution(
        agent_id="agent-verification-auditor",
        task_name="system_integrity_verification",
        status="SUCCESS" if overall_status in ["VERIFIED", "WARNING"] else "FAILED",
        details=json.dumps({"overall_status": overall_status, "checks_count": len(checks)})
    )

    return {
        "overall_status": overall_status,
        "verified_at": now_iso,
        "auditor": "agent-verification-auditor (Agent 10)",
        "checks_count": len(checks),
        "checks": checks
    }

if __name__ == "__main__":
    report = run_system_verification()
    print(json.dumps(report, indent=2))
