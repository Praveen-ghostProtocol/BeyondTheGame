# A4 → Phase B handoff: first-principles analysis specification

**Status:** Phase A desk-based analysis deliverables complete, measured baseline pending. Begin Phase B theory/causal design without claiming quantitative impact.

## B1 — Functional and system decomposition
- Define system purpose: make suitable sports equipment reliably available to authorized hostel users, without unacceptable administrative burden, cost or safety risk.
- Model physical assets, access keys, signed declarations, item handovers, storage, condition, maintenance, purchases and payments.
- Separate true physical state from recorded state. Distinguish student, guard, secretary, hostel office and repair vendor; account for sports kits and consumables.
- Formalize invariants and exceptional transitions, especially key-shared access and no-register tournament kits.

## B2 — Causal and Five Whys analysis
- Investigate lack of item verification, item-to-item/person transfers, delayed condition detection and repair handoff.
- Mark **observed process facts vs potential causal mechanisms** on each diagram.
- Consider unintended consequences: verification friction can discourage sports participation, guard workload, bypass, privacy and ID custody.
- Do not blame specific students or infer damage causality from a bat incident.

## B3 — Transformer candidates (evaluate at least two rigorously)
1. **Decompose:** item-issue process time and equipment lifecycle into event components; reveal where information is lost, not just where minutes are spent.
2. **Aggregate:** reconcile total assets by status, with stock conservation, e.g. N_total = N_available + N_issued + N_maintenance + N_missing + N_retired (mutually exclusive definitions needed). For kits, also reconcile constituent items.
3. **Normalize:** maintenance downtime per active asset-time or demand fulfilment per valid request, but do not compute from absent denominators.
4. **Perturb:** controlled hypothetical tests of simultaneous borrowers, transfers, delayed returns, 24/7 access and pre-match kit collection; show simulations as simulations.
For each transformer record operation → input provenance → insight → changed design requirement → validation method.

## B4 — Design constraints and provisional non-negotiables
- 24/7 self-service room access; do not require secretary on every issue.
- Minimal guard paperwork and match-day friction.
- Clear ownership of custody during handoffs and kits; do not conflate key sign-out with actual item withdrawal.
- An item failing condition check must not automatically become available.
- Respect purchase/reimbursement rules; don't implement unilateral spending outside approvals.
- The platform may be digital, hybrid or physical; select in Phase C against evidence, not preference.

## B5 — Phase B outputs expected
- Structured system boundary and entity-state model.
- Five Whys diagram with unsupported jumps explicitly flagged.
- Transformer worksheet including mathematical operations and decision consequences.
- Hypothesis-to-test table.
- Top-level functional requirements; no implementation architecture chosen prematurely.

## Baseline gate
Before quantitative impact reporting, perform or obtain a permissible observed accountability baseline and matched validation after the prototype. Without this, report only what was tested in scenarios and what remains unmeasured. An honest unmeasured baseline is preferable to an invented percentage.
