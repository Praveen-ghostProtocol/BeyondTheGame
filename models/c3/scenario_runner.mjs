/** Logical scenario checks using fictitious records. Not field trials or timing results. */
import {seed,apply,inventorySummary,safeApply} from './engine.mjs';
import fs from 'node:fs';
const row=[];
function run(id,mode,description,fn){try{const outcome=fn();const limited=(['C2-S06','C2-S08','C2-S09'].includes(id)&&mode!=='C')||(['C2-S11','C2-S12'].includes(id));const status=limited?'DESIGN_ONLY_NOT_END_TO_END_TESTED':(outcome?'LOGIC_CHECK_PASS':'LOGIC_CHECK_FAIL');row.push({scenario:id,concept:mode,mechanism:description,result:status,mechanism_sanity:!!outcome,evidence:'SYNTHETIC_CODE_EXECUTION'});}catch(e){row.push({scenario:id,concept:mode,mechanism:description,result:'LOGIC_CHECK_FAIL',error:e.message,evidence:'SYNTHETIC_CODE_EXECUTION'});}}
for(const mode of ['A','B','C']){
  run('C2-S01',mode,'Room key change independent of item state',()=>{let s=seed(mode);s=apply(s,'key_out',{student:'DEMO1'});s=apply(s,'key_back',{student:'DEMO1'});return s.assets['R-001'].status==='AVAILABLE';});
  run('C2-S02',mode,'Last usable item conflict handling',()=>{let s=seed(mode);let p={id:'R-001',to:'TEAM_A',role:'custodian'};s=apply(s,'issue',p);let second=safeApply(s,'issue',{...p,to:'TEAM_B'});return mode==='A'?second.ok&&second.state.exceptions.some(e=>e.type==='PAPER_CONFLICT_RISK'): !second.ok;});
  run('C2-S03',mode,'Separate durable IDs and consumable lot conservation',()=>{let s=apply(seed(mode),'consume',{lot:'SHUTTLE',qty:3});return s.lots.SHUTTLE.quantity===7&&s.assets['R-001'].id!==s.assets['R-002'].id;});
  run('C2-S04',mode,'Off-ground handover retains named operational custody',()=>{let s=seed(mode);s=apply(s,'issue',{id:'R-001',to:'TEAM_A',role:'custodian'});s=apply(s,'off_ground_transfer',{id:'R-001',to:'TEAM_B',role:'custodian'});return s.assets['R-001'].holder==='TEAM_B';});
  run('C2-S05',mode,'Key return and self-declared return do not verify stock',()=>{let s=seed(mode);s=apply(s,'key_out',{student:'DEMO1'});s=apply(s,'issue',{id:'R-001',to:'DEMO1',role:'custodian'});s=apply(s,'key_back',{student:'DEMO1'});s=apply(s,'return_claim',{id:'R-001'});return s.assets['R-001'].status==='INSPECTION'&&s.assets['R-001'].condition==='UNKNOWN';});
  run('C2-S06',mode,'Kit manifest or manual checklist mechanism',()=>{let s=seed(mode);return mode==='C'?(()=>{s=apply(s,'kit_issue',{kit:'KIT-CRICKET',to:'TEAM_C',role:'custodian'});s=apply(s,'kit_partial_return',{kit:'KIT-CRICKET',returned:['B-001','P-001'],role:'custodian'});return s.assets['P-002'].status==='UNRESOLVED';})():s.kits['KIT-CRICKET'].length===3;});
  run('C2-S07',mode,'Late damage report retains unknown occurrence time',()=>{let s=apply(seed(mode),'damage',{id:'B-001'});let e=s.events.at(-1);return s.assets['B-001'].status==='DAMAGED'&&e.occurrenceTime==='UNKNOWN'&&e.blame==='NOT_INFERRED';});
  run('C2-S08',mode,'Repair return requires independent inspection',()=>{let s=seed(mode);return mode==='C'?(()=>{s=apply(s,'damage',{id:'R-001'});s=apply(s,'repair_start',{id:'R-001',role:'secretary'});s=apply(s,'repair_finish',{id:'R-001',role:'maintenance'});return s.assets['R-001'].status==='INSPECTION';})():s.assets['T-001'].status==='DAMAGED';});
  run('C2-S09',mode,'Receipt mismatch visible without fabricated enrolled item',()=>{let s=seed(mode);return mode==='C'?(()=>{s=apply(s,'purchase_request',{role:'secretary',item:'Bats',ordered:2});s=apply(s,'purchase_receive',{role:'secretary',ref:'PUR-1',qty:1});return s.purchases[0].status==='RECEIPT_DISCREPANCY';})():true;});
  run('C2-S10',mode,'Offline conflict cannot silently overwrite item',()=>{let s=seed(mode);s=apply(s,'offline_conflict',{id:'R-001'});return s.assets['R-001'].status==='AVAILABLE'&&s.exceptions.some(e=>e.type==='OFFLINE_RECONCILIATION_REQUIRED');});
  run('C2-S11',mode,'Unknown audit attribute is not counted correct',()=>{let s=apply(seed(mode),'audit_note',{id:'R-001',attribute:'custody',verdict:'unknown'});return s.notes[0].verdict==='unknown';});
  run('C2-S12',mode,'Aggregate inventory state conservation',()=>inventorySummary(seed(mode)).reconciles);
}
const result={metadata:{kind:'SYNTHETIC_LOGIC_CHECKS',not:'field trial, outcome evidence, approval, or C2 measured comparison',method:'Deterministic concept workflow mechanics executed with invented identifiers',scenario_count:12,concepts:['A','B','C']},results:row};
const target=new URL('../../data/scenarios/c3/c3-mechanism-checks.json',import.meta.url);
fs.writeFileSync(target,JSON.stringify(result,null,2)+'\n');
const fails=row.filter(r=>r.result==='LOGIC_CHECK_FAIL');
console.log(`C3: ${row.length} synthetic scenario probes; ${row.filter(x=>x.result==='LOGIC_CHECK_PASS').length} implemented-logic passes, ${row.filter(x=>x.result==='DESIGN_ONLY_NOT_END_TO_END_TESTED').length} design-only, ${fails.length} failures. No physical scenarios completed.`);
if(fails.length){console.error(fails);process.exitCode=1;}
