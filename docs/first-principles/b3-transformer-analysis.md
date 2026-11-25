# B3 — Quantitative First-Principles Transformers

**Project:** Beyond the Game · Alaknanda Hostel, IIT Madras  
**Status:** Completed analytical model; no measured accountability baseline or impact study  
**Continuity:** [B1 system model](b1-functional-system-decomposition.md) → [B2 causal analysis](b2-causal-analysis.md) → **B3** → [B4 input specification](b3-b4-handoff.md)

## Purpose and constraint

The professor's brief asks for at least **two transformers**, and for each one: (1) what was transformed, (2) its mathematical operation, (3) the resulting insight and (4) how that insight changes the proposed reconstruction. We prioritize **Decompose** and **Aggregate** for the six-slide submission. **Normalize** and **Perturb** supply supplementary evidence and design robustness checks. This is not a deployed solution or observed improvement.

The secretary reports ~400 residents, easy-to-find equipment, paper key/register sign-out, unverified self-collection and return, informal handovers, 24/7 access, and occasional unregistered tournament kit collection. Current strict accountability **cannot be calculated**; a working 80:20 usable/damaged split is not an inventory survey. See [A3 baseline](../research/phase-a/a3-baseline-study.md) and [B2 hypotheses](b2-hypothesis-validation.csv).

## T1. DECOMPOSE — separate movements from their recorded proxies

**Transformation:** Replace one apparent operation, “borrow equipment,” with its independently meaningful events:

```mermaid
flowchart LR
  A[Room key/access event] --> B[Actual item withdrawal]
  B --> C[Custody transfer(s)]
  C --> D[Physical return]
  D --> E[Condition inspection]
  E --> F[Usable stock or repair]
  A -. Recorded in register .-> R[Key/declared-items record]
  B -. Not verified .-> R
  C -. Not normally recorded .-> R
  D -. Claimed return .-> R
  E -. No routine inspection .-> R
```

**Mathematical operation:** Additive decomposition of end-to-end time,

\[
T_{journey}=T_{walking}+T_{guard/registration}+T_{pickup/other}.
\]

User's informal estimate: ~300 s total, roughly 120 s walking and ~120 s guard interaction/entry. The **~60 s remainder is arithmetic, not a measured pickup duration**. Register entries record declared equipment, not verified physical movement. For a chain of \(k\) item transfers, at least \(k\) distinct potential updates arise beyond initial issue/return.

**Insight:** The largest evidential failure is **event observability**, not proven equipment search latency. A key ledger does not imply current custody or condition of a physical bat.

**Design consequence:** Investigate low-friction item/kit identity, accountable handover, return confirmation, and condition reporting. Compare required user actions against the known match-day fast-lane requirement. Do **not** presume the guard should inspect every item.

**Validation:** Stage matched borrowing scenarios; record the share of actual movements represented in a record, full-accountability correctness, and minutes/person of extra work. Independent observation and consent are required.

## T2. AGGREGATE — reconstruct a complete inventory accounting identity

**Transformation:** Combine **mutually exclusive administrative availability states at one timestamp**. Each durable asset appears once:

\[
N_{all}=N_{available}+N_{issued}+N_{pending\ inspection}+N_{quarantined}+N_{external\ repair}+N_{missing/unknown}+N_{retired}.
\]

\[
N_{active}=N_{all}-N_{retired};\quad 0\leq N_{available}\leq N_{active}.
\]

“Available” means usable and physically released for ordinary issue; “missing/unknown” does **not** imply theft. **Condition and custodian are separate attributes** from administrative state. A currently issued item can later be reported damaged; the system must preserve that history without double counting it in two state buckets. Kit components are reconciled by constituent asset/quantity rather than counting the kit container as additional equipment. Low-value consumables require separate **lot-and-quantity** accounting, not fake unit IDs.

**Toy identity check (entirely fictitious, not Alaknanda inventory):** 31 available + 9 issued + 2 awaiting inspection + 3 quarantined + 2 off-site repair + 1 missing/unknown + 2 retired = **50 lifetime counted assets**, of which **48 active** and **31 immediately available**. The usefulness is demonstrating a reconciliation invariant, not claiming the hostel has 50 items.

**Insight:** Purchase invoices and key logs alone cannot reliably produce a reconciled *current usable inventory*. State transitions need auditable ownership and exception handling.

**Design consequence:** Test individual IDs for durable assets, quantity-based stock for consumables, kit manifests, mutually exclusive status, repair quarantine and snapshot reconciliations.

**Validation:** Independently count a consented sample of physically held equipment, including issued/repair items where feasible; compare total and state/condition/location against ledger values. Report unverified and missing records explicitly.

## T3. NORMALIZE — compare categories and completeness fairly

**Transformation:** Express outcomes relative to their **correct** population and period; do not confuse a larger raw incident count with a worse rate.

