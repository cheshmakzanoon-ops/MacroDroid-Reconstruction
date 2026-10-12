"""Bounded independent review of the frozen alarm14 workflow; no device execution."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import yaml

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
OUT = BASE / 'alarm14-workflow-review'
CAP = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/04-fourteen-screen-workflow')
GIT = BASE / 'verification.git'
HEAD = '3d91187924af10457366ede7a1a8f10d3a1a6ac4'
CP_SHA = '805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066'
WORKFLOW_SHA = '575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f'
OUT.mkdir()
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
sys.dont_write_bytecode = True

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ident(data):
    return {'bytes': len(data), 'sha256': sha(data)}

def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def safe(name):
    assert type(name) is str and name
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and '\\' not in name
    assert p.as_posix() == name

cp_raw = (CAP / 'checkpoint.json').read_bytes()
assert sha(cp_raw) == CP_SHA
cp = json.loads(cp_raw)
assert cp['android_executed'] is False and cp['active_changes'] is False
assert len(cp['files']) == 13
file_checks = []
for row in cp['files']:
    safe(row['path'])
    p = CAP / row['path']
    mode = p.lstat().st_mode
    assert stat.S_ISREG(mode) and not p.is_symlink()
    actual = ident(p.read_bytes())
    assert actual == {'bytes': row['bytes'], 'sha256': row['sha256']}
    file_checks.append({'path': row['path'], **actual, 'mode': oct(stat.S_IMODE(mode))})
dump('capsule-file-verification.json', file_checks)

mapping = json.loads((CAP / 'offline-evidence-manifest.json').read_bytes())
assert mapping['file_count'] == len(mapping['files']) == 11900
assert mapping['unique_archived_payloads'] == 317
assert len({r['path'] for r in mapping['files']}) == 11900
blobs = {}
with tarfile.open(CAP / 'offline-evidence-blobs.tar.gz', 'r:gz') as archive:
    for member in archive:
        safe(member.name)
        assert member.isfile() and not member.issym() and not member.islnk()
        assert member.name not in blobs
        data = archive.extractfile(member).read()
        assert len(data) == member.size and stat.S_IMODE(member.mode) == 0o644
        assert member.name == 'blobs/sha256/' + sha(data) + '.bin'
        blobs[member.name] = data
assert len(blobs) == 317

tree = {}
for entry in git('ls-tree', '-rz', '--full-tree', HEAD).split(b'\0'):
    if entry:
        info, path = entry.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        tree[path.decode()] = (mode, kind, oid)
workflow_name = '.github/workflows/editor-exact-alarm-navigation.yml'
assert workflow_name not in tree
git_cache = {}

def git_bytes(path):
    safe(path)
    mode, kind, oid = tree[path]
    assert kind == 'blob' and mode in ('100644', '100755')
    if oid not in git_cache:
        data = git('cat-file', 'blob', oid)
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid
        git_cache[oid] = data
    return git_cache[oid]

external = mapping['exact_already_published_runtime_inputs']
assert set(external) == {
    '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
    '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
    '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745',
}
external_checks = []
for digest, row in external.items():
    path = Path(row['source'])
    assert path.is_file() and not path.is_symlink()
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert actual == digest == row['sha256'] and path.stat().st_size == row['bytes']
    manifest_raw = git('show', row['durable_commit'] + ':' + row['durable_manifest'])
    manifest = json.loads(manifest_raw)
    if row['path'].endswith('.apk'):
        assert manifest['size_bytes'] == row['bytes'] and manifest['sha256'] == digest
    external_checks.append({'path': row['path'], 'bytes': row['bytes'], 'sha256': digest,
                            'durable_commit': row['durable_commit'],
                            'durable_manifest': row['durable_manifest'],
                            'durable_manifest_sha256': sha(manifest_raw),
                            'local_runtime_file_rehashed': True})
dump('external-input-verification.json', external_checks)

raw_rows = {}
used_blobs = set()
external_roles = 0
for row in mapping['files']:
    safe(row['path'])
    assert type(row['mode']) is int and row['mode'] in (0o644, 0o755)
    if 'archive_member' in row:
        assert 'external_input_sha256' not in row
        data = blobs[row['archive_member']]
        assert ident(data) == {'bytes': row['bytes'], 'sha256': row['sha256']}
        used_blobs.add(row['archive_member'])
    else:
        ext = external[row['external_input_sha256']]
        assert row['sha256'] == ext['sha256'] and row['bytes'] == ext['bytes']
        external_roles += 1
    raw_rows[row['path']] = row
assert used_blobs == set(blobs)
assert len(mapping['inert_symlink_controls']) == 1
assert mapping['inert_symlink_controls'][0]['restored_as_symlink'] is False

def raw(name):
    row = raw_rows[name]
    return blobs[row['archive_member']]

dump('archive-mapping-verification.json', {
    'archive': ident((CAP / 'offline-evidence-blobs.tar.gz').read_bytes()),
    'manifest': ident((CAP / 'offline-evidence-manifest.json').read_bytes()),
    'regular_file_roles': len(raw_rows), 'unique_payloads': len(blobs),
    'external_runtime_roles': external_roles,
    'all_members_and_role_bytes_modes_verified': True,
    'symlink_control_restored_or_executed': False,
})

workflow_raw = (CAP / workflow_name).read_bytes()
assert sha(workflow_raw) == WORKFLOW_SHA
workflow = yaml.safe_load(workflow_raw)
triggers = workflow.get('on', workflow.get(True))
assert triggers == {'push': {'branches': ['main'], 'paths': [workflow_name,
    'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen/**']}, 'workflow_dispatch': None}
assert workflow['permissions'] == {'contents': 'read'}
assert workflow['concurrency']['cancel-in-progress'] is False
assert len(workflow['jobs']) == 1
job = workflow['jobs']['editor-exact-alarm-navigation']
assert job['runs-on'] == 'ubuntu-24.04' and job['timeout-minutes'] == 75
steps = job['steps']
assert len(steps) == 8
assert steps[0]['uses'] == 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262'
assert steps[0]['with'] == {'persist-credentials': False}
assert steps[-1]['uses'] == 'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02'
assert steps[-1]['if'] == steps[-2]['if'] == 'always()'
assert steps[-1]['with']['include-hidden-files'] is True
assert steps[-1]['with']['path'] == 'ci-exact-alarm-navigation/'
assert all(s['run'].startswith('set -euo pipefail\n') for s in steps if 'run' in s)
assert '--accept-package-data-removal --observe-denial-handoff --settle-full-frames --observe-notification-readiness' in steps[5]['run']
assert '--id exact-alarm-navigation-fourteen-screen --timeout 2400' in steps[5]['run']
assert "trap cleanup_trigger_runtime EXIT" in steps[5]['run']
assert "sys.argv[3:] == ['0', '0', '0']" in steps[5]['run']

spec = importlib.util.spec_from_file_location('alarm14_reviewed_preparation', CAP / 'prepare_trigger_journey.py')
preparation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparation)
assert preparation.REPORT_SCHEMA == 6
assert preparation.READINESS_POLICY_SHA256 == 'ddcaa7d3751e701b923d382a2a4662514f79b9bdc9096f1e62600dffef5f3583'
assert preparation.NAVIGATION_POLICY_SHA256 == 'db0c6bc7802788fc649b47909500b050d173da62d0eb7bc9d226e4b824b63994'
assert preparation.GUARD == 'work-in-progress/exact-alarm-navigation/03-corrected-source-and-host-controls'
assert preparation.PACKAGE == 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'

source = {}
expected = []
def append(name, digest, size=None, destination=None):
    safe(name)
    data = source[name] if name in source else git_bytes(name)
    actual = ident(data)
    assert actual['sha256'] == digest and (size is None or actual['bytes'] == size), name
    source[name] = data
    expected.append({'path': name, 'copy': destination or 'executed-inputs/' + name, **actual})

for path, digest in preparation.PINS.items():
    append(path, digest)
for prefix, count in ((preparation.GUARD, 166), (preparation.ANIMATION, 9)):
    manifest = json.loads(source[prefix + '/checkpoint.json'])
    rows = manifest['files']
    assert len(rows) == count and len({r['path'] for r in rows}) == count
    for row in rows:
        append(prefix + '/' + row['path'], row['sha256'], row['bytes'])
        if prefix == preparation.GUARD and row['path'].startswith('replay-source/'):
            append(prefix + '/' + row['path'], row['sha256'], row['bytes'],
                   'reviewed-source/' + row['path'][len('replay-source/'):])
fixture_inputs = json.loads(source[preparation.GUARD + '/reports/inputs-before.json'])
fixture_rows = [(p, r) for p, r in fixture_inputs.items() if p.endswith('/evidence.zip')]
assert len(fixture_rows) == 2
for path, row in fixture_rows:
    append(path, row['sha256'], row['bytes'])
    append(path, row['sha256'], row['bytes'], 'reviewed-source/' + path)
source[workflow_name] = workflow_raw
append(workflow_name, WORKFLOW_SHA)
literal = re.findall(r'^          pins = (\{\n.*?^          \})$', workflow_raw.decode(), re.M | re.S)
assert len(literal) == 1
helper_pins = ast.literal_eval(literal[0])
assert list(helper_pins) == [preparation.PACKAGE + '/prepare_trigger_journey.py', preparation.PACKAGE + '/verify_trigger_journey.py']
for path, digest in helper_pins.items():
    source[path] = (CAP / path[len(preparation.PACKAGE) + 1:]).read_bytes()
    append(path, digest)
assert len(expected) == 295 and len({r['copy'] for r in expected}) == 295
assert len([r for r in expected if r['copy'].startswith('reviewed-source/')]) == 100
actual_preflight = json.loads(raw('private-inputs/ci-exact-alarm-navigation/input-preflight.json'))
assert actual_preflight['files'] == expected
copies = {}
for row in expected:
    name = 'private-inputs/ci-exact-alarm-navigation/' + row['copy']
    assert ident(raw(name)) == {'bytes': row['bytes'], 'sha256': row['sha256']}
    copies[row['copy']] = raw(name)
dump('independently-reconstructed-inputs.json', expected)

# A virtual read-only filesystem adapter supplies the exact hash-verified Git
# and archive bytes. It exercises the real inventory/policy functions without
# materializing APKs, invoking AAPT2, or running any Android command.
SOURCE_ROOT, OUTPUT_ROOT = Path('/review-source'), Path('/review-output')
class VirtualFile:
    def __init__(self, data): self.data = data
    def read_bytes(self): return self.data
    def read_text(self): return self.data.decode()

def checked_virtual(root, name):
    safe(name)
    values = source if root == SOURCE_ROOT else copies if root == OUTPUT_ROOT else None
    assert values is not None
    return VirtualFile(values[name])

preparation.checked_file = checked_virtual
assert preparation.expected_inputs(SOURCE_ROOT) == expected
controls = []
def check(label, report, passed, changed_copy=None, changed_source=None):
    old_copy = None
    old_source = None
    try:
        if changed_copy:
            name, value = changed_copy; old_copy = (name, copies[name]); copies[name] = value
        if changed_source:
            name, value = changed_source; old_source = (name, source[name]); source[name] = value
        try:
            value = preparation.verify_prepared_inputs(SOURCE_ROOT, OUTPUT_ROOT, report)
            result = {'label': label, 'accepted': True, 'roles': len(value)}
        except (ValueError, KeyError) as error:
            result = {'label': label, 'accepted': False, 'reason': type(error).__name__ + ': ' + str(error)}
        assert result['accepted'] is passed, result
        controls.append(result)
    finally:
        if old_copy: copies[old_copy[0]] = old_copy[1]
        if old_source: source[old_source[0]] = old_source[1]

check('exact-positive', copy.deepcopy(actual_preflight), True)
for label, rows in [('omitted-row', expected[1:]), ('empty-rows', []), ('reordered-rows', list(reversed(expected))), ('duplicated-row', expected + [expected[0]])]:
    candidate = copy.deepcopy(actual_preflight); candidate['files'] = rows
    check(label, candidate, False)
runtime = 'tools/android/bootstrap_android_runtime.py'
runtime_copy = next(r['copy'] for r in expected if r['path'] == runtime)
check('changed-source-and-copy-retained', copy.deepcopy(actual_preflight), False,
      (runtime_copy, source[runtime] + b'\n# changed synthetic input\n'),
      (runtime, source[runtime] + b'\n# changed synthetic input\n'))
check('changed-copy-retained', copy.deepcopy(actual_preflight), False,
      (runtime_copy, source[runtime] + b'\n# changed synthetic copy\n'))
for label, key, value in [('legacy-schema', 'requested_report_schema', 5),
                          ('boolean-schema', 'requested_report_schema', True),
                          ('changed-navigation-pin', 'exact_alarm_navigation_policy_sha256', '0'*64),
                          ('changed-readiness-pin', 'notification_readiness_policy_sha256', '0'*64)]:
    candidate = copy.deepcopy(actual_preflight); candidate[key] = value
    check(label, candidate, False)
check('exact-positive-restoration', copy.deepcopy(actual_preflight), True)
dump('inventory-boundary-controls.json', {'scope': 'Actual verifier functions over exact virtual file bytes; no device or copied program execution.', 'controls': controls})

validation = json.loads((CAP / 'offline-validation.json').read_bytes())
assert validation['passed'] is True and validation['android_executed'] is False
assert len(validation['commands']) == 63 and validation['prepared_input_copies'] == 295
assert validation == cp['offline_validation']
command_checks = []
for row in validation['commands']:
    actual = json.loads(raw('commands/' + row['label'] + '/command.json'))
    assert actual == row, row['label']
    stdout = raw('commands/' + row['label'] + '/stdout.txt')
    stderr = raw('commands/' + row['label'] + '/stderr.txt')
    assert row['timed_out'] is False and row['android_executed'] is False
    command_checks.append({'label': row['label'], 'exit_code': row['exit_code'],
                           'stdout': ident(stdout), 'stderr': ident(stderr)})
test_checks = []
for index, count in ((0, 6), (1, 209), (2, 10)):
    label = 'packaged-host-controls-' + str(index)
    row = next(r for r in validation['commands'] if r['label'] == label)
    assert row['exit_code'] == 0
    text = (raw('commands/' + label + '/stdout.txt') + raw('commands/' + label + '/stderr.txt')).decode()
    assert re.search(r'Ran ' + str(count) + r' tests in [0-9.]+s\s+OK\s*$', text), label
    passed_lines = [line for line in text.splitlines() if re.search(r'\.\.\. ok$', line)]
    assert len(passed_lines) == count, (label, len(passed_lines))
    test_checks.append({'label': label, 'test_count': count, 'individual_success_lines': len(passed_lines), 'exit_code': 0})
assert next(r for r in validation['commands'] if r['label'] == 'owned-cleanup-clean')['exit_code'] == 0
assert next(r for r in validation['commands'] if r['label'] == 'owned-cleanup-failed-journey')['exit_code'] == 7
assert next(r for r in validation['commands'] if r['label'] == 'owned-cleanup-failed-service')['exit_code'] == 1
dump('closed-offline-command-verification.json', {'commands': command_checks, 'test_results': test_checks})

for row in cp['files']:
    assert ident((CAP / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}
assert (CAP / 'checkpoint.json').read_bytes() == cp_raw
for path, data in source.items():
    if path in tree:
        assert git_bytes(path) == data
result = {
    'status': 'BOUNDED_FROZEN_ALARM14_WORKFLOW_REVIEW_PASSED',
    'completed_utc': datetime.now(timezone.utc).isoformat(),
    'checkpoint_sha256': CP_SHA, 'workflow_sha256': WORKFLOW_SHA,
    'fetched_dependency_commit': HEAD,
    'capsule_files': 13, 'archive_payloads': 317, 'mapped_regular_files': 11900,
    'independently_reconstructed_input_roles': 295, 'reviewed_source_files': 98,
    'closed_command_logs_verified': 63, 'host_test_successes_verified': 225,
    'new_virtual_inventory_controls': len(controls),
    'all_frozen_source_and_evidence_unchanged': True,
    'new_android_execution': False, 'new_application_or_apk_change': False,
    'proposed_active_workflow_absent': True,
    'verdict': 'No concrete blocker in the reviewed frozen workflow/input/finite-scope boundary. Approval is for the separately authorized fourteen-screen diagnostic only; its real runtime result remains pending.',
    'scope_limits': [
        'The original and candidate APK identities remain fixed.',
        'Thirteen inputs per run include one observed explanation OK; zero Settings inputs are permitted.',
        'Both policy checks and the full recorded comparison must validate; any pixel difference retains exit 2.',
        'The review verifies existing closed host results and twelve new virtual inventory cases; it does not rerun the 209-test suite or Android.',
        'External AAPT2 bytes were rehashed locally and its published archive manifest binding checked; this review does not freshly extract that tool from the archive.',
    ],
}
dump('result.json', result)
print(json.dumps(result))
