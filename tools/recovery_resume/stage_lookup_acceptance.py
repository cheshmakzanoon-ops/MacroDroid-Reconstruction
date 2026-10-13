#!/usr/bin/env python3
"""Inspect and stage one fixed successful lookup acceptance run as Git blobs.

The downloaded archive is read as inert data. Its historical filesystem receipts
are preserved, not relabelled as observations of this extraction. This program
never executes downloaded code, creates a commit, or moves a branch.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO = 'cheshmakzanoon-ops/MacroDroid-Reconstruction'
REPO_ID = 1414876481
RUN_ID = 38365018305
SOURCE_COMMIT = 'daf58639000f449a55ac1985746925cd2a1816e8'
WORKFLOW = '.github/workflows/day-trigger-wip-acceptance.yml'
PINS_SHA256 = '8a492093e1b5b2fd602e56535f3f29746129d1a1755c23b4153eea450dbbd41b'
LOCAL_APK_SHA256 = 'bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2'
MAX_ARCHIVE = 512 * 1024 * 1024
MAX_EXPANDED = 2 * 1024 * 1024 * 1024
PART_BYTES = 8 * 1024 * 1024
PREFIX = 'docs/verification/lookup-hosted-daf5863'
PROJECT_PREFIX = 'combined-workspace/MacroDroid_v9/'


class PublicationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PublicationError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {'bytes': len(data), 'sha256': digest(data)}


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def document(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(PublicationError('Nonfinite JSON value')))


def relative(name):
    require(type(name) is str and name != '' and '\\' not in name and '\x00' not in name,
            'Invalid archive path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name,
            'Noncanonical archive path')
    return path


def release_input(name):
    """Match the pinned release-integrity scope, not root documentation."""
    path = relative(name)
    if len(path.parts) == 1:
        return path.suffix == '.py'
    if path.parts[0] not in ('source', 'test-support', 'tests', 'signing', 'tools', 'reference'):
        return False
    return ('__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')
            and not (path.parts[0] == 'tools' and 'classes' in path.parts))


def checked_run(run):
    require(run.get('id') == RUN_ID and type(run['id']) is int
            and run.get('repository', {}).get('id') == REPO_ID
            and run.get('head_repository', {}).get('id') == REPO_ID
            and run.get('head_branch') == 'main' and run.get('head_sha') == SOURCE_COMMIT
            and run.get('path') == WORKFLOW and run.get('event') in ('push', 'workflow_dispatch')
            and run.get('status') == 'completed' and run.get('conclusion') == 'success'
            and type(run.get('run_attempt')) is int and run['run_attempt'] > 0,
            'The exact successful main-branch source run is required')


def checked_archive(archive, expected_digest):
    require(re.fullmatch(r'sha256:[0-9a-f]{64}', expected_digest or '') is not None,
            'Missing exact artifact digest')
    require(archive.is_file() and not archive.is_symlink() and archive.stat().st_size <= MAX_ARCHIVE,
            'Archive exceeds bounded regular-file scope')
    with archive.open('rb') as stream:
        actual = 'sha256:' + hashlib.file_digest(stream, 'sha256').hexdigest()
    require(actual == expected_digest, 'Downloaded archive digest differs')
    inventory, seen = [], set()
    with zipfile.ZipFile(archive) as source:
        rows = source.infolist()
        require(len(rows) <= 50000 and sum(row.file_size for row in rows) <= MAX_EXPANDED,
                'Evidence expansion exceeds bounded scope')
        for row in rows:
            name = row.filename.rstrip('/') if row.is_dir() else row.filename
            relative(name)
            require(name not in seen and not stat.S_ISLNK(row.external_attr >> 16)
                    and row.file_size <= MAX_ARCHIVE and not row.flag_bits & 1,
                    'Duplicate, encrypted, symlink or oversized member')
            seen.add(name)
            if row.is_dir():
                continue
            checksum = hashlib.sha256(); size = 0
            with source.open(row) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    size += len(chunk); checksum.update(chunk)
            require(size == row.file_size, 'Member size differs')
            inventory.append({'path': name, 'bytes': size, 'sha256': checksum.hexdigest()})
    return inventory


def strict_success(report, pins):
    require(report.get('status') == 'ISOLATED_DAY_TRIGGER_NUMERIC_LOOKUP_ALL_16_HOST_GATES_VERIFIED'
            and report.get('passed') is True and report.get('active_promoted') is False
            and report.get('android_runtime_executed') is False
            and report.get('full_runtime_1_to_1_established') is False
            and report.get('candidate_is_wip_only') is True,
            'The live-host finalizer did not establish the required bounded source result')
    for key, value in [('gates_verified', 16), ('fresh_reports_verified', 24), ('actual_cases', 195151),
                       ('registered_methods', 1244), ('target_classes', 605), ('actual_ui_java_controls', 101)]:
        require(type(report.get(key)) is int and report[key] == value, 'Wrong acceptance count: ' + key)
    require(report.get('source_snapshot') == pins['future_snapshot']
            and report.get('future_manifest') == pins['future_manifest']
            and report.get('suite_cases') == pins['suite_cases']
            and report.get('lookup_source_commit') == pins['lookup_commit'],
            'Source, manifest, case partition or lookup commit differs')
    require(report.get('apks', {}).get('hybrid', {}).get('sha256') == LOCAL_APK_SHA256,
            'Hosted candidate does not match the independently rebuilt local APK')


def inspect(archive, expected_digest, repository):
    pins_raw = (repository / 'tools/day_trigger_acceptance/pins.json').read_bytes()
    require(digest(pins_raw) == PINS_SHA256, 'Reviewed acceptance pins differ')
    pins = document(pins_raw)
    inventory = checked_archive(archive, expected_digest)
    indexed = {row['path']: row for row in inventory}
    with zipfile.ZipFile(archive) as source:
        def raw(name):
            relative(name)
            require(name in indexed, 'Required artifact absent: ' + name)
            data = source.read(name)
            require(identity(data) == {key: indexed[name][key] for key in ('bytes', 'sha256')},
                    'Artifact changed during inspection')
            return data
        report_raw = raw('hosted-proof/verification.json')
        report = document(report_raw)
        strict_success(report, pins)
        preparation = document(raw('hosted-proof/preparation.json'))
        execution = document(raw('hosted-proof/execution.json'))
        require(preparation.get('passed') is True
                and preparation.get('status') == 'EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED'
                and execution.get('preparation_sha256') == digest(raw('hosted-proof/preparation.json')),
                'Preparation and execution linkage differs')
        wanted = report.get('verified_output_artifacts')
        require(type(wanted) is list and wanted and len({row['path'] for row in wanted}) == len(wanted),
                'Live-host verified file inventory is incomplete')
        for row in wanted:
            name = PROJECT_PREFIX + str(relative(row['path']))
            require(name in indexed and {key: indexed[name][key] for key in ('bytes', 'sha256')}
                    == {key: row[key] for key in ('bytes', 'sha256')},
                    'Archived bytes differ from final live-host verification: ' + name)
        latest = document(raw(PROJECT_PREFIX + 'reports/acceptance-latest.json'))
        require(latest.get('host_acceptance_passed') is True
                and latest.get('source_edit_probe_skipped') is False
                and latest.get('build_inputs_unchanged') is True
                and latest.get('input_snapshot_before') == latest.get('input_snapshot_after') == pins['future_snapshot']['snapshot_sha256'],
                'Application acceptance did not pass with exact unchanged inputs')
        gates = latest.get('commands')
        require(type(gates) is list and len(gates) == 16, 'Missing complete gate command inventory')
        for row, expected in zip(gates, pins['gate_commands']):
            require(row.get('label') == expected[0] and row.get('command') == [execution['python_executable'], *expected[1]]
                    and row.get('passed') is True and type(row.get('exit_code')) is int and row['exit_code'] == 0
                    and digest(raw(PROJECT_PREFIX + str(relative(row['log'])))) == row.get('log_sha256'),
                    'Gate label, command, literal exit or archived log differs')
        hashes = latest.get('fresh_evidence_sha256')
        require(type(hashes) is dict and set(hashes) == set(pins['fresh_reports']) and len(hashes) == 24,
                'Fresh report role inventory differs')
        for name, sha in hashes.items():
            require(digest(raw(PROJECT_PREFIX + 'reports/' + str(relative(name)))) == sha, 'Fresh gate report differs: ' + name)
        python_log = raw(PROJECT_PREFIX + 'reports/python-unit-tests.log').decode()
        require(len(re.findall(r'^test_\S+ \(.*\) \.\.\. ', python_log, re.M)) == 357
                and len(re.findall(r'(?:\.\.\. |^)ok$', python_log, re.M)) == 357
                and re.findall(r'^Ran (\d+) tests in [0-9.]+s$', python_log, re.M) == ['357']
                and python_log.rstrip().endswith('\nOK'), 'Python tests include omissions, skips or failures')
        snapshot = raw('hosted-proof/inputs/future-input-snapshot.json')
        require(identity(snapshot) == pins['future_manifest']
                and snapshot == raw(PROJECT_PREFIX + 'reports/release-input-snapshot.json'),
                'Full future input manifest is not exactly retained')
        selected = {}
        for row in pins['lookup_source_changes']:
            name = 'hosted-proof/inputs/lookup-overlay/project/' + str(relative(row['path']))
            data = raw(name)
            require(identity(data) == row['candidate'], 'Source delta differs: ' + name)
            selected['project/' + row['path']] = data
        require(len(selected) == 21, 'Lookup source path inventory differs')
        selected['project/reports/release-input-snapshot.json'] = snapshot
        apk_name = PROJECT_PREFIX + 'dist/MacroDroid-5.67.8-v9-hybrid.apk'
        apk = raw(apk_name)
        require(identity(apk) == report['apks']['hybrid'], 'Candidate bytes differ from closing proof')
        selected[PREFIX + '/selected/verification.json'] = report_raw
        for name in ('preparation.json', 'execution.json'):
            selected[PREFIX + '/selected/' + name] = raw('hosted-proof/' + name)
        for name in ('acceptance-latest.json', 'java-all-path-parity.json', 'java-ui-three-path-parity.json',
                     'day-numeric-dex-controls.json', 'day-lookup-dex-controls.json', 'python-unit-tests.log',
                     'hybrid-build.json', 'hybrid-roundtrip.json', 'hybrid-resource-parity.json'):
            selected[PREFIX + '/selected/' + name] = raw(PROJECT_PREFIX + 'reports/' + name)
    return pins, report, inventory, selected, apk


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Github:
    def __init__(self, token):
        self.token = token
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, payload=None):
        require(path.startswith('/') and not path.startswith('//'), 'Invalid repository API path')
        request = urllib.request.Request('https://api.github.com/repos/' + REPO + path,
            data=None if payload is None else json.dumps(payload).encode(),
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28'})
        for attempt in range(3):
            try:
                return self.opener.open(request, timeout=120)
            except urllib.error.HTTPError as error:
                if error.code not in (500, 502, 503, 504) or attempt == 2:
                    raise
                time.sleep(2 ** attempt)

    def json(self, path, payload=None):
        with self.request(path, payload) as stream:
            data = stream.read(32 * 1024 * 1024 + 1)
            require(len(data) <= 32 * 1024 * 1024, 'API response too large')
            return document(data)

    def download(self, artifact, output):
        try:
            with self.request('/actions/artifacts/' + str(artifact['id']) + '/zip'):
                raise PublicationError('Expected an artifact storage redirect')
        except urllib.error.HTTPError as error:
            if error.code != 302:
                raise PublicationError('Artifact API response is not the documented redirect') from None
            location = error.headers.get('Location', '')
        parsed = urllib.parse.urlsplit(location)
        require(parsed.scheme == 'https' and not parsed.username and not parsed.password and parsed.hostname
                and parsed.hostname.endswith(('.blob.core.windows.net', '.githubusercontent.com')),
                'Unapproved artifact storage host')
        # The signed URL is never printed; the API token is not forwarded.
        with self.opener.open(urllib.request.Request(location), timeout=120) as stream, output.open('xb') as target:
            size = 0
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                size += len(chunk); require(size <= MAX_ARCHIVE, 'Archive response exceeds bound'); target.write(chunk)
        require(size == artifact['size_in_bytes'], 'Artifact byte size differs from API metadata')

    def blob(self, name, data):
        require(len(data) <= 90 * 1024 * 1024, 'Git blob too large')
        value = self.json('/git/blobs', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
        oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(value.get('sha') == oid, 'Returned Git blob identity differs')
        return {'path': name, 'mode': '100644', 'type': 'blob', 'sha': oid, **identity(data)}


def multipart(data, directory, filename, purpose):
    files, parts = {}, []
    for index, offset in enumerate(range(0, len(data), PART_BYTES), 1):
        name = directory + '/parts/part-' + f'{index:04d}' + '.bin'
        chunk = data[offset:offset + PART_BYTES]
        files[name] = chunk
        parts.append({'path': name, 'size_bytes': len(chunk), 'sha256': digest(chunk)})
    manifest = {'format': 'macrodroid-multipart-artifact', 'format_version': 1,
                'filename': filename, 'purpose': purpose, 'size_bytes': len(data), 'sha256': digest(data), 'parts': parts}
    files[directory + '/manifest.json'] = encoded(manifest)
    return files, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--archive-digest')
    parser.add_argument('--upload-blobs', action='store_true')
    args = parser.parse_args()
    repository = args.repository.resolve(); output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    client, run, artifact = None, None, None
    if args.archive is None or args.upload_blobs:
        require(os.environ.get('GITHUB_REPOSITORY') == REPO and os.environ.get('GITHUB_REF') == 'refs/heads/main',
                'Publishing is limited to the explicitly selected main branch')
        token = os.environ.get('GH_TOKEN'); require(bool(token), 'Scoped workflow token required')
        client = Github(token)
        run = client.json('/actions/runs/' + str(RUN_ID)); checked_run(run)
        result = client.json('/actions/runs/' + str(RUN_ID) + '/artifacts?per_page=100')
        require(result.get('total_count', 0) <= 100, 'Unexpected artifact pagination')
        candidates = [row for row in result['artifacts'] if row['name'] == 'day-trigger-wip-' + SOURCE_COMMIT and row['expired'] is False]
        require(len(candidates) == 1, 'One exact complete-run artifact is required')
        artifact = candidates[0]
        require(artifact['workflow_run']['id'] == RUN_ID and artifact['workflow_run']['head_sha'] == SOURCE_COMMIT
                and artifact['size_in_bytes'] <= MAX_ARCHIVE, 'Artifact is from another execution')
    archive = args.archive or output / 'evidence.zip'
    if args.archive is None:
        client.download(artifact, archive)
    expected = artifact['digest'] if artifact is not None else args.archive_digest
    pins, proof, members, selected, apk = inspect(archive, expected, repository)
    accepted = PREFIX + '/candidate'
    apk_files, apk_manifest = multipart(apk, accepted, 'MacroDroid-5.67.8-current-hybrid.apk',
        '1,244-body recovered source candidate; all sixteen host gates passed; no Android or whole-app parity claim.')
    raw_files, archive_manifest = multipart(archive.read_bytes(), PREFIX + '/raw', 'full-hosted-acceptance.zip',
        'Exact complete CI artifact, including actual live-host receipts and failed controls as recorded.')
    selected.update(apk_files); selected.update(raw_files)
    summary = {'schema': 1, 'run_id': RUN_ID, 'source_commit': SOURCE_COMMIT,
               'artifact_api': artifact, 'archive': identity(archive.read_bytes()), 'members': members,
               'source_snapshot': pins['future_snapshot'], 'apk': proof['apks']['hybrid'],
               'host_file_metadata_reexecuted': False, 'downloaded_code_executed': False,
               'new_android_runtime_executed': False, 'full_runtime_1_to_1_established': False}
    selected[PREFIX + '/inventory.json'] = encoded(summary)
    current = copy.deepcopy(apk_manifest)
    current.update(id='current-hybrid', media_type='application/vnd.android.package-archive', recovered_method_bodies=1244,
        recovered_classes=605, full_functional_parity_established=False,
        source_input_snapshot={'path': 'project/reports/release-input-snapshot.json', **pins['future_snapshot'],
                               'manifest_file_bytes': pins['future_manifest']['bytes'], 'manifest_file_sha256': pins['future_manifest']['sha256']},
        origin={'kind':'hosted-sixteen-gate-numeric-lookup-acceptance', 'run_id':RUN_ID, 'tooling_commit':SOURCE_COMMIT,
                'immutable_apk_manifest':accepted + '/manifest.json', 'literal_verification_path':PREFIX + '/selected/verification.json'},
        validation_at_publication={'configured_acceptance_gates_passed':16, 'original_jvm_rebuilt_cases':195151,
            'registered_methods':1244, 'python_tests_passed':357, 'actual_ui_java_fault_controls_passed':101,
            'android_executed_for_this_candidate':False})
    selected['artifacts/current/manifest.json'] = encoded(current)
    # Never silently overwrite a newer active source. Every present delta input
    # must still match the reviewed numeric parent, including required absences.
    for row in pins['lookup_source_changes']:
        target = repository / 'project' / row['path']
        require(not target.is_symlink(), 'Active overlay path is a symlink')
        if target.exists():
            require(target.is_file() and row['baseline'] is not None and identity(target.read_bytes()) == row['baseline'],
                    'Active source changed since the numeric parent: ' + row['path'])
    current_snapshot = repository / 'project/reports/release-input-snapshot.json'
    require(identity(current_snapshot.read_bytes()) == pins['numeric_future_manifest'], 'Active source snapshot is no longer the numeric parent')
    entry_map = document(current_snapshot.read_bytes())['entries']
    for path in sorted((repository / 'project').rglob('*')):
        require(not path.is_symlink(), 'Symlink in active project overlay')
        if not path.is_file() or path == current_snapshot:
            continue
        name = path.relative_to(repository / 'project').as_posix()
        if not release_input(name):
            continue
        require(name in entry_map and identity(path.read_bytes()) ==
                {'bytes': entry_map[name]['size'], 'sha256': entry_map[name]['sha256']},
                'Unregistered or changed active overlay input: ' + name)
    files = output / 'staged'
    entries = []
    for name, data in sorted(selected.items()):
        relative(name); path = files / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        entries.append(client.blob(name, data) if args.upload_blobs else {'path':name, **identity(data)})
    result = {'schema':1, 'status':'ACCEPTED_CHECKPOINT_STAGED_NOT_COMMITTED', 'run_id':RUN_ID,
              'source_commit':SOURCE_COMMIT, 'publication_base_commit':os.environ.get('GITHUB_SHA'),
              'uploaded_git_blobs':args.upload_blobs, 'tree_elements':entries,
              'full_runtime_1_to_1_established':False}
    (output / 'publication.json').write_bytes(encoded(result))
    print(json.dumps({key:value for key,value in result.items() if key != 'tree_elements'},indent=2))


if __name__ == '__main__':
    main()
