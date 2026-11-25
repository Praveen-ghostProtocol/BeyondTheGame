> **LATEST OWNER DECISION (25 Nov 2026):** Proceed to Phase D by building Alternative C (integrated lifecycle application) as a user-approved development direction, **without claiming C4 field trials occurred**. Print QR labels only after the app's scanning workflow is implemented and tested. See [Phase D launch decision](docs/solution-design/phase-d-launch-decision.md).

# Beyond the Game

First-principles systems research and redesign of shared sports-equipment management, beginning at **Alaknanda Hostel, IIT Madras**.

## Status
**Phase C4 — all eight owner policies approved 25 November 2026 (₹0 new spending), controlled-trial plan, evidence-gated readiness tools and a counterbalanced 216-run study schedule are prepared. Human trials, field validation, eight non-negotiable gates, and winner selection remain pending. No real accountability baseline or measured outcome improvement exists.** This repository package contains no invented measurements or fabricated incidents.

## Repository plan
- `docs/research/phase-a/` — A1–A4 findings, process maps, evidence, field protocols.
- `docs/project-governance/` — quality, privacy, and attribution rules.
- `data/templates/` — anonymized observation templates; no student personal details.
- `docs/first-principles/` — Phase B analyses, beginning with B1 functional architecture, custody/state models and traceability.
- `docs/solution-design/` — Phase C solution comparison and Phase D design (when produced).
- `app/` — Phase D implementation (when produced).
- `tests/`, `docs/testing/` — Phase E validation (when produced).
- `docs/deployment/` — Phase F deployment research (when produced).
- `final/` — reserved for six-slide final submission and evidence appendix (create only when ready).

Only meaningful deliverables should be committed. Never commit raw student ID data, unredacted register images, access credentials, node_modules, intermediate exports, or synthetic observations presented as real.

## Current Phase C4 deliverables
- [C4 controlled-trial playbook](docs/solution-design/c4-controlled-trials-playbook.md) and [provisional design review](docs/solution-design/c4-design-review-and-provisional-selection.md)
- [216-row unexecuted counterbalanced trial plan](data/templates/c4-counterbalanced-trial-plan.csv); 12 C2 scenarios, six order permutations, three concepts
- [24 hard-gate reviews, all UNTESTED](data/templates/c4-gate-evidence.csv); [editable trial readiness workbook](data/templates/c4-trial-readiness-workbook.xlsx)
- [Eight approved owner decisions](docs/solution-design/c4-approved-owner-decisions.md), [zero-budget field-trial kit](docs/solution-design/c4-zero-budget-field-trial-kit.md), and [approved-decision CSV](data/templates/c4-approved-decisions.csv)
- [Executable evidence-gated assessor](models/c4/assess_readiness.py), [trial-plan builder](models/c4/prepare_trials.py), [workbook builder](models/c4/build_trial_workbook.py) and [C4 integrity tests](tests/test_c4_trials.py)
- [C4 execution report](docs/solution-design/c4-code-execution-report.md), [evidence status](docs/solution-design/c4-evidence-status.md), and [C5 / Phase D conditional handoff](docs/solution-design/c4-c5-handoff.md)

**C4 tool checks:** 33 Python unit tests, 31 Node mechanism tests, and 36 fictitious scenario probes (24 mechanism paths / 12 design-only). This verifies code, not field outcomes. **No solution chosen.**

Run from repository root:

```bash
python models/c4/prepare_trials.py
python models/c4/assess_readiness.py
python models/c4/build_trial_workbook.py  # artifact_tool; set BTG_C4_WORKBOOK_OUTPUT to override location
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/test_c3_engine.mjs
```

## Previous Phase C3 deliverables
- [Runnable A/B/C concept lab](prototypes/c3/index.html) ([setup instructions](prototypes/c3/README.md)), [printable 12 scenario cards](prototypes/c3/scenario-cards.html)
- [C3 prototype development report](docs/solution-design/c3-prototype-development.md), [verification and next decision](docs/solution-design/c3-testing-and-next-decision.md)
- [C3 per-scenario evidence-class coverage](docs/solution-design/c3-mechanism-coverage.csv), [synthetic execution log](data/scenarios/c3/c3-mechanism-checks.json)
- [Shared test mechanism engine](models/c3/engine.mjs), [scenario runner](models/c3/scenario_runner.mjs) and [unit tests](tests/test_c3_engine.mjs)
- [Blank field-trial preparation checklist](data/templates/c3-trial-setup-checklist.csv)

Run `node --test tests/test_c3_engine.mjs` and `node models/c3/scenario_runner.mjs`. 31 unit tests passed and 36 synthetic scenario-ID probes were executed (24 code-path checks passed, 12 design-only/not end-to-end, 0 failures). **These are NOT participant trials, physical verification, security validation, or measured comparative outcomes.** Browser interaction has not been certified in this environment.

## Previous Phase C2 deliverables
- [Controlled comparison protocol](docs/solution-design/c2-comparison-protocol.md) and [12 task scripts](docs/solution-design/c2-scenario-protocol.csv)
- [Preliminary design-only comparison](docs/solution-design/c2-preliminary-design-assessment.md) (**not evidence of impact**)
- [Decision framework](docs/solution-design/c2-decision-framework.md), [original proposed weights, now owner-approved](docs/solution-design/c2-proposed-criteria.csv) and [eight untested gates](docs/solution-design/c2-nonnegotiable-gates.csv)
- [Editable C2 evaluation workbook](data/templates/c2-comparison-workbook.xlsx), [CSV data dictionary](docs/solution-design/c2-data-dictionary.md), [blank trial](data/templates/c2-trial-log.csv), [audit](data/templates/c2-independent-audit.csv) and [cost](data/templates/c2-cost-log.csv) templates
- [C2 → C3 handoff](docs/solution-design/c2-c3-handoff.md) and [readiness status](docs/solution-design/c2-readiness-summary.md)
- [Reproducible evaluator](models/c2/evaluate.py) and [unit tests](tests/test_c2_comparison.py)

