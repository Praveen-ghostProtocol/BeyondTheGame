/* Synthetic Chromium integration. Uses the real HTTP handler + durable SQLite.
 * BTG_PLAYWRIGHT_PATH may point to an existing playwright/playwright-core module.
 * Default transport uses protocol byte streams because this workspace denies TCP.
 * It does not certify sockets, TLS, physical camera hardware or participant use.
 */
const assert=require('node:assert/strict');
const {spawn,spawnSync}=require('node:child_process');
const fs=require('node:fs');
const path=require('node:path');
const readline=require('node:readline');
const os=require('node:os');
const {chromium}=require(process.env.BTG_PLAYWRIGHT_PATH||'playwright');
const root=path.resolve(__dirname,'..');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'btg-e2e-'));
const db=path.join(temp,'browser.sqlite3');
const password='synthetic-browser-test-phrase';
const python=process.env.BTG_PYTHON||'python';
const setup=spawnSync(python,['-c',"import sys;sys.path.insert(0,'app');from domain import Store;from server import seed_demo;seed_demo(Store(sys.argv[1]),sys.argv[2])",db,password],{cwd:root,encoding:'utf8'});
if(setup.status!==0)throw new Error(setup.stderr||setup.stdout);
const bridge=spawn(python,[path.join(__dirname,'http_transport.py'),db],{cwd:root,stdio:['pipe','pipe','pipe']});
const pending=[];
readline.createInterface({input:bridge.stdout}).on('line',line=>{const task=pending.shift();if(!task)return;try{const r=JSON.parse(line);r.error?task.reject(new Error(r.error)):task.resolve(r);}catch(e){task.reject(e);}});
bridge.stderr.on('data',buf=>process.stderr.write(buf));
function transport(p){return new Promise((resolve,reject)=>{pending.push({resolve,reject});bridge.stdin.write(JSON.stringify(p)+'\n');});}
const checks=[];let browser;
function checked(name,condition=true){assert.ok(condition,name);checks.push(name);console.log('PASS',name);}
async function attach(context){
  await context.route('http://127.0.0.1:8000/**',async route=>{
    const req=route.request();const u=new URL(req.url());
    const r=await transport({method:req.method(),path:u.pathname+u.search,headers:await req.allHeaders(),body:(req.postDataBuffer()||Buffer.alloc(0)).toString('base64')});
    await route.fulfill({status:r.status,headers:r.headers,body:Buffer.from(r.body,'base64')});
  });
}
async function login(page,role){await page.goto('http://127.0.0.1:8000/');await page.getByLabel('Username',{exact:true}).fill(role);await page.getByLabel('Password',{exact:true}).fill(password);await page.getByRole('button',{name:'Sign in →',exact:true}).click();await page.getByRole('heading',{name:'Ready for the next game.'}).waitFor();}
async function navigate(page,hash){await page.goto('http://127.0.0.1:8000/#'+hash);await page.evaluate(()=>refresh());await page.locator('#content h1').waitFor();}
async function dialogSubmit(page,name='Save record'){await page.getByRole('dialog').getByRole('button',{name,exact:true}).click();await page.locator('#modal').waitFor({state:'hidden'});}
async function command(page,action,payload){return page.evaluate(async({action,payload})=>{const s=await fetch('/api/state').then(r=>r.json());const r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':s.csrf,'Idempotency-Key':crypto.randomUUID()},body:JSON.stringify({action,payload})});const out=await r.json();if(!r.ok)throw new Error(out.error);return out.result;},{action,payload});}
async function state(page){return page.evaluate(()=>fetch('/api/state').then(r=>r.json()));}
async function main(){
  browser=await chromium.launch({headless:true});
  const ctx=await browser.newContext({viewport:{width:1440,height:1050}});await attach(ctx);
  const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await login(page,'secretary');checked('Secretary signs in with persisted session');
  checked('Dashboard has 15 synthetic durable assets',(await state(page)).metrics.total===15);
  checked('Field accountability remains Not measured',(await state(page)).metrics.accountability.status==='NOT MEASURED');
  const shots=path.join(root,'.tmp','screenshots');fs.mkdirSync(shots,{recursive:true});
  await page.screenshot({path:path.join(shots,'desktop-overview.png'),fullPage:true});
  await navigate(page,'inventory');await page.getByLabel('Search inventory',{exact:true}).fill('CB-001');
  checked('Inventory filters by permanent asset ID',await page.locator('#inventory-rows tbody tr').count()===1);
  await page.getByRole('button',{name:'Open →',exact:true}).click();
  checked('Asset drawer opens with custody and condition',await page.getByRole('dialog').getByText('Accountable entity',{exact:true}).isVisible());
  await page.getByRole('button',{name:'Close dialog'}).click();await page.getByLabel('Search inventory',{exact:true}).fill('');
  await page.screenshot({path:path.join(shots,'desktop-inventory.png'),fullPage:true});
  async function rolePage(role,viewport){const c=await browser.newContext({viewport:viewport||{width:1440,height:1000}});await attach(c);const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await login(p,role);return p;}
  const student=await rolePage('student');
  await navigate(student,'inventory');await student.getByLabel('Search inventory',{exact:true}).fill('CB-001');
  await student.getByRole('button',{name:'Open →',exact:true}).click();await student.getByRole('button',{name:'Borrow this item',exact:true}).click();
  await student.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(student,'Confirm borrowing');
  let ss=await state(student),loan=ss.data.loans[0];
  checked('Direct borrowing creates an active loan without an approval step',loan.status==='ACTIVE');
  checked('Direct borrowing assigns private custody to the signed-in student',ss.data.assets.find(a=>a.id==='CB-001').custodian==='YOU');
  await student.getByRole('button',{name:'Open →',exact:true}).click();await student.getByRole('button',{name:'Return this item',exact:true}).click();
  await student.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(student,'Confirm return');
  checked('Return declaration keeps equipment unavailable',(await state(student)).data.assets.find(a=>a.id==='CB-001').status==='ISSUED');
  await student.getByRole('button',{name:'Open →',exact:true}).click();checked('Repeat scan cannot offer a duplicate return',await student.getByRole('button',{name:'Return this item',exact:true}).count()===0);await student.getByRole('button',{name:'Close dialog'}).click();
  const check=await rolePage('checker');await navigate(check,'borrowing');
  await check.getByRole('button',{name:'Receive items',exact:true}).click();await check.getByRole('dialog').getByLabel('Physically received components',{exact:true}).selectOption(['CB-001']);
  await check.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(check,'Confirm');
  checked('Physical receipt starts separate inspection',(await state(check)).data.assets.find(a=>a.id==='CB-001').status==='INSPECTION');
  await navigate(check,'inventory');await check.getByLabel('Search inventory',{exact:true}).fill('CB-001');await check.getByRole('button',{name:'Open →',exact:true}).click();
  await check.getByRole('button',{name:'Inspect condition',exact:true}).click();await check.getByLabel('Inspection result',{exact:true}).selectOption('USABLE');await check.getByLabel('Inspection method and findings',{exact:true}).fill('Synthetic browser inspection');await dialogSubmit(check,'Confirm');
  checked('Authorized inspection restores availability',(await state(check)).data.assets.find(a=>a.id==='CB-001').status==='AVAILABLE');
  await navigate(page,'repairs');await page.getByRole('button',{name:'+ Report damage',exact:true}).click();await page.getByLabel('Equipment ID (leave empty if unknown)').fill('CB-001');await page.getByLabel('What did you discover?').fill('Synthetic browser damage report');await dialogSubmit(page,'Report discovery');
  let current=(await state(page)).data.assets.find(a=>a.id==='CB-001');checked('Damage removes usable availability',current.status==='QUARANTINE');
  await command(page,'repair_create',{asset_id:current.id,version:current.version,assessment:'Synthetic',vendor:'TEST-SHOP',cost_paise:25000});
  for(const step of ['Authorize repair','Confirm vendor handoff','Record repair complete','Receive from vendor']){
    await navigate(page,'repairs');await page.getByRole('button',{name:step,exact:true}).click();await page.getByLabel('Authorization / handover evidence reference').fill('SYNTHETIC browser milestone');await dialogSubmit(page,'Confirm');
  }
  checked('Vendor return does not automatically certify usable',(await state(page)).data.assets.find(a=>a.id==='CB-001').status==='INSPECTION');
  current=(await state(check)).data.assets.find(a=>a.id==='CB-001');await command(check,'inspect',{id:current.id,version:current.version,condition:'USABLE',notes:'Synthetic reinspection'});
  const office=await rolePage('office');await navigate(office,'admin');await office.getByRole('button',{name:'Edit confirmed policy',exact:true}).click();await office.getByLabel('Office authority / source reference').fill('SYNTHETIC policy reference');await office.getByText('The hostel office has confirmed this procurement policy.',{exact:true}).check();await dialogSubmit(office);
  await navigate(page,'procurement');await page.getByRole('button',{name:'+ Purchase need',exact:true}).click();await page.getByLabel('Equipment / stock name').fill('Synthetic replacement bat');await page.getByLabel('Sport',{exact:true}).fill('Cricket');await page.getByLabel('Quantity needed').fill('2');await page.getByLabel('Estimated total (₹)').fill('9500');await page.getByLabel('Need, demand, repair alternatives and priority').fill('Synthetic repair alternative considered');await dialogSubmit(page);
  await page.getByRole('button',{name:'+ Quotation',exact:true}).click();await page.getByLabel('Vendor code').fill('TEST-VENDOR');await page.getByLabel('Quotation total (₹)').fill('9500');await page.getByLabel('Private document reference').fill('TEST-QUOTE');await dialogSubmit(page);
  for(const step of ['Record approval','Record payment']){await navigate(office,'procurement');await office.getByRole('button',{name:step,exact:true}).click();await office.getByLabel('Actual approval / payment reference').fill('SYNTHETIC office action');await dialogSubmit(office,'Confirm');}
  await navigate(page,'procurement');await page.getByRole('button',{name:'Receive stock',exact:true}).click();await page.getByLabel('New durable IDs, comma-separated').fill('RECEIPT-UI-001');await page.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(page,'Record receipt');
  checked('Partial delivery enrolls only one of two ordered assets',(await state(page)).data.purchases[0].received===1);
  checked('Received purchase requires inspection',(await state(page)).data.assets.find(a=>a.id==='RECEIPT-UI-001').status==='INSPECTION');
  const captain=await rolePage('captain');await navigate(captain,'kits');await captain.getByRole('button',{name:'Request team kit',exact:true}).click();await captain.getByLabel('Accountable team / group').fill('TEST-XI');await dialogSubmit(captain,'Create request');
  await navigate(page,'borrowing');await page.getByRole('button',{name:'Approve',exact:true}).click();await dialogSubmit(page,'Confirm');
  await navigate(captain,'borrowing');await captain.getByRole('button',{name:'Confirm pickup',exact:true}).click();await captain.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(captain,'Confirm');
  checked('One captain pickup commits all five kit components',(await state(captain)).data.loans.some(l=>l.team==='TEST-XI'&&l.remaining.length===5));
  await navigate(check,'borrowing');await check.getByRole('button',{name:'Receive items',exact:true}).click();await check.getByLabel('Physically received components',{exact:true}).selectOption(['CB-001','CB-002','CH-001','CH-002']);await check.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(check,'Confirm');
  checked('Partial kit return preserves exactly the missing pad set',(await state(captain)).data.loans.find(l=>l.team==='TEST-XI').remaining.join(',')==='CP-001');
  const guard=await rolePage('guard');await navigate(guard,'keys');await guard.getByRole('button',{name:'+ Key sign-out',exact:true}).click();await guard.getByLabel('Resident account code').fill((await state(student)).user.id);await dialogSubmit(guard,'Record key custody');await guard.getByRole('button',{name:'Record key return',exact:true}).click();await dialogSubmit(guard,'Confirm');checked('Guard key return remains separate from kit discrepancy',(await state(page)).data.loans.find(l=>l.team==='TEST-XI').remaining.length===1);
  const admin=await rolePage('admin');await navigate(admin,'admin');await admin.getByRole('button',{name:'+ Create account',exact:true}).click();await admin.getByLabel('Username / role code').fill('ui-resident');await admin.getByLabel('Initial password (12+ characters)').fill(password);await dialogSubmit(admin,'Create account');checked('Administrator account creation works through UI',(await state(admin)).data.users.length===9);
  await navigate(page,'audits');await page.getByRole('button',{name:'+ Start physical audit',exact:true}).click();await page.getByLabel('Eligible durable assets').selectOption(['FB-001']);await page.getByLabel('Sampling rule, scope and limitations').fill('Synthetic fixed single-item sample');await dialogSubmit(page,'Freeze record snapshot');
  await navigate(check,'audits');await check.getByRole('button',{name:'Continue audit',exact:true}).click();await check.getByLabel('Actual location').fill('SPORTS_ROOM');await check.getByLabel('Actual custodian / STORE').fill('STORE');await check.getByLabel('Observed condition').selectOption('USABLE');await check.getByLabel('Evidence reference / check notes').fill('SYNTHETIC CHECK');await dialogSubmit(check,'Record observation');await check.getByRole('button',{name:'Continue audit',exact:true}).click();await dialogSubmit(check,'Confirm');
  checked('Completed demo audit stays excluded from field KPI',(await state(check)).metrics.accountability.status==='NOT MEASURED');
  const mobile=await rolePage('student',{width:390,height:844});await mobile.getByRole('button',{name:'⌗  Scan QR',exact:true}).click();await mobile.getByLabel('Or enter the printed equipment ID').fill('FB-001');await mobile.getByRole('button',{name:'Find equipment →',exact:true}).click();checked('Manual scan fallback resolves registered asset',await mobile.getByRole('dialog').getByText('FB-001 · Football',{exact:true}).isVisible());
  await mobile.screenshot({path:path.join(shots,'mobile-asset.png'),fullPage:true});await mobile.getByRole('button',{name:'Close dialog'}).click();
  checked('Mobile viewport has no horizontal document overflow',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await mobile.getByRole('button',{name:'Toggle navigation'}).click();checked('Mobile navigation opens',await mobile.locator('.shell').evaluate(e=>e.classList.contains('menu-open')));
  await mobile.getByRole('button',{name:'Close navigation',exact:true}).click();checked('Mobile navigation has an accessible close control',!(await mobile.locator('.shell').evaluate(e=>e.classList.contains('menu-open'))));await mobile.getByRole('button',{name:'⌗  Scan QR',exact:true}).click();
  await mobile.evaluate(()=>{Object.defineProperty(navigator.mediaDevices,'getUserMedia',{configurable:true,value:async()=>{const e=new Error('Denied');e.name='NotAllowedError';throw e;}});});await mobile.getByRole('button',{name:'Start camera',exact:true}).click();await mobile.getByText('Camera permission declined. Use the equipment code below.',{exact:true}).waitFor();checked('Simulated camera denial presents working manual fallback');
  await mobile.getByRole('button',{name:'Close dialog'}).click();await mobile.getByRole('button',{name:'⌗  Scan QR',exact:true}).click();
  await mobile.evaluate(()=>{const qr=qrcode(0,'M');qr.addData('BTG:ASSET:FB-002');qr.make();const c=document.createElement('canvas'),s=qr.getModuleCount(),cell=8,quiet=4;c.width=c.height=(s+quiet*2)*cell;const x=c.getContext('2d');x.fillStyle='white';x.fillRect(0,0,c.width,c.height);x.fillStyle='black';for(let row=0;row<s;row++)for(let col=0;col<s;col++)if(qr.isDark(row,col))x.fillRect((col+quiet)*cell,(row+quiet)*cell,cell,cell);const stream=c.captureStream(10);window.__qrFixture={canvas:c,stream};Object.defineProperty(navigator.mediaDevices,'getUserMedia',{configurable:true,value:async()=>stream});});
  await mobile.getByRole('button',{name:'Start camera',exact:true}).click();await mobile.getByRole('dialog').getByText('FB-002 · Football',{exact:true}).waitFor();checked('Simulated video QR passes through actual camera decode loop');
  checked('Scanner stops video tracks after a match',await mobile.evaluate(()=>window.__qrFixture.stream.getTracks().every(t=>t.readyState==='ended')));
  await mobile.getByRole('button',{name:'Close dialog'}).click();checked('Scan does not automatically borrow equipment',!(await state(mobile)).data.loans.some(l=>l.remaining.includes('FB-002')));
  await navigate(page,'labels');await page.getByRole('button',{name:'Choose registered assets',exact:true}).click();await page.getByLabel('Equipment IDs to label').selectOption(['BD-001']);await page.getByRole('dialog').getByRole('checkbox').check();await dialogSubmit(page,'Prepare label sheet');checked('Label sheet is generated only on explicit registered-asset selection',await page.locator('.qr-label').count()===1);checked('Printed label uses the operational facility name',await page.locator('.qr-label').getByText('Beyond the Game · Alaknanda',{exact:true}).isVisible());
  await page.emulateMedia({media:'print'});checked('Print CSS hides application navigation',await page.locator('.sidebar').isHidden());await page.emulateMedia({media:'screen'});
  checked('Operational label page has no demo or simulated labels',!/\b(DEMO|SIMULATED)\b/i.test(await page.locator('#root').innerText()));
  checked('Historical provenance survives the label change',(await state(page)).data.events.some(e=>e.provenance==='SIMULATED'));
  checked('No JavaScript runtime errors across all roles',errors.length===0);
  const report={status:'PASSED',checks:checks.length,assertions:checks,runtime:{node:process.version,chromium:browser.version()},transport:'Real HTTP handler over byte streams; socket/TLS and physical camera not certified',provenance:'SIMULATED SOFTWARE TESTS',screenshots:shots};
  fs.mkdirSync(path.join(root,'.tmp'),{recursive:true});fs.writeFileSync(path.join(root,'.tmp','browser-e2e-result.json'),JSON.stringify(report,null,2));
}
main().then(()=>{console.log(JSON.stringify({status:'PASSED',checks,transport:'real HTTP handler over byte streams; no socket deployment certification'},null,2));}).catch(e=>{console.error(e.stack);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();bridge.stdin.end();bridge.kill();try{const resolved=fs.realpathSync(temp),allowed=fs.realpathSync(os.tmpdir())+path.sep;if(!resolved.startsWith(allowed)||!path.basename(resolved).startsWith('btg-e2e-'))throw new Error('Temporary cleanup path escaped expected directory');fs.rmSync(resolved,{recursive:true,force:true});}catch{}});
