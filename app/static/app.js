'use strict';
// UI implementation follows the three Stitch screens; all operational data comes from the API.
const $ = (s, root = document) => root.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty = v => String(v || '').replace(/_/g, ' ').toLowerCase().replace(/^./, c => c.toUpperCase());
const date = v => v ? new Date(v).toLocaleString('en-IN', {dateStyle:'medium',timeStyle:'short',timeZone:'Asia/Kolkata'}) + ' IST' : 'Not recorded';
const money = v => new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format((v || 0)/100);
const badge = v => `<span class="badge ${['AVAILABLE','USABLE','APPROVED','CLOSED','RETURNED','RECEIVED','RESOLVED'].includes(v)?'good':['QUARANTINE','DAMAGED','DENIED','OVERDUE'].includes(v)?'bad':['INSPECTION','REQUESTED','PARTIAL','RETURN_REPORTED','PENDING','UNKNOWN'].includes(v)?'warn':'blue'}">${esc(pretty(v))}</span>`;
const btn = (label, action, id='', cls='small', extra='') => `<button class="${cls}" data-action="${action}" data-id="${esc(id)}" ${extra}>${esc(label)}</button>`;
const empty = (title, sub='Records will appear here as you use the application.') => `<div class="empty"><strong>${esc(title)}</strong>${esc(sub)}</div>`;
const panel = (title, body, action='') => `<section class="panel"><div class="panel-head"><h2>${esc(title)}</h2>${action}</div>${body}</section>`;
const table = (heads, rows) => `<div class="table-wrap"><table><thead><tr>${heads.map(x=>`<th scope="col">${esc(x)}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;
const row = cells => `<tr>${cells.map(c=>`<td>${c}</td>`).join('')}</tr>`;
const iconPaths = {overview:'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',inventory:'M3 7h18v14H3zM2 3h20v4H2zM9 11h6',borrowing:'M4 7h16m-4-4 4 4-4 4M20 17H4m4-4-4 4 4 4',kits:'M8 6V3h8v3M3 7h18v14H3zM3 12h18M10 10v4h4v-4',repairs:'m14 6 4 4M6 14l4 4M3 21l7-7M14 10l7-7M3 3l7 7 4-4-7-3z',procurement:'M4 8h16v13H4zM8 8V6a4 4 0 0 1 8 0v2',keys:'M15 7a4 4 0 1 0 0 1M11 10 3 18v3h3v-3h3v-3h3',audits:'M4 20V4h16v16zM8 16v-4m4 4V8m4 8v-6',activity:'M3 12a9 9 0 1 0 3-7M3 3v6h6m3-3v6l4 2',admin:'M12 3 3 7v6c0 5 9 9 9 9s9-4 9-9V7zM8 12l3 3 5-6',help:'M9 8a3 3 0 1 1 5 2c-2 1-2 2-2 4M12 17v1M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20'};
const icon = key => `<svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${iconPaths[key]||iconPaths.inventory}"/></svg>`;
let state, data, me, csrf, route='overview', query='', sportFilter='', stateFilter='', toastTimer, busy=false, labelIds=[];
const manager = () => ['admin','secretary'].includes(me?.role);
const checker = () => ['admin','secretary','checker','captain'].includes(me?.role);
const record = (kind, id) => data[kind].find(x=>x.id===id);

