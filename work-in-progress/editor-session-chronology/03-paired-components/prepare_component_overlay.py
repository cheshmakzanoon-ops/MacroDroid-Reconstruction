"""Copy only the hash-pinned session02 inputs into a separate small worktree."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
source = ROOT / 'checkpoints/02-against-4745809'
manifest_path = source / 'checkpoint.json'
assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == 'b0b6929d2962d6c505cbfb68e73828365b111610969ea6fc5a9ab18a6c3e2bd1'
manifest = json.loads(manifest_path.read_bytes())
lookup = {row['path']: row for row in manifest['files']}
target = ROOT / 'component-pair-worktree'
target.mkdir(exist_ok=False)
rows = []
for relative in sorted(path[len('inputs/'):] for path in lookup if path.startswith('inputs/')):
    selected = 'proposed_files/' + relative if 'proposed_files/' + relative in lookup else 'inputs/' + relative
    row = lookup[selected]
    data = (source / selected).read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    out = target / relative
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    rows.append({'path': relative, 'bytes': len(data), 'sha256': row['sha256'], 'source': selected})
(ROOT / 'component-pair-input-manifest.json').write_text(json.dumps({
    'schema': 1, 'baseline_checkpoint': str(manifest_path),
    'baseline_checkpoint_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    'baseline_publication_commit': 'dfa130a90a271ad591dcdb86ec34ac4b6de8ddfb',
    'files': rows, 'file_count': len(rows), 'large_artifacts_copied': False}, indent=2) + '\n')
print(json.dumps({'files': len(rows), 'bytes': sum(row['bytes'] for row in rows), 'target': str(target)}))
