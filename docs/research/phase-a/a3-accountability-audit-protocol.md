# A3 — Accountability audit and measurement protocol

**Purpose:** Establish a fair, repeatable numeric baseline for **equipment accountability**, then compare redesigned workflow to current practice. **Status:** Protocol designed, not yet executed.

## Unit of analysis
One **uniquely identified physical item** at a defined snapshot time. For full sports kits, inventory components separately and record parent kit ID; for cheap consumables count stock lots rather than pretending each shuttlecock is individually tagged.

## Proposed lightweight baseline audit
1. Ask the sports secretary for authorization to inspect a small representative sample (suggest **20–30 items**, spanning cricket, badminton, volleyball/football, table tennis). Only if permitted; the sample size is a suggestion, not completed work.
2. Assign temporary anonymous IDs (e.g. `C-001`, `B-002`), and independently assess condition: `Usable`, `Damaged`, `Unknown`.
3. Obtain the best available *recorded* location, custodian, condition, and timestamp according to existing processes. If the current paper register **cannot** express a field, explicitly mark it `Unrecorded`; do not fill it from the physical verification.
4. Independently verify actual location, responsible custodian/group (or `Hostel storage`), and condition. A locker location alone is not proof of current custody when an item is issued.
5. Record attribute-wise comparison and status: verified-correct, verified-incorrect, or unassessable. Avoid personal identifiers: use anonymous roles/groups for exported data. Keep any sensitive raw notes off the public repository.
6. Summarize: audited N; fully assessable N; verified-correct all-three N; fully accountable N; fraction with each attribute recorded. Retain the raw audit date and source type.

## Definitions
- **Strict verified-accountability coverage:** Items with all three attributes **recorded and independently verified correct** ÷ all audited items. Missing fields in existing process do not count as successes, but should not be described as false entries.
- **Full assessability:** Items for which all three record-and-reality pairs exist ÷ audited items.
- **Accuracy conditional on assessability:** Fully correct items ÷ fully assessable items; report `Not available` if zero assessable.
- **Availability:** usable items / active audited items. This is different from verified accountability and cannot use the assumed 80:20 as an observed numerator.
- **Denominator:** explicitly list exclusions, lost-to-follow-up items and items not accessible for inspection. Never remove difficult cases without disclosure.

## Controlled future comparison
Use comparable randomized or counterbalanced scenarios: issue, return, damage reporting, sharing, and a kit borrow. Compare process accuracy and task time with current workflow and selected redesign. Staged test results must be labelled **staged**, not live operational impact. Retain failure cases. Include training and setup costs in trade-offs.

## Workbook workflow
Open `data/baseline/a3-baseline-model.xlsx`:
- `Sources & Inputs`: reported and assumed values; no invented measured data.
- `Demand Scenarios`: editable *what-if* frequency model; not transactions observed.
- `Accountability Audit`: blank sample rows and formulas; enter only verified items.
- `Transaction Trials`: optional blank timing observations; source-type field required.
- `Dashboard`: shows **not measured** until inputs have actual observations.

## Privacy and quality
Do not commit photographs of register pages containing names, roll numbers, signatures or ID cards, or scans of personal paperwork, to public GitHub. Do not infer legal culpability from missing evidence or from who held the room key. Keep synthetic pilot events and real incidents separate. Report which values are estimates and who provided the original report.
