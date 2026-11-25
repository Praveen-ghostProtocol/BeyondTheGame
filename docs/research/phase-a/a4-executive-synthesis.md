# A4 — Integrated discovery synthesis and Phase A closure

**Study:** Alaknanda Hostel, IIT Madras. **Method:** first-person sports-secretary account, iterative clarification, and analyst-built desk models. **Date:** 2026-11-25. **Status:** research synthesis complete; quantitative field validation outstanding.

## Problem statement
Alaknanda has a 24/7 guard-controlled sports-room key and a handwritten issue/return register recording students and **declared** equipment. Students independently take and return items, may transfer them among peers, and may obtain access while the key is already issued. The guard does not verify item counts or condition. Under a tournament exception, team captains may remove complete kits with secretary permission but without a register entry. Consequently, the recorded key/declared-item process does not establish **verified item-level custody, whereabouts, or usable condition**. Damage generally reaches the sports secretary only when later demand exposes it. This is a process-control gap, not a measured loss frequency.

## Approved scope
- Primary facility: Alaknanda Hostel only; other hostels not independently studied.
- Lifecycle: inventory/acquisition; physical storage; issue, informal transfer and returns; condition; repair/replacement; tournaments.
- Primary metric: **strict fully verified equipment accountability**. For a defined sample and snapshot, count items whose location, custodian/responsible entity, and condition are each recorded and independently correct, divided by all audited individually tracked items. Also report evidence completeness and accuracy among assessable items. Not currently measurable.
- Secondary metrics: issuance/return time, discrepancy rate, equipment downtime, repair lead time, admin effort, purchase lead time, usable stock, exceptions.
- Protect privacy; no student names/roll numbers/ID images in the public repo.

## Confirmed via secretary testimony (NOT independently audited)
1. Approximately 400 hostel residents; badminton and volleyball daily, football and cricket every other day.
2. Guard retains student ID and records name, roll, room, declared equipment, issue and return timestamps and signatures; provides key; self-collection and self-return unverified.
3. Room is accessible 24/7; items generally easy to find despite messy storage; users have minimal expressed complaints.
4. Equipment may change hands on the ground or be carried away later; the issue log does not trace the later chain.
5. Tournament captains can borrow whole kits with prior secretary permission and no normal register entry.
6. Sports secretary decides repair/discard; damaged items can remain with usable ones; shop repairs and purchases involve office procedures.
7. Recalled cases: an allegedly returned but missing badminton racket; prior high-value (~INR 15,000) cricket bat broke and was replaced with a cheaper bat; do not assign blame or assert unproven root cause.

## Explicit assumptions, estimates and missing measurements
- 80% usable/20% damaged: **scenario input, not stock assessment**.
- ~5 minutes acquisition, ~2 minutes each walking and guard/register, 3–7 days repair: recalled estimates, not sampled.
- 20–22 sports-use occasions per week: **derived sports cadence**, not number of requests, distinct users or key issues.
- 20–66 hypothetical loan events weekly under 1–3-per-occasion cases: sensitivity scenarios only.
- No independently audited item count, accountable percentage, transaction volume, missing/damage incidence rate, trial permissions or procurement turnaround evidence.

## Evidence-backed synthesis
**Core insight:** the system tracks *key access* and *declared items* but not reliably synchronized *physical item custody and condition*. Information reconciliation and lightweight handover verification should be investigated; a digital platform is a **candidate, not a proven solution**. Existing ease of locating items makes retrieval-speed optimization a weak initial assumption. The key opportunity is information reliability without disrupting 24/7 access or tournament readiness.

## What Phase A does and does not prove
**Established from testimony:** current workflow and its lack of item-level verification; real reported exceptions/incidents; reported responsibilities and purchasing pathways.
**Not proven:** that the system has a specific failure/accuracy percentage; that digitalization, QR or new processes reduce damage or save money; why the cricket bat broke; how representative Alaknanda is of other hostels.

## Research completeness gate
- A1: interview synthesis completed for primary source; guard/student/office triangulation open.
- A2: process maps completed, including informal transfers, tournament exception, repair and procurement; external validation open.
- A3: operational definitions, scenario workbook and data-collection instrument built; **field baseline not measured**.
- A4: prioritization, evidence map and Phase B handoff prepared. Overall Phase A = **desk-study complete, field validation pending**.

## Files
- [Evidence register](a1-evidence-register.csv)
- [Problem prioritization](a4-problem-prioritization.md)
- [Assumptions and validation backlog](a4-evidence-gaps-and-validation.md)
- [Evidence-to-design traceability](a4-traceability-matrix.csv)
- [Phase B handoff](a4-phase-b-handoff.md)
- [Baseline specification](a3-baseline-study.md)
- [Audit protocol](a3-accountability-audit-protocol.md)
