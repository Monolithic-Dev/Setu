# 13_FINAL_VERIFICATION_AND_SUBMISSION_READINESS.md — The Last-Mile Checklist

**Use this after `12` is resolved.** Most named features now claim "done" — the remaining work is verification, honest measurement, and rehearsal, not new features. Resist adding anything not on this list; scope creep this close to the deadline is a bigger risk than a missing nice-to-have (`RiskRegister.md` R6).

---

## Step 1 — Deployment reality check (do this today, not last)

- [ ] Confirm a real Zoho Catalyst deployment URL exists and serves the actual app (not `localhost`)
- [ ] Test it from a fresh, logged-out browser session, on a different network if possible
- [ ] Confirm all four roles can log in and get correctly scoped results on the deployed instance, not just in local dev

If this isn't true yet, stop everything else and fix it — no other item on this list matters if the submitted link doesn't work.

## Step 2 — Live-click every "Fully Implemented" claim

Don't trust the compliance doc's checkmarks — walk through each one as if you were a skeptical judge:
- [ ] Context-aware follow-up question — actually type it, don't assume
- [ ] Dashboard hotspot/trend view — confirm it changes when the underlying data changes (proves it's live)
- [ ] Voice input/output — test both directions, in both languages, out loud
- [ ] Network graph explainability tooltip — hover a suggested link, read the explanation aloud, would it make sense to a non-technical officer?
- [ ] PDF export — actually open the exported file, check Kannada renders correctly
- [ ] Sensitivity gate — try to access a restricted case as a role that shouldn't see it, confirm denial

## Step 3 — Run the real scalability stress test (per `10_SCALABILITY_HARDENING.md`)

- [ ] Generate 10x and 50x synthetic corpus
- [ ] Re-run latency benchmark at each scale point
- [ ] Produce the actual chart — replace any "should scale fine" language in the deck with the real number

## Step 4 — Fix the demographic-field issue (per `12`)

- [ ] Confirmed removed and re-tested

## Step 5 — Re-run the full eval suite one final time

- [ ] Confirm hit rate, hallucination rate, latency numbers in the deck match the most recent actual run — not a stale number from an earlier pass
- [ ] Confirm no eval subset has fewer than ~10 questions (per `04_ML_EVAL_TASKS.md`)

## Step 6 — Reconcile every document one last time

- [ ] `PitchDeck.md`, `SubmissionAnswers.md`, README, and `Datathon_Implemented_Features.md` all describe the same stack, the same numbers, the same scope decisions
- [ ] `06_IMPLEMENTATION_GAPS_TRACKER.md` reflects the true final state
- [ ] `11_OFFICIAL_FEATURE_COVERAGE_MATRIX.md` fully updated, no stale ⚠️ rows left unexplained

## Step 7 — Rehearse the demo, cold, in front of someone outside the team

- [ ] Full run-through against the 3-minute constraint (`DemoScript.md`)
- [ ] Confirm the pre-recorded fallback (per `JudgeReview.md` §8 fix) actually exists and plays, in case the live Catalyst link has issues on demo day
- [ ] Whoever presents has read and can deliver `09_RESPONSIBLE_AI_POSITIONING.md`'s prepared answer without notes

## Step 8 — Submission checklist (per `DeploymentStrategy.md` §5 / `SubmissionAnswers.md`)

- [ ] Deployed link loads on a fresh browser
- [ ] GitHub repo public, README verified on a clean machine
- [ ] Demo video public, plays without sign-in
- [ ] Deck PDF from official template, under 5MB
- [ ] Prototype Brief re-counted after any final wording changes
- [ ] Submit with buffer time before the deadline — not in the last hour

---

## If there's still time after all of this (optional, in priority order)

1. Hash-chained audit log (cheap, high judge-visibility)
2. Outcome-side bias monitoring panel (real, not just planned)
3. Thin multi-agent teaser (2 agents, one visible handoff)

Only attempt these once Steps 1–8 are fully green. A working, verified, honestly-presented MVP beats an ambitious but shaky addition every time this close to the deadline.
