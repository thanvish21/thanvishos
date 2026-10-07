import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from ThanvishOS.engine import srm_schedule
    from ThanvishOS.engine import db
    from ThanvishOS.engine import daily_test
except ImportError:
    import srm_schedule
    import db
    import daily_test

def get_today_command_center(date_str: Optional[str] = None) -> Dict[str, Any]:
    """Generates the Master Spec v4.0 Today Command Center data."""
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
    # 1. Date, Weekday, Holiday/Working status, Day Order, Classes
    schedule_data = srm_schedule.get_day_order(date_str)
    
    # 2. Query exams that matter (CT1 proximity & Semester countdown)
    conn = db.get_connection()
    exams_rows = conn.execute(
        "SELECT * FROM exams WHERE (exam_date >= ? OR exam_date IS NULL) ORDER BY exam_date ASC",
        (date_str,)
    ).fetchall()
    
    ct1_exams = []
    semester_exams = []
    urgent_exam = None
    
    for row in exams_rows:
        exam = dict(row)
        if exam["exam_category"] == "CT1":
            ct1_exams.append(exam)
            if not urgent_exam and exam["exam_date"]:
                urgent_exam = exam
        elif exam["exam_category"] == "SEMESTER":
            semester_exams.append(exam)
            
    # Calculate proximity for urgent exam
    days_to_exam = None
    if urgent_exam and urgent_exam["exam_date"]:
        target_date = datetime.datetime.strptime(urgent_exam["exam_date"], "%Y-%m-%d")
        current_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        days_to_exam = (target_date - current_date).days

    # 3. Attendance risks
    attendance_rows = conn.execute("SELECT * FROM attendance_records").fetchall()
    attendance_risks = []
    all_not_connected = True
    for row in attendance_rows:
        att = dict(row)
        if att["source"] != "NOT_CONNECTED":
            all_not_connected = False
        if att["risk_status"] != "SAFE" and att["source"] != "NOT_CONNECTED":
            attendance_risks.append(att)
            
    attendance_summary = "Attendance awaiting sync" if all_not_connected else (
        f"{len(attendance_risks)} courses at risk" if attendance_risks else "All synced courses are SAFE"
    )
    
    # 4. Learning, Building, Testing
    technical_learning = "Primary: Python (AI & CompBio) - Deep Dive | Secondary: C/C++ (Systems & DSA) - Maintenance"
    building_goal = "ThanvishOS v4.0 - Today Command Center & Database Integration"
    
    test_topic = "calculus_maths" if days_to_exam is not None and days_to_exam <= 2 else "python_dsa"
    testing_data = daily_test.get_daily_test(test_topic)
    testing_goal = f"3-Level Adaptive Test: {testing_data['topic']}"

    # 5. Section 88: What NOT to do today (Protect focus)
    what_not_to_do = ""
    why_these_priorities = ""
    
    if days_to_exam == 1:
        what_not_to_do = f"Do not jump into Rust exploration or unrelated side projects tonight with {urgent_exam['subject_name']} {urgent_exam['exam_category']} tomorrow."
        why_these_priorities = f"Tomorrow is a critical {urgent_exam['exam_category']} exam for {urgent_exam['subject_name']}. Focus must be strictly on revision, test practice, and getting adequate rest."
    elif days_to_exam == 0:
        what_not_to_do = f"Do not start heavy coding sessions before your {urgent_exam['subject_name']} exam today."
        why_these_priorities = f"Today is exam day for {urgent_exam['subject_name']}. Preserve cognitive energy and focus purely on calm review."
    elif schedule_data["power_day"]:
        what_not_to_do = "Do not waste the DO3 afternoon power slot on passive scrolling or minor tasks."
        why_these_priorities = "DO3 ends early at 12:25 PM, providing a rare contiguous block of time for deep engineering and portfolio work."
    else:
        what_not_to_do = "Avoid context switching between more than 2 technical domains today."
        why_these_priorities = "Standard academic day. Focus on completing assigned classwork and making incremental progress on the primary building goal."
        
    # 6. When can I relax? (Section 72 & 126)
    free_windows = schedule_data["free_windows"]
    if schedule_data["power_day"]:
        free_time_summary = "Afternoon Power Window (12:30 PM onwards) + Evening wind-down (9:30 PM - 10:30 PM)"
    else:
        free_time_summary = f"In-college free periods: {', '.join(free_windows) if free_windows else 'None'} | Evening wind-down (9:30 PM - 10:30 PM)"

    conn.close()

    return {
        "date_info": {
            "date": date_str,
            "weekday": schedule_data["weekday"],
            "day_order": schedule_data["day_order"],
            "is_working": schedule_data["day_order"] != "HOLIDAY",
            "power_day": schedule_data["power_day"]
        },
        "schedule": {
            "periods": schedule_data["periods"],
            "nss_block": schedule_data["nss_block"]
        },
        "exams": {
            "ct1_upcoming": ct1_exams,
            "semester_upcoming": semester_exams,
            "urgent_exam": urgent_exam,
            "days_to_urgent_exam": days_to_exam
        },
        "attendance": {
            "summary": attendance_summary,
            "risks": attendance_risks
        },
        "learning_goal": technical_learning,
        "building_goal": building_goal,
        "testing_goal": testing_goal,
        "what_not_to_do": what_not_to_do,
        "why_these_priorities": why_these_priorities,
        "free_time_windows": free_time_summary
    }

