# 04_ML_EVAL_TASKS.md — Agent Task: Fix the Evaluation Set and Report Honestly

**Scope:** `ml/eval/` and `ml/data_generation/`. Do this before finalizing `PitchDeck.md` Slide 9 — the current numbers are not safe to present.

---

## Problem with the current eval (per `PitchDeck.md` Slide 9)

- 42 total questions, but only **2 are Kannada**. A "100% Kannada hit rate" on n=2 is not a credible claim and a technical judge will notice immediately — it just means both got lucky or the two questions were easy.
- Overall 59.5% top-3 hit rate is well below the PRD's own stated target (≥85% precision@5, `PRD.md` §4). This isn't necessarily disqualifying — a well-explained gap reads better than a hidden one — but it needs an honest, specific explanation, not silence.
- No code-switched (mixed Kannada-English) questions are mentioned at all, despite `Requirements.md` FR-1.3 and `AIArchitecture.md` §7 both specifying this as a required eval dimension.

## Task 1 — Expand the eval set

**Target composition** (adjust total count to whatever's feasible in the time left, but keep proportions):
- ≥20 English questions
- ≥20 Kannada questions (not 2 — this is the single most important fix here)
- ≥10 code-switched (mixed Kannada/English mid-sentence) questions per FR-1.3
- Cover a spread of query types: exact-field lookups (should favor structured/ZCQL), natural-language pattern questions (should favor semantic/TF-IDF), and a few genuinely ambiguous ones that should correctly return "not found" rather than a wrong guess

**Where:** `ml/eval/eval_set_en.json`, `ml/eval/eval_set_kn.json`, add `ml/eval/eval_set_codeswitch.json` (new)

## Task 2 — Re-run the benchmark

Run `ml/eval/run_eval.py` (or equivalent) against the expanded set. Record:
- Retrieval precision@k (structured, semantic, and merged)
- Per-language accuracy, and the parity gap between English and Kannada (target: within ~10pp per PRD.md §4 — report the actual gap, don't round it away)
- Code-switch subset accuracy, reported separately
- Hallucination rate: manually review a sample (aim for at least 15–20 answers) against cited sources — did the system ever state something not actually supported? This directly feeds the grounding-verification work in `02_BACKEND_TASKS.md` Task 1.
- Latency (p50/p95)

## Task 3 — Report it honestly

Update `PitchDeck.md` Slide 9 and `AIArchitecture.md` §7 with the real numbers. Required framing:
1. State the number.
2. State the target from `PRD.md` §4.
3. If below target, give the actual reason (e.g., "TF-IDF struggles with paraphrased Kannada queries that don't share surface-level tokens with the narrative text — a known limitation of lexical over semantic-embedding retrieval") rather than a vague "still improving."
4. Note what would close the gap (e.g., "QuickML's semantic Knowledge Base search, once live, should meaningfully close this — see Roadmap").

This is a strength if handled honestly — `JudgeReview.md` already establishes that AI Quality is scored as "unproven until benchmarked," so an actual, honestly-reported benchmark (even an imperfect one) outperforms a vague claim every time.

## Acceptance criteria

- [ ] No eval subset has n<10
- [ ] Code-switch results exist and are reported
- [ ] Slide 9 states target vs. actual, with a reason for any gap
- [ ] Hallucination rate is a real measured number, not omitted
