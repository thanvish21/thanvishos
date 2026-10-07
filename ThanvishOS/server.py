"""ThanvishOS FastAPI Local Backend Daemon.

Serves the Next.js frontend with data from the canonical SQLite database and autonomous engines:
Today Command Center, Attendance What-If, SRM Portal Sync, SRM Mess System, Library OPAC,
3-Level Adaptive Testing, Semester Exam Radar, and Real 10-Agent Telemetry.
"""

import datetime
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure project paths are in sys.path
_current_dir = Path(__file__).resolve().parent
_parent_dir = _current_dir.parent
for p in [str(_parent_dir), str(_current_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Engine imports with fallback
try:
    from ThanvishOS.engine import (
        srm_schedule,
        srm_opac,
        dump_sorter,
        agents_runner,
        planner,
        attendance,
        srm_portal,
        srm_mess,
        daily_test,
        verification,
        db
    )
except ImportError:
    from engine import (
        srm_schedule,
        srm_opac,
        dump_sorter,
        agents_runner,
        planner,
        attendance,
        srm_portal,
        srm_mess,
        daily_test,
        verification,
        db
    )

app = FastAPI(title="ThanvishOS Hub API", version="4.0.0")

# Enable CORS for local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# Pydantic Request Models
# -----------------------------------------
class DumpTextRequest(BaseModel):
    content: str
    title: Optional[str] = None

class LibrarySearchRequest(BaseModel):
    query: str

class MasteryRoadmapRequest(BaseModel):
    topic: str
    hours_per_week: int = 10
    book_id: Optional[str] = None

class WhatIfRequest(BaseModel):
    course_code: str
    miss_count: int = 0
    attend_count: int = 0

class AttendanceUpdateRequest(BaseModel):
    course_code: str
    attended: int
    conducted: int
    source: str = "MANUAL_INPUT"

class TestEvaluateRequest(BaseModel):
    answers: Dict[str, str]
    topic_key: str = "calculus_maths"

class MessMenuUploadRequest(BaseModel):
    date: str
    breakfast: Optional[str] = None
    lunch: Optional[str] = None
    snacks: Optional[str] = None
    dinner: Optional[str] = None
    timings: Optional[Dict[str, str]] = None
    special_notes: Optional[str] = None

# -----------------------------------------
# Health & Status Endpoints
# -----------------------------------------

@app.get("/")
def read_root():
    return {
        "status": "ThanvishOS Daemon Online",
        "version": "4.0.0",
        "database": "canonical SQLite (/ThanvishOS/data/thanvishos.db)",
        "agents_online": 10
    }

# -----------------------------------------
# Today Command Center & Daily Planner
# -----------------------------------------

@app.get("/api/today")
@app.get("/api/planner/today")
def get_today_command_center(date: Optional[str] = None):
    """Returns the Master Spec v4.0 Today Command Center synthesis."""
    return planner.get_today_command_center(date)

@app.post("/api/planner/generate")
def generate_daily_plan(date: Optional[str] = None):
    """Generates the daily plan and persists it in the canonical database."""
    return planner.generate_daily_plan(date)

# -----------------------------------------
# SRM Schedule & Calendar
# -----------------------------------------

@app.get("/api/schedule/today")
def get_today_schedule(date: Optional[str] = None):
    """Returns the rotating SRM Day Order, active timetable, and exam radar."""
    return srm_schedule.get_day_order(date)

# -----------------------------------------
# Attendance Radar & What-If Engine
# -----------------------------------------

@app.get("/api/attendance/summary")
def get_attendance_summary(date: Optional[str] = None):
    """Returns attendance records, risk levels (Target >= 90%), and today's schedule warnings."""
    return attendance.get_attendance_summary()

@app.post("/api/attendance/what-if")
def simulate_what_if(payload: WhatIfRequest):
    """Simulates attendance percentage changes for missed/attended classes."""
    return attendance.simulate_what_if(
        course_code=payload.course_code,
        miss_count=payload.miss_count,
        attend_count=payload.attend_count
    )

@app.post("/api/attendance/update")
def record_attendance_update(payload: AttendanceUpdateRequest):
    """Records real attendance numbers into the database."""
    return attendance.record_attendance_update(
        course_code=payload.course_code,
        attended=payload.attended,
        conducted=payload.conducted,
        source=payload.source
    )

# -----------------------------------------
# SRM Portal Sync Adapter
# -----------------------------------------

@app.get("/api/portal/status")
def get_portal_status():
    """Returns the real connection status of the SRM Portal."""
    adapter = srm_portal.SRMPortalAdapter()
    return adapter.get_sync_status()

@app.post("/api/portal/sync")
def trigger_portal_sync():
    """Triggers a portal sync attempt."""
    adapter = srm_portal.SRMPortalAdapter()
    return adapter.trigger_sync()

# -----------------------------------------
# SRM Mess System
# -----------------------------------------

@app.get("/api/mess/today")
def get_today_mess(date: Optional[str] = None):
    """Returns today's mess menu or safe fallback state with exam overlap constraints."""
    adapter = srm_mess.SRMMessAdapter()
    return adapter.get_today_mess(date)

@app.post("/api/mess/upload")
def upload_mess_menu(payload: MessMenuUploadRequest):
    """Uploads/saves real mess menu data into the database."""
    adapter = srm_mess.SRMMessAdapter()
    return adapter.save_mess_menu(
        date=payload.date,
        breakfast=payload.breakfast,
        lunch=payload.lunch,
        snacks=payload.snacks,
        dinner=payload.dinner,
        timings=payload.timings,
        special_notes=payload.special_notes,
        source="MANUAL_UPLOAD"
    )

# -----------------------------------------
# Semester & CT1 Exams Radar
# -----------------------------------------

@app.get("/api/exams/all")
def get_all_exams():
    """Returns separated CT1 and Semester Exam schedules from canonical DB."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams ORDER BY exam_date ASC")
    rows = cursor.fetchall()
    conn.close()

    ct1_exams = []
    semester_exams = []
    for r in rows:
        item = dict(r)
        if item["exam_category"] == "CT1":
            ct1_exams.append(item)
        elif item["exam_category"] == "SEMESTER":
            semester_exams.append(item)

    return {
        "ct1_exams": ct1_exams,
        "semester_exams": semester_exams
    }

# -----------------------------------------
# Universal Brain Dump Dropzone
# -----------------------------------------

@app.post("/api/dump/text")
def dump_text(payload: DumpTextRequest):
    """Ingest raw text/notes/exam dates into the Universal Brain Dump dropzone."""
    result = dump_sorter.classify_and_route_text(payload.content, payload.title)
    return {"message": "Text dumped successfully.", "result": result}

@app.post("/api/dump/file")
async def dump_file(file: UploadFile = File(...)):
    """Ingest a PDF/file into the Universal Brain Dump dropzone."""
    try:
        contents = await file.read()
        result = dump_sorter.save_uploaded_file(file.filename, contents)
        return {"message": f"File {file.filename} dumped successfully.", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dump/recent")
def get_recent_dumps(limit: int = 10):
    """Get the recent history of autonomous dump classifications."""
    dumps = dump_sorter.get_recent_dumps(limit)
    return {"history": dumps}

# -----------------------------------------
# SRM Library OPAC & Mastery Engine
# -----------------------------------------

@app.post("/api/library/search")
def search_srm_library(payload: LibrarySearchRequest):
    """Query the SRM Central Library OPAC and OpenLibrary academic fallback."""
    result = srm_opac.search_srm_library(payload.query)
    return result

@app.post("/api/library/mastery")
def generate_mastery_roadmap(payload: MasteryRoadmapRequest):
    """Generate a step-by-step milestone learning roadmap for a given topic."""
    result = srm_opac.generate_mastery_roadmap(
        topic=payload.topic,
        hours_per_week=payload.hours_per_week,
        book_id=payload.book_id
    )
    return result

# -----------------------------------------
# 3-Level Multi-Format Daily Adaptive Test
# -----------------------------------------

@app.get("/api/test/today")
def get_today_test(topic_key: str = "calculus_maths"):
    """Generates today's 3-Level Adaptive Test."""
    return daily_test.get_daily_test(topic_key)

@app.post("/api/test/evaluate")
def evaluate_test_submission(payload: TestEvaluateRequest):
    """Evaluates test answers across all 5 dimensions and saves weaknesses."""
    return daily_test.evaluate_test_submission(payload.answers, payload.topic_key)

# -----------------------------------------
# Parallel Polyglot & Skills
# -----------------------------------------

@app.get("/api/polyglot/status")
def get_polyglot_status():
    """Returns parallel tracking metrics for C, Python, Java, DSA, and Codédex Pro sprint."""
    return {
        "codedex_pro_sprint": {
            "expires_in_days": 82,
            "days_completed": 108,
            "streak": 14,
            "progress_percent": 62
        },
        "languages": [
            {"name": "Python", "role": "PRIMARY DEEP • AI & CompBio", "progress": 75, "color": "bg-emerald-500"},
            {"name": "C / C++", "role": "SECONDARY • Systems & DSA", "progress": 45, "color": "bg-blue-500"},
            {"name": "Java", "role": "SECONDARY • Enterprise Backend", "progress": 30, "color": "bg-orange-500"},
            {"name": "DSA", "role": "CORE • Interview Foundations", "progress": 55, "color": "bg-purple-500"},
            {"name": "Rust", "role": "PARKING LOT • Modern Systems", "progress": 15, "color": "bg-rose-500"}
        ]
    }

# -----------------------------------------
# 10-Agent Real Telemetry & Verification Auditor
# -----------------------------------------

@app.get("/api/agents/telemetry")
@app.get("/api/agents/status")
def get_agents_telemetry():
    """Returns real telemetry for all 10 specialized agents from database logs."""
    return {"agents": agents_runner.get_agents_telemetry()}

@app.get("/api/verification/audit")
def run_verification_audit():
    """Runs Agent 10 Automated System Auditor on database, schedule, exams, and attendance."""
    return verification.run_system_verification()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
