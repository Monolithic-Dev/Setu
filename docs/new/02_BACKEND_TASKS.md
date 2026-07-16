# 02_BACKEND_TASKS.md — Agent Task: Backend/Functions Hardening

**Scope:** `functions/` and `ml/` per `FolderStructure.md`. All four tasks are independent; do them in any order, but Task 1 (grounding verification) is the highest-value one for judging.

---

## Task 1 — Grounding Verification Pass (highest priority)

**Why:** `AIArchitecture.md` §1 and `JudgeReview.md` §2 both flag that prompt-only grounding ("answer only from context, say not found otherwise") is a known-leaky control. Right now the local TF-IDF synthesis extracts top-ranked sentences directly from retrieved narratives, which is actually lower-risk than free-generation — but there's no explicit verification step proving that, and no visible artifact showing you thought about it.

**Implement in:** `functions/queryFunction/grounding_verifier.py` (new file)

**What it does:**
1. Takes the generated answer + the source sentence(s)/record(s) it was built from.
2. Runs a lightweight check that each factual claim in the answer is actually present in the cited source — for TF-IDF extraction this can be a straightforward substring/overlap check (the sentence *is* the source, so this should nearly always pass) plus a check that no sentence was pulled from a record outside the retrieved set.
3. If verification fails, return `"not found"` per FR-3.3 rather than showing the answer.
4. Log the verification result into the audit entry (pass/fail + which check), not just the final answer.

**Acceptance criteria:**
- [ ] Every answer returned by `/api/query` carries a verification result in its audit log entry
- [ ] A deliberately broken test case (inject a claim not present in retrieved source text) is caught and returns "not found"
- [ ] One paragraph added to `AIArchitecture.md` §1 or a new `docs/GroundingVerification.md` describing exactly what the check does and its limits (it's a real check, but be honest that substring-overlap is weaker than a full entailment model — say so)

---

## Task 2 — Case-Level Sensitivity Gate (FR-7.3)

**Why:** Planned in `Database.md` §4 / `Requirements.md` FR-7.3 but not confirmed implemented. This is a concrete, demoable responsible-AI feature that directly answers a likely judge question ("what about a case involving a minor?").

**Implement in:** `functions/shared/sensitivity_gate.py` (new), called from `RetrievalSvc` / `NetworkSvc` before returning any `CASE_RECORD`-derived data.

**What it does:**
1. Add `sensitivity_level` column to `CASE_RECORD` in the actual Data Store schema if not already present (check `catalyst_schema.json` — it is NOT currently in the schema file, only mentioned in `Database.md` prose; add it for real).
2. On every read of a `CASE_RECORD` (structured, semantic, or network-graph), check `sensitivity_level`. If `restricted`, require the requesting role to be in an explicit allow-list (start with: SCRB Analyst + System Admin only), independent of station/district scope match.
3. A `restricted` case denied at this gate should return the standard `SCOPE_DENIED` error shape from `APISpec.md` §3, not a generic error.

**Acceptance criteria:**
- [ ] `catalyst_schema.json` updated with the `sensitivity_level` column
- [ ] At least one synthetic `restricted` case exists in the seed data
- [ ] A test confirms a District SP (who would normally have district-scoped read access) is denied on a `restricted` case in their own district
- [ ] Denial is logged distinctly enough to show up in an audit review

---

## Task 3 — Real Feedback Endpoint (FR-10.1/10.2)

**Why:** `APISpec.md` already specs `POST /api/feedback`. Confirm it's not just a UI stub — it needs to actually persist.

**Implement in:** `functions/feedbackFunction/` (new folder, matches `FolderStructure.md` convention) or extend `queryFunction` if a separate function is overkill for the timeline.

**What it does:**
1. Accepts `{ audit_id, was_helpful }`.
2. Writes to a `FEEDBACK_ENTRY` table (add to `catalyst_schema.json`: `feedback_id`, `audit_id`, `was_helpful`, `timestamp_`) — kept separate from `AUDIT_ENTRY` per `APISpec.md`'s own note that flagged entries should be "logged separately... rather than buried in routine audit volume."
3. Returns `{ "status": "recorded" }` per spec.

**Acceptance criteria:**
- [ ] A flagged answer is queryable afterward (even via a simple internal query, doesn't need its own UI beyond what's already planned)
- [ ] Table added to schema, not just assumed
- [ ] `MonitoringStrategy.md`'s "user-flagged answers" signal actually has data to read from

---

## Task 4 — RBAC Enforcement Confirmation

**Why:** Every doc claims RBAC is enforced server-side at the Data Store layer. Confirm this is literally true in the current TF-IDF/regex build, not just true in the Catalyst-native design — the fallback implementation may have taken shortcuts.

**What to check:**
1. Does `structured_search.py` / the ZCQL query layer actually apply a `station_id`/`district_id` filter server-side, or is scoping happening only in the frontend/response-shaping layer? If the latter, fix it — this is the single most consequential shortcut to have accidentally taken.
2. Confirm the four roles (Station Officer, SCRB Analyst, District SP, System Admin) each get genuinely different query results, not just different UI treatment of the same underlying response.

**Acceptance criteria:**
- [ ] A written note (one paragraph, in `06_IMPLEMENTATION_GAPS_TRACKER.md`) confirming which enforcement layer is actually active
- [ ] If scoping was frontend-only, it's moved server-side before submission — this is not optional, it's the core security claim of the whole pitch
