# C3 runnable concept lab

**All assets and interactions are fictional. Do not enter actual student information.**

## Open the demonstrations
From the repository root:

```sh
python -m http.server 8765
```

Open `http://localhost:8765/prototypes/c3/index.html`.

- **A:** Interactive manual checklist; actual concept is the [C1 printable paper forms](../c1/a-physical-forms.html). This is not a completed physical trial.
- **B:** Browser-based QR-equivalent (asset code selection) lightweight event ledger. Supports simulated issuance, declared returns, inspection, damage, transfer and consumable counts.
- **C:** Browser-based conceptual lifecycle system supporting kit reconciliation, condition, repair, purchasing discrepancies, status history and illustrative actor-role restrictions.

To rehearse the same scenarios, print [`scenario-cards.html`](scenario-cards.html), derived directly from the 12 C2 scripts.

The B/C browser logs are stored only in local browser storage and can be reset or exported as synthetic JSON. Do not treat this as secure role authentication, a deployed database or independently verified ground truth.

Run validation from repository root:

```sh
node --test tests/test_c3_engine.mjs
node models/c3/scenario_runner.mjs
```

See [full C3 specification](../../docs/solution-design/c3-prototype-development.md) and [coverage matrix](../../docs/solution-design/c3-mechanism-coverage.csv).
