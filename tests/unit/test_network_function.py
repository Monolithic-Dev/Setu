import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests._helpers import load_function_module

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
network_index = load_function_module("networkFunction", REPO_ROOT)


def test_network_function_returns_real_graph_for_connected_person():
    """
    Proves fetch_edges_local returns genuine graph data, not an empty stub —
    finds whichever person is most connected in the generated dataset
    rather than hardcoding an ID, so this stays correct across reseeds.
    """
    from collections import Counter

    network = network_index._load_dev_network()
    edge_counts = Counter()
    for e in network["edges"]:
        edge_counts[e["person_id_a"]] += 1
        edge_counts[e["person_id_b"]] += 1
    most_connected_id, _ = edge_counts.most_common(1)[0]

    result = network_index.handle_request(most_connected_id, auth_context={})

    assert len(result["nodes"]) > 1, "A well-connected person should produce a multi-node graph"
    # Note: Jaccard link prediction will add edges between neighbors,
    # so not every edge involves most_connected_id.
    assert len(result["edges"]) > 0


def test_network_function_handles_isolated_entity_gracefully():
    """An entity_id with no edges should return a single-node graph, not crash."""
    result = network_index.handle_request("P-9999-does-not-exist", auth_context={})
    assert result["nodes"] == [{"id": "P-9999-does-not-exist", "label": "P-9999-does-not-exist"}]
    assert result["edges"] == []
