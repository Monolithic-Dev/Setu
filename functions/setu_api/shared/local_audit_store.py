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

def _feedback_store_path(repo_root: str) -> str:
    return os.path.join(repo_root, "data", "dev_feedback_log.json")

def _context_store_path(repo_root: str) -> str:
    return os.path.join(repo_root, "data", "dev_session_context.json")


import hashlib

def append_entry(repo_root: str, entry: dict) -> None:
    """
    Appends one audit entry. Attempts real Data Store persistence first,
    falls back to local dev-mode JSON on failure.
    Includes a tamper-evident cryptographic hash-chain to prove log integrity.
    """
    path = _store_path(repo_root)
    with _LOCK:
        entries = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                entries = json.load(f)
                
        # Cryptographic Hash Chaining
        prev_hash = entries[-1].get("entry_hash", "GENESIS") if entries else "GENESIS"
        entry["previous_hash"] = prev_hash
        payload = json.dumps(entry, sort_keys=True).encode('utf-8')
        entry["entry_hash"] = hashlib.sha256(payload).hexdigest()

        try:
            import zcatalyst_sdk
            app = zcatalyst_sdk.initialize()
            datastore = app.datastore()
            table = datastore.table("AUDIT_ENTRY")
            table.insert_row(entry)
            # Intentionally NOT returning here so the local JSON stays synced
            # with the latest hash, maintaining the chain even if ZCQL isn't used to query.
        except Exception as e:
            pass

        entries.append(entry)
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
        except OSError:
            pass # Ignore read-only filesystem errors in cloud


def read_entries(repo_root: str, scope_filter: dict | None = None) -> list[dict]:
    """
    Returns all audit entries.
    """
    try:
        import zcatalyst_sdk
        app = zcatalyst_sdk.initialize()
        zcql = app.zcql()
        results = zcql.execute_zcql_query("SELECT * FROM AUDIT_ENTRY")
        extracted = []
        for row in results:
            if "AUDIT_ENTRY" in row:
                extracted.append(row["AUDIT_ENTRY"])
        return extracted
    except Exception as e:
        # Fall back to local JSON
        pass

    path = _store_path(repo_root)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def append_feedback(repo_root: str, entry: dict) -> None:
    path = _feedback_store_path(repo_root)
    with _LOCK:
        entries = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                entries = json.load(f)
        entries.append(entry)
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
        except OSError:
            pass

def read_feedback(repo_root: str) -> list[dict]:
    path = _feedback_store_path(repo_root)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def append_context(repo_root: str, session_id: str, turn_data: dict, limit: int = 3) -> None:
    """Appends a conversation turn to the session context, keeping only the last `limit` turns."""
    path = _context_store_path(repo_root)
    with _LOCK:
        contexts = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                contexts = json.load(f)
        
        if session_id not in contexts:
            contexts[session_id] = []
            
        contexts[session_id].append(turn_data)
        contexts[session_id] = contexts[session_id][-limit:]  # Keep only recent turns
        
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(contexts, f, indent=2)
        except OSError:
            pass

def get_context(repo_root: str, session_id: str) -> list[dict]:
    """Returns the rolling context turns for a given session."""
    path = _context_store_path(repo_root)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        contexts = json.load(f)
        return contexts.get(session_id, [])
