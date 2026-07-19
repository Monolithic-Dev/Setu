"""
Regression test for the dev-mode retrieval baseline — locks in the real
numbers measured via ml/eval/run_eval.py so a future change to
structured_search.py or semantic_search.py can't silently regress
retrieval quality without a test failing.

Thresholds below are set from the actual measured baseline (see
ml/eval/eval_results.json), not aspirational targets — update them
deliberately if a real improvement changes the numbers, don't just loosen
them to make a failing test pass.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "catalyst_functions", "setu_api", "ml", "eval"))

from run_eval import run_eval


def test_dev_mode_recall_is_perfect_on_the_baseline_question_set():
    """
    Every one of the 40 baseline questions retrieves its target case
    somewhere in the full result set (0 true_misses) — this is the
    property that matters most: the system never fails to find a case
    that's genuinely there, per docs/TestingStrategy.md §2.
    """
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "functions", "setu_api", "ml", "eval", "eval_set_en.json"
        )
    ) as f:
        eval_set = json.load(f)

    results = evaluate_retrieval(eval_set)

    # These baseline thresholds are the expected dev-mode performance of the
    # naive TF-IDF + Regex extraction fallback, ensuring it doesn't degrade.
    # QuickML RAG integration (Phase 8) will raise these numbers.
    assert results["recall"] >= 1.0, f"Recall dropped below 1.0: {results['recall']}"
    assert results["precision"] >= 0.55, f"Precision dropped below 0.55: {results['precision']}"


def test_retrieval_baseline_kn():
    """Ensures Kannada dev-mode retrieval baseline hasn't degraded."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "setu_api", "ml", "eval"))
    from eval_harness import evaluate_retrieval

    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "functions", "setu_api", "ml", "eval", "eval_set_kn.json"
        )
    ) as f:
        eval_set = json.load(f)
    results = evaluate_retrieval(eval_set)
    assert results["recall"] >= 1.0, f"Recall (KN) dropped below 1.0: {results['recall']}"
    assert results["precision"] >= 0.55, f"Precision (KN) dropped below 0.55: {results['precision']}"
