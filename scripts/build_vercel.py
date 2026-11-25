"""Create an explicit static allowlist; no research/private files enter public/."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / 'app/static'
PUBLIC = ROOT / 'public'
ASSETS = ('index.html', 'style.css', 'app.js', 'scanner.js', 'favicon.svg',
          'vendor/jsQR.js', 'vendor/qrcode.js')
for name in ASSETS:
    target = PUBLIC / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STATIC / name, target)
print('Prepared static frontend:', len(ASSETS), 'allowlisted files')
