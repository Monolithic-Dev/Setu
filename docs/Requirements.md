# Requirements.md

**Phase 3 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*Numbered for traceability into `UserStories.md`, `FeaturePrioritization.md`, and later Phase 4/5 design docs.*

---

## Functional Requirements

### FA1 — Conversational Query
- **FR-1.1**: The system shall accept natural-language questions in English and Kannada, typed or spoken.
- **FR-1.2**: The system shall maintain conversational context across multiple turns (e.g., "show me his known associates" following a prior answer about a specific case).
- **FR-1.3**: The system shall handle code-switched input (Kannada and English mixed in one query), since this is how officers realistically speak.
- **FR-1.4**: The system shall respond in the same language/mode the officer used, unless asked otherwise.

### FA2 — Voice Interaction
- **FR-2.1**: The system shall convert spoken Kannada and English input to text (STT) via Bhashini and/or Sarvam AI.
- **FR-2.2**: The system shall optionally convert text answers to spoken output (TTS) in the matching language.
- **FR-2.3**: The system shall degrade gracefully to text-only mode if voice services are unavailable.

### FA3 — Retrieval & Grounding (RAG)
- **FR-3.1**: The system shall retrieve relevant records from the crime dataset before generating an answer (no answer without retrieval).
- **FR-3.2**: The system shall cite which record(s) informed each answer.
- **FR-3.3**: The system shall indicate uncertainty or return "not found" rather than fabricate an answer when retrieval confidence is low.

### FA4 — Criminal Network Visualization
- **FR-4.1**: The system shall generate a visual graph of linked entities (people, cases, locations) relevant to a query.
- **FR-4.2**: The graph shall be interactive (expand/collapse nodes, click through to source records).

### FA5 — Predictive Analytics & Early Warnings
- **FR-5.1**: The system shall surface emerging crime-pattern or hotspot signals proactively, not only in response to a direct question.
- **FR-5.2**: Pattern/"profiling" signals shall be derived from case- and modus-operandi-level features (weapon, method, timing, linked priors) — **never** from demographic or socio-economic identity proxies (`HackathonAnalysis.md` §9).
- **FR-5.3**: Predictive outputs shall be presented as aggregate/geographic/temporal signals (e.g., "cluster of similar break-ins in this zone"), not as individual risk scores attached to a named person.

### FA6 — Explainable AI & Audit Trail
- **FR-6.1**: Every answer shall include a visible reasoning/source trail.
- **FR-6.2**: All queries, retrievals, and answers shall be logged for later audit.
- **FR-6.3**: The audit log shall be exportable alongside the conversation (see FA8).

### FA7 — Role-Based Secure Access
- **FR-7.1**: The system shall authenticate users and enforce role-scoped data visibility (e.g., station-level vs. district-level vs. SCRB-level access).
- **FR-7.2**: The system shall never return data outside a user's role scope, even if asked directly.
- **FR-7.3** *(added Phase 7 review)*: The system shall support a case-level sensitivity flag (e.g., cases involving minors) that restricts access beyond normal role scope, independent of the requesting user's general role.

### FA8 — Export & Reporting
- **FR-8.1**: The system shall export a conversation (question, answer, sources, audit trail) as a PDF.

### FA9 — Data Layer
- **FR-9.1**: The system shall operate over a synthetic, bilingual, realistic Karnataka crime dataset (real SCRB data will not be released — see `PRD.md` §8).
- **FR-9.2**: The dataset schema shall be designed for extensibility toward real CCTNS/CAS data structures, to support the production roadmap (`ProductStrategy.md` §5).

### FA10 — User Feedback *(added Phase 7 review)*
- **FR-10.1**: The system shall let a user flag any answer as incorrect or unhelpful, in-conversation, without leaving the flow.
- **FR-10.2**: Flagged answers shall be logged for review, tagged separately from ordinary audit entries so quality issues are easy to surface (see `MonitoringStrategy.md`).

---

## Non-Functional Requirements

- **NFR-1 (Security):** Data encrypted at rest and in transit; role-scoped access enforced server-side, not just hidden in the UI.
- **NFR-2 (Privacy):** No synthetic data field should be modeled on real individuals; clear separation between demo/synthetic data and any future real-data integration.
- **NFR-3 (Explainability):** No output — conversational, visual, or predictive — without a traceable basis. Applies uniformly across FA3–FA5.
- **NFR-4 (Bilingual parity):** Kannada support tested to the same standard as English, not treated as a secondary/fallback language.
- **NFR-5 (Performance):** Conversational responses fast enough for mid-investigation use; exact latency target to be set once Catalyst QuickML benchmarks are available (Phase 4).
- **NFR-6 (Reliability):** System tested under degraded conditions (partial data, service timeouts, ambiguous queries) — not only the happy-path demo scenario, in direct response to the Odisha precedent (`CompetitorAnalysis.md` §5).
- **NFR-7 (Observability):** All system actions loggable and reviewable — supports both FA6 (audit trail) and the Phase-8 monitoring strategy.
- **NFR-8 (Accessibility):** UI usable by officers with varying levels of digital literacy — plain language, minimal jargon, voice as a first-class input method rather than a bonus.
- **NFR-9 (Scalability):** Architecture should not assume a single-station scale; design should visibly generalize toward 1,100+ stations even if the prototype demos a subset.
- **NFR-10 (Offline/low-connectivity degradation)** *(added Phase 7 review)*: Not every one of 1,100+ stations has strong connectivity. The system shall fail informatively, not silently, under poor connectivity — clear "unable to reach the server, retrying" states rather than a hung or blank UI — and shall queue a submitted query to retry automatically rather than losing it. Full offline functionality is out of scope for this submission; graceful degradation is not.

---

*Next: `UserStories.md`, `FeaturePrioritization.md`, `Roadmap.md`.*
