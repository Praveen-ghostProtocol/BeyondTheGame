# C1-A — Physical + Procedural Reconstruction

**Design maturity:** Paper-control proposal. No live deployment or measured benefit.

## What we build

1. Durable equipment tags using stable item IDs (e.g., `BAT-001`); location labels on racks; identifiable kit IDs and a printed kit manifest. No QR/phone requirement.
2. A **short handover ledger** recording item/kit, timestamp, accountable student or team (private operational record), actual collection declaration, and optional verifying witness. The current guard key/ID register stays separate.
3. A **return reconciliation slip** listing actually seen item IDs, missing components, condition: usable / damaged / unknown, with checker/time; if no physical check occurs, write *reported only*.
4. A **red quarantine tag and designated damaged-equipment shelf**. Student can flag an item; secretary or authorized delegate assesses it, not the guard.
5. A **maintenance board** with case ID, discovery, assessment, approval, shop possession, return, condition check and resolution.
6. **Procurement folder + paper receiving register**: proposed need, quotation evidence, office approval, payment/reimbursement, delivered item IDs, discrepancy and retirement reason.
7. **Periodic inventory audit sheet** separately records location, accountable entity and condition with date and source. No audit score can be inferred from paper ledger alone.
8. Explicit **manual exception log** for late returns, key/item mismatch, conflicting handovers and unidentified items.

## Normal issue/return workflow

`Guard receives ID / issues key` → *student identifies unique item or team kit* → `student makes short custody entry at equipment room` → `takes items` → `returns items` → `returner and checker compare item IDs/kit manifest where feasible` → `mark reported or verified return + condition or unknown` → `guard closes key session independently`.

**Key compromise:** No guard inspection is assumed. If no trustworthy verification/check is feasible during self-service at night, paper entries remain *self-reported*, and independent spot audits reveal record drift.

## Transfer/tournament

- Teammates sharing on the ground stay under one recorded **team/captain responsibility**; no every-touch entry.
- Off-ground change of responsible party uses a short dated transfer slip; if skipped, custody is **unresolved**, not falsely reassigned.
- Captain pre-books/pre-fills kit manifest; one team issue, then component-level return reconciliation after match. Existing secretary special-permission behavior is replaced only in a pilot with approval.

## Damage/maintenance and procurement

- Damaged item gets red tag and quarantined rack. Actual time of damage may be unknown; record only discovery time.
- Secretary may authorize discard; external shop repair requires recording departure, shop, receipt and reinspection. Shop repair does not equal return-to-service verification.
- Office procurement rules remain independent of a ledger; reports describe the secretary-reported under/over ₹10,000 workflows without treating them as formally verified policy.
- Physical receiving count verifies delivered equipment rather than converting invoices directly into usable stock.

## Human roles, interface, data

| Role | Physical touchpoint | Responsibility |
| --- | --- | --- |
| Student | Item tags, short paper issue and return slips | Declare actual physical movement; report mismatch |
| Guard | Existing ID/key register | Control access, **not** verify all sports assets |
| Captain | Pre-printed kit manifest | Accept team-level custody; account for kit components on return |
| Secretary | Inventory/repair/procurement board | Condition decisions, maintenance, purchasing and retirement |
| Shop/office | Purchase/repair evidence kept with secretary | External milestones and approvals, no software-induced authority |
| Auditor | Independent dated stock sheet | Compare recorded location/custody/condition to ground truth |

## Risks and testable limitations

- Paper compliance may fall during busy periods; photocopying and audit search are slow.
- If a student skips item recording, the system **does not know** what was physically taken.
- Public rack status can become stale, even when all forms look complete.
- A paper ledger may record two incompatible checkouts before reconciliation; must provide conflict log and physical audit, but cannot guarantee prevention.
- Some late-night handovers will remain self-attested; strict triad accountability must be independently audited.
- No actual effectiveness claim until matched task trials and audit.

## Minimum C1 prototype

[Print-ready kit and item forms](../../prototypes/c1/a-physical-forms.html). Print with fabricated blank records; enact 8+ B4 scenarios on a table. Capture the number of writing steps and seconds per actor during C2, not now.
