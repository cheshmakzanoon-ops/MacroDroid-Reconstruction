#!/usr/bin/env python3
"""Preserve every owned validation file without duplicating published APKs."""
from pathlib import Path
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
import shutil
import stat

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'checkpoints/01-multipart-workflow-and-offline-validation'
COMMIT = 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'
GUARD = 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls'
OWN = ['prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py',
       '.github/workflows/editor-exact-alarm-enable-return.yml']
MAX_PAYLOAD = 8 * 1024 * 1024


def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': info.st_size, 'sha256': digest}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


outer = json.loads((ROOT / 'reports/validation-01/result.json').read_bytes())
inner = json.loads((ROOT / 'reports/validation-01/validation/result.json').read_bytes())
assert outer['status'] == 'PASSED' and outer['exit_code'] == 0 and outer['timed_out'] is False
assert outer['all_immutable_input_bytes_and_modes_unchanged'] is True and outer['input_count'] == 402
assert inner['status'] == 'OFFLINE_EXACT_ALARM_ENABLE_RETURN_WORKFLOW_VALIDATED'
assert inner['passed'] is True and inner['android_executed'] is False
assert len(inner['commands']) == 74 and inner['prepared_input_copies'] == 317
assert inner['source_host_controls_reused']['distinct_tests'] == 259
assert inner['source_host_controls_reused']['locally_reexecuted'] is False
assert inner['multipart_preparation']['verified']['verified_members'] == 353
assert inner['helpers_before'] == inner['helpers_after']
for name in OWN:
    assert identity(ROOT / 'source-02' / name) == inner['helpers_before'][name]
assert identity(Path('/dev/shm/macrodroid-exact-alarm-enable-return/derive_workflow.py'))['sha256'] == '5a9cc48ddcc2f2fa32f72accc35240d81b20f6a0b307961a133da0f2f40233d3'

# The final four executable payloads are directly reviewable. Source/host
# archives remain at their already fetched commits and retain exact identities.
DEST.mkdir(parents=True, exist_ok=False)
for name in OWN:
    target = DEST / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'source-02' / name, target)
for name in ['derivation.json', 'derivation.patch']:
    shutil.copy2(ROOT / 'source-02' / name, DEST / name)

external = {}
checkout = json.loads((ROOT / 'reports/checkout-01/result.json').read_bytes())
assert checkout['file_count'] == 209 and checkout['logical_archive_absent'] is True
for row in checkout['files']:
    key = (row['bytes'], row['sha256'])
    external.setdefault(key, {'kind': 'git_blob', 'commit': COMMIT, 'path': row['path'],
                             'git_blob_sha1': row['git_blob_sha1']})
external[(13014001, '51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755')] = {
    'kind': 'multipart_manifest', 'commit': COMMIT,
    'path': GUARD + '/archive-layout/manifest.json',
    'manifest_bytes': 1549, 'manifest_sha256': '8be9e7dab79ccad82db4b98e33e8418044a372a456e45907bcec0f134bce6310'}
external[(95725918, '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800')] = {
    'kind': 'multipart_manifest', 'commit': COMMIT, 'path': 'vendor/original/manifest.json',
    'manifest_sha256': 'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684'}
external[(94683136, '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd')] = {
    'kind': 'multipart_manifest', 'commit': '48ddc442c61e383c4368606cb31984f15d03bb1f',
    'path': 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json',
    'manifest_bytes': 5189, 'manifest_sha256': 'e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152'}
capsule_contents = {(identity(DEST / name)['bytes'], identity(DEST / name)['sha256']): name for name in OWN}

paths = []
for relative in ['inputs', 'derived-01', 'source-02', 'reports']:
    paths.extend(path for path in (ROOT / relative).rglob('*') if path.is_file() or path.is_symlink())
paths.extend(path for path in ROOT.iterdir() if path.is_file())
paths = sorted(set(paths))
seen_inode = {}
records = []
retained = {}
external_uses = 0
raw_total = 0
symlinks = []


