"""Freeze transport observations and verify both final immutable Git payloads."""
from pathlib import Path
import difflib
import hashlib
import json
import os
import stat
import subprocess

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
OUTPUT = ROOT / 'indicator-blob-transport-incident'
GIT = ROOT / 'verification.git'
COMMIT = '78d8a01d2e02d2fbfc4d1f20da644dcfd2f8ea1c'
TARGET = 'docs/verification/indicator-publication-transport/01-retained-retries'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(name, raw):
    with (OUTPUT / name).open('xb') as stream:
        stream.write(raw)
    (OUTPUT / name).chmod(0o644)

first = json.loads((OUTPUT / 'incident.json').read_bytes())
second = json.loads((OUTPUT / 'second-response.json').read_bytes())
items = [dict(path=first['context']['row']['path'], bytes=first['context']['row']['size_bytes'],
              sha256=first['context']['row']['sha256'], git_blob_sha1=first['context']['row']['git_blob_sha1']),
         dict(path=second['observed']['path'], bytes=second['observed']['bytes'],
              git_blob_sha1=second['observed']['expected_git_blob_sha1'])]
for item in items:
    raw = subprocess.check_output(['git', '--git-dir=' + str(GIT), 'cat-file', 'blob', COMMIT + ':' + item['path']])
    assert len(raw) == item['bytes']
    if 'sha256' in item:
        assert sha(raw) == item['sha256']
    else:
        item['sha256'] = sha(raw)
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == item['git_blob_sha1']
    item['fetched_exact_bytes_verified'] = True
assert second['observed']['isError'] is True
assert 'Mcp error: -32603: Internal error' in '\n'.join(second['observed']['text'])
assert first['context']['prior_result_body_not_retained'] is True
assert first['retry_result']['structuredContent']['sha'] == items[0]['git_blob_sha1']
old = (OUTPUT / 'upload-batch-before.js').read_text()
new = (OUTPUT / 'upload-batch-after.js').read_text()
patch = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                  fromfile='before/upload-batch.js', tofile='after/upload-batch.js'))
write('diagnostic-retention.patch', patch.encode())
write('fetched-payload-verification.json', (json.dumps(dict(commit=COMMIT, rows=items,
    raw_payload_copies_added=False, application_tests_executed=False), indent=2) + '\n').encode())
os.link(ROOT / 'indicator-and-numeric-art-progress-export/remote-verification.json', OUTPUT / 'whole-batch-fetched-verification.json')
os.link(Path(__file__), OUTPUT / 'executed-freezer.py')
write('README.md', b'''# Exact-byte publication retries

Two blob calls stopped the inactive indicator publication before a ref update. The first call did not satisfy the strict expected Git blob SHA check. Its response body was not retained, so this record does not classify it as a wrong returned digest rather than an error or missing digest. An identical-byte retry returned the exact expected SHA; that response is preserved.

The later call's retained response explicitly reports an MCP internal error. The unchanged pending bytes were retried through the same strict SHA check. Both final payloads were independently read from the fetched commit and checked for complete byte size, SHA-256 and Git blob SHA-1. The complete 3,484-path fetched verification is retained here. No active source, APK, workflow or application outcome changed in these transport steps.

The only uploader edit added diagnostic response retention immediately before its unchanged strict acceptance check. The original and successor implementations and their exact diff are preserved. The root cause of the first missing response and of the connector internal error is not established here.
''')
files=[]
for path in sorted(OUTPUT.iterdir()):
    info=path.lstat();assert stat.S_ISREG(info.st_mode)
    raw=path.read_bytes()
    files.append(dict(path=path.name,bytes=len(raw),sha256=sha(raw),mode=stat.S_IMODE(info.st_mode)))
write('checkpoint.json',(json.dumps(dict(schema=1,repo_target=TARGET,active_files=[],
     status='TRANSPORT_RETRIES_PRESERVED_FINAL_FETCHED_BYTES_EXACT',files=files),indent=2)+'\n').encode())
print(json.dumps(dict(source=str(OUTPUT),target=TARGET,files=len(files),
     checkpoint_sha256=sha((OUTPUT/'checkpoint.json').read_bytes()))))
