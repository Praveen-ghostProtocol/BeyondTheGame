# C1-B — Lightweight QR/Form + Physical Controls

**Design maturity:** Browser/forms concept, not a deployed service; no backend/QR labels operational yet.

## What we build

1. Simple item and kit IDs/QR labels on durable assets and storage locations; consumables entered by lot quantity.
2. A **mobile-friendly scan/form journey**: choose item or kit, choose actual *collect / return / damage / off-ground transfer / census adjustment* event, submit with minimal inputs; separate from current guard key record.
3. One shared availability/status view showing last reported location, accountable entity, condition and *last verification source/time*; explicit `unknown`, `pending reconciliation`, `quarantine` states rather than false precision.
4. A captain **kit QR fast lane**: pre-approved roster or kit; one scan for pre-identified manifest at pickup, reconcile components on return, flag omissions.
5. A damage form with optional photograph, event time of *discovery*, secretary notification, and separate repair-stage fields. No student blame inference.
6. Procurement summary with existing office workflow fields, quote links, receipt acknowledgment and physical count. No automated money disbursement.
7. Basic audit export/print sheet for physical checking; append-only event history with corrected entries (not overwriting original claim).
8. A **paper fallback** when phones, QR or network fail, followed by reviewed reconciliation and collision resolution.

## Workflow

**Normal:** Guard logs key separately → student scans durable item or kit QR at physical collection → selects issue / responsible student or team → confirms actual pickup → shared ledger updated on server → at return scans item and condition report → status is `reported returned` or `inspection pending` until independently checked. A missing item stays unresolved even when key is returned.

**Sharing:** On-ground touch remains covered by team custody. For off-ground transfer, scan and acknowledge new responsible party; unconfirmed transfer shows pending, not automatically transferred. No compulsory scanning for each teammate.

**Damage:** Scan/identify item or choose unknown item → submit description and discovery timestamp → mark possibly unusable, request secretary assessment and physical red tag → repair milestones → check → restore/quarantine.

**Procurement:** Secretary registers need and office approval evidence; receiving physical count creates new item ID/lot entry; invoices alone do not mark usable stock.

## Interface concepts

- *Student mobile:* search or scan; three primary actions (Borrow, Return, Report Damage), simple kit selection and previous loans.
- *Secretary mobile/desktop:* pending damage, unmatched returns, repair milestones, procurement receipts, inventory audit list.
- *Guard:* no new mandatory equipment UI; key book remains.
- *Auditor:* per-item triad assessment via separate physical checklist.

See [click-through visual concept gallery](../../prototypes/c1/concept-gallery.html).

## Information model (minimum)

`Asset(id, category, location, condition, evidence_source, verified_at)`; `Lot(id, sku, quantity)`; `Kit(id, manifest)`; `Event(id, type, item_or_kit, actor_ref_private, responsible_entity, timestamp, source, confidence, correction_of)`; `RepairCase(...)`; `PurchaseCase(...)`; `AuditSnapshot(...)`. Actual borrower identifiers must be protected outside the public repo.

## Limitations to evaluate

- QR scan is a self-reported physical event unless a separate physical check confirms it.
- Two simultaneous offline borrowers may conflict; future pilot needs explicit **pending reconciliation**, never naive last-write-wins.
- Phone access, connectivity, labels and update discipline can burden students.
- A form cannot physically prevent a student from taking an extra unrecorded item.
- Approval and actual physical pickup are distinct.

## C1 prototype

The [concept gallery](../../prototypes/c1/concept-gallery.html) visualizes the intended phone form and status view; interactions are screen walkthroughs on **invented demonstration labels only**, not authenticated, persistent transactions. C2 must test this against physical-only and integrated alternatives with matched tasks.