\[
A_{strict}=\frac{N_{all\ three\ verified\ correct}}{N_{audited}};\quad
C_{record}=\frac{N_{all\ three\ assessable}}{N_{audited}};\quad
Q_{assessable}=\frac{N_{all\ three\ correct}}{N_{all\ three\ assessable}}.
\]

The first is the **approved primary metric** (fully verified location, custody/responsible entity and condition). The second measures completeness/assessability. The third isolates correctness **conditional on having all three fields and independent checks**. These must be reported together to avoid mistaking absent records for known incorrect ones. If the assessable denominator is zero, conditional accuracy is **undefined**, not zero.

Other candidate denominators:
- Unknown-custody assets per 100 *audited durable assets*.
- Maintenance downtime per 100 *active-asset-days* (if comparable periods and timestamps exist).
- Median days per *completed repair ticket* (include damage-severity strata when possible).
- Log-completion rate per *independently witnessed equipment event*, not per room key loan.

**Toy comparison, fabricated only to test arithmetic:** Badminton 5 of 20 audited fully verified, Cricket 3 of 10, Football 8 of 12. These are **not** reported or measured rates; categories are labelled synthetic in both CSV and workbook.

**Insight:** Recording completeness and verified correctness are different issues; sports with larger inventories need denominators. Small samples create uncertainty.

**Design consequence:** The future dashboard must show numerator, denominator, unknowns, audit date and condition/custody/location breakdown—not a single unexplained “accuracy score.”

**Validation:** Conduct anonymized, timestamp-matched audit with comparable categories and document sampling procedure. Treat personal identities privately; public outputs aggregate only.

## T4. PERTURB — stress the assumptions and examine friction

**Transformation A: event capture sensitivity**. Under a deliberately simplified **independence assumption**, the probability that all required record *events are captured* after \(k\) informal custody transfers is:

\[
P_{records}=p_{issue}\,(p_{transfer})^k\,p_{location}\,p_{condition}.
\]

This is *not* independently measured correctness or the approved accountability KPI. It ignores record staleness, correlated behavior, physical misplacement and whether responsibility is assigned to a team instead of an individual. For an illustrative assumption of 0.95 initial-issue recording, 0.80 per-transfer recording, 0.90 location and 0.90 condition recording:

- \(k=0\) → \(P_{records}=0.7695\) (76.95%).
- \(k=3\) → \(P_{records}=0.393984\) (39.3984%).

These are **hypothetical model outcomes**, not evidence that Alaknanda achieves those percentages. The model illustrates why repeated handover opportunities can make record completeness fragile.

**Transformation B: demand/effort sensitivity**. Secretary-reported sport-use frequency implies 20–22 *sport-use occasions* per week for four main sports. Using 1–3 hypothetical borrowings per occasion gives **20–66 possible events/week**, which are **not actual guard-register counts**. Additional administrative time under a candidate workflow:

\[
W_{extra}\,(minutes/week)=\frac{N_{loan\ events/week}\times t_{extra\ seconds/event}}{60}.
\]

For illustration, 40–44 event assumptions with 30 extra seconds implies **20–22 extra person-minutes weekly**. This does not include extra returns or transfers; those must be modelled separately before evaluating a real system.

**Insight:** Stronger records are not free. More transfer confirmations may improve completeness *if complied with*, but increased effort might reduce compliance and encourage tournament bypasses. The toy probabilities do not determine actual behavior.

**Design consequence:** Compare individual checkout vs team/kit-level accountability, one-tap self-confirmation, risk-tiered inspection and acceptable interaction costs. Design controls should be experimentally selected, not imposed based on synthetic calculations.

**Validation:** Counterbalanced prototype tasks, measuring field verification rates and staff/student burden with and without controls; later vary demand and compliance under realistic pilot conditions.

## Cross-transformer synthesis

1. **Decompose** shows which physical events the present register doesn't describe.
2. **Aggregate** gives the accounting invariant a redesigned system must preserve.
3. **Normalize** defines what counts as a verifiable improvement rather than a misleading raw count.
4. **Perturb** exposes potential trade-offs and tests whether a proposed control might cause avoidance.

**Working design requirement (still to test):** Improve verified item/kit location, custodian and condition while preserving 24/7 access, fast tournament operations, realistic guard effort and authorized privacy handling.

**Primary validation gap:** no audited equipment denominator and no independently verified recorded-versus-physical item snapshot; thus **strict accountability has no measured baseline**. Phase C must compare alternatives, Phase E must measure their performance.

## Artifact links

- [Input assumptions and boundaries](b3-model-assumptions.md)
- [Transformer-to-design traceability](b3-transformer-traceability.csv)
- [Validation plan](b3-validation-protocol.md)
- [Scenario generator](../../models/b3/scenario_model.py)
- [B3 scenario output directory](../../data/scenarios/b3/)
- [Formula workbook](../../data/baseline/b3-transformer-model.xlsx)
- [B4 handoff](b3-b4-handoff.md)
