#!/usr/bin/env python3
"""Create a counterbalanced C4 *planned* run manifest; never creates test outcomes."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCENARIOS=ROOT/'docs/solution-design/c2-scenario-protocol.csv'
OUT=ROOT/'data/templates/c4-counterbalanced-trial-plan.csv'
ORDERS=('ABC','BCA','CAB','ACB','CBA','BAC')


def make_plan(scenario_ids:list[str]):
    rows=[]
    for sid in scenario_ids:
        for block, sequence in enumerate(ORDERS,1):
            for period,concept in enumerate(sequence,1):
                rows.append({
                    'planned_trial_id':f'{sid}-BLOCK{block}-P{period}',
                    'scenario_id':sid,
                    'block':block,
                    'order_sequence':sequence,
                    'order_position_1_2_3':period,
                    'concept_A_B_C':concept,
                    'participant_code_TO_ASSIGN':'',
                    'equipment_set_TO_ASSIGN':'',
                    'tester_code_TO_ASSIGN':'',
                    'setting_STAGED_or_LIVE_TO_APPROVE':'',
                    'study_approval_status':'NOT_APPROVED',
                    'run_status':'NOT_RUN',
                    'notes':''
                })
    return rows


def main():
    with SCENARIOS.open(newline='',encoding='utf-8') as f:
        scenarios=list(csv.DictReader(f))
    ids=[s['scenario_id'] for s in scenarios]
    if len(ids)!=12 or len(set(ids))!=12: raise ValueError('Expected 12 unique original C2 scenarios')
    rows=make_plan(ids)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(f'Prepared {len(rows)} unexecuted rows for {len(ids)} scenarios, 3 concepts, 6 blocks. No observations generated.')

if __name__=='__main__': main()