async function api(path, payload, key) {
  const opt = {credentials:'same-origin',headers:{}};
  if (payload !== undefined) {
    opt.method='POST'; opt.headers={'Content-Type':'application/json','X-CSRF-Token':csrf||''};
    if (key) opt.headers['Idempotency-Key']=key;
    opt.body=JSON.stringify(payload);
  }
  let res;
  try { res=await fetch(path,opt); } catch { throw new Error('Connection lost. This action is not confirmed. Refresh when online; reconcile physical movements in Recovery.'); }
  const body=await res.json();
  if (!res.ok) { if(res.status===401 && path!=='/api/login') login(); const e=new Error(body.error||'Request failed');e.status=res.status;throw e; }
  return body;
}
function toast(msg) { const el=$('#toast'); el.textContent=msg;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('show'),4500); }
async function refresh() {
  state=await api('/api/state'); data=state.data;me=state.user;csrf=state.csrf;
  render();
}
async function command(action, payload, operationKey=crypto.randomUUID()) {
  const out=await api('/api/command',{action,payload},operationKey);
  await refresh(); return out.result;
}
function login() {
  state=null;data=null;me=null;csrf=null;
  $('#root').innerHTML=`<div class="login"><section class="login-story"><div class="brand"><span class="monogram">BTG</span><div><strong>Beyond the Game</strong><small>Alaknanda · IIT Madras</small></div></div><div><div class="eyebrow">A better innings for every piece of gear</div><h1>More play.<br>Less guesswork.</h1><p>One place for your hostel’s equipment, from the first checkout to the final repair.</p><p>Know what’s ready, who has it, and what needs care.</p></div><footer>Built from Alaknanda’s equipment lifecycle study · Phase D</footer></section><section class="login-form"><div><div class="login-badge">Alaknanda Hostel · IIT Madras</div><h2>Welcome to the team.</h2><p class="subtle">Sign in to manage equipment and get back to the game.</p><form id="login-form"><label for="username">Username</label><input id="username" name="username" autocomplete="username" required maxlength="64" placeholder="Your account code"><label for="password">Password</label><input id="password" name="password" type="password" autocomplete="current-password" required maxlength="256" placeholder="Enter your password"><div class="form-error" id="login-error" role="alert"></div><button class="primary" type="submit">Sign in →</button></form><hr class="divider"><p class="subtle">Accounts are issued by your administrator. The room-key register and equipment custody remain separate.</p><p class="form-hint">Local demo credentials are in app/private/demo-access.txt. Demo accounts and inventory are synthetic.</p></div></section></div>`;
  $('#login-form').addEventListener('submit',async e=>{e.preventDefault();const b=e.target.querySelector('button');b.disabled=true;try {const f=new FormData(e.target);const r=await api('/api/login',Object.fromEntries(f));csrf=r.csrf;await refresh();}catch(err){$('#login-error').textContent=err.message;}finally{b.disabled=false;}});
}
const navigation = [['overview','Overview'],['inventory','Inventory'],['borrowing','Borrowing & returns'],['kits','Team kits'],['repairs','Damage & repairs'],['procurement','Procurement'],['keys','Key access'],['audits','Audits & insights'],['activity','Activity'],['labels','QR labels'],['admin','Administration']];
function allowedRoute(r) {
  if (r==='procurement') return manager() || me.role==='office';
  if (r==='admin') return ['admin','office'].includes(me.role);
  if (r==='labels') return manager();
  if (r==='keys') return manager() || me.role==='guard';
  return true;
}
function render() {
  if(!me) return;
  let hash=location.hash.slice(1);
  if(hash.startsWith('asset/')) route='inventory';else route=navigation.some(x=>x[0]===hash)||hash==='help'?hash:'overview';
  if(!allowedRoute(route)) route='overview';
  const nav=navigation.filter(x=>allowedRoute(x[0])).map(([key,label],i)=>`${key==='audits'?'<div class="nav-label">Controls & evidence</div>':''}<a href="#${key}" class="${route===key?'active':''}" ${route===key?'aria-current="page"':''}>${icon(key)}${label}</a>`).join('');
  $('#root').innerHTML=`<div class="shell"><aside class="sidebar"><div class="brand"><span class="monogram">BTG</span><div><strong>Beyond the Game</strong><small>Alaknanda · IIT Madras</small></div></div><div class="nav-label">Equipment lifecycle</div><nav aria-label="Main navigation">${nav}</nav><div class="side-bottom"><a href="#help">${icon('help')} &nbsp; Help & recovery</a><div class="system-status"><span class="dot"></span> PHASE D · ${state.mode==='DEMO'?'DEMO ENVIRONMENT':'LOCAL APPLICATION'}</div></div></aside><div class="workspace"><header class="topbar">${btn('☰','menu','','menu-toggle','aria-label="Toggle navigation"')}<div class="facility">Alaknanda Hostel<small>IIT Madras · Sports equipment</small></div><form id="global-search" class="global-search"><input name="q" aria-label="Search equipment" placeholder="Search gear or equipment ID…" value="${esc(query)}"></form><div class="top-actions">${btn('⌗  Scan QR','scan','','lime')}<div class="user-chip"><b>${esc(me.username)}</b><small>${esc(pretty(me.role))}</small></div>${btn('↪','logout','','quiet','aria-label="Sign out"')}</div></header><div class="provenance ${navigator.onLine?'':'offline'}">${state.mode==='DEMO'?'DEMONSTRATION DATA · Synthetic equipment and events. No field results.':'OPERATOR RECORDS · App entries are declarations; independent audits establish accountability.'}${navigator.onLine?'':' · CONNECTION OFFLINE: physical movements need reconciliation.'}</div><main id="content" tabindex="-1">${views[route]()}<footer class="footer-line"><span>Beyond the Game · Equipment lifecycle · Alaknanda</span><span>Last refreshed ${esc(date(state.server_time))} · ${btn('Refresh','refresh','','link-button')}</span></footer></main></div></div>`;
  $('.side-bottom').insertAdjacentHTML('afterbegin',btn('Close navigation','menu','','sidebar-close quiet'));
  $$('.sidebar a').forEach(a=>a.addEventListener('click',()=>$('.shell').classList.remove('menu-open')));
  const gs=$('#global-search');if(gs)gs.onsubmit=e=>{e.preventDefault();query=new FormData(e.target).get('q');location.hash='inventory';render();};
  $('#inventory-query')?.addEventListener('input',e=>{query=e.target.value;renderInventoryRows();});
  $('#sport-filter')?.addEventListener('change',e=>{sportFilter=e.target.value;renderInventoryRows();});
  $('#state-filter')?.addEventListener('change',e=>{stateFilter=e.target.value;renderInventoryRows();});
  $$('.bar-fill').forEach(e=>e.style.setProperty('--bar',e.dataset.pct+'%'));
  if(hash.startsWith('asset/')) {const id=decodeURIComponent(hash.slice(6));if(!$('#modal').open) assetDetail(id);}
}
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
function heading(title,sub,actions='') {return `<div class="page-head"><div><div class="eyebrow">Alaknanda · equipment lifecycle</div><h1>${title}</h1><p class="subtle">${sub}</p></div><div class="actions">${actions}</div></div>`;}
function stat(label,n,sub,unit='') {return `<div class="stat"><div class="stat-label">${label}</div><div class="stat-symbol">↗</div><div class="stat-number">${n}${unit?` <span>${unit}</span>`:''}</div><div class="stat-footer">${sub}</div></div>`;}
const views = {
  overview() {
    const m=state.metrics,c=m.counts,needs=c.QUARANTINE+c.REPAIR+c.INSPECTION+c.UNKNOWN;
    const attention=data.assets.filter(a=>['QUARANTINE','INSPECTION','UNKNOWN','REPAIR'].includes(a.status));
    const queue=attention.slice(0,5).map(a=>`<div class="queue-row"><div class="queue-main"><span class="equipment-icon">${icon('inventory')}</span><div><strong>${esc(a.name)}</strong><small>${esc(a.id)} · ${esc(a.sport)}</small></div></div><div class="actions">${badge(a.status)}${btn('Review →','asset',a.id,'quiet small')}</div></div>`).join('');
    const distribution=Object.entries(c).filter(([,n])=>n>0).map(([s,n])=>`<div class="bar-row"><div class="bar-label"><span>${esc(pretty(s))}</span><span class="mono">${n} / ${m.total}</span></div><div class="bar"><div class="bar-fill" data-pct="${m.total?n/m.total*100:0}"></div></div></div>`).join('');
    const a=m.accountability;
    return heading('Ready for the next game.','A clear view of your equipment, from store to sports ground.',`${btn('Browse equipment','browse','','primary')}${manager()?btn('+ Register equipment','asset-create'):''}`)+
      `<div class="stats">${stat('Tracked equipment',m.total,'Unique durable items · kits are not double-counted')}${stat('Available now',c.AVAILABLE,'Recorded usable and ready for checkout',`/ ${m.total}`)}${stat('Active borrowings',m.active_loans,`${m.overdue} overdue · no automatic fines`)}${stat('Needs attention',needs,'Inspection, quarantine, repair or unknown',`/ ${m.total}`)}</div>`+
      `<div class="accountability"><div><div class="eyebrow">Strict independent accountability</div><h2>Records are a starting point. Checks are the evidence.</h2><p>Location, custodian and condition must all match an independent snapshot. Demo events never count as field evidence.</p></div><strong>${a.rate===null?'Not measured':`${a.numerator} / ${a.denominator}`}</strong></div>`+
      `<div class="grid-2">${panel('Attention queue',`<div class="panel-body">${queue||empty('No equipment waiting for attention','Damage reports and return inspections will appear here.')}</div>`,btn('View all','repairs-view','','link-button'))}${panel('Recorded equipment status',`<div class="panel-body">${distribution||empty('Register your first item')}<p class="form-hint">${m.reconciles?'All status categories reconcile to the registry.':'Reconciliation needed.'} This is a ledger view, not a physical stock audit.</p></div>`)}</div>`+
      panel('Recent activity',eventRows(data.events.slice(0,5)),`<a href="#activity" class="subtle">View history →</a>`);
  },
  inventory() {
    const sports=[...new Set(data.assets.map(a=>a.sport))].sort();
    return heading('The equipment room.','Individual IDs, explicit custody and a condition record for every durable item.',manager()?`${btn('+ Consumable lot','lot-create')}${btn('+ Register equipment','asset-create','','primary')}`:'')+
      `<section class="panel"><div class="toolbar"><input id="inventory-query" aria-label="Search inventory" placeholder="Search equipment, ID or location…" value="${esc(query)}"><select id="sport-filter" aria-label="Filter by sport"><option value="">All sports</option>${sports.map(s=>`<option ${s===sportFilter?'selected':''}>${esc(s)}</option>`).join('')}</select><select id="state-filter" aria-label="Filter by status"><option value="">All states</option>${['AVAILABLE','ISSUED','INSPECTION','QUARANTINE','REPAIR','UNKNOWN','RETIRED'].map(s=>`<option value="${s}" ${s===stateFilter?'selected':''}>${pretty(s)}</option>`).join('')}</select></div><div id="inventory-rows">${inventoryRows()}</div></section>`+
      panel('Consumable lots · quantity accounting',data.lots.length?table(['Lot / unit','Sport','Quantity remaining','Actions'],data.lots.map(l=>row([`<strong>${esc(l.name)}</strong><small class="mono">${esc(l.id)} · ${esc(l.unit)}</small>`,esc(l.sport),`<strong>${l.quantity}</strong>`,checker()?btn('Receive / consume','lot-adjust',l.id):'Quantity tracked by the store']))):empty('No consumable lots'));
  },
  borrowing() {
    const requests=data.requests.map(r=>row([`<strong>${esc(r.purpose)}</strong><small class="mono">${esc(r.id)}</small>`,esc(r.team||r.borrower),`<span class="mono">${esc(r.assets.join(', '))}</span>`,date(r.due_at),badge(r.status),`<div class="actions">${r.status==='REQUESTED'&&manager()?btn('Approve','request-approve',r.id)+btn('Decline','request-deny',r.id):''}${r.status==='APPROVED'&&(r.borrower===me.id||manager())?btn('Confirm pickup','pickup',r.id,'primary small'):''}${['APPROVED','REQUESTED'].includes(r.status)&&(r.borrower===me.id||manager())?btn('Cancel','request-cancel',r.id):''}</div>`]));
    const loans=data.loans.map(l=>{const late=l.remaining.length&&new Date(l.due_at)<new Date();return row([`<strong>${esc(l.team||l.borrower)}</strong><small class="mono">${esc(l.id)}</small>`,`<span class="mono">${esc(l.remaining.join(', ')||'All physically received')}</span>`,`${date(l.due_at)}${late?'<small>No automatic fine</small>':''}`,badge(late?'OVERDUE':l.status),`<div class="actions">${l.remaining.length&&(l.borrower===me.id||manager())?btn('Report return','return-report',l.id):''}${l.remaining.length&&checker()&&l.borrower!==me.id?btn('Receive items','return-receive',l.id,'primary small'):''}${l.status==='ACTIVE'&&(l.borrower===me.id||manager())?btn('Transfer custody','transfer',l.id):''}</div>`]);});
    const incoming=data.transfers.filter(t=>t.status==='PENDING'&&t.to===me.id).map(t=>`<div class="note"><b>Custody handover offered</b><p>${esc(t.from)} → you · ${esc(t.location)}. Accept only after physically receiving the equipment.</p>${btn('Accept handover','transfer-accept',t.id,'primary small')} ${btn('Reject','transfer-reject',t.id)}</div>`).join('');
    return heading('Borrow. Play. Bring it back.','Approval, physical pickup, return declaration and inspection are separate steps.',btn('+ Borrow equipment','request-create','','primary'))+
      incoming+`<div class="note">Routine individual pickup is available 24/7 under the configured policy. Team/tournament kits need pre-approval. Returning a room key does not close a borrowing.</div>`+
      panel('Borrowing requests',requests.length?table(['Purpose / reference','Responsible party','Manifest','Return by','Status','Actions'],requests):empty('No borrowing requests','Choose equipment from the inventory to get started.'))+
      panel('Equipment custody & returns',loans.length?table(['Borrower / team','Outstanding components','Due date','Status','Actions'],loans):empty('No equipment borrowings'));
  },
  kits() {
    return heading('Ready as a team.','One manifest, one accountable captain. No logging of every on-field pass.',manager()?btn('+ Create kit','kit-create','','primary'):'')+
      `<div class="note">Match-day target: no more than 60 seconds additional checkout effort. This remains a target; no participant timing has been measured.</div>`+
      (data.kits.length?`<div class="cards">${data.kits.map(k=>{const available=k.assets.every(id=>record('assets',id)?.status==='AVAILABLE')&&k.lots.every(l=>(record('lots',l.id)?.quantity||0)>=l.quantity);return `<article class="card"><div class="eyebrow">${esc(k.sport)} · ${esc(k.id)}</div><h2>${esc(k.name)}</h2>${badge(available?'AVAILABLE':'COMPONENTS_UNAVAILABLE')}<p>${k.assets.length} individually tracked components${k.lots.length?` + ${k.lots.length} consumable lots`:''}</p><ul>${k.assets.map(id=>`<li>${esc(record('assets',id)?.name||id)} <span class="mono">${esc(id)}</span></li>`).join('')}${k.lots.map(l=>`<li>${l.quantity} × ${esc(record('lots',l.id)?.name||l.id)}</li>`).join('')}</ul><div class="actions">${['captain','secretary','admin'].includes(me.role)?btn('Request team kit','request-kit',k.id,'primary small'):badge('CAPTAIN_REQUEST_REQUIRED')}</div></article>`;}).join('')}</div>`:panel('Team kits',empty('No team kits registered')));
  },
  repairs() {
    const attention=data.assets.filter(a=>['INSPECTION','QUARANTINE','REPAIR','UNKNOWN'].includes(a.status));
    const reports=data.damage.map(d=>row([`<strong>${esc(d.asset_id||'Identification unresolved')}</strong><small>${esc(d.description)}</small>`,date(d.discovered_at),'<span class="subtle">Occurrence time unknown<br>Fault not inferred</span>',badge(d.status),manager()&&d.status==='OPEN'?btn('Acknowledge','damage-ack',d.id):'']));
    const repairRows=data.repairs.map(r=>row([`<strong>${esc(record('assets',r.asset_id)?.name||r.asset_id)}</strong><small class="mono">${esc(r.id)}</small>`,esc(r.vendor),badge(r.stage),money(r.cost_paise),date(r.created_at),`${['ASSESSED','APPROVED','AT_VENDOR','REPAIRED'].includes(r.stage)?btn(({ASSESSED:'Authorize repair',APPROVED:'Confirm vendor handoff',AT_VENDOR:'Record repair complete',REPAIRED:'Receive from vendor'})[r.stage],'repair-advance',r.id,'primary small'):''}${r.stage==='RECEIVED'&&checker()?btn('Inspect equipment','asset',r.asset_id):''}`]));
    return heading('Keep good gear in play.','Record discovery, assess the problem, and track repairs through reinspection.',btn('+ Report damage','damage','','primary'))+
      `<div class="note amber">A damage report never implies fault or moves an item back to the store. Receive any outstanding borrowing before vendor handoff. Guards have no inspection duty.</div>`+
      panel('Inspection & quarantine',attention.length?table(['Equipment','Condition','Location','Custody','Action'],attention.map(a=>row([`<strong>${esc(a.name)}</strong><small class="mono">${esc(a.id)}</small>`,badge(a.condition),esc(a.location),esc(a.custodian),btn('Review','asset',a.id)]))):empty('No inspections or repairs pending'))+
      panel('Damage reports',reports.length?table(['Equipment / description','Discovered','Evidence boundary','Status','Action'],reports):empty('No reported damage'))+
      panel('Maintenance work orders',repairRows.length?table(['Equipment / case','Vendor','Milestone','Estimate','Opened','Next step'],repairRows):empty('No repair cases'))+
      (manager()?data.repairs.filter(r=>['ASSESSED','APPROVED','REASSESS'].includes(r.stage)).map(r=>`<div class="note"><b>${esc(r.asset_id)} · ${esc(pretty(r.stage))}</b><p>${r.stage==='REASSESS'?'Inspection did not restore usability. Reassess and re-authorize or cancel before retirement.':'Cancel only if equipment is still in store; vendor-held repairs must be physically returned first.'}</p>${r.stage==='REASSESS'?btn('Reassess repair','repair-reassess',r.id):''} ${btn('Cancel repair case','repair-cancel',r.id)}</div>`).join(''):'');
  },
  procurement() {
    const policy=data.settings[0];
    const rows=data.purchases.map(r=>row([`<strong>${esc(r.name)}</strong><small>${esc(r.rationale)}</small><small class="mono">${esc(r.id)}</small>`,money(r.amount_paise),`${r.quotes.length} recorded`,`${r.received} / ${r.quantity}`,badge(r.stage),`<div class="actions">${r.stage==='NEED'&&manager()?btn('+ Quotation','purchase-quote',r.id):''}${['NEED','APPROVED'].includes(r.stage)&&['office','admin'].includes(me.role)?btn(r.stage==='NEED'?'Record approval':'Record payment','purchase-advance',r.id,'primary small'):''}${['PAYMENT_RECORDED','PARTIAL_RECEIPT'].includes(r.stage)&&manager()?btn('Receive stock','purchase-receive',r.id,'primary small'):''}</div>`]));
    return heading('Buy for the next innings.','Need, quotations, authorization, payment evidence and physical receipt.',manager()?btn('+ Purchase need','purchase-create','','primary'):'')+
      `<div class="note ${policy.policy_confirmed?'':'amber'}">${policy.policy_confirmed?'Office-confirmed policy':'Reported policy · office confirmation pending'}: ${money(policy.threshold_paise)} and above requires three distinct quotations and office payment. Lower amounts use the reimbursement route with quotation evidence. The app records evidence and never moves money.</div>`+
      panel('Procurement register',rows.length?table(['Need / priority rationale','Total estimate','Quotations','Received / ordered','Stage','Next step'],rows):empty('No procurement cases','Physically received stock enters inspection; invoices alone do not add available inventory.'));
  },
  keys() {
    return heading('The key is its own record.','Keep room access separate from equipment custody.',btn('+ Key sign-out','key-out','','primary'))+
      `<div class="note">Existing ID and paper-register procedures remain in place. Do not photograph or upload student IDs. Overlapping access does not assign all equipment to the key holder.</div>`+
      panel('Room access sessions',data.keys.length?table(['Resident code','Key','Signed out','Returned','Status','Action'],data.keys.map(k=>row([esc(k.borrower),esc(k.key_code),date(k.out_at),date(k.back_at),badge(k.status),k.status==='OUT'?btn('Record key return','key-back',k.id):'<span class="subtle">Equipment not verified</span>']))):empty('No key sessions'));
  },
  audits() {
    const m=state.metrics,a=m.accountability;
    return heading('Check the record against reality.','Independent snapshots measure location, custody and condition together.',checker()?btn('+ Start physical audit','audit-start','','primary'):'')+
      `<div class="stats">${stat('Strict accountability',a.rate===null?'—':`${a.numerator} / ${a.denominator}`,a.rate===null?'Not measured · no eligible independent audit':`${(a.rate*100).toFixed(1)}% · ${date(a.snapshot_at)}`)}${stat('Unknown attributes',a.unknown??'—','Kept in the denominator')}${stat('Contradicted records',a.contradicted??'—','Distinct from missing / unknown')}${stat('Repair lead time',m.repair_lead_hours===null?'—':m.repair_lead_hours.toFixed(1),`${m.repair_lead_n} completed cases · hours`)}</div>`+
      `<div class="note">Baseline and before/after improvement: <b>NOT MEASURED</b>. Demo audits are excluded. Audits are snapshots, not guarantees of current accuracy. Checker must differ from the record operator and custodian; observations expire after 15 minutes or any asset change.</div>`+
      panel('Category-normalized stock',m.categories.length?table(['Sport','Active durable items','Available','Unusable / unknown','Share'],m.categories.map(c=>row([esc(c.sport),c.active,c.available,c.unusable_or_unknown,c.unusable_share===null?'—':`${(c.unusable_share*100).toFixed(1)}%`]))):empty('No category records'))+
      panel('Audit snapshots',data.audits.length?table(['Snapshot / sampling method','Recorded / sample','Source','Status','Action'],data.audits.map(a=>row([`${date(a.snapshot_at)}<small>${esc(a.method)}</small>`,`${a.observations.length} / ${a.snapshots.length}`,badge(a.provenance),badge(a.status),a.status==='OPEN'&&checker()?btn('Continue audit','audit-observe',a.id):btn('View audit','audit-detail',a.id)]))):empty('No independent audit snapshots'))+
      panel('Request fulfilment & burden',`<div class="panel-body"><p>${m.fulfilment.collected} collected / ${m.fulfilment.decided_requests} decided requests. Pending and cancelled requests are excluded from this descriptive count. No timed fulfilment rate is claimed because a service window has not been approved.</p><p class="subtle">Tournament additional effort: NOT MEASURED · target ≤60 seconds. Use the existing C4 workbook for actual task timing and comparative evaluation.</p></div>`);
  },
  activity() { return heading('Every change has a trail.','Append-only events preserve the actor, role, timestamp and prior decisions.',manager()||me.role==='office'?btn('Export public aggregates','export'):'')+panel('Recorded events',eventRows(data.events)); },
  labels() {
    const assets=labelIds.map(id=>record('assets',id)).filter(Boolean);
    return heading('A permanent identity for every item.','Prepare removable labels only after testing the app and scanner on the intended phone.',`${btn('Choose registered assets','labels-select','','primary')}${assets.length?btn('Print label sheet','labels-print'):''}`)+
      `<div class="note amber no-print">${state.mode==='DEMO'?'DEMO LABELS — synthetic IDs, not for real hostel equipment.':'Use actual registered equipment only.'} QR contains a permanent equipment ID, no student data or borrower information. Scanning opens details; it never automatically changes custody. Use 100% print scale and test one reversible label first.</div>`+
      (assets.length?`<div class="label-sheet">${assets.map(a=>{const qr=qrcode(0,'M');qr.addData('BTG:ASSET:'+a.id);qr.make();const svg=qr.createSvgTag({cellSize:4,margin:16,scalable:true});return `<article class="qr-label"><div class="eyebrow">Beyond the Game · ${state.mode==='DEMO'?'DEMO ONLY':'Alaknanda'}</div><img src="data:image/svg+xml,${encodeURIComponent(svg)}" alt="Equipment QR for ${esc(a.id)}"><strong class="mono">${esc(a.id)}</strong><small>${esc(a.name)} · ${esc(a.sport)}</small></article>`;}).join('')}</div>`:panel('QR label preparation',empty('Select actual registered equipment','No label sheet is generated automatically from the provisional trial inventory.')));
  },
  admin() {
    const p=data.settings[0];
    return heading('People, permissions and policy.','Accounts use role codes. Passwords and private activity never belong in Git.',me.role==='admin'?btn('+ Create account','user-create','','primary'):'')+
      panel('Facility policy',`<div class="panel-body"><p><b>Procurement threshold:</b> ${money(p.threshold_paise)} · ${badge(p.policy_confirmed?'OFFICE_CONFIRMED':'UNCONFIRMED')}</p><p><b>24/7 routine self-pickup:</b> ${p.ordinary_self_pickup?'Enabled':'Requires authorization'}</p><p class="subtle">${esc(p.confirmation_reference||'Reported purchasing split is provisional until office confirmation.')} Self-pickup records borrower declaration, not independent physical verification.</p>${btn('Edit confirmed policy','policy','','primary small')}</div>`)+
      (me.role==='admin'?panel('Resident & operator accounts',table(['Username / account code','Role','Access','Action'],data.users.map(u=>row([`<strong>${esc(u.username||u.id)}</strong><small class="mono">${esc(u.id)}</small>`,pretty(u.role),badge(u.active?'ACTIVE':'DISABLED'),u.id!==me.id?btn('Change access','user-update',u.id):'<span class="subtle">Your account</span>'])))):'')+
      panel('Your account',`<div class="panel-body"><p class="subtle">Changing your password revokes all existing sessions.</p>${btn('Change password','password')}</div>`);
  },
  help() {
    return heading('A simple system. A clear handover.',`Your account code: <code>${esc(me.id)}</code>. Use the app alongside physical equipment and existing hostel procedures.`)+
      `<div class="help-grid">${[['For residents',['Find an available item or scan its equipment QR.','Create a request and confirm actual pickup only when holding the item.','Share within your playing group under the responsible captain.','Report returns; a separate checker records physical receipt and inspection.']],['For captains & checkers',['Pre-authorize team kits before match day.','Confirm the kit manifest in one atomic pickup.','Receive only components actually returned; missing items stay outstanding.','Inspect returned and repaired items separately before marking usable.']],['For guards',['Record key handover and return only.','Keep the current ID and register process.','Do not inspect equipment or infer damage responsibility from key custody.']],['For the secretary & office',['Register actual inventory; keep unknown condition visible.','Acknowledge damage, assess repair, record authorization and vendor custody.','Confirm purchasing policy before financial approvals.','Record partial physical receipts; inspect new stock before availability.']]].map(([title,steps])=>`<section class="card"><h2>${title}</h2><ol>${steps.map(x=>`<li>${x}</li>`).join('')}</ol></section>`).join('')}</div><hr class="divider">`+
      panel('Interrupted, offline or conflicting movement',`<div class="panel-body"><p>Do not retry a physical handover as a new loan. Refresh first and check the record. The database rejects stale versions and duplicate issues. If something physically moved while offline, record a reconciliation case with the asset code and details. A secretary must compare the physical item and record a reasoned correction.</p>${btn('+ Reconciliation case','conflict','','primary small')}</div>`)+
      panel('Reconciliation inbox',data.conflicts.length?table(['Asset / report','Status','Action'],data.conflicts.map(c=>row([`${esc(c.asset_id)}<small>${esc(c.description)}</small>`,badge(c.status),manager()&&c.status==='PENDING'?btn('Resolve after checking','conflict-resolve',c.id):esc(c.resolution||'Awaiting secretary')]))):empty('No reconciliation cases'))+
      `<div class="note amber">The software tests are synthetic checks. C4 participant trials, the physical accountability baseline, adoption and the ≤60-second tournament target remain unmeasured. QR labels must use real registered asset IDs after on-device scanning is verified.</div>`;
  }
};
function inventoryRows() {
  const assets=data.assets.filter(a=>(!query||`${a.id} ${a.name} ${a.sport} ${a.location}`.toLowerCase().includes(query.toLowerCase()))&&(!sportFilter||a.sport===sportFilter)&&(!stateFilter||a.status===stateFilter));
  return assets.length?table(['Equipment / ID','Sport','Recorded location','State / condition','Custodian','Source / last update',''],assets.map(a=>row([`<button class="link-button" data-action="asset" data-id="${esc(a.id)}"><strong>${esc(a.name)}</strong><small class="mono">${esc(a.id)}</small></button>`,esc(a.sport),esc(pretty(a.location)),`${badge(a.status)}<small>${esc(pretty(a.condition))}</small>`,`<code>${esc(a.custodian)}</code>`,`<span class="badge">${esc(pretty(a.verification))}</span><small>${date(a.recorded_at)}</small>`,btn('Open →','asset',a.id,'quiet small')]))):empty('No equipment matches','Adjust the filters or register actual equipment.');
}
function renderInventoryRows() { $('#inventory-rows').innerHTML=inventoryRows(); }
function eventRows(events) {
  return events.length?table(['When','Event','Target','Actor / role','Source'],events.map(e=>row([date(e.at),esc(pretty(e.action)),`<code>${esc(e.target)}</code>`,`<code>${esc(e.actor)}</code><small>${esc(e.role)}</small>`,badge(e.provenance)]))):empty('No recorded events');
}

