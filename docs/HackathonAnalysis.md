# Hackathon Analysis — KSP Datathon 2026

**Phase 1 of 8 · Elite AI Datathon Mode**
**Date prepared:** 6 July 2026
**Status:** Complete — Challenge 1 confirmed as final. Team: 4–5 people, dedicated AI/ML + frontend + backend. Phase 2 (Product Discovery) complete — see `Research.md`, `CompetitorAnalysis.md`, `ProductDiscovery.md`.

---

## 1. Executive Summary

Datathon 2026 is a nationwide innovation challenge run by the Karnataka State Police (KSP) via the Hack2Skill (H2S) platform, with **Zoho Catalyst** as the exclusive technology and deployment partner. Two challenge tracks are open, sharing a ₹10 lakh prize pool. We are currently inside the **Prototype Submission window**, which closes **26 July 2026, 11:59 PM IST — about 20 days from today.** This is a two-stage funnel: this submission only needs to clear an *initial* shortlist (~19 Aug); a refinement window and mentor support follow before the in-person Grand Finale (26 Sep).

**Recommendation: Challenge 1 — Intelligent Conversational AI for the KSP Crime Database.** Full reasoning in Section 8. Short version: it's the more AI-native track, it maps almost exactly onto a Generative-AI capability (RAG + LLM Serving) that Zoho Catalyst has just shipped and is actively promoting around this exact event, and it plays best in a live demo for non-technical government judges. Challenge 2 is a fully credible second choice — particularly if your team's strengths skew toward data engineering, geospatial work, and dashboarding rather than NLP.

**The single biggest thing to flag before anything else:** both problem statements ask for "behavioral profiling," "socio-demographic insights," "socio-economic crime correlation," and "predictive risk scoring." These sit close to the feature categories behind well-documented predictive-policing controversies elsewhere (bias amplification, feedback loops, discriminatory targeting). See **Section 9** — this needs a deliberate design decision now, not a patch later. Handled well, it's also a genuine differentiator under the "Responsible AI" and "Ethical Concerns" lens your own brief cares about.

---

## 2. Source Materials Reviewed

| Document | What it contains |
|---|---|
| `Datathon_About.pdf` | Public event page: mission, eligibility, both challenge briefs, prize structure, full timeline, FAQ headers |
| `Submission_Requirements.pdf` | The live submission form: required fields, file/link rules, submission window dates |
| `KSP_Datathon_2026___Prototype_Submission_Template.pptx` | The **mandatory** 16-slide submission deck — extracted in full, see Section 5.3 |
| Official event page (cross-checked via web search) | `hack2skill.com/event/datathon2026` — content matches the PDFs; confirms no separate published evaluation rubric exists anywhere |
| Zoho Catalyst documentation (via web search) | Confirms current Catalyst AI capabilities relevant to architecture — see Section 6.3 |

I did not find a published, weighted judging rubric anywhere. Treat scoring as holistic against the stated goals in the "Why Participate" section (Section 6).

---

## 3. Program Rules & Constraints

- **Eligibility:** Students (UG/PG), working professionals, startups, independent innovators.
- **Team size:** 2–5 people.
- **Cost:** Free to enter.
- **Format:** Remote until the Grand Finale, which is **in person** (Demo Day) — factor travel into planning if your team isn't Karnataka-based.
- **Registration deadline:** 19 July 2026.
- **One challenge track per submission** — the form's Challenge field is single-select (see Section 8 for the case on whether to hedge across both).

---

## 4. Timeline

| Milestone | Date(s) |
|---|---|
| Registration window | 22 May – 19 Jul 2026 |
| **Prototype Submission window (current phase)** | **28 May 2026, 4:00 PM – 26 Jul 2026, 11:59 PM IST** |
| Problem Statement Explainer | 5 Jun 2026, 4–5 PM IST |
| Workshop 1: Introduction to Catalyst by Zoho | 11 Jun 2026 |
| AMA Session | 18 Jun 2026 |
| Initial Shortlist Announcement | 19 Aug 2026 |
| Prototype Refinement window | 19–30 Aug 2026 |
| Induction Session | 29 Aug 2026 |
| Mentor–Mentee Connects | Late Aug 2026 (exact range unclear in source image — worth confirming on your dashboard) |
| Final Shortlist Announcement | 9 Sep 2026 |
| **Grand Finale (in-person Demo Day)** | **26 Sep 2026** |

