"""Build the Phase C2 editable comparison instrument, with NO synthetic trial rows.
Requires artifact_tool. Run from repository root.
"""
from pathlib import Path
import csv
from artifact_tool import Workbook, SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data'/'templates'/'c2-comparison-workbook.xlsx'
wb=Workbook.create()
NAVY='#19324C'; TEAL='#176C6A'; LIGHT='#EAF2F1'; LIGHTGRAY='#F1F5F9'; YELLOW='#FFF3CE'
fmt_header={'fill':NAVY,'font':{'bold':True,'color':'#FFFFFF'},'row_height':28,'vertical_alignment':'center','wrap_text':True}
fmt_title={'fill':TEAL,'font':{'bold':True,'color':'#FFFFFF'},'row_height':32,'vertical_alignment':'center'}

def sheet(name,headers,rows=[],widths=None,head_row=3):
  s=wb.worksheets.add(name)
  s.get_range('A1').values=[[name]]
  s.get_range(f'A1:{chr(64+len(headers))}1').format=fmt_title
  s.get_range(f'A{head_row}:{chr(64+len(headers))}{head_row}').values=[headers]
  s.get_range(f'A{head_row}:{chr(64+len(headers))}{head_row}').format=fmt_header
  if rows:
    s.get_range(f'A{head_row+1}:{chr(64+len(headers))}{head_row+len(rows)}').values=rows
  widths=widths or [17]*len(headers)
  for i,width in enumerate(widths):
    col=chr(65+i)
    s.get_range(f'{col}:{col}').format.column_width=width
  s.freeze_panes.freeze_rows(head_row)
  return s

intro=sheet('Read Me',['Section','Instructions'],[
 ['Status','PROTOCOL ONLY. Zero real trials, no comparison outcome.'],
 ['Primary metric','Strict three-way physical verification: location, custody and condition, divided by eligible audited assets.'],
 ['Evidence','Only observed and independently audited trial rows count; never pass synthetic simulation as field evidence.'],
 ['Scenarios','12 matched scripts; proposed six participant runs per scenario per concept (216 total planned).'],
 ['Scoring','Seven criterion weights are PROPOSED and NOT APPROVED; no candidate scores have been assigned.'],
 ['Gates','8 hard gates UNTESTED. Do not select a winner before testing and project-owner approval.'],
 ['Workflow','Enter observations in Trial Entry and Audit Entry; Summary derives numerator and denominator.'],
 ['Offline analysis','python models/c2/evaluate.py --trials ... --audits ...; CSV templates have matching schema.'],
 ['Privacy','No names, roll numbers, ID photos or personal register details in a public repo.'],
],widths=[20,88])
intro.get_range('A4:B4').format.fill=YELLOW
critrows=[]
with (ROOT/'docs'/'solution-design'/'c2-proposed-criteria.csv').open(newline='',encoding='utf8') as f:
 for r in csv.DictReader(f):critrows.append([r['criterion'],int(r['proposed_weight_percent_UNAPPROVED']),r['operational_definition'],r['evidence_method']])
crit=sheet('Criteria',['Criterion','Weight % - unapproved','Definition','Measurement'],critrows,[29,25,62,64]);crit.get_range('B4:B10').format.fill=YELLOW
crit.get_range('A12').values=[['TOTAL - must be 100']]
crit.get_range('B12').formulas=[['=SUM(B4:B10)']]
crit.get_range('A13').values=[['Decision status']];crit.get_range('B13').values=[['NOT APPROVED']]
scenrows=[]
with (ROOT/'docs'/'solution-design'/'c2-scenario-protocol.csv').open(newline='',encoding='utf8') as f:
 for r in csv.DictReader(f):scenrows.append([r['scenario_id'],r['scenario_name'],r['linked_B4_tests'],r['expected_ground_truth_or_success']])
scen=sheet('Scenarios',['ID','Task','Linked B4 tests','Success condition'],scenrows,[16,42,29,90]);scen.get_range('D4:D15').format.wrap_text=True
trials=sheet('Trial Entry',['Trial ID','Scenario ID','Setting','Concept A B C','Source OBSERVED/SIMULATED','Complete Y/N','Elapsed seconds','Student active sec','Guard active sec','Secretary active sec','Errors','Participant code','Evidence reference'],[],[17,16,16,18,30,17,19,19,17,19,12,23,29])
trials.get_range('A4:M184').format.fill='#FFFBED'
trials.get_range('D4:D184').data_validation={'rule':{'type':'list','values':['A','B','C']}}
trials.get_range('E4:E184').data_validation={'rule':{'type':'list','values':['OBSERVED','SIMULATED']}}
trials.get_range('F4:F184').data_validation={'rule':{'type':'list','values':['Y','N']}}
trials.get_range('C4:C184').data_validation={'rule':{'type':'list','values':['STAGED','LIVE']}}
audits=sheet('Audit Entry',['Audit ID','Concept A B C','Setting','Eligible Y/N','Location Y/N/UNKNOWN/CONTRADICTED','Custody Y/N/UNKNOWN/CONTRADICTED','Condition Y/N/UNKNOWN/CONTRADICTED','Source OBSERVED/SIMULATED','Evidence reference'],[],[18,17,16,17,34,34,34,28,28])
audits.get_range('A4:I204').format.fill='#FFFBED'
audits.get_range('B4:B204').data_validation={'rule':{'type':'list','values':['A','B','C']}}
audits.get_range('C4:C204').data_validation={'rule':{'type':'list','values':['STAGED','LIVE']}}
audits.get_range('D4:D204').data_validation={'rule':{'type':'list','values':['Y','N']}}
for col in ['E','F','G']:
 audits.get_range(f'{col}4:{col}204').data_validation={'rule':{'type':'list','values':['Y','N','UNKNOWN','CONTRADICTED']}}
