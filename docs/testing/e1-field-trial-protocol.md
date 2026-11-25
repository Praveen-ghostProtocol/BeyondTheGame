# E1 — Same-day field trial: paper register vs. app

**Purpose:** produce the first *real* before/after evidence for slides 5–6. One staged script is run twice on the same 16 labelled items — once with the current paper register (OLD), once with the app (NEW) — and each run ends with an independent physical audit.

**Time:** ~75 minutes. **Cost:** ₹0 (labels already printed). **Setting:** STAGED, Alaknanda sports room. Results must be reported as *staged pilot, n = 16 items, 3 participants, one session*.

## People (use codes only — no names, roll numbers or ID cards anywhere in the data)

| Code | Role | Notes |
| --- | --- | --- |
| P1, P2, P3 | Borrowers | Use `pilot-student-1/2/3` accounts in the NEW run |
| C1 | Independent checker | Must **not** be P1–P3. Does physical truth audit and, in NEW, checker receipt/inspection |
| O1 | Observer / timekeeper | Stopwatch, fills timing sheet, asks the record queries. Praveen as secretary is fine |
| G | "Guard" | The real guard if willing, otherwise a teammate playing guard |

Before starting, tell every participant what is being recorded and that it is for a course project; continue only with verbal consent. Tick it on the data sheet.

## Equipment

The 16 labelled items: `BD-001…004`, `CB-001…002`, `CH-001…002`, `CP-001`, `FB-001…003`, `VB-001…003`, `TT-rac-001`.

- If one of them is genuinely damaged, use it as the damage item in E5 instead of BD-001 and note it.
- Otherwise tape a card reading **STAGED DAMAGE** to BD-001 for E5. Never damage equipment.
- The NEW run writes to the live app, and the event log cannot be deleted. That is acceptable — these are real trial events. Afterwards, C1 re-inspects BD-001 as usable so it returns to stock (if the damage was staged).

## Step 0 — Setup (10 min)

1. All 16 items in the sports room. C1 inspects each and writes its true condition in the audit sheet (`truth_condition`, both runs).
2. Sign P1–P3 into the app on their own phones; open **Scan QR** once to grant camera permission.
3. Prepare the OLD "register": a blank sheet with the same columns as the guard's book (name→use code, room, items declared, issue time, signature, return time).

## Step 1 — The event script (run identically in OLD and NEW)

| Event | What happens | OLD (paper) | NEW (app) |
| --- | --- | --- | --- |
| E1 | P1 borrows BD-001 and BD-002 | G writes P1 + "2 badminton rackets", hands key | P1 scans each → Borrow this item |
| E2 | P2 borrows FB-001 | G writes P2 + "1 football" | P2 scans → Borrow |
| E3 | P1 gives BD-002 to P3; P3 walks away with it | Nothing is written (as today) | P1 offers transfer to P3; P3 accepts in app |
| E4 | P2 returns FB-001 | G writes return time | P2 scans → Return; C1 scans → receives + inspects |
| E5 | P1 returns BD-001 with the damage card | G writes return time (damage only if P1 mentions it) | P1 scans → Return (reports damage); C1 receives + inspects as damaged |
| E6 | P2 borrows CB-001 and keeps it | G writes P2 + "1 bat" | P2 scans → Borrow |

**Timing rule (O1):** for every borrow and return, start the stopwatch when the student reaches the guard desk (OLD) or opens the scanner (NEW); stop when they are holding the item (borrow) or the item is back on the shelf (return). Include the guard/key step in both runs if the key is still needed. Time C1's receipt/inspection separately — it is extra work the new process adds and must be reported.

## Step 2 — Snapshot audit (10 min, after each run)

Physical truth at the snapshot should be:

| Item | Location | Custodian | Condition |
| --- | --- | --- | --- |
| BD-001 | STORE | HOSTEL | DAMAGED |
| BD-002 | OUT | P3 | as inspected |
| FB-001 | STORE | HOSTEL | as inspected |
| CB-001 | OUT | P2 | as inspected |
| other 12 | STORE | HOSTEL | as inspected |

C1 confirms this physically, and fills `truth_*` columns from what they **see**, not from the script.

Then O1 fills `rec_*` columns **from the system only** (the register sheet in OLD, the app in NEW). If the system cannot say which specific item, write `UNRECORDED`. Do not fill gaps from memory — that is the whole point.

Allowed values: location `STORE` / `OUT`; custodian `HOSTEL` / `P1` / `P2` / `P3`; condition `USABLE` / `DAMAGED`; any field may be `UNRECORDED`.

## Step 3 — Record queries (3 min, after each audit)

O1 (or a teammate who did not watch the run) answers from the records only, timed:

| Q | Question |
| --- | --- |
| Q1 | Where is BD-002 and who has it? |
| Q2 | Is BD-001 usable right now? |
| Q3 | Who has CB-001? |
| Q4 | Is FB-001 back in the room and usable? |

C1 marks each answer correct / incorrect / "can't tell" (counts as not correct).

## Step 4 — Label scan check (10 min, after the NEW run)

One participant scans all 16 printed labels with their phone inside the app. Record first-attempt success, number of attempts and seconds to open the item. This is the first physical camera + printed label evidence.

## Step 5 — Feedback (5 min)

Each of P1–P3: ease of OLD (1–5), ease of NEW (1–5), preference, one comment. Also ask G and C1 for one sentence each.

## Step 6 — Refinement

If anything fails or annoys people (unreadable label, confusing button, slow step), write it in `notes`. After the session, make one fix and repeat **only the affected event**, recording the re-run as a new row with `run = NEW-R`. This is the brief's required refinement.

## Recording the results

Fill in the printable sheet ([e1-field-trial-datasheet.html](e1-field-trial-datasheet.html)) on paper, then copy into the CSVs in [`data/field-trial/`](../../data/field-trial/). Set `source` to `OBSERVED` on each row you actually measured. Then run:

```
python models/e1/analyze_trial.py
```

It prints the before/after table for slides 5–6. Rows not marked `OBSERVED` are ignored, so blank templates report **NOT MEASURED**.

Take photos while you do this: labelled items on the shelf, a phone scanning a label, the mock register sheet (no names), C1 inspecting. Avoid faces unless the person agrees.

## Known limitations (state these on slide 6)

- Staged script, single session, 16 items, 3 borrowers — demonstrates the mechanism, not long-run hostel impact.
- OLD always runs first, so participants know the script by the NEW run (learning effect favours NEW on time, not on accountability — the register simply cannot record item-level custody).
- The checker step adds work the old process never did; report its seconds as a cost.
- Damage is staged unless a genuinely damaged item was used.
