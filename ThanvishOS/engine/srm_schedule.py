"""SRM Rotating Day Order (DO1-DO5) & Academic Schedule Engine.

Maps calendar dates to exact SRM Day Orders (never assuming weekdays),
computes period timetables, active energy levels, NSS 2-period block rules,
and tracks CT1/CT2 exams.
"""

import datetime
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "college"
DATA_DIR.mkdir(parents=True, exist_ok=True)
NSS_STATE_FILE = DATA_DIR / "nss_state.json"

# Official Authoritative SRM Rotating Day Order Calendar (Sep - Dec 2026)
SRM_DO_CALENDAR = {
    # September 2026
    "2026-09-01": "DO4", "2026-09-02": "DO5", "2026-09-03": "DO1", "2026-09-04": "HOLIDAY",
    "2026-09-05": "HOLIDAY", "2026-09-06": "HOLIDAY", "2026-09-07": "DO2", "2026-09-08": "DO3",
    "2026-09-09": "DO4", "2026-09-10": "DO5", "2026-09-11": "DO1", "2026-09-12": "HOLIDAY",
    "2026-09-13": "HOLIDAY", "2026-09-14": "HOLIDAY", "2026-09-15": "DO2", "2026-09-16": "DO3",
    "2026-09-17": "DO4", "2026-09-18": "DO5", "2026-09-19": "HOLIDAY", "2026-09-20": "HOLIDAY",
    "2026-09-21": "DO1", "2026-09-22": "DO2", "2026-09-23": "DO3", "2026-09-24": "DO4",
    "2026-09-25": "DO5", "2026-09-26": "HOLIDAY", "2026-09-27": "HOLIDAY", "2026-09-28": "DO1",
    "2026-09-29": "DO2", "2026-09-30": "DO3",

    # October 2026
    "2026-10-01": "DO4", "2026-10-02": "HOLIDAY", "2026-10-03": "HOLIDAY", "2026-10-04": "HOLIDAY",
    "2026-10-05": "DO5", "2026-10-06": "DO1", "2026-10-07": "DO2", "2026-10-08": "DO3",
    "2026-10-09": "DO4", "2026-10-10": "HOLIDAY", "2026-10-11": "HOLIDAY", "2026-10-12": "DO5",
    "2026-10-13": "DO1", "2026-10-14": "DO2", "2026-10-15": "DO3", "2026-10-16": "DO4",
    "2026-10-17": "HOLIDAY", "2026-10-18": "HOLIDAY", "2026-10-19": "HOLIDAY", "2026-10-20": "HOLIDAY",
    "2026-10-21": "DO5", "2026-10-22": "DO1", "2026-10-23": "DO2", "2026-10-24": "HOLIDAY",
    "2026-10-25": "HOLIDAY", "2026-10-26": "DO3", "2026-10-27": "DO4", "2026-10-28": "DO5",
    "2026-10-29": "DO1", "2026-10-30": "DO2", "2026-10-31": "HOLIDAY",

    # November 2026
    "2026-11-01": "HOLIDAY",
    "2026-11-02": "DO3", "2026-11-03": "DO4", "2026-11-04": "DO5", "2026-11-05": "DO1", "2026-11-06": "DO2", "2026-11-07": "HOLIDAY", "2026-11-08": "HOLIDAY",
    "2026-11-09": "DO3", "2026-11-10": "DO4", "2026-11-11": "DO5", "2026-11-12": "DO1", "2026-11-13": "DO2", "2026-11-14": "HOLIDAY", "2026-11-15": "HOLIDAY",
    "2026-11-16": "DO3", "2026-11-17": "DO4", "2026-11-18": "DO5", "2026-11-19": "DO1", "2026-11-20": "DO2", "2026-11-21": "HOLIDAY", "2026-11-22": "HOLIDAY",
    "2026-11-23": "DO3", "2026-11-24": "DO4", "2026-11-25": "DO5", "2026-11-26": "DO1", "2026-11-27": "DO2", "2026-11-28": "HOLIDAY", "2026-11-29": "HOLIDAY",
    "2026-11-30": "DO3",

    # December 2026
    "2026-12-01": "DO4", "2026-12-02": "DO5", "2026-12-03": "DO1", "2026-12-04": "DO2", "2026-12-05": "HOLIDAY", "2026-12-06": "HOLIDAY", "2026-12-07": "DO3",
    "2026-12-08": "HOLIDAY", "2026-12-09": "HOLIDAY", "2026-12-10": "HOLIDAY", "2026-12-11": "HOLIDAY", "2026-12-12": "HOLIDAY", "2026-12-13": "HOLIDAY",
    "2026-12-14": "HOLIDAY", "2026-12-15": "HOLIDAY", "2026-12-16": "HOLIDAY", "2026-12-17": "HOLIDAY", "2026-12-18": "HOLIDAY", "2026-12-19": "HOLIDAY",
    "2026-12-20": "HOLIDAY", "2026-12-21": "HOLIDAY", "2026-12-22": "HOLIDAY", "2026-12-23": "HOLIDAY", "2026-12-24": "HOLIDAY", "2026-12-25": "HOLIDAY",
    "2026-12-26": "HOLIDAY", "2026-12-27": "HOLIDAY", "2026-12-28": "HOLIDAY", "2026-12-29": "HOLIDAY", "2026-12-30": "HOLIDAY", "2026-12-31": "HOLIDAY"
}

