# A2 — Process-mapping review and design constraints

**Status:** Draft synthesized from sports secretary interviews; no physical audit or additional informants yet.

## Directly reported operating realities

1. The room is open via guard-controlled key **24/7**, and all stored equipment is hostel-owned.
2. Guard retains the initial signer's ID until that signer returns the checked-out key; multiple students can nevertheless access equipment while that key is out.
3. Students can pass equipment to other players on the ground, and occasionally another student takes it away and returns it later.
4. The sign-out register has student details, *intended* equipment, issue/return timestamps and student signatures. Guard does **not** verify actual items removed or returned.
5. Item damage timing and responsible individual are generally untraceable. Damaged and usable items are not segregated; damage often emerges only when someone asks for new equipment.
6. Sports secretary owns purchasing, repairs and final discarding decisions; security guard is responsible for access/register rather than equipment inspection.
7. Tournament captain can take a whole kit using the usual registration or with sports secretary's known permission **without an entry**, to avoid pre-match administrative burden.
8. Existing purchases are evidenced by bills, but no systematic location/condition inventory exists. All purchased items go to common sports room.
9. Secretary reports that sports are generally treated equally in purchasing, though hostel office prioritizes medal-winning sports when allocating scarce funds.
10. Realized pain is particularly evident in accountability, late damage discovery, repair/replacement and procurement effort; issue-time/search complaints are not prominent.

## Prioritized process gaps (hypotheses, not measured severity)

| Code | Gap | Why it matters | Evidence status | What to validate next |
| --- | --- | --- | --- | --- |
| G1 | Declared items differ from verified custody | Can't reliably identify what left the room | Reported no verification | Sample declaration-to-physical-item reconciliation |
| G2 | Informal on-ground transfers not recorded | Initial borrower may not be responsible for later damage | Reported transfers | Anonymous transfer frequency / chain scenario |
| G3 | Room entry possible during outstanding key loan | Key-control and equipment-use boundaries differ | Reported; mechanics unclear | Clarify entry mechanics and access overlap |
| G4 | Return lacks item and condition check | Missing/damaged items may go undetected | Reported | Small return-condition sample |
| G5 | Damage discovered only after subsequent request | Delayed maintenance, unavailable items | Reported | Date-stamped actual damage examples if available |
| G6 | Tournament kit exception bypasses register | High-value kits may lack a formal issue event | Reported | Frequency and kits/components involved |
| G7 | Purchases recorded only by bills | No real-time inventory or lifecycle trace | Reported | Reconcile a few invoice lines with active items |
| G8 | Repair/procurement coordination has external dependencies | Can prolong downtime and burden secretary | Reported; not timed | Historic quote/payment/collection milestones |
| G9 | Priority under budget pressure depends on sports outcomes | Fairness/utility trade-off in procurement | Reported | Clarify whether rule documented and how applied |

## Critical design constraints for later phases (not solution commitments)

- **Low-friction match-day operation** is essential: any replacement process must not impose a lengthy sign-out on captains immediately before competition.
- **Student self-service and 24/7 access** should remain feasible; do not assume a guard will inspect every racket or bat.
- **Shared assets and bundles** must be treated differently: captain-issued kits can contain multiple individual items, while cheap consumables may be counted by quantity.
- **Transfers between students** need a proportional accountability model, rather than assuming the original signer physically holds an item throughout use.
- **Condition detection** is likely more important than reducing shelf-search time, which was reported as generally easy.
- **Procurement approvals and repair authorizations** must reflect actual hostel controls; software cannot change official spending authority.
- **Privacy:** public repo must exclude personal register content, student IDs, signatures and identifiable borrower histories.

## Key finding and next phase

The existing system has an **access-recording workflow without a reconciled item-lifecycle workflow**. This is supported by the sports secretary's process description, not yet by physical audit, and does not prove that any student intentionally mishandles equipment.

**A2 ready for user review.** A3 should prioritize quantifying stock condition, document vs physical discrepancies, damage detection delay, procurement/repair turnaround, exception rates, and administrative effort **before** choosing a product or optimizing for issue speed.
