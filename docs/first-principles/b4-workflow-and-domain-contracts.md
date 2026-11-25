# B4 — Domain, Event, and Workflow Contracts (Technology Neutral)

**Status:** Candidate semantics for Phase C prototype comparison; not current hostel policy. Grounded in [B1](b1-state-and-custody-model.md), [B2](b2-causal-analysis.md), [B3](b3-transformer-analysis.md) and [A2 reported workflow](../research/phase-a/a2-current-state-process-maps.md).

## 1. Independent entities

| Entity | Meaning | Non-negotiable modeling distinction |
| --- | --- | --- |
| Access session | A key signed out by a resident, held by guard against an ID, and returned | Does **not** prove any physical equipment left/returned |
| Physical durable asset | One rack, bat, ball, helmet, etc., where individual tracking is proportionate | Model/type is not the same as its individual identity |
| Consumable stock lot | Category/unit/count of fungible items | Quantity management rather than one scan per shuttlecock |
| Kit/bundle | Package containing durable assets and/or stock quantities | Component reconciliation can be incomplete even if kit bag returned |
| Accountable party | Borrowing student, team, captain, hostel store, shop, or explicitly unknown | Accountability is operational custody, **not proof of damage blame** |
| Handover / event | Physically verified issue, return, off-ground transfer, inventory correction, etc. | Request and permission are not physical movement |
| Condition assessment | Current best-supported usability classification | Discovery time may differ from unknown damage occurrence time |
| Maintenance case | Discovery, approval, vendor movement, repair, restoration/discard | Repair completion alone does not certify condition |
| Procurement case | Need, quotes, approval, payment, receipt and new stock | Bills ≠ live usable inventory |

## 2. Three independent item-state attributes plus confidence

For an eligible durable item at time *t*, record `location`, `accountable_entity`, `condition`, **and** source/verification timestamp/confidence.

- **Location:** storage / with team or student / sports ground / at shop / other / unknown (examples, not fixed enum).
- **Custody:** facility / student / team/captain / vendor / unknown.
- **Condition:** verified usable / damaged or quarantine / inspection pending / undergoing repair / retired / unknown.
- **Confidence:** independently verified / reported / inferred / stale or unknown. The B4 KPI must not treat self-declared data as independently verified.

**Operational availability** (`available`, `issued`, `inspection pending`, `quarantine`, `repair`, `unknown`, `retired`) is a derived, mutually exclusive stock classification, not the same as either physical location or condition. These categories need controlled transitions and must sum to the physical census when an audit has resolved any unknowns.

## 3. Candidate workflow: ordinary borrowing

1. Resident seeks a suitable item. Existing key/access procedure remains separate and usable 24/7.
2. A request or permission may be expressed without recording physical handover.
3. Responsible party and actual individual asset/lot/kit are identified at a proportionate handover point; if unverified, status remains flagged.
4. Handover event produces a responsible party, timestamp and item or manifest reference.
5. Subsequent on-ground sharing may remain under team-level responsibility; off-ground transfer mechanisms are to be experimentally compared in Phase C.
6. A physical return records what was actually received, not just a returned key or verbal statement.
7. Condition follows risk-proportionate assessment and if uncertain is clearly labelled, not automatically claimed as verified usable.

**Forbidden conclusion:** If Student A signs for a key and Student B later holds a bat, a register alone cannot establish that A damaged or lost the bat.

## 4. Candidate workflow: captain / tournament kit

1. Captain has defined permission for a kit; pre-authorization may be done before the match.
2. At collection, an appropriate level of component / manifest verification occurs **without an onerous match-day process**.
3. Record responsible captain or team rather than treating every player touch as a new loan.
4. After the event, reconcile kit content and condition; unresolved items remain flagged.

**Unknowns to decide in C:** Acceptable checkout seconds, which kit categories need per-component verification, and whether team responsibility changes when a component leaves the match group.

## 5. Candidate workflow: damaged item

1. A user, guard or secretary discovers damage; capture the **discovery** timestamp, nature of problem and evidence confidence.
2. Mark the item not verified usable and prevent casual reissue pending a safety/quality decision.
3. Secretary or authorized delegate assesses repair versus discard; shop/office tasks follow their actual permitted procedures.
4. Record external vendor custody and milestones if applicable.
5. After repair, authorized inspection determines return to available stock; otherwise quarantine/retire remains.

**Never infer:** occurrence time or fault of a named person merely from the report.

## 6. Candidate workflow: procurement and retirement

1. Secretary identifies need using category demand, usable physical stock and repair prospects.
2. Record required quotations and approvals; the reported INR 10,000 process split is **not independently verified office policy**.
3. Record payment/reimbursement as authorized by office, without platform-initiated unauthorized disbursement.
4. Reconcile physically received items against bill; enroll item IDs or stock-lot quantities.
5. Record secretary-authorized discard, with institutional policy to be confirmed if wider deployment occurs.

**Financial example provenance:** the INR 2,500 refreshments reimbursement is **not** sports equipment procurement. The reported INR ~30,000 cricket equipment purchase is a separate equipment example.

## 7. Concurrency, failure, and correction contracts

- One durable asset cannot have two simultaneous physical issue/custody commitments.
- Interruption or offline event: create explicit pending-reconciliation state, not silently contradictory status.
- Incorrect record correction: preserve original event, correction reason, actor/role and timestamp.
- Missing / disputed item: treat as unresolved exception until checked, not evidence of theft.
- Retired equipment must be excluded from active usability and checkout calculations.
- Guard, secretary, student, team and vendor have separate permitted responsibilities; exact UI and access controls are Phase C/D decisions.

## 8. Measurement unit and audit protocol

The independently audited unit for strict accountability is an eligible **individually trackable durable item** at a fixed snapshot. A kit's constituent eligible assets are individually counted; the kit itself must not double-count them. Consumables get a separate lot-quantity accuracy measure. Explicitly record the eligibility rule, number sampled, all three independent matches, unknown or stale attributes, contradictions, and the snapshot time.

**These are intended workflow contracts.** Any Phase C prototype, even a physical ledger, can satisfy them if it demonstrates the specified outcomes under controlled tests.
