# PRD.md — Product Requirements Document

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Product Overview

**Working name: "Setu"** (Sanskrit/pan-Indian for "bridge" — bridging investigators and fragmented crime records; also a natural loanword in Kannada). This is a placeholder, not a final decision — swap freely, and if you keep any Kannada-language branding, get it checked by a native speaker before it goes on the deck or demo video. Naming isn't something I'll guess-verify with confidence.

**One-liner:** A bilingual (Kannada + English), voice-enabled conversational assistant that lets any Karnataka Police investigator query crime records in plain language, surfaces criminal-network links and early crime-pattern warnings automatically, and shows its reasoning and sources for every answer — built natively on Zoho Catalyst's Gen-AI stack.

**Vision (beyond this submission):** the analysis layer CCTNS was designed to eventually have in 2009 but never got — a single, explainable, statewide interface between 1,100+ stations' worth of siloed records and the officer who needs an answer right now.

---

## 2. Problem Statement

SCRB manages a large, continuously expanding repository of crime data from 1,100+ police stations across Karnataka. Current tooling is static dashboards and manual queries — no deep analysis, no real-time insight, and (per `Research.md` §1) a persistent language and self-service gap that likely suppresses use of the digital tools that already exist.

---

## 3. Target Users

Full personas in `Research.md` §4. Summary:
- **Investigating Sub-Inspector** (primary) — station-level, Kannada-first, needs fast answers usable mid-investigation
- **SCRB Data Analyst** (primary) — state HQ, today's human query bottleneck, wants self-service to reduce ticket load
- **District Superintendent of Police** (secondary) — wants pattern/hotspot summaries across their district

---

## 4. Goals & Success Metrics

| Goal | Metric (prototype-submission stage) |
|---|---|
| Answer investigator questions accurately | ≥85% retrieval precision@5 on a held-out synthetic test set; manually reviewed hallucination rate on a 50-question eval set |
| Work equally well in Kannada and English | Bilingual accuracy parity within ~10pp on the same eval set, tested with mixed-language (code-switched) input |
| Be fast enough to use mid-investigation | Median response latency target set and measured (exact number depends on Catalyst QuickML benchmarks — confirm in Phase 4) |
| Be explainable enough to trust | 100% of answers carry a visible source/reasoning trail; zero silent/unexplained outputs |
| Be demo-ready | Full flow (text + voice, both languages, one network-viz example, one early-warning example) fits inside the template's 3-minute video |

Longer-term (post-hackathon) success metrics belong in `ProductStrategy.md` §4.

---

## 5. Scope Summary

Full detail and rationale in `FeaturePrioritization.md`. Headline split:

- **MVP (must ship for 26 Jul submission):** bilingual text+voice chat, RAG over a synthetic Karnataka crime dataset, source-cited answers, RBAC, audit trail, PDF export, basic network visualization, basic hotspot surfacing.
- **Demo Features (present at Grand Finale, may be lighter-weight in the prototype round):** the full "Investigative Co-Pilot" experience end-to-end, benchmarked and narrated.
- **Stretch Goals (build if time allows, or target for the Aug refinement window):** deeper multi-agent orchestration (Concept C), richer predictive modeling, expanded dataset realism.
- **Production Roadmap (beyond this competition):** live CCTNS/CAS integration, ICJS integration, formal security certification, statewide rollout.

---

## 6. Functional Requirements (Summary)

Full numbered requirements in `Requirements.md`. Major capability areas:
1. Conversational query (bilingual, multi-turn, context-aware)
2. Voice interaction (speech-to-text / text-to-speech, both languages)
3. Retrieval-augmented answering grounded in crime records
4. Criminal network visualization
5. Predictive analytics & early-warning surfacing
6. Explainable AI with audit trails
7. Role-based secure access
8. PDF export of conversation history

---

## 7. Non-Functional Requirements

- **Security & privacy:** role-scoped data access; no PII beyond what a given role is entitled to see; encrypted at rest and in transit
- **Explainability:** every output traceable to source records and reasoning steps — not optional polish, see `HackathonAnalysis.md` §6.2
- **Responsible AI:** pattern/"profiling" outputs grounded in case/MO-level evidence only, never demographic or socio-economic identity proxies — see `HackathonAnalysis.md` §9 and `Research.md` (predictive-policing bias precedent)
- **Bilingual parity:** Kannada is a first-class language, not an afterthought translation layer
- **Reliability:** given the Odisha AI Command Centre precedent (`CompetitorAnalysis.md` §5), the system must be tested under realistic failure conditions, not just demo-path conditions
- **Performance:** conversational latency low enough to be usable mid-investigation (specific target set in Phase 4 once Catalyst QuickML benchmarks are known)
- **Auditability/observability:** every query, retrieval, and answer logged for later review

---

## 8. Assumptions & Dependencies

- Real SCRB crime data will not be released; a credible synthetic bilingual dataset must be built (Phase 4 workstream)
- Catalyst QuickML's Gen-AI features (LLM Serving, RAG, Knowledge Base) are early-access — assumes the team has requested or will immediately request access
- Kannada speech handled via Bhashini (free tier = proof-of-concept only) and/or Sarvam AI — assumes at least one is accessible and usable within the 20-day window
- Team maintains its current 4–5 person, role-specialized composition

---

## 9. Constraints (recap)

Deployment exclusively on Zoho Catalyst; submission deck must use the official 16-slide template; Prototype Brief ≤1024 characters; demo video ≈3 minutes; GitHub repo public with README + setup instructions. Full detail in `HackathonAnalysis.md` §5.

---

## 10. Out of Scope (this submission)

- Live integration with real CCTNS/CAS or ICJS data
- Formal security certification/audit
- Multi-state or cross-jurisdiction data sharing
- Public/citizen-facing interface (this is investigator-facing only)
- Full multi-agent orchestration (Concept C) — reserved for the refinement window

---

## 11. Risks (recap, full detail in HackathonAnalysis.md §9–10 and Research.md)

- Predictive-policing bias if "profiling"/"risk" features aren't deliberately scoped to case-level evidence
- Synthetic dataset credibility
- Gen-AI early-access approval delay
- Benchmarking a conversational system is a harder measurement problem than classical ML — must be planned as a Week 1 task, not left late

---

*Next: `ProductStrategy.md`, `Requirements.md`, `UserStories.md`, `FeaturePrioritization.md`, `Roadmap.md`.*
