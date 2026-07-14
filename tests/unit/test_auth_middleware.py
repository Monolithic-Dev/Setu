import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "shared"))

import pytest
from auth_middleware import can_access_case, enforce_or_raise, ScopeDeniedError
from models import CaseRecord, RoleName, SensitivityLevel, User


def make_case(sensitivity=SensitivityLevel.STANDARD, location_id="STN-001"):
    return CaseRecord(
        case_id="KA-2026-00001", fir_number="FIR/2026/1001", filed_date="2026-01-01",
        modus_operandi="test mo", weapon_type="none", status="under investigation",
        narrative_en="test", narrative_kn="test", location_id=location_id,
        sensitivity_level=sensitivity,
    )


def test_station_officer_sees_own_station_case():
    user = User(user_id="u1", role_id="r1", station_id="STN-001", district_id="D1")
    case = make_case(location_id="STN-001")
    assert can_access_case(user, RoleName.STATION_OFFICER, case, case_district="D1") is True


def test_station_officer_denied_other_station_case():
    user = User(user_id="u1", role_id="r1", station_id="STN-001", district_id="D1")
    case = make_case(location_id="STN-999")
    assert can_access_case(user, RoleName.STATION_OFFICER, case, case_district="D1") is False


def test_district_sp_sees_any_station_in_own_district():
    user = User(user_id="u2", role_id="r2", station_id="STN-005", district_id="D1")
    case = make_case(location_id="STN-999")  # different station, same district
    assert can_access_case(user, RoleName.DISTRICT_SP, case, case_district="D1") is True


def test_district_sp_denied_other_district():
    user = User(user_id="u2", role_id="r2", station_id="STN-005", district_id="D1")
    case = make_case(location_id="STN-999")
    assert can_access_case(user, RoleName.DISTRICT_SP, case, case_district="D2") is False


def test_scrb_analyst_sees_all():
    user = User(user_id="u3", role_id="r3", station_id="STN-001", district_id="D1")
    case = make_case(location_id="STN-999")
    assert can_access_case(user, RoleName.SCRB_ANALYST, case, case_district="D9") is True


def test_restricted_case_denied_to_station_officer_even_in_own_station():
    """The case-sensitivity gate (Database.md §4a) overrides an otherwise-valid role match."""
    user = User(user_id="u1", role_id="r1", station_id="STN-001", district_id="D1")
    case = make_case(sensitivity=SensitivityLevel.RESTRICTED, location_id="STN-001")
    assert can_access_case(user, RoleName.STATION_OFFICER, case, case_district="D1") is False


def test_restricted_case_allowed_for_scrb_analyst():
    user = User(user_id="u3", role_id="r3", station_id="STN-001", district_id="D1")
    case = make_case(sensitivity=SensitivityLevel.RESTRICTED, location_id="STN-999")
    assert can_access_case(user, RoleName.SCRB_ANALYST, case, case_district="D9") is True


def test_enforce_or_raise_raises_scope_denied():
    user = User(user_id="u1", role_id="r1", station_id="STN-001", district_id="D1")
    case = make_case(location_id="STN-999")
    with pytest.raises(ScopeDeniedError):
        enforce_or_raise(user, RoleName.STATION_OFFICER, case, case_district="D1")
