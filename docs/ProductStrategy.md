# ProductStrategy.md

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Positioning Statement

For **investigating officers and analysts across Karnataka's 1,100+ police stations**, who today wait days for cross-referenced answers from a single overloaded SCRB query desk, **Setu** is a **bilingual conversational AI assistant** that answers crime-data questions in seconds, in the officer's own language, with a visible audit trail — unlike static CCTNS dashboards or manual report requests, **Setu turns fifteen years of digitized-but-unanalyzed records into something an officer can actually talk to.**

---

## 2. Differentiation Pillars

From `CompetitorAnalysis.md`:
1. **Bilingual by design** — Kannada is a first-class language, not a translation bolt-on. No reviewed competitor (Indian or international) does this for Kannada specifically.
2. **Investigator-facing, not citizen-facing** — unlike Singapore's public chatbot, this serves the person doing the actual case work.
3. **Audit-trail-grade explainability** — built in from the MVP, not retrofitted; this is what makes an AI answer usable in a case file rather than just interesting to look at.
4. **Native on this year's tech partner's own AI stack** — Catalyst QuickML's new RAG/LLM Serving, not a bolted-on external API, which is both a technical and a judging-alignment advantage (`HackathonAnalysis.md` §6.3).
5. **Honest positioning** — we do not claim to be the first AI assistant in Indian policing (MahaCrimeOS and West Bengal's bot already exist); we claim the specific, true, defensible combination nobody else has assembled.

---

## 3. Why Now

Two independent timing arguments converge:
- **The institutional argument:** CCTNS's own 2009 design goals already called for pattern-analysis capability across crime data; the tooling to actually deliver that (LLMs + RAG) simply didn't exist until recently. This isn't a new problem being invented for a hackathon — it's a fifteen-year-old unmet mandate.
- **The platform argument:** Zoho Catalyst has just shipped no-code LLM Serving and RAG, and is actively promoting it around this exact event. Building on it now, while it's new and being showcased, is a materially different pitch than building on it in a year when every team does.

---

## 4. Success Criteria Across the Funnel

This is a two-stage competition, and the bar is different at each stage — worth designing to both, not just the first:

| Stage | What actually needs to be true |
|---|---|
| Prototype submission (26 Jul) | Working end-to-end demo of the MVP feature set, deployed on Catalyst, benchmarked, deck complete, video ≤3 min |
| Initial shortlist (19 Aug) | Judges believe the concept, trust the team, and see a credible path to more |
| Refinement window (19–30 Aug) | Visible, real progress since the prototype — this is where Concept C elements (deeper agentic behavior) start appearing |
| Grand Finale (26 Sep) | A live, resilient demo in front of government stakeholders who are evaluating adoptability as much as novelty (`HackathonAnalysis.md` §6.1) |

---

## 5. Adoption Path Beyond the Hackathon

Judges are explicitly told to look for solutions "that can potentially be adopted by law enforcement agencies" — so a credible adoption story is itself part of the pitch, not just a nice-to-have slide:

1. **Pilot** in one or two districts with proper data-governance sign-off, running alongside (not replacing) existing SCRB workflows
2. **Phased integration** with live CCTNS/CAS data once security review is complete
3. **Extension to ICJS** (courts, prisons, prosecution) for cross-referencing, mirroring CCTNS's own stated long-term integration goals
4. **Statewide rollout** across all 1,100+ stations, with ongoing model monitoring and periodic bias audits — directly answering the Odisha-style "it worked in the demo" failure mode by building monitoring in from the start

**Pilot impact measurement** *(added Phase 7 review)*: the pitch currently rests on a strong narrative (CCTNS's unmet mandate, understaffed investigators) but no plan to actually measure whether a pilot helped. If piloted, track: time-to-answer versus the current SCRB-request baseline, share of questions self-served versus escalated, and direct officer-reported usefulness (via the FR-10.1 feedback flag) — not just the technical benchmark metrics in `AIArchitecture.md` §7, which measure the AI's quality, not the tool's real-world impact.

---

## 6. Growth Arc (Concept B → Concept C)

Ship the "Investigative Co-Pilot" (Concept B) for the prototype deadline; use the Aug refinement window to grow toward the "Multi-Agent Command Assistant" (Concept C) — a supervisor agent orchestrating retrieval, network-analysis, pattern-detection, and explanation sub-agents. This gives mentors and judges a genuine "here's what changed" story at each checkpoint, rather than a system that looks finished (and therefore static) from day one.

---

*Next: `Requirements.md`, `UserStories.md`, `FeaturePrioritization.md`, `Roadmap.md`.*
