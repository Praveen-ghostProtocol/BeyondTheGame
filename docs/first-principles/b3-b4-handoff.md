# B3 → B4 Handoff — Quantitative Analysis to Design Requirements

**B3 status:** Four transformer specifications completed; symbolic equations, fictitious stock reconciliation, demand/friction sensitivity and event-compliance sensitivity implemented and test-verified. **All numerical scenario outcomes are hypothetical.** No measured accountability baseline.

## Candidate design requirements to carry into B4

| ID | Requirement hypothesis | Derivation | Decision needed later | Evidence still needed |
|---|---|---|---|---|
| BR-01 | Distinguish room access from individually or group-assigned equipment custody | Decompose: missing event boundaries | Approve individual vs team custody definitions | Consent-based event observations |
| BR-02 | Preserve single-record mutually exclusive item availability states | Aggregate: state stock identity | Approve state taxonomy and repair/inspection authority | Physical inventory snapshot |
| BR-03 | Capture condition before an item becomes generally available again | Decompose + Aggregate: inspection gap | Define risk-tiered inspection, not full-time guard inspection | Check burden and damage detectability |
| BR-04 | Provide minimal-step captain-level kit handover and component reconciliation | Decompose + Perturb: bypass vs documentation | Approve acceptable tournament interaction budget | Timed captain tasks |
| BR-05 | Display numerator, denominator, unknowns and audit timestamp for accountability | Normalize: strict vs assessable vs accuracy | Approve audit reporting definitions | Independent audit |
| BR-06 | Reconcile durable assets separately from consumable lots | Aggregate: avoid double counts | Approve categorization by item and kit | Item list and sample physical count |
| BR-07 | Make record capture robust under informal sharing and failures | Perturb: transfer-chain sensitivity | Choose event record mechanism after C comparison | Transfer test, offline test |
| BR-08 | Measure guard/student burden; avoid heavy recording requirements | Perturb: additional seconds accumulate | Set acceptable overhead only after testing | Timed tasks + user feedback |
| BR-09 | Preserve provenance of repair and purchase decisions | B2 lifecycle findings; B3 accountable states | Select maintenance ownership and approval protocol | Vendor/office process verification |

## Remaining Phase B sequence

- **B4:** convert above to scoped, measurable, testable requirements and nonfunctional constraints, tagged **provisional** until stakeholder approval and field validation; define acceptance tests and competing alternatives for Phase C.
- **Later:** evaluate three meaningfully distinct reconstruction families rather than assuming a software-first solution.
- **Always:** no synthetic observations passed off as actual events, and no private student or guard identities in this public repository.

## Reproducibility

1. 0Python standard library: `python models/b3/scenario_model.py` generates four synthetic CSV tables.
2. `python -m unittest discover -s tests -p 'test_b3*.py' -v` validates equations and edge cases.
3. Open `data/baseline/b3-transformer-model.xlsx` for editable formulas and what-if inputs.

Research source: professor's project brief mandates two interpretable transformers, traceable to design decisions and validation (FPT Term Project brief, p. 2). Source workup: A1–A4, B1, B2 documents in this repository.
