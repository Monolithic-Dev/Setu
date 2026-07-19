# 12_CRITICAL_FIX_REVERT_DEMOGRAPHIC_FIELDS.md — Agent Task: URGENT, Do This First

**Severity: Highest priority in the entire project right now.** This overrides `07`–`11` until resolved.

---

## What happened

A recent change added "Age Bracket" and "Occupation" fields to the Analytics Dashboard, framed as a "safe" way to satisfy the official Challenge's "Socio-demographic insights" bullet. This is a real reversal of a deliberate, foundational, documented project decision:

- `Database.md` §3: *"the schema does not include demographic, caste, religion, or socio-economic classification fields anywhere they could feed the Prediction Service... This is a schema-level decision, not just an application-level filter, so it can't be quietly worked around later."*
- `CodingStandards.md` §6 checklist: *"No demographic/socio-economic field is referenced, even indirectly via a derived feature."*
- `AIArchitecture.md` §4: identity-proxy fields are permanently excluded, "not just by policy... enforced at the data-access layer."

**Age bracket and occupation are demographic/socio-economic fields.** They are not a "safer" substitute for caste/religion — they are the same category of risk (identity/circumstance proxy) with different labels, and combined with location and case outcomes they can encode exactly the kind of discriminatory pattern the schema exclusion was designed to prevent.

## Required fix

1. **Remove `age_bracket` and `occupation`** (or any equivalent fields) from `PERSON`, `CASE_RECORD`, and `catalyst_schema.json` entirely.
2. **Remove the corresponding dashboard panel/visualization** in `Dashboard.tsx` that surfaces these as "insights."
3. **Check the Prediction Service's Data Store scope** (`hotspot_model.py`, `alertsFunction`) to confirm neither field was also wired into the hotspot/pattern model — if it was, that's an FR-5.2 violation, not just a dashboard issue.
4. **Check the synthetic data generator** (`ml/data_generation/generate_dataset.py`) — if it was updated to generate these fields, revert that too, so they don't silently reappear in a future data refresh.
5. **Replace the dashboard content** with the aggregate-only framing already correct elsewhere in the project: crime density by zone, trend by time period, MO-type distribution — nothing tied to an individual's identity or personal circumstances.
6. **Use `09_RESPONSIBLE_AI_POSITIONING.md`'s prepared answer** for the "socio-demographic insights" bullet instead of a literal feature. That answer is genuinely stronger for a government-adoption pitch than this implementation was.

## Process fix (so this doesn't happen again)

- Any PR touching `PERSON`, `CASE_RECORD`, `ml/prediction_model/`, or `functions/alertsFunction/` **must** have the `CodingStandards.md` §6 checklist run against it by a human reviewer before merge — not just by whichever agent wrote the change. This is exactly the review step that would have caught this before it shipped.
- If an agent is asked to "fully implement every official feature bullet," it needs an explicit instruction not to override responsible-AI schema exclusions to do so literally — add this as a standing constraint in `.agents/AGENTS.md` if that file governs agent behavior in this repo.

## Acceptance criteria

- [ ] `age_bracket` / `occupation` (or equivalents) removed from schema, dashboard, data generator, and prediction model — grep the whole repo for these field names to confirm nothing was missed
- [ ] Dashboard's socio-demographic panel replaced with aggregate-only content
- [ ] `CodingStandards.md` §6 checklist re-run and passing
- [ ] `Datathon_Implemented_Features.md` and the compliance doc updated to reflect the corrected, honest scope
- [ ] `.agents/AGENTS.md` (or equivalent) updated with an explicit standing rule: literal feature-checklist completion never overrides a documented responsible-AI exclusion
