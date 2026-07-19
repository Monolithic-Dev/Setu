# 10_SCALABILITY_HARDENING.md — Agent Task: Prove Scalability, Don't Just Claim It

**Why this matters:** the Datathon's own "Objective" states participants should "build scalable solutions." `JudgeReview.md` §6 already flagged that your 20-day synthetic dataset won't stress-test what 1,100+ stations' worth of real data would do to retrieval latency. This task turns that from an acknowledged risk into a demonstrated result.

---

## Task 1 — Synthetic scale stress test

**Where:** `ml/data_generation/generate_dataset.py`, `ml/eval/`

1. Generate an artificially inflated corpus — 10x and 50x your current synthetic case count — using the same generation methodology (`Database.md` §5), varying MO/location/timing enough to keep clusters realistic rather than just duplicating rows.
2. Re-run retrieval latency benchmarks (`ml/eval/run_eval.py`) against each scale point: current size, 10x, 50x.
3. Plot latency (p50/p95) vs. corpus size — a simple line chart is enough.

**Why this specific test:** it directly answers the single scalability question a technical judge is most likely to ask ("what happens at real volume?") with a real number instead of an architecture diagram.

## Task 2 — Identify and document the actual bottleneck

TF-IDF/local retrieval typically degrades roughly linearly (or worse, depending on implementation) with corpus size, unlike a proper vector index. Be honest about this:
- If latency holds up fine at 50x, say so with the number.
- If it degrades meaningfully, document *why* (e.g., "TF-IDF vectorization is recomputed per query against the full corpus — a proper ANN/vector index, or QuickML's managed Knowledge Base once available, would remove this bottleneck") — this is a legitimate, sophisticated answer, not a confession of failure.

## Task 3 — One architectural mitigation, if time allows

Pick the cheapest of these that meaningfully helps, don't do all three:
- **Pre-computed TF-IDF index with incremental updates** instead of recomputing per query (likely the highest ROI, moderate effort).
- **District/station-level index partitioning** — since RBAC already scopes most queries to a station/district anyway, you may only ever need to search within a much smaller partition at query time. This is a strong, specific engineering insight: *"scalability and RBAC scoping compound in our favor — a station officer's query only ever searches their own partition."*
- **Simple caching of recent/frequent queries** at the Cache layer.

## Task 4 — Add a "Scalability" note to the deck with real numbers

Replace any hand-wavy "Catalyst scales automatically" language (`TechStack.md` §3 already partially does this) with the actual measured result from Task 1, plus the honest bottleneck explanation from Task 2, plus whatever mitigation from Task 3 was implemented.

## Acceptance criteria

- [ ] A real latency-vs-corpus-size chart exists, generated from an actual run, not estimated
- [ ] The bottleneck (if any) is named specifically, not vaguely gestured at
- [ ] At least one mitigation is either implemented or, if not, explicitly scoped as a clearly-planned next step with a real technical reason (e.g., "requires QuickML's managed vector index, tracked for the refinement window")
- [ ] `PitchDeck.md`'s scalability claims are backed by this data, not just architecture-diagram assertion
