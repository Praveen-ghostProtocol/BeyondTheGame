# Phase D: integrated application architecture

Date: 25 November 2026. Implementation direction: owner-selected Alternative C, from `phase-d-launch-decision.md`. C4 field trials remain deferred and unchanged. This is implementation and synthetic verification evidence, not a measured research winner.

## Sources used

Read the handoff `START_HERE.md`, official `FPT_Term_Project_Official_Brief.pdf`, original proposal, A4 research synthesis, A3 audit protocol, B4 requirements/register/acceptance catalogue/domain contracts, C1 integrated concept, C4 owner decisions and evidence status, and C3 engine. The official brief supersedes the original proposal's old exclusion of implementation. Final submission remains at most six slides, four appendix pages and an optional two-minute video link. Contributor attribution, AI assistance disclosure and actual before/after evidence still belong in the eventual academic submission. `final/` has not been populated.

The first-principles links remain explicit: **Decompose** access/request/pickup/return/inspection; **Aggregate** mutually exclusive durable stock plus separate quantity lots and kit manifests; **Normalize** audit numerator/denominator and category stock; **Perturb** competing pickups, interruptions and partial returns without pretending these are human trials.

## Architecture decision

Use Python 3.11 standard-library HTTP handling, SQLite WAL transactions, and an HTML/CSS/JavaScript frontend. The conversation's Next.js/PostgreSQL/managed-auth stack was provisional. No existing Phase D stack was present. This implementation is locally runnable without installing packages, paid hosting, a database account or identity-provider credentials. It preserves relational constraints on users/sessions/operations and indexed typed records with JSON domain payloads. Strict command validation, permission checks and one write transaction surround all multi-record workflows.

Trade-offs: the standard-library HTTP server is suitable for a bounded local classroom/pilot service, not a certified public production service; SQLite serializes writers; typed JSON records require application-level cross-record invariants. The current single-facility architecture deliberately matches studied scope. For wider adoption, migrate records to explicit PostgreSQL tables and a supported production web service, use institutional identity, and test deployment load and privacy. No multi-hostel tenancy or managed auth provider is claimed.

| Component | Responsibility |
| --- | --- |
| `app/domain.py` | Authorized commands, state transitions, snapshots, metrics and transaction boundary |
| `app/schema.sql` | Versioned SQLite schema, users/sessions, indexed records, append-only events and idempotency ledger |
| `app/security.py` | PBKDF2 password hashing, throttled authentication and persisted hashed session tokens |
| `app/server.py` | Static-file allowlist, JSON API, CSRF/origin checks, setup, demo isolation and backups |
| `app/static/app.js` | Stitch-derived role-aware responsive UI; no browser-local mock database |
| `app/static/scanner.js` | On-device video frames, QR decoding, identifier validation and manual fallback |
| `tests/http_transport.py` | Byte-stream HTTP integration transport for restricted environments; same production handler |

## Data and transaction contracts

- Unique `(kind,id)` identities, monotonic record versions and explicit timestamps. Kits reference unique durable IDs and optional consumable quantities; kits never add to the durable census.
- Requests are not reservations or physical issues. Routine eligible individual requests use configurable 24/7 self-pickup authorization; captain/team kits require secretary pre-approval. A successful pickup checks every durable component and consumable quantity and commits the borrowing and all state changes atomically.
- SQLite `BEGIN IMMEDIATE` plus current-state checks ensures two competing pickups cannot both succeed. Commands require an actor-scoped idempotency key bound to the entire payload. Replaying a successful command returns the original result; changing its payload under the same key is rejected.
- Return declarations preserve the outstanding borrower/custodian. An authorized separate checker confirms actual receipt; received items go to inspection or quarantine. A returned key changes no equipment state. Partial returns leave only unreceived components outstanding.
- Team internal passes remain under team responsibility. Off-group transfers require an offer and recipient physical acceptance. Partial transfer creates a linked recipient borrowing while the original captain retains outstanding components. Transfer acceptance rejects changed source custody.
- Damage discovery does not move an item or imply the last borrower/key holder is at fault. Unknown occurrence time is stored as null. Location/custodian/condition each retain their own evidence time, source, confidence and actor. A damage-only change preserves location/custody provenance.
- Vendor handoff requires prior receipt from any active borrowing. Assessment, authorization, vendor custody, completion, receipt and inspection are different milestones. Failed reinspection preserves quarantine and allows reassessment. Cancellation is available only while equipment is in store. Retirement requires secretary/admin and reconciled outstanding custody.
- Procurement amounts are integer paise. Threshold and policy confirmation are configurable. Unconfirmed policy blocks office approval. The lower route needs quotation evidence; the threshold and above needs three distinct vendors. Approval and payment provenance are explicit office/admin actions. Receipt enrolls only the actual quantity; durable purchases begin in inspection. The app never transfers money or automatically approves a purchase.
- Corrections preserve before/after/reason events. Database triggers reject event updates and deletions. This is application append-only history, **not cryptographic protection against a person with direct database-owner access**.
- Offline/conflicting movement is recorded as pending reconciliation without overwriting asset state. No automatic offline custody queue or silent merge is claimed. Forms retain command IDs for safe retries during the current interaction; unresolved real movement must be independently checked.

