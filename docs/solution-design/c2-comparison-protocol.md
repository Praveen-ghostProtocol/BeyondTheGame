# C2 — Controlled comparison protocol (pre-test)

**Status:** Experimental protocol, not executed. **No winner, measured comparison or real accountability baseline yet.**

## 1. Question and hypotheses
Which of the three C1 approaches yields independently verified item-level accountability with acceptable student, guard, captain and secretary effort, cost and operational risk? A: physical procedures, B: lightweight QR/forms, C: integrated lifecycle system. All must distinguish room-key events from item events, and condition from custody.

- H1 (hypothesis): verified status accuracy improves as physical handovers are reconciled rather than inferred from key returns.
- H2 (hypothesis): QR reduces writing/search effort relative to paper in some contexts but introduces compliance and outage risks.
- H3 (hypothesis): integrated permissions and atomic issues reduce certain invalid double-issue states but create overhead and ongoing cost.
- H4 (hypothesis): captain fast-lane and grouped manifests protect match preparation without sacrificing accountability.

**No hypothesis is considered demonstrated by the design documents alone.**

## 2. Candidate interventions and fairness
- A: stable item labels, physical ledgers, kit manifests, return verification, damage tags and repair board.
- B: physical labels/QR, lightweight forms and status view, staged offline fallback, manual independent audit.
- C: integrated controlled handover/event histories, kit/maintenance/procurement states and role-based auditing plus physical labels.
- Give **all** concepts comparable storage labels and a clear staff handover brief. Treat C's software depth as a **cost and learning burden** as well as a potential benefit. Use the **same starting physical inventory and ground truth** for each concept.
- Preserve Alaknanda guard's current scope: the guard manages the key and existing register, **not** item inspection. Any newly proposed checker role is explicitly costed and approved.

## 3. Scripted scenarios
The detailed 12-script library is [`c2-scenario-protocol.csv`](c2-scenario-protocol.csv). Every script references the original C1/B4 scenarios and states the expected ground truth. All 32 B4 acceptance tests remain available for deeper coverage; scripted C2 scenarios combine the most informative ones.

**Suggested staged design:** 6 consenting participant/group runs per scenario per concept; 12 × 3 × 6 = **216 planned scenario runs**, not completed. Use comparable operators across concepts, and counterbalance concept order (ABC, ACB, BAC, BCA, CAB, CBA) to reduce learning effects. Permit team scenarios to use groups while still recording one run as one scenario attempt. Randomize order within operational constraints and keep safety/permission boundaries. These sample sizes are a proposal, not a power calculation.

## 4. Measurement instrumentation
At each run record in [`c2-trial-log.csv`](../../data/templates/c2-trial-log.csv): task outcome, seconds of active user/guard/secretary time, steps, errors, discrepancy handling, condition outcome, timestamp and evidence reference. Record interruptions separately (do not silently omit failures). No identifiable names, roll numbers or ID-card images in public source control.

For a subset of real or staged items, an **independent checker** establishes physical location, responsible entity and condition and records each attribute **correct, incorrect, unknown/unassessable or contradicted**, with source and time in [`c2-independent-audit.csv`](../../data/templates/c2-independent-audit.csv). We intentionally do not infer triad correctness from app or ledger alone.

**Strict accountability = verified-correct on all three dimensions / all eligible audited items**. Report separately item count, unknown/unassessable, contradicted and unverified statuses. If zero eligible audits, report **not measured**, not zero percent.

- Task completion = completed runs / eligible attempted runs (report denominator and design).
- Median task time = median of all completed runs, paired with completion/failure counts so speed does not hide failures.
- Actor burden = median active seconds by role, plus step counts; do not pretend total time and actor-active time are interchangeable.
- Cost = upfront + annual recurring, with actual quotes distinguished from guesses; count training, physical labels, scans/phones and hosting.
- Uncertainty = retain trial distribution; small sample size is a limitation, not precision.

## 5. Execution order
1. Prepare standardized equipment props and verification scripts with unique codes, kit manifests and condition states. Only actual participants/props with permission.
2. Train users **equally** to a defined minimum; log training time.
3. Run accessibility, safety and privacy checks before tests.
4. Stage counterbalanced paired tasks with matched initial conditions and independent physical ground truth.
5. Record trial times, failures, discrepancies and actor burden in blank templates.
6. Independent audit **without consulting each concept's dashboard as ground truth**.
7. Ingest CSVs using `python models/c2/evaluate.py` to compute only observed results.
8. Run documented error/failure cases; inspect gate status, costs and limitations.
9. Make a recommended but provisional selection **only when evidence exists**; obtain user approval before C3/Phase D.

## 6. Decision rules
Eight [`non-negotiable gates`](c2-nonnegotiable-gates.csv) must be addressed first. Design intention is not a passed test. Numerical selection criteria and suggested **unapproved** weights are in [`c2-proposed-criteria.csv`](c2-proposed-criteria.csv). A candidate cannot compensate for severe safety/privacy/accountability failures through glossy UI or high feature count. Even after passing gates, weights must be user-approved, and actual field data should inform the final selection.

## 7. Evidence and ethics
- Report R = recalled, O = observed, D = documented, I = inferred, E = estimated, S = simulated separately.
- Staged demos may validate mechanism, not claim observed hostel impact.
- Unknown damage timing and damage responsibility remain unknown unless separately verified.
- Do not publish personally identifiable borrowing logs, records, participant names or photos without permissions.
- The reported ₹10,000 hostel threshold is user testimony, not independently verified financial policy; keep authority with hostel office.
