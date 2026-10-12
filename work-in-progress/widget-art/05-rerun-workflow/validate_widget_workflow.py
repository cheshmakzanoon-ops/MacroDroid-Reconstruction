#!/usr/bin/env python3
"""Run only offline workflow input/cleanup controls and packaged host tests."""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

import yaml


HERE = Path(__file__).resolve().parent
REPOSITORY = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
WORKFLOW = HERE / '.github/workflows/widget-method-probe.yml'
PROBE = 'work-in-progress/widget-art/04-avd-parser-fix'
FROZEN_PROBE = HERE.parent / 'checkpoints/04-avd-parser-fix'
BASELINES = [
    '.github/workflows/widget-method-probe.yml',
    '.github/workflows/editor-journey.yml', 'scripts/assemble_artifact.py',
    'tools/android/bootstrap_android_runtime.py', 'tools/android/android-toolchain-pins.json',
    'tools/android/android_runtime_service.py', 'tools/android/runtime_job.py',
    'tools/android/wait_android_ready.py', 'tools/android/test_download_retry.py',
    'vendor/original/manifest.json',
    'work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json',
    PROBE + '/checkpoint.json',
]


def input_source(name: str) -> Path:
    if name.startswith(PROBE + '/'):
        return FROZEN_PROBE / name.removeprefix(PROBE + '/')
    return REPOSITORY / name


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def command(output: Path, argv: list[str], *, cwd: Path, env: dict, timeout: int = 60) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    with (output / 'stdout.txt').open('wb') as out, (output / 'stderr.txt').open('wb') as err:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=err, timeout=timeout)
    row = {'argv': argv, 'cwd': str(cwd), 'returncode': result.returncode,
           'elapsed_seconds': round(time.monotonic() - started, 6), 'android_executed': False}
    save(output / 'command.json', row)
    return row


