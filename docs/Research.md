# Research.md — Product Discovery

**Phase 2 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Root Cause Analysis

Karnataka's 1,100+ police stations already sit inside a national digitization effort, not a blank slate. CCTNS (Crime and Criminal Tracking Network & Systems), running since 2009, connects roughly 15,000 stations and 5,000+ higher offices nationwide, digitizing FIR registration, investigation records, and chargesheets — and Karnataka is consistently cited as one of the more advanced states in CCTNS rollout, with its own pre-CCTNS state system ("Police IT") before that. Nationally, the great majority of FIRs are now filed digitally.

So the honest root cause isn't "no digital crime data exists." It's that **digitization and insight are two different problems, and only the first one got solved.** CCTNS's own founding goals in 2009 explicitly included "enhanced ability to analyze crime patterns and modus operandi" — that was the plan from day one. But independent commentary on the program (including from the PM's Economic Advisory Council) has noted that CCTNS is a tool that facilitates police work without guaranteeing better outcomes, and that not every state uses every module to its full potential. The data got digitized; the analysis layer on top of it — the part that turns 1,100 stations' worth of siloed records into a single queryable, pattern-aware system — never got built. That's precisely the gap the problem statement describes as "static dashboards and manual queries."

Two compounding root causes worth naming:

- **Personnel math.** As of the Bureau of Police Research & Development's most recent reporting, India's actual police-to-population ratio (152.80 per lakh) runs well below its own sanctioned strength (196.23 per lakh). Investigators are structurally stretched thin — which means anything that removes manual query/analysis burden has outsized real leverage, not just convenience value.
- **Language mismatch.** CCTNS's Core Application Software and most dashboard tooling are English-first. A meaningful share of station-level officers work more naturally in Kannada. Tooling that doesn't meet them in their working language quietly gets under-used, which is itself a likely contributor to the "modules not used to full potential" observation above.

**Why this matters for our build:** we're not inventing a new problem category — we're finishing a specific, named, 15-year-old unmet promise of India's own police digitization program, with tools (LLMs, RAG) that didn't exist when CCTNS was designed. That's a strong, true framing for the Prototype Brief.

---

## 2. First-Principles Analysis

Stripped of the "chatbot" framing, what does an investigator actually need when they have a question about crime data?

1. **Retrieval** — find the right records out of a large, fragmented store
2. **Synthesis** — turn many records into one coherent answer, not a list of rows
3. **Accessibility** — in the language and mode (text or voice) the officer actually works in
4. **Speed** — an answer usable *during* an investigation, not a report that arrives after the moment has passed
5. **Defensibility** — traceable enough to cite in a case file or explain under questioning; an answer nobody can explain is an answer nobody can safely act on
6. **Safety** — scoped to what that officer's role should see, and never fabricated

Notice this decomposes, independent of the brief's wording, into exactly: **RAG (1+2) + a bilingual conversational interface (3+4) + explainability and audit trails (5) + RBAC (6).** The official feature list isn't an arbitrary checklist — it's what falls out of the problem when you take it seriously from first principles. Useful to know, because it means cutting any of these for time isn't a minor scope trim, it's removing something the problem structurally requires.

---

## 3. Stakeholder Analysis

| Stakeholder | Relationship to the system |
|---|---|
| Investigating Officer / Sub-Inspector (station level) | Primary user — asks questions, needs fast, trustworthy answers |
| SCRB Data Analyst (state HQ) | Primary user today acting as a human query bottleneck; becomes a power-user / data-quality owner once self-service exists |
| Circle Inspector / District SP | Secondary user — wants district-level pattern summaries, not just single-case answers |
| DGP / IG leadership | Consumes aggregate insight; likely audience at Grand Finale demo |
| Prosecution / Courts | Downstream consumer of anything exported from the tool (hence the PDF export + audit trail requirement) |
| Citizens (indirect) | Data subjects; not direct users, but the reason RBAC, privacy, and bias-avoidance are non-negotiable |
| Judges / evaluation panel | Evaluate adoptability, not just novelty (see HackathonAnalysis.md §6.1) |

---

## 4. User Personas

**Persona 1 — "Investigating Sub-Inspector"**
Station-level officer, 8–15 years of service, juggles 15–20 active cases, works primarily in Kannada with functional English for paperwork. Today, if she suspects a case is linked to a prior one, her options are: recall it from memory, ask colleagues informally, or file a request to SCRB and wait. She needs an answer in the next ten minutes, not next week, and needs to be able to explain how she got it if it ends up in a case file.

**Persona 2 — "SCRB Data Analyst"**
State HQ, handles incoming custom-query requests from stations across the state — currently the literal human bottleneck the problem statement is describing. Wants self-service to shrink his queue, but also wants confidence the tool won't hand out data outside a requester's role, since he's the one who'd be accountable for a leak.

