"""A4 pilot stickers from registered IDs; no credentials or personal data."""
import json
import subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
assets = [(f'BD-{i:03}', 'Badminton racket') for i in range(1, 5)]
assets += [(f'CB-{i:03}', 'Cricket bat') for i in range(1, 3)]
assets += [(f'CH-{i:03}', 'Cricket helmet') for i in range(1, 3)]
assets += [('CP-001', 'Batting pad set')]
assets += [(f'FB-{i:03}', 'Football') for i in range(1, 4)]
assets += [(f'VB-{i:03}', 'Volleyball') for i in range(1, 4)]
assets += [('TT-rac-001', 'Table tennis racket 1')]
js = """const qr=require('./app/static/vendor/qrcode.js');const ids=JSON.parse(process.argv[1]);console.log(JSON.stringify(ids.map(id=>{const q=qr(0,'M');q.addData('BTG:ASSET:'+id);q.make();return Array.from({length:q.getModuleCount()},(_,r)=>Array.from({length:q.getModuleCount()},(_,c)=>q.isDark(r,c)));})));"""
matrices = json.loads(subprocess.check_output(['node', '-e', js, json.dumps([a[0] for a in assets])], cwd=ROOT))
path = OUT / 'BeyondTheGame_Equipment_QR_Labels.pdf'
c = canvas.Canvas(str(path), pagesize=A4)
c.setTitle('Beyond the Game - Equipment QR labels')
c.setAuthor('Beyond the Game project team')
checks = []
for page in range(2):
    c.setFillColorRGB(.07,.27,.20); c.setFont('Helvetica-Bold', 17)
    c.drawString(12*mm, 282*mm, 'BEYOND THE GAME | EQUIPMENT LABELS')
    c.setFillColorRGB(0,0,0); c.setFont('Helvetica', 9)
    c.drawString(12*mm, 275*mm, 'A4 - Actual size / 100% - Single-sided - Do not fit to page')
    c.drawString(12*mm, 270*mm, 'Cut on dashed borders. Match each ID to one item. Test one label before attaching the batch.')
    c.drawString(12*mm, 265*mm, 'Open the app, sign in, then use Scan QR. These codes contain equipment IDs, not website links.')
    for i in range(page*8, min(page*8+8,len(assets))):
        aid,name=assets[i]; row,col=divmod(i-page*8,2)
        x=(12+97*col)*mm; y=(205-63*row)*mm; w,h=89*mm,55*mm
        c.setStrokeColorRGB(.65,.65,.65); c.setLineWidth(.4); c.setDash(2,2)
        c.rect(x,y,w,h); c.setDash()
        c.setFillColorRGB(0,0,0); c.setFont('Helvetica-Bold',8)
        c.drawString(x+4*mm,y+48*mm,'BEYOND THE GAME / ALAKNANDA')
        qx,qy=x+4*mm,y+10*mm; size=32*mm; matrix=matrices[i]; n=len(matrix); cell=size/(n+8)
        c.setFillColorRGB(1,1,1);c.rect(qx,qy,size,size,stroke=0,fill=1)
        c.setFillColorRGB(0,0,0)
        for r in range(n):
            for colm in range(n):
                if matrix[r][colm]: c.rect(qx+(colm+4)*cell,qy+(n+3-r)*cell,cell,cell,stroke=0,fill=1)
        c.setFont('Courier-Bold',10);c.drawCentredString(qx+size/2,y+5*mm,aid)
        tx=x+40*mm;ty=y+37*mm;c.setFont('Helvetica-Bold',11)
        for line in simpleSplit(name,'Helvetica-Bold',11,45*mm):c.drawString(tx,ty,line);ty-=13
        c.setFont('Helvetica',8)
        for line in ['Scan in the BTG app','Borrow when taking','Scan again to return']:
            c.drawString(tx,y+(21-4*['Scan in the BTG app','Borrow when taking','Scan again to return'].index(line))*mm,line)
        checks.append({'page':page,'id':aid,'qr_rect':[qx,qy,size,size]})
    c.setFont('Helvetica',8);c.drawString(12*mm,8*mm,'One permanent ID per item. Reprint the same ID when replacing a label.')
    c.drawRightString(198*mm,8*mm,f'{page+1} / 2');c.showPage()
c.save()
(ROOT / '.tmp/label-checks.json').write_text(json.dumps(checks))
print(path)
