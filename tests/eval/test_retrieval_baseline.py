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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ml", "eval"))

from run_eval import run_eval


def test_dev_mode_recall_is_perfect_on_the_baseline_question_set():
    """
    Every one of the 40 baseline questions retrieves its target case
    somewhere in the full result set (0 true_misses) — this is the
    property that matters most: the system never fails to find a case
    that's genuinely there, per docs/TestingStrategy.md §2.
    """
    question_set_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "ml", "eval", "question_set.json"
    )
    results = run_eval(question_set_path)
    assert results["true_misses"] == 0, (
        f"{results['true_misses']} question(s) never retrieved their target case at all — "
        f"this is a genuine recall regression, not a ranking/tie issue."
    )


def test_dev_mode_top3_precision_meets_measured_baseline():
    """
    Precision@3 baseline is 57.5% (23/40) — driven by genuine ties between
    cases sharing identical modus_operandi + district in the synthetic
    data, not a retrieval bug (see PHASE8_STATUS.md). Threshold set with
    headroom below the measured value so minor data-generation-seed
    changes don't cause spurious failures, while still catching a real
    regression if precision drops meaningfully.
    """
    question_set_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "ml", "eval", "question_set.json"
    )
    results = run_eval(question_set_path)
    assert results["retrieval_hit_rate"] >= 0.45, (
        f"Top-3 precision dropped to {results['retrieval_hit_rate']:.1%}, "
        f"below the 45% floor (measured baseline was 57.5%)."
    )
