"""ThanvishOS Canonical Database Engine & Persistence Layer.

Provides unified database access supporting SQLite (for local development/offline)
and PostgreSQL (for hosted production). Implements Master Specification v4.0.
"""

import os
import sqlite3
import datetime
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_DB_PATH = DATA_DIR / "thanvishos.db"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")

IS_POSTGRES = DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")

if IS_POSTGRES:
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        IS_POSTGRES = False

class PostgresCursorWrapper:
    """Wraps psycopg2 cursor to provide sqlite3-like parameter binding and dict access."""
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query: str, params: Optional[Tuple[Any, ...]] = None):
        # Translate SQLite ? placeholders to Postgres %s placeholders
        pg_query = query.replace("?", "%s")
        # Handle SQLite-specific keywords for Postgres DDL
        pg_query = pg_query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        pg_query = pg_query.replace("BOOLEAN DEFAULT 1", "BOOLEAN DEFAULT TRUE")
        pg_query = pg_query.replace("BOOLEAN DEFAULT 0", "BOOLEAN DEFAULT FALSE")
        pg_query = pg_query.replace("datetime('now')", "NOW()")
        pg_query = pg_query.replace("date('now')", "CURRENT_DATE")

        if params is not None:
            return self._cursor.execute(pg_query, params)
        return self._cursor.execute(pg_query)

    def executemany(self, query: str, params_seq):
        pg_query = query.replace("?", "%s")
        return self._cursor.executemany(pg_query, params_seq)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def __iter__(self):
        return iter(self._cursor)

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def close(self):
        return self._cursor.close()

class PostgresConnectionWrapper:
    """Wraps psycopg2 connection to mirror sqlite3 API."""
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return PostgresCursorWrapper(self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor))

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

