"""Unit tests for ThanvishOS 10-Agent Runner and Verification Engine."""

import pytest
from ThanvishOS.engine.agents_runner import (
    get_agents_telemetry,
    log_agent_execution,
    execute_agent_task,
    AGENTS_MANIFEST
)
from ThanvishOS.engine.verification import run_system_verification
from ThanvishOS.engine.db import get_connection, init_db

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_10_specialized_agents_manifest():
    assert len(AGENTS_MANIFEST) == 10
    agent_ids = [a["agent_id"] for a in AGENTS_MANIFEST]
    expected_ids = [
        "agent-ingest",
        "agent-srm-academic",
        "agent-daily-planner",
        "agent-learning-coach",
        "agent-testing-engine",
        "agent-project-engineer",
        "agent-second-brain",
        "agent-career-coach",
        "agent-system-infra",
        "agent-verification-auditor"
    ]
    assert agent_ids == expected_ids

def test_no_hardcoded_static_counts():
    for agent in AGENTS_MANIFEST:
        assert "tasks_completed" not in agent
        assert "42" not in str(agent)
        assert "128" not in str(agent)

def test_log_agent_execution_and_telemetry():
    agent_id = "agent-daily-planner"
    log_agent_execution(agent_id, "plan_daily_schedule", "RUNNING", "Generating DO3 plan")
    telemetry = get_agents_telemetry()
    agent_data = next((a for a in telemetry if a["agent_id"] == agent_id), None)
    assert agent_data is not None
    assert agent_data["status"] == "RUNNING"
    assert agent_data["current_task"] == "plan_daily_schedule"

    log_agent_execution(agent_id, "plan_daily_schedule", "SUCCESS", "Completed DO3 plan")
    telemetry = get_agents_telemetry()
    agent_data = next((a for a in telemetry if a["agent_id"] == agent_id), None)
    assert agent_data is not None
    assert agent_data["status"] == "IDLE"
    assert agent_data["success_count"] >= 1
    assert agent_data["last_finished"] is not None

def test_system_verification_audit():
    report = run_system_verification()
    assert report["overall_status"] == "VERIFIED"
    assert report["checks_count"] == 6
    assert len(report["checks"]) == 6

    # Verify all 6 checks passed
    for check in report["checks"]:
        assert check["status"] == "PASS"

    # Verify database record was saved
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM system_verifications")
    verif_count = cursor.fetchone()[0]
    assert verif_count >= 6
    conn.close()
