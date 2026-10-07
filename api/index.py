import sys
from pathlib import Path

# Ensure root is in python path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from ThanvishOS.server import app

# Export ASGI app for Vercel
export_app = app
