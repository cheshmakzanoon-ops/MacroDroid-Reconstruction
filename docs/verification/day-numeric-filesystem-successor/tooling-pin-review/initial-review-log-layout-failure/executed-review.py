"""Independent frozen tooling, Git baseline, workflow and complete input pin review."""
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import yaml

ROOT = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
SOURCE = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
OUTPUT = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-filesystem-tooling-review')
GIT = ['git', '--git-dir=/dev/shm/macrodroid-transfer-space-20261012/verification.git']
HEAD = '867791e6ad0f7ffb14d9cea4a7f1d8fbea7e0477'
BASE = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
OVERLAY = '811f979eda1b937917c18defef38455c49a59062'
PREFIX = 'work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor'
CHECKPOINT = '815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493'
SOURCE_CHECKPOINT = 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'
RUNTIME = 'a1b6464be0603913f9fe37b0b90e7026034fd1823f3b24b949355109b9632428'
WORKFLOW = '.github/workflows/day-numeric-wip-acceptance.yml'
TOOL_PREFIX = 'tools/day_numeric_acceptance/'
TOOL_NAMES = {'README.md', 'inputs.py', 'pins.json', 'prepare.py', 'run_acceptance.py',
              'runtime-files.json', 'test_day_numeric_acceptance.py', 'verify.py'}
OUTPUT.mkdir(exist_ok=False)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(raw):
    return {'bytes': len(raw), 'sha256': digest(raw)}

def write(name, value):
    (OUTPUT / name).write_text(json.dumps(value, indent=2) + '\n')

def git_bytes(commit, path):
    return subprocess.check_output(GIT + ['show', commit + ':' + path])

def git_tree(commit, prefix):
    result = {}
    raw = subprocess.check_output(GIT + ['ls-tree', '-r', '-z', commit, '--', prefix])
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        assert kind == 'blob'
        result[name.decode()] = {'mode': mode, 'git_blob_sha1': oid}
    return result

def verify_capsule(root, expected_hash, expected_count):
    raw = (root / 'checkpoint.json').read_bytes()
    assert digest(raw) == expected_hash
    cp = json.loads(raw)
    assert len(cp['files']) == len({row['path'] for row in cp['files']}) == expected_count
    for row in cp['files']:
        name = PurePosixPath(row['path'])
        assert not name.is_absolute() and '..' not in name.parts and str(name) == row['path']
        path = root / row['path']; mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) and stat.S_IMODE(mode) in (0o644, 0o755)
        assert identity(path.read_bytes()) == {key: row[key] for key in ('bytes', 'sha256')}
    actual = set()
    for path in root.rglob('*'):
        assert not path.is_symlink()
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    assert actual == {row['path'] for row in cp['files']} | {'checkpoint.json'}
    return cp

cp = verify_capsule(ROOT, CHECKPOINT, 2964)
source_cp = verify_capsule(SOURCE, SOURCE_CHECKPOINT, 408)
assert cp['active_application_modified'] is False and cp['full_host_acceptance_executed'] is False
assert cp['android_executed'] is False and source_cp['active_files'] == []
assert cp['baseline_commit'] == BASE and cp['source_overlay_commit'] == OVERLAY
assert identity(git_bytes(OVERLAY, PREFIX + '/checkpoint.json')) == cp['source_overlay_checkpoint']
assert digest(git_bytes(OVERLAY, PREFIX + '/checkpoint.json')) == SOURCE_CHECKPOINT

source_tree = git_tree(OVERLAY, PREFIX)
assert set(source_tree) == {PREFIX + '/' + row['path'] for row in source_cp['files']} | {PREFIX + '/checkpoint.json'}
source_bindings = []
for name, entry in sorted(source_tree.items()):
    local = SOURCE / name.removeprefix(PREFIX + '/')
    raw = local.read_bytes()
    assert entry['git_blob_sha1'] == hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert int(entry['mode'], 8) & 0o777 == stat.S_IMODE(local.stat().st_mode)
    source_bindings.append({'path': name, **entry, **identity(raw)})
write('fetched-source-capsule-bindings.json', source_bindings)

active = cp['active_files']
assert len(active) == len({row['path'] for row in active}) == 9
assert {row['path'] for row in active} == {WORKFLOW} | {TOOL_PREFIX + name for name in TOOL_NAMES}
assert set(git_tree(HEAD, TOOL_PREFIX)) == {TOOL_PREFIX + name for name in TOOL_NAMES}
active_bindings = []
for row in active:
    assert row['source'] == 'source/' + row['path'] and row['must_be_absent'] is False
    assert row['mode'] == '100644'
    old = git_bytes(HEAD, row['path']); new = (ROOT / row['source']).read_bytes()
    assert identity(old) == row['baseline'] and identity(new) == row['candidate']
    assert git_tree(HEAD, row['path'])[row['path']]['mode'] == row['mode']
    assert stat.S_IMODE((ROOT / row['source']).stat().st_mode) == 0o644
    active_bindings.append({'path': row['path'], 'baseline_commit': HEAD, 'baseline': identity(old),
                            'candidate': identity(new), 'mode': row['mode']})