function openDialog(title,html,after) {
  const dialog=$('#modal'); if(dialog.open) dialog.close(); window.BTGScanner.stop();
  dialog.innerHTML=`<div class="modal-head"><h2 id="modal-title">${esc(title)}</h2>${btn('×','close','','quiet','aria-label="Close dialog"')}</div><div class="modal-body">${html}</div>`;
  dialog.showModal();if(after) after();
}
function closeDialog() {window.BTGScanner.stop();$('#modal').close();}
$('#modal').addEventListener('close',()=>window.BTGScanner.stop());
const field = (name,label,type='text',value='',options={}) => {
  const id='f-'+name;const req=options.optional?'':'required';
  let input;
  if(type==='select'||type==='multi') input=`<select name="${name}" id="${id}" ${type==='multi'?'multiple':''} ${req}>${options.items.map(x=>{let[v,l]=Array.isArray(x)?x:[x,pretty(x)];return `<option value="${esc(v)}" ${Array.isArray(value)?value.includes(v)?'selected':'':v===value?'selected':''}>${esc(l)}</option>`;}).join('')}</select>`;
  else if(type==='textarea') input=`<textarea name="${name}" id="${id}" ${req} maxlength="1500">${esc(value)}</textarea>`;
  else if(type==='checkbox') return `<label class="check-label" for="${id}"><input id="${id}" name="${name}" type="checkbox" ${value?'checked':''} ${options.must?'required':''}>${esc(label)}</label>`;
  else input=`<input id="${id}" name="${name}" type="${type}" value="${esc(value)}" ${req} ${type==='number'?`min="${options.min??0}" step="${options.step||1}"`:'maxlength="1500"'} ${options.autocomplete?`autocomplete="${options.autocomplete}"`:''}>`;
  return `<div class="${options.full?'full':''}"><label for="${id}">${esc(label)}</label>${input}${options.hint?`<div class="form-hint">${esc(options.hint)}</div>`:''}</div>`;
};
function form(title,fields,onSubmit,submit='Save record',intro='') {
  const operationKey=crypto.randomUUID();
  openDialog(title,`${intro?`<div class="note">${intro}</div>`:''}<form id="workflow-form"><div class="form-grid">${fields.join('')}</div><div class="form-error" id="workflow-error" role="alert"></div><div class="modal-footer">${btn('Cancel','close')}<button class="primary" type="submit">${esc(submit)}</button></div></form>`,()=>{
    $('#workflow-form').onsubmit=async e=>{e.preventDefault();if(busy)return;busy=true;const b=e.target.querySelector('[type=submit]');b.disabled=true;const fd=new FormData(e.target);const values=Object.fromEntries(fd);
      e.target.querySelectorAll('select[multiple]').forEach(s=>values[s.name]=fd.getAll(s.name));
      e.target.querySelectorAll('input[type=checkbox]').forEach(s=>values[s.name]=s.checked);
      e.target.querySelectorAll('input[type=number]').forEach(s=>values[s.name]=Number(s.value));
      try{await onSubmit(values,operationKey);closeDialog();toast('Record saved.');}catch(err){const out=$('#workflow-error');if(out)out.textContent=err.message;}finally{busy=false;b.disabled=false;}
    };
  });
}
function confirmCommand(title,action,obj,fields=[],extra={},intro='') {
  form(title,fields,(v,key)=>command(action,{id:obj.id,version:obj.version,...extra,...v},key),'Confirm',intro);
}
function assetDetail(id) {
  const a=record('assets',id); if(!a){toast('No registered equipment matches that code.');return;}
  const loan=a.loan_id?record('loans',a.loan_id):data.loans.find(l=>l.remaining.includes(id));
  const history=data.events.filter(e=>e.target===id||JSON.stringify(e.detail||{}).includes(`"${id}"`)).slice(0,12);
  let actions=btn('Report damage','damage',a.id);
  if(a.status==='AVAILABLE'&&['admin','secretary','student','captain','checker'].includes(me.role))actions=btn('Request equipment','request-asset',id,'primary')+actions;
  if(checker()&&!a.loan_id&&['INSPECTION','QUARANTINE','UNKNOWN'].includes(a.status))actions+=btn('Inspect condition','inspect',id,'primary');
  if(manager()&&a.status==='QUARANTINE'&&!a.loan_id)actions+=btn('Open repair case','repair-create',id);
  if(manager()&&!a.loan_id&&!['ISSUED','REPAIR','RETIRED'].includes(a.status))actions+=btn('Correct record','asset-correct',id)+btn('Retire asset','retire',id,'danger');
  if(loan)actions+=btn('View borrowing','borrowing-view',loan.id);
  openDialog('Equipment detail',`<div class="asset-detail-top"><div class="eyebrow">${esc(a.id)} · ${esc(a.sport)}</div><h2>${esc(a.name)}</h2>${badge(a.status)} ${badge(a.condition)}</div><dl class="detail-grid">${[['Recorded location',a.location],['Accountable entity',a.custodian],['Verification',a.verification],['Last recorded',date(a.recorded_at)],['Inspection',date(a.inspected_at)],['Source',a.source]].map(([k,v])=>`<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl><div class="note">App status records a declared or inspected state. Custody does not imply blame. ${a.return_reported?'Return declared; physical receipt is still pending.':''}</div><div class="detail-actions">${actions}</div><hr class="divider"><h3>Recorded history</h3><div class="timeline">${history.length?history.map(e=>`<div class="timeline-item"><b>${esc(pretty(e.action))}</b><p>${date(e.at)} · ${esc(e.role)} · ${esc(e.provenance)}</p></div>`).join(''):'<p class="subtle">No history visible to your role.</p>'}</div>`);
  const proof=Object.entries(a.evidence||{}).map(([attribute,e])=>row([esc(pretty(attribute)),date(e.recorded_at),esc(pretty(e.confidence)),esc(pretty(e.source))]));
  if(proof.length)$('#modal .divider').insertAdjacentHTML('beforebegin',`<hr class="divider">${panel('Evidence by attribute',table(['Attribute','Recorded at','Confidence','Source'],proof))}`);
}
function borrowForm(assetIds=[],kit) {
  const choices=data.assets.filter(a=>a.status==='AVAILABLE').map(a=>[a.id,`${a.id} · ${a.name}`]);
  const due=new Date(Date.now()+86400000);const local=new Date(due.getTime()-due.getTimezoneOffset()*60000).toISOString().slice(0,16);
  form(kit?'Request team kit':'Request equipment',[
    ...(kit?[]:[field('assets','Equipment to request','multi',assetIds,{items:choices,full:true,hint:'Use Ctrl / Cmd to select several items on desktop.'})]),
    field('purpose','Purpose','text',kit?'Tournament':'Practice',{full:true}),
    ...(kit||me.role==='captain'?[field('team','Accountable team / group','text','',{optional:!kit,full:true})]:[]),
    field('due_at','Expected return','datetime-local',local,{full:true})
  ],(v,key)=>command('request_create',{...v,assets:v.assets||[],kit_id:kit?.id,due_at:new Date(v.due_at).toISOString()},key),'Create request',kit?`${esc(kit.name)} · ${kit.assets.length} components. This request does not move equipment. A secretary approves tournament kits before collection.`:'A request or approval does not prove physical pickup. Confirm collection as a separate step.');
}
async function handleAction(action,id) {
  switch(action) {
    case 'menu': $('.shell').classList.toggle('menu-open');break;
    case 'close': closeDialog();break;
    case 'refresh': await refresh();toast('Records refreshed.');break;
    case 'logout': await api('/api/logout',{});closeDialog();login();break;
    case 'browse': location.hash='inventory';render();break;
    case 'asset': assetDetail(id);break;
    case 'borrowing-view': closeDialog();location.hash='borrowing';render();break;
    case 'repairs-view': location.hash='repairs';render();break;
    case 'request-create': borrowForm();break;
    case 'request-asset': borrowForm([id]);break;
    case 'request-kit': borrowForm([],record('kits',id));break;
    case 'asset-create':form('Register a durable item',[
      field('id','Permanent equipment ID','text','',{hint:'Letters, digits and hyphens. One ID per physical durable item.'}),field('name','Equipment name'),
      field('sport','Sport','select','Badminton',{items:['Badminton','Cricket','Football','Volleyball','Table tennis','Basketball','Other']}),
      field('location','Storage location','text','SPORTS_ROOM'),field('condition','Recorded condition','select','UNKNOWN',{items:['UNKNOWN','USABLE','DAMAGED']}),field('cost','Purchase cost (₹, optional)','number',0,{step:'.01'})
    ],(v,key)=>{v.cost_paise=Math.round(v.cost*100);delete v.cost;return command('asset_create',v,key);},'Register item','Register only actual equipment. Unknown condition starts in inspection. Demo setup remains labelled synthetic.');break;
    case 'asset-correct': {const a=record('assets',id);confirmCommand('Correct equipment record','asset_correct',a,[field('name','Equipment name','text',a.name),field('sport','Sport','text',a.sport),field('location','Corrected location','text',a.location),field('reason','Reason and physical check','textarea','',{full:true})],{},'The original event stays in history. Active loans and repairs must be reconciled before correction.');break;}
    case 'lot-create':form('Register a consumable lot',[field('id','Lot ID'),field('name','Consumable name'),field('sport','Sport'),field('unit','Unit','text','pieces'),field('quantity','Opening physical quantity','number',0)],(v,key)=>command('lot_create',v,key));break;
    case 'lot-adjust':{const l=record('lots',id);confirmCommand('Receive or consume stock','lot_adjust',l,[field('delta','Quantity change','number',-1,{min:-1000000,hint:'Negative for consumption, positive for receipt or reconciliation.'}),field('reason','Reason / reference','textarea','',{full:true})],{},`${esc(l.name)} · Current recorded balance ${l.quantity} ${esc(l.unit)}.`);break;}
    case 'kit-create':form('Create a kit manifest',[field('id','Kit ID'),field('name','Kit name'),field('sport','Sport'),field('assets','Durable components','multi',[],{items:data.assets.filter(a=>a.status!=='RETIRED').map(a=>[a.id,`${a.id} · ${a.name}`]),full:true}),field('lot_id','Consumable lot (optional)','select','',{items:[['','No consumables'],...data.lots.map(l=>[l.id,l.name])],optional:true}),field('lot_qty','Consumable quantity','number',0)],(v,key)=>command('kit_create',{id:v.id,name:v.name,sport:v.sport,assets:v.assets,lots:v.lot_id?[{id:v.lot_id,quantity:v.lot_qty}]:[]},key),'Create manifest');break;
    case 'request-approve':confirmCommand('Approve request','request_approve',record('requests',id),[],{},'Approval does not assign physical custody. The borrower confirms actual pickup separately.');break;
    case 'request-deny':confirmCommand('Decline request','request_deny',record('requests',id),[field('reason','Reason / unmet need','textarea','',{full:true})]);break;
    case 'request-cancel':confirmCommand('Cancel request','request_cancel',record('requests',id));break;
    case 'pickup':{const r=record('requests',id);confirmCommand('Confirm physical pickup','pickup',r,[field('location','Equipment destination','text','SPORTS_GROUND',{full:true}),field('physical_confirmed',`I physically collected all ${r.assets.length} components in the manifest: ${r.assets.join(', ')}.`,'checkbox',false,{must:true})],{},'This commits one atomic borrowing. A competing pickup or unavailable component prevents the whole kit checkout.');break;}
    case 'return-report':{const l=record('loans',id);confirmCommand('Declare equipment return','return_report',l,[field('assets','Components you returned','multi',l.remaining.filter(a=>!record('assets',a)?.return_reported),{items:l.remaining.filter(a=>!record('assets',a)?.return_reported).map(a=>[a,`${a} · ${record('assets',a)?.name||''}`]),full:true})],{},'This is a declaration. Custody stays outstanding until a separate checker physically receives the equipment.');break;}
    case 'return-receive':{const l=record('loans',id);confirmCommand('Receive returned components','return_receive',l,[field('assets','Physically received components','multi',[],{items:l.remaining.map(a=>[a,`${a} · ${record('assets',a)?.name||''}`]),full:true}),field('physical_confirmed','I physically received only the selected components. Missing components remain outstanding.','checkbox',false,{must:true})],{},'Receipt moves equipment into inspection; it does not certify usable condition. Guard key return cannot substitute for this step.');break;}
    case 'inspect':confirmCommand('Record condition inspection','inspect',record('assets',id),[field('condition','Inspection result','select','UNKNOWN',{items:['UNKNOWN','USABLE','DAMAGED'],full:true}),field('notes','Inspection method and findings','textarea','',{full:true})],{},'Only physically received equipment can be inspected. Use a checker separate from the borrower.');break;
    case 'transfer':{const l=record('loans',id);confirmCommand('Offer off-group custody transfer','transfer_offer',l,[field('assets','Components leaving the responsible group','multi',l.remaining,{items:l.remaining.map(a=>[a,`${a} · ${record('assets',a)?.name||''}`]),full:true}),field('to','Receiving resident account code','text','',{full:true,hint:'Recipient finds their account code in Help or Administration.'}),field('location','New location','text','SPORTS_GROUND',{full:true})],{},'The current custodian remains responsible until the recipient accepts physical receipt. On-ground sharing inside the responsible team needs no per-pass record.');break;}
    case 'transfer-accept':confirmCommand('Accept physical custody','transfer_accept',record('transfers',id),[field('physical_confirmed','I physically received the entire offered borrowing and accept custody.','checkbox',false,{must:true})]);break;
    case 'transfer-reject':confirmCommand('Reject custody offer','transfer_reject',record('transfers',id));break;
    case 'damage':form('Report equipment damage',[field('asset_id','Equipment ID (leave empty if unknown)','text',id,{optional:true,full:true}),field('description','What did you discover?','textarea','',{full:true}),field('location','Where was it discovered?','text','UNKNOWN',{full:true})],(v,key)=>command('damage_report',{...v,asset_id:v.asset_id||null},key),'Report discovery','Discovery time is recorded now. Occurrence time and blame stay unknown. Reporting damage does not return the item or change its custodian.');break;
    case 'damage-ack':confirmCommand('Acknowledge damage report','damage_acknowledge',record('damage',id),[field('notes','Assessment / next action','textarea','',{full:true})]);break;
    case 'repair-create':{const a=record('assets',id);form('Open a repair case',[field('assessment','Assessment / repair need','textarea','',{full:true}),field('vendor','Repair shop / vendor code'),field('cost','Estimated repair cost (₹)','number',0,{step:'.01'})],(v,key)=>command('repair_create',{asset_id:id,version:a.version,assessment:v.assessment,vendor:v.vendor,cost_paise:Math.round(v.cost*100)},key),'Open assessment','Repair authorization is a separate step. Vendor custody, repair completion, physical receipt and reinspection are recorded separately.');break;}
    case 'repair-advance':confirmCommand('Record next repair milestone','repair_advance',record('repairs',id),[field('reference','Authorization / handover evidence reference','textarea','',{full:true})],{},`Current stage: ${esc(pretty(record('repairs',id).stage))}. Record only the milestone actually completed.`);break;
    case 'repair-reassess':confirmCommand('Reassess failed repair','repair_reassess',record('repairs',id),[field('reason','Reassessment and required next work','textarea','',{full:true})]);break;
    case 'repair-cancel':confirmCommand('Cancel in-store repair case','repair_cancel',record('repairs',id),[field('reason','Reason and next disposition','textarea','',{full:true})]);break;
    case 'retire':confirmCommand('Authorize equipment retirement','retire',record('assets',id),[field('reason','Reason and authority for retirement','textarea','',{full:true})],{},'Retired equipment is excluded from active stock. This records the secretary decision; it does not change institutional disposal policy.');break;
    case 'purchase-create':form('Record procurement need',[field('name','Equipment / stock name'),field('sport','Sport'),field('quantity','Quantity needed','number',1,{min:1}),field('amount','Estimated total (₹)','number',0,{min:.01,step:'.01'}),field('rationale','Need, demand, repair alternatives and priority','textarea','',{full:true})],(v,key)=>command('purchase_create',{name:v.name,sport:v.sport,quantity:v.quantity,amount_paise:Math.round(v.amount*100),rationale:v.rationale},key));break;
    case 'purchase-quote':{const p=record('purchases',id);form('Add distinct vendor quotation',[field('vendor','Vendor code'),field('amount','Quotation total (₹)','number',0,{min:.01,step:'.01'}),field('reference','Private document reference','text','',{full:true,hint:'Use an internal reference. Do not paste personal or banking details.'})],(v,key)=>command('purchase_quote',{id,version:p.version,vendor:v.vendor,amount_paise:Math.round(v.amount*100),reference:v.reference},key));break;}
    case 'purchase-advance':confirmCommand('Record office authorization / payment','purchase_advance',record('purchases',id),[field('reference','Actual approval / payment reference','textarea','',{full:true})],{},'Record an authorized action already completed. The application does not approve spending or send payments automatically.');break;
    case 'purchase-receive':{const p=record('purchases',id);form('Confirm physical stock receipt',[field('quantity','Quantity physically received','number',1,{min:1}),field('asset_ids','New durable IDs, comma-separated','textarea','',{optional:true,full:true}),field('lot_id','Or add to an existing consumable lot','select','',{items:[['','Receive durable items'],...data.lots.map(l=>[l.id,l.name])],optional:true,full:true}),field('physical_confirmed','I physically received this quantity. Missing items remain outstanding.','checkbox',false,{must:true})],(v,key)=>command('purchase_receive',{id,version:p.version,quantity:v.quantity,asset_ids:v.asset_ids.split(',').map(x=>x.trim()).filter(Boolean),lot_id:v.lot_id||null,physical_confirmed:v.physical_confirmed},key),'Record receipt','New durable equipment begins in inspection, not automatically usable stock. Partial deliveries keep discrepancies visible.');break;}
    case 'key-out':form('Record key sign-out',[field('borrower','Resident account code','text','',{full:true}),field('key_code','Key code','text','SPORTS_ROOM',{full:true})],(v,key)=>command('key_out',v,key),'Record key custody','No equipment is issued by this key event. Continue the existing ID/register process.');break;
    case 'key-back':confirmCommand('Record key return','key_back',record('keys',id),[],{},'This closes key custody only. Outstanding equipment borrowings remain open.');break;
    case 'audit-start':form('Start an independent audit snapshot',[field('assets','Eligible durable assets','multi',[],{items:data.assets.filter(a=>a.status!=='RETIRED').map(a=>[a.id,`${a.id} · ${a.name}`]),full:true}),field('method','Sampling rule, scope and limitations','textarea','',{full:true})],(v,key)=>command('audit_start',v,key),'Freeze record snapshot','Record actual observations within 15 minutes. Changed asset versions invalidate observations. A checker separate from the record operator and custodian is required.');break;
    case 'audit-observe':{const a=record('audits',id),remaining=a.snapshots.filter(s=>!a.observations.some(o=>o.asset_id===s.id));if(!remaining.length){confirmCommand('Close completed audit','audit_close',a,[],{},'All sampled items stay in the denominator. Unknowns are not silently removed.');break;}
      form('Record independent physical observation',[field('asset_id','Sampled item','select',remaining[0].id,{items:remaining.map(s=>[s.id,`${s.id} · ${s.name}`]),full:true}),field('location','Actual location','text','UNKNOWN'),field('custodian','Actual custodian / STORE','text','UNKNOWN'),field('condition','Observed condition','select','UNKNOWN',{items:['UNKNOWN','USABLE','DAMAGED','REPAIR','RETIRED']}),field('reference','Evidence reference / check notes','textarea','',{full:true})],(v,key)=>command('audit_observe',{id,version:a.version,...v},key),'Record observation','Use UNKNOWN where unassessable. Do not copy the record as ground truth. This observation does not correct inventory automatically.');break;}
    case 'audit-detail':{const a=record('audits',id);openDialog('Audit snapshot',`<p class="subtle">${date(a.snapshot_at)} · ${esc(a.method)}</p>${badge(a.provenance)}${table(['Asset','Location match','Custody match','Condition match','Assessability'],a.observations.map(o=>row([esc(o.asset_id),String(o.matches.location),String(o.matches.custodian),String(o.matches.condition),o.unknown?'Unknown':'Assessable'])))}`);break;}
    case 'conflict':form('Record reconciliation case',[field('asset_id','Equipment code'),field('description','Physical movement, interruption and observed state','textarea','',{full:true})],(v,key)=>command('conflict_record',v,key),'Save pending case','This records an exception without overwriting equipment state. A secretary must resolve it after checking.');break;
    case 'conflict-resolve':confirmCommand('Resolve after physical reconciliation','conflict_resolve',record('conflicts',id),[field('resolution','Physical findings and linked correction / event reference','textarea','',{full:true})]);break;
    case 'policy':{const p=data.settings[0];form('Record confirmed office policy',[field('threshold','Three-quotation threshold (₹)','number',p.threshold_paise/100,{min:.01,step:'.01'}),field('reference','Office authority / source reference','textarea',p.confirmation_reference||'',{full:true}),field('policy_confirmed','The hostel office has confirmed this procurement policy.','checkbox',p.policy_confirmed),field('ordinary_self_pickup','Enable routine 24/7 self-pickup declarations.','checkbox',p.ordinary_self_pickup)],(v,key)=>command('policy_update',{version:p.version,threshold_paise:Math.round(v.threshold*100),reference:v.reference,policy_confirmed:v.policy_confirmed,ordinary_self_pickup:v.ordinary_self_pickup},key));break;}
    case 'user-create':form('Create an authorized account',[field('username','Username / role code'),field('role','Role','select','student',{items:['student','captain','checker','guard','maintenance','secretary','office','admin']}),field('password','Initial password (12+ characters)','password','',{full:true,autocomplete:'new-password'})],async v=>{await api('/api/users',v);await refresh();},'Create account','Share credentials privately. Use pseudonymous account codes; never store ID-card scans here.');break;
    case 'user-update':{const u=data.users.find(x=>x.id===id);form('Change account access',[field('role','Role','select',u.role,{items:['student','captain','checker','guard','maintenance','secretary','office','admin']}),field('active','Account enabled','checkbox',u.active)],async v=>{await api('/api/users/update',{id,...v});await refresh();},'Update and revoke sessions');break;}
    case 'password':form('Change your password',[field('current_password','Current password','password','',{full:true,autocomplete:'current-password'}),field('password','New password (12+ characters)','password','',{full:true,autocomplete:'new-password'})],async v=>{await api('/api/account',v);closeDialog();login();},'Change password');break;
    case 'scan':openDialog('Scan equipment QR',`<div class="scanner-frame"><div class="scanner-placeholder">Point your camera at an equipment label</div><video id="qr-video" muted playsinline aria-label="Equipment QR camera"></video></div><div class="actions">${btn('Start camera','camera-start','','primary')} ${btn('Stop camera','camera-stop')}</div><p id="camera-status" class="form-hint" role="status">Camera images stay on your device. Scanning opens the asset; it never issues equipment automatically.</p><form id="scan-manual"><label for="equipment-code">Or enter the printed equipment ID</label><input id="equipment-code" name="code" placeholder="e.g. BD-001" required maxlength="300"><div class="modal-footer"><button type="submit" class="primary">Find equipment →</button></div><div id="scan-error" role="alert" class="form-error"></div></form>`,()=>{$('#scan-manual').onsubmit=e=>{e.preventDefault();try{scanFound(window.BTGScanner.parse(new FormData(e.target).get('code')));}catch(err){$('#scan-error').textContent=err.message;}};});break;
    case 'camera-start':window.BTGScanner.start($('#qr-video'),scanFound,msg=>{$('#camera-status').textContent=msg;});break;
    case 'camera-stop':window.BTGScanner.stop();$('#camera-status').textContent='Camera stopped. You can use the printed equipment ID.';break;
    case 'labels-select':form('Prepare registered asset labels',[field('assets','Equipment IDs to label','multi',labelIds,{items:data.assets.filter(a=>a.status!=='RETIRED').map(a=>[a.id,`${a.id} · ${a.name}`]),full:true}),field('tested','I understand that physical phone-camera and label durability checks are still required before live use.','checkbox',false,{must:true})],async v=>{labelIds=v.assets;render();},'Prepare label sheet','The integrated software has been tested; no physical field result is implied. Demo sheets remain clearly marked DEMO ONLY.');break;
    case 'labels-print':window.print();break;
    case 'export':{const out=await api('/api/export/aggregates');const blob=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='btg-anonymized-aggregates.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);break;}
  }
}
function scanFound(id) {if(!record('assets',id)){$('#scan-error').textContent='No registered equipment matches this code. Ask the secretary to register the physical item.';return;}window.BTGScanner.stop();closeDialog();assetDetail(id);}
document.addEventListener('click',e=>{const b=e.target.closest('[data-action]');if(!b)return;e.preventDefault();handleAction(b.dataset.action,b.dataset.id).catch(err=>toast(err.message));});
window.addEventListener('hashchange',()=>{closeDialog();if(me)render();});
window.addEventListener('offline',()=>{if(me)render();toast('Offline. Unconfirmed physical movements need reconciliation.');});
window.addEventListener('online',()=>{if(me)refresh().catch(err=>toast(err.message));});
refresh().catch(err=>{if(err.status===401)login();else $('#root').innerHTML=`<div class="loading"><h2>Unable to connect</h2><p>${esc(err.message)}</p>${btn('Try again','refresh')}</div>`;});
