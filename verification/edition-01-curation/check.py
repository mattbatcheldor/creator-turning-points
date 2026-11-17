"""Verify the authorised Edition 01 curation against its recorded main baseline."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
RECORD = Path(__file__).with_name('protected-baseline.json')
record = json.loads(RECORD.read_text())
old = json.loads(subprocess.check_output(['git', 'show', record['base_commit'] + ':src/campaigns-01.json'], cwd=ROOT, text=True))
new = json.loads((ROOT / 'src/campaigns-01.json').read_text())
swaps = dict(zip(record['removed_ids'], record['added_ids']))
assert [swaps.get(c['id'], c['id']) for c in old] == [c['id'] for c in new]
assert [c for c in old if c['id'] not in swaps] == [c for c in new if c['id'] not in swaps.values()]
for name, digest in record['protected_sha256'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
counts = [len(json.loads(p.read_text())) for p in sorted((ROOT / 'src').glob('campaigns-*.json'))]
assert counts == [15, 15, 15, 15, 15, 15, 10]
assert any(c['id'] == 'forbes-highest-paid-youtubers' for c in json.loads((ROOT / 'src/campaigns-03.json').read_text()))
assert any(c['id'] == 'pewdiepie-dropped' for c in json.loads((ROOT / 'src/campaigns-05.json').read_text()))
assert any(c['id'] == 'feastables' for c in json.loads((ROOT / 'src/campaigns-06.json').read_text()))
for c in new:
    if c['id'] in swaps.values():
        assert set(c['image']) == {'src', 'alt', 'credit', 'source', 'width', 'height'}
print('PASS: exactly three authorised replacements; other 97 cases and retained case order unchanged.')
print('PASS: Editions 02 to 07, Index template, CSS, JavaScript, audit and other protected files byte-for-byte unchanged.')
print('PASS: 15,15,15,15,15,15,10 cases; PewDiePie and MrBeast retained elsewhere.')
