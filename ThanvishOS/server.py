"""ThanvishOS FastAPI Local Backend Daemon.

Serves the Next.js frontend with data from the 6 autonomous engines:
SRM Academic Schedule, Library OPAC, Polyglot tracking, and Autonomous Dump ingestion.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
from typing import Optional, List

# Engine imports
try:
    from ThanvishOS.engine import srm_schedule
    from ThanvishOS.engine import srm_opac
    from ThanvishOS.engine import dump_sorter
    from ThanvishOS.engine import agents_runner
except ImportError:
    from engine import srm_schedule
    from engine import srm_opac
    from engine import dump_sorter
    from engine import agents_runner

app = FastAPI(title="ThanvishOS Hub API", version="1.0.0")

# Enable CORS for the local Next.js frontend (port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# Pydantic Models
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

# -----------------------------------------
# API Endpoints
# -----------------------------------------

@app.get("/")
def read_root():
    return {"status": "ThanvishOS Daemon Online", "version": "1.0"}

@app.get("/api/schedule/today")
def get_today_schedule(date: Optional[str] = None):
    """Returns the rotating SRM Day Order, active timetable, and exam radar."""
    return srm_schedule.get_day_order(date)

@app.get("/api/agents/status")
def get_agents_status():
    """Returns the live status of the 6 autonomous background agents."""
    return {"agents": agents_runner.get_agents_status()}

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

@app.get("/api/polyglot/status")
def get_polyglot_status():
    """Returns the parallel tracking metrics for C, Python, Java, DSA, and Codédex Pro sprint."""
    # Hardcoded stub for the web UI display.
    return {
        "codedex_pro_sprint": {
            "expires_in_days": 82,
            "days_completed": 108,
            "streak": 14,
            "progress_percent": 62
        },
        "languages": [
            {"name": "Python", "role": "AI & CompBio", "progress": 75, "color": "bg-emerald-500"},
            {"name": "C / C++", "role": "Systems & DSA", "progress": 45, "color": "bg-blue-500"},
            {"name": "Java", "role": "Enterprise Backend", "progress": 30, "color": "bg-orange-500"},
            {"name": "DSA", "role": "Interview Core", "progress": 55, "color": "bg-purple-500"},
            {"name": "Rust", "role": "Modern Systems", "progress": 15, "color": "bg-rose-500"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    # When run directly, start the server on port 8000
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
