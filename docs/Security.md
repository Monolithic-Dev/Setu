# Security.md

**Phase 4 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Access Control

Role-based, enforced at the data layer via Catalyst Data Store table scopes (`Database.md` §4), not only in application code — meaning a bug in the Functions layer can't accidentally expose out-of-scope rows, because the database itself refuses the query. Four roles: Station Officer, SCRB Analyst, District SP, System Admin.

## 2. Encryption

Data encrypted at rest and in transit as provided by Catalyst's managed infrastructure. No credentials or tokens stored client-side beyond what Catalyst Authentication's standard flow requires.

## 3. Threat Model

| Threat | Mitigation |
|---|---|
| **Prompt injection** — a query engineered to make the LLM ignore its grounding instructions and reveal out-of-scope data or fabricate authoritative-sounding answers | System prompt hardened against instruction override; retrieval results are the only source of factual claims (FR-3.3); RBAC scope is enforced *before* retrieval, not left to the LLM to self-police |
| **Data leakage across roles** | Table-level scopes (`Database.md` §4) + server-side scope filtering in the Retrieval Service, never client-side |
| **Synthetic-vs-real data confusion** | Clear labeling and separate storage boundary between the current synthetic dataset and any future real-data integration (`ProductStrategy.md` §5) |
| **Audit tampering** | Audit entries are append-only; no update/delete permission granted on the `AUDIT_ENTRY` table to any role except System Admin |
| **Over-reliance on a single external speech provider** | Adapter pattern (`Design.md` §3) allows fallback between Bhashini and Sarvam, and to text-only mode, rather than a single point of failure |
| **Operational failure under real conditions (Odisha precedent)** | See `Requirements.md` NFR-6 — tested under degraded conditions, not just the happy path |

## 4. Privacy by Design

- Synthetic data only for this submission; no real individual is represented.
- Person records store only what's operationally necessary — no demographic/socio-economic fields exist in the schema at all (`Database.md` §3), which is a stronger guarantee than "the application chooses not to use them."
- Audit trail exists specifically so any AI-assisted decision is reviewable after the fact — privacy and accountability reinforcing each other rather than trading off.

## 5. Responsible-AI Guardrail (recap, enforced technically here)

`AIArchitecture.md` §4 already excludes demographic/socio-economic fields from the Prediction Service's Data Store scope. This section confirms that exclusion is a **security control**, not just a product decision — it is implemented the same way any other access restriction is (table/column-level scope), so it inherits the same audit and enforcement guarantees as RBAC does.

---

*Next: `Deployment.md`, `UX.md`.*
