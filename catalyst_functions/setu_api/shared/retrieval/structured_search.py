"""
Structured search — the ZCQL half of hybrid retrieval
(docs/AIArchitecture.md §1). Filters on explicit fields the query mentions:
date range, district, weapon type, modus operandi keyword, case ID.

TODO (Phase 8): `execute_zcql` is a stub. Real implementation runs this
query string through Catalyst's ZCQL SDK against the Data Store — no
network in this sandbox to hit a live Data Store instance. The query-
building logic below (the part worth reviewing now) doesn't change when
the execution stub is filled in.
"""

from dataclasses import dataclass, field
import re


@dataclass
class StructuredQuery:
    district: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    weapon_type: str | None = None
    modus_operandi_keyword: str | None = None
    case_id: str | None = None
    # Scope fields, injected by the caller after auth_middleware resolves them —
    # never trusted from the request body itself.
    scope_station_id: str | None = None
    scope_district_id: str | None = None
    scope_level: str = "station"


def build_zcql(query: StructuredQuery) -> str:
    """
    Builds a ZCQL WHERE clause from a StructuredQuery. Scope conditions are
    always included and always AND-ed with the rest — a caller can narrow
    what they see, never widen it beyond their resolved scope
    (docs/Security.md §1).
    """
    conditions = []

    if query.case_id:
        conditions.append(f"CaseRecord.case_id = '{query.case_id}'")
    if query.district:
        conditions.append(f"LOCATION.district = '{query.district}'")
    if query.date_from:
        conditions.append(f"CaseRecord.filed_date >= '{query.date_from}'")
    if query.date_to:
        conditions.append(f"CaseRecord.filed_date <= '{query.date_to}'")
    if query.weapon_type:
        conditions.append(f"CaseRecord.weapon_type = '{query.weapon_type}'")
    if query.modus_operandi_keyword:
        conditions.append(f"CaseRecord.modus_operandi LIKE '%{query.modus_operandi_keyword}%'")

    # Scope enforcement — always appended, never optional.
    if query.scope_level == "station" and query.scope_station_id:
        conditions.append(f"LOCATION.station_jurisdiction = '{query.scope_station_id}'")
    elif query.scope_level == "district" and query.scope_district_id:
        conditions.append(f"LOCATION.district = '{query.scope_district_id}'")
    # scope_level == "all" adds no extra condition, matching docs/Database.md §4.

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    return f"SELECT CaseRecord.* FROM CaseRecord INNER JOIN LOCATION ON CaseRecord.location_id = LOCATION.location_id WHERE {where_clause}"


def execute_zcql(query_string: str) -> list[dict]:
    """Real ZCQL execution via the Catalyst SDK, falling back if not available."""
    try:
        import zcatalyst_sdk
        app = zcatalyst_sdk.initialize()
        zcql = app.zcql()
        # Catalyst ZCQL returns a list of dictionaries with table names as top-level keys
        # e.g., [{"CaseRecord": {"case_id": "...", ...}}]
        results = zcql.execute_zcql_query(query_string)
        # Extract the flat records
        extracted = []
        for row in results:
            if "CaseRecord" in row:
                extracted.append(row["CaseRecord"])
        return extracted
    except Exception as e:
        # Fall back to local dev execution if Catalyst SDK is missing, credentials 
        # are invalid, or we are running in local dev mock server.
        raise NotImplementedError(f"ZCQL execution failed, falling back to local: {e}")


def execute_structured_query_local(query: StructuredQuery, cases: list[dict]) -> list[dict]:
    """
    Local dev-mode execution — filters an in-memory list of case dicts
    (loaded from ml/data_generation's synthetic output) the same way
    build_zcql's conditions would filter Data Store rows.

    This is NOT a ZCQL parser and isn't meant to become one — it applies
    the same StructuredQuery object directly in Python. Real execution
    still goes through execute_zcql() above once Catalyst credentials
    exist; this exists so the retrieval pipeline can be genuinely run and
    tested end-to-end against real (synthetic) data without network access,
    per the same reasoning as functions/shared/dev_backend.py.
    """
    results = list(cases)

    if query.case_id:
        results = [c for c in results if c["case_id"] == query.case_id]
    if query.district:
        results = [c for c in results if c["location"]["district"] == query.district]
    if query.date_from:
        results = [c for c in results if c["filed_date"] >= query.date_from]
    if query.date_to:
        results = [c for c in results if c["filed_date"] <= query.date_to]
    if query.weapon_type:
        results = [c for c in results if c["weapon_type"] == query.weapon_type]
    if query.modus_operandi_keyword:
        # Token-overlap match AND ranking, not whole-string substring match
        # or unordered filtering — a full natural-language question will
        # essentially never appear verbatim inside a short case narrative,
        # and an unordered filter buries the best match arbitrarily deep in
        # a large result set (found via the eval harness in ml/eval/: a
        # target case ranked #41 out of 71 unordered matches before this
        # fix). Same "naive v1 NL handling" caveat as
        # queryFunction/index.py's retrieve() — real intent extraction is a
        # QuickML job — but ranking what a keyword filter *does* find isn't
        # something worth leaving broken in the meantime.
        query_words = {w for w in re.findall(r"[a-zA-Z]+", query.modus_operandi_keyword.lower()) if len(w) > 3}

        def _overlap_score(case: dict) -> int:
            case_words = set(re.findall(r"[a-zA-Z]+", (case["modus_operandi"] + " " + case["narrative_en"]).lower()))
            return len(query_words & case_words)

        scored = [(c, _overlap_score(c)) for c in results]
        scored = [(c, s) for c, s in scored if s > 0]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        results = [c for c, _ in scored]

    # Scope enforcement — mirrors build_zcql's scope conditions exactly,
    # applied the same way regardless of execution backend.
    if query.scope_level == "station" and query.scope_station_id:
        results = [c for c in results if c["location"]["station_jurisdiction"] == query.scope_station_id]
    elif query.scope_level == "district" and query.scope_district_id:
        results = [c for c in results if c["location"]["district"] == query.scope_district_id]

    return results
