# Direct student scan, borrow and return

Owner correction, 25 November 2026: routine borrowing should be scan → borrow → play → scan → return. Students should not manage an approval request for ordinary equipment.

The student asset drawer now presents **Borrow this item** when available and **Return this item** when the signed-in student holds it. One confirmation records collection; the second scan records a return declaration for that exact asset. A scan alone never changes custody accidentally. Repeated return is not offered after declaration. Damaged or unavailable items cannot be borrowed.

`borrow_now` reuses request authorization and pickup validation inside one database transaction. The request row is an internal policy record, not a separate user step. Checkout either commits the complete loan or leaves no request/loan behind. Idempotency, shared write locking, account ownership and availability checks apply. Disabled routine pickup policy and team/kit approval cannot be bypassed. Existing pending requests are preserved for collection or cancellation; previously collected routine records are omitted from the approvals queue.

Student return time is a declaration. Checker receipt and condition inspection remain separate: a QR code does not establish that the item is physically present or usable. Student catalog responses retain privacy filtering; the return action resolves only the student's own outstanding loan without requiring a public loan identifier.

UI/UX refinement used Stitch project `2787590971872242739`, screen `4db409d70bb146acad7f0f5e1f7930e5` (Student Scan, Borrow & Return), preserving the existing components and green/lime design.

Executed local verification: 107 Python tests passed, including six direct-borrow tests for lifecycle, idempotency, rollback, approval/ownership constraints, eligible roles and competing borrowers. The complete Chromium suite passed 32 checks against the real HTTP handler over byte-stream transport. Camera denial/video tests remain simulated; these are not phone-camera or field trials.

Hosted deployment `dpl_A7ZKGTDLH7txioTo719NbPvSvXfA` reached READY. A student session used the scanner's manual-ID fallback for synthetic `BD-003`, directly borrowed it with no separate approval step, scanned again and recorded its return. Loan `LOA-1e394273f3b1` remains RETURN_REPORTED awaiting separate checker receipt, deliberately preserving the distinction between a software declaration and physical verification. No real equipment was moved or inspected in this software smoke check. All 13 QR decoder tests also passed.
