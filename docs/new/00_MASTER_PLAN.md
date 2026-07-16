# 00_MASTER_PLAN.md — Setu Production-Upgrade Plan

**Context:** Prototype deadline 26 Jul 2026. Current live build (per `Datathon_Implemented_Features.md`) uses regex/heuristic NL parsing, TF-IDF local answer synthesis, Jaccard-similarity network suggestions, and a mocked analytics endpoint — NOT the QuickML/Zia pipeline described in `Architecture.md`/`AIArchitecture.md`. That gap is real and must be closed in the docs even where it can't be closed in code.

This file is the index. Hand each numbered file below to a separate agent/session, in roughly this order. Files are independent enough to parallelize *except* #1, which should go first since it changes what the other agents are allowed to claim in commit messages / READMEs.

---

## Priority order

| # | File | What it does | Blocking? |
|---|---|---|---|
| 1 | `01_DOC_RECONCILIATION.md` | Fixes every doc that overclaims vs. the real build | Do first — low effort, removes the single biggest judge-visible risk |
| 2 | `02_BACKEND_TASKS.md` | Grounding verification, sensitivity-level access gate, real feedback endpoint, RBAC hardening | Independent |
| 3 | `03_FRONTEND_TASKS.md` | Connectivity/offline state, feedback UI, network-graph explainability tooltip | Independent |
| 4 | `04_ML_EVAL_TASKS.md` | Expand and re-run the eval set honestly, especially Kannada | Independent, but do before finalizing Slide 9 numbers |
| 5 | `05_SECURITY_TESTING_TASKS.md` | RBAC boundary tests + prompt-injection probes, with a written report | Independent |
| 6 | `06_IMPLEMENTATION_GAPS_TRACKER.md` | Living gap-tracking doc — update as each item above ships | Ongoing, not a one-time task |

## Ground rules for every agent

1. **Never claim a capability in docs/deck/README that isn't actually in the code.** If something is partially done, say so explicitly (e.g., "grounding verification implemented for structured-search hits; semantic-hit verification is a stretch item").
2. **Every change should be traceable to a requirement ID** from `Requirements.md` (FR-x.x / NFR-x) where one exists. If a change doesn't map to an existing requirement, note that in `06_IMPLEMENTATION_GAPS_TRACKER.md` rather than inventing scope silently.
3. **Don't touch `sensitivity_level`/RBAC/responsible-AI exclusions to make them "more lenient."** These are the load-bearing responsible-AI claims across the whole pitch (`Database.md` §3–4, `AIArchitecture.md` §4, `CodingStandards.md` §6). Any agent touching the Prediction Service or `PERSON`/`CASE_RECORD` schema must run the checklist in `CodingStandards.md` §6 before committing.
4. **Small, reviewed commits.** Conventional Commits format (`feat:`, `fix:`, `docs:`), one reviewer minimum per `CodingStandards.md` §4 — still applies even under deadline pressure, especially for anything touching RBAC/scope code.
5. **Update `Datathon_Implemented_Features.md` the same day** a task from any file below ships — this is your running "what's actually built" source of truth, and it needs to stay accurate for both judges and future-you.

## Definition of done for this whole pass

- [ ] No document in the repo claims QuickML/Zia/Bhashini functionality that isn't actually wired in (or it's clearly labeled "target / refinement-window," not "current")
- [ ] Eval numbers are statistically non-embarrassing (no n=2 language claims) and reported honestly against a stated target
- [ ] `sensitivity_level` gate exists and is demoable
- [ ] Feedback endpoint actually persists flags somewhere reviewable
- [ ] At least one offline/degraded-connectivity state is visible in the UI
- [ ] A written RBAC + prompt-injection test report exists
- [ ] `06_IMPLEMENTATION_GAPS_TRACKER.md` reflects the true current state, not the Phase-6/7 planning state
