# B3 — Executive Summary for Instructor Review

**Status:** Analytical/sensitivity work only. **Not** a field-measured improvement.

| Transformer | What was transformed? | Explicit mathematical operation | Insight | Design decision to test |
| --- | --- | --- | --- | --- |
| **Decompose** (primary) | “Borrow sports equipment” split into key access, item withdrawal, transfer, return, inspection, and repair | \(T= T_{walking}+T_{guard}+T_{other}\); ~300 s ≈ 120 + 120 + 60 s (recalled/derived only) | Recording a room key does not verify item custody or condition; optimizing retrieval speed is not yet justified | Low-effort item or kit-level event confirmation, separated from room access |
| **Aggregate** (primary) | Fragmented physical stock into reconciled mutually exclusive administrative categories | \(N_{total}=N_{available}+N_{issued}+N_{inspection}+N_{quarantine}+N_{repair}+N_{unknown}+N_{retired}\) | An accurate usable count cannot be reconstructed from declarations and purchase bills alone | Durable item IDs, consumable quantity lots, quarantine, kit manifest and auditable reconciliation |
| Normalize (support) | Raw discrepancies into comparable inventory-normalized measures | \(A_{strict}=N_{3\ confirmed}/N_{audited}\) alongside assessability and conditional correctness | Missing records and inaccurate records are distinct | Report numerators/denominators, item-level audit timestamp and unknowns |
| Perturb (support) | Vary transfer recording probability and burden under **synthetic assumptions** | \(P_{all\ records}=p_i p_t^k p_l p_c\); \(W=N\,\Delta t/60\) min/week | Repeated transfers create recording opportunities; adding steps creates administrative friction | Test rapid kit-level/group-level flows and avoid designs that encourage bypass |

## Demo-worthy but clearly synthetic sensitivity

Assume an initial issue record is captured with 95% probability, any transfer with 80%, and location and condition records with 90% each, independently. The model gives 76.95% record-chain completeness with 0 transfers vs ~39.40% with 3 transfers. **These numbers describe toy assumptions only**, not Alaknanda's real accuracy or the predicted effectiveness of a QR system.

## What the user has actually provided

Secretary-described process, one missing badminton racket case, delayed damage discovery, informal sharing and match-day kit exceptions, ~5-minute end-to-end equipment journey, ~3–7-day typical repair recollection, and sport-use cadence. There is **no independently verified inventory audit, no current accountability percentage and no intervention trial**.

## Why this is a first-principles project, not simply an app

We identified which physical events matter for accountability, established a stock-conservation identity, specified a valid objective metric and exposed the record-completeness versus effort trade-off. The platform is **one candidate reconstruction** to compare against a physical/process-only approach in Phase C; its benefit is not presumed.

## Test required before presenting a measured result

Permissioned item sample with independent location/custody/condition checks, controlled transfer/return tasks with actual elapsed time, and a comparison of alternative record systems. See [validation plan](b3-validation-protocol.md).
