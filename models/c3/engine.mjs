/**
 * C3 browser-only mechanism prototypes for Beyond the Game.
 * Synthetic assets. NOT a live deployed system, real inventory, or secure multi-user backend.
 * Every operation simulates a declared action; it does not attest to physical ground truth.
 */
export const MODES = ['A','B','C'];
export const statuses = ['AVAILABLE','ISSUED','INSPECTION','DAMAGED','REPAIR','RETIRED','UNRESOLVED'];
export function seed(mode='B') {
  if (!MODES.includes(mode)) throw new Error('Unknown concept');
  const items = [
    ['R-001','Badminton racket','AVAILABLE'], ['R-002','Badminton racket','AVAILABLE'],
    ['B-001','Cricket bat','AVAILABLE'], ['P-001','Batting pads','AVAILABLE'],
    ['P-002','Batting pads','AVAILABLE'], ['T-001','TT bat','DAMAGED'],
    ['V-001','Volleyball','AVAILABLE']
  ];
  return { mode, tick:0, keySessions:[], assets:Object.fromEntries(items.map(([id,name,status])=>[id,{id,name,status,holder:'STORE',condition: status==='DAMAGED'?'DAMAGED':'USABLE',location:'SPORTS_ROOM',confidence:'DEMO_SEED',version:0}])),
    lots:{'SHUTTLE':{name:'Shuttlecock',quantity:10}},
    kits:{'KIT-CRICKET':['B-001','P-001','P-002']},
    events:[], exceptions:[], repairs:[], purchases:[], notes:[] };
}
export function apply(input, action, p={}) {
  const state = structuredClone(input);
  const mode=state.mode;
  const actor=(p.actor||'TEST_USER').trim();
  const role=p.role||'student';
  const id=p.id||'';
  const asset=state.assets[id];
  const logged=(detail={})=>{state.tick+=1;state.events.push({seq:state.tick,action,actor,role,...detail,source:'SIMULATED_ACTION'});};
  const need=(ok,msg)=>{ if(!ok) throw new Error(msg); };
  const isStaff=['secretary','custodian','maintenance'].includes(role);
  const ensureStaff=()=>need(isStaff,'Staff role required (demo role, NOT authentication)');
  const ensureSecretary=()=>need(role==='secretary','Secretary role required (demo role, NOT authentication)');
  const ensureItem=()=>need(!!asset,'Unknown equipment ID');
  const setAsset=(a,status,holder,location,condition)=>{
    a.status=status;a.holder=holder;a.location=location;a.condition=condition;a.version+=1;a.confidence='DECLARED_DEMO_EVENT';
  };
  const asStatus=(a,expected)=>need(a.status===expected,`${a.id} is ${a.status}, expected ${expected}`);
  if (action==='key_out') {
    need(!!p.student,'Student name/code required');
    state.keySessions.push({student:p.student,open:true,seq:state.tick+1}); logged({student:p.student});
  } else if(action==='key_back') {
    const sess=state.keySessions.findLast(k=>k.open&&k.student===p.student);
    need(!!sess,'No active key session for student');sess.open=false;logged({student:p.student,doesNotVerifyEquipment:true});
  } else if (action==='issue') {
    ensureItem();need(!!p.to,'Borrower/team code required');
    if (mode==='C') {need(role==='secretary'||role==='custodian','Verified issue requires custodian/secretary role');asStatus(asset,'AVAILABLE');}
    else if(mode==='B'){asStatus(asset,'AVAILABLE');}
    else { // In A, a physical paper card can be written even if another card exists: no enforced atomic conflict.
      if(asset.status!=='AVAILABLE') state.exceptions.push({type:'PAPER_CONFLICT_RISK',id});
    }
    setAsset(asset,'ISSUED',p.to,`WITH_${p.to}`,'USABLE');logged({id,to:p.to,quality:mode==='A'?'MANUAL_DECLARATION':'DEMO_LEDGER'});
  } else if(action==='off_ground_transfer'){
    ensureItem();asStatus(asset,'ISSUED');need(!!p.to,'New responsible entity required');
    if(mode==='C') ensureStaff();
    setAsset(asset,'ISSUED',p.to,`WITH_${p.to}`,'USABLE');logged({id,to:p.to});
  } else if (action==='return_claim') {
    ensureItem();asStatus(asset,'ISSUED');
    // Reported return is NOT a verified return for ANY concept.
    setAsset(asset,'INSPECTION','UNVERIFIED','LOCATION_UNVERIFIED','UNKNOWN');logged({id,physicalReturnVerified:false});
  } else if(action==='inspect') {
    ensureItem();ensureStaff();asStatus(asset,'INSPECTION');
    need(typeof p.pass==='boolean','pass true/false required');
    setAsset(asset,p.pass?'AVAILABLE':'DAMAGED',p.pass?'STORE':'STORE', 'SPORTS_ROOM',p.pass?'USABLE':'DAMAGED');logged({id,pass:p.pass,staffConfirmedInDemo:true});
  } else if(action==='damage') {
    ensureItem();
    need(asset.status!=='RETIRED','Retired item cannot be changed');
    setAsset(asset,'DAMAGED','STORE','SPORTS_ROOM','DAMAGED');logged({id,discoveredAtSequence:state.tick+1,occurrenceTime:'UNKNOWN',blame:'NOT_INFERRED'});
  } else if(action==='repair_start'){
    need(mode==='C','Full maintenance workflow only in concept C');ensureSecretary();ensureItem();asStatus(asset,'DAMAGED');
    setAsset(asset,'REPAIR',p.vendor||'REPAIR_SHOP','REPAIR_SHOP','DAMAGED');state.repairs.push({id,stage:'ACTIVE',case:state.tick+1});logged({id});
  } else if(action==='repair_finish'){
    need(mode==='C','Full maintenance workflow only in concept C');ensureStaff();ensureItem();asStatus(asset,'REPAIR');
    setAsset(asset,'INSPECTION','STORE','SPORTS_ROOM','UNKNOWN');state.repairs.findLast(r=>r.id===id&&r.stage==='ACTIVE').stage='RETURNED_AWAITING_INSPECTION';logged({id,returnedUsable:false});
  } else if(action==='retire'){
    need(mode==='C','Retirement workflow only in concept C');ensureSecretary();ensureItem();
    need(asset.status!=='ISSUED','Cannot retire issued item');setAsset(asset,'RETIRED','STORE','SPORTS_ROOM','UNUSABLE');logged({id});
  } else if(action==='kit_issue'){
    need(mode==='C','Controlled kit transaction only in concept C');ensureStaff();need(!!p.to,'Team required');
    const components=state.kits[p.kit];need(!!components,'Unknown kit');
    need(components.every(k=>state.assets[k].status==='AVAILABLE'),'Kit unavailable; no partial issue committed');
    components.forEach(k=>setAsset(state.assets[k],'ISSUED',p.to,`WITH_${p.to}`,'USABLE'));
    logged({kit:p.kit,components:[...components],to:p.to});
  } else if(action==='kit_partial_return'){
    need(mode==='C','Controlled kit transaction only in concept C');ensureStaff();
    const components=state.kits[p.kit];need(!!components,'Unknown kit');
    const returned=p.returned||[];need(returned.every(k=>components.includes(k)),'Unexpected component');
    const missing=components.filter(k=>!returned.includes(k));
    returned.forEach(k=>{asStatus(state.assets[k],'ISSUED');setAsset(state.assets[k],'INSPECTION','UNVERIFIED','SPORTS_ROOM','UNKNOWN');});
    missing.forEach(k=>{if(state.assets[k].status==='ISSUED')setAsset(state.assets[k],'UNRESOLVED',state.assets[k].holder,'LOCATION_UNKNOWN','UNKNOWN');});
    state.exceptions.push({type:'PARTIAL_KIT_RETURN',kit:p.kit,missing});logged({kit:p.kit,returned,missing});
  } else if(action==='consume'){
    const lot=state.lots[p.lot];need(!!lot,'Unknown stock lot');need(Number.isInteger(p.qty)&&p.qty>0&&p.qty<=lot.quantity,'Invalid quantity');
    lot.quantity-=p.qty;logged({lot:p.lot,qty:p.qty,balance:lot.quantity});
  } else if(action==='purchase_request'){
    need(mode==='C','Procurement workflow only in concept C');ensureSecretary();need(!!p.item&&Number(p.ordered)>0,'Item and ordered quantity required');
    state.purchases.push({ref:`PUR-${state.purchases.length+1}`,item:p.item,ordered:Number(p.ordered),received:0,status:'REQUESTED',approval:'NOT_VERIFIED'});logged({ref:state.purchases.at(-1).ref});
  } else if(action==='purchase_receive'){
    need(mode==='C','Procurement workflow only in concept C');ensureSecretary();
    const pr=state.purchases.find(x=>x.ref===p.ref);need(!!pr,'Unknown purchase');
    const qty=Number(p.qty);need(Number.isInteger(qty)&&qty>=0,'Invalid receipt quantity');pr.received+=qty;
    pr.status=pr.received===pr.ordered?'RECEIVED': 'RECEIPT_DISCREPANCY';
    logged({ref:p.ref,received:pr.received,expected:pr.ordered,approvalStillUnverified:true});
  } else if(action==='offline_conflict') {
    state.exceptions.push({type:'OFFLINE_RECONCILIATION_REQUIRED',id,payload:p.message||'Stale update'});
    logged({id,pending:true,noStateOverwrite:true});
  } else if(action==='audit_note'){
    const verdict=['correct','incorrect','unknown'].includes(p.verdict)?p.verdict:'unknown';
    state.notes.push({id,attribute:p.attribute||'UNSPECIFIED',verdict,source:'SIMULATED_AUDIT_NOTE'});logged({id,verdict});
  } else throw new Error(`Unknown action ${action}`);
  return state;
}
export function inventorySummary(state){
  const counts=Object.fromEntries(statuses.map(s=>[s,0]));
  for(const a of Object.values(state.assets)) counts[a.status]+=1;
  const total=Object.values(state.assets).length;
  return {total,counts,reconciles:Object.values(counts).reduce((a,b)=>a+b,0)===total};
}
export function safeApply(state,action,fields){try{return {ok:true,state:apply(state,action,fields)}}catch(err){return {ok:false,state,error:err.message}}}
