#!/usr/bin/env python3
"""Stream-check one hosted source artifact; do not extract APKs or large tables."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

BASE = Path(__file__).resolve().parent
REPO = BASE.parent / 'MacroDroid-Reconstruction'
ZIP = BASE.parent / 'tooling-validation/reconstruction-run-38214498395.zip'
OUT = BASE / 'source-run-38214498395-independent-review'
HEAD = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
ARCHIVE = {'bytes': 188134390, 'sha256': 'da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88'}
SNAPSHOT = 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
HYBRID = '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
GATES = ['input-integrity','baseline-build','hybrid-build','baseline-code','hybrid-code',
         'baseline-resources','hybrid-resources','positive-host-tests','reference-status',
         'engine-negative-controls','ui-negative-controls','core-negative-controls',
         'environment-negative-controls','legacy-negative-control','signed-source-edit','final-positive-host-tests']


def file_identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def byte_identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def git_bytes(name):
    result = subprocess.run(['git','show',HEAD + ':' + name], cwd=REPO,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    assert result.returncode == 0, (name, result.stderr.decode())
    return result.stdout


def main():
    started = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=False)
    assert file_identity(ZIP) == ARCHIVE
    member_rows = []
    with zipfile.ZipFile(ZIP) as zipped:
        names = zipped.namelist()
        assert len(names) == len(set(names)) == 1136
        for info in zipped.infolist():
            name = PurePosixPath(info.filename)
            assert not info.is_dir() and not name.is_absolute() and '..' not in name.parts
            assert name.as_posix() == info.filename and '\\' not in info.filename
            digest = hashlib.sha256()
            size = 0
            with zipped.open(info) as stream:
                while block := stream.read(1024 * 1024):
                    size += len(block)
                    digest.update(block)
            assert size == info.file_size
            member_rows.append({'path': info.filename, 'bytes': size, 'sha256': digest.hexdigest(),
                                'zip_compressed_bytes': info.compress_size, 'zip_crc32': f'{info.CRC:08x}'})
        members = {row['path']: row for row in member_rows}
        def metadata(name):
            return {k: members[name][k] for k in ('bytes','sha256')}
        def data(name):
            raw = zipped.read(name)
            assert byte_identity(raw) == metadata(name)
            return raw
        def document(name):
            return json.loads(data(name))
        latest = document('reports/acceptance-latest.json')
        assert latest['host_acceptance_passed'] is True
        assert latest['source_edit_probe_skipped'] is False
        assert latest['android_runtime_executed'] is False and latest['full_runtime_1_to_1_established'] is False
        assert latest['input_files'] == 81291 and latest['build_inputs_unchanged'] is True
        assert latest['input_snapshot_before'] == latest['input_snapshot_after'] == SNAPSHOT
        assert [row['label'] for row in latest['commands']] == GATES
        gate_folder = str(PurePosixPath(latest['commands'][0]['log']).parent)
        assert data(gate_folder + '/result.json') == data('reports/acceptance-latest.json')
        for index, row in enumerate(latest['commands'],1):
            assert row['log'] == f'{gate_folder}/{index:02d}-{row["label"]}.log'
            assert row['exit_code'] == 0 and row['passed'] is True
            assert row['timeout_seconds'] == (5400 if row['label'] == 'ui-negative-controls' else 1200)
            assert 0 <= row['seconds'] <= row['timeout_seconds']
            assert metadata(row['log'])['sha256'] == row['log_sha256']
        assert len(latest['fresh_evidence_sha256']) == 22
        fresh = []
        for name,digest in latest['fresh_evidence_sha256'].items():
            row = metadata('reports/' + name)
            assert row['sha256'] == digest
            fresh.append({'path': 'reports/' + name, **row})
        input_raw = data('reports/release-input-snapshot.json')
        inputs = json.loads(input_raw)
        assert inputs['format'] == 1 and inputs['files'] == len(inputs['entries']) == 81291
        canonical = json.dumps(inputs['entries'],sort_keys=True,separators=(',',':')).encode()
        assert hashlib.sha256(canonical).hexdigest() == inputs['snapshot_sha256'] == SNAPSHOT
        source_manifest = git_bytes('project/reports/release-input-snapshot.json')
        assert source_manifest == input_raw
        for variant,size,digest in [('baseline',94677674,'aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096'),
                                    ('hybrid',94683119,HYBRID)]:
            row = latest['apks'][variant]
            assert row['path'] == f'dist/MacroDroid-5.67.8-v9-{variant}.apk'
            assert {'bytes':row['bytes'],'sha256':row['sha256']} == {'bytes':size,'sha256':digest}
            assert metadata(row['path']) == {'bytes':size,'sha256':digest}
            built = document('reports/' + variant + '-build.json')
            assert built['sha256'] == digest and built['bytes'] == size
        current = json.loads(git_bytes('artifacts/current/manifest.json'))
        assert current['sha256'] == HYBRID and current['size_bytes'] == 94683119
        all_path = document('reports/java-all-path-parity.json')
        assert all_path['passed'] is True and all_path['cases'] == 193489
        assert all_path['methodsCovered'] == all_path['methodsExpected'] == 1242
        assert all_path['paths'] == 3 and all_path['apkSha256'] == HYBRID
        assert all_path['failedCases'] == all_path['unsupportedExecutions'] == 0
        assert all_path['rebuiltDexComparedToApk'] is True and all_path['exactMethodKeyPartitionVerified'] is True
        assert sum(all_path['suiteCases'].values()) == all_path['cases']
        controls = document('reports/ui-negative-controls.json')
        assert controls['pass'] is True and controls['status'] == 'ALL_78_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED'
        assert controls['expectedControlCount'] == controls['controlsCount'] == len(controls['controls']) == 78
        assert controls['positiveRestorationExactBaseline'] and controls['positiveRestorationPassed'] and controls['sourceFixtureAndApkUnchanged']
        mutant_checks = []
        for row in controls['controls']:
            assert row['pass'] and row['requiredCaseRejected'] and row['failedCases'] > 0
            assert row['exitCode'] == 2 and row['unsupportedExecutions'] == 0
            assert row['sourceFixtureAndApkUnchanged'] and row['originalCoverageAndInventoryUnchanged']
            assert metadata(row['retainedSource'])['sha256'] == row['mutantSourceSha256']
            assert metadata(row['retainedClass'])['sha256'] == row['mutantClassSha256']
            assert row['mutantClassSha256'] != row['positiveClassSha256']
            mutant_checks.append({'mutation':row['mutation'],'retained_source': {'path':row['retainedSource'],**metadata(row['retainedSource'])},
                                  'retained_class':{'path':row['retainedClass'],**metadata(row['retainedClass'])},
                                  'failed_cases':row['failedCases'],'required_case_rejected':True})
        positive = document('reports/ui-negative-baseline.json')
        restoration = document('reports/ui-positive-restoration.json')
        assert positive == restoration and positive['passed'] is True and positive['cases'] == 23174
        python_text = data('reports/python-unit-tests.log').decode()
        summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',python_text,re.M)
        headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ',python_text,re.M)
        successes = re.findall(r'(?:\.\.\. |^)ok$',python_text,re.M)
        assert len(summaries) == 1 and summaries[0][0] == '273' and len(headers) == len(successes) == 273
        assert python_text.rstrip().endswith('\nOK')
        source_pins = []
        for name in ('.github/workflows/reconstruction.yml','project/acceptance.py','project/test.py',
                     'project/release_integrity.py','artifacts/current/manifest.json'):
            raw = git_bytes(name)
            target = OUT / 'reviewed-source' / name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(raw)
            source_pins.append({'path':name,'git_commit':HEAD,**byte_identity(raw)})
        assert "build.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'python-unit-tests.log')" in git_bytes('project/test.py').decode()
        proof_names = sorted(set(['reports/acceptance-latest.json',gate_folder+'/result.json',
            'reports/java-staging.json','reports/python-unit-tests.log','reports/ui-negative-baseline.json',
            'reports/ui-positive-restoration.json','reports/baseline-build.json','reports/hybrid-build.json',
            *[row['log'] for row in latest['commands']], *[row['path'] for row in fresh]]))
        for name in proof_names:
            assert members[name]['bytes'] < 1_000_000
            target = OUT / 'compact-evidence' / name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data(name))
        write('all-1136-member-identities.json', member_rows)
        write('all-78-retained-mutant-checks.json',mutant_checks)
        write('all-22-fresh-evidence-checks.json',fresh)
        write('source-commit-pins.json',source_pins)
        report = {'schema':1,'status':'HOSTED_SOURCE_JOB_ALL_16_GATES_AND_EXACT_CANDIDATE_VERIFIED',
                  'run_id':38214498395,'source_job_id':114695960566,'head_sha':HEAD,
                  'artifact_id':11731218792,'archive':ARCHIVE,'archive_member_count':1136,
                  'archive_expanded_bytes_checked_by_stream':sum(row['bytes'] for row in member_rows),
                  'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
                  'gate_started_utc':latest['started_utc'],'gate_finished_utc':latest['finished_utc'],
                  'all16_gate_logs_match_recorded_hashes':True,'all22_fresh_report_hashes_verified':True,
                  'source_input_files':81291,'source_input_snapshot':SNAPSHOT,
                  'canonical_complete_input_inventory_digest_recomputed':True,
                  'complete_input_manifest_bytes_equal_exact_git_source_commit':True,
                  'new_source_filesystem_rehash_or_rebuild_performed':False,
                  'actual_host_cases':193489,'actual_methods':1242,'paths':3,'suite_cases':all_path['suiteCases'],
                  'python_unit_tests':{'count':273,'seconds':float(summaries[0][1]),'individual_successes':273,
                                       **metadata('reports/python-unit-tests.log')},
                  'actual_ui_controls':78,'all78_retained_source_and_class_hashes_verified':True,
                  'ui_positive_restoration_object_equals_complete_baseline':True,
                  'apks':latest['apks'],'fresh_candidate_equals_committed_candidate_identity':True,
                  'source_job_android_probe_status':latest['android_status'],
                  'source_job_android_runtime_executed':False,
                  'combined_workflow_android_job_pass_inferred':False,
                  'full_runtime_1_to_1_established':False,'complete_high_level_java_kotlin_source':False,
                  'large_tables_or_apk_members_extracted':False,'raw_zip_or_app_inputs_modified':False,
                  'all_source_zip_readers_closed_on_return':True}
        write('independent-source-review.json',report)
    assert file_identity(ZIP) == ARCHIVE
    (OUT / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:report[k] for k in ('status','archive_member_count','all16_gate_logs_match_recorded_hashes',
        'all22_fresh_report_hashes_verified','source_input_files','actual_host_cases','actual_methods','actual_ui_controls',
        'fresh_candidate_equals_committed_candidate_identity','all_source_zip_readers_closed_on_return')},indent=2))


if __name__=='__main__':
    main()
