# Operational transition - 25 November 2026

The owner requested normal operation from this point, removal of DEMO/SIMULATED interface labels, and preservation of every existing record, including earlier test entries.

Changed the hosted `meta.mode` configuration from DEMO to LIVE and recorded `operational_started_at`. New domain events now use OPERATOR_RECORDED; new independent audit snapshots use the existing independent-check eligibility rules. No earlier event, provenance value, equipment record, loan or account was edited, deleted or reclassified as field evidence. Historical test audits remain excluded from accountability metrics. The configuration update ran under the application's advisory write lock with checksum invariants.

Preservation check, before and after configuration change:

| Item | Before | After |
|---|---|---|
| Accounts | 11 | 11 |
| Domain records | 28 | 28 |
| Audit events | 34 | 34 |
| Domain-record checksum | `2eec9ce34a0e5692d9b3f0f7ab7261e2` | unchanged |
| Event checksum | `be83a2ebcfddf8b662d2a3740955e91f` | unchanged |

Removed test banners and copy from login, navigation, equipment registration, help, audits and QR preparation. Older event badges display Historical entry; new ones display Operator entry. Their underlying provenance is preserved. No free-text data was rewritten. The current print artifact is `output/pdf/BeyondTheGame_Equipment_QR_Labels.pdf`; the earlier pilot PDF remains available as a historical artifact. All 16 encoded IDs are unchanged.

Stitch project `2787590971872242739` supplied the operational copy refinement without a layout redesign. Production deployment `dpl_7Fe7HYLmununYtRw7d8J4MBnoiVB` reached READY. Hosted readiness returned LIVE. Secretary activity and QR pages were checked in Chrome; labels display Alaknanda and earlier events remain visible as Historical entry.

Validation: 107 Python tests passed; 34 Chromium integration checks passed against the real HTTP handler over byte-stream transport. The added checks confirm absence of demo/simulated labels on the rendered label page and continued presence of historical provenance in the API. Rendered the two updated PDF pages and decoded all 16 QR crops successfully. These are software checks, not new field observations.

Presentation readiness: research, first-principles transformers, requirements, alternatives, implementation and software verification can be presented now. Actual pilot timing, participant findings, independently audited baseline/improvement and actual team contributions must be reported from real evidence. Removing interface labels does not convert earlier tests into field results. `final/` remains reserved.
