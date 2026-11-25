# C1-C — Integrated Equipment Lifecycle Platform + Physical Process

**Design maturity:** System architecture and UI concept only; not a built working application, approved spending mechanism or measured pilot.

## What we build at full implementation (Phase D, if selected)

A role-restricted, multi-module platform connecting controlled inventory registration, requests, physical handover, responsible party, returns, damage inspection, external repairs, procurement, stock audits, analytics and multi-facility compatibility. Labelled racks, item tags and operational procedures remain necessary.

## Product modules and core workflows

| Module | Intent and workflow | Critical boundary |
| --- | --- | --- |
| Student catalog | Search **recorded** availability, request item/kit, see approved/pending/current borrowings | Request or reservation never changes physical custody |
| Access/key log | Guard signs out/receives room key separately | Key event never asserts item issue/return |
| Asset registry | IDs, photos, sport/type, physical location, condition, source/time | Model/type is not unique item; unknown remains visible |
| Custody and issue | Approved choice → actual pickup confirmation → atomic custody transition → receipt | Cannot double-issue same unique item |
| Kits/tournaments | Pre-authorize captain/kit → fast group checkout → component-level end reconciliation | One kit does not double count its items; no every-player scanning |
| Returns and inspection | Return declaration → actual component receipt → condition assessment → available/quarantine/unknown | Key return ≠ returned item; repair ≠ verified usable |
| Damage/maintenance | Report discovery, block verified availability if risk, secretary assessment, approval/vendor events, repair, receipt and inspection | Occurrence time and damage culprit unknown until independently supported |
| Procurement/retirement | Demand evidence, quotes, office approvals, actual payment provenance, physical receipt and enrollment, authorized retirement | Configurable reported threshold; never auto-pay/approve |
| Inventory audit | Independent snapshot, triad correctness, unknown and contradiction flags, corrections preserved | App status cannot substitute for audit |
| Analytics | Strict audited accountability n/N and secondary denominators; repair stages, category utilization, compliance, costs | No baseline effectiveness claim without real samples |

## Interface architecture

1. **Student mobile:** Browse, Request, My Gear, Report Damage. Explicit last-verified note and expected pickup process.
2. **Captain fast lane:** Upcoming approved kit, one QR / manifest acknowledgement, return and exception list, quick team handover.
3. **Guard micro-interface:** Key sign-out and key return only, optionally status of room availability; not required to inspect asset condition.
4. **Secretary dashboard:** Current inventory, unresolved custody, quarantine/repairs, kit exceptions, purchase approval status, item audits and decision history.
5. **Maintenance workbench:** Stage-based work orders, vendor receipt, milestone documents and reinspection.
6. **Office/admin oversight:** Budget evidence, approval documents, permission changes and aggregate metrics, with least-privilege access.

Review [illustrative interface gallery](../../prototypes/c1/concept-gallery.html), not a functional deployment.

## System architecture candidate

- Responsive frontend, transaction-safe API, relational database, access-controlled private documents; separate per-facility records if expanded.
- Distinct `KeySession`, `Asset`, `ConsumableLot`, `KitManifest`, `Request`, `PhysicalHandover`, `CustodyAssignment`, `ConditionInspection`, `MaintenanceCase`, `ProcurementCase`, `InventoryEvent`, `AuditSnapshot`, `Correction`, `UserRole`.
- Server rejects double-confirmed issue; constraints on exclusive derived operational state; all state corrections have reason/time/actor.
- Authorization for secretary retirement and office finance; user-facing views minimize personal data.
- Offline requests retain event IDs, causal ordering and `pending conflict review`; never silently merge impossible simultaneous handovers.
- Policy configuration for loan durations, kit rules, audit frequency and reported office spending threshold (not assumed official).

## Example of event logic

`Request created` → `Approved` → **physical pickup confirmed** → `Issued to student/team` → `reported return` → `physically checked` → `inspection pending` → `verified usable` OR `quarantined` → `repair + vendor handoff` → `reinspection` → `verified usable` OR `retired`.

**Note:** Not every request must be approved by secretary; routine authorization must allow 24/7 access. Approved roles and who verifies physically are Phase C decisions.

## Risks to test

- More interfaces and mandatory workflow steps may reduce compliance; costly to build/maintain.
- Device, internet, label damage and staff training barriers.
- Comprehensive event log still may be inaccurate if people fail to report physical movements; cannot infer accountability solely from software completion.
- Financial workflow and borrowed equipment records require permission/privacy safeguards.
- Integrated platform is **not selected** until C2 comparative testing supports it versus A/B and possible hybrids.
