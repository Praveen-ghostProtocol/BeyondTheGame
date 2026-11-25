# C1 — Alternative Solution Development (not a selection)

**Source of truth:** [B4 requirements specification](../first-principles/b4-requirements-specification.md), [B4 requirement register](../first-principles/b4-requirements-register.csv), [B4 acceptance catalog](../first-principles/b4-acceptance-tests.csv), [A2 current-state maps](../research/phase-a/a2-current-state-process-maps.md). **Status:** Three designed concepts and low-fidelity prototype artifacts, **not field-tested, deployed, user-approved, or ranked**.

## 1. Problem and design goal

Alaknanda Hostel (~400 residents, reported) uses a guard-held key and ID-card/paper-register process. A student declares intended gear, collects items themselves, may pass gear to someone else, then returns the key; the equipment's physical custody, return and condition are not independently verified. The sports secretary handles buying, repair and replacement, not ordinary issuing. Tournament captains sometimes use approved fast-path borrowing without register entries. Equipment is generally easy to find; do **not** invent a retrieval-delay crisis. The cost/need of more recording must be explicitly tested.

**Approved primary outcome:** Strict verified accountability of individually trackable durable equipment at a fixed-time independent audit: fraction of eligible audited items for which recorded **location, accountable entity and condition** all match the physical truth. No baseline % has been measured. Supplementary: assessability, request fulfilment, elapsed time and staff burden, unusable share, repair lead time, kit reconciliation, operating cost. Consumables use lot quantities rather than item-level KPI.

## 2. Design constraints carried from B4

- Room-key custody and physical item custody are different events; room access remains possible 24/7 without sports secretary presence.
- Ordinary on-ground teammate sharing should remain low-friction; off-ground handovers need an accountable *option*, not mandatory scans on every touch. Operational custody is **not proof of damage culpability**.
- Captains must be able to take kit quickly for a match; use pre-authorization or a manifest.
- Guard remains key/register operator, not automatic condition-inspection or equipment-counting staff.
- No item becomes `verified usable` solely because a key was returned, a borrower said so, or an external repair finished.
- Individually identifiable durable assets versus quantity-accounted consumables; kit container does not double-count component assets.
- No automatic fines, theft inference, money transfer, financial-policy override, or unverified hardcoded purchasing threshold. Reported ₹10,000 branch is configurable, pending office confirmation.
- Avoid personally identifying records in this **public** research repo. Any future live system must place sensitive data in private access-controlled storage.

## 3. Three distinct solution families

| | A: Physical and procedural | B: Lightweight digital + physical | C: Integrated lifecycle platform + physical |
|---|---|---|---|
| Core idea | Item tags, simplified issue/kit cards, physical quarantine shelf, repair board, physical audit | Item/kit QR tags linked to short mobile issue/return forms, lightweight availability ledger and repair log, manual fallback | Role-based integrated catalog, requests, transactional issue/return, item state engine, maintenance, procurement and audit dashboard |
| Main user interface | Paper book, tag board and labeled shelves | Scan-to-form, simple asset list and offline reconciliation card | Student / guard / secretary / maintenance / admin portals |
| Operational data | On-site paper record, dated audits | Central event table and current state derived from events | Relational assets, lots, kits, transactions, workflow and authorization tables |
| Guard duty | Key custody only | Key custody only; optional short check-out if the policy allows | Key custody only; guard portal limited to access events |
| Main risk | Missing or delayed manual updates; inaccessible history | Scan friction, phone/network availability, incorrect self-report | Software/training/operational complexity, stale physical truth despite digital sophistication |
| Prototype | [Printable paper controls](../../prototypes/c1/a-physical-forms.html) | [Interactive concept gallery](../../prototypes/c1/concept-gallery.html) | [Interactive concept gallery](../../prototypes/c1/concept-gallery.html) |

Read the [full A](c1-alternative-a-physical.md), [B](c1-alternative-b-lightweight.md), and [C](c1-alternative-c-integrated.md) specifications. **None is assumed to win.** Real costs, guard/user effort and accountability results are unknown.

## 4. Shared domain terms for fair comparison

- **Key session:** a record of permission to access room/key; can overlap with other entrants. Not an equipment loan.
- **Durable item:** unique identity, physical location, operational responsible party/team, condition, event source and verification confidence.
- **Consumable lot:** SKU and quantity; cannot be counted as individually triad-auditable assets.
- **Kit:** manifest with linked item IDs and lot quantities; one kit checkout with component reconciliation.
- **Item movement:** permission/request vs actual pickup vs handover vs report of return vs verified return.
- **Condition state:** verified usable, damaged/quarantined, inspection pending, repair, retired, or unknown; unknown is not falsely claimed usable.
- **Record credibility:** self-reported, staff-confirmed, physically audited, inferred/stale; source/time retained.
- **Exception:** missing, disputed, offline conflict, identity unknown, partial kit return; never silently resolved.

## 5. Full-lifecycle coverage

Every concept has a design for: 24/7 access; ordinary checkout; overlap with an existing key session; on-ground sharing and off-ground transfer; team-kit pre-approval and quick issue; partial return; condition report and quarantine; repair vendor handoff and return inspection; procurement quotes/approval, physical receipt and retirement; missing/disputed gear; audit; privacy, offline recovery and operator training. Methods and cost differ rather than capability being invented to make alternatives identical.

Cross-reference [40-requirement design mapping](c1-requirements-coverage.csv) and [32 B4 scenarios](c1-scenario-design-matrix.csv). The mapping is **proposed mechanism**, not acceptance-test pass status.

## 6. Transformer-to-concept traceability

| Transformer | B3 design insight | A | B | C |
|---|---|---|---|---|
| Decompose | Key, physical issue, transfer, return and condition cannot be one event | Separate columns/cards at handover, discrepancy and condition | Distinct scan/form event types | Transactional state-specific actions and history |
| Aggregate | Active, damaged, issued, unknown and retired counts must reconcile | Countable rack/board and periodic inventory audit | Per-item state ledger and count view | Database constraints plus reconciliation/audits |
| Normalize | Accountability requires independent item snapshot, eligibility and uncertainty | Paper stratified audit sheet | Exportable anonymous audit sheet | Auditable dashboard preserving all denominators |
| Perturb | More logging may reduce compliance or slow matches | Team cards, off-ground handover slip | Group QR checkout; offline card | Pre-approved kit fast lane, queued/conflicted updates |

## 7. What C1 can and cannot establish

**Can establish:** credible alternative architectures, feasible interactions, equipment data needed, testable differences and required physical procedures. **Cannot establish:** actual improvement, baseline, superiority, service-time target, adopted security policy or staff consent. The printable and browser prototypes are fictional design representations, not pilots. The next phase is [C2 comparison protocol](c1-c2-handoff.md); comparison scoring weights and workflow responsibility choices require user approval before actual trials.