write('nine-active-baseline-bindings.json', active_bindings)

tools = ROOT / 'source/tools/day_numeric_acceptance'
runtime_raw = (tools / 'runtime-files.json').read_bytes()
assert digest(runtime_raw) == RUNTIME and identity(runtime_raw) == cp['runtime_manifest']
runtime = json.loads(runtime_raw)
assert runtime['schema'] == 1 and len(runtime['files']) == 7
assert {row['path'] for row in runtime['files']} == TOOL_NAMES - {'runtime-files.json'}
assert {p.name for p in tools.iterdir() if p.is_file()} == TOOL_NAMES
for row in runtime['files']:
    assert identity((tools / row['path']).read_bytes()) == {key: row[key] for key in ('bytes', 'sha256')}

workflow_raw = (ROOT / 'source' / WORKFLOW).read_bytes()
assert digest(workflow_raw) == '978579fa935cfd95423f6394fa0df3a1a6e7be8b6ceb5d60672ccb894ac08372'
assert identity(workflow_raw) == cp['workflow']
old_workflow_raw = git_bytes(HEAD, WORKFLOW)
workflow = yaml.load(workflow_raw, Loader=yaml.BaseLoader)
expected_workflow = yaml.load(old_workflow_raw, Loader=yaml.BaseLoader)
expected_workflow['env']['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256'] = RUNTIME
steps = expected_workflow['jobs']['isolated-numeric-source']['steps']
assert len(steps) == 10
steps[2]['with']['ref'] = OVERLAY
steps[2]['with']['sparse-checkout'] = PREFIX + '\n'
steps[5]['env'] = {'DAY_NUMERIC_CONTROL_EVIDENCE_ROOT': '${{ github.workspace }}/hosted-tool-control-evidence'}
old_paths = steps[-1]['with']['path']
assert old_paths.count('hosted-tool-host-tests.log\n') == 1
steps[-1]['with']['path'] = old_paths.replace('hosted-tool-host-tests.log\n',
                                            'hosted-tool-host-tests.log\nhosted-tool-control-evidence/\n')
assert workflow == expected_workflow
assert workflow['permissions'] == {'contents': 'read'}
assert workflow['jobs']['isolated-numeric-source']['timeout-minutes'] == '120'
assert workflow['concurrency']['cancel-in-progress'] == 'false'
assert workflow['jobs']['isolated-numeric-source']['steps'][-1]['with']['include-hidden-files'] == 'true'
(OUTPUT / 'prior-workflow.yml').write_bytes(old_workflow_raw)
write('workflow-structural-review.json', {
    'exact_prior_workflow_plus_four_reviewed_changes': True,
    'changes': ['runtime manifest pin', 'fixed overlay checkout and capsule path',
                'owned test evidence environment', 'owned test evidence upload path'],
    'baseline_checkout': BASE, 'overlay_checkout': OVERLAY, 'job_checkout': '${{ github.sha }}',
    'permissions': workflow['permissions'], 'timeout_minutes': 120,
    'all_action_pins_unchanged': True, 'failure_verifier_and_upload_preserved': True,
    'complete_output_archive_includes_hidden_workflow': True})

old_pins = json.loads(git_bytes(HEAD, TOOL_PREFIX + 'pins.json'))
pins = json.loads((tools / 'pins.json').read_bytes())
expected_pins = copy.deepcopy(old_pins)
for key in ('overlay_commit', 'overlay_capsule_path', 'overlay_checkpoint', 'future_snapshot', 'future_manifest'):
    expected_pins[key] = pins[key]
old_changes = expected_pins['source_changes']
new_changes = pins['source_changes']
assert len(new_changes) == 19 and new_changes == source_cp['source_changes']
changed_rows = []
for index, (old, new) in enumerate(zip(old_changes, new_changes)):
    if old != new:
        assert old['path'] == new['path'] == 'day_numeric_dex_controls.py'
        allowed = copy.deepcopy(old); allowed['candidate'] = new['candidate']
        assert allowed == new
        old_changes[index] = new
        changed_rows.append(new['path'])
