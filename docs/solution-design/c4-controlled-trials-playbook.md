# C4 — Controlled trial, audit and refinement playbook

**Current status:** trial instruments and executable analysis **prepared**; no student/guard/captain trials conducted, no independent item audit, no field approval, no measured candidate winner. **Do not report simulation as field evidence.**

## 1. Study objective and scope
Compare the **same 12 C2 scenarios** across the three solutions developed in C1 and implemented at mechanism/prototype level in C3:

- **A:** numbered storage, paper issue/return/inspection forms and physical maintenance board;
- **B:** labels/QR-equivalent lightweight digital register and maintenance reporting;
- **C:** integrated item/kit lifecycle, controlled transitions, maintenance and procurement.

Primary outcome: independently verified **three-attribute equipment accountability** (actual location, responsible custodian/group, usable condition). An item is fully accountable only if all three attributes are verified correct by an independent checker. Distinguish unknown, contradicted, incorrect, and unassessable records. Do **not** use the candidate's ledger as physical ground truth.

Secondary outcomes: task completion, median completed-task time **with failure counts**, active actor-time (student, guard, sports secretary), steps, errors, equipment safety/condition, repair and procurement coverage, match-day burden, cost, privacy and adoption. The existing five-minute borrowing duration and 80:20 condition split are **informal assumptions**, not comparator measurements.

## 2. Design and experimental schedule
- The [C4 counterbalanced trial plan](../../data/templates/c4-counterbalanced-trial-plan.csv) contains **216 proposed, unrun rows** (12 scenarios × three concepts × six blocks). It is a workload proposal, **not** a statistical-power calculation or permission to deploy.
- Each scenario is attempted by six groups/participants, each completing the three concepts in one of six possible orders: `ABC`, `BCA`, `CAB`, `ACB`, `CBA`, `BAC`. This minimizes order imbalance. Assign anonymous participant/group codes only after consent.
- For every concept, start from an equivalent **known** set of tagged practice items; reset statuses/quantities/kit components between concept trials. Preserve comparable instructions and training, including paper-form familiarization. Record training time separately.
- Use the same facility conditions, prop inventory, scenario script, success definitions, and investigator prompts. An independent assessor verifies actual object/kit conditions after each run. Evaluators should not alter scenarios to favour one concept.
- Start with a **preflight and dry run** using mock props; then a controlled staged comparison; only later, if permitted, a live hostel pilot. Staged mock results must be labelled `STAGED`, not `LIVE`. Fictitious mechanism output is `SIMULATED`, not participant observation.
- Where six groups are impractical, record smaller n and uncertainty; never pad counts. For legitimate participant trials, use `OBSERVED` and preserve consent/authorization. Do not publish student IDs or identifiable photographs.

## 3. Material and people checklist
1. **Permission:** hostel/sports secretary permission for using item replicas/borrowable items; any guard participation requires their consent and administrative allowance.
2. **Equipment:** two independently identifiable badminton rackets, one other damaged *demo prop* (never actually damage usable equipment), some shuttlecock tokens, football, mock cricket kit (bat plus two pad pairs), storage zones, tags, QR-equivalent codes.
3. **Roles:** student, captain, custodian/checker, secretary/maintenance actor as needed. Do not force the guard into item inspection: this differs from the current Alaknanda role.
4. **Independent checker:** someone who can see the physical items, compare the recorded system status with reality, and log the three attribute judgements; should not be the participant completing the task.
5. **Timing:** stopwatch or screen recording with consent, measuring total elapsed time and actor-active time *separately* (overlapping actor work must not be summed as total elapsed time).
6. **Data control:** anonymous participant and asset codes; restricted local raw observations; publish only anonymized, approved aggregate evidence.

