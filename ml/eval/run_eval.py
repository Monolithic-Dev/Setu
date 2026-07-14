"""
Evaluation harness — runs the question set through the actual retrieval
pipeline (dev-mode backend, per functions/queryFunction/index.py) and
computes real metrics, implementing docs/AIArchitecture.md §7's framework.

Run against dev-mode now; re-run against real QuickML once early access
exists (RiskRegister R1) — same harness, same question set, just swap
which backend answers the query. Numbers from THIS run are a dev-mode
baseline, not the final submission numbers — labeled as such wherever
they're reported (docs/PitchDeck.md Slide 12).
"""

import argparse
import json
import os
import sys
import time

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, REPO_ROOT)
from tests._helpers import load_function_module

from dataclasses import dataclass

_query_index = load_function_module("queryFunction", REPO_ROOT)
handle_request = _query_index.handle_request
retrieve = _query_index.retrieve


@dataclass
class EvalUser:
    user_id: str = "eval-runner"
    station_id: str = ""
    district_id: str = ""
    role_scope_level: str = "all"  # eval runs unscoped to measure retrieval quality, not RBAC


def run_eval(question_set_path: str) -> dict:
    with open(question_set_path, encoding="utf-8") as f:
        questions = json.load(f)

    auth_context = {"user": EvalUser(), "role_name": "scrb_analyst"}

    hits, misses, ranking_misses, true_misses = 0, 0, 0, 0
    latencies = []
    miss_details = []

    for q in questions:
        start = time.perf_counter()
        result = handle_request({"text": q["query_text"]}, auth_context)
        full_retrieval = retrieve(q["query_text"], EvalUser(), "scrb_analyst")
        latencies.append(time.perf_counter() - start)

        retrieved_ids = set(result["sources"])
        expected_ids = set(q["expected_case_ids"])
        full_retrieved_ids = {r["case_id"] for r in full_retrieval}

        if retrieved_ids & expected_ids:
            hits += 1
        else:
            misses += 1
            # Distinguish "found but ranked below the top-3 sources shown" from
            # "genuinely never retrieved at all" — very different problems.
            # Discovered this distinction mattered while debugging the first
            # eval run: some "misses" were actually ties between cases with
            # identical modus_operandi + district, not retrieval failures.
            if expected_ids & full_retrieved_ids:
                ranking_misses += 1
                miss_type = "ranking_cutoff"
            else:
                true_misses += 1
                miss_type = "not_retrieved_at_all"

            miss_details.append({
                "question_id": q["question_id"],
                "query_text": q["query_text"],
                "expected": q["expected_case_ids"],
                "got": result["sources"],
                "miss_type": miss_type,
            })

    n = len(questions)
    return {
        "n_questions": n,
        "retrieval_hit_rate": hits / n if n else 0.0,
        "hits": hits,
        "misses": misses,
        "ranking_cutoff_misses": ranking_misses,
        "true_misses": true_misses,
        "latency_p50_seconds": sorted(latencies)[len(latencies) // 2] if latencies else None,
        "latency_p95_seconds": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else None,
        "miss_details": miss_details,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-set", default="question_set.json")
    parser.add_argument("--out", default="eval_results.json")
    args = parser.parse_args()

    results = run_eval(args.question_set)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"DEV-MODE BASELINE (not final submission numbers — see module docstring)")
    print(f"Questions: {results['n_questions']}")
    print(f"Retrieval hit rate (top-3 sources): {results['retrieval_hit_rate']:.1%} ({results['hits']}/{results['n_questions']})")
    print(f"  of the {results['misses']} misses: {results['ranking_cutoff_misses']} were retrieved but ranked below top-3, "
          f"{results['true_misses']} were never retrieved at all")
    print(f"Latency p50: {results['latency_p50_seconds']:.4f}s, p95: {results['latency_p95_seconds']:.4f}s")
    if results["miss_details"]:
        print(f"\nFirst few misses:")
        for m in results["miss_details"][:3]:
            print(f"  {m['question_id']} [{m['miss_type']}]: expected {m['expected']}, got {m['got']}")


if __name__ == "__main__":
    main()
