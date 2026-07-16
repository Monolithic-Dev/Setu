# Setu — Conversational AI for the KSP Crime Database

*Karnataka State Police Datathon 2026 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database*

> Working name — see `docs/PRD.md` for naming caveats.

---

## What This Is

Setu is a bilingual (Kannada + English), voice-enabled conversational AI that lets Karnataka Police investigators query crime records in plain language, get source-cited and explainable answers, visualize criminal networks, and receive proactive crime-pattern early warnings — all grounded in case evidence, never demographic profiling. Built natively on Zoho Catalyst.

Full problem framing, research, and product decisions are in [`docs/`](./docs) — this README covers what you need to run the project.

## Problem Statement

SCRB manages crime data from 1,100+ police stations across Karnataka. Current tooling is static dashboards and manual queries, with no real-time or deep analysis. See `docs/HackathonAnalysis.md` and `docs/Research.md` for the full problem framing.

## Features

- Bilingual (Kannada + English) conversational query, text and voice
- RAG-grounded answers with visible source citations
- Interactive criminal network visualization
- Proactive, case-evidence-based hotspot/early-warning alerts
- Full audit trail and role-based access control
- PDF export of any conversation

## Tech Stack

React + TypeScript · Python 3.10+ (Catalyst Functions) · TF-IDF + BM25 Retrieval · Local NLP Heuristics · Catalyst Data Store + OLAP · D3.js

Full target rationale in `docs/TechStack.md`.

## Architecture

See `docs/Architecture.md` and `docs/AIArchitecture.md` for target diagrams, and `docs/Datathon_Implemented_Features.md` for current implemented state. High level: a serverless Catalyst Functions layer orchestrates hybrid RAG (ZCQL structured search + TF-IDF semantic search), Data Store/OLAP (structured data + analytics), and local Jaccard-similarity network prediction, behind strict role-based access control.

## Setup & Installation

```bash
# Clone the repo
git clone https://github.com/<org>/setu-ksp-datathon.git
cd setu-ksp-datathon

# Install the Catalyst CLI
npm install -g zcatalyst-cli

# Log in and link the project
catalyst login
catalyst init

# Install frontend dependencies
cd client && npm install

# Install function dependencies (per function)
cd ../functions/queryFunction && pip install -r requirements.txt --break-system-packages
# repeat for each function in functions/
```

## Environment Configuration

Copy `.env.example` to `.env` in each relevant function directory and fill in:
```
BHASHINI_API_KEY=
SARVAM_API_KEY=
```
Catalyst-native services (Data Store, QuickML, Cache, Auth, Stratus) are configured through the Catalyst console, not environment variables — see `docs/DeploymentStrategy.md` §3.

## Running Locally

```bash
# Serve functions locally via Catalyst CLI
catalyst serve

# In a separate terminal, run the frontend
cd client && npm run dev
```

## Running Tests

```bash
# Backend / ML unit tests
pytest tests/unit

# Frontend tests
cd client && npm test

# AI evaluation harness (retrieval precision, bilingual accuracy, hallucination review)
python ml/eval/run_eval.py
```

## Deployment

```bash
catalyst deploy
```
Full deployment architecture and Catalyst service list in `docs/Deployment.md`.

## Project Documentation

The complete planning and design process — hackathon analysis, product research, architecture, engineering plan, and submission materials — lives in [`docs/`](./docs), generated phase by phase:

| Phase | Documents |
|---|---|
| 1. Hackathon Analysis | `HackathonAnalysis.md` |
| 2. Product Discovery | `Research.md`, `CompetitorAnalysis.md`, `ProductDiscovery.md` |
| 3. Product Definition | `PRD.md`, `ProductStrategy.md`, `Requirements.md`, `UserStories.md`, `FeaturePrioritization.md`, `Roadmap.md` |
| 4. Architecture | `Architecture.md`, `Design.md`, `AIArchitecture.md`, `Database.md`, `APISpec.md`, `Security.md`, `Deployment.md`, `UX.md` |
| 5. Engineering Plan | `FolderStructure.md`, `TechStack.md`, `CodingStandards.md`, `SprintPlan.md`, `TestingStrategy.md`, `DeploymentStrategy.md`, `MonitoringStrategy.md`, `RiskRegister.md` |
| 6. Submission | `PitchDeck.md`, `DemoScript.md`, `SubmissionAnswers.md` |

## Responsible AI

Predictive and pattern-detection features are deliberately grounded in modus-operandi and case-level evidence only — never demographic, caste, religion, or socio-economic proxies. This is enforced at the data-schema level (`docs/Database.md` §3), not just in application logic. See `docs/HackathonAnalysis.md` §9 for the full reasoning.

## Data

All data used in this prototype is synthetic. No real SCRB or individual data is represented. See `docs/Database.md` §5 for the generation methodology.

## Team

*[fill in team name and members]*

## License

*[fill in — MIT recommended for a hackathon submission unless the organizers specify otherwise]*
