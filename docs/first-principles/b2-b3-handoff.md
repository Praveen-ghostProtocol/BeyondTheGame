# B2 → B3 Handoff: What to Quantify Next

**B2 output:** A supported causal mechanism candidate is the **mismatch between key/access records and item-specific custody/condition events**. It is a stronger working hypothesis than issue-time bottlenecks because actual item verification and condition inspection are absent by report, while items are generally easy to locate. This is **not yet a quantified causal effect**.

## Recommended B3 transformers

| Order | Transformer | Operation and unit | Inputs currently available | Unknowns / evidence to collect | Design decision it should drive |
| --- | --- | --- | --- | --- | --- |
| 1 | **Decompose** | Decompose access → withdrawal → transfer → return → inspection into event boundaries; decompose issue time into walking + entry + pickup | Reported workflows; ~5 min informal total estimate | Stage observations, transaction frequency, required actor involvement | Locate the missing information event; avoid optimizing equipment search without evidence |
| 2 | **Aggregate** | At chosen audit timestamp reconcile \(N_{active}=N_{available}+N_{issued}+N_{quarantined}+N_{repair}+N_{missing/unknown}\), with mutually exclusive availability states and exclusions defined | Item categories and conceptual state model | Item inventory census; kit component and consumable classification | Define inventory ledger and discrepancy indicators |
| 3 | **Normalize** | Unknown-custody count per audited durable asset; reporting delay per known damage-discovery case; repaired days per completed ticket | Recalled repair span 3–7 days only | Denominators, case timestamps and representative sampling | Identify unequal failures between categories without over-weighting the most common sport |
| 4 | **Perturb** | Hypothetically vary transfer frequency, recording compliance, simultaneous demand and repair delay; report assumptions for each run | Sport-use cadence as a planning scenario only | Event-level actual counts; compliance | Select robust candidate controls; test when and how bypass risk increases |

## Two required first-principles transformers for eventual submission

The professor asks for at least **two relevant transformers**, with: **what changed, mathematical operation, insight, and design consequence**. Prioritize **Decompose** and **Aggregate**, because they directly explain *what existing records fail to represent*. Normalize and Perturb can strengthen the case if supported by data or transparently simulated.

## Pending research gates (not blockers for B3 symbolic work)

- Independent accountable-item census / physical sample and recorded-state comparison.
- Guard log form or anonymized counts; no identifying students in public repo.
- Any real repair/condition timestamps to distinguish delay components.
- Pilot authorization before altering guard, player or office workflows.
- User approval for the definition of group/kit custody and acceptable burden before Phase C final selection.

## B3 completion requirements

1. A transformer worksheet, with clearly annotated *reported*, *estimated*, *derived*, *simulated*, and *measured* inputs.
2. Equations, boundary cases, unit checks and independent calculations.
3. A small reproducible *hypothetical* sensitivity model if useful; never a fabricated operational baseline.
4. Traceability: each transformer must produce an explicit insight, design criterion and feasible validation test.
5. A reviewer-friendly summary appropriate to the six-slide academic presentation without claiming false outcomes.
