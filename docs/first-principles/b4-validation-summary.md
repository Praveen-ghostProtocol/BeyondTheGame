# B4 — Specification Integrity Check

**Scope:** Internal consistency and completeness of research-derived documents, **not** real-world functionality or validation.

## Test status

Executed from repository root:

```sh
python -m unittest discover -s tests -p 'test_b*.py' -v
```

**Result:** 10 automated checks passed: four B3 mathematical-model unit tests and six B4 document-integrity tests. The B4 tests verify:

1. Stable, unique IDs for all 40 requirements and 32 acceptance scenarios.
2. All requirements have source provenance, status and verification method, with valid evidence references.
3. Every P0 or P1 proposed requirement appears in at least one acceptance scenario.
4. All twelve traceability chains reference valid evidence, requirements and tests.
5. The principal B4 documents are present.
6. The specification explicitly distinguishes the unmeasured baseline, the approved accountability metric and the need for authorized field tests.

**Not completed:** No acceptance test has been physically executed. All scenarios in `b4-acceptance-tests.csv` have `evidence_status = Not executed`; no design has been selected, field-trial access approved, or implementation proven.
