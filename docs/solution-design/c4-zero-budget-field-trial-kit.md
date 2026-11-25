# C4 — Zero-spend, consented field-trial kit

**Status:** Ready-to-run protocol; **no human trials executed**. Based on owner approvals of 25 November 2026; see [decision record](c4-approved-owner-decisions.md).

## 1. Materials: zero new out-of-pocket spending
| Material | How to obtain with ₹0 spending | Restriction |
| --- | --- | --- |
| Real sports equipment | Existing Alaknanda hostel items, used with owner's approval | Do not damage, modify permanently or remove without authorization |
| Inventory identifiers | Existing markings or reversible handwritten temporary codes; use a separate map on an existing sheet | No purchased/adhesive tags required; avoid damaging surfaces |
| Phone and stopwatch | Personal devices already available | Opt-in; no compulsory app download or personal account |
| Working concepts | Existing C1/C3 printed/viewable prototypes and local browser/software | No paid services, hosting or QR label purchase |
| Trial log and audit | Reuse existing blank CSV/workbook templates; privately stored during collection | Never upload student identities to public repo |
| Damaged-equipment case | Previously unusable item if safe and permitted, **or** a fictional paper token | Never deliberately break an item |
| Tournament kit | Existing cricket gear or non-contact stand-ins from the equipment room | No disruption to real match preparation |

**Cost reporting:** Record new *out-of-pocket prototype spending* as ₹0 **only if no purchases occur**. Record existing assets, participant effort, electricity/data, and potential future hosting as in-kind/economic costs rather than asserting the system has no cost.

## 2. People and permissions
- Trial coordinator: project team under owner's authorization.
- Participants: **six consenting students or groups**; do not publish real identities.
- Independent checker: one or more authorized consenting individuals who do **not** perform the task being audited.
- Guard: normal key-management role only; do not add inspection, photography or tracking duties without explicit agreement.
- Trial may proceed only when participant consent, access authority, safe equipment use and privacy controls are confirmed **for each session**.

## 3. Preflight (before planned 216 scenario runs)
1. Assign anonymous participant and checker codes (e.g. P01–P06, V01); store any code-to-person list offline and privately, if absolutely needed.
2. Confirm allowed equipment, storage area, and an unobstructed test space; stage demo requests without changing normal equipment availability.
3. Independently establish and record the initial ground truth for location, person/group in custody, and item condition.
4. Open A's printable forms, B/C browser prototypes and the C2 scenario cards; ensure navigation works on available device(s).
5. Verify the independent audit method, trial timing rules, six counterbalanced orders and the 60-second **additional match-day** criterion.
6. Use two or three preflight scenarios to find instructions that confuse participants; record and explain any protocol change before formal testing. Do not silently pool preflight outcomes with the final comparison.

## 4. Each scenario trial
1. Confirm consent and document the trial ID/participant code. Avoid IDs that can identify students.
2. Restore the same starting equipment state across A/B/C.
3. Read the prewritten scenario exactly; log scenario, concept/version, operator and order.
4. Record success/failure, elapsed time, **participant/captain/guard/secretary active time separately**, steps and errors. For scenario S06, isolate extra match-day overhead.
5. Record what the system *claims* about the items after the task, **without** using it as physical ground truth.
6. An independent checker verifies actual **location + custodian/team + condition**. Log correct, wrong or unknown separately for each attribute.
7. Repeat comparable tasks across all three alternatives and order blocks; capture negative results without exclusion.
8. Keep raw participant evidence restricted locally; export only aggregate de-identified results cleared for public use.

## 5. Files to fill only with real outcomes
- [Planned trial plan (216 rows)](../../data/templates/c4-counterbalanced-trial-plan.csv) — remains `NOT_RUN` until a trial is executed.
- [Blank trials](../../data/templates/c2-trial-log.csv) and [blank independent audit](../../data/templates/c2-independent-audit.csv).
- [Eight gates × three alternatives](../../data/templates/c4-gate-evidence.csv): each `PASS` requires independent evidence and reviewer, not a code assertion.
- [Cost log](../../data/templates/c2-cost-log.csv): distinguish ₹0 incremental spending from nonzero in-kind or prospective operating costs.

## 6. Stop conditions
Stop or postpone a trial if it interferes with routine guard duties, reveals personal records, cannot verify consent or physical ground truth, risks equipment damage, causes unsafe crowding or cannot keep comparisons equivalent.

## 7. Claim discipline
Until independent audits are performed, **equipment accountability is not measured**; 80% usable stock and five-minute borrowing time remain recalled/assumed estimates. A clean prototype is not a verified improvement. Do not pick A, B or C until gates, human evidence and owner review are complete.
