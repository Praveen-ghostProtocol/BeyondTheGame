# C3 — Executable concept prototypes and scripted mechanism checks

**Status: browser demonstration built; software unit and scenario-mechanism checks executed on *synthetic* fixtures; no human trial, physical hostel audit, live deployment, measured efficiency improvement or winning candidate.**

## Purpose and provenance
C2 established 12 matched scenarios and eight non-compensatory gates. C3 now produces lightweight runnable demonstrations of the three C1 concepts to examine *mechanism feasibility* before field testing. See [C2 protocol](c2-comparison-protocol.md), [C2 scenarios](c2-scenario-protocol.csv), [B4 contracts](../first-principles/b4-workflow-and-domain-contracts.md).

The current Alaknanda process described in Phase A is **not** a browser simulation. The synthetic IDs and records below are fictional. The 80:20 usable/damaged proportion discussed earlier is a working assumption and not a verified sample.

## Three concept prototypes

| Concept | Built artifact | Hands-on interactions | What remains unproved |
| --- | --- | --- | --- |
| **A — Physical** | [Printable forms](../../prototypes/c1/a-physical-forms.html), [procedure rehearsal checklist](../../prototypes/c3/index.html), [12 print-ready scenario cards](../../prototypes/c3/scenario-cards.html) | Manual checklist of item identification, physical cards, handover, condition, discrepancy and return | No cards actually filled in by a guard/student; no observed operating times, manual accuracy, or physical inventory audit |
| **B — Lightweight** | Browser event register ([concept lab](../../prototypes/c3/index.html), B tab) | Select/enter item code as QR equivalent; issue, declare return, staff-confirm condition, transfer, stock quantity; local event log export | No camera QR scanner, genuine network synchronization, real users, authenticated staff or independently verified physical transactions |
| **C — Integrated** | Browser lifecycle demo ([concept lab](../../prototypes/c3/index.html), C tab) | Demo role checks, distinct access vs equipment custody, kit atomic issue, partial kit reconciliation, damage, repair → inspection, procurement receipt mismatch, retirement, event history | Not a production application: no server/database/authentication, true concurrent requests, approval validation, payments, multi-user access or real operations |

**Technical design:** Shared deterministic JavaScript [`engine.mjs`](../../models/c3/engine.mjs) and a simple static [browser UI](../../prototypes/c3/index.html). Concept A is a *manual operating procedure*; the reference engine includes intentionally non-atomic paper declarations, so a conflict is flagged but not magically prevented. B includes local single-browser validation. C includes illustrative workflow rules **not secure role authorization**. No personal student data is needed.

### How to run the concept lab
From repository root, using Python 3:

```bash
python -m http.server 8765
```
Open `http://127.0.0.1:8765/prototypes/c3/index.html` in a browser. No installation or internet connection required. Demo B/C state remains in local browser storage until reset. All submitted events are synthetic; do not enter real personal data. For A, open the existing printable forms and follow the scenario cards manually.

### How to execute software checks
Node.js 18+:

```bash
node --test tests/test_c3_engine.mjs
node models/c3/scenario_runner.mjs
```
The second command overwrites only the explicitly labelled [synthetic execution log](../../data/scenarios/c3/c3-mechanism-checks.json). It checks mechanistic guards against the 12 scenario IDs for A, B and C (36 probes). For subflows not implemented end-to-end, output is `DESIGN_ONLY_NOT_END_TO_END_TESTED`, not a spurious pass. For tested code paths it records `LOGIC_CHECK_PASS`; neither label means a human participant has completed that scenario.

## Examples of mechanisms implemented
1. Room-key sign-out and return never changes individual item custody.
2. A paper double-issue can be declared twice and receives a discrepancy marker; B and C reference models block a duplicate digital issue in one browser session.
3. A claimed return moves to inspection, not directly to verified available.
4. A damage report records **discovery**, not unknown occurrence or blame.
5. A full kit issue either updates every component or fails without a partial commitment; a partial return marks unresolved components explicitly.
6. Repair-shop handoff and completion cannot skip the final condition inspection in C.
7. A procurement receipt shortfall remains a discrepancy; an invoice does not silently create physical equipment units.
8. An offline-stale-update signal becomes an unresolved exception rather than overwriting equipment status.

## Deliberate boundaries and gaps
- The C event engine runs in a browser. It does **not** demonstrate atomicity across two phones or genuine cryptographic identity; `structuredClone` applies changes to one in-memory snapshot. Database transactions and server authorization belong to Phase D.
- A human may still take an item without recording it; only independent audits can establish that information quality improved.
- Paper approach usability is **not** measured by clicks on the walkthrough checklist.
- The scenario runner exercises selected mechanistic paths, not all actions or the 32 full B4 acceptance tests.
- No empirical times, compliance levels, costs, accountability scores, or decision weights are inferred from tests.
- Live trials should not involve actual student identifiers in the public repo. Trial records need consent and anonymized IDs.

## Required before recommending a winner
1. Project owner approves trial access/roles, test asset pool and acceptable match-day burden.
2. Print/prepare A assets, create coded real/prop items for B/C, establish independent physical ground truth.
3. Carry out the 12 C2 scripts with matched starting conditions and counterbalanced concept order; capture times, task completion, staff effort, discrepancies and audit metrics using C2's blank CSVs.
4. Test eight non-compensatory gates with evidence, then review **proposed, unapproved** criterion weights.
5. Document at least one measured refinement and retest. Only then recommend and seek project-owner approval for Phase D selection.
