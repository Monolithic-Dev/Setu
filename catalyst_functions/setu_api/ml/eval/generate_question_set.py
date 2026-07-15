"""
Generates a held-out question set from the synthetic dataset, with known
correct case_id(s) per question — implements the "held-out synthetic test
set" described in docs/AIArchitecture.md §7.

Each question is built directly from a real case's own fields, so the
correct answer is unambiguous by construction: if the pipeline can't
retrieve the case whose modus operandi and district the question literally
names, that's a genuine retrieval failure, not an artifact of a hand-
written question not matching the generator's phrasing.
"""

import argparse
import json
import random


def build_question_set(cases: list[dict], n_questions: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    sample = rng.sample(cases, min(n_questions, len(cases)))

    questions = []
    for case in sample:
        mo_words = " ".join(case["modus_operandi"].split()[:3])
        questions.append({
            "question_id": f"eval-{case['case_id']}",
            "query_text": f"{mo_words} {case['location']['district']}",
            "language": "en",
            "expected_case_ids": [case["case_id"]],
            "notes": f"Built from {case['case_id']}'s own MO and district — should be directly retrievable.",
        })
    return questions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="../data/synthetic_cases.json")
    parser.add_argument("--n-questions", type=int, default=40)
    parser.add_argument("--seed", type=int, default=7)  # different seed than data generation on purpose
    parser.add_argument("--out", default="question_set.json")
    args = parser.parse_args()

    with open(args.data, encoding="utf-8") as f:
        cases = json.load(f)

    questions = build_question_set(cases, args.n_questions, args.seed)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2)

    print(f"Generated {len(questions)} eval questions -> {args.out}")


if __name__ == "__main__":
    main()