PERIOD_TIMES = [
    {"period": "P1", "time": "08:00–08:50"},
    {"period": "P2", "time": "08:50–09:40"},
    {"period": "P3", "time": "09:45–10:35"},
    {"period": "P4", "time": "10:40–11:30"},
    {"period": "P5", "time": "11:35–12:25"},
    {"period": "P6", "time": "12:30–01:20"},
    {"period": "P7", "time": "01:25–02:15"},
    {"period": "P8", "time": "02:20–03:10"},
    {"period": "P9", "time": "03:10–04:00"},
    {"period": "P10", "time": "04:00–04:50"},
    {"period": "P11", "time": "04:50–05:30"},
    {"period": "P12", "time": "05:30–06:10"}
]

CT1_EXAMS = [
    {"subject": "Programming for Problem Solving / C", "date": "2026-10-05", "time": "08:00 AM - 09:40 AM", "completed": True},
    {"subject": "Chemistry for Computer Science", "date": "2026-10-07", "time": "12:30 PM - 02:10 PM", "completed": True},
    {"subject": "Calculus and Linear Algebra (Mathematics)", "date": "2026-10-09", "time": "12:30 PM - 02:10 PM", "completed": False},
    {"subject": "Programming for Problem Solving", "date": "2026-10-12", "time": "08:00 AM - 09:40 AM", "completed": False},
    {"subject": "Foreign Language (Japanese)", "date": "2026-10-13", "time": "09:45 AM - 11:35 AM", "completed": False},
    {"subject": "Introduction to Computational Biology", "date": "2026-10-14", "time": "02:20 PM - 04:00 PM", "completed": False}
]

def get_nss_block_preference() -> str:
    """Gets currently selected 2-period NSS block for DO2 ('A' = P1+P2, 'B' = P3+P4)."""
    if NSS_STATE_FILE.exists():
        try:
            with open(NSS_STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("active_block", "A")
        except Exception:
            return "A"
    return "A"

def set_nss_block_preference(block: str):
    """Sets active NSS block ('A' or 'B')."""
    with open(NSS_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"active_block": block, "updated_at": datetime.datetime.now().isoformat()}, f, indent=2)