## Audit and analytics semantics

A snapshot freezes the sampled eligible durable records and their versions. Observations must be made by an authorized checker distinct from the latest record operator and custodian, within 15 minutes of the snapshot and before the individual record changes. Closing requires an observation for every sampled item; UNKNOWN is accepted as unknown and kept in the denominator. Attributes are compared separately; no observation silently corrects inventory.

The displayed strict numerator counts all-three-correct items with no unknown attribute. Denominator is all sampled eligible durable items. Assessability, conditional accuracy, unknowns and contradictions are separate. The latest completed **non-simulated** audit is a historical snapshot, never an assertion that current inventory remains correct. Unclosed audits do not count. DEMO audits never count as field results. An operator-entered field claim still requires actual independent physical work and evidence; the software cannot verify an operator's honesty.

Available stock is a ledger classification, not the accountability metric. Category shares use active durable denominators, exclude retired items, and show unknown/inspection with unusable stock. Consumables remain quantity balances. Repair lead time counts completed cases with both recorded endpoints. Request collected/decided counts are descriptive; no timed service-window rate is claimed. Baseline improvement, participant burden and tournament checkout time remain NOT MEASURED. No fines are created.

## Authentication, privacy and operations

Passwords: unique random salt and PBKDF2-HMAC-SHA256 with 310,000 iterations. Session tokens: 256 random bits; only SHA-256 hashes persisted, 12-hour absolute expiry. Cookies: HttpOnly, SameSite=Strict, Secure with the production flag. Mutations check session-specific CSRF and the configured exact origin and Host. Eight failed attempts for a client/account bucket produce a 15-minute throttle. Session revocation follows account changes, logout or password change. A managed provider, MFA, email reset and institutional SSO are not implemented; administrator provisioning and password changes cover the local application scope.

HTTP serves an explicit static allowlist; no arbitrary paths, databases, source files or credentials are served. Request sizes are capped. Static scripts/styles are local, with a restrictive CSP and no frame embedding. QR scanning never uploads camera pixels. There are no third-party fonts, CDNs or image services at runtime. Shared student catalogue redacts other borrowers and evidence actors; full operational histories and finance are role-restricted. Public exports use an aggregate-only whitelist rather than raw transactions or free text.

Database files, WAL/SHM journals, credential files, backups, temporary browser state and dependency directories are excluded from Git. Private filenames remain in `app/private/`. No real resident data was introduced. The demo mix is exactly a synthetic illustration of the approved provisional trial mix, not an audited stock register. Database connections close deterministically, including on Windows, and online backups use SQLite's backup API.

## Remaining deployment and field work

The server can run locally. Browser tests use real handler byte streams because outgoing loopback is denied by the execution sandbox. These tests do not certify TCP routing, reverse proxy settings, HTTPS, multi-device access, phone camera hardware, printed QR legibility, labels remaining attached, independent operator diligence or actual hostel permissions. Check those on the intended deployment and devices. Managed hosting/public deployment has not been performed. Maintain paper/key continuity if devices or network fail.

The owner's instruction to build first was followed. Core integration was tested before QR label implementation. Software QR tests use generated synthetic pixel/video fixtures; no QR code has been physically printed or affixed. Real inventory enrollment and one-label phone preflight precede real batch printing.
