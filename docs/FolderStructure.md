# FolderStructure.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. Repository Layout

```
setu-ksp-datathon/
├── catalyst.json                    # Catalyst project manifest
├── .catalystrc
├── README.md                        # setup + execution instructions (submission requirement)
├── LICENSE
│
├── client/                          # Frontend — Catalyst Web Client Hosting (owner: Frontend)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/                # text + voice chat UI
│   │   │   ├── NetworkGraph/        # interactive graph view
│   │   │   ├── AlertsPanel/         # hotspot/early-warning view
│   │   │   └── AuditExport/         # audit log + PDF export view
│   │   ├── hooks/
│   │   ├── i18n/                    # EN/KN string resources
│   │   ├── api/                     # typed API client for functions/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── functions/                       # Backend — Catalyst Functions (owner: Backend, with AI/ML on specific ones)
│   ├── queryFunction/                    # POST /api/query — Conversation Service (AI/ML)
│   ├── voiceTranscribeFunction/           # POST /api/voice/transcribe (AI/ML)
│   ├── voiceSynthesizeFunction/           # POST /api/voice/synthesize (AI/ML)
│   ├── networkFunction/                   # GET /api/network/{entityId} (Backend)
│   ├── alertsFunction/                    # GET /api/alerts/hotspots — Prediction Service (AI/ML)
│   ├── exportFunction/                    # POST /api/export/pdf (Backend)
│   ├── auditFunction/                     # GET /api/audit/logs (Backend)
│   └── shared/                            # shared auth/RBAC middleware, schemas, adapters
│       ├── auth_middleware.py
│       ├── speech_adapter.py              # Bhashini/Sarvam adapter (Design.md §3)
│       └── retrieval/
│           ├── structured_search.py       # ZCQL queries
│           └── semantic_search.py         # QuickML Knowledge Base client
│
├── ml/                               # AI/ML workstream artifacts (owner: AI/ML)
│   ├── data_generation/              # synthetic dataset generation scripts
│   ├── prediction_model/             # classical ML hotspot/pattern model (AIArchitecture.md §4)
│   ├── prompts/                      # QuickML LLM prompt templates
│   └── eval/                         # benchmark harness (AIArchitecture.md §7)
│
├── docs/                             # all phase deliverables from this project (this doc set)
│
└── tests/
    ├── unit/
    ├── integration/
    └── eval/                          # bilingual/hallucination/retrieval benchmark tests
```

---

## 2. Ownership Map (given 4–5 people: dedicated AI/ML, frontend, backend)

| Area | Primary owner | Notes |
|---|---|---|
| `client/` | Frontend | Also owns `i18n/` bilingual UI strings |
| `functions/query*`, `functions/voice*`, `functions/alerts*`, `ml/` | AI/ML | Owns everything touching QuickML, Bhashini/Sarvam, the prediction model |
| `functions/network*`, `functions/export*`, `functions/audit*`, `functions/shared/auth_middleware.py` | Backend | Owns RBAC enforcement, Data Store schema, audit logging |
| `tests/` | Shared, written by whoever owns the code being tested | Reviewed by at least one other team member regardless of area |

If the team is 5 rather than 4, the fifth person is best placed either pairing with AI/ML on the prediction model + eval harness (the two most time-boxed-but-important pieces per `Roadmap.md`), or owning `docs/` + demo/deck production so that work doesn't compete with build time in Week 3.

---

*Next: `TechStack.md`, `CodingStandards.md`, `SprintPlan.md`, `TestingStrategy.md`, `DeploymentStrategy.md`, `MonitoringStrategy.md`, `RiskRegister.md`.*
