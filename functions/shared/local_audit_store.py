"""
Local dev-mode audit log persistence — append-only JSON store standing in
for the real Data Store AUDIT_ENTRY table (docs/Database.md ER diagram).

Until now, queryFunction created AuditEntry objects and discarded them
(the TODO said "stubbed here since there's no live Data Store connection")
— which meant auditFunction had structurally-correct RBAC logic but
literally nothing to show even in dev-mode. This closes that loop: real
persistence, real retrieval, same append-only guarantee docs/Security.md
§3 requires of the real implementation ("no update/delete permission
granted on the AUDIT_ENTRY table to any role except System Admin").
"""

import json
import os
import threading

_LOCK = threading.Lock()  # dev-mode only; real Data Store handles this concurrency for real


def _store_path(repo_root: str) -> str:
    return os.path.join(repo_root, "data", "dev_audit_log.json")


def append_entry(repo_root: str, entry: dict) -> None:
    """
    Appends one audit entry. Append-only by construction — this function
    has no delete/update counterpart, deliberately, mirroring
    docs/Security.md §3's real access-control requirement at the code
    level for dev-mode too, not just documenting it as a future rule.
    """
    path = _store_path(repo_root)
    with _LOCK:
        entries = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                entries = json.load(f)
        entries.append(entry)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)


def read_entries(repo_root: str, scope_filter: dict | None = None) -> list[dict]:
    """
    Returns all audit entries. `scope_filter` is accepted for interface
    parity with the real Data Store query but not yet applied here — dev-
    mode audit entries don't currently carry enough scope metadata
    (station/district) to filter by it meaningfully; every entry is
    visible in dev-mode regardless of scope_filter. auditFunction's
    role-gate (SCRB Analyst/District SP/Admin only) still applies before
    this is ever called — that's the real access boundary, not this filter.
    """
    path = _store_path(repo_root)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)