def generate_daily_plan(date_str: Optional[str] = None) -> Dict[str, Any]:
    """Generates the daily plan, saves to database and legacy JSON file."""
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
    cmd_center = get_today_command_center(date_str)
    
    plan_summary = f"Plan for {cmd_center['date_info']['weekday']}, {cmd_center['date_info']['day_order']}. "
    if cmd_center['exams']['days_to_urgent_exam'] == 1:
        plan_summary += f"Exam Tomorrow: {cmd_center['exams']['urgent_exam']['subject_name']}. "
    elif cmd_center['date_info']['power_day']:
        plan_summary += "Power Day (DO3) - Afternoon is free for deep work. "
        
    academic_priority = "Regular classes"
    if cmd_center['exams']['urgent_exam']:
        academic_priority = f"Prepare for {cmd_center['exams']['urgent_exam']['subject_name']} exam"
        
    now_iso = datetime.datetime.now().isoformat()
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO daily_plans (
            date, day_order, plan_summary, academic_priority, 
            technical_learning, building_goal, testing_goal, 
            what_not_to_do, why_these_priorities, free_time_windows, 
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            day_order=excluded.day_order,
            plan_summary=excluded.plan_summary,
            academic_priority=excluded.academic_priority,
            technical_learning=excluded.technical_learning,
            building_goal=excluded.building_goal,
            testing_goal=excluded.testing_goal,
            what_not_to_do=excluded.what_not_to_do,
            why_these_priorities=excluded.why_these_priorities,
            free_time_windows=excluded.free_time_windows,
            updated_at=excluded.updated_at
    """, (
        date_str,
        cmd_center['date_info']['day_order'],
        plan_summary,
        academic_priority,
        cmd_center['learning_goal'],
        cmd_center['building_goal'],
        cmd_center['testing_goal'],
        cmd_center['what_not_to_do'],
        cmd_center['why_these_priorities'],
        cmd_center['free_time_windows'],
        now_iso,
        now_iso
    ))
    conn.commit()
    conn.close()
    
    # Save legacy JSON file
    base_dir = Path(__file__).resolve().parents[2] / "ThanvishOS"
    out_dir = base_dir / "tracking" / "daily"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"plan_{date_str}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cmd_center, f, indent=2)
        
    return cmd_center

class Engine:
    """Wrapper class for backwards compatibility with dynamic agents."""
    def __init__(self, config: dict):
        self.config = config

    def run(self, args):
        plan = generate_daily_plan()
        print(f"Generated daily plan for {plan['date_info']['date']}. View at tracking/daily/plan_{plan['date_info']['date']}.json")

if __name__ == "__main__":
    plan = generate_daily_plan("2026-10-08")
    print(json.dumps(plan, indent=2))
