"""Prepare exactly three reviewed combined-tooling checkout-layout changes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import stat
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--parent', required=True)
parser.add_argument('--receipt', type=Path, required=True)
args = parser.parse_args()
ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ['git', '--git-dir=' + str(ROOT / 'verification.git')]
PACKAGE = 'work-in-progress/day-trigger-lookup/13-checkout-layout-controls'
BASELINE = 'work-in-progress/day-trigger-lookup/12-combined-tooling-host-controls'
REVIEW = 'docs/verification/day-trigger-combined/checkout-correction-review'
LOCAL = Path('/dev/shm/macrodroid-day-lookup-checkout-fix/checkpoints/01-checkout-layout-controls')
EXPORT = ROOT / 'combined-checkout-correction-activation-export'
EXPECTED = {'.github/workflows/day-trigger-wip-acceptance.yml',
            'tools/day_trigger_acceptance/runtime-files.json',
            'tools/day_trigger_acceptance/test_day_trigger_acceptance.py'}
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*argv):
    return subprocess.check_output(GIT + list(argv))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

assert git('rev-parse', 'refs/heads/main').decode().strip() == args.parent
entries = {}
for item in git('ls-tree', '-rz', '--full-tree', args.parent).split(b'\0'):
    if item:
        header, name = item.split(b'\t', 1)
        entries[name.decode()] = tuple(header.decode().split())

def fetched(name):
    mode, kind, object_id = entries[name]
    assert mode == '100644' and kind == 'blob', name
    raw = git('cat-file', 'blob', object_id)
    assert oid(raw) == object_id
    return raw

proofs = []
for prefix, expected, count in [
    (PACKAGE, '79d1895420bedcc3a28463f55ba989ecf0c460e72d683787395caad078d7767b', 66),
    (REVIEW, 'c8f60111d0ef63cd88e1bfcb65b9b5cfc919ccc56e9a9bcf7e2799a5a1c5fad0', 11),
]:
    raw = fetched(prefix + '/checkpoint.json')
    assert sha(raw) == expected
    checkpoint = json.loads(raw)
    assert len(checkpoint['files']) == len({row['path'] for row in checkpoint['files']}) == count
    for row in checkpoint['files']:
        data = fetched(prefix + '/' + row['path'])
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
        mode = row.get('mode', 0o644)
        assert (int(mode, 8) & 0o777 if isinstance(mode, str) else mode) == 0o644
    proofs.append(dict(path=prefix + '/checkpoint.json', sha256=expected, payloads=count,
                       all_fetched_payloads_verified=True))
checkpoint = json.loads(fetched(PACKAGE + '/checkpoint.json'))
assert checkpoint['changed_paths'] == sorted(EXPECTED)
assert checkpoint['parent_checkpoint_sha256'] == '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88'
assert sha(fetched(BASELINE + '/checkpoint.json')) == checkpoint['parent_checkpoint_sha256']
assert checkpoint['tooling_tests_passed'] == 155 and checkpoint['full_host_acceptance_executed'] is False
source_rows = [row for row in checkpoint['files'] if row['path'].startswith('source/')]
assert len(source_rows) == 9
manifest, elements, changed, unchanged = [], [], [], []
for row in source_rows:
    name = row['path'].removeprefix('source/')
    source = fetched(PACKAGE + '/' + row['path'])
    old = fetched(BASELINE + '/' + row['path'])
    current = fetched(name)
    assert current == old, name
    local = LOCAL / row['path']
    info = local.lstat()
    assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
    assert local.read_bytes() == source
    binding = dict(path=name, before_sha256=sha(old), candidate_sha256=sha(source),
                   bytes=len(source), mode='100644', baseline_package_path=BASELINE + '/' + row['path'],
                   source_package_path=PACKAGE + '/' + row['path'])
    if name in EXPECTED:
        assert old != source
        elements.append(dict(path=name, mode='100644', type='blob', sha=oid(source)))
        manifest.append(dict(path=name, local_path=str(local), size_bytes=len(source), sha256=sha(source),
                             git_blob_sha1=oid(source), mode='100644'))
        changed.append(binding)
    else:
        assert old == source
        unchanged.append(binding)
assert len(changed) == 3 and len(unchanged) == 6
assert next(row['candidate_sha256'] for row in changed if row['path'].startswith('.github/')) == '11f32372ed4fd7ac078eaa83de407e9867d88b3112bf1bf48f49f5513310f8fc'
assert next(row['candidate_sha256'] for row in changed if row['path'].endswith('/runtime-files.json')) == 'ae4d37a41a1e9c62e57715d6dbd63a481d14d8bd0052666ffccc78c0ecc84fe7'
receipt_raw = args.receipt.read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == args.parent and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
guard = dict(schema=1, status='THREE_REVIEWED_CHECKOUT_LAYOUT_PATHS_READY', parent=args.parent,
             paths=3, checkpoint_proofs=proofs, changed_bindings=changed,
             unchanged_production_bindings=unchanged,
             preserved_failure=dict(run_id=38245093369, archive_sha256='cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833'),
             tooling_tests_measured=155, new_combined_application_acceptance='PENDING_NEW_HOSTED_RUN',
             protected_tree_oids={name: git('rev-parse', args.parent + ':' + name).decode().strip()
                                  for name in ('project', 'artifacts', 'vendor', 'docs', 'work-in-progress')},
             latest_fetched_receipt_sha256=sha(receipt_raw), executed_source_sha256=sha(Path(__file__).read_bytes()),
             active_application_source_or_apk_changed=False, no_workspace_or_index_mutation=True,
             completed_utc=datetime.now(timezone.utc).isoformat())
EXPORT.mkdir(exist_ok=False)
for filename, value in [('manifest.json', manifest), ('tree-elements.json', elements), ('preparation.json', guard)]:
    with (EXPORT / filename).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')
    (EXPORT / filename).chmod(0o644)
print(json.dumps({key: guard[key] for key in ('status', 'parent', 'paths', 'tooling_tests_measured', 'completed_utc')}))
