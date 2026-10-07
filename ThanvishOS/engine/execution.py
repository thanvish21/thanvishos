import subprocess
import shlex
import sys
from pathlib import Path

class Engine:
    """Execution engine – safe wrappers around git operations.

    Currently provides:
    * ``status`` – runs ``git status`` in a given repo.
    * ``commit`` – creates a commit with a message after verifying no force‑push.
    The engine never runs destructive commands (no ``--force``) and aborts
    with a clear error if such a flag is detected.
    """

    def __init__(self, config: dict):
        self.config = config
        self.repo_root = None
        # Determine repo root from config or fallback to current directory
        for key in ["PROJECTS_ROOT", "GITHUB_ROOT", "COLLEGE_ROOT"]:
            val = self.config.get(key)
            if val and Path(val).is_dir():
                self.repo_root = Path(val)
                break
        if not self.repo_root:
            self.repo_root = Path.cwd()

    def _run_git(self, args: list):
        cmd = ["git"] + args
        # Guard against destructive flags
        if any(flag in args for flag in ["--force", "-f"]):
            print("[Error] Destructive git flags are not allowed.")
            sys.exit(1)
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            print(result.stdout)
        except FileNotFoundError:
            print("git executable not found – ensure Git is installed.")

    def run(self, args):
        # ``args`` is an argparse.Namespace with a ``command`` attribute
        command = getattr(args, "command", None)
        if command == "status":
            self._run_git(["status"])
        elif command == "commit":
            msg = getattr(args, "message", "Auto commit")
            self._run_git(["add", ".", "&&", "git", "commit", "-m", msg])
        else:
            print("[Execution Engine] No recognized sub‑command provided.")
