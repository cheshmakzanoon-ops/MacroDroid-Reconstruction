#!/usr/bin/env python3
"""Bind the tooling successor to the separately fetched immutable source capsule."""
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
TOOLS = SOURCE / 'tools/day_numeric_acceptance'
GIT = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
COMMIT = '811f979eda1b937917c18defef38455c49a59062'
OLD_COMMIT = '394234b0e74c9f1d660836c8f2a89901fe05ff9d'
CAPSULE = ROOT / 'checkpoints/01-command-filesystem-source-successor'
CP_SHA = 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'
OUT = ROOT / 'reports/07-final-tool-bindings-from-fetched-git'
OUT.mkdir(parents=True, exist_ok=False)

def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

cp = json.loads((CAPSULE / 'checkpoint.json').read_bytes())
assert identity(CAPSULE / 'checkpoint.json')['sha256'] == CP_SHA
git_command = ['git', '--git-dir=' + str(GIT), 'show', COMMIT + ':' + cp['repo_target'] + '/checkpoint.json']
git = subprocess.run(git_command, capture_output=True, timeout=15)
assert git.returncode == 0 and hashlib.sha256(git.stdout).hexdigest() == CP_SHA
def git_blob(commit, name):
    result = subprocess.run(['git', '--git-dir=' + str(GIT), 'show', commit + ':' + name], capture_output=True, timeout=15)
    assert result.returncode == 0, name
    return result.stdout
tree_command = ['git', '--git-dir=' + str(GIT), 'ls-tree', '-r', '-z', COMMIT, '--', cp['repo_target']]
tree = subprocess.run(tree_command, capture_output=True, timeout=15)
assert tree.returncode == 0
expected_tree = {}
for entry in tree.stdout.split(b'\0'):
    if not entry:
        continue
    header, path = entry.split(b'\t', 1)
    mode, kind, digest = header.decode().split()
    assert kind == 'blob'
    name = Path(path.decode()).relative_to(cp['repo_target']).as_posix()
    expected_tree[name] = {'mode': mode, 'git_blob_sha1': digest}
assert set(expected_tree) == {row['path'] for row in cp['files']} | {'checkpoint.json'}
source_rows = []
for name, expected in sorted(expected_tree.items()):
    path = CAPSULE / name
    raw = path.read_bytes()
    mode = '100755' if path.stat().st_mode & 0o111 else '100644'
    digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert expected == {'mode': mode, 'git_blob_sha1': digest}, name
    source_rows.append({'path': name, **identity(path), **expected})
write(OUT / 'fetched-source-tree-verification.json', {'command': tree_command, 'returncode': tree.returncode,
                                                    'files': source_rows})
baseline = []
for path in sorted(SOURCE.rglob('*')):
    if path.is_file():
        name = path.relative_to(SOURCE).as_posix()
        original = ROOT / 'baseline-source' / name
        assert git_blob(COMMIT, name) == original.read_bytes(), name
        baseline.append({'path': name, **identity(original)})
assert len(baseline) == 9
pins_path = TOOLS / 'pins.json'
pins = json.loads(pins_path.read_bytes())
assert pins['overlay_commit'] == OLD_COMMIT
pins['overlay_commit'] = COMMIT
write(pins_path, pins)
readme = TOOLS / 'README.md'
text = readme.read_text()
assert text.count('`' + OLD_COMMIT + '`') == 1
readme.write_text(text.replace('`' + OLD_COMMIT + '`', '`' + COMMIT + '`'))
workflow = SOURCE / '.github/workflows/day-numeric-wip-acceptance.yml'
text = workflow.read_text()
assert text.count('ref: ' + OLD_COMMIT) == 1
text = text.replace('ref: ' + OLD_COMMIT, 'ref: ' + COMMIT)
tests = TOOLS / 'test_day_numeric_acceptance.py'
tests.write_text(tests.read_text().replace('import hashlib\n', ''))
manifest = json.loads((TOOLS / 'runtime-files.json').read_bytes())
manifest['files'] = [{'path': path.name, **identity(path)} for path in sorted(TOOLS.iterdir())
                     if path.is_file() and path.name != 'runtime-files.json']
assert len(manifest['files']) == 7
write(TOOLS / 'runtime-files.json', manifest)
runtime_sha = identity(TOOLS / 'runtime-files.json')['sha256']
text, replaced = re.subn(r"(DAY_NUMERIC_RUNTIME_MANIFEST_SHA256: ')[0-9a-f]{64}(')",
                         lambda match: match[1] + runtime_sha + match[2], text)
assert replaced == 1
workflow.write_text(text)