Run `python models/c2/evaluate.py --trials data/templates/c2-trial-log.csv --audits data/templates/c2-independent-audit.csv` (returns `NOT MEASURED` with blank data). No actual participant trials have been run.

## Previous Phase C1 deliverables
- [Alternative concept overview](docs/solution-design/c1-concept-development.md) and [C2 handoff](docs/solution-design/c1-c2-handoff.md)
- [Physical/procedural design](docs/solution-design/c1-alternative-a-physical.md), [lightweight QR design](docs/solution-design/c1-alternative-b-lightweight.md), [integrated lifecycle design](docs/solution-design/c1-alternative-c-integrated.md)
- [40-requirement design coverage](docs/solution-design/c1-requirements-coverage.csv), [32-scenario design matrix](docs/solution-design/c1-scenario-design-matrix.csv)
- [Printable physical forms](prototypes/c1/a-physical-forms.html), [interactive low-fidelity concept gallery](prototypes/c1/concept-gallery.html)
- [C1 documentation validation tests](tests/test_c1_concepts.py)

## Previous Phase B4 deliverables
- [B4 requirements specification](docs/first-principles/b4-requirements-specification.md) and [40-row requirements register](docs/first-principles/b4-requirements-register.csv)
- [B4 workflow and domain contracts](docs/first-principles/b4-workflow-and-domain-contracts.md)
- [B4 acceptance-test catalog (32 scenarios)](docs/first-principles/b4-acceptance-tests.csv)
- [B4 research-to-requirements traceability](docs/first-principles/b4-evidence-to-requirement-traceability.csv)
- [B4 pending decisions](docs/first-principles/b4-decision-register.md)
- [B4 to Phase C comparison brief](docs/first-principles/b4-phase-c-handoff.md)
- [B4 specification validation tests](tests/test_b4_specification.py)

## Previous Phase B3 deliverables
- [B3 full transformer analysis](docs/first-principles/b3-transformer-analysis.md)
- [B3 instructor-ready summary](docs/first-principles/b3-executive-summary.md)
- [B3 source classes and assumptions](docs/first-principles/b3-model-assumptions.md)
- [B3 validation protocol](docs/first-principles/b3-validation-protocol.md)
- [B3 traceability](docs/first-principles/b3-transformer-traceability.csv)
- [B3 → B4 handoff](docs/first-principles/b3-b4-handoff.md)
- [B3 editable formula workbook](data/baseline/b3-transformer-model.xlsx)
- [B3 scenario generator](models/b3/scenario_model.py) and [generated toy scenarios](data/scenarios/b3/README.md)
- [Reproducible formula workbook builder](models/b3/build_workbook.py)
- [Equation tests](tests/test_b3_scenarios.py)

Run from the repository root:

```sh
python models/b3/scenario_model.py
python -m unittest discover -s tests -p 'test_b3*.py' -v
python models/b3/build_workbook.py  # requires artifact_tool
```

All B3 numerical scenario results are **explicitly hypothetical**; real item accountability is **not measured**.

## Previous Phase B documents
- [B2 causal/Five Whys analysis](docs/first-principles/b2-causal-analysis.md)
- [B2 feedback and stock-flow model](docs/first-principles/b2-causal-loops.md)
- [B2 testable hypothesis matrix](docs/first-principles/b2-hypothesis-validation.csv)
- [B2 trade-off and risk register](docs/first-principles/b2-tradeoff-risk-register.csv)
- [B2 to B3 quantitative handoff](docs/first-principles/b2-b3-handoff.md)

## B1 foundation
- [Functional/system decomposition](docs/first-principles/b1-functional-system-decomposition.md)
- [Asset state, custody and exceptions](docs/first-principles/b1-state-and-custody-model.md)
- [B1 requirements-to-evidence traceability](docs/first-principles/b1-requirements-traceability.csv)

## Read next
- [A1 field study](docs/research/phase-a/a1-field-study.md)
- [Detailed A2 current-state maps](docs/research/phase-a/a2-current-state-process-maps.md)
- [A2 review and design constraints](docs/research/phase-a/a2-review-and-design-constraints.md)
- [A3 provisional baseline and scenarios](docs/research/phase-a/a3-baseline-study.md)
- [A3 accountability audit protocol](docs/research/phase-a/a3-accountability-audit-protocol.md)
- [A3 editable baseline workbook](data/baseline/a3-baseline-model.xlsx)
- [A4 executive synthesis](docs/research/phase-a/a4-executive-synthesis.md)
- [A4 problem prioritization](docs/research/phase-a/a4-problem-prioritization.md)
- [A4 evidence gaps and validation backlog](docs/research/phase-a/a4-evidence-gaps-and-validation.md)
- [A4 traceability matrix](docs/research/phase-a/a4-traceability-matrix.csv)
- [A4 Phase B handoff](docs/research/phase-a/a4-phase-b-handoff.md)
- [A3 baseline plan (historical draft)](docs/research/phase-a/a3-measurement-plan-draft.md)
- [A1 provisional process map (historical)](docs/research/phase-a/a1-provisional-process-map.md)
- [Evidence register](docs/research/phase-a/a1-evidence-register.csv)
- [Research protocol](docs/project-governance/evidence-protocol.md)

## Team
- Akshath M — ME23B010
- Akash Rudra — ME23B095
- Praveen Kumar S — ED23B038

Actual contributions remain to be recorded from completed work.
