#!/usr/bin/env python3
"""Read-only independent audit of the frozen workflow and actual offline proof."""
from __future__ import annotations

from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
import time

from recheck_prepared_inputs import SOURCE_ROWS, WORKFLOW, SUITE, identity, source_inputs

CAPSULE = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/02-thirteen-screen-readiness-workflow')
PARENT = Path('/workspace/scratch/4130730d15aa/day-time-trigger-forward/checkpoints/03-zero-scale-thirteen-screen-workflow')
GUARD = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard')
OUTPUT = Path(__file__).resolve().parent / 'reports/frozen-workflow-audit'
CHECKPOINT_SHA256 = '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'
OFFLINE_SHA256 = 'e7f4ece8436cc55c020a6cea94d57de15aaa7dbfff645586e3b3933d020092df'
EXTERNAL_BYTES = {
    '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800': 95725918,
    '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182': 94683119,
    '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745': 6135688,
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def safe_relative(value):
    need(type(value) is str and bool(value), 'Invalid evidence path')
    path = PurePosixPath(value)
    need(not path.is_absolute() and '..' not in path.parts and '\\' not in value
         and path.as_posix() == value, 'Unconfined evidence path: ' + value)
    return value


def metadata(path):
    value = path.lstat()
    return (value.st_dev, value.st_ino, value.st_size, value.st_mode,
            value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = {'status': 'INDEPENDENT_FROZEN_WORKFLOW_AUDIT_RUNNING', 'passed': False,
              'android_executed': False, 'host_suites_rerun': False,
              'parent_results_inspected_not_reexecuted': True,
              'started_utc': datetime.now(timezone.utc).isoformat()}
    try:
        before_sources = source_inputs()
        checkpoint = CAPSULE / 'checkpoint.json'
        need(identity(checkpoint)['sha256'] == CHECKPOINT_SHA256, 'Frozen checkpoint changed')
        frozen = json.loads(checkpoint.read_bytes())
        need(frozen['status'] == 'DAY_TIME_READINESS_WORKFLOW_OFFLINE_CONTROLS_PASSED_REVIEW_PENDING'
             and frozen['android_executed'] is False and frozen['active_changes'] is False,
             'Frozen scope differs')
        need(len(frozen['files']) == 13 and len({row['path'] for row in frozen['files']}) == 13,
             'Frozen source membership differs')
        for row in frozen['files']:
            path = CAPSULE / safe_relative(row['path'])
            need(not path.is_symlink() and identity(path) == {k: row[k] for k in ('bytes', 'sha256')},
                 'Frozen file changed: ' + row['path'])
        for row in SOURCE_ROWS:
            need(identity(CAPSULE / row['path']) == {k: row[k] for k in ('bytes', 'sha256')},
                 'Freeze differs from independently reviewed source: ' + row['path'])
        bindings = json.loads((CAPSULE / 'parent-source-identities.json').read_bytes())
        need(identity(PARENT / 'checkpoint.json')['sha256'] == bindings['parent_checkpoint_sha256'],
             'Parent checkpoint changed')
        need(identity(GUARD / 'checkpoint.json') == bindings['guard_checkpoint'], 'Guard checkpoint changed')
        independently_rebuilt_patch = ''
        parent_guard_files = 0
        for capsule in (PARENT, GUARD):
            for row in json.loads((capsule / 'checkpoint.json').read_bytes())['files']:
                need(identity(capsule / row['path']) == {k: row[k] for k in ('bytes', 'sha256')},
                     'A frozen derivation dependency changed')
                parent_guard_files += 1
        for row in bindings['changes']:
            old, new = PARENT / row['parent_path'], CAPSULE / row['path']
            need(identity(old) == row['before'] and identity(new) == row['after'], 'Derivation source identity differs')
            independently_rebuilt_patch += ''.join(difflib.unified_diff(
                old.read_text().splitlines(True), new.read_text().splitlines(True),
                fromfile='parent-thirteen-screen/' + row['parent_path'],
                tofile='readiness-thirteen-screen/' + row['path']))
        need(independently_rebuilt_patch == (CAPSULE / 'derivation.patch').read_text(),
             'The exact derivation patch does not describe the frozen source')
        manifest_path = CAPSULE / 'offline-evidence-manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        entries, links = manifest['files'], manifest['inert_symlink_controls']
        need(manifest['schema'] == 2 and manifest['android_executed'] is False
             and len(entries) == manifest['file_count'] == frozen['evidence_files'] == 8641,
             'Frozen evidence count or scope differs')
        external = manifest['exact_already_published_runtime_inputs']
        need(set(external) == set(EXTERNAL_BYTES), 'Unexpected external runtime payload')
        for digest, row in external.items():
            need(row['sha256'] == digest and row['bytes'] == EXTERNAL_BYTES[digest]
                 and identity(Path(row['source'])) == {'bytes': row['bytes'], 'sha256': digest},
                 'External runtime bytes changed')
            need(row['durable_repository'] == 'https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction.git'
                 and re.fullmatch('[0-9a-f]{40}', row['durable_commit']) is not None,
                 'Malformed durable runtime reference')
        expected_payloads = {}
        all_paths, snapshots, physical_hashes = set(), {}, {}
        external_roles = 0
        for row in entries:
            name = safe_relative(row['path'])
            need(name not in all_paths, 'Duplicate evidence role')
            all_paths.add(name)
            expected_keys = {'path', 'bytes', 'sha256', 'mode'}
            extra = 'external_input_sha256' if 'external_input_sha256' in row else 'archive_member'
            need(set(row) == expected_keys | {extra}, 'Unexpected evidence fields')
            path = SUITE / name
            facts = metadata(path)
            need(stat.S_ISREG(facts[3]) and facts[3] & 0o777 == row['mode'], 'Nonregular or changed evidence mode')
            if facts not in physical_hashes:
                physical_hashes[facts] = identity(path)
                need(metadata(path) == facts, 'Evidence changed while reading')
            need(physical_hashes[facts] == {k: row[k] for k in ('bytes', 'sha256')}, 'Raw evidence payload differs: ' + name)
            snapshots[name] = facts
            if extra == 'external_input_sha256':
                need(row[extra] == row['sha256'] and row['sha256'] in external
                     and row['bytes'] == EXTERNAL_BYTES[row['sha256']], 'External role binding differs')
                external_roles += 1
            else:
                need(row[extra] == 'blobs/sha256/' + row['sha256'] + '.bin', 'Payload name is not content-bound')
                expected = {'bytes': row['bytes'], 'sha256': row['sha256']}
                need(expected_payloads.setdefault(row[extra], expected) == expected, 'Conflicting payload identity')
        for row in links:
            name = safe_relative(row['path'])
            need(set(row) == {'path', 'target', 'restored_as_symlink'} and row['restored_as_symlink'] is False,
                 'Symlink control is not explicitly inert')
            need(name not in all_paths, 'Duplicate symlink evidence role')
            all_paths.add(name)
            path = SUITE / name
            need(path.is_symlink() and str(path.readlink()) == row['target'], 'Inert symlink control differs')
            snapshots[name] = metadata(path)
        observed = {path.relative_to(SUITE).as_posix() for path in SUITE.rglob('*')
                    if path.is_file() or path.is_symlink()}
        need(observed == all_paths, 'The complete closed raw inventory differs')
        archive = CAPSULE / 'offline-evidence-blobs.tar.gz'
        archived = {}
        with tarfile.open(archive, 'r:gz') as stream:
            for member in stream:
                need(member.isfile() and not member.linkname and member.name in expected_payloads
                     and member.name not in archived and member.mode == 0o644 and member.mtime == 0,
                     'Unexpected archived payload or metadata')
                data = stream.extractfile(member).read()
                actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                need(actual == expected_payloads[member.name] and member.size == len(data), 'Archived payload differs')
                archived[member.name] = actual
        need(archived == expected_payloads and len(archived) == 276 == manifest['unique_archived_payloads'],
             'Archive membership differs')
        result_path = SUITE / 'result.json'
        need(identity(result_path)['sha256'] == OFFLINE_SHA256
             and (CAPSULE / 'offline-validation.json').read_bytes() == result_path.read_bytes(),
             'The frozen and actual offline results differ')
        result = json.loads(result_path.read_bytes())
        need(result == frozen['offline_validation'] and result['passed'] is True
             and result['status'] == 'OFFLINE_DAY_TIME_READINESS_WORKFLOW_VALIDATED'
             and result['android_executed'] is False and result['prepared_input_copies'] == 252,
             'Actual offline validation scope differs')
        expected_commands = [(f'bash-syntax-{index:02}', 0) for index in range(1, 7)]
        expected_commands += [('exact-frozen-preflight', 0)]
        expected_commands += [(label, 1) for label in [
            'changed-original-manifest', 'changed-active-manifest', 'changed-chronology-guard',
            'changed-animation-helper', 'changed-readiness-guard', 'symlinked-runtime-input',
            'changed-reviewed-finalizer', 'existing-output']]
        expected_commands += [('exact-offline-apk-preflight', 0)]
        for label in [
                'omit-runtime-row', 'empty-inventory', 'duplicate-row', 'reorder-rows', 'extra-row',
                'changed-source-and-copy-retained', 'changed-source-and-copy-omitted',
                'changed-source-and-copy-empty', 'changed-source-and-copy-rehashed',
                'changed-copy-retained', 'changed-copy-rehashed', 'omit-reviewed-copy-role',
                'legacy-readiness-schema', 'boolean-readiness-schema',
                'missing-readiness-policy-pin', 'changed-readiness-policy-pin']:
            expected_commands += [('inventory-' + label + '-materialized', 1),
                                  ('inventory-' + label + '-final', 2)]
        expected_commands += [('workflow-policy-controls', 0)]
        expected_commands += [('packaged-host-controls-' + str(index), 0) for index in range(3)]
        expected_commands += [('owned-cleanup-clean', 0), ('owned-cleanup-failed-journey', 7),
                              ('owned-cleanup-failed-service', 1)]
        need(len(expected_commands) == 55 and [(r['label'], r['exit_code']) for r in result['commands']] == expected_commands,
             'Actual command order or intended exit status differs')
        for row in result['commands']:
            need(row['timed_out'] is False and row['android_executed'] is False
                 and json.loads((SUITE / 'commands' / row['label'] / 'command.json').read_bytes()) == row,
                 'Per-command record differs')
        host_tests = []
        for index, (expected_count, log_name) in enumerate([(6, 'download-tests.log'), (166, 'journey-host-tests.log'), (10, 'animation-host-tests.log')]):
            output = (SUITE / 'commands' / ('packaged-host-controls-' + str(index)) / 'stdout.txt').read_bytes()
            matches = re.findall(rb'^Ran ([0-9]+) tests in ([0-9.]+)s$', output, re.MULTILINE)
            need(len(matches) == 1 and int(matches[0][0]) == expected_count and output.rstrip().endswith(b'OK'),
                 'Actual host test count or outcome differs')
            need(output == (SUITE / 'private-inputs/ci-day-time-readiness' / log_name).read_bytes(), 'Copied host log differs')
            host_tests.append({'label': log_name, 'tests': expected_count,
                               'unittest_reported_seconds': float(matches[0][1]), 'passed': True,
                               'inspection_only': True})
        policy = json.loads((SUITE / 'workflow-policy-controls.json').read_bytes())
        need(policy['passed'] is True and policy['positive_and_restore'] is True and policy['android_executed'] is False
             and [r['label'] for r in policy['negative_controls']] == ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-policy', 'changed-policy']
             and all(r['rejected'] is True for r in policy['negative_controls']), 'Actual policy-format controls differ')
        for name, facts in snapshots.items():
            need(metadata(SUITE / name) == facts, 'A closed raw role changed during the independent audit')
        need(source_inputs() == before_sources and identity(checkpoint)['sha256'] == CHECKPOINT_SHA256,
             'Reviewed source changed during the independent audit')
        report.update(status='INDEPENDENT_FROZEN_READINESS_WORKFLOW_AUDIT_PASSED', passed=True,
                      frozen_checkpoint={'path': str(checkpoint), **identity(checkpoint)},
                      archive={'path': str(archive), **identity(archive)},
                      archive_manifest={'path': str(manifest_path), **identity(manifest_path)},
                      complete_regular_evidence_roles=len(entries), inert_symlink_roles=len(links),
                      physical_files_hashed=len(physical_hashes), all_8641_roles_bound_to_exact_bytes_and_mode=True,
                      verified_archive_members=len(archived), external_runtime_roles=external_roles,
                      external_runtime_byte_identities_rehashed=True,
                      durable_commit_references_inspected_not_network_reverified=True,
                      exact_frozen_source_files_verified=13, exact_parent_guard_files_verified=parent_guard_files,
                      exact_five_file_derivation_rebuilt=True, all_nine_pre_review_source_hashes_preserved=True,
                      actual_parent_commands_verified=len(expected_commands), host_tests_inspected=host_tests,
                      policy_format_faults_inspected=5, raw_source_and_evidence_unchanged=True,
                      fresh_android_execution_still_required=True,
                      full_runtime_1_to_1_established=False)
    except Exception as error:
        report.update(status='INDEPENDENT_FROZEN_READINESS_WORKFLOW_AUDIT_FAILED',
                      reason=type(error).__name__ + ': ' + str(error))
    report['seconds'] = time.monotonic() - started
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUTPUT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
