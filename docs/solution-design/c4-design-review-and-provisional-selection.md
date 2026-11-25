# C4 — Design review and provisional selection status

**Decision: NO WINNER SELECTED.** The C3 proofs of concept demonstrate limited code paths using fictitious assets; the C2/C4 comparison plan is not field-executed. A feature-rich prototype is not evidence of better accountability, faster borrowing or fewer damages at Alaknanda.

## What can be stated from design architecture
| Alternative | Plausible benefit to validate | Key limitation / risk to validate | Where it might win |
| --- | --- | --- | --- |
| A — physical/procedural | Low upfront cost, naturally offline, visible storage and paper manifests | Unverified handovers, paper errors, poor distributed visibility, effort to reconcile | Small inventory, no reliable devices/network, low borrowing volume |
| B — lightweight QR/register | Timestamped item events and quick lookups with relatively low complexity | Scan noncompliance, permission/privacy design, stale state if offline, cost of supervision | Moderate usage where item traceability matters more than full lifecycle automation |
| C — integrated lifecycle | Controlled kit, repairs, roles, audits and procurement linked to item states | Greater training, technical complexity, maintenance cost, integration/deployment burden | Multiple hostels or complex stock/repair flows **if** user testing supports the extra cost |

## Existing code-level evidence (not comparative performance)
- C3 reference engine and unit tests must be rerun and recorded for the current package version.
- The 12 scenarios are grouped into 36 concept probes; the C3 code notes indicate **24 implemented-logic paths and 12 design-only paths**. This is a coverage indicator, **not** 24 successful participant trials.
- A/B and C prototypes differ in implemented depth, so simply counting code paths cannot compare user performance.
- The eight C2 hard gates, independent physical verification, trial times, human usability and annualized costs remain open.

## Evidence required to recommend one reconstruction
1. Permissioned, counterbalanced real participant tasks with independent physical audits for the same cases and comparable props.
2. A candidate-by-gate outcome including proof references, not assumptions.
3. Role-level effort and match-day overhead, particularly guard and captain workload.
4. Item-status accuracy, failure handling, and ongoing operational cost.
5. Approval of criterion weights and hard thresholds by the project owner.

Until then, **all three candidates remain under consideration**; retain all original prototypes for reproducibility and do not present a synthetic weighted-ranking chart in the final academic submission.
