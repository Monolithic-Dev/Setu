# MonitoringStrategy.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

---

## 1. What Gets Monitored

| Signal | Why it matters | Source |
|---|---|---|
| Function error rate by endpoint | Catches breakage before a demo does | Catalyst APM |
| Latency (p50/p95) per endpoint | Directly tied to NFR-5 — "usable mid-investigation" is a latency claim, not just a feature claim | Catalyst APM |
| RBAC denial rate | A spike could mean a bug (legitimate users wrongly denied) or someone probing scope boundaries — either way, worth knowing immediately | Auth/RBAC Service logs |
| Retrieval confidence / "not found" rate | A rising "not found" rate suggests the Knowledge Base or synthetic dataset has gaps worth patching before the finale | Retrieval Service logs |
| Bhashini/Sarvam service health | External dependency — if it degrades, we want to know before an officer (or a judge) does | Adapter-level health checks |
| QuickML usage/rate limits | Still early-access as of this writing — worth watching in case limits are tighter than expected | Catalyst console / QuickML dashboard |
| Audit log completeness | Every query should produce exactly one audit entry — a gap here undermines the explainability claim the whole pitch rests on | Reconciliation check: query count vs. audit entry count |
| **Geographic concentration of hotspot flags** *(added Phase 7 review)* | Input-side exclusion of demographic fields doesn't guarantee bias-free outputs, since location can itself be a proxy (`AIArchitecture.md` §4) — this needs outcome-level checking, not just clean-input design | Periodic comparison of flagged-area distribution against independent crime indicators, not just internal consistency |
| **User-flagged answers ("was this helpful?")** *(added Phase 7 review, FR-10.2)* | Surfaces real quality issues an automated eval set won't catch | Flagged-answer log, reviewed separately from ordinary audit entries |

---

## 2. Dashboards (lightweight, not enterprise-scale)

A single internal dashboard (can be a simple page reading from Catalyst APM + a few custom counters) showing: current error rate, p95 latency, today's query volume by language, and RBAC denial count. Enough for a small team to glance at before a demo, not a full observability platform this project doesn't need yet.

## 3. Alerting

Given team size and timeline, real-time paging isn't necessary — but a daily check-in on the dashboard above during Week 3 specifically (when regressions are most costly) is a firm recommendation, not optional polish.

## 4. Post-Submission Monitoring (shortlist → finale)

If shortlisted, monitoring matters more, not less — the Aug refinement window and the live Grand Finale demo are exactly where an unnoticed regression would be most damaging. Carry the same dashboard forward and add: multi-agent orchestration health (once Concept C work begins) and rehearsal-specific latency checks in the days before 26 Sep.

---

*Next: `RiskRegister.md`.*
