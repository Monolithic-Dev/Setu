# 03_FRONTEND_TASKS.md — Agent Task: Frontend UX Gaps

**Scope:** `client/src/` per `FolderStructure.md`. Three tasks, independent of each other.

---

## Task 1 — Connectivity/Degraded-Network State (NFR-10)

**Why:** `JudgeReview.md` §7 flags this as "the most concrete miss" — no offline/low-connectivity handling exists anywhere, despite 1,100+ target stations realistically having patchy connectivity. This is cheap to build and a strong, specific answer if a judge asks about real deployment conditions.

**Implement in:** `client/src/components/ConnectivityBanner/` (new component)

**What it does:**
1. Detects a failed/timed-out request to `/api/query` (or any endpoint).
2. Shows a visible, non-blocking banner: "Unable to reach the server — retrying…" (plain language, not a raw error code, per NFR-8).
3. Queues the in-flight query and retries automatically (simple exponential backoff is enough — 3 attempts is fine for this timeline) rather than silently dropping it.
4. On success, banner dismisses and the queued query completes normally.

**Acceptance criteria:**
- [ ] Manually killing the network mid-query shows the banner, not a hang or blank screen
- [ ] The query the user was waiting on actually completes once connectivity returns, without them re-typing it
- [ ] Full offline mode is explicitly NOT required — don't over-build this

---

## Task 2 — Feedback Control on Answer View (FR-10.1)

**Why:** `UX.md` §2 specs a "was this helpful?" flag on the Answer View. Confirm it's wired to the real backend endpoint from `02_BACKEND_TASKS.md` Task 3, not just a static UI element.

**Implement in:** `client/src/components/Chat/` (extend existing Answer View)

**What it does:**
1. A simple thumbs-up/thumbs-down (or "helpful / not helpful") control next to every answer.
2. On click, calls `POST /api/feedback` with the answer's `audit_id`.
3. Shows a brief confirmation ("Thanks, noted") — doesn't need to be elaborate.

**Acceptance criteria:**
- [ ] Clicking the control actually reaches the backend (check network tab, not just UI state)
- [ ] Control doesn't block or interrupt the chat flow — this needs to be a lightweight, in-conversation action per FR-10.1's own wording

---

## Task 3 — Network Graph Explainability Tooltip

**Why:** `Datathon_Implemented_Features.md` §4 already computes a Jaccard-similarity score for suggested links, but currently surfaces only the confidence number. `JudgeReview.md` §4 specifically flags that a raw similarity score "means nothing to an investigating officer or a court" — you need the plain-language basis, not just the number.

**Implement in:** `client/src/components/NetworkGraph/` (extend existing suggested-link rendering)

**What it does:**
1. On hover/click of a `suggested_link` edge, show: the Jaccard score AND the actual shared associates driving it (e.g., "Suspect A and Suspect B share 3 of 8 known associates: [names or IDs]").
2. If full names aren't appropriate to surface at the requesting role's scope, show count + case IDs instead — respect the same RBAC scoping as everything else.

**Acceptance criteria:**
- [ ] A suggested-link edge shows its basis in one sentence a non-technical officer could read aloud in court
- [ ] Explanation respects role scope (doesn't leak identity of people outside the requester's access)

---

## Optional (only if time allows after 1–3)

- Font/contrast pass for low-light field conditions per `UX.md` §4 — quick visual QA, not a redesign.
- Bilingual symmetry check: confirm the Kannada UI isn't visibly secondary (same layout, same prominence) per `UX.md` §1.
