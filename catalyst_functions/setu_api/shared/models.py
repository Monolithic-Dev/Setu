"""
Domain models matching docs/Database.md's ER diagram exactly — per
docs/CodingStandards.md §3, schema and code should never drift apart.

These are plain dataclasses, not tied to any specific Catalyst SDK call,
per docs/Design.md §1: domain logic stays independent of infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SensitivityLevel(str, Enum):
    STANDARD = "standard"
    RESTRICTED = "restricted"  # docs/Database.md §4a — independent access gate


class RoleName(str, Enum):
    STATION_OFFICER = "station_officer"
    SCRB_ANALYST = "scrb_analyst"
    DISTRICT_SP = "district_sp"
    SYSTEM_ADMIN = "system_admin"


@dataclass
class Location:
    location_id: str
    latitude: float
    longitude: float
    district: str
    station_jurisdiction: str


@dataclass
class CaseRecord:
    case_id: str
    fir_number: str
    filed_date: str
    modus_operandi: str
    weapon_type: str
    status: str
    narrative_en: str
    narrative_kn: str
    location_id: str
    sensitivity_level: SensitivityLevel = SensitivityLevel.STANDARD
    # Deliberately no demographic/socio-economic field exists on this model
    # at all (docs/Database.md §3) — not filtered out downstream, absent here.


@dataclass
class Person:
    person_id: str
    name: str
    role_in_case: str


@dataclass
class NetworkEdge:
    edge_id: str
    person_id_a: str
    person_id_b: str
    relationship_type: str
    confidence: float


@dataclass
class Role:
    role_id: str
    role_name: RoleName
    scope_level: str  # "station" | "district" | "state"


@dataclass
class User:
    user_id: str
    role_id: str
    station_id: str
    district_id: str = ""


@dataclass
class QueryLog:
    query_id: str
    user_id: str
    query_text: str
    language: str  # "en" | "kn"
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AuditEntry:
    audit_id: str
    query_id: str
    sources_used: list
    answer_summary: str
    flagged_helpful: bool | None = None  # FR-10.2, added Phase 7 review
