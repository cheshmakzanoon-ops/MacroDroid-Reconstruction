"""Prepare exactly the approved 22 numeric promotion paths from fetched Git."""
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
PACKAGE = 'work-in-progress/day-trigger-numeric/11-source-promotion-proposal'
REVIEW = 'docs/verification/day-trigger-numeric/11-source-promotion-independent-review'
LOCAL = ROOT / 'numeric-source-promotion-proposal'
EXPORT = ROOT / 'numeric-source-promotion-activation-export'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*argv):
    return subprocess.check_output(GIT + list(argv))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

assert git('rev-parse', 'refs/heads/main').decode().strip() == args.parent
entries = {}
for line in git('ls-tree', '-rz', '--full-tree', args.parent).split(b'\0'):
    if line:
        header, name = line.split(b'\t', 1)
        entries[name.decode()] = tuple(header.decode().split())

def fetched(name):
    mode, kind, object_id = entries[name]
    assert mode == '100644' and kind == 'blob', name
    raw = git('cat-file', 'blob', object_id)
    assert oid(raw) == object_id
    return raw

checkpoints = []
for prefix, expected, count in [
    (PACKAGE, '0695be31f63f25952d8236d403206a2b292eef4b4e28ab7fd071c045f0401e14', 34),
    (REVIEW, '171694b92732192f2a509c0e8da0a509289522303c12934563f078901e88b409', 25),
]:
    raw = fetched(prefix + '/checkpoint.json')
    assert sha(raw) == expected
    checkpoint = json.loads(raw)
    assert len(checkpoint['files']) == len({row['path'] for row in checkpoint['files']}) == count
    for row in checkpoint['files']:
        content = fetched(prefix + '/' + row['path'])
        assert len(content) == row['bytes'] and sha(content) == row['sha256']
        mode = row.get('mode', 0o644)
        assert (int(mode, 8) & 0o777 if isinstance(mode, str) else mode) == 0o644
    checkpoints.append(dict(path=prefix + '/checkpoint.json', sha256=expected, payloads=count,
                            all_fetched_bytes_and_modes_verified=True))

proposal = json.loads(fetched(PACKAGE + '/promotion-manifest.json'))
rows = proposal['proposed_active_files']
assert len(rows) == len({row['path'] for row in rows}) == 22
assert len([row for row in rows if row['must_be_absent'] is True]) == 7
assert len([row for row in rows if row['must_be_absent'] is False]) == 15
assert {row['path'] for row in rows if not row['path'].startswith('project/')} == {'README.md', 'artifacts/current/manifest.json'}
assert git('rev-parse', args.parent + ':project').decode().strip() == proposal['baseline_project_tree'] == 'ad5c834ef56e039bafdcf7c2e9a52cfb8c3ce3a5'
manifest, elements, bindings = [], [], []
for row in rows:
    name = row['path']
    assert row['mode'] == '100644'
    before = entries.get(name)
    if row['must_be_absent']:
        assert before is None and row['baseline'] is None and row['baseline_git_blob_sha1'] is None
    else:
        assert before == ('100644', 'blob', row['baseline_git_blob_sha1']), name
        old = fetched(name)
        assert len(old) == row['baseline']['bytes'] and sha(old) == row['baseline']['sha256']
    source_name = PACKAGE + '/proposed/' + name
    raw = fetched(source_name)
    assert len(raw) == row['candidate']['bytes'] and sha(raw) == row['candidate']['sha256']
    assert oid(raw) == row['candidate_git_blob_sha1']
    if row.get('source_commit'):
        assert git('show', row['source_commit'] + ':' + row['source_path']) == raw
    local = LOCAL / 'proposed' / name
    info = local.lstat()
    assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
    assert local.read_bytes() == raw
    assert before is None or before[2] != oid(raw)
    elements.append(dict(path=name, mode='100644', type='blob', sha=oid(raw)))
    manifest.append(dict(path=name, local_path=str(local), size_bytes=len(raw), sha256=sha(raw),
                         git_blob_sha1=oid(raw), mode='100644'))
    bindings.append(dict(path=name, before=row['baseline'], required_absent=row['must_be_absent'],
                         candidate=row['candidate'], mode='100644', fetched_proposal_path=source_name))

current = json.loads(fetched(PACKAGE + '/proposed/artifacts/current/manifest.json'))
assert current['filename'] == 'MacroDroid-5.67.8-current-hybrid.apk'
assert current['size_bytes'] == 94683136 and current['sha256'] == '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
assert len(current['parts']) == len({part['path'] for part in current['parts']}) == 12
combined, total = hashlib.sha256(), 0
for part in current['parts']:
    raw = fetched(part['path'])
    assert len(raw) == part['size_bytes'] and sha(raw) == part['sha256']
    assert oid(raw) == part['git_blob_sha1']
    combined.update(raw)
    total += len(raw)
assert total == current['size_bytes'] and combined.hexdigest() == current['sha256']
receipt_raw = args.receipt.read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == args.parent and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
guard = dict(schema=1, status='EXACT_22_PATH_NUMERIC_PROMOTION_READY', parent=args.parent,
             paths=22, active_source_paths=19, companion_paths=3, absence_guards=7, existing_guards=15,
             checkpoint_proofs=checkpoints, path_bindings=bindings,
             exact_active_baseline_project_tree=proposal['baseline_project_tree'],
             input_derivation=proposal['input_derivation'], candidate_apk_bytes=total,
             candidate_apk_sha256=combined.hexdigest(), all_12_fetched_parts_verified=True,
             android_result_for_this_candidate='NOT_YET_OBSERVED',
             latest_fetched_receipt_sha256=sha(receipt_raw),
             protected_tree_oids={name: git('rev-parse', args.parent + ':' + name).decode().strip()
                                  for name in ('.github', 'tools', 'vendor', 'docs', 'work-in-progress')},
             no_workspace_or_index_mutation=True, no_new_build_or_android_execution=True,
             executed_source_sha256=sha(Path(__file__).read_bytes()),
             completed_utc=datetime.now(timezone.utc).isoformat())
EXPORT.mkdir(exist_ok=False)
for filename, data in [('manifest.json', manifest), ('tree-elements.json', elements), ('preparation.json', guard)]:
    with (EXPORT / filename).open('x') as stream:
        stream.write(json.dumps(data, indent=2) + '\n')
    (EXPORT / filename).chmod(0o644)
print(json.dumps({key: guard[key] for key in ('status', 'parent', 'paths', 'absence_guards', 'existing_guards', 'candidate_apk_bytes', 'candidate_apk_sha256', 'completed_utc')}))
