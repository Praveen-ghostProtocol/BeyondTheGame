# C2 — Decision framework (approval required before final selection)

## Primary metric
Verified three-attribute equipment accountability for eligible audited items: actual location, responsible custodian/team, usable condition. Audits must compare system records with **independently established physical ground truth**.

## Sequence
1. Define the configuration and user roles for each candidate without relaxing the same real-world scenario rules.
2. Test all non-negotiable gates. Mark `UNTESTED`, `PASS`, `PARTIAL`, or `FAIL` with source and recorded result. No design-only passes.
3. Evaluate the **same** scripted tasks. Report successes and failures, error rates, timed burden by role, independently audited triad correctness, and operational costs.
4. If any critical gate fails, require redesign/retest before considering any weighted composite. Use worst-case operational scenarios (night access, match-day kit, offline conflict).
5. For viable candidates, discuss the criterion weights with the user. Proposed unapproved weights: accountability 30%, workflow burden 20%, reliability 15%, tournament 10%, lifecycle 10%, total ownership cost 10%, privacy/adoption 5% (sum 100%). **No scores assigned until data exist.**
6. Document uncertainty, sample sizes, and whether comparisons are staged or live. Seek explicit project-owner approval for the selected reconstruction.

## Important design approvals needed later
- Which durable assets get individual IDs; which consumables are tracked by lots.
- Responsible team/captain rule for on-field sharing and exception handling off-field.
- Who is permitted to perform condition verification (not assumed to be the guard).
- Maximum acceptable match-time interaction overhead and priority between speed and accountability.
- Trial access, student consent, privacy, and controlled-pilot authority.
- Approval of decision weights after evidence review.

## Recording selection
At present record `NO SELECTION — A/B/C design comparison complete; staged and live evidence not collected`.