def build_do_periods(day_order: str, nss_block: str = "A") -> List[Dict[str, str]]:
    """Generates the exact period-by-period timetable for Thanvish based on Day Order & NSS block."""
    if day_order == "HOLIDAY":
        return [{"period": "All Day", "time": "Full Day", "subject": "No College Classes — Free for Projects, Study & Rest", "type": "FREE"}]

    if day_order == "DO1":
        return [
            {"period": "P1", "time": "08:00–08:50", "subject": "FREE / Self-Study", "type": "FREE"},
            {"period": "P2", "time": "08:50–09:40", "subject": "FREE / Self-Study", "type": "FREE"},
            {"period": "P3", "time": "09:45–10:35", "subject": "Japanese (26LCA1005J)", "type": "CLASS"},
            {"period": "P4", "time": "10:40–11:30", "subject": "Japanese (26LCA1005J)", "type": "CLASS"},
            {"period": "P5", "time": "11:35–12:25", "subject": "CompBio (26BTB1001T)", "type": "CLASS"},
            {"period": "P6", "time": "12:30–01:20", "subject": "LUNCH BREAK", "type": "BREAK"},
            {"period": "P7", "time": "01:25–02:15", "subject": "Workshop Practice (26MEE1001L)", "type": "LAB"},
            {"period": "P8", "time": "02:20–03:10", "subject": "Workshop Practice (26MEE1001L)", "type": "LAB"},
            {"period": "P9", "time": "03:10–04:00", "subject": "Workshop Practice (26MEE1001L)", "type": "LAB"},
            {"period": "P10", "time": "04:00–04:50", "subject": "Workshop Practice (26MEE1001L)", "type": "LAB"},
            {"period": "P11", "time": "04:50–05:30", "subject": "FREE / Done", "type": "FREE"},
            {"period": "P12", "time": "05:30–06:10", "subject": "FREE / Done", "type": "FREE"}
        ]

    elif day_order == "DO2":
        # Section 17: NSS 2-Period Block Rule
        if nss_block == "A":
            nss_p1, nss_p2 = "NSS Active Block (26GNN1004L)", "NSS Active Block (26GNN1004L)"
            nss_p3, nss_p4 = "FREE (Batch B in NSS)", "FREE (Batch B in NSS)"
            nss_t1, nss_t2 = "NSS", "NSS"
            nss_t3, nss_t4 = "FREE", "FREE"
        else:
            nss_p1, nss_p2 = "FREE (Batch A in NSS)", "FREE (Batch A in NSS)"
            nss_p3, nss_p4 = "NSS Active Block (26GNN1004L)", "NSS Active Block (26GNN1004L)"
            nss_t1, nss_t2 = "FREE", "FREE"
            nss_t3, nss_t4 = "NSS", "NSS"

        return [
            {"period": "P1", "time": "08:00–08:50", "subject": nss_p1, "type": nss_t1},
            {"period": "P2", "time": "08:50–09:40", "subject": nss_p2, "type": nss_t2},
            {"period": "P3", "time": "09:45–10:35", "subject": nss_p3, "type": nss_t3},
            {"period": "P4", "time": "10:40–11:30", "subject": nss_p4, "type": nss_t4},
            {"period": "P5", "time": "11:35–12:25", "subject": "FREE / Buffer", "type": "FREE"},
            {"period": "P6", "time": "12:30–01:20", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P7", "time": "01:25–02:15", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P8", "time": "02:20–03:10", "subject": "CompBio (26BTB1001T)", "type": "CLASS"},
            {"period": "P9", "time": "03:10–04:00", "subject": "CompBio (26BTB1001T)", "type": "CLASS"},
            {"period": "P10", "time": "04:00–04:50", "subject": "FREE / Done", "type": "FREE"},
            {"period": "P11", "time": "04:50–05:30", "subject": "Japanese / Free", "type": "FREE"},
            {"period": "P12", "time": "05:30–06:10", "subject": "Online / Free", "type": "FREE"}
        ]

    elif day_order == "DO3":
        # Section 14: DO3 Power Day! Done by 12:25 PM
        return [
            {"period": "P1", "time": "08:00–08:50", "subject": "FREE / Morning Coding", "type": "FREE"},
            {"period": "P2", "time": "08:50–09:40", "subject": "FREE / Morning Coding", "type": "FREE"},
            {"period": "P3", "time": "09:45–10:35", "subject": "FREE / Buffer", "type": "FREE"},
            {"period": "P4", "time": "10:40–11:30", "subject": "Calculus & Linear Algebra (26MAB1001T)", "type": "CLASS"},
            {"period": "P5", "time": "11:35–12:25", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P6", "time": "12:30–01:20", "subject": "🎉 Done for the day! Prime Power Slot", "type": "FREE"},
            {"period": "P7", "time": "01:25–02:15", "subject": "FREE — Deep Engineering & Projects", "type": "FREE"},
            {"period": "P8", "time": "02:20–03:10", "subject": "FREE — Deep Engineering & Projects", "type": "FREE"},
            {"period": "P9", "time": "03:10–04:00", "subject": "FREE — Deep Engineering & Projects", "type": "FREE"},
            {"period": "P10", "time": "04:00–04:50", "subject": "FREE", "type": "FREE"},
            {"period": "P11", "time": "04:50–05:30", "subject": "FREE", "type": "FREE"},
            {"period": "P12", "time": "05:30–06:10", "subject": "FREE", "type": "FREE"}
        ]

    elif day_order == "DO4":
        return [
            {"period": "P1", "time": "08:00–08:50", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P2", "time": "08:50–09:40", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P3", "time": "09:45–10:35", "subject": "FREE / Self-Study", "type": "FREE"},
            {"period": "P4", "time": "10:40–11:30", "subject": "FREE / Self-Study", "type": "FREE"},
            {"period": "P5", "time": "11:35–12:25", "subject": "FREE / Self-Study", "type": "FREE"},
            {"period": "P6", "time": "12:30–01:20", "subject": "Calculus & Linear Algebra (26MAB1001T)", "type": "CLASS"},
            {"period": "P7", "time": "01:25–02:15", "subject": "Calculus & Linear Algebra (26MAB1001T)", "type": "CLASS"},
            {"period": "P8", "time": "02:20–03:10", "subject": "Chemistry (26CYB1002J)", "type": "CLASS"},
            {"period": "P9", "time": "03:10–04:00", "subject": "Programming for Problem Solving (26CSE1002J)", "type": "CLASS"},
            {"period": "P10", "time": "04:00–04:50", "subject": "Calculus & Linear Algebra (26MAB1001T)", "type": "CLASS"},
            {"period": "P11", "time": "04:50–05:30", "subject": "Japanese / Free", "type": "FREE"},
            {"period": "P12", "time": "05:30–06:10", "subject": "FREE / Done", "type": "FREE"}
        ]

    elif day_order == "DO5":
        return [
            {"period": "P1", "time": "08:00–08:50", "subject": "Programming for Problem Solving (26CSE1002J)", "type": "CLASS"},
            {"period": "P2", "time": "08:50–09:40", "subject": "Programming for Problem Solving (26CSE1002J)", "type": "CLASS"},
            {"period": "P3", "time": "09:45–10:35", "subject": "FREE / Buffer", "type": "FREE"},
            {"period": "P4", "time": "10:40–11:30", "subject": "Japanese (26LCA1005J)", "type": "CLASS"},
            {"period": "P5", "time": "11:35–12:25", "subject": "Calculus & Linear Algebra (26MAB1001T)", "type": "CLASS"},
            {"period": "P6", "time": "12:30–01:20", "subject": "LUNCH BREAK", "type": "BREAK"},
            {"period": "P7", "time": "01:25–02:15", "subject": "Programming for Problem Solving (26CSE1002J)", "type": "CLASS"},
            {"period": "P8", "time": "02:20–03:10", "subject": "Programming for Problem Solving (26CSE1002J)", "type": "CLASS"},
            {"period": "P9", "time": "03:10–04:00", "subject": "FREE / Done for the day", "type": "FREE"},
            {"period": "P10", "time": "04:00–04:50", "subject": "FREE", "type": "FREE"},
            {"period": "P11", "time": "04:50–05:30", "subject": "FREE", "type": "FREE"},
            {"period": "P12", "time": "05:30–06:10", "subject": "FREE", "type": "FREE"}
        ]

    return []

def get_day_order(date_str: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves Day Order, schedule, energy level, and exam alert for a specific date (default today)."""
    if not date_str:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")

    # Authoritative DO lookup
    do = SRM_DO_CALENDAR.get(date_str, "DO3")

    # Determine weekday name
    try:
        curr_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        weekday_name = curr_dt.strftime("%A")
        tomorrow_dt = curr_dt + datetime.timedelta(days=1)
        tomorrow_str = tomorrow_dt.strftime("%Y-%m-%d")
        tomorrow_do = SRM_DO_CALENDAR.get(tomorrow_str, "DO4")
    except Exception:
        weekday_name = "Thursday"
        tomorrow_str = "2026-10-09"
        tomorrow_do = "DO4"

    nss_block = get_nss_block_preference()
    periods = build_do_periods(do, nss_block)

    # Check for upcoming exam within 2 days (Section 20 Exam Priority Engine)
    exam_alert = None
    for ex in CT1_EXAMS:
        if ex["date"] == date_str and not ex["completed"]:
            exam_alert = {
                "urgency": "TODAY",
                "subject": ex["subject"],
                "time": ex["time"],
                "message": f"⚠️ EXAM TODAY: {ex['subject']} at {ex['time']}! Prioritize revision."
            }
            break
        elif ex["date"] == tomorrow_str and not ex["completed"]:
            exam_alert = {
                "urgency": "TOMORROW",
                "subject": ex["subject"],
                "time": ex["time"],
                "message": f"⚠️ EXAM ALERT: {ex['subject']} is TOMORROW at {ex['time']}. Keep interview prep light and prioritize revision tonight."
            }
            break

    # Calculate free windows
    free_periods = [p["period"] + " (" + p["time"] + ")" for p in periods if p["type"] == "FREE"]

    return {
        "date": date_str,
        "weekday": weekday_name,
        "day_order": do,
        "nss_block": nss_block,
        "power_day": (do == "DO3"),
        "periods": periods,
        "free_windows": free_periods,
        "tomorrow": {
            "date": tomorrow_str,
            "day_order": tomorrow_do
        },
        "exam_alert": exam_alert,
        "all_exams": CT1_EXAMS
    }
