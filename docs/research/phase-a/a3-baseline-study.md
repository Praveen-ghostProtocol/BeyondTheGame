# A3 — Baseline measurement study: Alaknanda Hostel

**Status:** Provisional desk-based baseline from sports secretary's firsthand account; **no physical audit, measured transaction sample, or verified register counts** have been collected.  
**Approved primary outcome:** equipment accountability (correct location **and** custodian **and** usable condition for an identified item).  
**Source:** Sports secretary's responses in project conversation, after A2 workflow mapping. This study is one site (Alaknanda Hostel), not an IIT Madras-wide audit.

## 1. Updated inputs and evidence classifications

| Input | Value / report | Classification | Interpretation |
| --- | --- | --- | --- |
| Hostel population | ~400 | Recalled/estimated | Not validated against hostel roll |
| Badminton | Played daily | Secretary-reported schedule | **Sport-use occasions**, not observed loans |
| Volleyball | Played daily | Secretary-reported schedule | **Sport-use occasions**, not observed loans |
| Football | Every other day | Secretary-reported schedule | 3–4 sport-use occasions/week |
| Cricket | Every other day | Secretary-reported schedule | 3–4 sport-use occasions/week |
| Journey to get equipment | ~5 min end-to-end | Informal estimate | Includes walking and guard/register; no stopwatch |
| Walking component | ~2 min | Rough verbal estimate | Not necessarily all walking steps separately |
| Guard interaction/register | ~2 min | Rough verbal estimate | Remainder of 5 min not allocated or measured |
| Usable/damaged stock | 80% / 20% | **Unverified user-selected scenario** | **Not audited inventory condition**; denominator unknown |
| Typical repair turnaround | ~3–7 days | Recalled typical range | Case timestamps absent; includes coordination, approvals, vendor and secretary availability |
| Item accountability | Primary metric approved | User decision | **No numerical baseline available** |
| Missing racket | At least one recalled incident | User-reported example | Racket allegedly returned but not found; no contemporaneous documentation |
| High-value bat breakage | ~₹15,000 cost; broke beyond repair | User-reported example | Circumstances/causal mechanism reported; no independent validation |
| Sub-₹10,000 procurement example | ~₹2,500 refreshments for tennis-ball tournament | Recalled transaction | **Event refreshments, not equipment purchase**; demonstrates reimbursement route only |
| ≥₹10,000 procurement example | ~₹30,000 cricket equipment | Recalled transaction | Amount estimated, ~10 months prior; itemized invoice not yet reviewed |
| Tournament exception | At inter-hostel tournament (Feb–Mar); captain kit handover may bypass register with secretary permission | Recalled procedure | Number or percentage of exceptions unknown |

## 2. Activity-based scenario calculation (not borrowing evidence)

Badminton 7 occasions/week + volleyball 7 + football 3–4 + cricket 3–4 = **20–22 estimated sport-use occasions/week**, central approximation **21**. These are occasions of sport, **not individual player count, sports-room key loans, registered items or fulfilled requests**. Counting a session as a loan is a modeling assumption; overlapping sessions and shared key access can invalidate it.

Three strictly **hypothetical** registered-loan demand scenarios use 1, 2, or 3 distinct borrowing events per sport-use occasion: **20–22**, **40–44**, and **60–66** weekly events respectively. These are scenario outputs, **not observations**. They are included only for workload/sensitivity planning, and **must not be described as actual register counts**. The workbook makes the multiplicity editable.

An 80:20 usable/damaged split is a **scenario assumption**, not a finding. It must not be turned into an equipment count without a known inventory denominator, or cited as an observed condition rate. The 5-minute journey is likewise a recollection, not a timed sample.

## 3. Primary metric specification

**Fully verified item accountability** for a defined audit snapshot:

- Define sampling frame: a known list of individually trackable hostel-owned assets; temporarily label sampled items with anonymous item IDs if necessary.
- For each item, independently verify (i) physical location or off-site whereabouts, (ii) current custodian or storage responsibility, and (iii) usability/condition.
- Compare all three with what the *existing operating record* can actually support **at the same snapshot**.
- Mark attribute matches only when **both** recorded and verified values exist. Treat an unknown/unrecorded attribute as **not verifiable**, not automatically incorrect.
- **Strict full-accountability rate = verified-correct on all three / items sampled.** For every audited item with an unrecorded attribute, strict successful verification fails. Additionally show **fully assessable share** (all three recorded and verified) and **accuracy among assessable items**; otherwise one combined percentage conflates missing data and incorrect data.
- Numerators and denominators should be reported along with the percent. Separate in-storage and checked-out equipment if their custody evidence differs. Exclude non-individual consumables from individual-item audit or audit by stock lot.

**Important:** Because there is no physical audit or contemporaneous three-attribute reference, the **current numerical baseline is unmeasured**; do not claim 0% or 80%. We can conclude only that the *present process lacks a mechanism for routine verified item-level accountability*.

## 4. Secondary metrics to collect later

| Metric | Definition | Status |
| --- | --- | --- |
| Issue journey | Requestor starts journey to moment equipment obtained; record walking/register/collection separately | Estimated ~5 min, not measured |
| Guard desk time | Time interacting with guard and writing register | ~2 min recalled |
| Physical stock condition | Usable units / assessed active units; define sports and exclusions | 80% is provisional assumption only |
| Repair turnaround | Timestamp restored to usable service minus first reported fault | 3–7 days recalled, not measured |
| Missing/disputed asset frequency | Reconciled disputed/missing events / total audited asset-time | One incident remembered; denominator unknown |
| Tournament exception rate | Documented no-register kit issues / all kit issues | Unknown |
| Workload | Person-minutes per issuing, return, repair, quotation and purchase | Not timed |
| Purchase lead time | Need acknowledged → physically usable equipment available | No usable stopwatch/case chronology yet |

## 5. Procurement caveats

The user's example below ₹10k is **refreshments, not sports-equipment procurement**; use it solely to illustrate handling of a small reimbursement. The reported ₹30k cricket purchase is a high-value sports-equipment case. Do not infer exact lead times, process compliance, or typical prices from either without vouchers or records. Sports secretary reported under-₹10k self-pay/reimbursement and ≥₹10k three-quotation/direct-pay rules in A1; treat as reported practice until reviewed with the hostel office.

## 6. Conclusions and Phase B implications

- The core gap is **record-to-reality reconciliation**, not proven retrieval delay. A register can be completed while actual item movements, transfers, and post-return condition remain unknown.
- A small, honest simulation can test definitions, assumptions, sensitivity and software mechanics. It cannot establish current performance or causal improvement.
- The professor's project brief emphasizes measured before/after evidence and distinguishing measured effects from estimates. No claimed impact should enter the final presentation until supported by a real audited/controlled comparison.

## 7. Remaining evidence needs (not blockers for designing the measurement system)

1. A permitted, anonymized 10–30 item condition and record-reconciliation spot-check, when feasible.
2. Optional 5–10 consented, timed ordinary checkouts, with no ID or roll numbers retained.
3. Redacted invoice for the ₹30k cricket equipment example if contribution to procurement analysis is needed.
4. Clarify later whether any staged test with volunteers/guard is authorized; no permission is assumed.
5. Scope: include ordinary borrowing, tournament kits, maintenance and procurement **as distinct strata**; no conflation of transaction, kit or quantity units.

## 8. Source traceability

See `a1-evidence-register.csv` (A3 entries), A1 field study, A2 process maps, and workbook `../../../data/baseline/a3-baseline-model.xlsx` (relative to project root: `data/baseline/a3-baseline-model.xlsx`). All current figures are source labels or assumptions, not measured trials.
