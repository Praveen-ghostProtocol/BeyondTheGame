# C2 — Preliminary design-only comparison

**Status: concept assessment only.** This table evaluates architectural affordances and likely trade-offs based on C1 design descriptions; it is **not** a controlled test result, validated score or selection.

| Comparison dimension | A: physical/procedural | B: lightweight QR/forms | C: integrated lifecycle |
|---|---|---|---|
| Unique asset labels + kits | Planned physical tags/manifests | Planned QR codes/forms | Planned registry/manifests |
| 24/7 borrowing | Designed for self-service paper | Designed for phone+fallback | Needs workable role/offline design |
| Separate room key from item custody | Separate guard key ledger and item card | Key record separate from scan | Independent KeySession vs PhysicalHandover |
| Concurrent unique-item issues | **Detection/reconciliation**, cannot guarantee preventing duplicate paper signs | Needs central checkout and conflict handling | Atomic server-side exclusivity by design, untested |
| Ground/team sharing | Team card, off-ground slip | Team lending + scan off-ground | Group account + controlled exception |
| Missing reported return | Open discrepancy on paper | Pending digital reconciliation | Discrepancy workflow and history |
| Damage/repair | Quarantine tag and repair board | Damage form, status/quarantine | End-to-end controlled repair workflow |
| Financial approval control | Existing office paperwork | Digital evidence, office remains authority | Role-restricted workflow, no auto-disbursement |
| Audit confidence | Requires **independent** physical checker | Requires **independent** physical checker | Requires **independent** physical checker |
| Connectivity dependency | None | Some; paper fallback required | Higher; safe offline procedure essential |
| Ongoing burden | Writing, filing, audits | Scanning, reconciliation | Training, technical support and updates |
| Relative implementation complexity | Lower by architecture | Medium by architecture | Higher by architecture |

## Provisional interpretation
- A could be sufficient where disciplined physical controls prove effective. It is not inherently inaccurate, but misses can be reconciled late.
- B may offer a strong **complexity–benefit compromise**, provided item/kit scans are actually performed and offline events are not silently overwritten.
- C offers explicit transactional and lifecycle capabilities, but cannot prove that recorded status mirrors physical reality without independent checks; features entail setup and maintenance costs.
- A **hybrid** may eventually outperform any pure concept, but that would be a reconstruction justified by actual C2 trials, not an assumed winner.

**Conclusion:** All three remain candidates. There is no valid quantitative ranking because **zero controlled comparison trials have been supplied**.
