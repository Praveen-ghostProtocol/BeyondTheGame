# C2 measurement data dictionary and reporting conventions

The three input CSVs in `data/templates/` contain **headers only**. No simulated or observed rows are present.

## Trial log
- `trial_id`: unique test attempt identifier (not student ID).
- `participant_code`: anonymized actor/team code, non-identifying to readers.
- `scenario_id`: C2-S01 .. C2-S12; `concept_A_B_C`: A, B or C.
- `order_position_1_2_3`: 1–3 within counterbalancing schedule.
- `setting_STAGED_or_LIVE`: STAGED or LIVE. Simulated cases must not be called live pilot evidence.
- `source_type_OBSERVED_or_SIMULATED`: OBSERVED or SIMULATED; measured staged user task may still be OBSERVED with setting=STAGED.
- `completed_Y_N`, `total_seconds`: actual observed outcome and elapsed time. Never fabricate missing time; mark blanks.
- `student_active_seconds`, `guard_active_seconds`, `secretary_active_seconds`: time per actor, not necessarily additive due to simultaneous activity.
- `recording_actions`, `errors_count`, `discrepancies_resolved_count`, `discrepancies_unresolved_count`: nonnegative integer event counts.
- `ground_truth_expected` / `observed_outcome`: describe discrepancy behavior without identifying borrowers.
- `evidence_reference`: location of consented evidence or private reference identifier; no personal data in repo.

## Audit log
- `asset_code_ANON`: anonymized item token; no person identifiers.
- `eligible_Y_N`: only eligible records enter denominator; all exclusions must be justified.
- `location_correct_Y_N_UNKNOWN_CONTRADICTED` and equivalents for custody and condition: `Y` (independently correct), `N` (verified wrong), `UNKNOWN` (unassessable/unavailable) or `CONTRADICTED` (two observations conflict; requires adjudication).
- Strict accountable requires `Y` on **all three** dimensions. Incomplete audit entries (blank) are not counted as verified correct and must be flagged for data-quality review.
- A self-asserted app or ledger value is **not** independent ground truth.

## Cost log
- `cost_type_SETUP_OR_RECURRING`: distinguishes one-time and annual costs.
- `source_class_ACTUAL_QUOTE_ESTIMATE`: invoices/quotes/estimates must not be blended without labels.
- `expected_recurrence_per_year` for recurring items; if unknown, leave blank and do not claim computed TCO.

## Reporting
For candidate A/B/C, report n, completed, median completed seconds, actor seconds, strict audit numerator/denominator, unknown count, contradicted count, gates passed/failed/untested and provenance. No records ⇒ `NOT MEASURED`, not 0%. Report staged and live datasets separately, not as equivalent.

## Reproducible analysis
`python models/c2/evaluate.py --trials data/templates/c2-trial-log.csv --audits data/templates/c2-independent-audit.csv --output /tmp/c2-summary.json` generates **measurement status only** until rows are added. Ingest only consented, anonymized data. Unit tests use synthetic fixtures **in memory** and are not written to the evidence directory.
