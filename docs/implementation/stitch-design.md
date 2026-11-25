# UI/UX design provenance

The project owner explicitly requested Stitch for UI/UX during implementation on 25 November 2026. Stitch was used for UI/UX only. Application rules, authentication, persistence and testing were implemented locally from existing research/specifications.

Project: [Beyond the Game in Stitch](https://stitch.withgoogle.com/projects/2787590971872242739) (private).

| Generated screen | Screen ID | Applied pattern |
| --- | --- | --- |
| Secretary Dashboard – Beyond the Game | `174d8f8152ab4f38a0fbd792e0ef02f8` | White sidebar, facility topbar, pine/lime brand, metric cards, truthful accountability panel, attention queue and ledger status distribution |
| Equipment Inventory & Asset Drawer | `8f0a509c66c04bdba32a84ee17f1c4a0` | Dense filtered register, permanent IDs, condition chips and detailed history/action panel |
| Student Scan & Borrow Mobile | `a9330de654574d3aadf2387e81538f66` | Phone-first scan frame, manual fallback, asset preview and separated request/physical pickup |

Design system: **Utilitarian Athletic Inventory**, asset `f3e0816f8a8543b0ba465520eabd7339`. Implemented tokens: pine `#175c45`, dark pine `#004330`, lime `#c8f53c`, off-white `#f6f7f9`, white panels, subtle borders, compact spacing, strong hierarchy, small uppercase status labels and monospace equipment IDs.

Generated HTML was inspected as a design reference, then translated into locally served semantic HTML/CSS/JavaScript connected to the application API. CDN Tailwind, externally hosted logos/fonts and arbitrary demo names/roll numbers were not retained. Generated fictional metrics, facility room numbers, RFID references, audit schedules and institutional claims were discarded. The original design's dummy operational numbers are not research evidence. Runtime counts come from the database; independent accountability starts NOT MEASURED.

All role views reuse the generated visual system and established form/table patterns. All forms have labels, modal focus management uses native dialogs, keyboard focus is visible, mobile navigation has an explicit close control, and camera failure keeps manual entry available. Screenshots of the implemented application in `docs/testing/screenshots/` contain synthetic data only. They are implementation evidence, not photographs of hostel operations.
