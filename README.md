<div align="center">
  <img src="docs/assets/dashboard.png" alt="Setu Network Dashboard" width="800"/>
  <br/><br/>
  <h1>Setu Intelligence Platform</h1>
  <p><b>Advanced Conversational AI & Analytics for the Karnataka State Police</b></p>

  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Zoho_Catalyst-4353FF?style=for-the-badge&logo=zoho&logoColor=white" alt="Zoho Catalyst" />
  </p>
</div>

<br/>

## Overview

Setu is an enterprise-grade, bilingual (Kannada & English) conversational AI designed exclusively for law enforcement. It empowers investigators to query vast crime databases using natural language, providing source-cited intelligence, advanced network visualization, and proactive pattern recognition. 

Built natively on **Zoho Catalyst**, the platform ensures all intelligence is strictly grounded in case evidence.

<div align="center">
  <img src="docs/assets/login.png" alt="Setu Authentication" width="400" style="border-radius: 8px;"/>
</div>

---

## Core Capabilities

- **Bilingual Conversational Interface**: Native support for English and Kannada via both text and voice.
- **Explainable RAG**: Retrieval-Augmented Generation provides deterministic answers backed by explicitly cited, clickable case sources.
- **Criminal Network Visualization**: Interactive D3.js node graphs identifying relationships between suspects, locations, and modus operandi.
- **Tamper-Evident Auditing**: Immutable hash-chained query logs ensure complete transparency.
- **Strict Role-Based Access Control**: Enforces jurisdiction boundaries automatically (e.g., Station Officer vs. State Analyst).
- **High-Performance Hybrid Search**: Proprietary District-Level Index Partitioning achieving sub-100ms retrieval latency at scale.

---

## System Architecture

The architecture utilizes a serverless event-driven design, leveraging Zoho Catalyst Advanced I/O functions for orchestration, hybrid semantic search, and LLM synthesis.

```mermaid
graph TD
    classDef client fill:#000000,stroke:#333333,stroke-width:1px,color:#ffffff
    classDef serverless fill:#1e293b,stroke:#334155,stroke-width:1px,color:#ffffff
    classDef data fill:#0f172a,stroke:#334155,stroke-width:1px,color:#ffffff
    classDef external fill:#171717,stroke:#404040,stroke-width:1px,color:#ffffff

    User((Investigator))
    
    subgraph Frontend Client
        Chat[Web Application<br/>React + Vite]:::client
    end
    
    subgraph Serverless Backend
        API[API Gateway]:::serverless
        RBAC[Auth & Security Gate]:::serverless
        RAG[Hybrid Search Engine]:::serverless
    end
    
    subgraph Data Layer
        Index[(Local Partitioned<br>TF-IDF Index)]:::data
        Audit[(Catalyst<br>Audit Store)]:::data
    end
    
    subgraph AI Services
        LLM[QuickML LLM]:::external
    end
    
    User -->|Voice / Text| Frontend
    Chat -->|HTTPS Request| API
    
    API --> RBAC
    RBAC -->|Authorized| RAG
    RBAC -->|Log Request| Audit
    
    RAG -->|Filter & Score| Index
    RAG -->|Context Injection| LLM
    LLM -->|Synthesized Analysis| API
    
    API -->|Encrypted Payload| Chat
```

---

## User Flow

```mermaid
sequenceDiagram
    autonumber
    actor Investigator
    participant UI as Setu Web Client
    participant API as Security API
    participant Index as Retrieval Engine
    participant LLM as AI Synthesizer
    
    Investigator->>UI: Voice/Text Query Input
    UI->>API: Authenticated POST Request
    
    API->>API: Enforce Jurisdiction (RBAC)
    API-->>Index: Scoped Request
    
    Index->>Index: Semantic & Structured Match
    Index-->>API: Extracted Case Sources
    
    API->>API: Mask Restricted Cases
    
    API->>LLM: Provide Sanitized Context
    LLM-->>API: Intelligence Summary
    
    API->>UI: Source-Cited Answer payload
    UI->>Investigator: Actionable Dashboard UI
```

---

## Technical Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | React, TypeScript, Vite, D3.js | High-performance, reactive user interface and data visualization. |
| **Backend** | Python 3.10+ | Orchestration, text processing, and security middleware. |
| **Infrastructure** | Zoho Catalyst | Serverless Advanced I/O, Data Store, and Edge Caching. |
| **AI/ML** | QuickML, TF-IDF, BM25 | Hybrid retrieval and generative summarization. |

---

## Installation & Deployment

**1. Repository Setup**
```bash
git clone https://github.com/Monolithic-Dev/Datathon-Hack.git
cd Datathon-Hack
```

**2. Catalyst CLI Initialization**
```bash
npm install -g zcatalyst-cli
catalyst login
catalyst init
```

**3. Dependency Management**
```bash
# Initialize client environment
cd client && npm install

# Initialize serverless functions
cd ../functions/setu_api && pip install -r requirements.txt --break-system-packages
```

**4. Local Development**
```bash
# Boot the Catalyst local server
catalyst serve

# Start the frontend dev server (in a separate terminal)
cd client && npm run dev
```

---

## Responsible AI Commitment

Setu is engineered with strict ethical guardrails. Predictive models and pattern recognition engines operate exclusively on **modus operandi and case-level evidence**. The system actively strips and prohibits filtering by demographic, religious, caste, or socio-economic indicators at the schema level.

<br/>
<div align="center">
  <p><i>Developed for the Karnataka State Police Datathon 2026</i></p>
</div>
