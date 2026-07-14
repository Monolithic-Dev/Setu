# ProductDiscovery.md — Product Discovery

**Phase 2 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Concept Brainstorm

### Concept A — "Query Assistant"
A focused NL chatbot over crime records: bilingual (English/Kannada), RAG-grounded, with an audit trail and PDF export. Answers questions, cites its sources. No proactive behavior, no multi-agent orchestration.
- **Strengths**: lowest build risk, directly satisfies the core ask, easiest to benchmark and explain.
- **Weaknesses**: doesn't touch "predictive analytics & early warnings" or "criminal network visualization" from the official feature list — leaves two named requirements unaddressed.

### Concept B — "Investigative Co-Pilot"
Everything in Concept A, plus: criminal network visualization generated from query results, proactive hotspot/early-warning surfacing (not just reactive Q&A), and a visible reasoning trail per answer.
- **Strengths**: covers the full official feature list; still a single coherent system rather than a distributed one, so it's buildable by a 4–5 person team in 20 days with clear ownership splits (AI/ML on RAG + prediction models, backend on data/RBAC/audit, frontend on chat + voice + graph view).
- **Weaknesses**: more integration surface than Concept A; needs disciplined scope control.

### Concept C — "Multi-Agent Command Assistant"
A supervisor agent orchestrating specialized sub-agents: a retrieval agent, a network-analysis agent, a pattern-detection agent, and an explanation agent, each independently reasoning and handing off to the next.
- **Strengths**: the most architecturally sophisticated, closest to genuine "agentic AI," strong differentiation ceiling.
- **Weaknesses**: highest complexity and failure surface for a 20-day build; multi-agent handoff reliability is exactly the kind of thing that looks great in architecture diagrams and breaks in live demos — echoes the Odisha cautionary lesson (CompetitorAnalysis.md §5) about impressive-on-paper systems failing operationally.

---

## 2. Evaluation

| Criterion | A: Query Assistant | B: Investigative Co-Pilot | C: Multi-Agent Command Assistant |
|---|---|---|---|
| Covers official feature list | Partial | Full | Full |
| Feasible in 20 days, 4–5 people | High confidence | Good confidence with discipline | Low confidence |
| Demo strength | Solid, a bit plain | Strong — visual + conversational + proactive | Highest ceiling, highest variance |
| Benchmarking ease (template slide 12) | Easy | Moderate — needs a deliberate eval plan | Hard — has to benchmark orchestration reliability too |
| Room to grow into the Aug refinement window | Limited | Good | Already "maximal" — less headroom |
| Catalyst-native fit | Good | Good | Good, but adds unnecessary orchestration risk on top |

---

## 3. Recommendation

**Build Concept B — "Investigative Co-Pilot" — for the prototype submission**, with **Concept C's multi-agent structure explicitly reserved as the refinement-window upgrade path** between the 19 Aug shortlist and the 26 Sep Grand Finale.

This does two things at once: it keeps the 20-day build inside what a well-staffed team can realistically deliver *and* benchmark credibly, and it gives us a genuine, visible growth story to show mentors and judges between shortlist and finale ("here's what we shipped for the prototype round, here's how it's evolved into a fully agentic system for the finale") — which HackathonAnalysis.md §8 already flagged as a real scoring advantage in a two-stage funnel.

**One-line articulation for the Prototype Brief**: *A bilingual (Kannada + English), voice-enabled conversational assistant that lets any investigator query Karnataka's crime records in plain language, surfaces criminal-network links and early crime-pattern warnings automatically, and shows its reasoning and sources for every answer — built natively on Zoho Catalyst's Gen-AI stack.*

---

## 4. Scope Preview (full MVP/stretch boundary owned by Phase 3)

Rough split, to be finalized in `PRD.md` / `FeaturePrioritization.md`:
- **In for prototype submission**: bilingual chat (text + voice), RAG over a synthetic Karnataka crime dataset, source-cited answers, basic network visualization, basic hotspot/early-warning surfacing, RBAC, audit trail, PDF export.
- **Likely refinement-window additions**: deeper multi-agent orchestration (Concept C elements), richer predictive modeling, expanded synthetic dataset realism, more sophisticated benchmarking.
- **Likely production-only (not this submission)**: integration with live CCTNS/CAS data, integration with ICJS (courts/prisons/prosecution), formal security audit/certification.

---

*Next (on your approval): Phase 3 — Product Definition (`PRD.md`, `ProductStrategy.md`, `Requirements.md`, `UserStories.md`, `FeaturePrioritization.md`, `Roadmap.md`), which will formalize the MVP/stretch/production split above.*
