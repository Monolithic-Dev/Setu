# memory.md — KSP Datathon 2026 Project Memory

*Consult this file before generating any new artifact. Update it at the end of every phase.*

## Project
KSP Datathon 2026 (Karnataka State Police × Hack2Skill × Zoho Catalyst). Prototype submission deadline: **26 Jul 2026, 11:59 PM IST** (a Sunday).

## Status
- Phases 1–6 — complete (see each doc's own header)
- Phase 7 (Judge Review) — complete → `JudgeReview.md`, plus targeted edits to 8 existing documents (see below)
- Awaiting user approval before Phase 8 (Implementation) — the last checkpoint before code gets written

## Key Facts (reference, don't re-derive)
- Team: 4–5 people, dedicated AI/ML + frontend + backend roles
- Challenge locked: Challenge 1 — Conversational AI for KSP Crime Database
- Product concept: "Investigative Co-Pilot" (Concept B), working name **"Setu"** (placeholder)
- Prototype Brief finalized: 885/1024 characters (`SubmissionAnswers.md`)
- Full submission package ready: `PitchDeck.md` (16 slides), `DemoScript.md` (timed 3:00), `SubmissionAnswers.md`, `README.md`
- Stack: React+TypeScript / Python 3.10+ Catalyst Functions / Catalyst QuickML (LLM Serving+RAG+KB) / scikit-learn+Zia AutoML for prediction / Bhashini+Sarvam for Kannada speech / Data Store+ZCQL+OLAP / D3.js
- 20-day build (7–26 Jul 2026), internal deadline 24–25 Jul; day-by-day plan in `SprintPlan.md`

## Phase 7 Findings & Fixes (this is now the current state — don't re-derive from earlier phase docs alone)
Genuine gaps found and fixed directly in the existing docs, not just logged:
1. **No offline/low-connectivity handling** → NFR-10 added (`Requirements.md`), connectivity state added (`UX.md`)
2. **No case-level sensitivity beyond role-based RBAC** → `sensitivity_level` field + independent access gate added (`Database.md` §4a, FR-7.3)
3. **RAG grounding relied only on prompting, not verification** → explicit grounding-verification step added to the pipeline (`AIArchitecture.md` §1)
4. **Responsible-AI framing was overconfident** ("solved" via schema exclusion) → corrected to "strongly mitigated, requires ongoing outcome monitoring" since location can itself be a demographic proxy (`HackathonAnalysis.md` §9, `AIArchitecture.md` §4, `MonitoringStrategy.md`)
5. **No user feedback mechanism** → FA10/FR-10.1/FR-10.2 added (`Requirements.md`), feedback control added (`UX.md`)
6. **No live-demo platform-outage contingency** → pre-recorded fallback plan added (`DemoScript.md`)
7. **No real-world pilot impact-measurement plan** (only technical benchmarks existed) → added (`ProductStrategy.md` §5)
8. **RiskRegister** updated with R13–R16 capturing all of the above as the canonical tracked list

Findings surfaced but *not* fixed (deliberately, explained in `JudgeReview.md`): demo breadth-vs-depth tension in the 3-minute video (rehearsal-dependent, not a document fix); Slide 8 communication risk (presenter preparation, not a content gap); retrieval-at-scale stress testing (needs the real system built first — Phase 8 item).

## Decisions & Assumptions
(carried forward from Phases 1–6, all still current — see `HackathonAnalysis.md` through `SubmissionAnswers.md` for full detail)

## Open Questions
- Team name and leader name — still needed for deck Slide 1, README, SubmissionAnswers.
- License choice for the GitHub repo (MIT suggested).
- Whether Catalyst QuickML Gen-AI early access has been requested/granted.
- Final product name ("Setu" is a placeholder).

## Completed Documents
All Phase 1–6 documents, plus:
- [x] JudgeReview.md
- [x] Targeted Phase 7 edits to: Requirements.md, Database.md, AIArchitecture.md, UX.md, MonitoringStrategy.md, DemoScript.md, ProductStrategy.md, HackathonAnalysis.md, RiskRegister.md

## Next Up — Phase 8: Implementation (on approval)
Only begins once the user approves the plan overall. Every implementation decision must follow PRD, Architecture, AI Design, UX, Security Design, Coding Standards, and Folder Structure exactly as now finalized (including Phase 7's fixes) — this is the point where 20 days of calendar time actually starts running out, so approval here should mean "build this," not "one more review pass."
