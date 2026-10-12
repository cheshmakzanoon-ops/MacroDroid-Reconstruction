"""Bounded read-only manifest-presence audit; this does not re-audit payloads."""
from pathlib import Path
import argparse, hashlib, json, subprocess

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--git-dir', type=Path, required=True)
p.add_argument('--commit', required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
by_oid = {}
for raw in subprocess.check_output(['git', '--git-dir=' + str(a.git_dir),
                                    'ls-tree', '-rz', a.commit]).split(b'\0'):
    if not raw:
        continue
    info, path = raw.split(b'\t', 1)
    mode, kind, oid = info.decode().split()
    if kind == 'blob' and (path.endswith(b'checkpoint.json') or path.endswith(b'/manifest.json')):
        by_oid.setdefault(oid, []).append(path.decode())
checks = []
for path in sorted(a.root.glob('*/checkpoints/*/checkpoint.json')):
    if not path.is_file() or path.is_symlink():
        continue
    data = path.read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    checks.append(dict(path=str(path.relative_to(a.root)), bytes=len(data),
                       sha256=hashlib.sha256(data).hexdigest(),
                       remote_paths=by_oid.get(oid, [])))
summary = dict(head=a.commit, bounded_pattern='*/checkpoints/*/checkpoint.json',
               local_checkpoints=len(checks),
               byte_identical_published_manifests=sum(bool(r['remote_paths']) for r in checks),
               unmatched=[r for r in checks if not r['remote_paths']],
               archive_and_payload_reverification_performed_here=False)
a.output.write_text(json.dumps(summary | dict(checks=checks), indent=2) + '\n')
print(json.dumps(summary))
