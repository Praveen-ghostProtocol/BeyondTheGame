/* Pixel fixtures only, not phone-camera or label durability trials. */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const qrcode=require('../app/static/vendor/qrcode.js');
const jsQR=require('../app/static/vendor/jsQR.js');
const context={window:{},location:{origin:'https://equipment.example'},URL};
vm.runInNewContext(fs.readFileSync(require.resolve('../app/static/scanner.js'),'utf8'),context);
const parse=context.window.BTGScanner.parse;
function pixels(value,cell=5,quiet=4){
  const qr=qrcode(0,'M');qr.addData(value);qr.make();const modules=qr.getModuleCount(),size=(modules+quiet*2)*cell;
  const data=new Uint8ClampedArray(size*size*4);data.fill(255);
  for(let y=0;y<modules;y++)for(let x=0;x<modules;x++)if(qr.isDark(y,x))for(let j=0;j<cell;j++)for(let i=0;i<cell;i++){
    const offset=(((y+quiet)*cell+j)*size+(x+quiet)*cell+i)*4;data[offset]=data[offset+1]=data[offset+2]=0;
  }
  return {data,size};
}
for(const id of ['BD-001','CB-001','CH-002','CP-001','FB-003','VB-001','A'.repeat(64)])test('QR roundtrip '+id,()=>{
  const value='BTG:ASSET:'+id,{data,size}=pixels(value);const decoded=jsQR(data,size,size,{inversionAttempts:'attemptBoth'});
  assert.ok(decoded);assert.equal(decoded.data,value);assert.equal(parse(decoded.data),id);
});
test('Plain ID and same-origin deep link resolve',()=>{assert.equal(parse('BD-001'),'BD-001');assert.equal(parse('https://equipment.example/#asset/BD-001'),'BD-001');});
test('Foreign website QR rejected',()=>assert.throws(()=>parse('https://untrusted.example/#asset/BD-001')));
test('Executable HTML / javascript QR rejected',()=>{assert.throws(()=>parse('javascript:alert(1)'));assert.throws(()=>parse('<img onerror=alert(1)>'));});
test('Empty, malformed and oversized codes rejected',()=>{for(const value of ['', 'BTG:ASSET:', 'A'.repeat(65),'BD 001'])assert.throws(()=>parse(value));});
test('Inverted pixels decode with fallback',()=>{const {data,size}=pixels('BTG:ASSET:BD-001');for(let i=0;i<data.length;i+=4)data[i]=data[i+1]=data[i+2]=255-data[i];assert.equal(jsQR(data,size,size,{inversionAttempts:'attemptBoth'}).data,'BTG:ASSET:BD-001');});
test('Blank frame never fabricates an equipment ID',()=>{const data=new Uint8ClampedArray(200*200*4).fill(255);assert.equal(jsQR(data,200,200),null);});
