"""E1 field trial: before/after summary from data/field-trial/*.csv.

Only rows with source == OBSERVED are counted, so blank templates report NOT MEASURED.
Run: python models/e1/analyze_trial.py
"""
import csv
import statistics
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / 'data' / 'field-trial'
NM = 'NOT MEASURED'


def load(name):
    with open(DATA / name, encoding='utf-8') as f:
        return [r for r in csv.DictReader(f) if r.get('source', '').strip().upper() == 'OBSERVED']


def accountability(rows):
    """Strict accountability: location, custodian and condition all recorded AND equal to truth."""
    out = {}
    for run in sorted({r['run'] for r in rows}):
        rs = [r for r in rows if r['run'] == run]
        attr = {}
        for a in ('location', 'custodian', 'condition'):
            attr[a] = sum(r['rec_' + a].strip().upper() == r['truth_' + a].strip().upper() != '' for r in rs)
        full = sum(all(r['rec_' + a].strip().upper() == r['truth_' + a].strip().upper() != ''
                       for a in ('location', 'custodian', 'condition')) for r in rs)
        out[run] = {'n': len(rs), 'full': full, **attr}
    return out


def med(xs):
    return statistics.median(xs) if xs else None


def timings(rows):
    out = {}
    for r in rows:
        if r['seconds'].strip():
            out.setdefault((r['run'], r['action'].split()[0]), []).append(float(r['seconds']))
    return {k: (len(v), med(v)) for k, v in out.items()}


def queries(rows):
    out = {}
    for r in rows:
        n, ok, secs = out.get(r['run'], (0, 0, []))
        out[r['run']] = (n + 1, ok + (r['correct_Y_N'].strip().upper() == 'Y'),
                         secs + ([float(r['seconds'])] if r['seconds'].strip() else []))
    return {k: (n, ok, med(s)) for k, (n, ok, s) in out.items()}


def scans(rows):
    if not rows:
        return None
    ok = sum(r['first_attempt_ok_Y_N'].strip().upper() == 'Y' for r in rows)
    secs = [float(r['seconds_to_open']) for r in rows if r['seconds_to_open'].strip()]
    return len(rows), ok, med(secs)


def pct(a, b):
    return f'{a}/{b} ({100 * a / b:.0f}%)' if b else NM


def main():
    acc = accountability(load('e1-audit.csv'))
    print('## Strict accountability (all three attributes recorded and correct)')
    if not acc:
        print(NM)
    for run, v in acc.items():
        print(f"- {run}: {pct(v['full'], v['n'])} | location {v['location']}, custodian {v['custodian']}, condition {v['condition']} of {v['n']}")

    print('\n## Median task time (s)')
    t = timings(load('e1-timings.csv'))
    if not t:
        print(NM)
    for (run, kind), (n, m) in sorted(t.items()):
        print(f'- {run} {kind}: median {m:.0f} s (n={n})')

    print('\n## Record queries answered correctly')
    q = queries(load('e1-queries.csv'))
    if not q:
        print(NM)
    for run, (n, ok, m) in sorted(q.items()):
        print(f"- {run}: {pct(ok, n)}, median {m:.0f} s" if m is not None else f'- {run}: {pct(ok, n)}')

    print('\n## Printed label scans')
    s = scans(load('e1-scans.csv'))
    print(NM if s is None else f'- first-attempt success {pct(s[1], s[0])}' + (f', median {s[2]:.0f} s to open' if s[2] is not None else ''))

    fb = load('e1-feedback.csv')
    print('\n## Feedback (median ease 1-5)')
    old = [float(r['ease_old_1to5']) for r in fb if r['ease_old_1to5'].strip()]
    new = [float(r['ease_new_1to5']) for r in fb if r['ease_new_1to5'].strip()]
    print(f'- OLD {med(old)} vs NEW {med(new)} (n={len(fb)})' if fb else NM)


if __name__ == '__main__':
    main()