We are **~20 days** from the prototype deadline as of the date of this analysis.

---

## 5. Submission Requirements — What Actually Gets Graded

### 5.1 The submission form requires
1. **Challenge** — single select (pick one track)
2. **Prototype Brief** — in-form text box, **capped at 1024 characters.** Short — this needs to be drafted and edited as its own artifact, not shortened from a longer doc.
3. **GitHub Public Repository Link** — must include `http://` or `https://`; needs complete source, a proper README, and setup/execution instructions
4. **Prototype Deployed Link** — **must be on Zoho Catalyst exclusively.** Non-Catalyst deployments don't qualify for evaluation, full stop.
5. **Demo Video Link (public)** — Google Drive (public access) or an unlisted/accessible YouTube link
6. **Prototype Deck** — PDF upload, ≤5MB, **must be built from the official template.** Any other format isn't considered for evaluation.

### 5.2 Hard disqualification risks
- Deploying anywhere other than Catalyst
- Submitting a deck not built from the official template
- Any broken or inaccessible link at final submission time

### 5.3 The official template, slide by slide (extracted directly from your file)

| # | Slide asks for |
|---|---|
| 1 | Team details (name, leader, size) + problem statement selected |
| 2 | Brief about the solution |
| 3 | Opportunities: differentiation, how it solves the problem, USP |
| 4 | List of features |
| 5 | Process flow / use-case diagram |
| 6 | Wireframes / mockups *(optional)* |
| 7 | Architecture diagram |
| 8 | Technologies used |
| 9 | **List of Catalyst Services used** |
| 10 | Estimated implementation cost *(optional)* |
| 11 | Prototype snapshots |
| 12 | **Prototype performance report / benchmarking** |
| 13 | Links: GitHub, **demo video (3 minutes)**, deployed link |
| 14 | Additional details / future development |
| 15–16 | Blank / closing |

Two things buried in the template that appear nowhere else in the materials — easy to miss without opening it:
- **The demo video has an explicit 3-minute target** (slide 13) — tighter than "public link" alone suggests.
- **Slide 9 wants named Catalyst services**, and **slide 12 wants a performance/benchmark report.** This isn't "just deploy it there" — it's "show you built with the platform's actual services and can back your numbers." That materially shapes the Phase 4 architecture conversation.

---

## 6. Reading Between the Lines: Hidden Expectations

**6.1 Adoptability is weighted, not just novelty.** The "Why Participate" section frames this as building "solutions that can potentially be adopted by law enforcement agencies," judged partly by government stakeholders, not only technologists. A flashy demo that couldn't plausibly run inside a police department will likely score worse than a more modest one that clearly could.

**6.2 Explainability and security aren't optional extras.** Challenge 1 names "Explainable AI with audit trails" and "Role-based secure access" as *key features*, not stretch goals. For a law-enforcement-facing tool, treat XAI and RBAC as MVP, not Phase-8 polish.

**6.3 Tech-partner alignment appears to be a real, recurring signal.** The previous edition (KSP Datathon 2024) required deployment on Microsoft Azure specifically because Microsoft was that year's partner. This year it's Zoho Catalyst — and Catalyst's QuickML service has just shipped no-code **LLM Serving + RAG + a document Knowledge Base** (currently early access for requested users — worth requesting on day one, don't assume it's on by default), which Zoho is actively promoting via webinars tied to this exact event. Building the AI core natively on Catalyst's own Gen-AI stack, rather than bolting on an external LLM API, is plausibly worth real judging credit — and it directly satisfies slide 9's "Catalyst Services used" ask. This is a concrete point in favor of Challenge 1.

**6.4 No public rubric implies holistic judging.** Since nothing is weighted publicly, expect judges to informally weigh: working demo > architectural elegance > code polish, with real-world plausibility as a multiplier across all of it.

---

## 7. Challenge-by-Challenge Analysis

### Challenge 1 — Intelligent Conversational AI for KSP Crime Database

**Problem stated:** SCRB manages crime data from 1,100+ stations; current tools are static dashboards and manual queries with no real-time or deep analysis.

**Required:** Bilingual (English + Kannada) NL chatbot, voice interaction, context-aware multi-turn conversation, PDF export of chat history, criminal network visualization, crime trend/hotspot detection, predictive analytics & early warnings, explainable AI with audit trails, role-based secure access.

