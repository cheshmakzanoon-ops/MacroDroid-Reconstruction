#!/usr/bin/env python3
"""Freeze source and every regular report artifact with exact inventory verification."""
from pathlib import Path
import argparse, datetime, gzip, hashlib, io, json, shutil, tarfile

ROOT = Path(__file__).resolve().parent

def identity(path):
    content = path.read_bytes()
    return {'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--operation', action='append', default=[])
    args = parser.parse_args()
    target = ROOT / 'checkpoints' / args.name
    if target.exists(): raise RuntimeError('Immutable checkpoint already exists')
    report = (ROOT / args.report).resolve()
    report.relative_to(ROOT / 'reports')
    result = json.loads((report / 'result.json').read_text())
    sources = [(path, 'inputs/' + path.relative_to(ROOT / 'inputs').as_posix())
               for path in sorted((ROOT / 'inputs').rglob('*')) if path.is_file()]
    for name in [args.document, 'prepare_inputs.py', 'freeze_day_checkpoint.py', *args.operation]:
        sources.append((ROOT / name, name))
    names = [name for _, name in sources]
    if len(names) != len(set(names)): raise RuntimeError('Duplicate source roles')
    target.mkdir(parents=True)
    source_rows = []
    for source, name in sources:
        if source.is_symlink(): raise RuntimeError('Unexpected source symlink')
        dest = target / name; dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        if identity(source) != identity(dest): raise RuntimeError('Copied source differs')
        source_rows.append({'path': name, **identity(dest)})
    evidence = [path for path in sorted(report.rglob('*')) if path.is_file()]
    if any(path.is_symlink() for path in report.rglob('*')): raise RuntimeError('Unexpected report symlink')
    archive = target / 'evidence.tar.gz'; evidence_rows = []
    with archive.open('xb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w') as stream:
            for path in evidence:
                name = path.relative_to(report).as_posix(); content = path.read_bytes()
                row = {'path': name, **identity(path)}; evidence_rows.append(row)
                item = tarfile.TarInfo(name); item.size = len(content); item.mode = path.stat().st_mode & 0o777
                item.mtime = 0; stream.addfile(item, io.BytesIO(content))
    with tarfile.open(archive, 'r:gz') as stream:
        if [item.name for item in stream.getmembers()] != [row['path'] for row in evidence_rows]:
            raise RuntimeError('Archived evidence membership mismatch')
        for row in evidence_rows:
            content = stream.extractfile(row['path']).read()
            if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
                raise RuntimeError('Archived evidence identity mismatch')
    checkpoint = {'status': result['status'], 'createdUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'scope': result['scope'], 'sourceFiles': source_rows,
                  'evidenceArchive': {'path': archive.name, **identity(archive)},
                  'evidenceFiles': evidence_rows, 'result': identity(report / 'result.json'),
                  'activeRegistryChanged': False, 'apkChanged': False}
    path = target / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), **identity(path), 'sourceFiles': len(source_rows),
                      'evidenceFiles': len(evidence_rows), 'archive': identity(archive)}, indent=2))

if __name__ == '__main__': main()