def readable_copy(relative):
    parts = Path(relative).parts
    if parts[0] in ('derived-01', 'source-02'):
        return True
    if parts[0] == 'inputs' and len(parts) == 2:
        return True
    if parts[0] != 'reports':
        return len(parts) == 1
    excluded = {'private-inputs', 'input-faults', 'inventory-faults',
                'matching-existing-logical', 'cleanup-controls'}
    if not any(part in excluded for part in parts):
        return True
    return parts[-1] in {'input-preflight.json', 'materialized-inputs.json',
        'exact-alarm-enable-return-verification.json', 'runtime-cleanup.json',
        'download-tests.log', 'animation-host-tests.log'}


for path in paths:
    relative = path.relative_to(ROOT).as_posix()
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        target = os.readlink(path)
        records.append({'path': relative, 'kind': 'inert_symlink', 'target': target})
        symlinks.append({'path': relative, 'target': target})
        continue
    assert stat.S_ISREG(info.st_mode), relative
    cache_key = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
    if cache_key not in seen_inode:
        seen_inode[cache_key] = identity(path)
    actual = seen_inode[cache_key]
    key = (actual['bytes'], actual['sha256'])
    raw_total += actual['bytes']
    if readable_copy(relative):
        target_name = 'review/' + relative
        target = DEST / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        assert actual['bytes'] <= MAX_PAYLOAD, relative
        shutil.copy2(path, target)
        assert identity(target) == actual
        capsule_contents.setdefault(key, target_name)
    if key in capsule_contents:
        content = {'kind': 'capsule_file', 'path': capsule_contents[key]}
    elif key in external:
        content = dict(external[key])
        external_uses += 1
    else:
        target_name = 'objects/' + actual['sha256']
        target = DEST / target_name
        if key not in retained:
            assert actual['bytes'] <= MAX_PAYLOAD, relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with path.open('rb') as source, target.open('xb') as stream:
                shutil.copyfileobj(source, stream, 1024 * 1024)
            assert identity(target) == actual
            retained[key] = target_name
        content = {'kind': 'capsule_file', 'path': retained[key]}
    records.append({'path': relative, 'kind': 'regular', **actual,
        'mode': stat.S_IMODE(info.st_mode),
        'closure_stat': {'device': info.st_dev, 'inode': info.st_ino,
            'links': info.st_nlink, 'mtime_ns': info.st_mtime_ns, 'ctime_ns': info.st_ctime_ns},
        'content': content})

index = {'schema': 1,
    'scope': 'Complete closed owned file inventory, with literal symlinks encoded inertly and exact already-published duplicate bytes referenced by immutable Git or multipart identities.',
    'original_owned_root': str(ROOT), 'regular_paths': len(records) - len(symlinks),
    'symlink_paths': len(symlinks), 'logical_regular_bytes': raw_total,
    'inode_metadata_scope': 'Observed at evidence closure only; these values are not reconstructed-file metadata or substituted for serialized command-time observations.',
    'files': records}
raw = (json.dumps(index, indent=2) + '\n').encode()
compressed = gzip.compress(raw, compresslevel=9, mtime=0)
(DEST / 'complete-evidence-index.json.gz').write_bytes(compressed)
assert len(compressed) <= MAX_PAYLOAD
save(DEST / 'complete-evidence-index.json.metadata', {
    'compressed': identity(DEST / 'complete-evidence-index.json.gz'),
    'uncompressed': {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()},
    'files': len(records), 'regular_paths': index['regular_paths'], 'inert_symlinks': symlinks,
    'logical_regular_bytes': raw_total, 'external_reference_uses': external_uses,
    'unique_novel_content_objects': len(retained),
    'all_novel_bytes_retained': True, 'apks_recopied_into_capsule': False})

save(DEST / 'closed-validation-summary.json', {
    'status': inner['status'], 'passed': True, 'commands': 74,
    'started_utc': inner['started_utc'], 'finished_utc': inner['finished_utc'],
    'outer_seconds': (outer['finished_monotonic_ns'] - outer['started_monotonic_ns']) / 1e9,
    'timeout_seconds': 900, 'timed_out': False,
    'literal_sparse_checkout': {'commit': COMMIT, 'files': 209, 'bytes': 27190225,
                                'logical_archive_initially_absent': True},
    'prepared_copy_roles': 317, 'complete_guard_payloads': 181, 'guard_source_files': 102,
    'archived_members': 353, 'input_faults': 16, 'multipart_faults': 7,
    'matching_existing_archive_positive': True,
    'inventory_and_contract_mutations': 21, 'entry_points_per_inventory_mutation': 2,
    'workflow_policy_mutations': 10, 'downloader_tests': 6, 'zero_animation_tests': 10,
    'closed_source_tests_reused': 259, 'fresh_259_source_suite_locally_executed': False,
    'hosted_full_source_suite_retained': True,
    'owned_cleanup_expected_exit_codes': [0, 7, 1],
    'protected_input_files': 402, 'protected_bytes_and_modes_unchanged': True,
    'apks_transported_as_verified_read_only_hardlinks': True,
    'application_build_executed': False, 'android_executed': False,
    'full_runtime_1_to_1_established': False})
