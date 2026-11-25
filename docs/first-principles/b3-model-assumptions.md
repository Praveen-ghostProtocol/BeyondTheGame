# B3 — Model Inputs, Assumptions, Boundaries and Limitations

## Source hierarchy

| Source | Supported statement | Label | Safe use |
|---|---|---|---|
| Sports secretary's Alaknanda account | Key/ID and handwritten register, no item-level verification, informal transfers, damage reporting and tournament exception | **R — reported** | Map actual reported processes; not a measured transaction rate |
| Same respondent | ~5 min issue journey, ~2 min walking, ~2 min guard/entry, ~3–7 days repair | **E — approximate recollection** | Illustrative timing decomposition only |
| Same respondent | Badminton and volleyball daily, cricket and football every other day | **R** | ~20–22 sport-use occasions/week; NOT actual loans |
| User-selected 80/20 usable/damaged | Explicitly proposed split | **E — scenario** | No claim about actual inventory status |
| A2/B2 analysis | Access != custody != condition | **I — inference supported by workflow** | Formulate measurable hypotheses |
| B3 model probability, loan multiplier and fictitious inventory sample | Pure scenario construction | **S — simulated** | Algorithm verification and what-if design, never evidence of baseline |

## Definitions

- **Durable asset** — individually trackable item, with an item/kit identity distinct from student details.
- **Active asset** — a registered durable asset not permanently retired; may be missing/under repair.
- **Immediately available** — usable, in authorized storage, not already issued, reserved or awaiting condition verification.
- **Responsible custodian** — individual or authorized group designated by a policy; do not assume record of room key proves it.
- **Strict verified accountability** — all three item attributes (location, responsible custody, condition) exist in records **and** independently match the physical snapshot.
- **Unknown** — no reliable evidence, NOT proof of incorrect record, loss, or theft.

## Key assumptions and boundary checks

1. Time components are approximate and may not add perfectly; their 60-second leftover is not an observed equipment-collection segment.
2. Administrative state buckets are exclusive at one timestamp; physical condition and location remain separately recorded attributes. Damage can be present while an item is issued.
3. Stock identities require a known census; without it a reconciliation percentage cannot be published.
4. Retired items are included in the lifetime count but excluded from active count; lost/unknown remain active until formal write-off.
5. An individual kit can contain multiple distinct items; inventory counts should not double count its container/manifest.
6. Consumables are lot/quantity-tracked, outside individually audited durable-asset denominators unless explicitly sampled as lots.
7. The event-chain probability model assumes independent recording compliance, not independent record *correctness*. It never produces real hostel accountability rates.
8. No permission to audit student identity or publish unredacted guard log has been provided; do not store private identities in this public repository.
9. Reported procurement threshold for different quotation rules is a local process description requiring office confirmation before implementation.
10. Repair duration is a recalled range; do not calculate a mean or dominant bottleneck without case-level timestamps.

## Boundaries and falsification

- If field audits show informal custody is almost always identifiable, the magnitude of accountability gains may be small despite missing formal records.
- If added verification burden suppresses compliance, fewer required steps may outperform stricter capture.
- If equipment is mostly usable and easily retrieved, the strongest gains might come from maintenance workflow and replacement decisions, not issuance speed.
- If a large majority of transactions are kit-level, a strict individual-handover rule may misrepresent responsible group usage.

**Research gate before claims of effectiveness:** permissioned independent inventory snapshot, anonymized transaction sample, user and guard burden observation, and matched intervention trial. Never describe B3 what-ifs as a before/after result.
