"""
Integration smoke test for queryFunction — proves the pipeline actually
wires together (imports resolve, function signatures match, no runtime
errors) end to end, even though the real QuickML/ZCQL calls are stubbed.
This is exactly the kind of test that would have caught an import typo or
a signature mismatch before Phase 8 — cheap to run, catches real bugs.

Uses tests/_helpers.py's load_function_module instead of sys.path + `from
index import` — see that file's docstring for why: multiple functions/*/
index.py files collide in sys.modules under the plain name "index" when
more than one gets imported in the same process, which a full test-suite
run does. Found via a real collision, not a hypothetical one.
"""

import sys
import os
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests._helpers import load_function_module

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
query_index = load_function_module("queryFunction", REPO_ROOT)

handle_request = query_index.handle_request
detect_language = query_index.detect_language
QueryFunctionError = query_index.QueryFunctionError


@dataclass
class FakeUser:
    user_id: str = "u1"
    station_id: str = "STN-001"
    district_id: str = "D1"


def test_detect_language_kannada():
    assert detect_language("ಇದು ಕನ್ನಡ ಪಠ್ಯ") == "kn"


def test_detect_language_english():
    assert detect_language("this is english text") == "en"


def test_handle_request_end_to_end_with_no_matches():
    """With retrieval stubbed to return nothing (no live Data Store/QuickML
    in this sandbox), the pipeline should still complete cleanly and return
    a well-formed 'not found' response rather than crashing."""
    auth_context = {"user": FakeUser(), "role_name": "station_officer"}
    result = handle_request({"text": "any question"}, auth_context)

    assert "answer" in result
    assert "sources" in result
    assert "audit_id" in result
    assert result["language"] == "en"


def test_handle_request_rejects_empty_query():
    auth_context = {"user": FakeUser(), "role_name": "station_officer"}
    try:
        handle_request({"text": "   "}, auth_context)
        raise AssertionError("Expected QueryFunctionError for empty query text")
    except QueryFunctionError as e:
        assert e.error_code == "BAD_REQUEST"


def _get_real_case_at_station_any(sensitivity: str) -> dict:
    import json
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "synthetic_cases.json"),
              encoding="utf-8") as f:
        cases = json.load(f)
    matches = [c for c in cases if c["sensitivity_level"] == sensitivity]
    if not matches:
        raise RuntimeError(f"No case with sensitivity={sensitivity!r} found — regenerate the dataset.")
    return matches[0]


def test_real_retrieval_finds_an_actual_matching_case():
    """Proves the dev-mode pipeline genuinely retrieves real data, not just
    returning 'not found' for everything — caught during manual verification
    that this needed an actual assertion, not just an eyeballed print statement."""
    @dataclass
    class FakeAnalyst:
        user_id: str = "analyst-1"
        station_id: str = ""
        district_id: str = ""
        role_scope_level: str = "all"

    auth_context = {"user": FakeAnalyst(), "role_name": "scrb_analyst"}
    result = handle_request({"text": "chain snatching market"}, auth_context)

    assert "not found" not in result["answer"].lower()
    assert len(result["sources"]) > 0


def test_station_officer_cannot_see_restricted_case_at_own_station():
    """Regression test for real behavior discovered during manual dev-mode
    verification: a restricted-sensitivity case is denied even to an
    officer at the exact station it belongs to (docs/Database.md §4a,
    FR-7.3) — this was initially mistaken for a bug until traced back to
    the sensitivity gate working as designed."""
    restricted_case = _get_real_case_at_station_any(sensitivity="restricted")

    @dataclass
    class FakeStationOfficer:
        user_id: str = "officer-1"
        station_id: str = restricted_case["location"]["station_jurisdiction"]
        district_id: str = ""
        role_scope_level: str = "station"

    auth_context = {"user": FakeStationOfficer(), "role_name": "station_officer"}
    mo_keyword = " ".join(restricted_case["modus_operandi"].split()[:2])
    result = handle_request({"text": mo_keyword}, auth_context)

    assert result.get("error_code") == "SCOPE_DENIED"
