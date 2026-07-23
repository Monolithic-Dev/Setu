"""
Alerts Function — implements GET /api/alerts/hotspots from docs/APISpec.md.

Unlike queryFunction's LLM-dependent path, this one is fully real end to
end against the synthetic dataset — it reuses ml/prediction_model/hotspot_model.py
directly, which is genuinely tested (see tests/, and the standalone run in
this repo's build log). Scope-filtering by the requesting user's
station/district still needs to be layered on before this goes to Phase 8 —
marked below, not hidden.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ml", "prediction_model"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

from hotspot_model import load_cases, detect_hotspots, explain_cluster


def handle_request(auth_context: dict, data_path: str = None) -> dict:
    """
    Returns current hotspot alerts scoped to the requesting user.

    TODO(Phase 8): `data_path` currently points at the local synthetic JSON
    file for demo purposes; replace with a real Data Store/OLAP query once
    live credentials exist, and add the same station/district scope
    filtering that queryFunction applies (docs/Database.md §4) — this
    endpoint doesn't yet filter clusters by the requester's scope, which
    must be fixed before this is genuinely production-safe, not just demo-safe.
    """
    if data_path is None:
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "synthetic_cases.json"
        )

    cases = load_cases(data_path)
    clusters = detect_hotspots(cases)

    return {
        "alerts": [
            {
                "cluster_id": c.cluster_id,
                "district": c.district,
                "explanation": explain_cluster(c),
                "case_count": c.case_count,
            }
            for c in clusters[:10]
        ]
    }
