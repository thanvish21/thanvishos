import os
import json
from pathlib import Path

class Engine:
    """Project engine – lists projects and can filter by stage.

    Expected directory layout under the configured ``PROJECTS_ROOT``:
    projects/backlog, projects/active, projects/shipped, projects/abandoned
    """

    def __init__(self, config: dict):
        self.config = config
        self.base_dir = Path(__file__).parents[2] / "ThanvishOS"

    def _collect_projects(self):
        root = self.config.get("PROJECTS_ROOT")
        if not root:
            return {}
        proj_path = Path(root)
        stages = ["backlog", "active", "shipped", "abandoned"]
        result = {stage: [] for stage in stages}
        for stage in stages:
            stage_path = proj_path / stage
            if stage_path.is_dir():
                result[stage] = [p.name for p in stage_path.iterdir() if p.is_dir()]
        return result

    def run(self, args):
        projects = self._collect_projects()
        if args.list:
            # Simple text output
            print("=== Projects by stage ===")
            for stage, names in projects.items():
                print(f"{stage.title()}: {', '.join(names) if names else 'none'}")
        elif args.stage:
            names = projects.get(args.stage.lower(), [])
            print(f"Projects in {args.stage}: {', '.join(names) if names else 'none'}")
        else:
            # Default: print full JSON
            out_path = self.base_dir / "tracking" / "projects.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(projects, f, indent=2)
            print(f"Project overview written to {out_path}")
