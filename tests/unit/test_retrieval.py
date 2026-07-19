import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "setu_api", "shared", "retrieval"))

from structured_search import StructuredQuery, build_zcql
from semantic_search import SemanticMatch, merge_and_rank


def test_build_zcql_includes_requested_filters():
    query = StructuredQuery(district="Mysuru", weapon_type="knife", scope_level="all")
    zcql = build_zcql(query)
    assert "district = 'Mysuru'" in zcql
    assert "weapon_type = 'knife'" in zcql


def test_build_zcql_always_enforces_station_scope():
    """A station-level user's query can never widen beyond their own station,
    even if they don't explicitly filter by it (docs/Security.md §1)."""
    query = StructuredQuery(scope_level="station", scope_station_id="STN-001")
    zcql = build_zcql(query)
    assert "LOCATION.station_jurisdiction = 'STN-001'" in zcql


def test_build_zcql_district_scope_not_station_scope():
    query = StructuredQuery(scope_level="district", scope_district_id="D1")
    zcql = build_zcql(query)
    assert "LOCATION.district = 'D1'" in zcql
    assert "station_id" not in zcql


def test_build_zcql_all_scope_adds_no_extra_condition():
    query = StructuredQuery(scope_level="all")
    zcql = build_zcql(query)
    assert "WHERE 1=1" in zcql


def test_merge_deduplicates_by_case_id():
    structured = [{"case_id": "KA-001", "modus_operandi": "theft"}]
    semantic = [
        SemanticMatch(case_id="KA-001", similarity_score=0.9, matched_text="dup"),
        SemanticMatch(case_id="KA-002", similarity_score=0.8, matched_text="new"),
    ]
    merged = merge_and_rank(structured, semantic)
    case_ids = [r["case_id"] for r in merged]
    assert case_ids.count("KA-001") == 1
    assert "KA-002" in case_ids


def test_merge_prioritizes_structured_hits_first():
    structured = [{"case_id": "KA-001"}]
    semantic = [SemanticMatch(case_id="KA-002", similarity_score=0.99, matched_text="x")]
    merged = merge_and_rank(structured, semantic)
    assert merged[0]["case_id"] == "KA-001"
    assert merged[0]["match_type"] == "structured"
