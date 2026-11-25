# Pilot QR labels and student accounts

25 November 2026. The owner reported that borrowing and return were working and requested printable labels and three friend-testing accounts.

`output/pdf/BeyondTheGame_Pilot_QR_Labels.pdf` contains the original 15 IDs plus the newly registered `TT-rac-001`: 16 labels across two A4 pages. Labels use the app's exact `BTG:ASSET:<id>` format, with no student data or credentials. They are marked PILOT TEST and are scanned inside the BTG app, not with a generic phone URL scanner. Print single-sided at actual size/100%, cut on dashed borders, and attach with removable material only after mapping each ID to one specific item. Test one printed label before applying the whole batch. The registry's quarantined BD-004 does not become borrowable from printing a sticker.

Build using `python scripts/build_pilot_labels.py` with ReportLab and Node available. QR matrices come from the app's vendored generator. Rendered both PDF pages for visual review and decoded all 16 PDF-rendered QR crops using the app's vendored jsQR decoder; all matched their intended IDs. This is a software rendering/decoder check, not a physical print or camera test.

Created `pilot-student-1`, `pilot-student-2` and `pilot-student-3` with separate random passwords and student-only permissions. Verified all three sign-ins against the hosted app and confirmed separate identities. Creation was recorded in the synthetic audit trail. Passwords/hashes and provisioning SQL stay under ignored `app/private/`; no credentials are committed or printed on labels.

The shared database remains DEMO. Friend testing must be documented separately with actual participant observations and limitations; its occurrence, physical inspection and measured outcomes are not established by account creation. No real names, roll numbers or other identity data were collected. `final/` remains reserved.
