import pytest
import datetime
from ThanvishOS.engine.srm_mess import SRMMessAdapter, parse_time_to_minutes, check_lunch_overlap
from ThanvishOS.engine.db import get_connection

def setup_module(module):
    """Setup tests."""
    pass

def teardown_module(module):
    """Teardown tests."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mess_menu WHERE date LIKE 'TEST-%'")
    # reset sync state
    cursor.execute("UPDATE mess_sync_state SET status = 'NOT_CONNECTED' WHERE id = 'current'")
    conn.commit()
    conn.close()

def test_time_parser():
    assert parse_time_to_minutes("12:30 PM") == 750
    assert parse_time_to_minutes("02:10 PM") == 850
    assert parse_time_to_minutes("12:30") == 750
    assert parse_time_to_minutes("14:10") == 850
    assert parse_time_to_minutes("10:00") == 600
    assert parse_time_to_minutes("08:00 AM") == 480
    assert parse_time_to_minutes("13:00") == 780

def test_check_lunch_overlap():
    assert check_lunch_overlap("12:30 PM", "02:10 PM") is True
    assert check_lunch_overlap("10:00", "13:00") is True
    assert check_lunch_overlap("08:00 AM", "09:40 AM") is False
    assert check_lunch_overlap("02:20 PM", "04:00 PM") is False
    assert check_lunch_overlap("12:30 PM - 02:10 PM") is True
    assert check_lunch_overlap("10:00 - 13:00") is True
    assert check_lunch_overlap("14:05 - 16:00") is False

def test_srm_mess_adapter():
    adapter = SRMMessAdapter()

    # 1. Ensure initial state
    adapter._ensure_sync_state()
    # Let's force NOT_CONNECTED just in case
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mess_sync_state SET status = 'NOT_CONNECTED' WHERE id = 'current'")
    conn.commit()
    conn.close()

    # 2. Check get_today_mess without any data
    res = adapter.get_today_mess("TEST-2026-10-09")
    assert res["status"] == "AWAITING_MENU"
    assert res["menu"] is None
    assert "upload hostel menu PDF/text in Brain Dump" in res["message"]
    assert res["timings"]["lunch"] == "12:30–14:00"

    # 3. Check exam overlap (2026-10-09 has an exam 12:30 PM - 02:10 PM)
    res_exam = adapter.get_today_mess("2026-10-09")
    assert "constraint_note" in res_exam
    assert "Exam overlaps standard lunch window" in res_exam["constraint_note"]

    # 4. Save a menu
    adapter.save_mess_menu(
        date="TEST-2026-10-09",
        breakfast="Idli",
        lunch="Meals",
        snacks="Tea",
        dinner="Roti",
        timings={"lunch": "12:00–14:00"},
        source="PDF_UPLOAD"
    )

    # 5. Check sync state updated
    assert adapter.get_sync_state() == "SYNCED"

    # 6. Check get_today_mess with data
    res_synced = adapter.get_today_mess("TEST-2026-10-09")
    assert res_synced["status"] == "SYNCED"
    assert res_synced["menu"]["breakfast"] == "Idli"
    assert res_synced["menu"]["lunch"] == "Meals"
    assert res_synced["timings"]["lunch"] == "12:00–14:00"

    # Check that another day returns awaiting menu
    res_other = adapter.get_today_mess("TEST-OTHER")
    assert res_other["status"] == "AWAITING_MENU"
    assert res_other["menu"] is None
