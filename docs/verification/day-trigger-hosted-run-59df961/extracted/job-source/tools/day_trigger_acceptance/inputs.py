#!/usr/bin/env python3
"""Exact input derivation for the isolated, unpublished DayTrigger numeric build."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
INPUT_DIRECTORIES = ('source', 'test-support', 'tests', 'signing', 'tools', 'reference')


def require(value, message):
    if not value:
        raise ValueError(message)


def pairs(rows):
    result = {}
    for key, value in rows:
        require(key not in result, 'Duplicate JSON object key: ' + key)
        result[key] = value
    return result


def document(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Non-finite JSON number: ' + value)))


def read_json(path):
    return document(Path(path).read_bytes())


def encoded(value):
    return json.dumps(value, indent=2, ensure_ascii=True).encode()


def write_json(path, value, *, replace=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not replace:
        with path.open('xb') as stream:
            stream.write(encoded(value) + b'\n')
        return
    atomic_bytes(path, encoded(value) + b'\n')


def byte_identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def identity(path):
    path = Path(path)
    before = path.stat()
    require(stat.S_ISREG(before.st_mode) and not path.is_symlink(), 'Not a regular file: ' + str(path))
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'File changed while hashing: ' + str(path))
    return {'bytes': after.st_size, 'sha256': digest}


def relative(value):
    require(isinstance(value, str) and value and '\\' not in value and '\x00' not in value
            and not any(ord(char) < 32 for char in value), 'Invalid relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == value
            and ':' not in path.parts[0], 'Noncanonical or unsafe relative path: ' + value)
    return path


def regular(root, name):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'Invalid regular root: ' + str(root))
    path = root
    for part in relative(name).parts:
        path /= part
        require(not path.is_symlink(), 'Symlink in evidence/input path: ' + name)
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'Missing regular file: ' + str(path))
    require(path.resolve().is_relative_to(root.resolve()), 'Resolved path escaped root: ' + name)
    return path


def checked_identity(root, name, expected):
    path = regular(root, name)
    require(identity(path) == expected, 'Exact file identity differs: ' + name)
    return path


def metadata(value, size_key='size'):
    require(isinstance(value, dict) and set(value) == {size_key, 'sha256'}
            and type(value[size_key]) is int and value[size_key] >= 0
            and isinstance(value['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', value['sha256']),
            'Malformed exact file identity')


def snapshot(entries):
    require(isinstance(entries, dict) and entries, 'Empty or malformed input inventory')
    for name, value in entries.items():
        relative(name)
        metadata(value)
    entries = dict(sorted(entries.items()))
    canonical = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    return {'format': 1, 'files': len(entries),
            'snapshot_sha256': hashlib.sha256(canonical).hexdigest(), 'entries': entries}


def validate_snapshot(value):
    require(isinstance(value, dict) and set(value) == {'format', 'files', 'snapshot_sha256', 'entries'}
            and type(value['format']) is int and value['format'] == 1
            and type(value['files']) is int, 'Malformed complete input snapshot')
    actual = snapshot(value['entries'])
    require(value == actual, 'Complete input snapshot counters or digest differ')
    return actual


def input_name(name):
    path = relative(name)
    return ((len(path.parts) == 1 and path.suffix == '.py') or
            (path.parts[0] in INPUT_DIRECTORIES and '__pycache__' not in path.parts
             and not (path.parts[0] == 'tools' and 'classes' in path.parts)
             and path.suffix not in ('.pyc', '.pyo')))


def derive(base, changes):
    """Reconstruct the whole future inventory, including every unchanged baseline row."""
    base = validate_snapshot(base)
    require(isinstance(changes, list) and changes, 'Empty source change list')
    entries = dict(base['entries'])
    seen = set()
    for row in changes:
        require(isinstance(row, dict) and set(row) == {'path', 'baseline', 'candidate', 'must_be_absent_if_new', 'source'},
                'Unexpected source change fields')
        name = row['path']
        require(input_name(name) and name not in seen, 'Duplicate or excluded source change: ' + str(name))
        seen.add(name)
        require(row['source'] == 'project/' + name, 'Source change copy role differs: ' + name)
        metadata(row['candidate'], 'bytes')
        old = row['baseline']
        if old is None:
            require(row['must_be_absent_if_new'] is True and name not in entries, 'New source file already exists: ' + name)
        else:
            metadata(old, 'bytes')
            require(row['must_be_absent_if_new'] is False and entries.get(name) ==
                    {'size': old['bytes'], 'sha256': old['sha256']}, 'Source baseline differs: ' + name)
        entries[name] = {'size': row['candidate']['bytes'], 'sha256': row['candidate']['sha256']}
    return snapshot(entries)


def scan_inputs(root):
    """Independently enumerate the release-integrity scope; reject aliases and special files."""
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'Invalid input tree')
    names = []
    for directory in INPUT_DIRECTORIES:
        start = root / directory
        require(start.is_dir() and not start.is_symlink(), 'Missing input directory: ' + directory)
        for folder, dirs, files in os.walk(start, followlinks=False, onerror=lambda error: (_ for _ in ()).throw(error)):
            kept = []
            for name in sorted(dirs):
                if name == '__pycache__' or (directory == 'tools' and name == 'classes'):
                    continue
                path = Path(folder) / name
                require(not path.is_symlink(), 'Symlink input directory: ' + str(path))
                kept.append(name)
            dirs[:] = kept
            for name in sorted(files):
                if Path(name).suffix in ('.pyc', '.pyo'):
                    continue
                names.append((Path(folder) / name).relative_to(root).as_posix())
    names += [path.name for path in sorted(root.glob('*.py'))]
    require(len(names) == len(set(names)), 'Duplicate enumerated input role')
    entries, physical = {}, {}
    for name in sorted(names):
        path = regular(root, name)
        value = path.stat()
        key = (value.st_dev, value.st_ino)
        require(key not in physical, 'Physical input alias: ' + name + ' / ' + physical.get(key, ''))
        physical[key] = name
        value = identity(path)
        entries[name] = {'size': value['bytes'], 'sha256': value['sha256']}
    return snapshot(entries)


def compare_inputs(actual, expected):
    validate_snapshot(actual)
    validate_snapshot(expected)
    old, new = expected['entries'], actual['entries']
    missing, extra = sorted(old.keys() - new.keys()), sorted(new.keys() - old.keys())
    changed = sorted(name for name in old.keys() & new.keys() if old[name] != new[name])
    require(not (missing or extra or changed),
            'Full input inventory differs: ' + json.dumps({'missing': missing[:20], 'extra': extra[:20], 'changed': changed[:20]}))
    require(actual == expected, 'Complete source identity differs')


def atomic_bytes(path, raw):
    """Replace one owned output or reviewed source path without following an existing link."""
    path = Path(path)
    require(not path.is_symlink(), 'Refusing symlink replacement: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.day-numeric-', dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply_changes(root, capsule, changes):
    """Check every role before any of the nineteen narrowly scoped replacements."""
    root, capsule = Path(root), Path(capsule)
    payloads = []
    for row in changes:
        name = row['path']
        source = checked_identity(capsule, row['source'], row['candidate'])
        target = root.joinpath(*relative(name).parts)
        if row['baseline'] is None:
            require(not target.exists() and not target.is_symlink(), 'New source destination is present: ' + name)
        else:
            checked_identity(root, name, row['baseline'])
        parent = target.parent
        while parent != root:
            require(not parent.is_symlink(), 'Symlink replacement parent: ' + name)
            parent = parent.parent
        raw = source.read_bytes()
        require(byte_identity(raw) == row['candidate'], 'Candidate changed during source preflight: ' + name)
        payloads.append((name, target, raw, row['candidate']))
    for name, target, raw, expected in payloads:
        atomic_bytes(target, raw)
        require(identity(target) == expected, 'Atomic source replacement differs: ' + name)


def load_pins():
    return read_json(HERE / 'pins.json')


def checked_capsule(repository, specification):
    capsule = Path(repository) / relative(specification['path'])
    checkpoint = checked_identity(capsule, 'checkpoint.json', specification['checkpoint'])
    manifest = read_json(checkpoint)
    rows = manifest['files']
    require(isinstance(rows, list) and len(rows) == specification['file_count']
            and len({row['path'] for row in rows}) == len(rows), 'Source capsule inventory differs')
    actual = set()
    for path in capsule.rglob('*'):
        require(not path.is_symlink(), 'Symlink in frozen source capsule')
        if path.is_file(): actual.add(path.relative_to(capsule).as_posix())
    require(actual == {row['path'] for row in rows} | {'checkpoint.json'},
            'Frozen capsule has omitted or extra file roles')
    for row in rows:
        path = checked_identity(capsule, row['path'], {k: row[k] for k in ('bytes', 'sha256')})
        if 'mode' in row:
            require(type(row['mode']) is int and stat.S_IMODE(path.stat().st_mode) == row['mode'],
                    'Frozen capsule mode differs: ' + row['path'])
    return capsule, manifest


def combined_inventory_contract(pins, base, numeric_manifest, lookup_manifest):
    """Preserve both before-state boundaries; this does not scan a physical tree."""
    numeric_changes, lookup_changes = pins['source_changes'], pins['lookup_source_changes']
    require(len(numeric_changes) == 19 and len(lookup_changes) == 21, 'Combined source-stage path counts differ')
    numeric = derive(base, numeric_changes)
    require({k: numeric[k] for k in ('files', 'snapshot_sha256')} == pins['numeric_future_snapshot']
            and byte_identity(encoded(numeric)) == pins['numeric_future_manifest'], 'Derived numeric intermediate inventory differs')
    require(numeric_manifest['active_files'] == [] and numeric_manifest['source_changes'] == numeric_changes,
            'Frozen nineteen source roles differ')
    normalized = []
    for row in lookup_manifest['changes']:
        normalized.append({'path': row['path'],
                           'baseline': None if row['baseline'] is None else {k: row['baseline'][k] for k in ('bytes', 'sha256')},
                           'candidate': {k: row['after'][k] for k in ('bytes', 'sha256')},
                           'must_be_absent_if_new': row['must_be_absent_if_new'], 'source': 'project/' + row['path']})
    require(normalized == lookup_changes, 'Final lookup twenty-one source roles differ')
    future = derive(numeric, lookup_changes)
    require({k: future[k] for k in ('files', 'snapshot_sha256')} == pins['future_snapshot']
            and byte_identity(encoded(future)) == pins['future_manifest'], 'Derived combined future inventory differs')
    numeric_names = {row['path'] for row in numeric_changes}
    lookup_names = {row['path'] for row in lookup_changes}
    union = sorted(numeric_names | lookup_names)
    require(len(union) == 25 and union == pins['source_union_paths']
            and len(set(future['entries']) - set(base['entries'])) == 13, 'Combined union or new-input count differs')
    numeric_only = [{'path': name, **future['entries'][name]} for name in sorted(numeric_names - lookup_names)]
    require(len(numeric_only) == 4 and numeric_only == pins['numeric_only_files'], 'Four preserved numeric-only inputs differ')
    return numeric, future


def contract(baseline_repository, overlay_repository, lookup_repository):
    pins = load_pins()
    baseline_path = checked_identity(baseline_repository, pins['baseline_manifest']['path'],
                                     {k: pins['baseline_manifest'][k] for k in ('bytes', 'sha256')})
    base = validate_snapshot(read_json(baseline_path))
    require(base['files'] == pins['baseline_files'] and base['snapshot_sha256'] == pins['baseline_snapshot_sha256'],
            'Pinned baseline inventory differs')
    numeric_root, numeric_manifest = checked_capsule(overlay_repository, {
        'path': pins['overlay_capsule_path'], 'checkpoint': pins['overlay_checkpoint'], 'file_count': 408})
    roots, manifests = {}, {}
    for role in ('merge', 'successor'):
        roots[role], manifests[role] = checked_capsule(lookup_repository, pins['lookup_capsules'][role])
        require(manifests[role]['active_source_changed'] is False, 'Lookup capsule changed active application inputs')
    overlay = read_json(checked_identity(roots['successor'], 'complete-future-overlay-manifest.json', pins['lookup_final_overlay_manifest']))
    numeric, future = combined_inventory_contract(pins, base, numeric_manifest, overlay)
    payloads = []
    resolutions = pins['lookup_payload_resolutions']
    require(len(resolutions) == 21 and [r['path'] for r in resolutions] == [r['path'] for r in pins['lookup_source_changes']],
            'Final lookup payload selection differs')
    for row, resolution in zip(pins['lookup_source_changes'], resolutions):
        role = resolution['capsule']
        require(role in roots and resolution['source'] == row['source'], 'Lookup payload capsule or source role differs')
        require((role == 'successor') == (row['path'] in ('day_lookup_dex_controls.py', 'tests/test_day_lookup.py')),
                'Lookup successor must replace exactly its two reviewed files')
        source = checked_identity(roots[role], resolution['source'], row['candidate'])
        payloads.append({'path': row['path'], 'source': str(source), 'identity': row['candidate']})
    context = {'numeric_root': numeric_root, 'lookup_roots': roots, 'lookup_payloads': payloads,
               'baseline_snapshot': base, 'numeric_snapshot': numeric, 'future_snapshot': future}
    return pins, base, future, context


def prepared_stage_records(pins, context):
    records = []
    snapshots = [context['baseline_snapshot'], context['numeric_snapshot'], context['future_snapshot']]
    names = ['baseline', 'numeric', 'combined']
    for number, (stage, changes) in enumerate([('numeric', pins['source_changes']), ('lookup', pins['lookup_source_changes'])]):
        before, after = snapshots[number:number + 2]
        records.append({'stage': stage, 'source_paths': len(changes),
                        'new_files': sum(row['baseline'] is None for row in changes),
                        'before_snapshot': {k: before[k] for k in ('files', 'snapshot_sha256')},
                        'after_snapshot': {k: after[k] for k in ('files', 'snapshot_sha256')},
                        'before_scan': {'path': 'inputs/' + names[number] + '-complete-inputs.json', **byte_identity(encoded(before))},
                        'after_scan': {'path': 'inputs/' + names[number + 1] + '-complete-inputs.json', **byte_identity(encoded(after))}})
    return records


def verify_prepared_boundaries(pins, prepared, output, context):
    """Recheck the literal two-stage receipt and every retained source copy."""
    require(prepared.get('passed') is True and prepared.get('status') == 'EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED',
            'The exact two-stage preparation proof is absent')
    require(prepared.get('source_stages') == prepared_stage_records(pins, context), 'Physical source-stage receipt differs')
    for field, wanted in [('complete_baseline_files_checked', pins['baseline_files']),
                          ('complete_numeric_files_checked', pins['numeric_future_snapshot']['files']),
                          ('complete_future_files_checked', pins['future_snapshot']['files']),
                          ('numeric_source_changes_applied', 19), ('lookup_source_changes_applied', 21),
                          ('distinct_final_source_paths', 25), ('new_files', 13)]:
        require(type(prepared.get(field)) is int and prepared[field] == wanted, 'Preparation count differs: ' + field)
    for label, value in [('baseline', context['baseline_snapshot']), ('numeric', context['numeric_snapshot']), ('combined', context['future_snapshot'])]:
        path = checked_identity(output, 'inputs/' + label + '-complete-inputs.json', byte_identity(encoded(value)))
        require(read_json(path) == value, 'Retained physical scan differs: ' + label)
    for role, changes in [('overlay', pins['source_changes']), ('lookup-overlay', pins['lookup_source_changes'])]:
        for row in changes: checked_identity(output, 'inputs/' + role + '/' + row['source'], row['candidate'])
    for name, expected in [('source-checkpoint.json', pins['overlay_checkpoint']),
                           ('lookup-merge-checkpoint.json', pins['lookup_capsules']['merge']['checkpoint']),
                           ('lookup-successor-checkpoint.json', pins['lookup_capsules']['successor']['checkpoint']),
                           ('baseline-input-snapshot.json', {k: pins['baseline_manifest'][k] for k in ('bytes', 'sha256')}),
                           ('future-input-snapshot.json', pins['future_manifest'])]:
        checked_identity(output, 'inputs/' + name, expected)
    require(read_json(regular(output, 'inputs/source-changes.json')) == pins['source_changes']
            and read_json(regular(output, 'inputs/lookup-source-changes.json')) == pins['lookup_source_changes']
            and read_json(regular(output, 'inputs/pins.json')) == pins, 'Retained source-stage policy differs')
    for row in pins['baseline_repository_files']:
        checked_identity(output, 'inputs/baseline-tools/' + row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    return prepared['source_stages']


def verify_git_commit(root, expected):
    require(isinstance(expected, str) and re.fullmatch(r'[0-9a-f]{40}', expected), 'Invalid fixed Git commit')
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=15)
    require(result.returncode == 0 and result.stdout.strip() == expected, 'Checkout does not have the expected commit: ' + str(root))
    return {'path': str(Path(root).resolve()), 'commit': result.stdout.strip()}


def verify_runtime_manifest(expected_sha256):
    manifest_path = regular(HERE, 'runtime-files.json')
    require(identity(manifest_path)['sha256'] == expected_sha256, 'Hosted runtime manifest differs from the workflow pin')
    manifest = read_json(manifest_path)
    rows = manifest['files']
    require(manifest['schema'] == 1 and len(rows) == len({row['path'] for row in rows})
            and {row['path'] for row in rows} == {p.name for p in HERE.iterdir() if p.is_file() and p.name != 'runtime-files.json'},
            'Hosted runtime source inventory differs')
    for row in rows:
        checked_identity(HERE, row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    return {'manifest': identity(manifest_path), 'files': rows}
