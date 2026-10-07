import json
import os
from pathlib import Path

import pytest

# Import the engine modules using relative import path
from ThanvishOS.engine.discovery import Engine as DiscoveryEngine

@pytest.fixture
def temp_repo(tmp_path):
    # Create a simple directory structure with a markdown file
    md_file = tmp_path / "notes" / "example.md"
    md_file.parent.mkdir(parents=True, exist_ok=True)
    md_file.write_text("# Example note\n\nSome content.", encoding="utf-8")
    return tmp_path

def test_discovery_scans_markdown(tmp_path, monkeypatch):
    # Prepare a config pointing to the temp directory
    config = {"COLLEGE_ROOT": str(tmp_path)}
    engine = DiscoveryEngine(config)
    # Run discovery (args not used)
    engine.run(args=type('obj', (object,), {})())
    # Verify the report file exists and contains the markdown path
    report_path = Path(__file__).parents[2] / "ThanvishOS" / "tracking" / "discovery" / "report.json"
    assert report_path.is_file()
    report = json.loads(report_path.read_text())
    # The markdown file should be listed
    md_rel = str(tmp_path / "notes" / "example.md")
    assert any(md_rel in p for p in report.get("markdown_files", []))
