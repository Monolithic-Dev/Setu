# UserStories.md

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*Personas from `Research.md` §4. Requirement IDs reference `Requirements.md`.*

---

## Persona 1: Investigating Sub-Inspector

**US-1.1** — As an Investigating Sub-Inspector, I want to ask a question about a case in Kannada, so that I don't have to translate my thinking into English first. *(FR-1.1, FR-1.3)*
- Acceptance: a spoken or typed Kannada query returns a Kannada answer without requiring English input.

**US-1.2** — As an Investigating Sub-Inspector, I want to ask a follow-up question without repeating context, so that I can dig deeper the way I would with a colleague. *(FR-1.2)*
- Acceptance: a second query referencing "he," "that case," or similar resolves correctly using prior conversation context.

**US-1.3** — As an Investigating Sub-Inspector, I want to see which records an answer came from, so that I can trust it enough to act on it. *(FR-3.2, FR-6.1)*
- Acceptance: every answer displays at least one traceable source reference.

**US-1.4** — As an Investigating Sub-Inspector, I want to export a conversation as a PDF, so that I can attach it to a case file. *(FR-8.1)*
- Acceptance: exported PDF includes the question, answer, sources, and timestamp.

**US-1.5** — As an Investigating Sub-Inspector, I want to see a visual map of who a suspect is connected to, so that I can spot leads I wouldn't find by reading text alone. *(FR-4.1, FR-4.2)*
- Acceptance: a query about a named individual can produce an interactive network graph.

---

## Persona 2: SCRB Data Analyst

**US-2.1** — As an SCRB Data Analyst, I want officers to self-serve routine cross-reference questions, so that my query backlog shrinks. *(FA1, FA3)*
- Acceptance: a representative sample of today's "typical SCRB request" question types can be answered without analyst involvement.

**US-2.2** — As an SCRB Data Analyst, I want a full audit log of every AI-assisted query, so that I remain accountable for what the system surfaces. *(FR-6.2)*
- Acceptance: every query/answer pair is logged with user identity, timestamp, and sources used.

**US-2.3** — As an SCRB Data Analyst, I want confidence that officers only see data within their role's scope, so that a self-service tool doesn't create a new leak vector. *(FR-7.1, FR-7.2)*
- Acceptance: a test query from a station-level account for out-of-scope data is correctly denied.

---

## Persona 3: District Superintendent of Police

**US-3.1** — As a District SP, I want to see emerging patterns across my district without requesting a custom report, so that I can allocate patrols proactively. *(FR-5.1, FR-5.3)*
- Acceptance: the system surfaces at least one aggregate/geographic pattern signal without a direct query prompting it.

**US-3.2** — As a District SP, I want any "risk" or "pattern" signal explained in case-evidence terms, so that I can trust it wasn't generated from demographic profiling. *(FR-5.2, NFR-3)*
- Acceptance: every predictive signal's explanation references modus-operandi/case features, never demographic fields.

---

## Cross-Cutting: Judges / Evaluators (not an end user, but worth writing for)

**US-4.1** — As a judge reviewing the submission, I want to see a working demo of the actual system, not just slides, so that I can evaluate real capability. *(supports HackathonAnalysis.md §6.1 — adoptability signal)*
- Acceptance: deployed Catalyst link is live and walks through the same flow shown in the demo video.

**US-4.2** — As a judge, I want to see quantified performance, not just a qualitative demo, so that I can compare submissions fairly. *(supports template slide 12 — benchmarking)*
- Acceptance: a benchmarking report exists with concrete metrics (retrieval precision, bilingual accuracy, latency).

---

*Next: `FeaturePrioritization.md`, `Roadmap.md`.*
