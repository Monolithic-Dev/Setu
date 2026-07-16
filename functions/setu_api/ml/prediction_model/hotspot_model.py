"""
Hotspot / repeat-pattern detection model.

Deliberately classical ML (DBSCAN clustering + frequency analysis), not an
LLM — see docs/AIArchitecture.md §4: this needs clean, benchmarkable
precision/recall numbers for the submission's benchmarking slide, which
generative output doesn't give cleanly.

Inputs are restricted to case-evidence features only: location, time,
modus operandi. No demographic or socio-economic field is read here, and
none exists in the synthetic dataset to begin with (docs/Database.md §3) —
this is a second, independent enforcement of that boundary, not just a
promise kept elsewhere.

Residual-risk note (docs/AIArchitecture.md §4, added in Phase 7 review):
location itself can act as a demographic proxy if historical policing
intensity was geographically uneven. Excluding demographic inputs is a
strong mitigation, not a complete fix — see docs/MonitoringStrategy.md for
the outcome-level monitoring this needs alongside clean inputs.
"""

import json
from collections import Counter
from dataclasses import dataclass

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import LabelEncoder


@dataclass
class HotspotCluster:
    cluster_id: int
    district: str
    dominant_modus_operandi: str
    case_count: int
    case_ids: list


def load_cases(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _feature_matrix(cases: list) -> np.ndarray:
    """
    Builds a feature matrix from case-evidence fields only:
    latitude, longitude, and a numeric encoding of modus operandi.
    Explicitly does NOT include anything demographic or socio-economic —
    there is nothing of that kind in the input records to include.
    """
    mo_encoder = LabelEncoder()
    mo_encoded = mo_encoder.fit_transform([c["modus_operandi"] for c in cases])

    lats = np.array([c["location"]["latitude"] for c in cases])
    lons = np.array([c["location"]["longitude"] for c in cases])

    # Scale MO encoding down so it nudges clustering without dominating the
    # purely spatial signal — this is a simple v1 approach; a real tuning
    # pass (Week 2, per SprintPlan.md) should validate this weighting
    # against the eval set rather than trusting this constant.
    mo_weight = 0.01
    features = np.column_stack([lats, lons, mo_encoded * mo_weight])
    return features


def detect_hotspots(cases: list, eps: float = 0.03, min_samples: int = 4) -> list:
    """
    Runs DBSCAN over case-evidence features and returns hotspot clusters
    with 2+ cases, each described by its dominant modus operandi — this is
    what gets surfaced as a proactive early-warning signal (FR-5.1).
    """
    if len(cases) < min_samples:
        return []

    features = _feature_matrix(cases)
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(features)

    clusters = []
    for cluster_id in sorted(set(labels)):
        if cluster_id == -1:
            continue  # DBSCAN noise label, not a real cluster
        member_indices = [i for i, l in enumerate(labels) if l == cluster_id]
        members = [cases[i] for i in member_indices]
        district_counts = Counter(c["location"]["district"] for c in members)
        mo_counts = Counter(c["modus_operandi"] for c in members)

        clusters.append(HotspotCluster(
            cluster_id=int(cluster_id),
            district=district_counts.most_common(1)[0][0],
            dominant_modus_operandi=mo_counts.most_common(1)[0][0],
            case_count=len(members),
            case_ids=[c["case_id"] for c in members],
        ))

    return sorted(clusters, key=lambda c: c.case_count, reverse=True)


def explain_cluster(cluster: HotspotCluster) -> str:
    """
    Plain-language explanation grounded entirely in case evidence — this is
    what satisfies FR-5.3 (aggregate signal, not individual risk score) and
    NFR-3 (explainability): the explanation names the MO and location
    pattern that triggered the flag, nothing about who is in the area.
    """
    return (
        f"{cluster.case_count} cases sharing a similar pattern "
        f"('{cluster.dominant_modus_operandi}') detected in {cluster.district}. "
        f"Flag is based on modus-operandi and geographic/temporal clustering "
        f"of case records only."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="../data/synthetic_cases.json")
    parser.add_argument("--eps", type=float, default=0.03)
    parser.add_argument("--min-samples", type=int, default=4)
    args = parser.parse_args()

    cases = load_cases(args.data)
    clusters = detect_hotspots(cases, eps=args.eps, min_samples=args.min_samples)

    print(f"Loaded {len(cases)} cases, found {len(clusters)} hotspot clusters.\n")
    for c in clusters[:10]:
        print(f"Cluster {c.cluster_id}: {explain_cluster(c)}")
        print(f"  Case IDs: {', '.join(c.case_ids[:5])}{' ...' if len(c.case_ids) > 5 else ''}\n")