## 4. Preflight — mandatory before trials
- Owner approves: study access, participant roles, authority to modify operating practices, budget/props, permitted data handling and scope.
- Confirm eight C2 hard gates and **numeric or operational** thresholds where required: 24/7 access, room key ≠ item transfer, no duplicate confirmed issues, known damaged quarantine, offline conflict flagging, triad verification, minimal guard/captain burden, privacy/official financial approvals.
- Decide acceptable additional match-day checkout seconds **before** collecting times; avoid post-hoc targets.
- Confirm which items have unique IDs and which consumables use quantity tracking. Decide who authorizes condition verification and whether captains can act as responsible group custodians.
- Check that demonstration screens genuinely work in a browser; C3 browser interaction remained unverified in the prior environment.
- Ensure negative scenarios use props only; do not lose, damage or falsely accuse a student in real trials.

## 5. Run procedure for each scheduled row
1. Assign code from plan, consent, equipment set, scenario, concept, actor, order position; log training and setup time.
2. Independent checker records starting physical ground truth. Reset between variants.
3. Moderator reads the exact C2 scenario prompt; participant performs the task without coaching except predefined assistance.
4. Log completion, elapsed/actor-active time, steps, errors, exceptions and the evidence identifier in [blank C2 trial CSV](../../data/templates/c2-trial-log.csv).
5. Independently audit the post-task physical location, custodian/group and condition for every eligible sampled item in [blank C2 audit CSV](../../data/templates/c2-independent-audit.csv).
6. Execute the relevant hard-gate checklist and attach evidence; enter status only after verification in [C4 gate ledger](../../data/templates/c4-gate-evidence.csv).
7. Record user friction, potential harm, unexpected cases and tool constraints; reset the controlled state.
8. Before making changes, mark the candidate build/version. After changes, rerun matched cases and maintain the original results.

## 6. Scenarios and traceability
The authoritative scenario details are in [C2 scenario protocol](c2-scenario-protocol.csv): S01 night room access; S02 simultaneous last item; S03 consumable versus asset; S04 transfers; S05 missing item after key return; S06 partial kit return; S07 late damage; S08 repair inspection; S09 purchase discrepancy; S10 offline conflict; S11 independent triad audit; S12 training/usability and export checks. Link back to [32 B4 acceptance tests](../first-principles/b4-acceptance-tests.csv).

## 7. Refinement cycle
Choose one change **because a documented trial revealed a failure** (for example, confusing item-tag positions or high tournament effort), not because a feature is visually appealing. Record:
- Candidate + version before change;
- observation and independent evidence reference;
- hypothesized mechanism;
- exact rule/UI/process modification;
- same scenario test repeated after change;
- difference in outcome plus any newly introduced burden;
- decision to keep/revert and limitations.

Do not claim a before/after improvement unless both sides were actually tested. If no issue appears, document what tests justify keeping the design as-is.

## 8. Analysis and decision rules
- Run `python models/c4/assess_readiness.py` from project root; the tool rejects unconsented or unsupported observations and reports **no selected concept** automatically.
- Keep `STAGED` and `LIVE` results separate. Report per-concept sample size, strict triad n/N, unknown/incorrect/contradictory counts, task failures and actor burden.
- Evaluate **all 8 non-negotiable gates per concept** before scoring. A `PASS` requires an actual evidence reference and reviewer; C3 code tests alone cannot clear privacy or field safety gates.
- The [C2 weights](c2-proposed-criteria.csv) are **proposed, not approved**; even after approval, composite scores must not silently outweigh a safety/privacy failure.
- Candidate decision is an **owner approval** following evidence review. C offers broadest features but is not automatically best. A low-cost, robust physical/hybrid approach may win.

## 9. Reproducibility and run commands
```bash
python models/c4/prepare_trials.py
python models/c4/assess_readiness.py --output docs/solution-design/c4-empty-evidence-readiness.json
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/test_c3_engine.mjs
node models/c3/scenario_runner.mjs
```

Do not commit identifying field data to this public repository. An empty results template stays empty until ethically and legitimately populated.
