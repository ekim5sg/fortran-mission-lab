"""Generate a static dashboard from the actual, verified Fortran output files."""
from datetime import datetime, timezone
from decimal import Decimal
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

root = Path(__file__).resolve().parent
results = root / 'results'
subprocess.run(['python3', str(root / 'verify_outputs.py'), str(results / 'modern-output.txt'), str(results / 'fortran77-output.txt')], check=True)

def records(name):
    return [dict(day=int(day), km=int(Decimal(km))) for day, km in
            re.findall(r'Day\s+(\d+):\s+([\d.]+)\s+km', (results / name).read_text())]

repo = os.environ.get('GITHUB_REPOSITORY', 'ekim5sg/fortran-mission-lab')
sha = os.environ.get('GITHUB_SHA', '')
run_id = os.environ.get('GITHUB_RUN_ID', '')
base = 'https://github.com/' + repo
run_url = base + '/actions/runs/' + run_id if run_id else base + '/actions'
data = dict(modern=records('modern-output.txt'), legacy=records('fortran77-output.txt'))
site = root / '_site'
site.mkdir(exist_ok=True)
for name in ['styles.css', 'app.js']:
    shutil.copyfile(root / 'dashboard' / name, site / name)
for name in ['modern-output.txt', 'fortran77-output.txt', 'verification.txt', 'compiler.txt']:
    shutil.copyfile(results / name, site / name)
for name in ['mission.f90', 'mission77.f']:
    shutil.copyfile(root / name, site / name)
rows = ''.join(f'<tr><th scope="row">Day {a["day"]:02}</th><td>{a["day"]*24}</td><td>{a["km"]:,}</td><td>{b["km"]:,}</td><td class="match">Match</td></tr>' for a,b in zip(data['modern'],data['legacy']))
replacements = {
    'ROWS': rows,
    'DATA': json.dumps(data).replace('<', '\\u003c'),
    'MODERN_RAW': escape((results / 'modern-output.txt').read_text()),
    'LEGACY_RAW': escape((results / 'fortran77-output.txt').read_text()),
    'COMPILER': escape((results / 'compiler.txt').read_text().splitlines()[0]),
    'BUILT': datetime.now(timezone.utc).strftime('%b %d, %Y · %H:%M UTC'),
    'RUN_URL': escape(run_url, quote=True),
    'COMMIT_URL': escape(base + '/commit/' + sha if sha else base, quote=True),
    'COMMIT': escape(sha[:7] or 'local build'),
    'REPO_URL': escape(base, quote=True),
}
html = (root / 'dashboard/index.html').read_text()
for key, value in replacements.items():
    html = html.replace('@@'+key+'@@', value)
assert not re.search(r'@@[A-Z_]+@@', html)
(site / 'index.html').write_text(html)
(site / '.nojekyll').touch()
(site / 'results.json').write_text(json.dumps(data, indent=2))
print('Dashboard generated from verified program output: _site/index.html')
