#!/usr/bin/env python3
"""Independently verify the exact completed ART05 artifact without executing ADB."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
CAPTURE = ROOT / 'hosted-run-38207925500'
FROZEN = ROOT / 'checkpoints/04-avd-parser-fix'
COMMIT = 'c1a6d71d2e290d16ea3a047d036996f79005883a'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
        'scope': 'Read-only verification of the complete fresh eight-case original/candidate Widget ART artifact.',
        'verification_executed_android_commands': False, 'historical_failed_job_relabelled': False,
        'full_runtime_1_to_1_established': False, 'nonempty_widget_behavior_verified': False,
        'widget_rendering_verified': False}
    output = CAPTURE / 'independent-verification'
    output.mkdir(exist_ok=False)
    try:
        manifest = json.loads((CAPTURE / 'download-manifest.json').read_text())
        if (manifest['run_id'] != 38207925500 or manifest['job_id'] != 114675450663 or
                manifest['head_sha'] != COMMIT or manifest['artifact_id'] != 11728078034):
            raise RuntimeError('Unexpected downloaded job identity')
        archive = CAPTURE / 'artifact.zip'
        if (archive.stat().st_size != 4_778_227 or
                sha(archive) != '6e6124822bb17bf89b75a1683445b67c527d84ea575776bce315aff0e84a2607'):
            raise RuntimeError('Exact GitHub artifact ZIP identity differs')
        result['archive'] = record(archive)
        expected = {row['path']: row for row in manifest['files']}
        if len(expected) != len(manifest['files']) or len(expected) != 7213:
            raise RuntimeError('Duplicate or missing historical artifact member bindings')
        seen = set()
        with zipfile.ZipFile(archive) as stream:
            for member in stream.infolist():
                name = member.filename
                relative = PurePosixPath(name)
                if (relative.is_absolute() or '..' in relative.parts or '\\' in name or
                        name in seen or stat.S_ISLNK(member.external_attr >> 16)):
                    raise RuntimeError('Unsafe or duplicate archive path')
                seen.add(name)
                if member.is_dir():
                    continue
                row = expected.pop(name)
                data = stream.read(member)
                path = CAPTURE / 'extracted' / name
                if (len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256'] or
                        path.is_symlink() or path.read_bytes() != data):
                    raise RuntimeError('Downloaded/extracted evidence differs: ' + name)
        if expected:
            raise RuntimeError('The ZIP omitted bound members')
        result['archive_member_count_verified'] = len(manifest['files'])
        jobs = json.loads((CAPTURE / 'github-jobs.json').read_text())['structuredContent']['jobs']
        if (len(jobs) != 1 or jobs[0]['id'] != 114675450663 or jobs[0]['run_id'] != 38207925500 or
                jobs[0]['status'] != 'completed' or jobs[0]['conclusion'] != 'success' or
                any(step['status'] != 'completed' or step['conclusion'] != 'success' for step in jobs[0]['steps'])):
            raise RuntimeError('The fresh job or one of its steps did not succeed')
        artifacts = json.loads((CAPTURE / 'github-artifacts.json').read_text())['structuredContent']['artifacts']
        artifact = next(row for row in artifacts if row['id'] == 11728078034)
        if (artifact['workflow_run']['head_sha'] != COMMIT or artifact['workflow_run']['id'] != 38207925500 or
                artifact['size_in_bytes'] != result['archive']['bytes'] or
                artifact['digest'] != 'sha256:' + result['archive']['sha256'] or artifact['expired'] is not False):
            raise RuntimeError('GitHub artifact metadata disagrees with downloaded bytes')
        extracted = CAPTURE / 'extracted'
        preflight = json.loads((extracted / 'input-preflight.json').read_text())
        if preflight['passed'] is not True or preflight['github_sha'] != COMMIT or len(preflight['files']) != 19:
            raise RuntimeError('Bound nineteen-file input preflight is absent')
        reviewed = ROOT / 'checkpoints/05-rerun-workflow'
        if sha(reviewed / 'checkpoint.json') != '670bb7a33921547e74460669d940da8cb4f223d17366e28eab7430ac7276c501':
            raise RuntimeError('Reviewed workflow capsule changed')
        baseline = json.loads((reviewed / 'baseline-inputs.json').read_text())
        expected_inputs = {item['path']: (item['bytes'], item['sha256']) for item in baseline['files']
                           if item['path'] != '.github/workflows/editor-journey.yml'}
        actual_workflow = reviewed / '.github/workflows/widget-method-probe.yml'
        expected_inputs['.github/workflows/widget-method-probe.yml'] = (actual_workflow.stat().st_size, sha(actual_workflow))
        names = set()
        for item in preflight['files']:
            path = extracted / 'executed-inputs' / item['path']
            if (item['path'] in names or path.is_symlink() or path.stat().st_size != item['bytes'] or
                    sha(path) != item['sha256'] or item['sha256'] != item['expected_sha256'] or
                    expected_inputs.get(item['path']) != (item['bytes'], item['sha256'])):
                raise RuntimeError('Executed input bytes differ from the observed preflight')
            names.add(item['path'])
        if names != set(expected_inputs):
            raise RuntimeError('Executed input set differs from the reviewed workflow bindings')
        policy = FROZEN / 'android_widget_method_probe.py'
        policy_sha = '4738616dd655fd74832b501b95390ae744c7c6050fbb3d16f17bf78300aec541'
        if sha(policy) != policy_sha or sha(extracted / 'probe/executed-wrapper.py') != policy_sha:
            raise RuntimeError('The executed evidence policy differs from root-reviewed ART04')
        workflow = extracted / 'executed-inputs/.github/workflows/widget-method-probe.yml'
        if sha(workflow) != 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7':
            raise RuntimeError('The actual workflow differs from root-reviewed ART05')
        specification = importlib.util.spec_from_file_location('verified_frozen_widget_policy', policy)
        implementation = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(implementation)
        report_path = extracted / 'probe/probe-result.json'
        before = record(report_path)
        report = json.loads(report_path.read_text())
        if report['status'] != 'ART_WIDGET_CASES_VERIFIED' or report['execution_backend'] != 'adb-android-runtime':
            raise RuntimeError('Actual final evidence guard did not accept real ART execution')
        implementation.verify_result(extracted / 'probe', report, serial='emulator-5560')
        if len(report['commands']) != 60:
            raise RuntimeError('The full expected device command sequence is absent')
        avd = extracted / 'probe/010-avd-name.stdout.txt'
        if avd.read_bytes() != b'MacroDroid_API35_Disposable\r\nOK\r\n':
            raise RuntimeError('Fresh job did not exercise the actual complete CRLF AVD form')
        results = {}
        for variant in ('original', 'candidate'):
            execution = report['executions'][variant]
            command = execution['command']
            stdout = extracted / 'probe' / command['stdout']['path']
            stderr = extracted / 'probe' / command['stderr']['path']
            if (command['returncode'] != 0 or command['timed_out'] is not False or
                    stdout.read_bytes() != implementation.EXPECTED_STDOUT.encode() or stderr.read_bytes() != b''):
                raise RuntimeError('An exact guest case comparison failed')
            results[variant] = {'guest_argv': execution['guest_argv'], 'returncode': command['returncode'],
                'seconds': command['seconds'], 'host_timeout_seconds': command['timeout_seconds'],
                'stdout': record(stdout), 'stderr': record(stderr), 'cases': execution['completed_case_prefix']}
        response = json.loads((extracted / 'environment/queue/responses/widget-method-art.json').read_text())
        if response['exit_code'] != 0 or response['timeout_s'] != 720.0:
            raise RuntimeError('Bound service job did not return success')
        cleanup = json.loads((extracted / 'runtime-cleanup.json').read_text())
        for field in ('probe_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
                      'bounded_service_wait_exit_code', 'owned_service_exit_code'):
            if cleanup[field] != '0':
                raise RuntimeError('Service/probe lifecycle operation failed: ' + field)
        if cleanup['service_cleanup_confirmed'] is not True:
            raise RuntimeError('Owned runtime service cleanup was not observed')
        for name, count in (('wrapper-tests.log', 31), ('download-tests.log', 6)):
            text = (extracted / name).read_text()
            if f'Ran {count} tests in ' not in text or not text.rstrip().endswith('OK'):
                raise RuntimeError('Packaged controls did not pass in the actual job')
        if record(report_path) != before:
            raise RuntimeError('Actual report changed during read-only verification')
        result.update(status='FRESH_ART_EIGHT_CASE_COMPARISON_AND_COMPLETE_EVIDENCE_VERIFIED',
            passed=True, run_id=38207925500, job_id=114675450663, commit=COMMIT,
            actual_android_runtime_executed=True, both_eight_case_sets_passed=True,
            exact_stdout_equal=True, strict_guest_diagnostics_passed=True,
            initial_and_final_avd_crlf_checks_passed=True, command_count_verified=60,
            raw_command_streams_verified=120, input_preflight_files_verified=19,
            reviewed_policy_sha256=policy_sha, original_actual_report=before,
            executions=results, apk_and_probe_inputs=report['inputs_before'],
            binary_identities=report['binaries_before'], device_environment=report['environment-before'],
            before_after_device_input_identities_equal=all(
                report['device_inputs_before'][name][field] == report['device_inputs_after'][name][field]
                for name in ('probe', 'original', 'candidate') for field in ('path', 'sha256')),
            guest_owned_cleanup_complete=report['cleanup_complete'], service_cleanup=cleanup)
    except Exception as error:
        result['status'] = 'INDEPENDENT_VERIFICATION_FAILED'
        result['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
