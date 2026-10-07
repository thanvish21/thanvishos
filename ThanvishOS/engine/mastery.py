import json
from pathlib import Path

class Engine:
    """Mastery engine – maintains SKILLS.md with evidence and weakness tracking.

    For this prototype it can add a new skill entry or list existing entries.
    """

    def __init__(self, config: dict):
        self.config = config
        self.skills_path = Path(__file__).parents[2] / "SKILLS.md"
        if not self.skills_path.is_file():
            # Create a minimal file if missing
            self.skills_path.write_text("# Skills\n\n", encoding="utf-8")

    def _load_skills(self):
        try:
            content = self.skills_path.read_text(encoding="utf-8")
        except Exception:
            return []
        skills = []
        current = {}
        for line in content.splitlines():
            if line.startswith("## "):
                if current:
                    skills.append(current)
                current = {"title": line[3:].strip()}
            elif ":" in line and current is not
                "title" in current:
                key, val = line.split(":", 1)
                current[key.strip().lower()] = val.strip()
        if current:
            skills.append(current)
        return skills

    def run(self, args):
        # Simple CLI – list skills
        skills = self._load_skills()
        print("=== Skills Overview ===")
        for s in skills:
            print(f"- {s.get('title', 'Unnamed')} (Level: {s.get('level', 'UNKNOWN')})")