assert changed_rows == ['day_numeric_dex_controls.py'] and expected_pins == pins
assert pins['baseline_commit'] == BASE and pins['overlay_commit'] == OVERLAY
assert pins['overlay_capsule_path'] == PREFIX and pins['overlay_checkpoint'] == cp['source_overlay_checkpoint']
assert pins['future_snapshot'] == cp['future_snapshot'] == source_cp['future_snapshot']
assert pins['future_manifest'] == cp['future_manifest'] == source_cp['future_manifest']
assert (tools / 'prepare.py').read_bytes() == git_bytes(HEAD, TOOL_PREFIX + 'prepare.py')
old_inputs = git_bytes(HEAD, TOOL_PREFIX + 'inputs.py')
assert old_inputs.count(b'== 113') == 2
assert old_inputs.replace(b'== 113', b'== 408') == (tools / 'inputs.py').read_bytes()

baseline_raw = git_bytes(BASE, pins['baseline_manifest']['path'])
assert identity(baseline_raw) == {key: pins['baseline_manifest'][key] for key in ('bytes', 'sha256')}
baseline = json.loads(baseline_raw)
assert baseline['files'] == len(baseline['entries']) == 81291
assert digest(json.dumps(baseline['entries'], sort_keys=True, separators=(',', ':')).encode()) == pins['baseline_snapshot_sha256']
future_raw = gzip.decompress((SOURCE / 'evidence/future-input-snapshot.json.gz').read_bytes())
assert identity(future_raw) == pins['future_manifest']
future = json.loads(future_raw)
expected_entries = dict(baseline['entries'])
for row in new_changes:
    candidate = (SOURCE / row['source']).read_bytes()
    assert identity(candidate) == row['candidate']
    if row['baseline'] is None:
        assert row['path'] not in expected_entries and row['must_be_absent_if_new'] is True
    else:
        assert expected_entries[row['path']] == {'size': row['baseline']['bytes'], 'sha256': row['baseline']['sha256']}
    expected_entries[row['path']] = {'size': len(candidate), 'sha256': digest(candidate)}
assert expected_entries == future['entries'] and len(expected_entries) == 81298
assert digest(json.dumps(expected_entries, sort_keys=True, separators=(',', ':')).encode()) == pins['future_snapshot']['snapshot_sha256']
write('complete-input-derivation.json', {
    'baseline_manifest': identity(baseline_raw), 'baseline_files': len(baseline['entries']),
    'source_changes': len(new_changes), 'only_changed_source_payload_from_prior_numeric': changed_rows,
    'future_manifest': identity(future_raw), 'future_snapshot': pins['future_snapshot'],
    'all_other_pins_and_prepare_bytes_unchanged': True, 'decompressed_large_manifest_written': False})

test_root = ROOT / 'evidence/08-complete-tooling-discovery'
test_result = json.loads((test_root / 'result.json').read_bytes())
assert test_result['returncode'] == 0 and test_result['passed'] is True and test_result['tests'] == 92
assert test_result['source_before'] == test_result['source_after']
for row in test_result['source_before']:
    assert identity((ROOT / 'source' / row['path']).read_bytes()) == {key: row[key] for key in ('bytes', 'sha256')}
    assert (test_root / 'executed-source' / row['path']).read_bytes() == (ROOT / 'source' / row['path']).read_bytes()
for role in ('stdout', 'stderr'):
    assert identity((test_root / (role + '.log')).read_bytes()) == test_result['streams'][role]
test_log = (test_root / 'stderr.log').read_text()
assert len(re.findall(r'^test[^\n]* \.\.\. ok$', test_log, re.M)) == 92
assert 'Ran 92 tests in 3.888s\n\nOK\n' in test_log
write('closed-host-test-evidence-verification.json', {
    'tests': 92, 'actual_result': identity((test_root / 'result.json').read_bytes()),
    'stderr': identity((test_root / 'stderr.log').read_bytes()), 'source_copies_exact': 9,
    'all_success_lines_present': True, 'tests_rerun_here': False})

assert verify_capsule(ROOT, CHECKPOINT, 2964) == cp
assert verify_capsule(SOURCE, SOURCE_CHECKPOINT, 408) == source_cp
result = dict(schema=1, status='INDEPENDENT_TOOLING_WORKFLOW_AND_INPUT_PINS_REVIEW_PASSED',
              checkpoint_sha256=CHECKPOINT, frozen_tooling_files=2964, frozen_source_files=408,
              source_overlay_commit=OVERLAY, active_baseline_observed_at=HEAD,
              proposed_active_files=9, runtime_manifest_sha256=RUNTIME,
              workflow_sha256=digest(workflow_raw), future_snapshot=pins['future_snapshot'],
              closed_host_test_successes_verified=92, sources_unchanged=True,
              active_changes=False, application_build_or_android_execution=False,
              verifier_recorder_semantics_review_owned_by_parent=True,
              completed_utc=datetime.now(timezone.utc).isoformat(),
              executed_source_sha256=digest(Path(__file__).read_bytes()))
write('result.json', result)
(OUTPUT / 'review_numeric_filesystem_tooling.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(result))