# Only the fixed inventory length changes in the input reader. Preparation stays exact.
assert (TOOLS / 'prepare.py').read_bytes() == (ROOT / 'baseline-source/tools/day_numeric_acceptance/prepare.py').read_bytes()
old_inputs = (ROOT / 'baseline-source/tools/day_numeric_acceptance/inputs.py').read_text()
assert (TOOLS / 'inputs.py').read_text() == old_inputs.replace('== 113', '== 408')
for path in TOOLS.glob('*.py'):
    ast.parse(path.read_text())
names = {'command_clock', 'command_file_stat', 'CommandStreamEvidence'}
def producer(path):
    return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(path.read_text()).body
            if hasattr(node, 'name') and node.name in names}
assert producer(TOOLS / 'run_acceptance.py') == producer(CAPSULE / 'project/day_numeric_dex_controls.py')

sys.path.insert(0, str(TOOLS))
inputs = importlib.import_module('inputs')
runtime = inputs.verify_runtime_manifest(runtime_sha)
actual_pins = inputs.load_pins()
base_raw = git_blob(actual_pins['baseline_commit'], actual_pins['baseline_manifest']['path'])
assert inputs.byte_identity(base_raw) == {key: actual_pins['baseline_manifest'][key] for key in ('bytes', 'sha256')}
base = inputs.validate_snapshot(inputs.document(base_raw))
assert base['files'] == actual_pins['baseline_files'] and base['snapshot_sha256'] == actual_pins['baseline_snapshot_sha256']
assert cp['source_changes'] == actual_pins['source_changes'] and cp['active_files'] == []
future = inputs.derive(base, actual_pins['source_changes'])
assert actual_pins['overlay_commit'] == COMMIT
assert {'files': future['files'], 'snapshot_sha256': future['snapshot_sha256']} == cp['future_snapshot']
assert inputs.byte_identity(inputs.encoded(future)) == cp['future_manifest']

import yaml
loaded = yaml.load(workflow.read_text(), Loader=yaml.BaseLoader)
steps = loaded['jobs']['isolated-numeric-source']['steps']
checks = []
for index, step in enumerate(steps):
    if 'run' in step:
        command = ['bash', '-n']
        result = subprocess.run(command, input=step['run'].encode(), capture_output=True, timeout=15)
        assert result.returncode == 0, step['name']
        checks.append({'kind': 'bash-syntax-only', 'step': step['name'], 'argv': command,
                       'returncode': result.returncode, 'stderr': result.stderr.decode()})
for name in ('prepare.py', 'run_acceptance.py', 'verify.py'):
    command = [sys.executable, '-B', str(TOOLS / name), '--help']
    result = subprocess.run(command, capture_output=True, timeout=15,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(OUT)})
    assert result.returncode == 0
    (OUT / (name + '.help.stdout')).write_bytes(result.stdout)
    (OUT / (name + '.help.stderr')).write_bytes(result.stderr)
    checks.append({'kind': 'argument-import-only', 'argv': command, 'returncode': result.returncode})

final = [{'path': row['path'], **identity(SOURCE / row['path'])} for row in baseline]
report = {'schema': 1, 'status': 'FINAL_SOURCE_TOOL_BINDINGS_AND_BOUNDED_STATIC_CHECKS_PASSED',
          'scope': 'Immutable Git blob/input derivation and tooling/CLI checks; no materialization, Java, D8, application build or Android',
          'source_commit': COMMIT, 'source_checkpoint': identity(CAPSULE / 'checkpoint.json'),
          'fixed_commit_blob_check': {'argv': git_command,
                                     'returncode': git.returncode, 'sha256': hashlib.sha256(git.stdout).hexdigest()},
          'source_capsule_files': len(cp['files']), 'baseline_snapshot': {'files': base['files'], 'snapshot_sha256': base['snapshot_sha256']},
          'future_snapshot': cp['future_snapshot'], 'future_manifest': cp['future_manifest'],
          'complete_contract_payloads_checked_from_fetched_tree_and_local_closed_capsule': True,
          'production_contract_function_executed': False,
          'contract_scope': 'Exact fetched baseline blob, all 409 source capsule Git blobs/modes and the unchanged production derivation; no checkout or application materialization',
          'prepare_py_byte_identical': True,
          'inputs_py_only_inventory_count_diff': True, 'both_producer_helper_asts_identical': True,
          'runtime_manifest': identity(TOOLS / 'runtime-files.json'), 'runtime_verification': runtime,
          'active_repository_baselines': baseline, 'proposed_tool_files': final, 'checks': checks,
          'application_build_executed': False, 'active_promoted': False, 'full_runtime_1_to_1_established': False}
write(OUT / 'result.json', report)
print(json.dumps({'result': str(OUT / 'result.json'), 'runtime_sha256': runtime_sha,
                  'tool_files': len(final), 'source_files': len(cp['files']), 'future_snapshot': cp['future_snapshot'],
                  'checks': len(checks)}, indent=2))
