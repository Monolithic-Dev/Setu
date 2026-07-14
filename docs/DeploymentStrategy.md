# DeploymentStrategy.md

**Phase 5 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*This is the process/practice companion to Phase 4's `Deployment.md`, which covers the architecture. This one covers how the team actually ships changes day to day.*

---

## 1. Environments

- **Development** — Catalyst Dev environment, continuous deploys from feature branches for individual testing
- **Production** — Catalyst Production environment (the one submitted as the "Prototype Deployed Link"), promoted only after passing integration testing on Dev

No separate staging environment for this timeline — Dev doubles as the pre-production gate, with a full rehearsal on Production specifically scheduled for the Week 3 buffer day (`SprintPlan.md` Day 19).

## 2. Release Process

1. Feature branch → PR → at least one review → merge to `main`
2. `main` auto-deploys to Dev via Catalyst CLI
3. Manual promotion to Production after: (a) integration tests pass, (b) the person promoting has personally clicked through the main flow on Dev first
4. Tag each Production promotion (`v0.1`, `v0.2`, …) so it's clear which version was live during any given rehearsal or the actual Grand Finale demo

## 3. Secrets & Configuration

- API keys (Bhashini/Sarvam) stored in Catalyst's environment configuration, never committed to the repo
- `.env.example` committed so setup instructions in the README are accurate and complete (a submission requirement)

## 4. Rollback Plan

- Keep the last known-good Production tag deployable within minutes — if a Week 3 change breaks something close to the deadline, roll back rather than debug live
- The internal 24–25 Jul buffer (`Roadmap.md`) exists specifically so a rollback decision on Day 19 doesn't threaten the actual Day 20 submission

## 5. Submission-Specific Checklist (run this exact list before clicking submit)

- [ ] Deployed link loads on a fresh, logged-out browser session
- [ ] GitHub repo is public (not just "unlisted") and README setup steps work on a clean machine
- [ ] Demo video link is public/accessible without sign-in
- [ ] Prototype Deck PDF built from the official template, under 5MB
- [ ] Prototype Brief is within the 1024-character limit (copy-paste it into a character counter, don't estimate)
- [ ] Correct Challenge selected in the submission form

---

*Next: `MonitoringStrategy.md`, `RiskRegister.md`.*
