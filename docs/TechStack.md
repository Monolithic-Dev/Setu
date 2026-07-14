# TechStack.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Stack Summary

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + TypeScript, Catalyst's React CLI plugin, Tailwind CSS | TypeScript gives a 4–5 person team real collaboration safety; Catalyst's own React plugin handles build/deploy integration with Web Client Hosting |
| Backend runtime | Python 3.10+ (Catalyst Advanced I/O Functions) | One language across backend and AI/ML keeps a small team from context-switching runtimes; explicitly avoids the Python 3.9 deprecation flagged in Phase 1/4 |
| Conversational AI | Catalyst QuickML — LLM Serving + RAG + Knowledge Base | Native to the mandated platform; directly satisfies template slide 9 |
| Predictive/hotspot model | scikit-learn (clustering/classification) or Catalyst Zia AutoML, run against the built-in OLAP layer | Classical ML for clean, benchmarkable metrics (`AIArchitecture.md` §4) |
| Entity extraction | Zia Text Analytics (NER, Keyword Extraction) | Enriches structured fields from narrative text during ingestion |
| Speech (Kannada/English) | Bhashini (POC tier) and/or Sarvam AI, behind a shared adapter interface | Verified to handle Kannada, including code-switching (`AIArchitecture.md` §2) |
| Structured data | Catalyst Data Store + ZCQL | Verified genuinely relational, with native table-level RBAC scopes |
| Analytics | Catalyst built-in OLAP | No separate warehouse needed |
| Caching | Catalyst Cache | Conversation/session context |
| Auth | Catalyst Authentication | RBAC token issuance |
| Object storage | Catalyst Stratus | Exported PDFs; explicitly not the deprecated File Store |
| Network graph rendering | D3.js (or a React-friendly wrapper such as react-force-graph) | Well-established, flexible enough for interactive expand/collapse (FR-4.2) |
| Monitoring | Catalyst APM + Automation Testing | Function performance, API test/failure diagnostics |
| Version control | Git / GitHub (public repo per submission requirement) | — |
| Testing | pytest (backend/ML), Jest + React Testing Library (frontend) | Standard, well-supported in each ecosystem |

---

## 2. Alternatives Considered

| Decision | Alternative considered | Why not chosen |
|---|---|---|
| Catalyst QuickML RAG | Custom RAG with an external vector DB (Pinecone/Weaviate) + external LLM API | More infrastructure, weaker "built natively on Catalyst" story for judging (`HackathonAnalysis.md` §6.3); revisit only if QuickML's retrieval quality proves insufficient |
| Python for backend Functions | Node.js | Would split the team across two runtimes for no clear benefit, given AI/ML work is naturally Python-centric |
| scikit-learn for prediction | Deep learning model for hotspot detection | Unnecessary complexity for tabular case-pattern data; classical ML is more interpretable and easier to benchmark credibly in the time available |
| Bhashini/Sarvam for speech | Google Cloud Speech-to-Text/Text-to-Speech | Bhashini/Sarvam are India-specific and Kannada-tested with code-switching support, and Bhashini in particular tells a stronger "built for India's own infrastructure" adoption story (`ProductStrategy.md` §2) |

---

## 3. Scalability Notes

Catalyst Functions scale automatically with request volume; Data Store and OLAP are managed and scale with usage. The main scaling consideration for this specific system isn't infrastructure — it's **QuickML's early-access status and any associated rate limits**, which should be confirmed directly with Catalyst once access is granted (open item in `memory.md`), since that's the one component whose scaling behavior isn't yet verified firsthand.

---

*Next: `CodingStandards.md`, `SprintPlan.md`, `TestingStrategy.md`, `DeploymentStrategy.md`, `MonitoringStrategy.md`, `RiskRegister.md`.*