def get_connection():
    """Returns a connection to either PostgreSQL or SQLite depending on DATABASE_URL."""
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return PostgresConnectionWrapper(conn)

    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes all canonical tables with proper foreign keys and timestamps."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        institution TEXT NOT NULL,
        degree TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Courses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        code TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        credits INTEGER DEFAULT 3,
        course_type TEXT NOT NULL,
        mandatory BOOLEAN DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)

    # 3. Course Schedule / Day Order Mapping
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_order TEXT NOT NULL,
        period TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        course_code TEXT,
        activity_type TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (course_code) REFERENCES courses(code)
    )
    """)

    # 4. Day Orders & Academic Calendar
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS academic_calendar (
        date TEXT PRIMARY KEY,
        day_order TEXT NOT NULL,
        is_working BOOLEAN NOT NULL,
        holiday_reason TEXT,
        notes TEXT
    )
    """)

    # 5. NSS Occurrences & Batch Preference
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nss_occurrences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL UNIQUE,
        assigned_batch TEXT NOT NULL,
        status TEXT NOT NULL,
        source TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 6. Attendance Targets & Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_targets (
        course_code TEXT PRIMARY KEY,
        personal_target REAL DEFAULT 90.0,
        university_min REAL DEFAULT 75.0,
        FOREIGN KEY (course_code) REFERENCES courses(code)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_records (
        course_code TEXT PRIMARY KEY,
        classes_conducted INTEGER DEFAULT 0,
        classes_attended INTEGER DEFAULT 0,
        classes_missed INTEGER DEFAULT 0,
        percentage REAL DEFAULT 0.0,
        risk_status TEXT NOT NULL,
        last_sync TEXT,
        source TEXT NOT NULL,
        FOREIGN KEY (course_code) REFERENCES courses(code)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL,
        recorded_at TEXT NOT NULL,
        conducted INTEGER NOT NULL,
        attended INTEGER NOT NULL,
        percentage REAL NOT NULL,
        FOREIGN KEY (course_code) REFERENCES courses(code)
    )
    """)

    # 7. Exams (CT1, CT2, Semester)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id TEXT PRIMARY KEY,
        exam_category TEXT NOT NULL,
        course_code TEXT NOT NULL,
        subject_name TEXT NOT NULL,
        exam_date TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT NOT NULL,
        syllabus_status TEXT,
        preparation_percent INTEGER DEFAULT 0,
        FOREIGN KEY (course_code) REFERENCES courses(code)
    )
    """)

    # 8. Portal Sync State & Events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portal_sync_state (
        id TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        last_attempt TEXT,
        last_successful_sync TEXT,
        error_message TEXT,
        sync_interval_minutes INTEGER DEFAULT 60
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portal_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        title TEXT NOT NULL,
        details TEXT NOT NULL,
        detected_at TEXT NOT NULL,
        acknowledged BOOLEAN DEFAULT 0
    )
    """)

    # 9. SRM Mess System
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_sync_state (
        id TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        last_sync TEXT,
        source_type TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_menu (
        date TEXT PRIMARY KEY,
        breakfast TEXT,
        breakfast_timings TEXT,
        lunch TEXT,
        lunch_timings TEXT,
        snacks TEXT,
        snacks_timings TEXT,
        dinner TEXT,
        dinner_timings TEXT,
        special_notes TEXT,
        updated_at TEXT NOT NULL
    )
    """)

    # 10. Daily Plans & Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_plans (
        date TEXT PRIMARY KEY,
        day_order TEXT NOT NULL,
        plan_summary TEXT NOT NULL,
        academic_priority TEXT NOT NULL,
        technical_learning TEXT NOT NULL,
        building_goal TEXT,
        testing_goal TEXT,
        what_not_to_do TEXT NOT NULL,
        why_these_priorities TEXT NOT NULL,
        free_time_windows TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        estimated_minutes INTEGER DEFAULT 30,
        due_date TEXT,
        priority TEXT NOT NULL,
        reason TEXT,
        created_at TEXT NOT NULL,
        completed_at TEXT
    )
    """)

    # 11. Skills & Polyglot Matrix
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        progress_percent INTEGER DEFAULT 0,
        color_class TEXT,
        target_hours INTEGER DEFAULT 100,
        logged_hours REAL DEFAULT 0.0,
        last_practiced TEXT
    )
    """)

    # 12. Adaptive Tests, Questions, Weaknesses & Retests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_questions (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        level INTEGER NOT NULL,
        level_name TEXT NOT NULL,
        question_format TEXT NOT NULL,
        question_text TEXT NOT NULL,
        expected_points TEXT NOT NULL,
        rubric_dimension TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_attempts (
        id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        topic TEXT NOT NULL,
        overall_score INTEGER NOT NULL,
        conceptual_score INTEGER NOT NULL,
        coding_score INTEGER NOT NULL,
        debugging_score INTEGER NOT NULL,
        interview_score INTEGER NOT NULL,
        critical_thinking_score INTEGER NOT NULL,
        strongest_area TEXT,
        weakest_area TEXT,
        answers_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weaknesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        issue TEXT NOT NULL,
        evidence TEXT,
        identified_date TEXT NOT NULL,
        retest_date TEXT NOT NULL,
        status TEXT NOT NULL,
        resolved_at TEXT
    )
    """)

    # 13. Brain Dumps & Local Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS brain_dumps (
        id TEXT PRIMARY KEY,
        content_type TEXT NOT NULL,
        title TEXT,
        raw_content TEXT,
        file_path TEXT,
        tags TEXT,
        dumped_at TEXT NOT NULL
    )
    """)

    # 14. Real Agent Telemetry & Verification Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_telemetry (
        agent_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL,
        avatar TEXT NOT NULL,
        color TEXT NOT NULL,
        current_task TEXT,
        last_started TEXT,
        last_finished TEXT,
        success_count INTEGER DEFAULT 0,
        failure_count INTEGER DEFAULT 0,
        last_error TEXT,
        last_verified TEXT,
        verified_by TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL,
        task_name TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        details TEXT,
        error_message TEXT,
        FOREIGN KEY (agent_id) REFERENCES agent_telemetry(agent_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL,
        check_name TEXT NOT NULL,
        status TEXT NOT NULL,
        evidence TEXT NOT NULL,
        verified_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("ThanvishOS canonical database initialized successfully.")
