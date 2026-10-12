#!/usr/bin/env python3
"""Apply only the frozen lookup dependency delta to the frozen numeric recorder.

This is a small inactive source derivation, not a full-project snapshot or build.
All three ancestors are fixed independently of their mutable metadata rows.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import copy
import difflib
import gzip
import hashlib
import json
import shutil
import traceback

ROOT = Path(__file__).resolve().parent
BASE = Path('/workspace/scratch/4130730d15aa/day-trigger-integration/checkpoints/04-source-acceptance-integration')
OURS = ROOT / 'checkpoints/03-source-three-path-controls'
THEIRS = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
STAGE = ROOT / 'stage-03'
OUT = ROOT / 'reports/16-numeric-successor-merge'
MODULE = 'day_numeric_dex_controls.py'
ANCESTORS = {
    'numeric19': (BASE, 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'),
    'lookup07': (OURS, 'd40df7530d090b6717d99e5011f1a0e5c0774297576ecc88047737301812a292'),
    'numeric08': (THEIRS, 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'),
}
MODULE_PINS = {
    'numeric19': '2d5c58fc15dc50d74aeaf85802e5d57a785937439f6692772801a621209211e2',
    'lookup07': 'f211cfe656674f1bae4485d98bd2619ce03f53c2f5f80eae7fa8974617d1d1bc',
    'numeric08': '10bd78a41dcc9f16e0a301229e7b714189fd3bf7e497c5b35c49c7ccbcfd9e7c',
}
DEPENDENCY_NODES = {'DEPENDENCY_SHA256', 'LOOKUP_METHOD', 'LOOKUP_GETTERS',
                    'validate_dependency_declaration', 'validate_dependencies'}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': sha, 'mode': path.stat().st_mode & 0o777}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def verified_manifest(folder, expected):
    require(identity(folder / 'checkpoint.json')['sha256'] == expected, 'Ancestor checkpoint identity changed')
    rows = json.loads((folder / 'checkpoint.json').read_text())['files']
    paths = set()
    for row in rows:
        name = row['path']
        require(name not in paths and not Path(name).is_absolute() and '..' not in Path(name).parts,
                'Invalid ancestor inventory path')
        paths.add(name)
        actual = identity(folder / name)
        require(all(actual[key] == row[key] for key in ('bytes', 'sha256')), 'Ancestor payload changed: ' + name)
        if 'mode' in row:
            require(actual['mode'] == row['mode'], 'Ancestor mode changed: ' + name)
    return {'checkpoint': identity(folder / 'checkpoint.json'), 'verified_payload_files': len(paths)}


def function_block(text, start):
    begin = text.index(start)
    end = text.index('\n\ndef target_entry(', begin)
    return text[begin:end]


def pinned_merge(base, ours, theirs):
    for label, data in [('numeric19', base), ('lookup07', ours), ('numeric08', theirs)]:
        require(digest(data) == MODULE_PINS[label], 'Pinned module changed: ' + label)
    base, ours, theirs = (data.decode() for data in (base, ours, theirs))
    before_pin = "DEPENDENCY_SHA256 = 'e30552cc8ba0520bbee3a993298cb0bcaa973a9d4633649e80362d35b3eda631'"
    after_pin = "DEPENDENCY_SHA256 = '159061ce552e3364c113f28e72e5a4c1bc091a21153d0d5e0a793d2f773b0229'"
    old = function_block(base, 'def validate_dependencies(')
    new = function_block(ours, 'LOOKUP_METHOD = ')
    for name, text in [('numeric19', base), ('numeric08', theirs)]:
        require(text.count(before_pin) == 1 and text.count(old) == 1, 'Dependency splice anchors changed: ' + name)
    require(ours == base.replace(before_pin, after_pin).replace(old, new),
            'Lookup changed source outside its two exact dependency splices')
    return theirs.replace(before_pin, after_pin).replace(old, new).encode()


def nodes(text):
    result = {}
    for index, node in enumerate(ast.parse(text).body):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            key = node.name
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            key = node.targets[0].id
        else:
            key = 'other:' + ast.dump(node, include_attributes=False)
        require(key not in result, 'Duplicate top-level source identity: ' + key)
        result[key] = {'ast_sha256': digest(ast.dump(node, include_attributes=False).encode()),
                       'text_sha256': digest(ast.get_source_segment(text, node).encode()),
                       'kind': type(node).__name__}
    return result


def ast_proof(base, ours, theirs, merged):
    tables = {name: nodes(data.decode()) for name, data in
              [('numeric19', base), ('lookup07', ours), ('numeric08', theirs), ('merged', merged)]}
    without = lambda table: {key: row for key, row in table.items() if key not in DEPENDENCY_NODES}
    require(without(tables['numeric19']) == without(tables['lookup07']), 'Lookup ordinary code AST/text changed')
    require(without(tables['numeric08']) == without(tables['merged']), 'Merged recorder or ordinary code changed')
    require({key: tables['merged'][key] for key in DEPENDENCY_NODES} ==
            {key: tables['lookup07'][key] for key in DEPENDENCY_NODES}, 'Merged dependency AST/text differs from lookup')
    protected = ['command_clock', 'command_file_stat', 'CommandStreamEvidence', 'run_controls']
    return {'top_level_nodes': tables, 'exact_dependency_node_names': sorted(DEPENDENCY_NODES),
            'numeric19_vs_lookup_ordinary_nodes_exact': True,
            'numeric08_vs_merged_all_non_dependency_nodes_exact': True,
            'lookup_vs_merged_dependency_nodes_exact': True,
            'protected_recorder_and_runner_nodes': {key: tables['merged'][key] for key in protected},
            'text_outside_exact_two_splices_equal': True,
            'note': 'Text equality of the complete canonical splice additionally binds comments, whitespace, imports, every child argv and timeout.'}


def manifest_merge(old, changes):
    require(old['format'] == 1 and type(old['files']) is int and old['files'] == len(old['entries']),
            'Invalid baseline future manifest count')
    canonical = json.dumps(old['entries'], sort_keys=True, separators=(',', ':')).encode()
    require(digest(canonical) == old['snapshot_sha256'], 'Baseline future entry digest changed')
    entries = copy.deepcopy(old['entries'])
    require(len(changes) == 21 and len({r['path'] for r in changes}) == 21, 'Wrong 21-path merge domain')
    for row in changes:
        name = row['path']
        before = row['baseline']
        if before is None:
            require(name not in entries and row['must_be_absent_if_new'] is True, 'New lookup path was not absent: ' + name)
        else:
            require(entries.get(name) == {'size': before['bytes'], 'sha256': before['sha256']},
                    'Future baseline row changed: ' + name)
        entries[name] = {'size': row['after']['bytes'], 'sha256': row['after']['sha256']}
    require(len(entries) - len(old['entries']) == 6, 'Expected exactly six new future inputs')
    altered = set(row['path'] for row in changes)
    require(all(entries[key] == value for key, value in old['entries'].items() if key not in altered),
            'Unrelated future input changed')
    entries = dict(sorted(entries.items()))
    return {'format': 1, 'files': len(entries),
            'snapshot_sha256': digest(json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()),
            'entries': entries}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, OUT / 'executed-driver.py')
    report = {'status': 'RUNNING', 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'active_source_changed': False, 'full_source_tree_or_apk_copied': False}
    save(OUT / 'result.json', report)
    try:
        require(not STAGE.exists(), 'New merge stage already exists')
        ancestors = {name: verified_manifest(folder, expected) for name, (folder, expected) in ANCESTORS.items()}
        save(OUT / 'ancestor-verification.json', ancestors)
        data = {name: (folder / 'project' / MODULE).read_bytes() for name, (folder, _) in ANCESTORS.items()}
        merged = pinned_merge(data['numeric19'], data['lookup07'], data['numeric08'])
        proof = ast_proof(data['numeric19'], data['lookup07'], data['numeric08'], merged)
        for name, raw in {**data, 'merged': merged}.items():
            (OUT / (name + '-' + MODULE)).write_bytes(raw)
        save(OUT / 'three-way-ast-and-text-proof.json', proof)
        changes = copy.deepcopy(json.loads((OURS / 'merge-manifest.json').read_text())['changes'])
        successor = json.loads((THEIRS / 'checkpoint.json').read_text())
        same_numeric = []
        for row in successor['source_changes']:
            name = row['path']; src = THEIRS / row['source']; old = BASE / 'project' / name
            if name != MODULE:
                require(src.read_bytes() == old.read_bytes(), 'Unexpected numeric successor overlap: ' + name)
                same_numeric.append(name)
            target = STAGE / 'project' / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
        require(len(same_numeric) == 18, 'Numeric successor does not preserve its other 18 source files')
        for row in changes:
            name = row['path']; src = OURS / 'project' / name; target = STAGE / 'project' / name
            require(identity(src) == row['after'], 'Frozen lookup payload differs from merge declaration: ' + name)
            if name == MODULE:
                row['previous_numeric19_baseline'] = row['baseline']
                row['previous_lookup07_candidate'] = row['after']
                row['baseline'] = identity(THEIRS / 'project' / MODULE)
                row['baseline_source'] = str(THEIRS / 'project' / MODULE)
                target.write_bytes(merged)
                row['after'] = identity(target)
                row['reason'] = 'Exact two dependency splices onto the frozen filesystem recorder; every other byte is retained.'
            else:
                if row['baseline'] is None:
                    require(not target.exists(), 'New source path was not absent: ' + name)
                else:
                    require(identity(target) == row['baseline'], 'Non-overlap baseline mismatch: ' + name)
                target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, target)
            require(identity(target) == row['after'], 'Copied merged source identity changed: ' + name)
        require(len(changes) == 21, 'Source scope widened')
        files = sorted(path.relative_to(STAGE / 'project').as_posix() for path in (STAGE / 'project').rglob('*') if path.is_file())
        require(len(files) == 25, 'Expected 21 edited/new paths plus four unchanged numeric supporting paths')
        save(STAGE / 'merge-manifest.json', {'schema': 1, 'ancestors': ancestors, 'changes': changes,
             'unchanged_numeric_successor_paths': same_numeric, 'edited_or_new_paths': 21, 'copied_project_files': 25,
             'lookup07_other_twenty_source_files_byte_exact': True, 'active_source_changed': False})
        for label, old in [('numeric08', data['numeric08']), ('lookup07', data['lookup07'])]:
            patch = ''.join(difflib.unified_diff(old.decode().splitlines(keepends=True), merged.decode().splitlines(keepends=True),
                        fromfile=label + '/' + MODULE, tofile='merged/' + MODULE))
            (OUT / (label + '-to-merged.patch')).write_text(patch)
        compressed = THEIRS / 'evidence/future-input-snapshot.json.gz'
        manifest_raw = gzip.decompress(compressed.read_bytes())
        require({'bytes': len(manifest_raw), 'sha256': digest(manifest_raw)} == successor['future_manifest'],
                'Frozen full future manifest identity changed')
        old_manifest = json.loads(manifest_raw)
        require({key: old_manifest[key] for key in ('files', 'snapshot_sha256')} == successor['future_snapshot'],
                'Frozen full future snapshot header changed')
        future = manifest_merge(old_manifest, changes)
        raw = json.dumps(future, indent=2).encode()
        (OUT / 'future-input-snapshot.json.gz').write_bytes(gzip.compress(raw, mtime=0))
        save(OUT / 'future-manifest-derivation.json', {
            'scope': 'Derived complete future manifest. All unchanged rows were retained from a verified frozen full inventory; the full tree was not materialized or rehashed here.',
            'baseline_compressed_manifest': identity(compressed), 'baseline_manifest': successor['future_manifest'],
            'baseline_snapshot': successor['future_snapshot'], 'changed_existing_entries': 15, 'new_absent_entries': 6,
            'retained_existing_entries': len(old_manifest['entries']) - 15,
            'future_manifest': {'bytes': len(raw), 'sha256': digest(raw)},
            'future_snapshot': {key: future[key] for key in ('files', 'snapshot_sha256')},
            'compressed_future_manifest': identity(OUT / 'future-input-snapshot.json.gz')})
        controls = []
        def reject(name, action, reason):
            try:
                action()
            except RuntimeError as error:
                require(reason in str(error), 'Guard rejected for an unexpected reason: ' + name)
                controls.append({'name': name, 'rejected': True, 'error': str(error)})
            else:
                raise RuntimeError('Altered merge input was accepted: ' + name)
        for key in data:
            altered = dict(data); altered[key] += b'\n'
            reject('altered-' + key, lambda altered=altered: pinned_merge(altered['numeric19'], altered['lookup07'], altered['numeric08']), 'Pinned module changed')
        bad_recorder = merged.replace(b'time.monotonic_ns()', b'time.time_ns()', 1)
        require(bad_recorder != merged, 'Recorder fault was a no-op')
        reject('recorder-clock-substitution', lambda: ast_proof(data['numeric19'], data['lookup07'], data['numeric08'], bad_recorder), 'recorder or ordinary code')
        bad_dependency = merged.replace(b"keys.count(LOOKUP_METHOD) == 1", b"keys.count(LOOKUP_METHOD) >= 1", 1)
        require(bad_dependency != merged, 'Dependency fault was a no-op')
        reject('duplicate-consumer-loosening', lambda: ast_proof(data['numeric19'], data['lookup07'], data['numeric08'], bad_dependency), 'dependency AST/text')
        bad = copy.deepcopy(old_manifest); bad['entries'][MODULE]['sha256'] = '0' * 64
        bad['snapshot_sha256'] = digest(json.dumps(bad['entries'], sort_keys=True, separators=(',', ':')).encode())
        reject('rehashed-wrong-baseline-module-row', lambda: manifest_merge(bad, changes), 'baseline row changed')
        new_name = next(row['path'] for row in changes if row['baseline'] is None)
        bad = copy.deepcopy(old_manifest); bad['entries'][new_name] = {'size': 0, 'sha256': digest(b'')}
        bad['files'] += 1; bad['snapshot_sha256'] = digest(json.dumps(bad['entries'], sort_keys=True, separators=(',', ':')).encode())
        reject('rehashed-existing-new-path', lambda: manifest_merge(bad, changes), 'was not absent')
        reject('widened-path-domain', lambda: manifest_merge(old_manifest, changes + [copy.deepcopy(changes[0])]), '21-path merge domain')
        save(OUT / 'merge-guard-controls.json', {'scope': 'Source/inventory false-positive guards only; no application execution credit.',
                                                'controls': controls, 'passed': True})
        require(all(identity(folder / 'checkpoint.json')['sha256'] == expected for folder, expected in ANCESTORS.values()),
                'Ancestor checkpoint changed during derivation')
        save(OUT / 'merged-source-identities.json', {name: identity(STAGE / 'project' / name) for name in files})
        report.update(status='BOUNDED_NUMERIC_LOOKUP_MERGE_AND_FUTURE_MANIFEST_PASSED', passed=True,
                      edited_or_new_paths=21, copied_project_files=25, numeric_other_eighteen_files_unchanged=True,
                      lookup_other_twenty_files_unchanged=True, merge_guard_controls=len(controls),
                      merged_numeric_module=identity(STAGE / 'project' / MODULE),
                      future_manifest={'bytes': len(raw), 'sha256': digest(raw)},
                      future_snapshot={key: future[key] for key in ('files', 'snapshot_sha256')})
    except BaseException as error:
        report.update(status='MERGE_FAILED_PRESERVED', error=repr(error))
        (OUT / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(OUT / 'result.json', report)
        print(json.dumps(report, indent=2))
        require(sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file()) <= 256 * 1024 * 1024,
                'Owned initial workspace budget exceeded')


if __name__ == '__main__':
    main()
