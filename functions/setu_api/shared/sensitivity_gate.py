from models import CaseRecord, RoleName, SensitivityLevel
from auth_middleware import RESTRICTED_CASE_CLEARANCE, ScopeDeniedError

def check_sensitivity(case: CaseRecord, role_name: RoleName) -> None:
    """
    Gate 1: Case-level sensitivity check (independent of role-scope match).
    Called before returning any CASE_RECORD-derived data.
    """
    if case.sensitivity_level == SensitivityLevel.RESTRICTED:
        if role_name not in RESTRICTED_CASE_CLEARANCE:
            raise ScopeDeniedError(
                f"Case {case.case_id} is restricted and requires special clearance."
            )
