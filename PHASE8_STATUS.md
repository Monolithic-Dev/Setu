# Phase 8 Scaffold — What's Real vs. What's Stubbed

This repo was scaffolded by Claude from the Phase 1–7 planning docs in `docs/`, built and tested in a sandboxed environment **with no network access** — meaning anything requiring a live API call (Catalyst Data Store, QuickML, Bhashini, Sarvam) could be written correctly but not executed against the real service. Being upfront about exactly what that means in practice, and — just as importantly — where a "no network" limitation stops being the explanation and something is a genuine bug instead.

## Actually built, run, and verified in this sandbox

- **`ml/data_generation/generate_dataset.py`** — runs end to end, generates a genuinely bilingual (Kannada text is real Kannada, not English dropped into a Kannada sentence) synthetic dataset, **plus Person/NetworkEdge records** (`--persons-out`) with real co-occurrence structure — 300 cases, 75 persons, 339 edges, one person linked across 15 cases.
- **`ml/prediction_model/hotspot_model.py`** — real DBSCAN clustering, produces coherent district/modus-operandi clusters.
- **`functions/shared/auth_middleware.py`** — RBAC + case-sensitivity gate, **8/8 unit tests**, plus a regression test for a subtle real finding: a restricted case is denied to a station officer even at their own station (initially mistaken for a bug, traced back to correct behavior).
- **`functions/shared/speech_adapter.py`** — provider fallback logic, **4/4 tests** (against fakes; real Bhashini/Sarvam need network + keys).
- **`functions/shared/grounding_verifier.py`** — the Phase 7 addition, **4/4 tests**, including one that catches an unsupported claim.
- **`functions/shared/retrieval/`** — real local dev-mode execution: `execute_structured_query_local` genuinely filters (and, after a fix, genuinely *ranks*) the real dataset; `LocalTfidfIndex` is a real scikit-learn TF-IDF search, not a stub.
- **`functions/shared/local_answer_synthesis.py`** — real extractive answer synthesis from retrieved records, standing in for the QuickML LLM call.
- **`functions/shared/local_audit_store.py`** — real append-only JSON persistence, standing in for the Data Store AUDIT_ENTRY table.
- **`functions/queryFunction/index.py`** — the full pipeline (language detection → hybrid retrieval → extractive generation → grounding verification → **real audit persistence**) runs genuinely end to end against real synthetic data.
- **`functions/alertsFunction/index.py`** — genuinely wired to the tested hotspot model, returns real clusters.
- **`functions/networkFunction/index.py`** — genuinely wired to the new synthetic network data; verified to return real multi-node graphs for connected persons, and to degrade cleanly (single-node graph, no crash) for an unknown entity.
- **`functions/auditFunction/index.py`** — genuinely reads real persisted audit entries; RBAC gate verified to allow SCRB Analyst/District SP/Admin and deny Station Officer; a full round-trip test proves queryFunction's writes and auditFunction's reads actually connect, not just that each half works in isolation.
- **`functions/exportFunction/index.py`** — real PDF generation via `reportlab`, verified by extracting text back out of the generated file, not just checking it exists. **English export is correct.** See the confirmed bug below for Kannada.
- **`ml/eval/`** — a real evaluation harness. 40 held-out questions generated from the real dataset. **Result: 100% recall, 57.5% top-3 precision.** The first run showed 0% and looked like a serious bug; traced it to structured search having no relevance ranking (fixed, re-measured); the remaining gap is genuine ties between cases sharing identical modus-operandi + district (a data-granularity limit, confirmed by hand-checking specific misses, not a retrieval failure).
- **Frontend TypeScript** — type-checked; the only remaining `tsc` errors are uninstalled packages (`npm install` resolves them), not logic errors. Two real bugs caught by actually trying to run things, not just reading code: a missing `vite-env.d.ts`, and `import.meta.env` itself being undefined outside a real Vite runtime (`queryClient.ts` now guards this with optional chaining). **`client/scripts/verify_ssr.tsx`** — a genuine runtime smoke test using globally-available `react`/`react-dom`/`tsx` (no `npm install` needed) — **actually run, 8/8 checks passed**: `App` and `ChatWindow` server-render without throwing in both languages, with real Kannada text confirmed in the output. `client/src/components/Chat/ChatWindow.test.tsx` is a proper Vitest test file written correctly for the team's real setup but **not run here** (`vitest`/`@testing-library/react` aren't available in this sandbox) — run it right after `npm install` to confirm. Also added `client/vite.config.ts`, which didn't exist at all despite `npm run dev`/`build`/`test` all depending on it.