audits.get_range('H4:H204').data_validation={'rule':{'type':'list','values':['OBSERVED','SIMULATED']}}
summary=sheet('Summary',['Candidate','Observed trials','Successful trials','Completion rate','Eligible audits','Strict correct triad','Verified accountability rate','Status'],[['A',None,None,None,None,None,None,'NOT TESTED'],['B',None,None,None,None,None,None,'NOT TESTED'],['C',None,None,None,None,None,None,'NOT TESTED']],[19,24,24,24,22,23,32,27])
for row in [4,5,6]:
 summary.get_range(f'B{row}').formulas=[[f'=COUNTIFS(\'Trial Entry\'!$D$4:$D$184,A{row},\'Trial Entry\'!$E$4:$E$184,"OBSERVED")']]
 summary.get_range(f'C{row}').formulas=[[f'=COUNTIFS(\'Trial Entry\'!$D$4:$D$184,A{row},\'Trial Entry\'!$E$4:$E$184,"OBSERVED",\'Trial Entry\'!$F$4:$F$184,"Y")']]
 summary.get_range(f'D{row}').formulas=[[f'=IF(B{row}=0,"",C{row}/B{row})']]
 summary.get_range(f'E{row}').formulas=[[f'=COUNTIFS(\'Audit Entry\'!$B$4:$B$204,A{row},\'Audit Entry\'!$D$4:$D$204,"Y",\'Audit Entry\'!$H$4:$H$204,"OBSERVED")']]
 summary.get_range(f'F{row}').formulas=[[f'=COUNTIFS(\'Audit Entry\'!$B$4:$B$204,A{row},\'Audit Entry\'!$D$4:$D$204,"Y",\'Audit Entry\'!$H$4:$H$204,"OBSERVED",\'Audit Entry\'!$E$4:$E$204,"Y",\'Audit Entry\'!$F$4:$F$204,"Y",\'Audit Entry\'!$G$4:$G$204,"Y")']]
 summary.get_range(f'G{row}').formulas=[[f'=IF(E{row}=0,"",F{row}/E{row})']]
 summary.get_range(f'H{row}').formulas=[[f'=IF(AND(B{row}=0,E{row}=0),"NOT TESTED","PARTIAL — REVIEW DATA")']]
summary.get_range('D4:D6').set_number_format('0.0%');summary.get_range('G4:G6').set_number_format('0.0%')
summary.get_range('A9').values=[['Interpretation']]
summary.get_range('B9').values=[['Blank rates mean NOT MEASURED, never 0%. Candidate selection requires gate reviews and project-owner approval.']]
summary.get_range('B9:H9').format.wrap_text=True
summary.get_range('A11').values=[['Caveat']]
summary.get_range('B11').values=[['Workbook does not calculate a winner and does not validate provenance. Use Python evaluator and inspect raw field evidence.']]
summary.get_range('B11:H11').format.wrap_text=True

with (ROOT/'docs'/'solution-design'/'c2-nonnegotiable-gates.csv').open(newline='',encoding='utf8') as f:
 gate_rows=[[r['gate_id'],r['gate'],r['linked_requirement_ids'],r['status'],r['decision_rule']] for r in csv.DictReader(f)]
gate=sheet('Hard Gates',['ID','Gate','Linked requirements','Status','Decision rule'],gate_rows,[14,46,30,19,96]);gate.get_range('D4:D11').format.fill=YELLOW
cost=sheet('Cost Entry',['Cost ID','Candidate','Setup / Recurring','Item','Qty','Unit cost INR','Source ACTUAL/QUOTE/ESTIMATE','Evidence','Occurrences/year'],[],[17,18,22,43,13,22,34,29,22]);cost.get_range('A4:I64').format.fill='#FFFBED'
SpreadsheetFile.export_xlsx(wb).save(str(OUT))
print('EXPORTED',OUT,OUT.stat().st_size)
for area in ['Summary!A3:H7','Criteria!A11:B13']:
 try:
  check=wb.inspect({'kind':'table','range':area,'include':'values,formulas','table_max_rows':7,'table_max_cols':8})
  print('CHECK',area,check.ndjson[:1500])
 except Exception as exc:print('INSPECT WARN',type(exc).__name__,str(exc)[:250])
try:
 e=wb.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':80},'summary':'C2 formula error scan'})
 print('FORMULA SCAN',e.ndjson[:1000])
except Exception as exc:print('FORMULA SCAN WARN',type(exc).__name__,str(exc)[:250])
