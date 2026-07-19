# 07_CONTEXT_AWARE_CONVERSATIONS.md — Agent Task: Multi-Turn Context (FR-1.2)

**Why this matters:** "Context-aware conversations" is a named bullet in the official Challenge feature list, and `Requirements.md` FR-1.2 / `UserStories.md` US-1.2 both specify it explicitly: *"show me his known associates" following a prior answer about a specific case should resolve correctly without re-stating the case.* The handoff doc doesn't confirm this is actually working — verify first, then fix if it isn't.

---

## Task 1 — Verify current behavior

Test manually:
1. Ask: "Show me recent chain snatching cases in Mysuru."
2. Follow up: "Who are the known associates of the main suspect in that case?"
3. Confirm the second query correctly resolves "that case" / "the main suspect" using the first turn's result, without requiring the case ID to be repeated.

If this already works — document it (screenshot or transcript) in `Datathon_Implemented_Features.md` and stop here. If it doesn't, proceed to Task 2.

## Task 2 — Implement session context (if missing)

**Where:** `catalyst_functions/setu_api/shared/` (new: `conversation_context.py`), used by `queryFunction`.

**Approach (kept simple for the timeline):**
1. Each `session_id` maps to a small rolling context object: last N (start with 3) turns — the user's query, the entities/case IDs resolved, and the answer summary.
2. On a new query, run a lightweight coreference resolution pass before retrieval: check for pronouns/anaphora ("he," "that case," "the suspect," "ಆ ಕೇಸ್") and substitute the most recently referenced entity/case ID from context.
3. This does not need to be a general NLP coreference model — a rule-based check against the last 1–2 referenced entities is enough for this timeline and is honestly describable as such.
4. Store context in Catalyst Cache (per `Architecture.md`'s intended mapping) or `local_audit_store.py`'s pattern if Cache isn't wired yet — but note in `06_IMPLEMENTATION_GAPS_TRACKER.md` which one is actually in use.

## Task 3 — Test and document

- [ ] Re-run the Task 1 test case — confirm it now resolves correctly
- [ ] Add at least 3 multi-turn test cases to `ml/eval/` (one English, one Kannada, one code-switched) so this is measured, not just demoed once
- [ ] Update `Datathon_Implemented_Features.md` with what was actually built (rule-based reference resolution vs. a fuller model — be precise)

## Acceptance criteria

- [ ] A follow-up query using a pronoun/reference correctly resolves against the prior turn, in both English and Kannada
- [ ] Context window is bounded (doesn't grow unbounded per session — cap it, note the cap)
- [ ] This is demoable live, since `DemoScript.md` doesn't currently show a follow-up-question beat — consider adding one if this ships cleanly
