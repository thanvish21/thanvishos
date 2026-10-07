import json
import os
from pathlib import Path
import datetime

class Engine:
    """Planner engine – generates daily plans based on discovered data.

    For now it combines:
    * Academic deadlines (if provided in ``college`` directory)
    * Project priorities (simple FIFO of active projects)
    * A static list of technical learning tasks

    The generated plan is written to ``tracking/daily/plan_<date>.json``.
    """

    def __init__(self, config: dict):
        self.config = config
        self.base_dir = Path(__file__).parents[2] / "ThanvishOS"

    def _load_academic(self):
        """Load exam schedule from ``college`` markdown files.
        Expected format: lines like ``Chemistry — Oct 7``.
        Returns a list of dicts with ``subject`` and ``date``.
        """
        exams = []
        college_root = self.config.get("COLLEGE_ROOT")
        if not college_root:
            return exams
        path = Path(college_root)
        if not path.is_dir():
            return exams
        for md in path.rglob("*.md"):
            try:
                with open(md, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or "—" not in line:
                            continue
                        subject, date_str = [p.strip() for p in line.split("—", 1)]
                        try:
                            date = datetime.datetime.strptime(date_str, "%b %d").date()
                            # Assume current year
                            date = date.replace(year=datetime.date.today().year)
                        except ValueError:
                            continue
                        exams.append({"subject": subject, "date": date.isoformat()})
            except Exception:
                continue
        return exams

    def _load_projects(self):
        """Gather active project directories under ``projects/active``.
        Returns a list of project folder names.
        """
        projects_root = self.config.get("PROJECTS_ROOT")
        if not projects_root:
            return []
        active_path = Path(projects_root) / "active"
        if not active_path.is_dir():
            return []
        return [p.name for p in active_path.iterdir() if p.is_dir()]

    def run(self, args):
        today = datetime.date.today().isoformat()
        plan = {
            "date": today,
            "academic": self._load_academic(),
            "projects": self._load_projects(),
            "technical_learning": [
                "Read a chapter from *Clean Code*",
                "Practice 2 algorithm problems",
                "Review recent PRs on GitHub"
            ]
        }
        out_dir = self.base_dir / "tracking" / "daily"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"plan_{today}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2)
        print(f"Daily plan written to {out_path}")
