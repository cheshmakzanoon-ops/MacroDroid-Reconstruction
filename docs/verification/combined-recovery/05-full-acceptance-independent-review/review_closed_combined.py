"""Independently review the closed combined05 evidence; no build or Android calls."""
from __future__ import annotations
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import time

BASE = Path(__file__).resolve().parent.parent
CAP = BASE / 'combined-recovery/checkpoints/05-full-acceptance'
PREP = BASE / 'combined-recovery/checkpoints/04-fresh-source-preparation'
OUT = BASE / 'combined-acceptance-review/01-closed-capsule'
CPIN = 'e4cd0b6af4cf95d7131138b3ad3dab8a070042cea077a80cf83c322168457063'
PPIN = 'da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6'
PIN = 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
OLD_PIN = '19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183'
APK = '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def meta(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def data_meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(name, data):
    with (OUT / name).open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def load(path):
    return json.loads(path.read_bytes())


def capsule(path, pin):
    assert meta(path / 'checkpoint.json')['sha256'] == pin
    value = load(path / 'checkpoint.json')
    rows = value['files']
    assert len(rows) == len({row['path'] for row in rows})
    actual_paths = {p.relative_to(path).as_posix() for p in path.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts and p.name != 'checkpoint.json'}
    assert actual_paths == {row['path'] for row in rows}
    for row in rows:
        source = path / row['path']
        assert not source.is_symlink() and source.resolve().is_relative_to(path.resolve())
        assert meta(source) == {key: row[key] for key in ('bytes', 'sha256')}, row['path']
    return value