**Persona 3 — "District Superintendent of Police"**
Oversees dozens of stations in a district, wants pattern-level and hotspot-level summaries rather than single-case detail. Bridges naturally toward Challenge 2's territory — worth keeping this persona in mind if a district-level summary view becomes a stretch feature later (Phase 3 decides).

---

## 5. Law Enforcement Workflow Analysis (Current State)

FIR filed at station (CCTNS/CAS) → case investigated locally by the IO → if a pattern or link to another case is suspected, the IO has no direct way to check → informal ask-around, or a formal request to SCRB → SCRB analyst manually runs a query/report → result delivered as a static document, often days later → IO incorporates it into the case file if it's still relevant by then.

The bottleneck isn't data capture — it's every step *after* capture requiring a human intermediary.

---

## 6. User Journey Mapping — As-Is vs. To-Be

| Stage | As-Is | To-Be |
|---|---|---|
| IO has a question | Recalls from memory or asks colleagues informally | Asks the assistant in Kannada or English, typed or spoken |
| Getting an answer | Formal request to SCRB, days of wait | Answer in seconds, grounded in retrieved records |
| Verifying the answer | No standard way to check "why" | Audit trail shows which records/reasoning produced the answer |
| Using it in a case file | Manually re-typed/summarized from SCRB's static report | Exported directly (PDF export of conversation) with traceability intact |
| Spotting a wider pattern | Essentially impossible for a single IO to do alone | Network visualization / hotspot detection surfaces it directly |

---

## 7. Pain Point Analysis

- **Latency**: days between question and answer, when investigations often need answers in hours
- **Language mismatch**: English-first tooling under-serves Kannada-first officers, plausibly suppressing usage of what digital tools already exist
- **No self-service**: every cross-reference question routes through a single human bottleneck (the SCRB analyst)
- **No explainability**: even where analytics exist today, there's no visible "why" — a real problem the moment output needs to support a legal case
- **No cross-station pattern visibility**: an individual IO has no practical way to see whether their case connects to a pattern spanning other stations
- **(Relevant if Challenge 2 territory ever resurfaces)**: command-level reporting is manual and siloed, so district/state leadership can't easily see hotspot or trend shifts either

---

## 8. Existing Solution Analysis

| Solution | What it is | Relevance / Gap |
|---|---|---|
| **CCTNS / CAS** | The actual incumbent — national police IT backbone since 2009, digitizes FIRs/chargesheets across ~15,000 stations | This is the system we're building *on top of*, not replacing. Its own stated goals (pattern analysis) are what our solution finally delivers |
| **MahaCrimeOS AI (Maharashtra)** | AI crime-investigation copilot built on Microsoft Foundry, helps process complaints and navigate case data/procedures; rolled out from a Nagpur pilot to all ~1,100 stations statewide as of Dec 2025 | The closest direct state-police analog in India right now. Focused on complaint/FIR processing and procedural navigation in English/Hindi/Marathi — not clearly a conversational query layer over the full crime database with network visualization or predictive alerts, and not Kannada. Genuinely relevant precedent to study, not a like-for-like competitor |
| **West Bengal AI Legal-Assistant Bot** | Investigator-facing bot with 50,000+ pages of legal material (case law, NHRC/MHA guidance), rolled out to ~400 investigators across 8 units (Dec 2025) | Shows investigator-facing AI assistants are an active, credible pattern in Indian policing right now — but this one answers legal-procedure questions, not crime-database queries |
| **Singapore Police AI Chatbot** | Citizen-facing chatbot on crime prevention/procedure, built on Microsoft Azure, handles 100,000+ inquiries/year | Proves the "chatbot for policing" pattern works at scale — but citizen-facing, not investigator-facing |
| **CrimeTracer (SoundThinking, US)** | Commercial conversational search over a unified law-enforcement records platform; investigators refine queries conversationally and get compliant results in seconds | The closest *functional* analog anywhere — conversational querying of a large crime-records store. Commercial, foreign, not localized, not built for this data environment |
| **Odisha AI Command Centre (cautionary tale)** | AI-processed CCTV/drone system for crowd management, deployed for the 2025 Rath Yatra | Failed to deliver actionable alerts during a fatal stampede — investigation found under half the cameras were functional and feeds were inconsistent. Important reminder that a system judged well in a demo but built shakily can fail badly in the real deployment it's meant for; reinforces why "adoptability," not just novelty, should drive our engineering choices |

---

## 9. Opportunity Mapping

None of the reviewed systems combine all of the following in one place: **investigator-facing conversational query, over a full state crime database, bilingual in Kannada and English, with audit-trail-grade explainability, built natively on this year's own technology partner's AI stack.** MahaCrimeOS comes closest institutionally but is intake/procedure-focused and not Kannada; CrimeTracer comes closest functionally but is foreign and commercial. That combination — not any single piece of it — is the actual whitespace.

---

*Next: `CompetitorAnalysis.md` (detailed profiles + feature matrix) and `ProductDiscovery.md` (concept brainstorm + recommendation).*
