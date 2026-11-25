# Phase D launch decision — 25 November 2026

**Owner direction:** Begin building the full integrated sports-equipment lifecycle application and only afterwards prepare/print QR codes. C4 controlled human trials are intentionally deferred; they must not be marked as completed or successful.

The system selected for *implementation* is the integrated digital lifecycle platform (Alternative C, with necessary physical processes). This is a **user-approved development choice**, not the evidence-based selection originally planned in C4.

Read `../../README.md`, `c4-approved-owner-decisions.md`, `c4-evidence-status.md`, the Phase B requirements and the top-level `../START_HERE.md` in the ZIP for context. The `START_HERE.md` resides outside the repo in the handoff bundle and should not be committed unless desired.

Priorities: inventory, item-/kit-level custody, role-based actions, returns, condition checks, maintenance, procurement and auditable transactions. Important guardrails: 24/7 access, not requiring guard inspections, safe conflict handling, no fictitious field measurements, match-day additional effort target <=60s, secure student data, economical QR labelling after end-to-end validation.

**Implementation update, 25 November 2026:** The full local Phase D application is now implemented in [`app/`](../../app/README.md). See [architecture](../implementation/phase-d-architecture.md) and [verification](../testing/phase-d-verification.md). Existing `prototypes/` remain earlier concept demos. Synthetic software tests do not change C4 field evidence or establish comparative effectiveness. Physical phone/label testing and live deployment checks remain pending.
