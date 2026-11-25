"""Beyond the Game B3: transparent WHAT-IF arithmetic, not observed hostel results.

Standard-library-only deterministic sensitivity calculations. Reproducible tables can be
regenerated with: python models/b3/scenario_model.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "data" / "scenarios" / "b3"


def full_record_probability(p_issue: float, p_transfer: float, transfers: int,
                            p_location: float, p_condition: float) -> float:
    """Modelled full-record probability, assuming independent compliance events.

    This is NOT physical accuracy or an audited accountability rate. The model
    assumes a recorded issue, each of k handovers, plus current location and
    condition records. Real-world dependence or staleness breaks this model.
    """
    if transfers < 0:
        raise ValueError("transfers must be nonnegative")
    if any(not 0 <= x <= 1 for x in (p_issue, p_transfer, p_location, p_condition)):
        raise ValueError("probabilities must be between 0 and 1")
    return p_issue * (p_transfer ** transfers) * p_location * p_condition


def hypothetical_weekly_event_range(sessions_low: int, sessions_high: int,
                                    events_per_session: int) -> tuple[int, int]:
    """Sport-use OCCASIONS multiplied by arbitrary events/occasion assumption."""
    if sessions_low < 0 or sessions_high < sessions_low or events_per_session < 0:
        raise ValueError("bad session assumptions")
    return sessions_low * events_per_session, sessions_high * events_per_session


def added_workload_minutes(weekly_events: float, seconds_extra_per_event: float) -> float:
    if weekly_events < 0 or seconds_extra_per_event < 0:
        raise ValueError("workload inputs must be nonnegative")
    return weekly_events * seconds_extra_per_event / 60


def aggregate_stock(states: dict[str, int]) -> tuple[int, int, int]:
    """Returns total counted, active count, usable-in-storage count.

    Administrative states are exclusive; condition is a separate attribute.
    """
    required = ("available", "issued", "pending_inspection", "quarantine",
                "external_repair", "missing_unknown", "retired")
    if set(states) != set(required) or any(not isinstance(v, int) or v < 0 for v in states.values()):
        raise ValueError("exact seven nonnegative integer states required")
    total = sum(states.values())
    return total, total - states["retired"], states["available"]


def _write_csv(name: str, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("empty scenario")
    DEST.mkdir(parents=True, exist_ok=True)
    with (DEST / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    trace = []
    for transfer_rate in (0.5, 0.7, 0.8, 0.95):
        for k in range(0, 6):
            prob = full_record_probability(.95, transfer_rate, k, .90, .90)
            trace.append({
                "scenario_label": "HYPOTHETICAL INDEPENDENT-EVENT MODEL",
                "issue_capture_probability_assumed": 0.95,
                "transfer_capture_probability_assumed": transfer_rate,
                "unrecorded_transfer_opportunities_k_assumed": k,
                "location_capture_probability_assumed": 0.90,
                "condition_capture_probability_assumed": 0.90,
                "all_records_present_probability_modelled": round(prob, 6),
                "interpretation": "not a field baseline; not independent verification of truth",
            })
    _write_csv("hypothetical-record-completeness.csv", trace)

    overhead = []
    for event_multiplier in (1, 2, 3):
        low, high = hypothetical_weekly_event_range(20, 22, event_multiplier)
        for seconds in (15, 30, 60, 120):
            overhead.append({
                "scenario_label": "HYPOTHETICAL DEMAND AND FRICTION",
                "estimated_sport_use_occasions_per_week_low": 20,
                "estimated_sport_use_occasions_per_week_high": 22,
                "assumed_borrowings_per_occasion": event_multiplier,
                "hypothetical_loan_events_week_low": low,
                "hypothetical_loan_events_week_high": high,
                "added_seconds_per_loan_assumed": seconds,
                "total_extra_admin_minutes_week_low": round(added_workload_minutes(low, seconds), 2),
                "total_extra_admin_minutes_week_high": round(added_workload_minutes(high, seconds), 2),
                "interpretation": "sport-use occasions are not observed borrowing events",
            })
    _write_csv("hypothetical-workload-tradeoff.csv", overhead)

    # Toy stock figures test the accounting identity; THESE ARE NOT ALAKNANDA COUNTS.
    toy = {"available": 31, "issued": 9, "pending_inspection": 2,
           "quarantine": 3, "external_repair": 2, "missing_unknown": 1,
           "retired": 2}
    counted, active, ready = aggregate_stock(toy)
    rows = [{"scenario_label": "FICTITIOUS ACCOUNTING EXAMPLE; NOT AN AUDIT",
             "administrative_state": s, "hypothetical_item_count": count,
             "description": "One snapshot, mutually exclusive status assignment"}
            for s, count in toy.items()]
    rows.append({"scenario_label": "FICTITIOUS ACCOUNTING EXAMPLE; NOT AN AUDIT",
                 "administrative_state": "TOTAL (including retired)",
                 "hypothetical_item_count": counted,
                 "description": f"active={active}; immediately available={ready}; count once only"})
    _write_csv("hypothetical-stock-reconciliation.csv", rows)

    # Illustrates denominator effects; sample sizes chosen for arithmetic, not observed.
    toy_categories = [("badminton", 20, 8, 5), ("cricket", 10, 5, 3),
                      ("football", 12, 10, 8)]
    comparison = []
    for sport, audited, assessable, correct in toy_categories:
        comparison.append({
            "scenario_label": "FICTITIOUS DENOMINATOR EXAMPLE; NOT AN AUDIT",
            "sport": sport, "sampled_assets": audited,
            "complete_records_assessable": assessable,
            "complete_and_independently_correct": correct,
            "strict_verified_share": round(correct / audited, 6),
            "assessable_share": round(assessable / audited, 6),
            "accuracy_conditional_on_assessable": round(correct / assessable, 6),
        })
    _write_csv("hypothetical-normalized-accountability.csv", comparison)

    print("Created 4 explicitly hypothetical tables at", DEST)
    print("Cross-check: 0.95 * 0.8^3 * 0.9 * 0.9 =",
          round(full_record_probability(.95, .8, 3, .9, .9), 6))
    print("Stock reconciliation: total", counted, "active", active, "available", ready)


if __name__ == "__main__":
    main()
