#!/usr/bin/env python3
"""Evidence-gated C4 comparison. Never assigns a winner or fabricates results."""
from __future__ import annotations
import argparse,csv,json,sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'models/c2'))
from evaluate import summarize  # existing C2 strict-triad evaluator
VALID_GATES={'UNTESTED','PASS','PARTIAL','FAIL'}


def read_csv(path):
    with Path(path).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))


def filtered_evidence(trials,audits):
    """Only consented, referenced, completed observation records can enter measured summaries."""
    accepted_t=[];accepted_a=[];warnings=[]
    seen=set()
    for row in trials:
        if row.get('source_type_OBSERVED_or_SIMULATED')!='OBSERVED': continue
        identity=row.get('trial_id','').strip()
        if not identity or identity in seen:
            warnings.append(f'Dropped trial: missing/duplicate trial_id {identity!r}');continue
        seen.add(identity)
        if row.get('consent_and_permission_confirmed_Y_N')!='Y':
            warnings.append(f'Dropped trial {identity}: missing permission/consent');continue
        if not row.get('evidence_reference','').strip():
            warnings.append(f'Dropped trial {identity}: no evidence reference');continue
        if row.get('setting_STAGED_or_LIVE') not in ('STAGED','LIVE'):
            warnings.append(f'Dropped trial {identity}: invalid setting');continue
        if row.get('concept_A_B_C') not in 'ABC':
            warnings.append(f'Dropped trial {identity}: invalid concept');continue
        accepted_t.append(row)
    seen=set()
    for row in audits:
        if row.get('source_type_OBSERVED_or_SIMULATED')!='OBSERVED':continue
        identity=row.get('audit_id','').strip()
        if not identity or identity in seen:
            warnings.append(f'Dropped audit: missing/duplicate audit_id {identity!r}');continue
        seen.add(identity)
        if row.get('eligible_Y_N')!='Y':continue
        if not row.get('independent_checker_code','').strip() or not row.get('ground_truth_evidence_reference','').strip():
            warnings.append(f'Dropped audit {identity}: independent checker or ground-truth reference missing');continue
        if row.get('setting_STAGED_or_LIVE') not in ('STAGED','LIVE'):
            warnings.append(f'Dropped audit {identity}: invalid setting');continue
        if row.get('concept_A_B_C') not in 'ABC':
            warnings.append(f'Dropped audit {identity}: invalid concept');continue
        accepted_a.append(row)
    return accepted_t,accepted_a,warnings


def summarize_gates(gates):
    expected={(g,c) for g in [f'G{i:02}' for i in range(1,9)] for c in 'ABC'}
    observed=set();d={c:{'PASS':0,'FAIL':0,'PARTIAL':0,'UNTESTED':0} for c in 'ABC'};warnings=[]
    for row in gates:
        key=(row.get('gate_id'),row.get('concept_A_B_C'))
        if key not in expected or key in observed:
            warnings.append(f'Invalid/duplicate gate row {key!r}');continue
        observed.add(key)
        status=row.get('status','UNTESTED')
        if status not in VALID_GATES:
            warnings.append(f'Invalid gate status {status!r} at {key!r}');status='UNTESTED'
        if status=='PASS' and (not row.get('evidence_reference','').strip() or not row.get('reviewer_code','').strip()):
            warnings.append(f'PASS unsupported for {key!r}; treated as UNTESTED');status='UNTESTED'
        d[key[1]][status]+=1
    for missing in sorted(expected-observed):warnings.append(f'Missing gate entry {missing!r}');d[missing[1]]['UNTESTED']+=1
    return d,warnings


def assess(trials,audits,gates,weights_approved=False):
    valid_t,valid_a,warnings=filtered_evidence(trials,audits)
    gate_summary,gate_warnings=summarize_gates(gates)
    field=summarize(valid_t,valid_a,setting='LIVE')
    staged=summarize(valid_t,valid_a,setting='STAGED')
    status={}
    for c in 'ABC':
        f=field['by_concept'][c];g=gate_summary[c]
        status[c]={
            'gates':g,
            'all_gates_pass':g['PASS']==8,
            'live_trials':f['observed_trials'],
            'live_independent_audits':f['eligible_audits'],
            'live_strict_accountability_rate':f['strict_accountability_rate'],
            'ready_for_owner_selection':bool(g['PASS']==8 and f['observed_trials']>0 and f['eligible_audits']>0 and weights_approved),
        }
    return {
        'status':'NO SOLUTION SELECTED',
        'criteria_weights_owner_approved':weights_approved,
        'note':'Design and synthetic code checks cannot satisfy human testing, independent physical audits, or safety gates.',
        'valid_observed_staged':staged,
        'valid_observed_live':field,
        'gate_summary':gate_summary,
        'selection_readiness':status,
        'warnings':warnings+gate_warnings
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--trials',default=str(ROOT/'data/templates/c2-trial-log.csv'))
    p.add_argument('--audits',default=str(ROOT/'data/templates/c2-independent-audit.csv'))
    p.add_argument('--gates',default=str(ROOT/'data/templates/c4-gate-evidence.csv'))
    p.add_argument('--weights-approved',action='store_true',help='Owner explicitly approved weights; cannot substitute for evidence.')
    p.add_argument('--output')
    args=p.parse_args()
    res=assess(read_csv(args.trials),read_csv(args.audits),read_csv(args.gates),args.weights_approved)
    text=json.dumps(res,indent=2,ensure_ascii=False)+'\n'
    if args.output:Path(args.output).write_text(text,encoding='utf-8')
    else:print(text)

if __name__=='__main__':main()
