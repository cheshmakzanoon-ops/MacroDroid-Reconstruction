"""Freeze the independent pin review and its retained reviewer log-layout failure."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
ROOT = BASE / 'numeric-filesystem-tooling-review'
PRIOR = BASE / 'numeric-filesystem-tooling-review-attempt01'
SOURCE = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
result = json.loads((ROOT / 'result.json').read_bytes())
assert result['status'] == 'INDEPENDENT_TOOLING_WORKFLOW_AND_INPUT_PINS_REVIEW_PASSED'
cp = json.loads((SOURCE / 'checkpoint.json').read_bytes())

def retain(source, relative):
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    assert source.read_bytes() == target.read_bytes()

for path in sorted(PRIOR.rglob('*')):
    if path.is_file():
        retain(path, 'initial-review-log-layout-failure/' + path.relative_to(PRIOR).as_posix())
for row in cp['active_files']:
    retain(SOURCE / row['source'], 'reviewed-source/' + row['path'])
(ROOT / 'README.md').write_text('''# Independent numeric tooling and workflow pin review

The frozen tooling successor passes this bounded activation-integrity review.
All 2,964 tooling payloads and all 408 source-successor payloads were rehashed
before and after. The complete 409-object source capsule at commit
`811f979eda1b937917c18defef38455c49a59062` matches local bytes and Git modes.
Every proposed active path matches its existing baseline at fetched commit
`867791e6ad0f7ffb14d9cea4a7f1d8fbea7e0477`.

The runtime manifest binds all seven other top-level tooling files, and its own
hash is fixed in the workflow. The parsed workflow equals the prior workflow
with only the reviewed runtime pin, immutable overlay checkout/path, owned host
test evidence environment and corresponding upload path changed. Action pins,
read-only permissions, timeout, failure verification and complete upload remain
unchanged. The job tools come from the triggering commit; application inputs
come from the immutable baseline and the nineteen-file source successor.

The complete 81,298-entry future input inventory reconstructs from the fetched
81,291-entry application baseline and exactly nineteen reviewed copy roles.
Only `day_numeric_dex_controls.py` differs from the earlier numeric overlay.
The full manifest bytes and canonical digest match their fixed identities.
`prepare.py` remains byte-identical; `inputs.py` changes only the required source
capsule count from 113 to 408. Every other input pin remains unchanged.

The existing full tooling run's 92 successes, nine exact executed source copies
and both raw log identities were independently checked. No test suite was
rerun here. The first review reader incorrectly expected every success to end
on its test-header line. One intended fail-fast control prints its diagnostic
before a standalone `ok`. The failed reviewer source, partial results and exact
host log remain under `initial-review-log-layout-failure`; the corrected reader
checks all 91 same-line successes and that single exact diagnostic/success pair.
The frozen production package was unchanged throughout.

The parent separately owns the producer/verifier semantic review and actual
small-child controls under the sibling `root-review` directory. This capsule
does not execute the full application acceptance, build an APK, run Android or
activate any proposed path. Both closed reviews and the complete frozen package
must be fetched before the authorized nine-path tooling activation. Active
application source and its current APK remain separate from that hosted WIP run.
''')
(ROOT / 'freeze_numeric_filesystem_tooling_review.py').write_bytes(Path(__file__).read_bytes())
files = []
for path in sorted(ROOT.rglob('*')):
    if path.is_dir():
        continue
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) and stat.S_IMODE(mode) in (0o644, 0o755)
    raw = path.read_bytes()
    files.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest(), 'mode': stat.S_IMODE(mode)})
checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
              'status': result['status'], 'active_files': [],
              'repo_target': 'docs/verification/day-numeric-filesystem-successor/tooling-pin-review',
              'reviewed_checkpoint_sha256': result['checkpoint_sha256'],
              'application_or_android_execution': False, 'files': files}
raw = (json.dumps(checkpoint, indent=2) + '\n').encode()
with (ROOT / 'checkpoint.json').open('xb') as stream:
    stream.write(raw)
print(json.dumps({'path': str(ROOT / 'checkpoint.json'), 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest(), 'files': len(files),
                  'payload_bytes': sum(row['bytes'] for row in files)}))
