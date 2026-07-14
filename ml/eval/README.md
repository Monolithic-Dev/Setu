# Eval Harness

Implements the evaluation framework from `docs/AIArchitecture.md` §7 — this is a
**Week 1 deliverable per `docs/SprintPlan.md` Day 6**, not something to leave until submission week.

Needed here (not yet built — this needs real QuickML access to be meaningful, unlike the
ml/data_generation and ml/prediction_model pieces which don't):
- `question_set.json` — held-out test questions with known correct case IDs, covering
  English, Kannada, and code-switched queries per `docs/TestingStrategy.md` §2
- `run_eval.py` — runs the question set against the live system, computes retrieval
  precision@k, bilingual accuracy parity, hallucination rate (via manual review sampling)
- Results should feed directly into `docs/PitchDeck.md` Slide 12 — replace that slide's
  placeholder with real numbers from here, not estimates
