# Phase D software verification

**Executed:** 25 November 2026. **Provenance:** synthetic automated software checks only. These results do not establish physical accountability, field effectiveness, security certification, deployment networking or participant usability.

## Executed results

| Suite | Passed | Failed | Scope |
| --- | ---: | ---: | --- |
| Existing A–C4 Python regression checks | 33 | 0 | Research/model/specification and evidence integrity |
| Phase D Python domain and HTTP-handler checks | 57 | 0 | Persistence, concurrency, lifecycle rules, auth, roles, privacy and HTTP responses |
| Existing C3 JavaScript mechanism checks | 31 | 0 | Earlier A/B/C synthetic reference engine, retained unchanged |
| New QR pixel/identifier checks | 13 | 0 | Roundtrips, long IDs, inverted images, blank frames and unsafe/foreign payload rejection |
| Chromium integration assertions | 31 | 0 | Actual UI with the real HTTP handler and isolated SQLite across desktop/mobile and all eight roles |
| **Total** | **165** | **0** | **Software checks; zero participant field trials claimed** |

Python 3.11, Node v22.18.0, Chromium 154.0.8037.0; existing installed Playwright Core 1.64.0-alpha-1789764292000. Browser viewport checks used 1440-pixel desktop and 390×844 mobile. JavaScript syntax checks also passed. See [machine-readable summary](phase-d-software-results.json) and [screenshots](screenshots/README.md).

Commands executed from repository root:

```powershell
python -m unittest discover -s tests -p 'test_*.py' -q
node --test tests/test_c3_engine.mjs tests/test_d_qr.cjs
node tests/browser_e2e.cjs
```

The browser command uses an installed Playwright path and browser cache via environment variables; see `app/README.md` for ordinary setup. Test fixtures run in temporary databases, never the local interactive demonstration or real inventory.

## What the checks establish

- Two actual competing domain threads issue the same last available item; exactly one succeeds. Kit checkout rolls back all assets/quantities if one component is unavailable.
- Repeating the same command ID returns its original result; reusing it for another payload fails. Stale versions reject updates rather than overwrite newer custody.
- Request approval leaves custody at STORE until physical pickup. A declaration of return preserves outstanding custody; a separate checker receives actual components before inspection. Partial kit return leaves precisely the missing component outstanding.
- Full and partial off-group transfers require the receiving account's physical acceptance and preserve the original group's remaining manifest.
- Damage reports preserve location/custodian/loan and retain unknown occurrence/fault. Attribute-specific provenance is preserved. Guard key return never changes equipment custody; the same physical key cannot be handed out twice.
- Maintenance separates approval, vendor custody, repair completion, receipt and reinspection. Vendor return alone is not usable. Failed inspections allow reassessment without accidentally restoring availability.
- The reported procurement threshold is unconfirmed by default. Office confirmation, financial role and distinct quotes are enforced. Only physically received quantities enter stock; a duplicate ID midway through a receipt rolls back the entire transaction. No software payment is sent.
- HTTP handling rejects unauthenticated reads, wrong roles, missing CSRF, foreign origins and attempts to retrieve database/source paths. Session expiry/revocation, account disable, password changes and login throttling are exercised. Event SQL triggers reject deletion; corrections retain before/after/reason. This is targeted testing, not a penetration test.
- Students do not receive other borrowers' identities or financial records. Public aggregate export excludes identities, raw activity and free-text evidence references. Private runtime files are excluded from Git.
- Synthetic strict-accountability arithmetic produces 6/10 with two unknown and two contradicted cases; independent observations cannot come from the record's operator or custodian. Changed/unfinished samples do not silently enter metrics. Completed DEMO audits remain excluded from field accountability.
- Actual browser forms cover the eight roles, state-changing workflows, mobile navigation, manual scan fallback and camera-denial recovery. A generated canvas video stream goes through the real camera frame/decode loop, opens the matching asset and stops tracks; scanning never automatically borrows it. This is a simulated camera source, not physical hardware.
- QR codes are generated and decoded locally; plain IDs and same-origin deep links work, foreign/executable payloads fail. Label-sheet generation requires explicit selected registered IDs. Demo labels say DEMO ONLY; print CSS hides application navigation. No physical print command was issued.

## Transport limitation

An actual loopback HTTP-client attempt was blocked by Windows sandbox permissions (`WinError 10013`). Consequently, HTTP and browser integration use byte streams through the **same production `BaseHTTPRequestHandler` implementation**, JSON routes, session/cookie logic, authorization and durable database. Playwright route interception forwards requests to a persistent Python handler process; responses are not mocked. This verifies protocol/application behavior but does **not** certify listening sockets, HTTPS, reverse-proxy origin forwarding, internet deployment, multi-phone routing or camera devices. Those remain target-host checks.

## Refinements supported by observed software failures

| Observed failure | Refinement | Recheck |
| --- | --- | --- |
| Windows test DB could not be removed because context-managed SQLite handles were still open | Added deterministic connection closing around commit/rollback contexts | Entire Python suite passes and temporary test DBs clean up |
| An older C1 test decoded UTF-8 HTML using Windows' default CP1252 | Made its source read explicitly UTF-8 without changing research claims | All 33 prior Python checks pass |
| Open mobile sidebar covered the original menu toggle | Added a close control inside the sidebar and close-on-navigation behavior | Mobile open/close assertions pass |
| API-created test setup was not visible when a browser test revisited the same URL hash | Browser test explicitly refreshes stored state before each staged task | All browser lifecycle assertions pass |

These are code/test refinements supported by actual executions. They are **not** user-trial refinements or before/after hostel improvements.

## Evidence still pending

No physical inventory audit, controlled participant trial, actual field borrowing, phone-camera hardware check, printed-label test, label durability trial, measured tournament burden or measured before/after impact has been performed. No real resident accounts or transactions were introduced. C4 worksheets and gate statuses remain unchanged. The original comparative alternatives have not been scored using invented data. Core implementation/integration testing preceded implementation of printable sheets; only synthetic QR fixtures were generated in software tests. `final/` is empty.

## Publication

GitHub metadata appeared writable, but an actual write returned 403 `Resource not accessible by integration`. Direct Git HTTPS also lacked DNS access. Local commits and the standalone Git bundle preserve the implementation; no remote success is claimed. See [deployment handoff](../deployment/local-pilot.md).
