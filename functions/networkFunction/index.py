"""
Network Function — implements GET /api/network/{entityId} from docs/APISpec.md.

Builds a graph structure from NETWORK_EDGE records (docs/Database.md ER
diagram), scoped to the requester (docs/Security.md §1).

Has a genuine local dev-mode fallback (fetch_edges_local), same pattern as
functions/shared/retrieval/ — real filtering over real synthetic network
data (ml/data_generation/generate_dataset.py's --persons-out output), not
a stub returning nothing. TODO(Phase 8): `fetch_edges` (the real path) is
still a stub pending real Data Store access; the graph-shaping logic below
doesn't change once that's wired in.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

_DEV_NETWORK_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "synthetic_network.json")
_dev_network_cache = None


def fetch_edges(entity_id: str, scope_filter: dict) -> list[dict]:
    """TODO(Phase 8): real ZCQL query against NETWORK_EDGE, scoped per docs/Database.md §4."""
    raise NotImplementedError("Wire in real Data Store query once Catalyst credentials exist.")


def _load_dev_network() -> dict:
    global _dev_network_cache
    if _dev_network_cache is None:
        with open(_DEV_NETWORK_PATH, encoding="utf-8") as f:
            _dev_network_cache = json.load(f)
    return _dev_network_cache


def fetch_edges_local(entity_id: str) -> list[dict]:
    """
    Real local dev-mode: returns every edge touching entity_id from the
    synthetic network data. Not a stub — genuinely filters real generated
    graph structure, standing in for the real Data Store query above.
    """
    network = _load_dev_network()
    return [
        e for e in network["edges"]
        if e["person_id_a"] == entity_id or e["person_id_b"] == entity_id
    ]


def build_graph(entity_id: str, edges: list[dict]) -> dict:
    """
    Shapes raw edge records into a { nodes, edges } structure the frontend's
    D3.js graph component can render directly (docs/TechStack.md).
    """
    nodes = {entity_id: {"id": entity_id, "label": entity_id}}
    graph_edges = []

    for edge in edges:
        for pid in (edge["person_id_a"], edge["person_id_b"]):
            if pid not in nodes:
                nodes[pid] = {"id": pid, "label": pid}
        graph_edges.append({
            "source": edge["person_id_a"],
            "target": edge["person_id_b"],
            "relationship": edge["relationship_type"],
            "confidence": edge["confidence"],
        })

    return {"nodes": list(nodes.values()), "edges": graph_edges}


def handle_request(entity_id: str, auth_context: dict) -> dict:
    try:
        edges = fetch_edges(entity_id, scope_filter=auth_context)
    except NotImplementedError:
        edges = fetch_edges_local(entity_id)  # real dev-mode data, not an empty stub
    return build_graph(entity_id, edges)
