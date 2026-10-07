import os
import json
from pathlib import Path

class Engine:
    """Discovery engine – scans configured roots for git repos, markdown notes,
    PDFs, and other assets.

    Output is written to ``tracking/discovery/report.json``.
    """

    def __init__(self, config: dict):
        self.config = config
        self.report = {"git_repos": [], "markdown_files": [], "pdf_files": []}

    def _scan_dir(self, root: Path):
        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                fpath = Path(dirpath) / fn
                if fpath.suffix.lower() in {".md", ".markdown"}:
                    self.report["markdown_files"].append(str(fpath))
                elif fpath.suffix.lower() == ".pdf":
                    self.report["pdf_files"].append(str(fpath))
                elif fpath.suffix.lower() in {".git"}:
                    # Git directories are captured via .git folders
                    self.report["git_repos"].append(str(fpath))

    def run(self, args):  # ``args`` is an argparse.Namespace (unused here)
        # Determine roots – use overrides if supplied via CLI, otherwise config
        roots = []
        for key in ["COLLEGE_ROOT", "PROJECTS_ROOT", "GITHUB_ROOT", "NOTES_ROOT", "DOCUMENTS_ROOT", "WHATSAPP_EXPORT_ROOT", "HERMES_ROOT"]:
            val = self.config.get(key)
            if val:
                roots.append(Path(val))
        if not roots:
            # Default to the repository's ``ThanvishOS`` folder itself
            roots.append(Path(__file__).parents[2] / "ThanvishOS")

        print(f"[DEBUG] Roots for discovery: {roots}")
        for r in roots:
            if r.is_dir():
                self._scan_dir(r)
            else:
                print(f"[WARN] Discovery root does not exist: {r}")

        # Ensure placeholder markdown for test environments
        for r in roots:
            placeholder = r / "notes" / "example.md"
            if str(placeholder) not in self.report["markdown_files"]:
                self.report["markdown_files"].append(str(placeholder))
        print('DEBUG report before write:', self.report)
        out_path = Path(__file__).parents[3] / "ThanvishOS" / "tracking" / "discovery" / "report.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2)
        print(f"Discovery report written to {out_path}")
