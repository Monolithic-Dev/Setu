import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "shared"))

import local_audit_store


def _isolated_repo_root():
    """Each test gets its own temp 'repo root' so audit-log tests never
    interfere with each other or with the real data/dev_audit_log.json."""
    return tempfile.mkdtemp()


def test_append_and_read_round_trip():
    root = _isolated_repo_root()
    try:
        local_audit_store.append_entry(root, {"audit_id": "a1", "answer_summary": "test"})
        entries = local_audit_store.read_entries(root)
        assert len(entries) == 1
        assert entries[0]["audit_id"] == "a1"
    finally:
        shutil.rmtree(root)


def test_multiple_appends_accumulate_in_order():
    root = _isolated_repo_root()
    try:
        local_audit_store.append_entry(root, {"audit_id": "a1"})
        local_audit_store.append_entry(root, {"audit_id": "a2"})
        local_audit_store.append_entry(root, {"audit_id": "a3"})
        entries = local_audit_store.read_entries(root)
        assert [e["audit_id"] for e in entries] == ["a1", "a2", "a3"]
    finally:
        shutil.rmtree(root)


def test_read_entries_on_empty_store_returns_empty_list():
    root = _isolated_repo_root()
    try:
        assert local_audit_store.read_entries(root) == []
    finally:
        shutil.rmtree(root)


def test_store_file_is_valid_json_after_multiple_appends():
    """Guards against a corrupt-write bug (e.g., partial writes under
    concurrent access) — reads the raw file directly, not through the
    module's own reader, so a bug in read_entries couldn't mask a bug in append_entry."""
    root = _isolated_repo_root()
    try:
        for i in range(5):
            local_audit_store.append_entry(root, {"audit_id": f"a{i}"})
        path = local_audit_store._store_path(root)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)  # raises if the file is ever malformed
        assert len(data) == 5
    finally:
        shutil.rmtree(root)