save(DEST / 'proposed-source-files.json', [
    {'source': name, 'target': name if name.startswith('.github/') else
        'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/' + name,
     **identity(DEST / name), 'mode': '100644'} for name in OWN])
save(DEST / 'input-bindings.json', {
    'source_checkpoint': {'commit': COMMIT, 'path': GUARD + '/checkpoint.json',
        'bytes': 39880, 'sha256': '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051'},
    'archive_layout': {'commit': COMMIT, 'path': GUARD + '/archive-layout/manifest.json',
        'bytes': 1549, 'sha256': '8be9e7dab79ccad82db4b98e33e8418044a372a456e45907bcec0f134bce6310'},
    'parent_workflow_checkpoint_sha256': '805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066',
    'unchanged_generator_sha256': '5a9cc48ddcc2f2fa32f72accc35240d81b20f6a0b307961a133da0f2f40233d3',
    'prior_unexecuted_draft_checkpoint_sha256': '0a44bf777d28ae560e227a8d16c77c65e92d5c167158e6d8d0ec5921b440839d',
    'independent_source_review_sha256': 'd49cf08ea042abb8a05e05f724906bf1b4e6fa4371b016346fce4ad326859257',
    'candidate_manifest': external[(94683136, '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd')],
    'plan_sha256': 'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211',
    'settings_contract_sha256': '379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07',
    'report_schema': 7, 'screens_per_run': 16, 'inputs_per_run': 15,
    'settings_inputs_total': 4, 'permission_api_result_observed': False})
