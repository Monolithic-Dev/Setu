# FeaturePrioritization.md

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## Framework

MoSCoW (Must/Should/Could/Won't) mapped against four delivery buckets. The bucket a feature lands in matters more than the MoSCoW label alone — a "Must" for the Grand Finale isn't necessarily a "Must" for the 26 Jul prototype submission.

---

## MVP — must ship for the 26 Jul prototype submission

| Feature | Req IDs | MoSCoW | Owner (role) |
|---|---|---|---|
| Bilingual text chat (English + Kannada) | FR-1.1–1.4 | Must | AI/ML |
| RAG grounding with source citation | FR-3.1–3.3 | Must | AI/ML |
| Voice input/output (Bhashini/Sarvam) | FR-2.1–2.3 | Must | AI/ML + Frontend |
| Audit trail logging | FR-6.1–6.3 | Must | Backend |
| Role-based access control | FR-7.1–7.2 | Must | Backend |
| PDF export | FR-8.1 | Must | Backend |
| Basic network visualization | FR-4.1–4.2 | Must | Frontend |
| Basic hotspot/early-warning surfacing | FR-5.1–5.3 | Must | AI/ML |
| Synthetic bilingual dataset | FR-9.1–9.2 | Must | AI/ML + Backend |
| Benchmark/eval report | supports slide 12 | Must | AI/ML |
| Catalyst deployment + named services (slide 9) | — | Must | Backend/DevOps |

## Demo Features — polish for how the MVP is *presented*, not new capability

| Feature | Rationale |
|---|---|
| Guided demo script hitting all MVP capabilities in ≤3 minutes | Required by template slide 13 |
| Clean, jargon-free UI copy | Supports NFR-8 (accessibility) and judge impression |
| Pre-loaded example queries showcasing English, Kannada, voice, network graph, and an early-warning signal | Maximizes visible breadth within the time limit |

## Stretch Goals — build only if MVP is solid ahead of schedule, otherwise defer to the Aug refinement window

| Feature | Notes |
|---|---|
| Multi-agent orchestration (Concept C: retrieval / network-analysis / pattern-detection / explanation sub-agents) | Reserved explicitly as the refinement-window growth story (`ProductStrategy.md` §6) |
| Deeper predictive modeling (e.g., graph-based co-offending analysis) | Meaningful uplift, but higher risk to bolt on late |
| Expanded synthetic dataset realism/scale | Improves demo credibility but not required to prove the concept |
| Estimated implementation cost slide (template slide 10, optional) | Nice-to-have, not scored as heavily as the required slides |

## Production Roadmap — beyond this competition entirely

| Feature | Notes |
|---|---|
| Live CCTNS/CAS data integration | Requires formal data-governance approval |
| ICJS integration (courts, prisons, prosecution) | Long-term, mirrors CCTNS's own stated goals |
| Formal security certification/audit | Prerequisite for any real deployment |
| Statewide rollout across all 1,100+ stations | Final destination of the adoption path in `ProductStrategy.md` §5 |
| Ongoing model monitoring & periodic bias audits | Directly answers the Odisha-style reliability gap |

---

## Explicit "Won't" (this submission)

- Public/citizen-facing interface
- Cross-state data sharing
- Any individual-level predictive risk score tied to a named person (permanently out of scope on responsible-AI grounds, not just a time-boxing decision — see `HackathonAnalysis.md` §9)

---

*Next: `Roadmap.md`.*
