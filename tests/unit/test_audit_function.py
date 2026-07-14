import sys
import os
import shutil
import tempfile
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests._helpers import load_function_module

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def test_audit_function_denies_station_officer():
    audit_index = load_function_module("auditFunction", REPO_ROOT)
    result = audit_index.handle_request({"role_name": "station_officer"})
    assert result["status"] == "error"
    assert result["error_code"] == "SCOPE_DENIED"


def test_audit_function_allows_scrb_analyst():
    audit_index = load_function_module("auditFunction", REPO_ROOT)
    result = audit_index.handle_request({"role_name": "scrb_analyst"})
    assert "entries" in result
    assert "status" not in result  # no error shape on the success path


def test_audit_function_allows_district_sp_and_admin():
    audit_index = load_function_module("auditFunction", REPO_ROOT)
    for role in ("district_sp", "system_admin"):
        result = audit_index.handle_request({"role_name": role})
        assert "entries" in result, f"{role} should have audit access"


def test_query_function_actually_persists_and_audit_function_actually_reads_it():
    """
    End-to-end integration: a real query through queryFunction should
    produce a real entry that auditFunction can then read — not two
    independently-tested halves that were never proven to connect.
    Uses an isolated temp repo root so this doesn't pollute the real
    dev-mode audit log or depend on test execution order.
    """
    import local_audit_store

    query_index = load_function_module("queryFunction", REPO_ROOT)
    audit_index = load_function_module("auditFunction", REPO_ROOT)

    temp_root = tempfile.mkdtemp()
    try:
        original_repo_root = query_index._REPO_ROOT
        original_audit_root = audit_index._REPO_ROOT
        query_index._REPO_ROOT = temp_root
        audit_index._REPO_ROOT = temp_root

        @dataclass
        class FakeAnalyst:
            user_id: str = "analyst-1"
            station_id: str = ""
            district_id: str = ""
            role_scope_level: str = "all"

        auth_context = {"user": FakeAnalyst(), "role_name": "scrb_analyst"}
        query_index.handle_request({"text": "chain snatching market"}, auth_context)

        result = audit_index.handle_request({"role_name": "scrb_analyst"})
        assert len(result["entries"]) == 1
        assert result["entries"][0]["query_text"] == "chain snatching market"
    finally:
        query_index._REPO_ROOT = original_repo_root
        audit_index._REPO_ROOT = original_audit_root
        shutil.rmtree(temp_root)
