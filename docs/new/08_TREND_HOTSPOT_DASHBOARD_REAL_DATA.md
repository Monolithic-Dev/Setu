# 08_TREND_HOTSPOT_DASHBOARD_REAL_DATA.md — Agent Task: Wire the Dashboard to Real Model Output

**Why this matters:** "Crime trend & hotspot detection" is a named official feature. Earlier notes indicate `Analytics/Dashboard.tsx` was originally backed by a mock `/api/dashboard/stats` endpoint with synthetic charts. Confirm this is now wired to `hotspot_model.py`'s actual output, not still a mock — a judge who asks "is this live or a static mockup" needs a truthful "live" answer.

---

## Task 1 — Audit current wiring

1. Trace `Dashboard.tsx`'s data source end to end. Is it calling a real endpoint backed by `hotspot_model.py`, or still reading a hardcoded/mocked response?
2. Check `alertsFunction/index.py` — does `GET /api/alerts/hotspots` actually call the prediction model, or return static data?

## Task 2 — Wire it for real (if not already)

1. `hotspot_model.py` should run its clustering/frequency analysis (per `AIArchitecture.md` §4: grid-based or density-based clustering of case location+time+MO vectors) against the actual synthetic dataset (`data/synthetic_cases.json` / `synthetic_network.json`), not a separately-hardcoded mock dataset.
2. `alertsFunction` calls this and returns real cluster/hotspot output.
3. `Dashboard.tsx`'s charts (crime trend line, MO pie chart) should read from this real endpoint.
4. Confirm the output still strictly follows FR-5.3: aggregate/geographic/temporal framing only ("cluster of similar break-ins in this zone this month"), never an individual-level score.

## Task 3 — Add the "why" alongside the "what"

Per `JudgeReview.md` §4 and your own explainability pitch, don't just show a hotspot on a map/chart — show its basis: which case/MO features triggered it (shared weapon type, shared MO, time-of-day clustering, etc.), matching what you already built for the network-graph suggested links.

## Acceptance criteria

- `[x]` Killing/changing the underlying dataset visibly changes the dashboard output (proves it's live, not static)
- `[x]` Every hotspot signal shown has a one-line plain-language basis, not just a number/color on a map
- `[x]` No individual-level score anywhere on the dashboard — spot-check against `CodingStandards.md` §6 checklist
- `[x]` `Datathon_Implemented_Features.md` updated to say "live" explicitly, replacing any earlier "mock" language
