# 06_IMPLEMENTATION_GAPS_TRACKER.md — Living Document

*Update this the same day anything from `02`–`05` ships, or the same day you discover a new gap. This is the canonical "what's actually true right now" doc — when in doubt, trust this file over any Phase 1–7 planning doc, including `memory.md` until it's updated per `01_DOC_RECONCILIATION.md`.*

---

## How to use this file

One row per requirement or claim that has a gap between plan and reality. Don't delete rows once closed — mark them Done and keep the history; it's useful for the README's transparency section and for answering judge questions about your process.

## Gap Table

| Req/Claim ID | What was planned | What's actually true (as of last update) | Status | Owner | Notes |
|---|---|---|---|---|---|
| AI Core | QuickML LLM Serving + RAG (`AIArchitecture.md`) | TF-IDF local synthesis + regex/heuristic entity extraction | Open / Shipped-as-fallback *(pick one and update)* | AI/ML | Confirm QuickML access status before Week 3 |
| FR-3.3 (grounding) | Prompt-only "answer only from context" | Added explicit verification pass via grounding_verifier.py | Done | AI/ML | See `02_BACKEND_TASKS.md` Task 1 |
| FR-7.3 (sensitivity) | `sensitivity_level` gate on `CASE_RECORD` | Added sensitivity_gate.py enforcing strict allowlist | Done | Backend | See `02_BACKEND_TASKS.md` Task 2 |
| FR-10.1/10.2 (feedback) | `POST /api/feedback` persists flags | Wired UI to endpoint and shows confirmation | Done | Frontend/Backend | See `02_BACKEND_TASKS.md` & `03_FRONTEND_TASKS.md` |
| NFR-10 (offline) | Graceful degradation, queued retry | Built connectivity banner with exponential backoff | Done | Frontend | See `03_FRONTEND_TASKS.md` Task 1 |
| PRD §4 (retrieval precision) | ≥85% precision@5 | 67.7% measured on a 62-question set (proper EN, KN, and KN-EN split), gap acknowledged in PitchDeck | Done | AI/ML | See `04_ML_EVAL_TASKS.md` |
| Security claims | RBAC enforced server-side at Data Store layer | Confirmed structured_search.py and index.py apply role/scope filtering strictly server-side | Done | Backend | See `02_BACKEND_TASKS.md` Task 4 | See `tests/security/rbac_boundary_test_report.md` |
| Explainability (semantic hits) | Plain-language basis for network suggested-links | Tooltip shows plain language Jaccard score and shared associates | Done | Frontend | See `03_FRONTEND_TASKS.md` Task 3 |
| FR-1.2 (context-aware conversations) | Multi-turn reference resolution (e.g. "that case") | Implemented lightweight rule-based coreference context window | Done | Backend | See `07_CONTEXT_AWARE_CONVERSATIONS.md` |
*(Add rows as new gaps surface. Don't let this list only shrink — if something new breaks, log it here immediately rather than letting the deck/README drift out of sync again.)*

---

## Known Limitations to State Honestly (not fix, just disclose)

- Retrieval-at-scale (1,100+ stations' worth of data) is untested — synthetic dataset is demo-sized (`JudgeReview.md` §6).
- Semantic-match explainability is weaker than structured-match explainability even after the Task 3 fix above — a Jaccard-based tooltip is still not a full entailment explanation.
- Location-as-demographic-proxy risk in hotspot outputs is mitigated, not solved (`AIArchitecture.md` §4, `JudgeReview.md` Ethical Concerns) — outcome monitoring is a plan, not yet a running process this early in the build.
- No real pilot impact data exists yet (`ProductStrategy.md` §5) — this is a hackathon prototype, not a validated deployment.

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Completed frontend tasks (NFR-10, FR-10.1, Network Tooltip) | Agent |
| 2026-07-16 | Completed backend tasks (FR-3.3, FR-7.3, Security confirmation) | Agent |
| 2026-07-16 | Completed RBAC & Prompt-Injection testing, verified fallback build, and generated report | Agent |
| 2026-07-16 | Completed ML eval tasks: expanded dataset to 62 queries, benchmarked, updated docs | Agent |
| 2026-07-19 | Implemented rule-based context-aware conversations (FR-1.2) and added multi-turn evals | Agent |

