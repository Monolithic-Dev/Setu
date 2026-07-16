# RiskRegister.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*Consolidates every risk flagged across Phases 1–4 into one place, rather than leaving them scattered across documents. Likelihood/Impact are qualitative (High/Medium/Low) — this is a 20-day hackathon project, not a context where a numeric risk model adds real precision.*

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Catalyst QuickML Gen-AI early access delayed | Materialized | High | Materialized; fallback (TF-IDF/ZCQL) is the shipped path for this submission | AI/ML |
| R2 | Kannada NLU/voice quality underwhelms | Low–Medium | Medium — undercuts the core differentiator | Bhashini/Sarvam verified via research to handle Kannada + code-switching; dedicated bilingual eval track (`TestingStrategy.md` §2) | AI/ML |
| R3 | Synthetic dataset lacks credibility | Medium | Medium — weak demo, weak benchmark results | Deliberate generation strategy documented in README (`Database.md` §5); reviewed by the whole team before Week 2 | AI/ML |
| R4 | Predictive/"profiling" features drift toward demographic proxies over time | Low (now technically blocked) | High — real harm + judging penalty | Schema-level exclusion (`Database.md` §3) + code-review checklist (`CodingStandards.md` §6) — a structural control, not just a reminder | Backend + AI/ML |
| R5 | Benchmarking a conversational system proves harder than expected | Medium | Medium — weak showing on template slide 12 | Eval plan defined Week 1, not Week 3 (`AIArchitecture.md` §7, `SprintPlan.md` Day 6) | AI/ML |
| R6 | Scope creep across 7+ MVP features in 20 days | Medium | High — nothing finished well | Firm MVP/Stretch/Won't split (`FeaturePrioritization.md`); Day 7 and Day 14 checkpoints explicitly ask "cut something?" | Whole team |
| R7 | Reliability gap between demo and real conditions (Odisha precedent) | Medium | High — exactly the failure mode judges are primed to notice | Dedicated chaos/reliability testing Day 16 (`TestingStrategy.md` §4) | Whole team |
| R8 | Prompt injection against the conversational endpoint | Low–Medium | Medium–High given sensitive data domain | Hardened system prompt, RBAC enforced before retrieval, dedicated security test pass (`Security.md` §3, `TestingStrategy.md` §3) | Backend + AI/ML |
| R9 | Missed or broken submission link/format at deadline | Low if buffer is respected | High — disqualification | Internal 24–25 Jul deadline, explicit pre-submit checklist (`DeploymentStrategy.md` §5) | Whole team |
| R10 | Higher competition on this track (chatbot is the "obvious" AI choice) | Unknown — no visibility into other teams | Medium | Differentiation leans on bilingual + explainability + Catalyst-native depth, not novelty of concept alone (`ProductStrategy.md` §2) | Whole team |
| R11 | QuickML rate limits or early-access constraints tighter than expected | N/A | Medium | N/A-for-this-submission (QuickML was not reached) | AI/ML |
| R12 | Team member availability/illness across 20 days | Low–Medium | Medium | Ownership map (`FolderStructure.md` §2) is documented, not tribal knowledge — anyone can see what any area needs | Whole team |
| R13 | Poor connectivity at rural stations causes silent failures | Medium | Medium–High for real adoptability credibility | Graceful degradation added (NFR-10, `UX.md`) — queued retry + visible state, not silent failure | Frontend |
| R14 | Case-level sensitive data (e.g., minors) exposed via otherwise-valid role access | Low (now technically blocked) | High | `sensitivity_level` field + independent access gate added (`Database.md` §4a, FR-7.3) | Backend |
| R15 | Location acts as an unaddressed demographic proxy in hotspot outputs | Medium (inherent to any location-based model) | Medium–High | Reframed from "solved" to "mitigated + monitored"; outcome-level monitoring added (`MonitoringStrategy.md`) | AI/ML |
| R16 | Catalyst platform outage during the live Grand Finale demo | Low | High — single point of failure outside team control | Pre-recorded fallback run-through rehearsed and ready (`DemoScript.md`) | Whole team |

---

*Phase 5 complete. Next (on your approval): Phase 6 — Submission Preparation (Prototype Brief, Executive Summary, Technical Summary, AI Justification, Innovation Summary, Architecture Explanation, Business & Social Impact, Demo Script, Pitch Deck Outline, GitHub README, Submission Answers) — this is where everything so far gets compressed into what judges will actually read and watch.*
