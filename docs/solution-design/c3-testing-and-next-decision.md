# C3 — Test status, evidence gaps, and next decision

## Executed verification
- **31 passing unit tests:** Node.js `node --test tests/test_c3_engine.mjs` verified (logic tests only).
- **36 scenario-ID probes:** 24 implemented-logic passes; 12 design-only/not end-to-end tested; 0 failed in synthetic runs (`node models/c3/scenario_runner.mjs`). This is **not** 36 completed real-world scenarios.
- **Web UI:** HTML/JS source delivered and HTTP static file response checked; actual rendered browser interaction not certified because sandbox browser navigation was blocked by environment policy. Manual UI acceptance test pending.
- **Prior-phase regression tests:** Run with repository command below; record new executions rather than copying prior test numbers.

## What remains untested
- Actual scanning, device performance, camera support, offline reconciliation and synchronized multi-user concurrency.
- Real security, authorization, identity verification, privacy approval and institutional adoption.
- Student, captain, guard and secretary task times, including extra effort for checking physical item states.
- Independent physical accountability audits, inventory accuracy, repair time, procurement lead time and operating cost.
- All eight C2 non-negotiable gates, which remain `UNTESTED` from a field-validation standpoint.

## Trial approvals and resources to request from project owner later
1. Study site and permission: Alaknanda sports room or a small consented mock equipment set.
2. Participant roles, independent checker and privacy plan (avoid names/roll numbers in public logs).
3. Item types, consumables and kit manifest to be tested.
4. Acceptable additional match-day checkout time and scope of secretary/guard role changes.
5. Confirmation/adjustment of C2 criterion weights and any hard constraints prior to selecting a winner.

## Run commands
```bash
node --test tests/test_c3_engine.mjs
node models/c3/scenario_runner.mjs
python -m unittest discover -s tests -p 'test_*.py'
```

## Next phase
**C4 — Controlled human trials, empirical comparison, refinement and owner-approved reconstruction selection.** Do not assume C wins because it has more features. If physical trial data cannot be collected, present design mechanisms and limitations honestly and keep selection provisional.