def main() -> None:
    output = HERE / 'reports/validation-01'
    output.mkdir(parents=True, exist_ok=False)
    report = {'scope': 'Offline YAML/bash parsing, real pinned-input rejection and simulated owned-service cleanup; all ADB responses in packaged host tests are simulated.',
              'android_executed': False, 'passed': False, 'workflow_sha256': digest(WORKFLOW),
              'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'commands': [], 'checks': []}
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    temporary = Path(tempfile.mkdtemp(prefix='widget-workflow-offline-'))
    try:
        workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
        if workflow['on'] != {'push': {'branches': ['main'], 'paths': [
            '.github/workflows/widget-method-probe.yml', PROBE + '/**']}, 'workflow_dispatch': ''}:
            raise RuntimeError('Workflow trigger scope changed')
        job = workflow['jobs']['widget-method-probe']
        steps = job['steps']
        actions = [s['uses'] for s in steps if 'uses' in s]
        if actions != ['actions/checkout@11d5960a326750d5838078e36cf38b85af677262',
                       'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02']:
            raise RuntimeError('Action pins changed')
        if steps[-1].get('if') != 'always()' or steps[-1]['with']['path'] != 'ci-widget-method/':
            raise RuntimeError('Failure artifact preservation missing')
        if 'materialize_v9.py' in WORKFLOW.read_text() or 'artifacts/current/manifest.json' in WORKFLOW.read_text():
            raise RuntimeError('Unrelated project or active APK materialization')
        report['checks'].append('Exact triggers, pinned actions, always-artifact and two-artifact-only scope')
        for index, step in enumerate(steps):
            if 'run' in step:
                script = output / ('step-%02d.sh' % index)
                script.write_text(step['run'])
                row = command(output / ('bash-syntax-%02d' % index), ['bash', '-n', str(script)], cwd=HERE, env=env)
                report['commands'].append(row)
                if row['returncode'] != 0:
                    raise RuntimeError('Bash syntax failed')

        checkpoint = json.loads((FROZEN_PROBE / 'checkpoint.json').read_text())
        names = BASELINES + [PROBE + '/' + r['path'] for r in checkpoint['files']]
        snapshots = []
        seed = temporary / 'pinned-seed'
        for name in names:
            source, target = input_source(name), seed / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            if digest(source) != digest(target):
                raise RuntimeError('Baseline copy changed')
            snapshots.append({'path': name, 'source': str(source.resolve()),
                'bytes': source.stat().st_size, 'sha256': digest(source)})
        target = seed / '.github/workflows/widget-method-probe.yml'
        shutil.copyfile(WORKFLOW, target)
        save(HERE / 'baseline-inputs.json', {'scope': 'Exact read-only existing repository inputs plus the frozen reviewed corrected wrapper package; no active workflow/APK mutation.',
            'reference_workflow': '.github/workflows/editor-journey.yml', 'files': snapshots,
            'baseline_workflow_sha256': digest(REPOSITORY / '.github/workflows/widget-method-probe.yml'),
            'new_workflow': {'path': '.github/workflows/widget-method-probe.yml', 'sha256': digest(WORKFLOW)}})
        mutations = [
            ('clean-inputs', None, None),
            ('changed-original-manifest', 'vendor/original/manifest.json', 'bytes'),
            ('changed-candidate-manifest', 'work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json', 'bytes'),
            ('changed-bootstrap', 'tools/android/bootstrap_android_runtime.py', 'bytes'),
            ('changed-runtime-service', 'tools/android/android_runtime_service.py', 'bytes'),
            ('changed-frozen-checkpoint', PROBE + '/checkpoint.json', 'bytes'),
            ('changed-frozen-wrapper', PROBE + '/android_widget_method_probe.py', 'bytes'),
            ('changed-frozen-dex', PROBE + '/probes/widget-method-probe.dex', 'bytes'),
            ('symlinked-runtime-script', 'tools/android/runtime_job.py', 'symlink'),
            ('existing-output', None, 'existing-output'),
        ]
        for label, name, mode in mutations:
            root = temporary / label
            shutil.copytree(seed, root)
            if mode == 'bytes':
                path = root / name
                path.write_bytes(path.read_bytes() + b'\nDELIBERATE_OFFLINE_INPUT_FAULT\n')
            elif mode == 'symlink':
                path = root / name
                data = path.read_bytes()
                outside = temporary / 'runtime-job-symlink-target.py'
                outside.write_bytes(data)
                path.unlink()
                path.symlink_to(outside)
            elif mode == 'existing-output':
                (root / 'ci-widget-method').mkdir()
            local_env = {**env, 'GITHUB_WORKSPACE': str(root), 'GITHUB_SHA': 'offline-control-no-git-execution'}
            row = command(output / label, ['bash', str(output / 'step-01.sh')], cwd=root, env=local_env)
            report['commands'].append(row)
            copied_output = output / label / 'observed-ci-output'
            shutil.copytree(root / 'ci-widget-method', copied_output)
            expected_pass = label == 'clean-inputs'
            if (row['returncode'] == 0) != expected_pass:
                raise RuntimeError('Preflight control outcome mismatch: ' + label)
            result = root / 'ci-widget-method/input-preflight.json'
            if mode != 'existing-output':
                value = json.loads(result.read_text())
                if value['passed'] is not expected_pass:
                    raise RuntimeError('Preflight evidence disagrees: ' + label)
                if expected_pass and len(value['files']) != 19:
                    raise RuntimeError('Preflight omitted bound source files')
            report['checks'].append(label + ': ' + ('passed' if expected_pass else 'rejected'))

        runtime = steps[5]['run']
        start = runtime.index('cleanup_widget_runtime() {')
        end = runtime.index("trap 'exit 143' TERM") + len("trap 'exit 143' TERM")
        cleanup = runtime[start:end]
        cleanup_cases = [('clean-service', 0, 0, False), ('failed-probe-status-retained', 7, 0, False),
                         ('failed-service-status', 0, 5, False), ('failed-cleanup-evidence', 0, 0, True)]
        for label, original_status, service_status, evidence_failure in cleanup_cases:
            root = temporary / label
            queue = root / 'ci-widget-method/environment/queue'
            queue.mkdir(parents=True)
            adb = root / 'tooling/macrodroid-widget-tooling/android/platform-tools/adb'
            adb.parent.mkdir(parents=True)
            adb.write_text('#!/bin/sh\nprintf "OFFLINE SIMULATED DIAGNOSTIC ONLY\\n"\nexit 0\n')
            adb.chmod(0o755)
            if evidence_failure:
                (root / 'ci-widget-method/runtime-cleanup.json').mkdir()
            script = output / (label + '.sh')
            script.write_text('set -euo pipefail\n' +
                "bash -c 'for ((n=0;n<200;n++)); do if test -e ci-widget-method/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ " + str(service_status) + ' &\n' +
                'widget_service_pid=$!\n' + cleanup + '\nexit ' + str(original_status) + '\n')
            row = command(output / label, ['bash', str(script)], cwd=root, env={**env, 'RUNNER_TEMP': str(root / 'tooling')}, timeout=10)
            report['commands'].append(row)
            shutil.copytree(root / 'ci-widget-method', output / label / 'observed-ci-output')
            expected_code = original_status or (1 if service_status or evidence_failure else 0)
            if row['returncode'] != expected_code or not (queue / 'STOP').is_file():
                raise RuntimeError('Owned cleanup control mismatch: ' + label)
            if not evidence_failure:
                value = json.loads((root / 'ci-widget-method/runtime-cleanup.json').read_text())
                if value['service_cleanup_confirmed'] is not (service_status == 0):
                    raise RuntimeError('Cleanup evidence overclaims: ' + label)
            report['checks'].append(label + ': correct owned STOP, return code and retained evidence')

        host = temporary / 'host-tests'
        shutil.copytree(seed, host)
        host_env = {**env, 'WIDGET_PROBE_CONTROL_EVIDENCE': str(output / 'packaged-wrapper-control-evidence')}
        for label, argv, count in [
            ('download-controls', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tools/android', '-p', 'test_download_retry.py', '-v'], 6),
            ('packaged-wrapper-controls', [sys.executable, '-m', 'unittest', 'discover', '-s', PROBE, '-p', 'test_android_widget_method_probe.py', '-v'], 31),
        ]:
            row = command(output / label, argv, cwd=host, env=host_env, timeout=120)
            report['commands'].append(row)
            stderr = (output / label / 'stderr.txt').read_text()
            if row['returncode'] != 0 or f'Ran {count} tests in ' not in stderr or not stderr.rstrip().endswith('OK'):
                raise RuntimeError('Exact packaged host controls did not pass: ' + label)
            report['checks'].append(str(count) + ' actual ' + label + ' passed; no Android execution')
        if digest(WORKFLOW) != report['workflow_sha256']:
            raise RuntimeError('Workflow changed during validation')
        for item in snapshots:
            if digest(input_source(item['path'])) != item['sha256']:
                raise RuntimeError('Repository baseline changed during validation')
        report['passed'] = True
    except Exception as error:
        report['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['finished_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save(output / 'result.json', report)
        shutil.rmtree(temporary)
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
