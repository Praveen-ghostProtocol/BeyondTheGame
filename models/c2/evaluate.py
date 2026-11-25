#!/usr/bin/env python3
"""Measure A/B/C staged or live results. Does not synthesize evidence or score unrun designs."""
from __future__ import annotations
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path

ALLOWED={'A','B','C'}
AUDIT_VALUES={'Y','N','UNKNOWN','CONTRADICTED'}

def load_rows(path):
    with open(path,newline='',encoding='utf-8') as f: return list(csv.DictReader(f))

def summarize(trials, audits, setting=None):
    result={'status':'NOT MEASURED','setting':setting or 'ALL','by_concept':{},'data_warnings':[]}
    # Hard guard against treating simulated measurements as field evidence.
    if setting and setting not in {'STAGED','LIVE'}: raise ValueError('setting must be STAGED or LIVE')
    filtered_trials=[r for r in trials if not setting or r.get('setting_STAGED_or_LIVE')==setting]
    filtered_audits=[r for r in audits if not setting or r.get('setting_STAGED_or_LIVE')==setting]
    for candidate in ('A','B','C'):
        observed_t=[r for r in filtered_trials if r.get('concept_A_B_C')==candidate and r.get('source_type_OBSERVED_or_SIMULATED')=='OBSERVED']
        observed_a=[r for r in filtered_audits if r.get('concept_A_B_C')==candidate and r.get('source_type_OBSERVED_or_SIMULATED')=='OBSERVED']
        completed=[]; durations=[]; actor_times={name:[] for name in ('student','guard','secretary')}
        for t in observed_t:
            if t.get('completed_Y_N') not in ('Y','N'): result['data_warnings'].append(f"incomplete task result {t.get('trial_id','?')}");continue
            completed.append(t)
            if t['completed_Y_N']=='Y' and t.get('total_seconds') not in ('',None):
                durations.append(float(t['total_seconds']))
            for name in actor_times:
                field=f'{name}_active_seconds'
                if t.get(field) not in ('',None):actor_times[name].append(float(t[field]))
        num_correct=0; eligible=0; unknown=0; contradicted=0; wrong=0; incomplete=0
        for a in observed_a:
            if a.get('eligible_Y_N')!='Y': continue
            eligible+=1
            states=[a.get(f'{attr}_correct_Y_N_UNKNOWN_CONTRADICTED','') for attr in ('location','custody','condition')]
            if all(s=='Y' for s in states):num_correct+=1
            if any(s=='CONTRADICTED' for s in states):contradicted+=1
            elif any(s=='UNKNOWN' for s in states):unknown+=1
            elif any(s=='N' for s in states):wrong+=1
            elif any(s not in AUDIT_VALUES for s in states):incomplete+=1
        if observed_t or observed_a:result['status']='PARTIAL EVIDENCE — NOT A FINAL WINNER'
        result['by_concept'][candidate]={
            'observed_trials':len(observed_t),
            'completed_trials':len(completed),
            'task_success_rate':sum(t['completed_Y_N']=='Y' for t in completed)/len(completed) if completed else None,
            'median_completed_total_seconds':statistics.median(durations) if durations else None,
            'median_actor_active_seconds':{k:(statistics.median(v) if v else None) for k,v in actor_times.items()},
            'eligible_audits':eligible,
            'strict_triad_correct':num_correct,
            'strict_accountability_rate':num_correct/eligible if eligible else None,
            'unknown_audit_count':unknown,
            'contradicted_audit_count':contradicted,
            'wrong_audit_count':wrong,
            'incomplete_audit_count':incomplete,
        }
    # Avoid promoting a concept to 'winner' from partial trial evidence. No scoring here.
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--trials',required=True);p.add_argument('--audits',required=True)
    p.add_argument('--setting',choices=['STAGED','LIVE'])
    p.add_argument('--output')
    a=p.parse_args();o=summarize(load_rows(a.trials),load_rows(a.audits),a.setting)
    s=json.dumps(o,indent=2,ensure_ascii=False)
    if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
    else:print(s)

if __name__=='__main__':main()
