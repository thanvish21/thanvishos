import json
import datetime
from pathlib import Path
import sys

# Ensure engine is in path if running directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from engine.db import get_connection, init_db
from engine.srm_schedule import SRM_DO_CALENDAR, CT1_EXAMS

def populate_courses(conn):
    courses = [
        ("26BTB1001T", "Introduction to Computational Biology", 3, "THEORY", 1),
        ("26MEE1001L", "Workshop Practice", 2, "LAB", 1),
        ("26CYB1002J", "Chemistry for Computer Science", 4, "INTEGRATED", 1),
        ("26CSE1002J", "Programming for Problem Solving", 4, "INTEGRATED", 1),
        ("26MAB1001T", "Calculus and Linear Algebra", 4, "THEORY", 1),
        ("26LCA1005J", "Japanese", 3, "INTEGRATED", 1),
        ("26GNN1004L", "National Service Scheme", 2, "LAB", 1),
    ]

    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    for code, title, credits, c_type, mandatory in courses:
        cursor.execute(
            "INSERT OR REPLACE INTO courses (code, title, credits, course_type, mandatory, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (code, title, credits, c_type, mandatory, now)
        )
    conn.commit()

def populate_academic_calendar(conn):
    cursor = conn.cursor()
    for date_str, do in SRM_DO_CALENDAR.items():
        is_working = (do != "HOLIDAY")
        cursor.execute(
            "INSERT OR REPLACE INTO academic_calendar (date, day_order, is_working) VALUES (?, ?, ?)",
            (date_str, do, is_working)
        )
    conn.commit()

def populate_exams(conn):
    cursor = conn.cursor()

    # Clear exams to ensure clean idempotent migration
    cursor.execute("DELETE FROM exams")

    ct1_mapping = {
        "Programming for Problem Solving / C": "26CSE1002J",
        "Chemistry for Computer Science": "26CYB1002J",
        "Calculus and Linear Algebra (Mathematics)": "26MAB1001T",
        "Programming for Problem Solving": "26CSE1002J",
        "Foreign Language (Japanese)": "26LCA1005J",
        "Introduction to Computational Biology": "26BTB1001T"
    }

    for ex in CT1_EXAMS:
        times = ex["time"].split(" - ")
        start_time = times[0].strip() if len(times) > 0 else None
        end_time = times[1].strip() if len(times) > 1 else None

        status = "COMPLETED" if ex["completed"] else "SCHEDULED"
        c_code = ct1_mapping.get(ex["subject"], "UNKNOWN")
        exam_id = f"CT1_{c_code}_{ex['date']}"

        cursor.execute(
            "INSERT OR REPLACE INTO exams (id, exam_category, course_code, subject_name, exam_date, start_time, end_time, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (exam_id, "CT1", c_code, ex["subject"], ex["date"], start_time, end_time, status)
        )

    # Semester Exams (Dec 14-19)
    sem_exams = [
        ("26CSE1002J", "Programming for Problem Solving", "2026-12-14", "10:00", "13:00", "SCHEDULED"),
        ("26LCA1005J", "Japanese", "2026-12-15", "10:00", "13:00", "SCHEDULED"),
        ("26BTB1001T", "Introduction to Computational Biology", "2026-12-16", "10:00", "13:00", "SCHEDULED"),
        ("26CYB1002J", "Chemistry for Computer Science", "2026-12-17", "10:00", "13:00", "SCHEDULED"),
        ("26MAB1001T", "Calculus and Linear Algebra", "2026-12-19", "10:00", "13:00", "SCHEDULED"),
        ("26MEE1001L", "Workshop Practice", None, None, None, "DATE_NOT_PROVIDED"),
        ("26GNN1004L", "National Service Scheme", None, None, None, "DATE_NOT_PROVIDED")
    ]

    for c_code, subject, date, start_time, end_time, status in sem_exams:
        exam_id = f"SEM_{c_code}"
        cursor.execute(
            "INSERT OR REPLACE INTO exams (id, exam_category, course_code, subject_name, exam_date, start_time, end_time, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (exam_id, "SEMESTER", c_code, subject, date, start_time, end_time, status)
        )

    conn.commit()

def populate_attendance(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM courses")
    courses = cursor.fetchall()
    for row in courses:
        c_code = row["code"]
        cursor.execute(
            "INSERT OR REPLACE INTO attendance_records (course_code, classes_conducted, classes_attended, classes_missed, percentage, risk_status, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (c_code, 0, 0, 0, 0.0, "NOT_CONNECTED", "NOT_CONNECTED")
        )
    conn.commit()

def migrate_test_history(conn):
    test_history_path = Path(__file__).resolve().parent.parent / "data" / "personal" / "test_history.json"
    if not test_history_path.exists():
        print("test_history.json not found")
        return

    with open(test_history_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cursor = conn.cursor()
    cursor.execute("DELETE FROM weaknesses")
    cursor.execute("DELETE FROM test_attempts")

    now = datetime.datetime.now().isoformat()
    for entry in data:
        date = entry.get("date", now)
        attempt_id = f"attempt_{date}"
        topic = entry.get("topic", "Unknown")
        overall = entry.get("overall", 0)
        scores = entry.get("scores", {})

        cursor.execute("""
            INSERT OR REPLACE INTO test_attempts
            (id, date, topic, overall_score, conceptual_score, coding_score, debugging_score, interview_score, critical_thinking_score, answers_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt_id, date, topic, overall,
            scores.get("conceptual", 0),
            scores.get("coding", 0),
            scores.get("debugging", 0),
            scores.get("interview", 0),
            scores.get("critical_thinking", 0),
            "{}",
            now
        ))

        weaknesses = entry.get("weaknesses", [])
        for w in weaknesses:
            w_topic = w.get("topic", "Unknown")
            issue = w.get("issue", "Unknown")
            retest_in_days = w.get("retest_in_days", 1)

            try:
                dt = datetime.datetime.fromisoformat(date)
            except ValueError:
                dt = datetime.datetime.now()

            retest_date = (dt + datetime.timedelta(days=retest_in_days)).isoformat()

            cursor.execute("""
                INSERT INTO weaknesses
                (topic, issue, identified_date, retest_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (w_topic, issue, date, retest_date, "ACTIVE"))

    conn.commit()

def print_row_counts(conn):
    tables = [
        "courses",
        "academic_calendar",
        "exams",
        "attendance_records",
        "test_attempts",
        "weaknesses"
    ]
    print("\n--- Row Counts ---")
    cursor = conn.cursor()
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()["count"]
        print(f"{table}: {count}")

def main():
    print("Initializing DB...")
    init_db()
    conn = get_connection()
    try:
        print("Populating courses...")
        populate_courses(conn)
        print("Populating academic calendar...")
        populate_academic_calendar(conn)
        print("Populating exams...")
        populate_exams(conn)
        print("Populating attendance...")
        populate_attendance(conn)
        print("Migrating test history...")
        migrate_test_history(conn)

        print_row_counts(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
