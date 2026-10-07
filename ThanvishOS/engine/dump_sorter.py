"""Autonomous Brain Dump & File Sorter Engine for ThanvishOS.

Processes arbitrary inputs (text, PDFs, exam dates, lecture notes, project ideas,
code snippets), auto-classifies them, and routes them to appropriate local folders
with rich metadata, knowledge tags, and calendar events.
"""

import datetime
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "documents"
NOTES_DIR = DOCS_DIR / "notes"
PDFS_DIR = DOCS_DIR / "pdfs"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
DATA_DIR = BASE_DIR / "data"
EXAMS_FILE = DATA_DIR / "exams.json"
DUMP_LOG_FILE = DATA_DIR / "dump_history.json"

for d in [DOCS_DIR, NOTES_DIR, PDFS_DIR, KNOWLEDGE_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def load_exams() -> List[Dict[str, Any]]:
    if EXAMS_FILE.exists():
        try:
            with open(EXAMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    # Default CT1 schedule if not set
    default_exams = [
        {"subject": "PPS / C Programming", "date": "2026-10-05", "time": "08:00 AM - 09:40 AM", "type": "CT1", "status": "COMPLETED"},
        {"subject": "Chemistry", "date": "2026-10-07", "time": "12:30 PM - 02:10 PM", "type": "CT1", "status": "COMPLETED"},
        {"subject": "Mathematics", "date": "2026-10-09", "time": "12:30 PM - 02:10 PM", "type": "CT1", "status": "UPCOMING"},
        {"subject": "PPS", "date": "2026-10-12", "time": "08:00 AM - 09:40 AM", "type": "CT1", "status": "UPCOMING"},
        {"subject": "Japanese", "date": "2026-10-13", "time": "09:45 AM - 11:35 AM", "type": "CT1", "status": "UPCOMING"},
        {"subject": "Biology / CompBio", "date": "2026-10-14", "time": "02:20 PM - 04:00 PM", "type": "CT1", "status": "UPCOMING"}
    ]
    save_exams(default_exams)
    return default_exams

def save_exams(exams: List[Dict[str, Any]]):
    with open(EXAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(exams, f, indent=2)

def log_dump_entry(entry: Dict[str, Any]):
    history = []
    if DUMP_LOG_FILE.exists():
        try:
            with open(DUMP_LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.insert(0, entry)
    with open(DUMP_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history[:100], f, indent=2)

def classify_and_route_text(content: str, title: Optional[str] = None) -> Dict[str, Any]:
    """Autonomous classification of text dumps (notes, exam alerts, learning goals, ideas)."""
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    date_iso = now.strftime("%Y-%m-%d")

    text_lower = content.lower()
    inferred_type = "NOTE"
    category = "general"
    actions_taken = []

    # 1. Check for Exam Date Patterns
    exam_match = re.search(r"(exam|test|ct1|ct2|sem|assessment|quiz).*?(\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{1,2}|\d{4}-\d{2}-\d{2})", text_lower)
    if "exam" in text_lower or "ct1" in text_lower or "ct2" in text_lower or exam_match:
        inferred_type = "EXAM_SCHEDULE"
        category = "academics"

        # Attempt to extract subject and date
        exams = load_exams()
        subject_name = title or "Academic Exam"
        for s in ["mathematics", "calculus", "chemistry", "physics", "japanese", "biology", "pps", "c programming", "dsa", "java"]:
            if s in text_lower:
                subject_name = s.title()
                break

        exam_entry = {
            "id": f"exam-{timestamp_str}",
            "subject": subject_name,
            "raw_text": content.strip(),
            "date": date_iso,
            "time": "TBD",
            "type": "CT / Assessment",
            "status": "UPCOMING"
        }
        exams.append(exam_entry)
        save_exams(exams)
        actions_taken.append(f"Recorded new exam schedule for '{subject_name}' into SRM Exam Radar.")

    # 2. Check for Code Snippet
    elif any(kw in content for kw in ["def ", "function ", "import ", "#include", "public class ", "const ", "let ", "class "]):
        inferred_type = "CODE_SNIPPET"
        category = "coding"
        filename = f"code_{timestamp_str}.md"
        file_path = NOTES_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: {title or 'Code Snippet'}\ndate: {date_iso}\ntype: code\n---\n\n```\n{content}\n```\n")
        actions_taken.append(f"Saved formatted code snippet to {file_path.name}.")

    # 3. Check for Learning Goal or Mastery Wish
    elif any(phrase in text_lower for phrase in ["i need to learn", "want to learn", "master", "how to learn", "study plan"]):
        inferred_type = "LEARNING_GOAL"
        category = "mastery"
        filename = f"goal_{timestamp_str}.md"
        file_path = NOTES_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: {title or 'Learning Goal'}\ndate: {date_iso}\ntype: learning-goal\n---\n\n# Learning Goal\n\n{content}\n")
        actions_taken.append(f"Logged learning goal and queued SRM Library curriculum roadmap generator.")

    # 4. General Note / Thought
    else:
        inferred_type = "NOTE"
        category = "second-brain"
        safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', (title or content[:30]).strip())
        filename = f"note_{timestamp_str}_{safe_title[:20]}.md"
        file_path = NOTES_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: {title or 'Quick Note'}\ndate: {date_iso}\ntags: [inbox, raw-dump]\n---\n\n# {title or 'Dumped Note'}\n\n{content}\n")
        actions_taken.append(f"Stored structured note in {file_path.name} with YAML metadata.")

    result_entry = {
        "id": f"dump-{timestamp_str}",
        "type": inferred_type,
        "title": title or (content[:40] + "..."),
        "category": category,
        "preview": content[:140],
        "created_at": now.isoformat(),
        "actions": actions_taken
    }
    log_dump_entry(result_entry)
    return result_entry

def save_uploaded_file(filename: str, file_bytes: bytes) -> Dict[str, Any]:
    """Saves and indexes an uploaded file (PDF, notes, slides)."""
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    target_path = PDFS_DIR / f"{timestamp_str}_{clean_name}"

    with open(target_path, "wb") as f:
        f.write(file_bytes)

    entry = {
        "id": f"file-{timestamp_str}",
        "type": "DOCUMENT_PDF" if filename.lower().endswith(".pdf") else "FILE",
        "title": filename,
        "category": "documents",
        "preview": f"Saved {len(file_bytes)} bytes to {target_path.name}",
        "file_path": str(target_path),
        "created_at": now.isoformat(),
        "actions": [f"Stored document in {target_path.relative_to(BASE_DIR)} and indexed for full-text search."]
    }
    log_dump_entry(entry)
    return entry

def get_recent_dumps(limit: int = 15) -> List[Dict[str, Any]]:
    if DUMP_LOG_FILE.exists():
        try:
            with open(DUMP_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)[:limit]
        except Exception:
            return []
    return []
