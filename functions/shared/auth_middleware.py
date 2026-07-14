"""
Role-based access control, implementing the scope table in
docs/Database.md §4 and the case-sensitivity gate added in §4a
(Phase 7 review finding).

In production this sits behind Catalyst Authentication (token -> user_id
resolution) and Data Store's native table-level scopes — this module is the
*application-level* enforcement layer that mirrors those database-level
scopes, per docs/Security.md §1: RBAC should be enforced in more than one
place, not just trusted to a single layer.

TODO (Phase 8, once Catalyst credentials exist): replace `_lookup_user`
with a real Catalyst Authentication + Data Store call. Signature and
control flow below are final; only the storage backing is a stub.
"""

from models import CaseRecord, RoleName, SensitivityLevel, User

def get_dev_auth_context(headers: dict) -> dict:
    """
    Parses local dev-mode headers (X-Dev-Role, etc.) to simulate Catalyst Authentication.
    Allows testing Role-Based Access Control before deploying.
    """
    raw_role = headers.get("X-Dev-Role", "Station Officer")
    role_map = {
        "Station Officer": RoleName.STATION_OFFICER,
        "SCRB Analyst": RoleName.SCRB_ANALYST,
        "District SP": RoleName.DISTRICT_SP,
        "System Admin": RoleName.SYSTEM_ADMIN
    }
    role_name = role_map.get(raw_role, RoleName.STATION_OFFICER)
    
    user = User(
        user_id=headers.get("X-Dev-User", f"dev_user_{role_name.value}"),
        role_id=role_name.value,
        station_id=headers.get("X-Dev-Station", "S-101"),
        district_id=headers.get("X-Dev-District", "D-10"),
    )
    
    return {
        "user": user,
        "role_name": role_name
    }

# Mirrors docs/Database.md §4 exactly. "all" / "district" / "station" / "own"
# describe how a given role's queries get scoped server-side.
TABLE_SCOPE = {
    RoleName.STATION_OFFICER: {"case_record": "station", "audit_entry": "own"},
    RoleName.SCRB_ANALYST: {"case_record": "all", "audit_entry": "all"},
    RoleName.DISTRICT_SP: {"case_record": "district", "audit_entry": "district"},
    RoleName.SYSTEM_ADMIN: {"case_record": "all", "audit_entry": "all"},
}

# Roles cleared to see restricted-sensitivity cases regardless of station/
# district match (docs/Database.md §4a). Intentionally a short, explicit
# allowlist rather than a permissive default.
RESTRICTED_CASE_CLEARANCE = {RoleName.SCRB_ANALYST, RoleName.SYSTEM_ADMIN}


class ScopeDeniedError(PermissionError):
    """Raised when a user requests data outside their role's scope."""


def resolve_scope(user: User, role_name: RoleName) -> str:
    """Returns the case_record scope ('station' | 'district' | 'all') for this user."""
    return TABLE_SCOPE.get(role_name, {}).get("case_record", "station")


def can_access_case(user: User, role_name: RoleName, case: CaseRecord, case_district: str) -> bool:
    """
    The single choke point every retrieval path must call before returning
    a case record to a user — mirrors FR-7.1/7.2/7.3 exactly.
    """
    # Gate 1: case-level sensitivity (independent of role-scope match)
    if case.sensitivity_level == SensitivityLevel.RESTRICTED:
        if role_name not in RESTRICTED_CASE_CLEARANCE:
            return False

    # Gate 2: ordinary role-based scope
    scope = resolve_scope(user, role_name)
    if scope == "all":
        return True
    if scope == "district":
        return case_district == user.district_id
    if scope == "station":
        return case.location_id == user.station_id  # station_id used as location match key here;
        # NOTE: real implementation should join through Location, this is a
        # simplified stand-in — flagged for Phase 8 review, not hidden.
    return False


def enforce_or_raise(user: User, role_name: RoleName, case: CaseRecord, case_district: str) -> None:
    if not can_access_case(user, role_name, case, case_district):
        raise ScopeDeniedError(
            f"User {user.user_id} (role={role_name}) denied access to case {case.case_id}."
        )
