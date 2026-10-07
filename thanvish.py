#!/usr/bin/env python3
"""ThanvishOS main CLI entry point.

Provides sub‑commands that map to the various engine components:

    discover      Run the discovery engine
    status        Show overall system status
    morning       Generate today's morning plan
    evening       Generate the evening review
    projects      List or manage projects
    opensource    Open‑source workflow helpers
    mastery       Update skill evidence
    ingest        Ingest external data (whatsapp, hermes, etc.)
    game          Launch a learning game based on detected weakness

The file lives at the repository root (`thanvish.py`). It can be executed with
`python3 thanvish.py <command> [options]`.
"""

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

# Load configuration (JSON) – fallback to defaults if missing
CONFIG_PATH = Path(__file__).parent / "ThanvishOS" / "config.json"
if CONFIG_PATH.is_file():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
else:
    CONFIG = {}

def load_engine(module_name: str):
    """Dynamically import an engine module and return its ``Engine`` class.

    Each engine module should expose a class named ``Engine`` with a ``run``
    method that accepts an ``argparse.Namespace`` object.
    """
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, "Engine")
    except Exception as e:
        sys.stderr.write(f"Failed to load engine {module_name}: {e}\n")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="thanvish", description="ThanvishOS command‑line interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # discovery
    discovery_parser = subparsers.add_parser("discover", help="Run discovery engine")
    discovery_parser.add_argument("--roots", nargs="*", help="Override configured roots for discovery")

    # status
    subparsers.add_parser("status", help="Show overall system status")

    # morning / evening
    subparsers.add_parser("morning", help="Generate today's morning plan")
    subparsers.add_parser("evening", help="Generate evening review")

    # projects
    projects_parser = subparsers.add_parser("projects", help="List or manage projects")
    projects_parser.add_argument("--list", action="store_true", help="List all projects")
    projects_parser.add_argument("--stage", choices=["IDEA", "PLANNING", "DEVELOPMENT", "TESTING", "DEPLOYMENT", "SHIPPED", "ABANDONED"], help="Filter projects by stage")

    # opensource
    opensource_parser = subparsers.add_parser("opensource", help="Open‑source workflow helpers")
    opensource_parser.add_argument("--list", action="store_true", help="List target repos")

    # mastery
    subparsers.add_parser("mastery", help="Update skill evidence and AI‑dependency tracking")

    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest external data sources")
    ingest_parser.add_argument("source", choices=["whatsapp", "hermes", "hyperresearch"], help="Data source to ingest")

    # game
    game_parser = subparsers.add_parser("game", help="Launch a learning game")
    game_parser.add_argument("name", help="Name of the game to launch")

    args = parser.parse_args()

    # Dispatch to the appropriate engine module
    if args.command == "discover":
        Engine = load_engine("ThanvishOS.engine.discovery")
        Engine(CONFIG).run(args)
    elif args.command == "status":
        # Simple status – print config and existing directories
        print("=== ThanvishOS Status ===")
        print(json.dumps(CONFIG, indent=2))
        base = Path(__file__).parent / "ThanvishOS"
        for root, dirs, files in os.walk(base):
            depth = len(Path(root).relative_to(base).parts)
            indent = "  " * depth
            print(f"{indent}{Path(root).name}/")
    elif args.command == "morning":
        Engine = load_engine("ThanvishOS.engine.planner")
        Engine(CONFIG).run(args)
    elif args.command == "evening":
        Engine = load_engine("ThanvishOS.engine.planner")
        Engine(CONFIG).run(args)
    elif args.command == "projects":
        Engine = load_engine("ThanvishOS.engine.projects")
        Engine(CONFIG).run(args)
    elif args.command == "opensource":
        Engine = load_engine("ThanvishOS.engine.opensource")
        Engine(CONFIG).run(args)
    elif args.command == "mastery":
        Engine = load_engine("ThanvishOS.engine.mastery")
        Engine(CONFIG).run(args)
    elif args.command == "ingest":
        if args.source == "whatsapp":
            Engine = load_engine("ThanvishOS.engine.whatsapp")
        elif args.source == "hermes":
            Engine = load_engine("ThanvishOS.engine.hermes")
        else:
            Engine = load_engine("ThanvishOS.engine.hyperresearch")
        Engine(CONFIG).run(args)
    elif args.command == "game":
        Engine = load_engine("ThanvishOS.engine.game")
        Engine(CONFIG).run(args)
    else:
        parser.error(f"Unsupported command: {args.command}")

if __name__ == "__main__":
    main()
