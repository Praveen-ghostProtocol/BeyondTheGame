# C4 — Reproducible code-level execution report

**Category: SYNTHETIC / CODE-LEVEL — NEVER A HUMAN TRIAL.**

Execution source | Command | Outcome
--- | --- | ---
Python research/analysis regression | `python -m unittest discover -s tests -p 'test_*.py' -v` | 33/33 passed
C3 JS mechanism regression | `node --test tests/test_c3_engine.mjs` | 31/31 passed
C3 synthetic scenarios | `node models/c3/scenario_runner.mjs` | 36 probes: 24 implemented-path passes; 12 design-only; 0 failures
C4 counterbalanced plan | `python models/c4/prepare_trials.py` | 216 rows **planned/unexecuted**, equal A/B/C order positions
C4 evidence-gated assessment | `python models/c4/assess_readiness.py` | NO SOLUTION SELECTED; 0 observed results; 24 untested hard-gates
C4 workbook generation | `python models/c4/build_trial_workbook.py` | Exported editable trial coordination workbook; status `NOT MEASURED`, no raw participants

**What this does not test:** real QR camera/scanner performance, actual inventory state, physical audits, consent compliance in deployment, guard/captain burden, live network conflicts or cost efficiency. Do not use test-pass percentages as an impact claim in the term-project submission.
