import subprocess
import json
import sys
from pathlib import Path

def run_cli(args):
    cmd = ["python3", "thanvish.py"] + args
    result = subprocess.run(cmd, cwd=Path.cwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout)
    return result

if __name__ == "__main__":
    # Simple smoke test: run discovery and print exit code
    res = run_cli(["discover"])
    if res.returncode != 0:
        sys.exit(1)
    print("Smoke test passed.")
