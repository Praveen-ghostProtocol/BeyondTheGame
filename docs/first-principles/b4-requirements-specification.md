# B4 — Implementation-Neutral Requirements Specification

**Project:** Beyond the Game, Alaknanda Hostel (IIT Madras)  
**Phase:** B4: convert A1–A4 and B1–B3 findings into verifiable design requirements  
**Status:** **Analytical draft for Phase C comparison. Not a solution selection, deployed policy, or field-validated specification.**

## 1. Purpose, approval boundary, and evidence

**Fundamental function:** Make suitable hostel-owned sports equipment accessible to authorized residents, with accurate, proportionate responsibility and equipment condition information over its full life cycle: acquire → store → issue/share → return → assess → repair/replace/retire.

**User-approved primary outcome:** Strict verified equipment accountability: the fraction of *audited eligible, individually trackable physical items* whose recorded **location, accountable custodian/entity and condition** all agree with an independent check at an explicitly matching time. No measured baseline is available.

**Primary rule:** Every proposed requirement below is a **design or evaluation candidate**, not an authorized change to hostel operating procedures. The sports secretary's descriptions are firsthand **reports**, not independently verified institutional policy. No live test or identifying data collection is approved by this document.

- Canonical **40 requirements**: [B4 requirements register](b4-requirements-register.csv).
- **32 executable/manual acceptance scenarios**: [B4 acceptance test catalog](b4-acceptance-tests.csv).
- **12 evidence chains**: [B4 evidence-to-requirement matrix](b4-evidence-to-requirement-traceability.csv).
- [B4 state and workflow contracts](b4-workflow-and-domain-contracts.md); [pending decision gates](b4-decision-register.md); [Phase C experiment brief](b4-phase-c-handoff.md).

Sources: [A2 current state](../research/phase-a/a2-current-state-process-maps.md), [A4 evidence/gaps](../research/phase-a/a4-evidence-gaps-and-validation.md), [B1 state model](b1-state-and-custody-model.md), [B2 causal hypotheses](b2-hypothesis-validation.csv), [B3 transformers](b3-transformer-analysis.md). The professor's term-project brief requires demonstrable first-principles links, alternatives, a built/piloted improvement and actual comparison testing.

## 2. Requirement categories and prioritization

- **P0:** safety, evidence integrity, authorization, core accounting invariants, 24/7 operating constraint, or measurable primary outcome. A Phase C candidate must **show how** these will be respected; the implementation mechanism remains flexible.
- **P1:** central proposed features to test and compare; may be satisfied by a manual, hybrid, or digital workflow.
- **P2:** secondary features; implement only if they materially improve measured outcomes relative to cost/effort.

| Group | Scope (requirement IDs) | Acceptance focus |
| --- | --- | --- |
| Access | R01–R03 | 24/7 borrowing, key record separated from item custody |
| Inventory | R04–R09 | Durable IDs, consumable lots, team kits, truthful stock and audit |
| Borrowing | R10–R14 | Valid requests, handover, individual/team responsibility and transfer |
| Returns / tournament | R15–R18 | Physical reconciliation, kit discrepancy, low-friction exception and inspection |
| Condition / maintenance | R19–R24 | Unusable stock quarantine, discovery provenance, repair and retirement |
| Procurement | R25–R28 | Approval/provenance, physical receipt and budget reasoning |
| Metrics | R29–R31 | Strict triad accountability, unknown-vs-wrong, normalized denominators |
| Usability / integrity | R32–R34 | Interaction time, event trace and failure recovery |
| Security / evaluation | R35–R38 | Roles, privacy, test provenance and refinement |
| Operations | R39–R40 | Training and overdue treatment without inventing fines |

The **source_evidence** field in the CSV points to the A1–A4 evidence register, not to a verified causal effect. The `verification` field defines how the proposed requirement can be checked. Requirement numbering is stable across subsequent Phase C and D work.

## 3. Core objective and guardrail metrics

**Strict accountability** (a fixed-time audit):

\[
A_{strict}=\frac{N_{location+custody+condition\ verified\ correct}}{N_{all\ eligible\ items\ audited}}.
\]

Unrecorded, unverifiable and contradicted attributes are separately flagged; no "0%" baseline is inferred from current register limitations. Every report must show **numerator, denominator, audit timestamp and sample method**. For each independently checked item, all three attributes must agree at a contemporaneous time to count as verified.

**Supporting measures** (secondary, not silently promoted to the main KPI):

- *Assessability rate* = audited items for which all three recorded fields are evaluable / all audited eligible items.
- *Conditional accuracy* = all-three-correct / all-three-assessable; meaningful only with a nonzero denominator.
- *Request fulfilment* = valid requests receiving suitable items within a **user-approved service window** / total valid requests.
- *Condition-discrepancy rate* = mismatched usable condition classifications / condition-audited items.
- *Repair lead time* = recorded restoration time − reported discovery time, only for cases with both timestamps.
- *Burden* = seconds/user and seconds/custodian per comparable task; recording-compliance and missing-step frequency.
- *Consumables* = quantity reconciliation by lot, not strict individual-item accountability.

**Targets are undecided.** The 80:20 usable/damaged assumption, ~5-minute acquisition estimate, 3–7-day recalled repair range and B3 toy scenarios are **not measured baselines**.

## 4. Governing principles and transformer-to-requirement linkage

| Principle / transformer | Fact, equation or model | Design consequence |
| --- | --- | --- |
| **Decompose** | Access ≠ withdrawal ≠ transfer ≠ return ≠ condition | Separate event verification at the points that create information loss (R02, R12, R15, R18) |
| **Aggregate** | Physical stock in mutually exclusive active/retired/unknown operational categories must reconcile without duplicate counts | Unique asset/lot/kit identity, reconciliation, quarantine (R04–R09, R19) |
| **Normalize** | Strict accountability is a proportion with a known eligibility definition and independent sample | Record missing fields, audit timestamps and denominators (R29–R31) |
| **Perturb** | More transfer-record events may increase information opportunity but add effort | Evaluate group custody, tournament fast lane, offline fallback and measured interaction burden (R14, R17, R32, R34) |

These relationships do **not** establish that any specific app, QR code or recording frequency will succeed. Phase C must compare genuinely different solution families with the same scenarios.

## 5. Explicit out-of-scope / unsafe shortcuts

1. No automatic attribution of damage or theft to the last key holder.
2. No automatic fines, spending approvals, disposal authority or relaxation of hostel purchase policy.
3. No claim that every on-ground pass of a racket needs to be scanned; this is exactly the friction trade-off to evaluate.
4. No retroactive imputation of damage occurrence time from discovery time.
5. No replacing physical stock audit with the 80:20 planning assumption or purchase bills.
6. No requirement that a security guard becomes an equipment-quality inspector.
7. No assumption that electronics are required; Phase C must test physical, lightweight and integrated workflows.
8. No unredacted student/guard personal data committed to this **public** repository.

## 6. Design maturity and exit criterion

B4 is complete as a **structured, testable, evidence-linked proposal** once all 40 requirements have a source, test, and status, and all P0/P1 requirements have a verification scenario. This does not mean the requirements have been accepted by stakeholders or that the prototype meets them. Phase C decides which solution mechanisms and service targets to adopt. Before a live pilot: obtain explicit permission, select user-data handling rules, audit sample method, and documented operational approvals.