**Total: 42/42 tests passing from a genuinely clean checkout.** `conftest.py` auto-generates the synthetic dataset, eval question set, and network data if they don't exist (all correctly gitignored as generated output) — this was added after a true clean-room extraction test failed with a raw `FileNotFoundError` before the fix existed. Run tests yourself: `python3 tests/run_tests_locally.py` (a local fallback runner, since this sandbox couldn't `pip install pytest` without network either — once you have network, `pytest tests/` works directly, everything here is ordinary pytest-compatible code).

## A confirmed bug, not a "needs network" limitation

**Kannada text in the PDF export currently renders as unreadable boxes**, not real characters — verified by generating an actual Kannada export and extracting its text back out (`tests/unit/test_export_function.py`). `reportlab`'s built-in Helvetica font has no Kannada glyphs, and no Kannada-capable font (e.g., Noto Sans Kannada) was available anywhere in this sandbox to register instead — only CJK and Latin fonts were present. This is a real, demo-blocking bug for a bilingual product, found and confirmed by actually testing it, not left as an assumption. Fix: download a Kannada Unicode TTF (network required) and register it via `reportlab.pdfmetrics.registerFont` in `functions/exportFunction/index.py`'s `generate_pdf_local`. The test documenting this (`test_kannada_export_is_currently_broken_pending_unicode_font`) is written to start *failing* once that fix lands — that's the intended signal to update it, not a bug in the test.

## Deliberately stubbed — needs your real Catalyst credentials, not more code review

Every one of these raises `NotImplementedError` on the *real* API path — and every one now has a genuine local dev-mode fallback that actually runs, so "stubbed" means "the live external call," not "untested code":

- `functions/shared/speech_adapter.py` — real Bhashini/Sarvam HTTP calls
- `functions/shared/retrieval/structured_search.py`'s `execute_zcql` — real ZCQL execution
- `functions/shared/retrieval/semantic_search.py`'s `query_knowledge_base` — real QuickML Knowledge Base call
- `functions/queryFunction/index.py`'s `generate_answer` — real QuickML LLM Serving call (will read as templated, not fluent, until wired in)
- `functions/networkFunction/index.py`'s `fetch_edges` — real Data Store query
- `functions/exportFunction/index.py` — real Stratus upload (PDF generation itself is real, see above)
- `functions/auditFunction/index.py`'s `fetch_audit_entries` — real Data Store query

## One thing flagged, not fixed, on purpose

`retrieve()`'s NL-to-filter extraction is still naive v1 (raw query text as a keyword filter, now with real ranking on top). Understanding "in the last month" as a date range, or "similar entry method" as an MO match, needs a real QuickML call to do properly — didn't fake that part without a real model to verify it against.

## Also worth knowing

- **`catalyst.json` is illustrative, not verified** — no network here to run `catalyst init` and confirm the current real schema. Regenerate it and treat that output as authoritative.
- The **Catalyst Advanced I/O Python function handler signature** is written as plain, framework-agnostic logic — correct internally, not yet wrapped in whatever exact entry-point convention `catalyst function:create` actually scaffolds.
- Kannada text in `generate_dataset.py` and `client/src/i18n/strings.ts` is machine-drafted — get it reviewed by a native speaker, same caveat as `docs/PRD.md`.
- Synthetic person names are deliberately generic IDs ("Person 0001"), not invented realistic names — this is graph-structure demo data, and fabricating culturally-specific names wasn't worth the risk of getting it wrong for data nobody needs to read as an actual name.

## Recommended first hour on this repo

1. `catalyst login && catalyst init` — get real credentials wired in, regenerate `catalyst.json`
2. Request QuickML Gen-AI early access if not already done (RiskRegister R1 — the top blocker since Phase 4)
3. `cd client && npm install` — resolves the `@types/react`/`vite` noise immediately
4. `pip install -r requirements-dev.txt --break-system-packages && python3 tests/run_tests_locally.py` — confirm all 42 Python tests still pass in your environment
5. `cd client && npm test` — run the real Vitest suite (`ChatWindow.test.tsx`) for the first time; it was written but not executable in the build sandbox
6. `cd ml/eval && python3 run_eval.py` — see the real dev-mode baseline (100% recall, 57.5% top-3 precision) yourself
7. Download a Noto Sans Kannada TTF and wire it into `exportFunction`'s PDF generation — the one confirmed bug, worth fixing before anyone rehearses a Kannada export
