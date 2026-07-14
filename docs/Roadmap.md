# Roadmap.md

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*High-level milestones only — day-by-day tickets belong to Phase 5's `SprintPlan.md`.*

---

## Sprint to Submission (19 days: 7 Jul – 26 Jul 2026)

### Week 1 (7–13 Jul) — Foundation
- Request Catalyst QuickML Gen-AI (LLM Serving/RAG) early access **immediately** — this is the one dependency that can silently block everything else if left late
- Design and begin generating the synthetic bilingual crime dataset (schema + generation strategy)
- Stand up Catalyst project skeleton: Functions, data store, auth scaffold
- Define the benchmarking/eval plan and test-question set (flagged in Phase 2 as a task that can't be left late)
- Evaluate Bhashini vs. Sarvam AI for Kannada STT/TTS and pick one (or both, for redundancy)

### Week 2 (14–20 Jul) — Core Build
- English conversational query working end-to-end (RAG + source citation)
- Kannada support added and tested for parity, including code-switched input
- Voice integration wired in
- Basic network visualization and basic hotspot/early-warning surfacing built
- RBAC and audit-trail logging implemented (not deferred — these are MVP, not polish)
- PDF export working

### Week 3 (21–26 Jul) — Integration, Proof, Submission
- Full end-to-end demo flow rehearsed against the 3-minute template constraint
- Benchmark report generated with real numbers (retrieval precision, bilingual accuracy, latency, hallucination review)
- Official pptx deck completed, exported to PDF (≤5MB)
- Demo video recorded and uploaded (public Google Drive or unlisted/accessible YouTube)
- GitHub repo finalized: complete source, README, setup instructions
- **Target internal deadline: 24–25 Jul**, leaving a buffer day before the actual 26 Jul, 11:59 PM IST cutoff for link/upload issues — don't plan to submit at the literal deadline

---

## Post-Submission Funnel

| Date | Milestone | What matters |
|---|---|---|
| 19 Aug 2026 | Initial Shortlist Announcement | Judges assess the submitted prototype as-is |
| 19–30 Aug 2026 | Prototype Refinement window | Begin Concept C (multi-agent) upgrades here, not before — see `ProductStrategy.md` §6 |
| 29 Aug 2026 | Induction Session | — |
| Late Aug 2026 | Mentor–Mentee Connects | Use this to pressure-test the refinement direction with outside eyes |
| 9 Sep 2026 | Final Shortlist Announcement | — |
| 26 Sep 2026 | Grand Finale (in-person Demo Day) | Live resilience matters as much as feature count — rehearse for degraded conditions, not just the happy path |

---

## Production Roadmap (beyond the competition)

1. Pilot in 1–2 districts with formal data-governance approval
2. Phased integration with live CCTNS/CAS data
3. Extension to ICJS (courts, prisons, prosecution) for cross-referencing
4. Statewide rollout across all 1,100+ stations
5. Ongoing model monitoring and periodic bias audits, built in from the start rather than added after an incident

---

*Phase 3 complete. Next (on your approval): Phase 4 — System & AI Architecture (`Architecture.md`, `Design.md`, `AIArchitecture.md`, `Database.md`, `APISpec.md`, `Security.md`, `Deployment.md`, `UX.md`), including Mermaid diagrams and the concrete Catalyst service selection referenced throughout Phase 3.*