def verify_pin(value, pin, count):
    assert value['format'] == 1 and value['files'] == len(value['entries']) == count
    assert value['snapshot_sha256'] == pin
    assert hashlib.sha256(json.dumps(value['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest() == pin


def full_inputs(root, expected):
    start = time.monotonic()
    observed = {}
    paths = []
    for directory in ('source', 'test-support', 'tests', 'signing', 'tools', 'reference'):
        paths.extend(path for path in (root / directory).rglob('*')
                     if path.is_file() and '__pycache__' not in path.parts
                     and path.suffix not in ('.pyc', '.pyo')
                     and not (directory == 'tools' and 'classes' in path.relative_to(root).parts))
    paths.extend(root.glob('*.py'))
    assert len(paths) == len({path.relative_to(root).as_posix() for path in paths}) == expected['files']
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        identity = meta(path)
        actual = {'size': identity['bytes'], 'sha256': identity['sha256']}
        assert actual == expected['entries'][relative], relative
        observed[relative] = actual
    assert observed == expected['entries']
    digest = hashlib.sha256(json.dumps(observed, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == expected['snapshot_sha256']
    return {'root': str(root), 'files_rehashed': len(observed), 'total_bytes_rehashed': sum(row['size'] for row in observed.values()),
            'actual_input_inventory_exact': True, 'canonical_sha256': digest,
            'elapsed_seconds': time.monotonic() - start}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    result = {'schema': 1, 'status': 'REVIEW_RUNNING', 'passed': False, 'started_utc': now(),
              'combined_checkpoint_sha256': CPIN, 'reviewed_preparation_checkpoint_sha256': PPIN,
              'build_executed': False, 'tests_reexecuted': False, 'android_executed': False,
              'active_source_modified': False, 'whole_application_1_to_1_established': False}
    try:
        cap, prep = capsule(CAP, CPIN), capsule(PREP, PPIN)
        assert len(cap['files']) == 125 and cap['preparation_checkpoint_sha256'] == PPIN
        assert cap['passed'] is True and cap['status'] == 'COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED'
        result['capsule_files_verified'] = 125
        result['preparation_files_verified'] = len(prep['files'])
        print('All 125 combined capsule files and reviewed preparation bytes verified.', flush=True)
        preparation = load(PREP / 'preparation/preparation.json')
        closed = load(CAP / 'result.json')
        assert closed['preparation']['sha256'] == meta(PREP / 'preparation/preparation.json')['sha256']
        assert preparation['candidate_inputs']['snapshot_sha256'] == PIN
        snapshot_path = CAP / 'project/reports/release-input-snapshot.json'
        new = load(snapshot_path)
        verify_pin(new, PIN, 81291)
        with tarfile.open(PREP / 'input-snapshot.tar.gz', 'r:gz') as archive:
            members = archive.getmembers()
            assert len(members) == 1 and members[0].isfile()
            assert archive.extractfile(members[0]).read() == snapshot_path.read_bytes()
        baseline_root = Path(preparation['baseline_project'])
        baseline_manifest = baseline_root / 'reports/release-input-snapshot.json'
        assert meta(baseline_manifest)['sha256'] == preparation['baseline_manifest_sha256'] == '713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883'
        old = load(baseline_manifest)
        verify_pin(old, OLD_PIN, 81245)
        repository_manifest = BASE / 'MacroDroid-Reconstruction/project/reports/release-input-snapshot.json'
        assert repository_manifest.read_bytes() == baseline_manifest.read_bytes()
        old_entries, new_entries = old['entries'], new['entries']
        delta = {'added': sorted(new_entries.keys() - old_entries.keys()),
                 'removed': sorted(old_entries.keys() - new_entries.keys()),
                 'changed': sorted(path for path in old_entries.keys() & new_entries.keys() if old_entries[path] != new_entries[path])}
        assert delta == preparation['input_delta']
        assert (len(delta['added']), len(delta['changed']), len(delta['removed'])) == (46, 17, 0)
        paths = set(delta['added'] + delta['changed'])
        cap_delta = {row['path'].removeprefix('project/') for row in cap['files']
                     if row['path'].startswith('project/') and row['path'] != 'project/reports/release-input-snapshot.json'}
        assert paths == cap_delta and len(paths) == 63
        delta_rows = []
        reconstructed = dict(old_entries)
        for path in sorted(paths):
            a, b = PREP / 'project' / path, CAP / 'project' / path
            assert meta(a) == meta(b) == {'bytes': new_entries[path]['size'], 'sha256': new_entries[path]['sha256']}
            actual_old = meta(baseline_root / path) if (baseline_root / path).exists() else None
            expected_old = ({'bytes': old_entries[path]['size'], 'sha256': old_entries[path]['sha256']}
                            if path in old_entries else None)
            assert actual_old == expected_old
            repository_path = BASE / 'MacroDroid-Reconstruction/project' / path
            assert (meta(repository_path) if repository_path.exists() else None) == expected_old
            reconstructed[path] = {'size': b.stat().st_size, 'sha256': meta(b)['sha256']}
            delta_rows.append({'path': path, 'before': expected_old, 'after': meta(b),
                               'reviewed04_equal': True, 'current_and_repository_baseline_equal': True})
        assert reconstructed == new_entries
        assert hashlib.sha256(json.dumps(reconstructed, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == PIN
        write('exact-63-path-source-delta.json', delta_rows)
        registry = load(CAP / 'project/source/java-method-map.json')
        base_registry = load(baseline_root / 'source/java-method-map.json')
        ui_registry = load(CAP / 'project/source/ui-methods.json')
        assert len(registry) == 1242 and registry[:-2] == base_registry and len({row['target'] for row in registry}) == 605
        assert len(ui_registry) == 10 and ui_registry[:-2] == load(baseline_root / 'source/ui-methods.json')
        result['source_coherence'] = {'old_pin': OLD_PIN, 'new_pin': PIN, 'added': 46, 'changed': 17, 'removed': 0,
            'all_63_reviewed04_delta_files_exact': True, 'entire_new_manifest_reconstructed_from_current_baseline': True,
            'existing_registry_entries_retained': 1240, 'new_registry_entries': registry[-2:], 'registry_classes': 605}
        acceptance = load(CAP / 'reviewable/acceptance-latest.json')
        assert data_meta((CAP / 'reviewable/acceptance-latest.json').read_bytes()) == closed['acceptance']
        labels = ['input-integrity', 'baseline-build', 'hybrid-build', 'baseline-code', 'hybrid-code', 'baseline-resources',
                  'hybrid-resources', 'positive-host-tests', 'reference-status', 'engine-negative-controls',
                  'ui-negative-controls', 'core-negative-controls', 'environment-negative-controls', 'legacy-negative-control',
                  'signed-source-edit', 'final-positive-host-tests']
        assert [row['label'] for row in acceptance['commands']] == labels
        assert acceptance['host_acceptance_passed'] is True and acceptance['source_edit_probe_skipped'] is False
        assert acceptance['input_snapshot_before'] == acceptance['input_snapshot_after'] == PIN
        assert acceptance['build_inputs_unchanged'] is True and acceptance['android_runtime_executed'] is False
        assert len(acceptance['fresh_evidence_sha256']) == 22
        report_manifest = load(CAP / 'complete-reports-manifest.json')
        assert meta(CAP / 'complete-reports.tar.gz') == {key: report_manifest[key] for key in ('bytes', 'sha256')}
        expected_reports = {row['path']: row for row in report_manifest['files']}
        assert len(expected_reports) == len(report_manifest['files']) == report_manifest['file_count'] == 551
        verified_reports, documents = {}, {}
        with tarfile.open(CAP / 'complete-reports.tar.gz', 'r|gz') as archive:
            for member in archive:
                assert member.isfile() and member.name not in verified_reports
                assert not Path(member.name).is_absolute() and '..' not in Path(member.name).parts
                data = archive.extractfile(member).read()
                actual = data_meta(data)
                assert actual == {key: expected_reports[member.name][key] for key in ('bytes', 'sha256')}
                verified_reports[member.name] = actual
                if member.name in {'ui-negative-baseline.json', 'ui-positive-restoration.json'} or member.name.endswith('-negative-failures.json'):
                    parsed = json.loads(data)
                    if member.name.endswith('-negative-failures.json'):
                        parsed.pop('failures', None)
                    documents[member.name] = parsed
        assert set(verified_reports) == set(expected_reports)
        write('all-551-archive-member-verification.json', verified_reports)
        assert verified_reports['release-input-snapshot.json'] == meta(snapshot_path)
        assert verified_reports['acceptance-latest.json'] == meta(CAP / 'reviewable/acceptance-latest.json')
        fresh = []
        for name, digest in acceptance['fresh_evidence_sha256'].items():
            actual = meta(CAP / 'reviewable' / name)
            assert actual == verified_reports[name] and actual['sha256'] == digest
            fresh.append({'path': name, **actual})
        write('all-22-fresh-report-verification.json', fresh)
        gates = []
        for row in acceptance['commands']:
            actual = meta(CAP / 'commands' / Path(row['log']).name)
            assert actual['sha256'] == row['log_sha256'] and actual == verified_reports[row['log'].removeprefix('reports/')]
            assert row['passed'] is True and type(row['exit_code']) is int and row['exit_code'] == 0
            assert row['timeout_seconds'] == (5400 if row['label'] == 'ui-negative-controls' else 1200)
            assert 0 < row['seconds'] < row['timeout_seconds']
            gates.append({**row, 'local_and_archived_log': actual})
        write('all-16-gate-log-verification.json', gates)
        controls = load(CAP / 'reviewable/ui-negative-controls.json')
        assert controls['pass'] is True and controls['controlsCount'] == controls['expectedControlCount'] == len(controls['controls']) == 78
        assert len({row['mutation'] for row in controls['controls']}) == 78
        positive = documents['ui-negative-baseline.json']
        assert positive == documents['ui-positive-restoration.json']
        assert controls['positiveRestorationPassed'] is True and controls['positiveRestorationExactBaseline'] is True
        assert controls['restorationCases'] == positive['cases'] == 23174
        assert controls['positiveBaselineSha256'] == fresh[[row['path'] for row in fresh].index('java-ui-three-path-parity.json')]['sha256']
        mutants = []
        for row in controls['controls']:
            source, bytecode = row['retainedSource'].removeprefix('reports/'), row['retainedClass'].removeprefix('reports/')
            assert verified_reports[source]['sha256'] == row['mutantSourceSha256']
            assert verified_reports[bytecode]['sha256'] == row['mutantClassSha256'] != row['positiveClassSha256']
            assert row['pass'] is True and row['requiredCaseRejected'] is True and row['exitCode'] == 2
            assert row['sourceFixtureAndApkUnchanged'] is True and row['originalCoverageAndInventoryUnchanged'] is True
            failure = documents[row['mutation'] + '-negative-failures.json']
            assert failure['passed'] is False and failure['failedCases'] == row['failedCases'] > 0
            assert failure['unsupportedExecutions'] == row['unsupportedExecutions'] == 0
            assert all(case in failure['failedCaseLabels'] for case in row['requiredCases'])
            for key in ('cases', 'methodsCovered', 'methodKeys', 'methods', 'instructionCoverage', 'paths'):
                assert failure[key] == positive[key], (row['mutation'], key)
            mutants.append({'mutation': row['mutation'], 'retained_source': verified_reports[source],
                            'retained_class': verified_reports[bytecode], 'failed_cases': row['failedCases'],
                            'required_cases_actually_rejected': row['requiredCases'],
                            'full_original_method_case_and_instruction_inventory_unchanged': True})
        write('all-78-retained-mutant-verification.json', mutants)
        python_log = (CAP / 'reviewable/python-unit-tests.log').read_text()
        python_match = re.search(r'\nRan (\d+) tests in ([0-9.]+)s\s+OK\s*$', python_log)
        assert python_match and int(python_match[1]) == 273
        assert len(re.findall(r'^test_.* \.\.\. ok$', python_log, re.M)) == 273
        assert meta(CAP / 'reviewable/python-unit-tests.log') == verified_reports['python-unit-tests.log']
        overall = load(CAP / 'reviewable/java-all-path-parity.json')
        assert overall['passed'] is True and overall['cases'] == sum(overall['suiteCases'].values()) == 193489
        assert overall['methodsCovered'] == overall['methodsExpected'] == 1242 and overall['paths'] == 3
        assert overall['failedCases'] == overall['unsupportedExecutions'] == 0
        assert overall['apkSha256'] == APK and overall['schemaValid'] is True
        assert overall['exactMethodKeyPartitionVerified'] is True and overall['rebuiltDexComparedToApk'] is True
        apk_manifest = load(CAP / 'apk/manifest.json')
        assert len(apk_manifest['parts']) == 12 and apk_manifest['sha256'] == APK
        joined, total, parts = hashlib.sha256(), 0, []
        for index, row in enumerate(apk_manifest['parts'], 1):
            name = f'part-{index:04d}.bin'
            assert row['path'] == 'work-in-progress/combined-recovery/05-full-acceptance/apk/' + name
            data = (CAP / 'apk' / name).read_bytes()
            assert len(data) == row['size_bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
            assert hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest() == row['git_blob_sha1']
            joined.update(data)
            total += len(data)
            parts.append({'name': name, 'bytes': len(data), 'sha256': row['sha256'], 'git_blob_sha1': row['git_blob_sha1']})
        assert total == apk_manifest['size_bytes'] == 94683119 and joined.hexdigest() == APK
        assert closed['apks'] == acceptance['apks'] == cap['apks']
        private = Path(closed['project'])
        for variant, identity in closed['apks'].items():
            assert meta(private / identity['path']) == {key: identity[key] for key in ('bytes', 'sha256')}
        write('all-12-apk-part-verification.json', {'parts': parts, 'total_bytes': total, 'joined_sha256': joined.hexdigest(),
                                                'exact_closed_dist_apks_verified': closed['apks']})
        print('All 551 archive members, 22 fresh reports, 16 gate logs, 78 actual mutants and 12 APK parts verified.', flush=True)
        rehashed = [full_inputs(baseline_root, old), full_inputs(private, new)]
        write('full-input-rehash-verification.json', rehashed)
        assert meta(baseline_manifest)['sha256'] == preparation['baseline_manifest_sha256']
        assert meta(snapshot_path)['sha256'] == prep['input_manifest']['sha256']
        result.update(status='INDEPENDENT_COMBINED05_COHERENCE_REVIEW_PASSED', passed=True,
            archive_members_verified=551, fresh_report_hashes_verified=22, gate_logs_verified=16,
            retained_mutant_source_class_pairs_verified=78, full_positive_restoration_json_equal=True,
            actual_python_tests=273, actual_python_seconds=float(python_match[2]),
            actual_three_path_cases=193489, actual_registered_methods=1242,
            multipart_apk_bytes=total, multipart_apk_sha256=joined.hexdigest(),
            current_baseline_input_files_rehashed=81245, closed_candidate_input_files_rehashed=81291,
            source_delta_files=63, full_input_rehash=rehashed,
            publication_verdict='APPROVED_AS_SCOPED_CLOSED_HOST_EVIDENCE; ANDROID_RESULT_PENDING_FOR_THIS_APK')
    except BaseException as error:
        result.update(status='INDEPENDENT_COMBINED05_REVIEW_REJECTED', error=repr(error))
        raise
    finally:
        result['finished_utc'] = now()
        write('review-result.json', result)
        print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
