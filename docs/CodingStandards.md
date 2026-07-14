# CodingStandards.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*Right-sized for a 4–5 person team on a 20-day build — enough to keep collaboration clean, not a large-org style guide nobody has time to follow.*

---

## 1. Python (backend Functions, ML)
- PEP 8, enforced via `ruff` or `flake8` in CI/pre-commit
- Type hints on all function signatures; `mypy` optional but encouraged for `functions/shared/`
- Docstrings on every public function: one-line summary + args/returns
- No bare `except:` — catch specific exceptions, especially around external calls (Bhashini/Sarvam/QuickML) so failures route into the fallback paths from `Design.md` §3, not silent crashes

## 2. TypeScript (frontend)
- ESLint + Prettier, strict mode enabled in `tsconfig.json`
- No `any` in committed code without an inline comment explaining why
- Component files colocated with their styles/tests

## 3. Naming Conventions
- Files: `snake_case.py`, `PascalCase.tsx` for components
- API routes: `/api/<resource>` (plural nouns), matching `APISpec.md`
- Data Store tables: `PascalCase` matching `Database.md`'s ER diagram exactly, so schema and code never drift apart under time pressure

## 4. Git Workflow
- `main` is always deployable
- Feature branches: `feature/<area>-<short-description>` (e.g., `feature/aiml-hybrid-retrieval`)
- Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`) — makes it fast to reconstruct what changed when writing the GitHub README and the "Additional Details" slide later
- At least one reviewer per PR, even under time pressure — a second pair of eyes on the RBAC/scope code in particular is non-negotiable given what it protects

## 5. Documentation-as-you-go
- Every Function includes a short `README.md` in its own folder: purpose, inputs/outputs, dependencies
- Any deviation from `Requirements.md` or `Database.md` (schema drift, dropped feature) gets a one-line note in `memory.md` the same day, not reconstructed from memory later

## 6. Responsible-AI Code Review Checklist (applies specifically to `ml/prediction_model/` and `functions/alertsFunction/`)
- [ ] No demographic/socio-economic field is referenced, even indirectly via a derived feature
- [ ] Every predictive output includes its MO/case-evidence basis
- [ ] No individual-level risk score is generated or stored anywhere

---

*Next: `SprintPlan.md`, `TestingStrategy.md`, `DeploymentStrategy.md`, `MonitoringStrategy.md`, `RiskRegister.md`.*
