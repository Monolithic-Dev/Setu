# 01_DOC_RECONCILIATION.md — Agent Task: Fix Doc/Reality Mismatches

**Goal:** Every document a judge might read (deck, brief, README, risk register) should describe the system that actually exists, not the one that was planned. This is a documentation-only task — no code changes.

**Do not delete the aspirational architecture.** Keep it, but clearly labeled as target/refinement-window, separate from what's shipped now.

---

## Task 1 — `PitchDeck.md`

**Slide 7 (Architecture Diagram):** Currently already shows the real stack (Python Core Engine, TF-IDF + ZCQL, no QuickML) — leave as is, but add one line making the QuickML upgrade path explicit: *"Interface designed so QuickML LLM Serving can replace the local synthesis step directly, once Gen-AI early access is confirmed — see Roadmap."*

**Slide 8 (Technologies Used):** Currently correctly says "TF-IDF + BM25," which conflicts with `TechStack.md` and `Architecture.md` elsewhere in the repo. Action:
- Keep Slide 8 as the source of truth for "what's live now."
- Add a one-line "Why classical retrieval for the prototype" justification so it doesn't read as a downgrade: e.g., *"We prioritized a fully working, benchmarked pipeline over a dependency on early-access Gen-AI infrastructure that could block the whole demo if access was delayed — see RiskRegister R1."*

**Slide 9 (AI Evaluation Metrics):** Do not finalize this slide until `04_ML_EVAL_TASKS.md` is complete. Current numbers (59.5% hit rate on 42 questions, Kannada n=2) are not safe to present as-is:
- Replace "100% Kannada Hit Rate (2/2)" with the expanded, re-run number once available. n=2 is not a credible claim — a judge will notice immediately.
- Add one honest line comparing the result to your own stated target: *"Target (PRD.md): ≥85% precision@5. Current: [X]%. Gap primarily attributable to [reason] — tracked in ImplementationGaps.md."* Do not silently omit the comparison; stating a miss honestly reads better than an unexplained shortfall a judge finds themselves.

## Task 2 — `SubmissionAnswers.md`

Rewrite the Prototype Brief (currently 885/1024 chars, describes QuickML LLM Serving + Bhashini/Sarvam as live) to match the real stack:
- Replace "QuickML's LLM Serving and RAG power the conversational core" with an accurate description of the hybrid ZCQL + TF-IDF retrieval-and-synthesis approach actually shipped.
- Keep the Bhashini/Sarvam voice claim ONLY if voice I/O is actually wired and working end to end — confirm with whoever owns `functions/voiceTranscribeFunction/` and `voiceSynthesizeFunction/` before leaving this in. If voice is stubbed/partial, say "voice input supported for [English/Kannada/both]" precisely, not more than what's true.
- Re-count characters after editing; do not assume the 1024 limit still holds.

## Task 3 — `RiskRegister.md`

Close out R1 and R11 with the actual outcome instead of leaving them "open/mitigated-in-theory":
- **R1** (QuickML early access delayed): change status to reflect what happened — either "materialized; fallback (TF-IDF) is the shipped path for this submission" or "resolved; QuickML now live" — whichever is true.
- **R11** (QuickML rate limits): same — mark N/A-for-this-submission if QuickML was never reached, rather than leaving it as an open unknown.

## Task 4 — `memory.md`

Update the Status section — it currently states "nothing has been built yet... Phase 8 is implementation" which is now false. Replace with an accurate current-state summary: what's built (per `Datathon_Implemented_Features.md`), what's still planned, and link to `06_IMPLEMENTATION_GAPS_TRACKER.md` as the canonical up-to-date source going forward instead of re-deriving status from Phase 1–7 docs alone.

## Task 5 — README (repo root)

Confirm the README's architecture/stack description matches Slide 7/8 of the corrected deck, not `Architecture.md`/`TechStack.md`'s original QuickML-centric version. A judge reading the repo cold should get the same story the deck tells.

## Task 6 — `Architecture.md`, `AIArchitecture.md`, `Design.md`, `TechStack.md` (light touch only)

Do not rewrite these wholesale — they're legitimate design targets and show real engineering thought. Just add a one-line callout near the top of each: *"Note: this document describes the target architecture. See `Datathon_Implemented_Features.md` and `06_IMPLEMENTATION_GAPS_TRACKER.md` for what's implemented in the current submission."*

---

## Acceptance check

Read `PitchDeck.md`, `SubmissionAnswers.md`, and the README back to back. If they'd leave a judge with three different impressions of what the AI core actually is, this task isn't done yet.
