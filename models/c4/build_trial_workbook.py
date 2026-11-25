#!/usr/bin/env python3
"""Generate an editable C4 trial coordination workbook; no fabricated observations."""
from artifact_tool import Workbook, SpreadsheetFile
import csv
import os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
with (ROOT/'data/templates/c4-counterbalanced-trial-plan.csv').open() as f:plan=list(csv.DictReader(f))
with (ROOT/'data/templates/c4-gate-evidence.csv').open() as f:gates=list(csv.DictReader(f))
wb=Workbook.create()
navy='#172B43'; dark='#0B7567'
h={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':28,'vertical_alignment':'center'}
t={'fill':navy,'font':{'bold':True,'color':'#FFFFFF','size':16},'row_height':38}

def title(sh,range_,label):
 sh.merge_cells(range_)
 sh.get_range(range_.split(':')[0]).values=[[label]]
 sh.get_range(range_).format=t

def headings(sh,range_,values):
 sh.get_range(range_).values=[values]
 sh.get_range(range_).format=h

s=wb.worksheets.add('C4 Overview')
title(s,'A1:F1','C4 | Controlled trials & decision readiness')
items=[['Status','PREPARED — NO REAL TRIALS / NO WINNER'],['Current evidence','C3 synthetic code checks only; no field comparison.'],['Planned run count',len(plan)],['Scenarios',12],['Concepts',3],['Counterbalanced blocks',6],['Gate checks to test',len(gates)],['Measured accountability','NOT MEASURED'],['Decision','NO SOLUTION SELECTED'],['Next action','Owner approval → consented trials → independent audits → refinement.']]
s.get_range('A3:B12').values=items
s.get_range('A3:A12').format={'font':{'bold':True,'color':navy},'row_height':28}
s.get_range('A3:A12').format.column_width=28
s.get_range('B3:B12').format.column_width=72
s.get_range('B3:B12').format.wrap_text=True
s.merge_cells('D3:F3');headings(s,'D3',['Gate status counts'])
headings(s,'D4:E4',['Status','Count'])
for i,status in enumerate(['PASS','PARTIAL','FAIL','UNTESTED'],start=5):
 s.get_range(f'D{i}').values=[[status]]
 s.get_range(f'E{i}').formulas=[[f'=COUNTIF(\'Gate Review\'!$D$4:$D$27,"{status}")']]
s.get_range('D4:D8').format.column_width=20
s.get_range('E4:E8').format.column_width=15
s.merge_cells('D10:F12')
s.get_range('D10').values=[['Statuses alone do not prove a gate passed; cite independent evidence and reviewer before a PASS. Never auto-select a winner.']]
s.get_range('D10:F12').format.wrap_text=True

s=wb.worksheets.add('Run Plan')
title(s,'A1:J1','COUNTERBALANCED TRIAL PLAN — 216 UNRUN TASKS')
headings(s,'A3:J3',['Run ID','Scenario','Block','Order','Position','Concept','Participant','Equipment set','Approval','Run status'])
rows=[[r['planned_trial_id'],r['scenario_id'],r['block'],r['order_sequence'],r['order_position_1_2_3'],r['concept_A_B_C'],'','',r['study_approval_status'],r['run_status']] for r in plan]
s.get_range('A4:J219').values=rows
s.freeze_panes.freeze_rows(3)
for col,width in {'A':34,'B':14,'C':12,'D':12,'E':12,'F':12,'G':19,'H':19,'I':19,'J':19}.items():s.get_range(f'{col}4:{col}219').format.column_width=width
s.get_range('I4:I219').data_validation={'rule':{'type':'list','values':['NOT_APPROVED','APPROVED']}}
s.get_range('J4:J219').data_validation={'rule':{'type':'list','values':['NOT_RUN','STAGED','LIVE','SKIPPED']}}

s=wb.worksheets.add('Gate Review')
title(s,'A1:H1','24 NON-NEGOTIABLE GATE CHECKS — UNTESTED')
headings(s,'A3:H3',['Gate ID','Concept','Gate','Status','Test scenario','Evidence ref','Reviewer','Notes'])
s.get_range('A4:H27').values=[[r['gate_id'],r['concept_A_B_C'],r['gate'],r['status'],r['test_scenario'],'','',''] for r in gates]
s.freeze_panes.freeze_rows(3)
for col,width in {'A':12,'B':11,'C':38,'D':16,'E':30,'F':24,'G':16,'H':35}.items():s.get_range(f'{col}4:{col}27').format.column_width=width
s.get_range('C4:H27').format.wrap_text=True
s.get_range('C4:H27').format.row_height=39
s.get_range('D4:D27').data_validation={'rule':{'type':'list','values':['UNTESTED','PARTIAL','FAIL','PASS']}}

s=wb.worksheets.add('Owner Decisions')
title(s,'A1:E1','OWNER DECISIONS — PENDING APPROVAL')
headings(s,'A3:E3',['ID','Decision','Proposed default','Status','Owner notes / approved value'])
decisions=[
('D01','Study setting','STAGED first; live after separate permission'),
('D02','Participants + checker','Anonymous codes, independent checker; no new guard duties'),
('D03','Equipment + labels','Reversible tags; item IDs for durable items'),
('D04','Custody policy','Team-level on-field accountability; record off-field transfers'),
('D05','Condition verifier','Designated checker; not guard'),
('D06','Tournament extra time','≤ 60 seconds suggested, NOT approved'),
('D07','Criterion weights','30/20/15/10/10/10/5 suggested, UNAPPROVED'),
('D08','Budget + privacy','Budget TBD, non-identifying public aggregates')]
s.get_range('A4:E11').values=[[i,d,default,'PENDING',''] for i,d,default in decisions]
for col,width in {'A':10,'B':31,'C':70,'D':16,'E':43}.items():s.get_range(f'{col}4:{col}11').format.column_width=width
s.get_range('B4:E11').format.wrap_text=True
s.get_range('B4:E11').format.row_height=45
s.get_range('D4:D11').data_validation={'rule':{'type':'list','values':['PENDING','APPROVED','REVISED','REJECTED']}}

s=wb.worksheets.add('Refinement Log')
title(s,'A1:H1','REFINEMENTS — REAL TEST-LED CHANGES ONLY')
headings(s,'A3:H3',['Ref ID','Concept','Before version','Evidence reference','Observed failure','Change made','Retest evidence','Decision'])
for col,width in {'A':12,'B':12,'C':16,'D':24,'E':40,'F':43,'G':24,'H':20}.items():s.get_range(f'{col}4:{col}43').format.column_width=width
s.get_range('H4:H43').data_validation={'rule':{'type':'list','values':['PENDING','KEEP','REVERT']}}
s.freeze_panes.freeze_rows(3)
output=Path(os.environ.get('BTG_C4_WORKBOOK_OUTPUT', str(ROOT/'data/templates/c4-trial-readiness-workbook.xlsx')))
SpreadsheetFile.export_xlsx(wb).save(str(output))
print('Workbook exported:',output,output.stat().st_size,'bytes')
print(wb.inspect({'kind':'table','range':'C4 Overview!A3:B12','include':'values,formulas','table_max_rows':11,'table_max_cols':2}).ndjson[:1000])
print(wb.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':30},'summary':'formula error scan'}).ndjson[:1000])
