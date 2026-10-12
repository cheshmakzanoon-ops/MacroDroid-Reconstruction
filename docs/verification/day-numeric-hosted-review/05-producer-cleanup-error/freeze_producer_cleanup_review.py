"""Freeze the bounded producer cleanup review, without editing the reviewed source."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat

root = Path('/dev/shm/macrodroid-transfer-space-20261012/producer-cleanup-review')
summary = json.loads((root / 'result.json').read_text())
assert summary['status'] == 'PARTIAL_ERROR_DESCRIPTOR_CLEANUP_GAP_REPRODUCED'
assert len(summary['cases']) == 2 and summary['source_unchanged'] is True
assert hashlib.sha256(Path(summary['source_path']).read_bytes()).hexdigest() == summary['source_sha256']
(root / 'README.md').write_text('''# Producer cleanup error review

The exact draft producer at SHA-256 `8e8c26a472c42843147d5aeca159cc48c61dd9d66ad7228059ce2d7d24808591`
has a reproducible partial-error cleanup gap. Its context exit loop catches a
stream-flush error, then calls `handle.close()` in an unguarded `finally` block.
When that close also raises, the loop exits before closing the remaining stdout
descriptor and before recording `finished`.

`result.json` records two direct calls to the actual source-derived context. The
ordinary empty-stream control closed both descriptors, completed its real
filesystem bracket, and recorded completion. The fault control injected a flush
error and a close error on stderr. The stderr descriptor closed, but stdout
remained open and completion was absent. The reviewer explicitly closed that
remaining descriptor after recording the observation. All created evidence files
and exact context observations are retained.

This is a synthetic I/O-error cleanup finding. No child process, Java, D8, Android,
full test suite, or full verifier was executed. It does not establish a false
acceptance or identify the cause of the earlier hosted timestamp failure. The
reviewed source remained byte-identical. A separately reviewed correction can
preserve this failure while continuing cleanup for every owned descriptor and
recording the final state even when fallback closure reports an error.
''')
(root / 'freeze_producer_cleanup_review.py').write_bytes(Path(__file__).read_bytes())
files = []
for path in sorted(root.rglob('*')):
    if path.is_dir():
        continue
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode)
    data = path.read_bytes()
    files.append(dict(path=path.relative_to(root).as_posix(), bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest(), mode='100644'))
value = dict(schema=1, created_utc=datetime.now(timezone.utc).isoformat(),
             status=summary['status'],
             repo_target='docs/verification/day-numeric-hosted-review/05-producer-cleanup-error',
             active_files=[], files=files, source_unchanged=True,
             application_or_android_execution=False, false_acceptance_claimed=False)
raw = (json.dumps(value, indent=2) + '\n').encode()
with (root / 'checkpoint.json').open('xb') as stream:
    stream.write(raw)
print(json.dumps(dict(path=str(root / 'checkpoint.json'), bytes=len(raw),
                      sha256=hashlib.sha256(raw).hexdigest(), files=len(files),
                      payload_bytes=sum(row['bytes'] for row in files))))
