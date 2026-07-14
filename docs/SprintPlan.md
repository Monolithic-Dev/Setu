# SprintPlan.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*20-day build, 7 Jul – 26 Jul 2026. Three tracks run in parallel (AI/ML, Backend, Frontend), syncing at the checkpoints marked below. Detailed day-by-day for Week 1 (where dependency delays are most costly if caught late), grouped for Weeks 2–3.*

---

## Week 1 — Foundation (7–13 Jul)

| Day | Date | AI/ML | Backend | Frontend |
|---|---|---|---|---|
| 1 | Tue 7 Jul | **Whole team: request Catalyst QuickML Gen-AI early access now** — this blocks everything downstream if delayed | Repo + Catalyst project scaffold per `FolderStructure.md` | Repo + React/TS scaffold |
| 2 | Wed 8 Jul | Design synthetic dataset schema; start generation script | Create Data Store tables per `Database.md` ER diagram; configure table-level RBAC scopes | i18n (EN/KN) setup |
| 3 | Thu 9 Jul | Continue dataset generation; evaluate Bhashini vs. Sarvam for Kannada STT/TTS | Catalyst Authentication integration; Function scaffolding | Chat UI shell (no backend wiring yet) |
| 4 | Fri 10 Jul | Finalize synthetic dataset v1; begin QuickML Knowledge Base ingestion (once access is live) | ZCQL structured-search query layer | Voice capture UI component |
| 5 | Sat 11 Jul | First end-to-end RAG query test, English only | Audit logging table + service (append-only, per `Security.md` §3) | Network graph library integration (empty state) |
| 6 | Sun 12 Jul | Define the benchmark/eval question set (`AIArchitecture.md` §7) — this is due now, not later | Buffer / catch-up | Buffer / catch-up |
| 7 | Mon 13 Jul | **Checkpoint**: internal demo of a working English RAG query, end to end. If QuickML access is still pending, fall back temporarily to an external LLM API so the rest of the build isn't blocked, and migrate once access lands. | | |

---

## Week 2 — Core Build (14–20 Jul)

| Days | Focus | AI/ML | Backend | Frontend |
|---|---|---|---|---|
| 8–9 | Bilingual + RBAC | Kannada support + prompt tuning; test code-switched input | RBAC enforcement testing across all four roles (deliberately try to breach scope and confirm denial) | Wire chat UI to `/api/query`; source-citation display |
| 10–11 | Network + Prediction | Hotspot/prediction model v1 (clustering over OLAP); begin eval harness runs | Network Function (entities/edges from Zia NER output); Export Function (PDF) | Network graph wired to real data; alerts panel UI |
| 12 | **Integration day** | Full flow test together: voice input (Kannada) → answer → network graph → export, run by the whole team, not one person's laptop | | |
| 13 | Buffer | Fix whatever integration day surfaced | | |
| 14 | **Checkpoint** | Internal demo rehearsal v1; get an outside pair of eyes (mentor, or anyone not on the team) to try it cold | | |

---

## Week 3 — Proof, Polish, Submission (21–26 Jul)

| Day | Date | Focus |
|---|---|---|
| 15 | Tue 21 Jul | Run the full benchmark suite (retrieval precision, bilingual parity, latency, hallucination review) — produces the numbers for template slide 12 |
| 16 | Wed 22 Jul | Reliability/chaos testing: deliberately break a dependency (simulate a Bhashini timeout, a QuickML slowdown) and confirm the fallback paths actually work — this is the Odisha lesson, applied |
| 17 | Thu 23 Jul | Build the official 16-slide deck; draft and edit the Prototype Brief down to ≤1024 characters |
| 18 | Fri 24 Jul | Record the demo video (target ≤3 minutes, per template slide 13); finalize the GitHub README | **Internal target deadline — aim to be submission-ready today** |
| 19 | Sat 25 Jul | Buffer day: fix anything the recording/rehearsal exposed; verify every link (GitHub, deployed, video, deck) works from a fresh browser session |
| 20 | Sun 26 Jul | Final checks only. Submit well before 11:59 PM IST — not in the last hour |

---

## Sync Cadence

- Daily 15-minute standup (async is fine given a small team, but don't skip it — this is exactly the kind of project where "I assumed you were handling that" costs a day)
- Checkpoints on Day 7 and Day 14 are the two points where the team should honestly ask "are we still on track for the MVP in `FeaturePrioritization.md`, or do we need to cut something" — better to cut a Stretch Goal on Day 14 than discover the gap on Day 24.

---

*Next: `TestingStrategy.md`, `DeploymentStrategy.md`, `MonitoringStrategy.md`, `RiskRegister.md`.*
