"""Read-only review of the exact numeric22 proposal; no application execution."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import copy
import difflib
import gzip
import hashlib
import json
import platform
import stat
import subprocess
import sys
import traceback

ROOT = Path('/dev/shm/macrodroid-numeric-promotion-independent-review')
PROPOSAL = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-source-promotion-proposal')
GIT = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
EXPECTED_CHECKPOINT = '0695be31f63f25952d8236d403206a2b292eef4b4e28ab7fd071c045f0401e14'
PARENT = '59df96186fefb2bf883031c09562af08b48bde16'
BASELINE = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
SOURCE_COMMIT = '811f979eda1b937917c18defef38455c49a59062'
PROOF_COMMIT = '48ddc442c61e383c4368606cb31984f15d03bb1f'
SOURCE_PREFIX = 'work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor'
PROOF_PREFIX = 'docs/verification/day-numeric-hosted-run-3d91187'
OUT = ROOT / 'attempt-01'
READS = []

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}

def oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def put(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, indent=2) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o644)

def safe(name):
    p = PurePosixPath(name)
    assert name and not p.is_absolute() and '..' not in p.parts and str(p) == name
    return p

def inventory():
    result = []
    for path in sorted(PROPOSAL.rglob('*')):
        st = path.lstat()
        assert not stat.S_ISLNK(st.st_mode), str(path)
        if stat.S_ISDIR(st.st_mode):
            continue
        assert stat.S_ISREG(st.st_mode), str(path)
        result.append({'path': path.relative_to(PROPOSAL).as_posix(), **identity(path.read_bytes()),
                       'mode': stat.S_IMODE(st.st_mode)})
    return result

def git(*args):
    return subprocess.run(['git', '--git-dir=' + str(GIT), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30).stdout

def tree_row(commit, path):
    safe(path)
    rows = [r for r in git('ls-tree', '-z', commit, '--', path).split(b'\0') if r]
    if not rows:
        return None
    assert len(rows) == 1
    metadata, actual_path = rows[0].split(b'\t', 1)
    mode, kind, blob = metadata.decode().split()
    assert actual_path.decode() == path and kind == 'blob' and mode == '100644'
    return {'mode': mode, 'git_blob_sha1': blob}

def read_git(commit, path):
    row = tree_row(commit, path)
    assert row is not None, (commit, path)
    raw = git('cat-file', 'blob', row['git_blob_sha1'])
    assert oid(raw) == row['git_blob_sha1']
    READS.append({'commit': commit, 'path': path, **row, **identity(raw)})
    return raw

def canonical(entries):
    return sha(json.dumps(entries, sort_keys=True, separators=(',', ':')).encode())

def verify():
    before = inventory()
    put('proposal-before.json', before)
    cp_raw = (PROPOSAL / 'checkpoint.json').read_bytes()
    assert sha(cp_raw) == EXPECTED_CHECKPOINT
    cp = json.loads(cp_raw)
    assert cp['active_files'] == [] and cp['proposed_file_count'] == 22
    assert len({r['path'] for r in cp['files']}) == len(cp['files'])
    assert [r for r in before if r['path'] != 'checkpoint.json'] == sorted(cp['files'], key=lambda r: r['path'])
    put('bound-proposal-checkpoint.json', cp_raw)
    manifest_raw = (PROPOSAL / 'promotion-manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    put('bound-promotion-manifest.json', manifest_raw)
    assert (manifest['reviewed_parent'], manifest['baseline_commit'], manifest['source_overlay_commit'],
            manifest['evidence_commit']) == (PARENT, BASELINE, SOURCE_COMMIT, PROOF_COMMIT)
    parent_tree = git('rev-parse', PARENT + ':project').decode().strip()
    baseline_tree = git('rev-parse', BASELINE + ':project').decode().strip()
    assert parent_tree == baseline_tree == manifest['baseline_project_tree']
    source_raw = read_git(SOURCE_COMMIT, SOURCE_PREFIX + '/checkpoint.json')
    assert source_raw == (PROPOSAL / 'source-checkpoint.json').read_bytes()
    source = json.loads(source_raw)
    assert sha(source_raw) == manifest['source_checkpoint_sha256']
    assert source['active_files'] == [] and len(source['source_changes']) == 19
    rows = manifest['proposed_active_files']
    assert len(rows) == len({r['path'] for r in rows}) == 22
    expected_source_paths = {'project/' + r['path'] for r in source['source_changes']}
    assert {r['path'] for r in rows} == expected_source_paths | {
        'README.md', 'artifacts/current/manifest.json', 'project/reports/release-input-snapshot.json'}
    assert {r['path'].removeprefix('proposed/') for r in cp['files'] if r['path'].startswith('proposed/')} == {r['path'] for r in rows}
    declared_source = {'project/' + r['path']: r for r in source['source_changes']}
    old_pin = read_git(BASELINE, 'project/reports/release-input-snapshot.json')
    assert old_pin == read_git(PARENT, 'project/reports/release-input-snapshot.json')
    base = json.loads(old_pin)
    assert base['files'] == len(base['entries']) == 81291 and canonical(base['entries']) == base['snapshot_sha256']
    reconstructed = copy.deepcopy(base['entries'])
    source_results = []
    old_payloads = {}
    for row in rows:
        name = row['path']
        safe(name)
        raw = (PROPOSAL / 'proposed' / name).read_bytes()
        assert row['mode'] == '100644' and row['candidate'] == identity(raw) and row['candidate_git_blob_sha1'] == oid(raw)
        fetched_row = tree_row(PARENT, name)
        assert row['must_be_absent'] is (row['baseline'] is None)
        if row['baseline'] is None:
            assert fetched_row is None and row['baseline_git_blob_sha1'] is None
            old = None
        else:
            old = read_git(PARENT, name)
            assert row['baseline'] == identity(old) and row['baseline_git_blob_sha1'] == oid(old)
        old_payloads[name] = old
        if name in declared_source:
            s = declared_source[name]
            assert row['source_commit'] == SOURCE_COMMIT and row['source_path'] == SOURCE_PREFIX + '/' + s['source']
            assert raw == read_git(SOURCE_COMMIT, row['source_path'])
            assert row['candidate'] == s['candidate'] and row['baseline'] == s['baseline']
            assert row['must_be_absent'] is s['must_be_absent_if_new']
            rel = name.removeprefix('project/')
            if old is None:
                assert rel not in reconstructed
            else:
                assert reconstructed[rel] == {'size': len(old), 'sha256': sha(old)}
            reconstructed[rel] = {'size': len(raw), 'sha256': sha(raw)}
            source_results.append({'path': name, 'new': old is None, 'bytes': len(raw), 'sha256': sha(raw),
                                   'unchanged_from_executed_numeric_overlay': True})
    assert len(source_results) == 19 and sum(r['new'] for r in source_results) == 7
    new_pin = (PROPOSAL / 'proposed/project/reports/release-input-snapshot.json').read_bytes()
    frozen_gzip = read_git(SOURCE_COMMIT, SOURCE_PREFIX + '/evidence/future-input-snapshot.json.gz')
    assert new_pin == gzip.decompress(frozen_gzip)
    future = json.loads(new_pin)
    assert future['files'] == len(reconstructed) == 81298
    assert future['entries'] == reconstructed
    assert canonical(reconstructed) == future['snapshot_sha256'] == source['future_snapshot']['snapshot_sha256']
    derived = {'format': 1, 'files': len(reconstructed), 'snapshot_sha256': canonical(reconstructed), 'entries': dict(sorted(reconstructed.items()))}
    assert json.dumps(derived, indent=2, ensure_ascii=True).encode() == new_pin
    assert identity(new_pin) == source['future_manifest']
    put('nineteen-source-rows.json', source_results)
    new_map = json.loads((PROPOSAL / 'proposed/project/source/java-method-map.json').read_bytes())
    old_map = json.loads(old_payloads['project/source/java-method-map.json'])
    key = lambda row: (row['target'], row['method'])
    old_by_key = {key(r): r for r in old_map}
    new_by_key = {key(r): r for r in new_map}
    assert len(old_by_key) == len(old_map) == 1242 and len(new_by_key) == len(new_map) == 1243
    assert all(new_by_key[k] == v for k, v in old_by_key.items())
    added = [v for k, v in new_by_key.items() if k not in old_by_key]
    assert len(added) == 1 and added[0]['target'] == 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;'
    assert added[0]['method'] == 'r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'
    assert len({r['target'] for r in new_map}) == 605
    day = [r for r in new_map if r['target'] == added[0]['target']]
    assert len(day) == 2 and {r['method'] for r in day} == {added[0]['method'], 'requiresScheduleExactAlarm()Z'}
    old_ui = json.loads(old_payloads['project/source/ui-methods.json'])
    new_ui = json.loads((PROPOSAL / 'proposed/project/source/ui-methods.json').read_bytes())
    assert len(old_ui) == 10 and len(new_ui) == 11 and [r for r in new_ui if key(r) != key(added[0])] == old_ui
    assert [r for r in new_ui if key(r) == key(added[0])] == added
    put('registry-delta.json', {'registered_before': len(old_map), 'registered_after': len(new_map),
                               'all_previous_rows_unchanged': True, 'added': added,
                               'complete_day_trigger_rows': day, 'ui_methods': len(new_ui)})
    v_raw = read_git(PROOF_COMMIT, PROOF_PREFIX + '/selected/hosted-proof/verification.json')
    review_raw = read_git(PROOF_COMMIT, PROOF_PREFIX + '/analysis/attempt-02/result.json')
    assert v_raw == (PROPOSAL / 'literal-numeric-verification.json').read_bytes()
    assert review_raw == (PROPOSAL / 'independent-numeric-result.json').read_bytes()
    v = json.loads(v_raw)
    reviewed = json.loads(review_raw)
    assert v['passed'] is True and reviewed['passed'] is True
    assert v['status'] == 'ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED'
    assert v['overlay_checkpoint'] == identity(source_raw) and v['source_overlay_commit'] == SOURCE_COMMIT
    assert v['source_snapshot'] == source['future_snapshot'] and v['future_manifest'] == identity(new_pin)
    assert v['actual_acceptance_execution']['returncode'] == 0 and v['actual_acceptance_execution']['timed_out'] is False
    assert (v['gates_verified'], v['fresh_reports_verified'], v['actual_cases'], v['registered_methods'], v['target_classes']) == (16, 23, 194780, 1243, 605)
    assert sum(v['suite_cases'].values()) == 194780 and v['suite_cases']['ui'] == 24465
    assert v['python']['tests'] == v['python']['individual_successes'] == 308
    assert reviewed['tooling_python']['tests'] == reviewed['tooling_python']['individual_successes'] == 92
    assert v['actual_ui_java_controls'] == len(v['all_ui_mutant_checks']) == 91
    assert (v['numeric']['cases'], v['numeric']['paths'], v['numeric']['original_instructions'],
            v['numeric']['rebuilt_instructions'], v['numeric']['conditional_edges_per_path'], v['numeric']['actual_dex_faults']) == (1291, 3, 32, 25, 4, 2)
    assert v['numeric']['signed_positive_instruction_bytes_equal'] is True and v['numeric']['exact_positive_restoration'] is True
    assert v['source_edit_signed_apk_probe_verified'] is True
    assert v['android_runtime_executed'] is False and v['android_probe_status'] == 'BLOCKED'
    new_apk = json.loads((PROPOSAL / 'proposed/artifacts/current/manifest.json').read_bytes())
    old_apk = json.loads(old_payloads['artifacts/current/manifest.json'])
    origin = new_apk['origin']
    assert origin['proof_commit'] == PROOF_COMMIT and origin['run_id'] == 38238858564 and origin['job_id'] == 114776169911
    immutable_raw = read_git(PROOF_COMMIT, origin['immutable_apk_manifest'])
    immutable = json.loads(immutable_raw)
    assert sha(immutable_raw) == origin['immutable_apk_manifest_sha256']
    assert new_apk['parts'] == immutable['parts'] and len(immutable['parts']) == 12
    assert {k: old_apk[k] for k in ('format', 'format_version', 'id', 'filename', 'media_type', 'source_build_filename')} == {k: new_apk[k] for k in ('format', 'format_version', 'id', 'filename', 'media_type', 'source_build_filename')}
    assert new_apk['filename'] == 'MacroDroid-5.67.8-current-hybrid.apk'
    assert {'bytes': new_apk['size_bytes'], 'sha256': new_apk['sha256']} == v['apks']['hybrid'] == reviewed['apks']['hybrid']
    combined = hashlib.sha256()
    total = 0
    part_rows = []
    for number, part in enumerate(new_apk['parts'], 1):
        assert part['path'] == 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/parts/part-%04d.bin' % number
        raw = read_git(PROOF_COMMIT, part['path'])
        assert len(raw) == part['size_bytes'] and sha(raw) == part['sha256'] and oid(raw) == part['git_blob_sha1']
        combined.update(raw)
        total += len(raw)
        part_rows.append({'path': part['path'], **identity(raw), 'git_blob_sha1': oid(raw)})
    assert total == new_apk['size_bytes'] == 94683136
    assert combined.hexdigest() == new_apk['sha256'] == '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
    put('streamed-apk-parts.json', {'parts': part_rows, 'combined': {'bytes': total, 'sha256': combined.hexdigest()}, 'apk_file_written': False})
    review_cp_raw = read_git(PROOF_COMMIT, origin['independent_review_manifest'])
    assert sha(review_cp_raw) == origin['independent_review_manifest_sha256']
    review_cp = json.loads(review_cp_raw)
    assert {k: review_cp['passed_result'][k] for k in ('bytes', 'sha256')} == identity(review_raw)
    zip_manifest = json.loads(read_git(PROOF_COMMIT, origin['complete_ci_artifact_manifest']))
    assert zip_manifest['run_id'] == origin['run_id'] and zip_manifest['source_commit'] == origin['tooling_commit']
    assert {'bytes': zip_manifest['size_bytes'], 'sha256': zip_manifest['sha256']} == reviewed['zip']
    assert zip_manifest['whole_application_1_to_1_established'] is False
    prep = json.loads(read_git(PROOF_COMMIT, PROOF_PREFIX + '/selected/hosted-proof/preparation.json'))
    assert prep['passed'] is True and prep['source_changes_applied'] == 19 and prep['new_files'] == 7
    assert prep['complete_baseline_files_checked'] == 81291 and prep['complete_future_files_checked'] == 81298
    assert prep['future_complete_input_verification'] == source['future_snapshot']
    assert prep['overlay_checkout']['commit'] == SOURCE_COMMIT and prep['baseline_checkout']['commit'] == BASELINE
    assert new_apk['source_input_snapshot'] == {'path': 'project/reports/release-input-snapshot.json', 'files': 81298,
        'canonical_sha256': future['snapshot_sha256'], 'manifest_file_bytes': len(new_pin), 'manifest_file_sha256': sha(new_pin)}
    val = new_apk['validation_at_publication']
    assert (val['registered_methods'], val['original_jvm_rebuilt_cases'], val['ui_cases'], val['python_tests_passed'], val['tooling_host_tests_passed']) == (1243, 194780, 24465, 308, 92)
    assert val['android_executed_for_this_candidate'] is False and new_apk['full_functional_parity_established'] is False
    old_readme = old_payloads['README.md']
    new_readme = (PROPOSAL / 'proposed/README.md').read_bytes()
    assert old_readme == (PROPOSAL / 'before/README.md').read_bytes()
    assert old_payloads['artifacts/current/manifest.json'] == (PROPOSAL / 'before/artifacts-current-manifest.json').read_bytes()
    readme_patch = ''.join(difflib.unified_diff(old_readme.decode().splitlines(True), new_readme.decode().splitlines(True), fromfile='before/README.md', tofile='proposed/README.md')).encode()
    assert readme_patch == (PROPOSAL / 'README.patch').read_bytes()
    manifest_patch = ''.join(difflib.unified_diff(old_payloads['artifacts/current/manifest.json'].decode().splitlines(True), (PROPOSAL / 'proposed/artifacts/current/manifest.json').read_text().splitlines(True), fromfile='before/artifacts/current/manifest.json', tofile='proposed/artifacts/current/manifest.json')).encode()
    assert manifest_patch == (PROPOSAL / 'current-manifest.patch').read_bytes()
    section = lambda raw: raw.split(b'## Latest trigger-navigation observations\n', 1)[1].split(b'## Get the working source\n', 1)[0]
    assert section(old_readme) == section(new_readme)
    assert sha(section(new_readme)) == manifest['readme_checks']['section_sha256']
    assert b'Android behavior for this new `0762aad9' in new_readme and b'APK has not yet been observed.' in new_readme
    assert b'The previous 1,242-body combined source passed all 16 configured acceptance gates:' in new_readme
    for name in ('README.patch', 'current-manifest.patch', 'independent-numeric-result.json'):
        put('reviewed-copies/' + name, (PROPOSAL / name).read_bytes())
    after = inventory()
    put('proposal-after.json', after)
    assert before == after
    return {'passed': True, 'status': 'INDEPENDENT_NUMERIC_22_PROMOTION_IDENTITY_REVIEW_PASS',
            'proposal_checkpoint': identity(cp_raw), 'proposal_payloads_rehashed': len(cp['files']),
            'proposed_active_paths': 22, 'source_paths': 19, 'new_source_paths': 7, 'existing_source_paths': 12,
            'companion_paths': 3, 'fixed_parent_project_tree': parent_tree, 'baseline_entries_checked': 81291,
            'future_entries_derived_and_checked': 81298, 'exact_future_manifest': identity(new_pin),
            'future_canonical_sha256': future['snapshot_sha256'], 'registered_methods': len(new_map),
            'registered_classes': len({r['target'] for r in new_map}), 'all_previous_registry_rows_unchanged': True,
            'existing_day_constant_mapping_unchanged': True, 'lookup_p0_promoted': False,
            'apk_parts_streamed': len(part_rows), 'apk': {'bytes': total, 'sha256': combined.hexdigest()},
            'independent_git_reads': len(READS), 'readme_latest_navigation_section_unchanged': True,
            'readme_historical_android_scope_preserved': True, 'proposal_inputs_unchanged': True,
            'blockers': [], 'approval_scope': 'Exact 22-path proposal only, subject to publisher rechecking all before/absence states at its coherent promotion.',
            'new_application_gate_executions': 0, 'android_executed_by_review': False, 'git_writes': False,
            'full_runtime_1_to_1_established': False, 'apk_materialized_by_review': False,
            'review_scope': 'Fresh hashes/immutable Git reads/complete source-entry derivation/streamed part identity and narrow documentation review; closed successful host results inspected, not rerun.'}

if __name__ == '__main__':
    OUT.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    result = {'passed': False, 'started_utc': started}
    put('executed-review.py', Path(__file__).read_bytes())
    runtime = Path(sys.executable).resolve()
    put('runtime.json', {'executable': str(runtime), **identity(runtime.read_bytes()), 'python_version': sys.version,
                         'platform': platform.platform(), 'argv': sys.argv, 'bytecode_writes_disabled': bool(sys.dont_write_bytecode)})
    try:
        result.update(verify())
    except BaseException as exc:
        result.update({'error_type': type(exc).__name__, 'error': str(exc)})
        put('traceback.txt', traceback.format_exc().encode())
    finally:
        put('immutable-git-reads.json', READS)
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        put('result.json', result)
        print(json.dumps(result, indent=2))
    sys.exit(0 if result['passed'] else 1)
