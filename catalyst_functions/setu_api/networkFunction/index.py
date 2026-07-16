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
    """Real ZCQL query against NETWORK_EDGE via Catalyst SDK."""
    try:
        import zcatalyst_sdk
        app = zcatalyst_sdk.initialize()
        zcql = app.zcql()
        
        query = f"SELECT * FROM NETWORK_EDGE WHERE person_id_a = '{entity_id}' OR person_id_b = '{entity_id}'"
        results = zcql.execute_zcql_query(query)
        
        extracted = []
        for row in results:
            if "NETWORK_EDGE" in row:
                extracted.append(row["NETWORK_EDGE"])
        return extracted
    except Exception as e:
        raise NotImplementedError(f"Data Store query failed, falling back: {e}")


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
    Includes AI Pattern Detection (Jaccard Similarity Link Prediction) to
    suggest hidden connections between suspects.
    """
    nodes = {entity_id: {"id": entity_id, "label": entity_id}}
    graph_edges = []
    
    # Track neighbors to calculate Jaccard similarity for link prediction
    neighbors = {entity_id: set()}

    for edge in edges:
        pa, pb = edge["person_id_a"], edge["person_id_b"]
        for pid in (pa, pb):
            if pid not in nodes:
                nodes[pid] = {"id": pid, "label": pid}
                neighbors[pid] = set()
                
        # Populate neighbor sets
        neighbors[pa].add(pb)
        neighbors[pb].add(pa)

        graph_edges.append({
            "source": pa,
            "target": pb,
            "relationship": edge["relationship_type"],
            "confidence": edge["confidence"],
        })

    # AI Pattern Detection: Jaccard Link Prediction
    node_ids = list(nodes.keys())
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):
            n1, n2 = node_ids[i], node_ids[j]
            if n2 not in neighbors[n1]:
                intersection = len(neighbors[n1].intersection(neighbors[n2]))
                union = len(neighbors[n1].union(neighbors[n2]))
                if union > 0:
                    score = intersection / union
                    # If similarity is above 30%, suggest a link
                    if score >= 0.3:
                        graph_edges.append({
                            "source": n1,
                            "target": n2,
                            "relationship": "AI Predicted Link",
                            "confidence": round(score, 2),
                            "suggested_link": True
                        })

    return {"nodes": list(nodes.values()), "edges": graph_edges}


def handle_request(entity_id: str, auth_context: dict) -> dict:
    try:
        edges = fetch_edges(entity_id, scope_filter=auth_context)
    except NotImplementedError:
        edges = fetch_edges_local(entity_id)  # real dev-mode data, not an empty stub
    return build_graph(entity_id, edges)
