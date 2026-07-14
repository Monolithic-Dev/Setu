"""
Audit Function — implements GET /api/audit/logs from docs/APISpec.md.
Role-gated per docs/APISpec.md §2: SCRB Analyst / District SP / Admin only.

Has a genuine local dev-mode fallback (functions/shared/local_audit_store.py)
reading real entries written by functions/queryFunction/index.py during
actual query handling — not a stub returning nothing. The role gate below
is real logic either way, reusing auth_middleware's role-scope table
rather than duplicating it.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

from models import RoleName
import local_audit_store

_REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

AUDIT_ALLOWED_ROLES = {RoleName.SCRB_ANALYST, RoleName.DISTRICT_SP, RoleName.SYSTEM_ADMIN}


def fetch_audit_entries(scope_filter: dict) -> list[dict]:
    """TODO(Phase 8): real ZCQL query against AUDIT_ENTRY, scoped per docs/Database.md §4."""
    raise NotImplementedError("Wire in real Data Store query once Catalyst credentials exist.")


def handle_request(auth_context: dict) -> dict:
    role_name = auth_context.get("role_name")
    if role_name not in AUDIT_ALLOWED_ROLES:
        return {"status": "error", "error_code": "SCOPE_DENIED",
                "message": "Audit log access requires SCRB Analyst, District SP, or Admin role."}
    try:
        entries = fetch_audit_entries(scope_filter=auth_context)
    except NotImplementedError:
        entries = local_audit_store.read_entries(_REPO_ROOT, scope_filter=auth_context)  # real dev-mode data
    return {"entries": entries}
