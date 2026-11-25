# B4 → Phase C: Comparable Alternative-Design Experiment Brief

**B4 outcome:** Implementation-neutral, evidence-linked requirements and acceptance tests are ready. **Phase C must select a mechanism**; B4 does not prove an app is needed.

## 1. Three meaningfully distinct families to compare

| Family | Core design change | Potential strengths | Potential failure |
| --- | --- | --- | --- |
| **C-A Physical + procedural** | Labelled bins/tags, standardized team ledger, condition/quarantine tags, paper repair queue and inventory census | Low cost, no network, easy pilot | Manual updating and lost records |
| **C-B Lightweight digital + physical** | Item/kit IDs with short QR/form record, shared availability/repair status, paper fallback | Searchable events with moderate complexity | Scanning friction and stale self-reported status |
| **C-C Integrated lifecycle platform + physical** | Unified requests, custody, condition, repairs, procurement, roles, analytics, receipt records | Potentially strong visibility and integration | High implementation cost; errors persist if real-world updates are skipped |

Do not treat C-C as the default winner. Criterion weights and actual scenario results must determine the choice. Hybrids can be evaluated after the initial comparison.

## 2. Same tasks across candidates (test IDs in [B4 catalog](b4-acceptance-tests.csv))

1. Ordinary resident borrows an identified usable racket while key controlled by guard.
2. Second resident accesses equipment while initial key session remains outstanding.
3. One racket is passed around within a team, then moved away by another student.
4. Student claims return but the item is not physically found.
5. Captain takes a cricket kit shortly before match; inspect manifest and return short one component.
6. A damaged racket is reported and segregated; later approved repair restores it.
7. Office procurement approvals and physical delivery are represented accurately.
8. The system goes offline (where relevant), then recovers without silently corrupting custody.
9. Auditor samples location/custody/condition for same fixed-time item set; count assessable, correct and discrepant states.

**Test design:** Consent-based staged or live scenarios, task counterbalancing when possible, identical asset lists, identical participants or matched groups, explicit control of task order and learning effects. Document what a physical system can and cannot represent instead of inventing a digital equivalent.

## 3. Comparison measures and no-fabrication controls

- **Primary:** Independently verified *strict accountability* on eligible physical items after task completion, reported as n/N with audit time.
- **Secondary:** Task completion and errors, issuing/return seconds by actor, reporting latency, kit reconciliation accuracy, record omissions, cost and ongoing maintenance burden.
- **Critical constraints:** 24/7 access, no secretary required for ordinary requests, low-friction tournament flow, no automatic attribution of damage, usable/repair distinction, privacy and policy compliance.
- **Costs:** setup effort, ongoing time per event, materials/hosting, risk of record drift and repair burden.
- **Evidence labels:** observed / documented / reported / estimated / synthetic. No measured effectiveness exists yet.

## 4. Decision gates before Phase D

- User approves what constitutes acceptable operational burden and which responsibility model (individual/team) to adopt.
- A physical or staged test demonstrates meaningful advantages without unacceptable record gaps.
- Key/stakeholder permissions and public/private data boundaries are clarified.
- The chosen system has passed its relevant P0 contractual acceptance tests **in a documented test**; until then record as planned, not passed.
- Final selection memo states *why the competing alternatives were rejected* with results or explicit constraints.

## 5. Suggested Phase C work products

`docs/solution-design/c1-alternative-concepts.md`, a prototype for each concept (not necessarily software), `docs/solution-design/c2-comparison-protocol.md`, `docs/testing/c3-comparison-results.md` (when actual trials exist), and `docs/solution-design/c4-selection-memo.md`. Only create files when their contents exist. Keep `final/` reserved for submission.
