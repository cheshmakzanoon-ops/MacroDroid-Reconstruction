#!/usr/bin/env python3
"""Read the pinned cada56 source-job artifact without rebuilding or running Android."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess

BASE = Path('/workspace/scratch/4130730d15aa')
REPO = BASE / 'MacroDroid-Reconstruction'
SOURCE = BASE / 'tooling-validation/hosted-source-run-38202401393'
OUT = BASE / 'tooling-validation/source-run-38202401393-publication'
COMMIT = 'cada56c8a11ff5cbd892ec6d0beaeab60b3e644d'
APK_COMMIT = '3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677'
PIN = '19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text())


def git_file(commit, path):
    return subprocess.check_output(['git', 'show', commit + ':' + path], cwd=REPO)


def main():
    assert not OUT.exists()
    extraction = read(BASE / 'tooling-validation/hosted-source-run-38202401393-extraction.json')
    api = read(BASE / 'tooling-validation/cada-source-api-metadata.json')
    artifact = api['artifact']
    job = api['source_job']
    assert job['id'] == 114658428239 and job['conclusion'] == 'success'
    assert artifact['id'] == 11726184276 and artifact['workflow_run']['id'] == 38202401393
    assert artifact['workflow_run']['head_sha'] == COMMIT
    archive = BASE / 'tooling-validation/source-build-cada56c.zip'
    assert archive.stat().st_size == artifact['size_in_bytes'] == 127146419
    archive_hash = digest(archive)
    assert 'sha256:' + archive_hash == artifact['digest']
    assert archive_hash == '6e4290fb8e54265cb441db0317a771ea9320be0b720d241b36ac6a7dc94f575f'
    assert extraction['all_payload_bytes_verified'] is True
    assert extraction['zip_sha256'] == archive_hash and extraction['source_commit'] == COMMIT
    rows = extraction['files']
    assert len(rows) == len({r['path'] for r in rows}) == 108
    reports = []
    preserved = []
    secret_matches = []
    for row in rows:
        p = PurePosixPath(row['path'])
        assert not p.is_absolute() and '..' not in p.parts
        if row['path'].endswith('.apk'):
            assert row['durable_apk_commit'] == APK_COMMIT
            pin = json.loads(git_file(APK_COMMIT, row['durable_apk_manifest']))
            assert pin['size_bytes'] == row['size_bytes'] and pin['sha256'] == row['sha256']
            kept = {'kind': 'exact_apk_in_existing_multipart_manifest',
                    'repository_path': row['durable_apk_manifest'], 'commit': APK_COMMIT}
        else:
            assert row['path'].startswith('reports/')
            path = SOURCE / row['path']
            data = path.read_bytes()
            assert len(data) == row['size_bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
            reports.append(row)
            kept = {'kind': 'exact_report_file', 'repository_relative_path': row['path']}
            if re.search(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}', data):
                secret_matches.append(row['path'])
        preserved.append({'artifact_path': row['path'], 'size_bytes': row['size_bytes'],
                          'sha256': row['sha256'], 'preserved_as': kept})
    assert len(reports) == 106 and not secret_matches
    result = read(SOURCE / 'reports/acceptance-latest.json')
    run_path = 'reports/acceptance-20261012T040751585250Z'
    assert result == read(SOURCE / run_path / 'result.json')
    labels = ['input-integrity', 'baseline-build', 'hybrid-build', 'baseline-code', 'hybrid-code',
              'baseline-resources', 'hybrid-resources', 'positive-host-tests', 'reference-status',
              'engine-negative-controls', 'ui-negative-controls', 'core-negative-controls',
              'environment-negative-controls', 'legacy-negative-control', 'signed-source-edit',
              'final-positive-host-tests']
    assert [r['label'] for r in result['commands']] == labels
    gate_checks = []
    for command in result['commands']:
        assert type(command['exit_code']) is int and command['exit_code'] == 0 and command['passed'] is True
        assert command['log'].startswith(run_path + '/')
        assert digest(SOURCE / command['log']) == command['log_sha256']
        gate_checks.append(dict(label=command['label'], path=command['log'], sha256=command['log_sha256'], verified=True))
    assert result['host_acceptance_passed'] is True and result['source_edit_probe_skipped'] is False
    assert result['input_snapshot_before'] == result['input_snapshot_after'] == PIN
    assert result['input_files'] == 81245 and result['build_inputs_unchanged'] is True
    assert result['android_runtime_executed'] is False and result['full_runtime_1_to_1_established'] is False
    assert result['complete_high_level_java_kotlin_source'] is False and result['android_status'] == 'BLOCKED'
    fresh_checks = []
    assert len(result['fresh_evidence_sha256']) == 19
    for name, expected in result['fresh_evidence_sha256'].items():
        assert digest(SOURCE / 'reports' / name) == expected
        fresh_checks.append(dict(path='reports/' + name, sha256=expected, verified=True))
    parity = read(SOURCE / 'reports/java-all-path-parity.json')
    assert parity['passed'] is True and parity['schemaValid'] is True
    assert parity['cases'] == 188791 and parity['methodsCovered'] == parity['methodsExpected'] == 1240
    assert parity['paths'] == 3 and parity['failedCases'] == parity['unsupportedExecutions'] == 0
    assert parity['exactMethodKeyPartitionVerified'] is True and parity['rebuiltDexComparedToApk'] is True
    assert parity['androidRuntime'] is False
    assert parity['apkSha256'] == result['apks']['hybrid']['sha256']
    for variant, apk in result['apks'].items():
        match = [r for r in rows if r['path'] == apk['path']]
        assert len(match) == 1 and match[0]['size_bytes'] == apk['bytes'] and match[0]['sha256'] == apk['sha256']
    controls = read(SOURCE / 'reports/ui-negative-controls.json')
    assert controls['pass'] is True and controls['positiveRestorationPassed'] is True
    assert controls['sourceFixtureAndApkUnchanged'] is True and controls['androidRuntime'] is False
    assert controls['restorationCases'] == 18476 and len(controls['controls']) == 37
    assert len({c['mutation'] for c in controls['controls']}) == 37
    for c in controls['controls']:
        assert c['pass'] is True and c['requiredCaseRejected'] is True and c['failedCases'] > 0
        assert c['unsupportedExecutions'] == 0 and type(c['exitCode']) is int and c['exitCode'] == 2
        assert c['sourceFixtureAndApkUnchanged'] is True
    log = (SOURCE / 'reports/python-unit-tests.log').read_text()
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', log, re.M) == [('259', '6.340')]
    assert len(re.findall(r'^test.* \.\.\. ok$', log, re.M)) == 259
    assert log.splitlines()[-1] == 'OK'
    for filename in ['migration-static-proof.json', 'migration-linkage-check.json']:
        report = read(SOURCE / 'reports' / filename)
        assert report['pass'] is True and report['constructor_owner_corrections'] == []
    snapshot_bytes = git_file(COMMIT, 'project/reports/release-input-snapshot.json')
    assert hashlib.sha256(snapshot_bytes).hexdigest() == '713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883'
    snapshot = json.loads(snapshot_bytes)
    assert snapshot['snapshot_sha256'] == PIN and snapshot['files'] == len(snapshot['entries']) == 81245
    verification = dict(
        status='COMPLETE_CONFIGURED_HOST_ACCEPTANCE_VERIFIED', verified_utc=datetime.now(timezone.utc).isoformat(),
        source_checkpoint=COMMIT, workflow_run_id=38202401393, source_job_id=job['id'],
        source_job_completed_utc=job['completed_at'], github_artifact_digest_verified=True,
        all_108_payload_hashes_verified=True, exact_reports_preserved=len(reports),
        exact_report_bytes=sum(r['size_bytes'] for r in reports), gate_log_checks=gate_checks,
        fresh_evidence_checks=fresh_checks,
        input_binding=dict(before_and_after_snapshot=PIN, input_files_reported_by_ci=81245,
                           unchanged_reported_by_ci=True,
                           committed_snapshot_file_sha256=hashlib.sha256(snapshot_bytes).hexdigest(),
                           committed_snapshot_entries_verified=len(snapshot['entries']),
                           independent_publisher_rehash_of_all_source_inputs=False),
        host_cases=188791, methods=1240, execution_paths=3, mismatches=0, unsupported_executions=0,
        python_tests=259, python_test_seconds=6.340, ui_negative_controls=37,
        each_named_case_rejected_without_unsupported=True, ui_positive_restoration_cases=18476,
        apks={variant: next(r for r in preserved if r['artifact_path'] == apk['path']) for variant, apk in result['apks'].items()},
        constructor_owner_corrections_static_and_linkage=0,
        android_executed_by_source_acceptance=False, separate_android_job_conclusion='failure',
        full_runtime_1_to_1_established=False, historical_report_files_preserved_without_relabeling=True,
        report_key_material_scan_matches=0,
    )
    OUT.mkdir()
    for row in reports:
        dst = OUT / row['path']; dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / row['path'], dst)
    manifest = dict(source_commit=COMMIT, workflow_run=38202401393, artifact_id=artifact['id'],
                    original_zip_size_bytes=archive.stat().st_size, original_zip_sha256=archive_hash,
                    complete_payloads_preserved=True, payload_count=len(preserved), files=preserved)
    for name, data in [('manifest.json', manifest), ('independent-verification.json', verification),
                       ('source-job.json', job), ('github-artifact.json', artifact)]:
        (OUT / name).write_text(json.dumps(data, indent=2) + '\n')
    shutil.copyfile(Path(__file__), OUT / Path(__file__).name)
    print(json.dumps({k: verification[k] for k in ['status', 'exact_reports_preserved', 'host_cases', 'methods', 'python_tests', 'ui_negative_controls']} | {'output': str(OUT)}))


if __name__ == '__main__':
    main()