| Dimension | Assessment |
|---|---|
| Problem significance | High — named as SCRB's core pain point |
| Social impact | High — direct investigator efficiency gain statewide |
| AI opportunities | Very high — genuinely LLM/RAG-centric; richest track for showcasing modern AI engineering |
| Technical complexity | High — bilingual NLU, voice I/O, audit-grade explainability, and RBAC is a lot of surface area for 20 days; needs firm scope discipline |
| Innovation potential | High — conversational + bilingual + voice is memorable, less "seen it before" than a dashboard |
| Scalability | Good on paper; a RAG/agent pattern generalizes cleanly across 1,100+ stations |
| Data requirements | Real SCRB data won't be released (sensitive) — needs a credible **synthetic** bilingual crime-record corpus; the harder of the two synthetic datasets to build well |
| Deployment feasibility | Maps very well onto Catalyst QuickML's new LLM Serving/RAG/Knowledge Base (pending early-access approval) |
| Security considerations | High — explicitly named requirement (RBAC, audit trails) |
| Explainability | Explicitly required, not optional — strong natural fit for XAI-pipeline design |
| Demo potential | Very high — a bilingual, voice-enabled chatbot is the single most "wow" thing you can show live to non-technical judges |
| Est. winning probability | Likely the more *popular* track among entrants (chatbots are the obvious "AI datathon" answer) — probably more competition, but also the track judges will instinctively read as "most AI" |
| Key risks | Scope creep (7+ major features at once); Kannada NLU quality; synthetic data credibility; Gen-AI early-access approval delay |

### Challenge 2 — AI-Driven Crime Analytics & Visualization Platform

**Problem stated:** Siloed data, manual reporting, limited advanced analytics/proactive policing.

**Required:** Network/link analysis, repeat-offender tracking, socio-economic crime correlation, predictive risk scoring, AI/ML pattern detection, interactive dashboards + geospatial maps, hotspot detection, district drilldowns, trend/anomaly alerts.

| Dimension | Assessment |
|---|---|
| Problem significance | High — same institutional pain point, operations-facing |
| Social impact | High, arguably more "usable tomorrow" by a duty officer |
| AI opportunities | Solid but more classical (clustering, graph analysis, anomaly detection, risk scoring) — legitimate AI/ML, less "cutting-edge LLM" |
| Technical complexity | High but more conventional: GIS/geospatial + graph analytics + predictive modeling + dashboarding — well-understood engineering, lower execution risk |
| Innovation potential | Moderate–high; real ceiling exists (e.g., graph-based co-offending analysis) but risks reading as "just a BI dashboard" if AI isn't foregrounded |
| Scalability | Good — dashboards naturally extend district-by-district |
| Data requirements | Still needs synthetic data, but a large synthetic tabular/geospatial crime dataset is comparatively easier to make convincing than Challenge 1's bilingual conversational corpus |
| Deployment feasibility | Same Catalyst constraint; charts/dashboards are straightforward to host; can use QuickML's classical AutoML for the risk-scoring piece |
| Security considerations | Real, but not explicitly named as a headline feature the way Challenge 1 does |
| Explainability | Not explicitly requested — an opportunity to differentiate by adding it anyway |
| Demo potential | High visually (maps, network graphs, heatmaps), but "dashboard" demos are a more familiar genre to judges than a live bilingual conversation |
| Est. winning probability | Possibly *less* contested if most teams gravitate to the chatbot track — a genuinely strong analytics platform could stand out through lower competition + clean execution |
| Key risks | Blending into "generic BI tool" perception; "predictive risk scoring" and "socio-economic correlation" are the most ethically loaded phrases in either problem statement (Section 9); needs real GIS boundary data to look credible |

---

## 8. Head-to-Head & Recommendation

| | Challenge 1 (Conversational AI) | Challenge 2 (Analytics Platform) |
|---|---|---|
| Best fit if your team is strong in... | NLP/LLM engineering, conversational UX | Data engineering, geospatial/GIS, dashboards |
| Catalyst tech-partner alignment | Very strong (native RAG/LLM Serving showcase) | Moderate (QuickML AutoML fits, but less headline) |
| Live-demo memorability | Highest | High, but a more familiar genre |
| Build risk in 20 days | Higher (more moving parts) | Lower (more conventional stack) |
| Likely competition | Higher (the "obvious" AI choice) | Possibly lower |

