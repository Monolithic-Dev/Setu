"""
Ensures the synthetic dataset exists before any test that needs it runs —
several tests in integration/ and eval/ depend on data/synthetic_cases.json,
which is correctly gitignored as generated output (not something to commit).
Without this, a fresh clone fails tests with a raw FileNotFoundError instead
of a clear signal of what's missing — found via a genuine fresh-extraction
test run while packaging this repo, not a hypothetical concern.

Real pytest picks this file up automatically. run_tests_locally.py (the
no-network-fallback runner) calls the same function directly — see its
top-level setup call.
"""

import json
import os
import random
import sys

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
# Canonical data location: inside the function bundle (committed, deployed with the function)
DATA_PATH = os.path.join(REPO_ROOT, "functions", "setu_api", "data", "synthetic_cases.json")

def ensure_synthetic_data(n_cases: int = 300, seed: int = 42) -> str:
    """Generates the synthetic dataset if it doesn't already exist. Idempotent —
    safe to call at the start of every test run."""
    if os.path.exists(DATA_PATH):
        return DATA_PATH

    sys.path.insert(0, os.path.join(REPO_ROOT, "functions", "setu_api", "ml", "data_generation"))
    import generate_dataset  # the real generator, not a duplicate implementation

    random.seed(seed)
    cases = [generate_dataset.generate_case(i) for i in range(1, n_cases + 1)]

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    return DATA_PATH


NETWORK_PATH = os.path.join(REPO_ROOT, "functions", "setu_api", "data", "synthetic_network.json")


def ensure_network_data() -> str:
    """Generates Person/NetworkEdge data if it doesn't already exist. Idempotent."""
    if os.path.exists(NETWORK_PATH):
        return NETWORK_PATH

    data_path = ensure_synthetic_data()
    with open(data_path, encoding="utf-8") as f:
        cases = json.load(f)

    sys.path.insert(0, os.path.join(REPO_ROOT, "functions", "setu_api", "ml", "data_generation"))
    import generate_dataset

    persons, edges, case_person_links = generate_dataset.generate_network(cases)
    with open(NETWORK_PATH, "w", encoding="utf-8") as f:
        json.dump({"persons": persons, "edges": edges, "case_person_links": case_person_links}, f, indent=2)

    return NETWORK_PATH


def ensure_question_set(n_questions: int = 40, seed: int = 7) -> str:
    """Generates the eval question set if it doesn't already exist. Idempotent."""
    question_set_path = os.path.join(REPO_ROOT, "functions", "setu_api", "ml", "eval", "question_set.json")
    if os.path.exists(question_set_path):
        return question_set_path

    data_path = ensure_synthetic_data()
    with open(data_path, encoding="utf-8") as f:
        cases = json.load(f)

    sys.path.insert(0, os.path.join(REPO_ROOT, "functions", "setu_api", "ml", "eval"))
    import generate_question_set as gqs

    questions = gqs.build_question_set(cases, n_questions, seed)
    with open(question_set_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2)

    return question_set_path


# Auto-run for real pytest (conftest.py files execute on collection).
ensure_synthetic_data()
ensure_question_set()
ensure_network_data()
