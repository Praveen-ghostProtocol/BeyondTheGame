# Phase D application

Working integrated application for Alaknanda Hostel. Python 3.11+ is the only runtime dependency. The frontend implements the dashboard, inventory drawer and mobile scanning design generated in Stitch. Earlier research and C3 prototypes remain intact.

## Open the isolated demonstration

From the repository root:

```powershell
python app/server.py --demo
```

Open **http://127.0.0.1:8000**. On first start, eight role accounts and the **synthetic** provisional 15-item mix are created. Credentials are generated locally in `app/private/demo-access.txt`; no password is committed. Usernames: `secretary`, `student`, `captain`, `checker`, `guard`, `maintenance`, `office`, `admin`. All demo accounts share the generated demo-only password. Restarting preserves data. Never reuse a demo password for real accounts.

The default demo is `app/private/demo.sqlite3`. Its mode is permanently DEMO; events and audits remain synthetic. No demo observation contributes to the field accountability metric. Label sheets are visibly DEMO ONLY.

## Initialize real use separately

```powershell
python app/server.py --init
python app/server.py
```

Initialization prompts for the first administrator and a password of at least 12 characters. The separate `app/private/live.sqlite3` starts with **no equipment and no residents**. Register real assets, authorized operators and pseudonymous resident accounts. Unknown initial condition enters inspection. Obtain the necessary local consent and operating arrangements before a live pilot.

Administrator creates accounts and assigns roles. Give credentials privately. Secretary manages the registry and borrowing; office confirms procurement policy and records financial authorizations. The reported ₹10,000 split is **unconfirmed by default**, so financial approval is blocked until office confirmation. Admin is a superuser; a real separation-of-duties deployment should use distinct secretary and office accounts.

## Workflows available

- Durable inventory, permanent IDs, sport/location filters, stock quantities, kit manifests and authorized corrections.
- Routine 24/7 requests, separate actual pickup, pre-approved captain kits, atomic checkout and partial returns.
- Return declaration → separate physical receipt → authorized condition inspection.
- Accepted off-group transfers of an entire borrowing or selected team components, with remaining custody preserved.
- Damage reports including unidentified items, discovery provenance and secretary acknowledgement.
- Assessment → approval → vendor custody → repaired → physically received → reinspection. Failed repairs can be reassessed or cancelled in-store.
- Need/rationale, distinct quotations, office approval, payment provenance and partial physical receipts linked to assets or stock lots. No automatic payments.
- Independent key records, inspection/audit snapshots, honest analytics, append-only history, interrupted-movement reconciliation and anonymous aggregate export.
- Camera QR scanning with a bundled decoder, manual ID fallback and opt-in printable label sheets.
- Account creation, role changes/deactivation, session revocation and password changes.

## QR labels

Core software integration was exercised before the label feature was implemented. Under **QR labels**, choose actual registered assets, prepare a sheet and use the browser's print command at 100% scale. IDs encode `BTG:ASSET:<ID>`; there are no personal details or deployment-specific URLs. No physical print job is issued automatically.

Actual phone-camera compatibility, lighting, label attachment/durability and field borrowing are **not validated**. Test one reversible label on the intended phone before attaching a batch. Cameras need localhost or HTTPS. A phone cannot use the server's localhost address; see the deployment notes for secure network access. Do not print the provisional demo inventory as real hostel labels.

## Verification

```powershell
python -m unittest discover -s tests -p 'test_*.py' -q
node --test tests/test_c3_engine.mjs tests/test_d_qr.cjs
```

Optional browser integration needs Playwright (development only):

```powershell
npm install --prefix tests --no-save playwright
npx --prefix tests playwright install chromium
node tests/browser_e2e.cjs
```

The browser runner can use a preinstalled package via `BTG_PLAYWRIGHT_PATH` and browser cache via `PLAYWRIGHT_BROWSERS_PATH`; set `BTG_PYTHON` if Python has another executable name. It drives Chromium against the real HTTP handler and temporary SQLite DB through byte streams because this execution environment blocks outgoing loopback connections. **It is not a TCP, HTTPS, production-load or physical-camera test.** No mocked domain results are used. See [the verification report](../docs/testing/phase-d-verification.md).

## Backups and recovery

```powershell
python app/server.py --db app/private/live.sqlite3 --backup app/private/backups/live-backup.sqlite3
```

Backup uses SQLite's consistent online-backup API and refuses to overwrite an existing file. Stop the server before restoring a chosen backup to the live database path; keep a copy of the current DB first. Treat backups, database journals and demo credentials as private. Database modes must not be changed to relabel synthetic data as live evidence.

In an interrupted handover, first refresh and compare actual equipment with the record. **Help & recovery** records a pending reconciliation case without changing custody. A secretary checks the item, records any permitted correction or outstanding return, and resolves the case with references. Active loans cannot be silently overwritten through inventory correction.

## Deployment boundary

The included HTTP server is a local classroom/pilot application. It has transaction-safe persistence and access controls; it is not certified for internet-scale production. For phone access use a trusted HTTPS reverse proxy, preserve its browser-facing Host header, and configure:

```powershell
python app/server.py --host 0.0.0.0 --origin https://your-approved-host.example --secure-cookies
```

Keep the backend private behind that proxy. Test actual sockets, TLS, cookie behavior, backups and authorized phone access on the deployment host before real use. Public deployment, managed hosting, email delivery and cloud identity-provider integration have not been performed. See [architecture and operational limits](../docs/implementation/phase-d-architecture.md).