**Recommendation: Challenge 1**, on balance — mainly because it's the closest match to both "what an AI datathon judge wants to see" and "what this year's specific tech partner just built and is actively promoting." This is a genuine judgment call, not a runaway winner, and it should bend toward your team's actual skills: if your team is 3+ people with strength in backend/data/geospatial work and comparatively little NLP experience, Challenge 2 is the more executable bet in 20 days and a perfectly credible submission. Better to nail Challenge 2 than half-build Challenge 1.

Submitting to **both** is technically possible (nothing in the rules forbids it) but not advisable unless your team is 5 people with clearly separable workstreams — splitting a 20-day sprint two ways usually produces two mediocre entries instead of one strong one.

---

## 9. Responsible-AI Flag (applies to either track)

Both problem statements explicitly ask for features in genuinely sensitive territory: "behavioral profiling," "socio-demographic insights" (Challenge 1), and "socio-economic crime correlation," "predictive risk scoring" (Challenge 2). These are close cousins of the feature categories behind well-documented predictive-policing controversies elsewhere — risk-scoring tools shown to encode demographic bias, and hotspot systems that create feedback loops by sending more patrols to already over-policed areas, generating more recorded "crime" there, which the model then reads as confirmation. This isn't hypothetical for this specific event: the 2024 edition of this same Datathon carried an almost identical ask ("predicting the likelihood of future crimes based on demographic information and criminal history"), so it's a recurring design tension organizers haven't resolved on their own end.

Recommended approach, in either track:
- Ground pattern-detection and "profiling" features in **modus operandi and case-level features** (weapon/method, time, location, linked priors) — **not** demographic or socio-economic proxies for identity.
- Keep predictive elements at the **aggregate/geographic/temporal level** (patrol resource allocation, which case clusters look linked) rather than **individual risk scores** attached to a named person.
- Surface this reasoning explicitly in the XAI/audit trail — show *why* a pattern was flagged in case-evidence terms, not demographic ones.

Handled this way, it's not just risk mitigation — it directly strengthens the score on "Explainable AI," "Responsible AI," and "Ethical Concerns," all explicitly named as evaluation lenses in your own brief.

**Update from Phase 7 (Judge Review):** worth stating honestly — excluding demographic fields from the schema is a strong mitigation of the most direct harm, not a claim that the bias problem is fully solved. Location itself can function as a demographic proxy if certain areas have been historically over-policed for reasons unrelated to actual crime rates. The complete answer pairs input-side exclusion (this section) with output-side monitoring — periodically checking whether hotspot flags disproportionately concentrate in specific areas relative to independent crime indicators. See `AIArchitecture.md` §4 and `MonitoringStrategy.md` for where this is now tracked.

---

## 10. Cross-Cutting Constraints & Risks (either track)

- **Synthetic data is mandatory, not optional.** Real SCRB crime/offender data is sensitive and won't be provided or usable as-is. Both tracks need a deliberately designed synthetic dataset strategy realistic enough to demo convincingly — a Phase 2/4 workstream either way.
- **Catalyst Gen-AI features are "early access for requested users"** per Zoho's own docs — request access on day one rather than assuming it's enabled.
- **Two Catalyst components are being sunset:** Event Listeners, File Store, and Cron entered deprecation in Aug 2025 and reach end-of-life 30 Apr 2026 — don't build on them; use replacements (e.g., Stratus instead of File Store). Also, Python 3.9 support on Catalyst began deprecating 1 Jun 2026 — target Python 3.10+ for any Python Functions.

---

## 11. Open Items / What I Need From You

- ~~Team size and skill mix~~ — **Resolved**: 4–5 people, dedicated AI/ML + frontend + backend. This shape favors Challenge 1 structurally (clean ownership split across the three roles).
- ~~Confirm the challenge choice~~ — **Resolved**: Challenge 1 confirmed. Kannada voice risk de-risked via Bhashini/Sarvam AI (see Phase 2 discussion); benchmarking plan for the conversational system to be scoped as a Week 1 task, not an afterthought.
- Exact "Mentor–Mentee Connects" date range was unclear in the source image (showed as an inverted range) — worth a 30-second check on your Hack2Skill dashboard; not urgent.

---

*Next: Phase 2 — Product Discovery (Research.md, CompetitorAnalysis.md, ProductDiscovery.md), on your approval.*