(DEST / 'README.md').write_text('''# Settings enable and return: exact multipart workflow and offline proof

This inactive package contains the three workflow helpers and complete sixteen-screen workflow for the already reviewed Settings source. The application inputs are the exact original 84333011… APK and the accepted numeric 0762aad9… APK. No application source, APK, build, Android device, or active workflow was changed during this preparation.

The unchanged root generator (5a9cc48d…) was copied and executed once against the exact source03 checkpoint (6a4ea8e…), its independent review (d49cf08e…), parent workflow (805c4574…), and exact candidate manifest. Its generated four files and complete successful derivation receipt remain under `review/derived-01/` and `review/reports/derive-01/`. The older unexecuted authoring draft (0a44bf77…) is retained as a separate input. `derivation.patch` shows the subsequent narrow multipart preparation and host-validation changes. The final comparison helper is byte-identical to the unchanged generator output.

## Executable preparation contract

The source evidence is published as two parts, with manifest 8be9e7da… at commit fc825ede…. The preparer checks the original source checkpoint, exact manifest, ordered part identities, sizes and modes on every entry. Both parts must match even if the logical archive already exists. A wrong existing archive is rejected and is never overwritten.

When the logical archive is absent, the preparer writes only its own exclusive temporary output, rechecks each part and the exact concatenation, sets mode 0644 and creates the missing logical path without replacing an existing file. It retains preparation observations in the ordinary preflight report. The exact 13,014,001-byte archive (51749196…) and all 353 regular members are verified against the pinned member inventory. Only then does preparation validate and copy all 181 original capsule payloads, including the unchanged 102 source files. Partial failures retain their raw reports and any owned temporary output.

The final verifier still requires schema 7, the exact sixteen-screen plan and Settings contract, two complete fixed-APK runs, fifteen inputs per run, four Settings inputs in total, complete command/capture ownership and chronology, and all full-frame pixel/XML comparisons. The workflow retains the full 259-test source suite on the hosted runner. It makes no permission-API-result or unrestricted 1:1 claim.

## Actual offline results

The validation began at 2026-10-12T12:24:36.583113+00:00 and finished at 12:28:35.861296+00:00. All **74 bounded commands passed their expected outcomes**, including deliberate nonzero rejection and cleanup statuses. The wrapper completed within its 900-second bound. Complete raw command streams, argv, status reports, source copies and input inventories are retained.

The actual sparse checkout read 209 exact blobs from fetched commit fc825ede… and omitted the uncommitted logical archive. Literal workflow preparation assembled it, verified all 353 archive members and 181 payloads, and produced **317 independently enumerated copy roles**. A second complete preparation accepted a matching existing archive while checking both parts again.

Sixteen input faults were rejected. Seven specifically exercise missing first/second parts, a same-size altered first part, a truncated second part, a changed manifest, a symlinked part and a wrong existing logical archive. Each of these stopped before any source copy. Twenty-one inventory/schema/policy/Settings-contract mutations were rejected at both materialized and final boundaries, including the missing and changed Settings contract pins. Ten separate policy-format mutations were rejected with exact positive restoration.

The actual fixed APKs and AAPT2 were inspected through read-only hardlinks to already verified tmpfs inputs; no additional APK copy was made. Six downloader tests and ten zero-animation helper tests passed. The already closed 259 source tests were reused locally through their exact capsule binding, and were not rerun. Three simulated owned-service controls retained success, a journey exit of 7, and a service failure mapped to exit 1. No real Android command was executed. All 402 recorded immutable inputs retained their bytes and modes before and after the attempt.

## Complete evidence without duplicate application payloads

`complete-evidence-index.json.gz` is the lossless inventory of every owned file in the derivation, literal checkout and validation trees. Its companion metadata pins both compressed and decompressed bytes. Novel files are retained directly under `review/` or as exact SHA-addressed objects. The numerous unchanged copies and hardlinks refer to immutable fetched Git blobs, or to the already published original/candidate/source-archive multipart manifests with exact bytes and hashes. This retains the complete 7+ GB logical case inventory without uploading duplicate applications. The two deliberate symlinks are recorded as inert link targets rather than created as active links in this capsule.

The recorded inode/ctime data is explicitly a closure observation. Reconstructed copies do not claim those live filesystem values. `verify_frozen_evidence.py` checks the exact content bindings and all locally retained novel bytes without executing application or Android code. `proposed-source-files.json` lists the final four proposed executable paths; this checkpoint remains inactive until independent review and separate activation.
''')
# Copy the independent, non-executing index verifier written alongside this freezer.
shutil.copy2(ROOT / 'verify_frozen_evidence.py', DEST / 'verify_frozen_evidence.py')
for name in OWN:
    assert identity(ROOT / 'source-02' / name) == inner['helpers_before'][name]
files = []
for path in sorted(DEST.rglob('*')):
    assert not path.is_symlink(), str(path)
    if path.is_file():
        row = {'path': path.relative_to(DEST).as_posix(), **identity(path),
               'mode': '100755' if path.stat().st_mode & 0o111 else '100644'}
        assert row['bytes'] <= MAX_PAYLOAD, row
        files.append(row)
save(DEST / 'checkpoint.json', {
    'schema': 1, 'status': 'INACTIVE_SETTINGS_MULTIPART_WORKFLOW_OFFLINE_VALIDATED',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'repo_target': 'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen',
    'active_files': [], 'workflow_generated': True, 'workflow_offline_validated': True,
    'executable_payloads': 4, 'offline_commands': 74, 'complete_input_copy_roles': 317,
    'complete_source_payloads': 181, 'archive_members': 353,
    'closed_source_tests_reused': 259, 'local_additional_helper_tests_passed': 16,
    'protected_input_files_unchanged': 402,
    'android_executed': False, 'application_build_executed': False,
    'full_runtime_1_to_1_established': False,
    'indexed_owned_paths': len(records), 'indexed_logical_regular_bytes': raw_total,
    'frozen_payload_count': len(files), 'frozen_payload_bytes': sum(row['bytes'] for row in files),
    'files': files})
print(json.dumps({'path': str(DEST / 'checkpoint.json'), **identity(DEST / 'checkpoint.json'),
    'payload_count': len(files), 'payload_bytes': sum(row['bytes'] for row in files),
    'indexed_paths': len(records), 'logical_bytes': raw_total}, indent=2))
