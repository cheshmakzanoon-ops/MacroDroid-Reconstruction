#!/usr/bin/env python3
"""Measure offline workflow input, syntax, APK and owned-cleanup controls."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import yaml
import prepare_normal_journey as preparation


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    workspace, output = args.workspace.resolve(), args.output.resolve()
    home = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'OFFLINE_VALIDATION_RUNNING', 'passed': False, 'android_executed': False,
              'commands': [], 'checks': [], 'started_utc': datetime.now(timezone.utc).isoformat()}
    root = output / 'private-inputs'
    root.mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'GITHUB_WORKSPACE': str(root),
           'GITHUB_SHA': 'offline-control-no-git-or-android-execution'}
    def execute(label, argv, *, cwd=root, extra=None, timeout=60):
        folder = output / 'commands' / label
        folder.mkdir(parents=True, exist_ok=False)
        started = time.monotonic()
        timed_out = False
        with (folder / 'stdout.txt').open('wb') as out, (folder / 'stderr.txt').open('wb') as err:
            try:
                process = subprocess.run(argv, cwd=cwd, env={**env, **(extra or {})},
                                         stdout=out, stderr=err, timeout=timeout)
                code = process.returncode
            except subprocess.TimeoutExpired:
                code, timed_out = 124, True
        row = {'label': label, 'argv': argv, 'cwd': str(cwd), 'exit_code': code, 'timed_out': timed_out,
               'seconds': round(time.monotonic() - started, 6), 'android_executed': False}
        save(folder / 'command.json', row)
        report['commands'].append(row)
        return row
    def source(name):
        for package, origin in [
                (preparation.GUARD, workspace / 'trigger-catalog-forward/checkpoints/04-chronology-host-success'),
                (preparation.ANIMATION, workspace / 'animation-diagnostic/checkpoints/01-normal-animation-source'),
                (preparation.PACKAGE, home)]:
            if name.startswith(package + '/'):
                return origin / name[len(package) + 1:]
        if name == preparation.WORKFLOW:
            return home / name
        return workspace / 'MacroDroid-Reconstruction' / name
    try:
        workflow = home / preparation.WORKFLOW
        report['workflow_sha256'] = preparation.identity(workflow)['sha256']
        parsed = yaml.load(workflow.read_text(), Loader=yaml.BaseLoader)
        job = parsed['jobs']['editor-normal-animation']
        steps = job['steps']
        if parsed['permissions'] != {'contents': 'read'} or job['timeout-minutes'] != '75':
            raise ValueError('Workflow permission or timeout differs')
        if parsed['on'] != {'push': {'branches': ['main'], 'paths': [preparation.WORKFLOW,
                         preparation.PACKAGE + '/**']}, 'workflow_dispatch': ''}:
            raise ValueError('Unexpected workflow trigger scope')
        if (steps[-1].get('if') != 'always()' or steps[-1]['with']['path'] != 'ci-normal-animation/'
                or steps[-1]['with']['include-hidden-files'] != 'true'
                or '--disable-animations' in workflow.read_text()
                or 'trigger_category_journey.py"' in workflow.read_text()):
            raise ValueError('Diagnostic scope or complete evidence preservation changed')
        if [step['uses'] for step in steps if 'uses' in step] != [
                'actions/checkout@11d5960a326750d5838078e36cf38b85af677262',
                'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02']:
            raise ValueError('Pinned actions changed')
        for number, step in enumerate(steps):
            if 'run' not in step:
                continue
            path = output / f'step-{number:02}.sh'
            path.write_text(step['run'])
            if execute(f'bash-syntax-{number:02}', ['bash', '-n', str(path)])['exit_code']:
                raise ValueError('Invalid shell syntax')
        names = set(preparation.PINS)
        for package in [preparation.GUARD, preparation.ANIMATION]:
            checkpoint = json.loads(source(package + '/checkpoint.json').read_text())
            names.update(package + '/' + row['path'] for row in checkpoint['files'])
        guard_inputs = json.loads(source(preparation.GUARD + '/reports/inputs-before.json').read_text())
        names.update(name for name in guard_inputs if name.endswith('/evidence.zip'))
        names.update([preparation.WORKFLOW, preparation.PACKAGE + '/prepare_normal_journey.py',
                      preparation.PACKAGE + '/verify_normal_journey.py'])
        inputs = []
        for name in sorted(names):
            original, target = source(name), root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            expected = preparation.identity(original)
            if preparation.identity(target) != expected:
                raise ValueError('Input copy changed')
            inputs.append({'path': name, 'source': str(original), **expected})
        save(output / 'inputs-before.json', inputs)
        row = execute('exact-frozen-preflight', ['bash', str(output / 'step-01.sh')])
        if row['exit_code']:
            raise ValueError('Exact real input preflight did not pass')
        clean = json.loads((root / 'ci-normal-animation/input-preflight.json').read_text())
        if not clean['passed']:
            raise ValueError('Input report disagrees')
        report['prepared_input_copies'] = len(clean['files'])
        report['checks'].append('Real preflight copied every declared input, including hidden workflow and exact reviewed-source dependencies')

        mutations = [
            ('changed-original-manifest', 'vendor/original/manifest.json', 'bytes'),
            ('changed-active-manifest', 'artifacts/current/manifest.json', 'bytes'),
            ('changed-chronology-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/capture_chronology.py', 'bytes'),
            ('changed-animation-helper', preparation.ANIMATION + '/enable_normal_animations.py', 'bytes'),
            ('symlinked-runtime-input', 'tools/android/runtime_job.py', 'symlink'),
            ('changed-reviewed-finalizer', preparation.PACKAGE + '/verify_normal_journey.py', 'bytes'),
        ]
        for label, name, mode in mutations:
            case = output / 'input-faults' / label
            case.mkdir(parents=True)
            for entry in inputs:
                target = case / entry['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(root / entry['path'], target)
            path = case / name
            raw = path.read_bytes()
            path.unlink()
            if mode == 'bytes':
                path.write_bytes(raw + b'\nDELIBERATE_OFFLINE_INPUT_FAULT\n')
            else:
                path.symlink_to(root / name)
            row = execute(label, ['bash', str(output / 'step-01.sh')], cwd=case,
                          extra={'GITHUB_WORKSPACE': str(case)})
            if row['exit_code'] == 0:
                raise ValueError('Deliberate input fault was accepted: ' + label)
            report['checks'].append(label + ': rejected')
        row = execute('existing-output', ['bash', str(output / 'step-01.sh')])
        if row['exit_code'] == 0:
            raise ValueError('Existing evidence root was reused')

        # Exact already-published APKs are linked for read-only offline inspection;
        # no Android installation or extra signed build is performed.
        runtime_inputs = [
            (workspace / 'recovered/automation android app', 'workspace/artifacts/' + preparation.APKS[0][1]),
            (workspace / 'current/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk', 'workspace/artifacts/' + preparation.APKS[1][1]),
            (workspace / 'current/MacroDroid_v9/tools/prebuilt/linux/aapt2', 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2'),
        ]
        runtime_before = []
        for original, relative in runtime_inputs:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(original, target)
            runtime_before.append({'source': str(original), 'path': relative, **preparation.identity(original)})
        save(output / 'runtime-inputs-before.json', runtime_before)
        row = execute('exact-offline-apk-preflight', [sys.executable, str(home / 'prepare_normal_journey.py'),
            '--root', str(root), '--output', str(root / 'ci-normal-animation'), '--materialized'], timeout=120)
        if row['exit_code']:
            raise ValueError('Exact offline APK and AAPT2 inspection did not pass')
        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))
        for index, script in enumerate(host.splitlines()[1:]):
            row = execute('packaged-host-controls-' + str(index), ['bash', '-o', 'pipefail', '-c', script], timeout=300)
            if row['exit_code']:
                raise ValueError('Packaged host controls failed')
        runtime = next(step['run'] for step in steps if step['name'].startswith('Observe the same ten'))
        start = runtime.index('cleanup_normal_runtime() {')
        stop = runtime.index("trap 'exit 143' TERM") + len("trap 'exit 143' TERM")
        cleanup = runtime[start:stop]
        for label, step_status, service_status in [('clean', 0, 0), ('failed-journey', 7, 0), ('failed-service', 0, 5)]:
            case = output / 'cleanup-controls' / label
            queue = case / 'ci-normal-animation/environment/queue'
            queue.mkdir(parents=True)
            adb = case / 'tooling/macrodroid-normal-animation-tooling/android/platform-tools/adb'
            adb.parent.mkdir(parents=True)
            adb.write_text('#!/bin/sh\nprintf "SIMULATED OFFLINE DIAGNOSTIC ONLY\\n"\nexit 0\n')
            adb.chmod(0o755)
            script = output / ('cleanup-' + label + '.sh')
            script.write_text('set -euo pipefail\n' +
                "bash -c 'for ((n=0;n<200;n++)); do if test -e ci-normal-animation/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ " + str(service_status) + ' &\n' +
                'normal_service_pid=$!\n' + cleanup + '\nexit ' + str(step_status) + '\n')
            row = execute('owned-cleanup-' + label, ['bash', str(script)], cwd=case,
                          extra={'RUNNER_TEMP': str(case / 'tooling')}, timeout=10)
            expected = step_status or (1 if service_status else 0)
            value = json.loads((case / 'ci-normal-animation/runtime-cleanup.json').read_text())
            if (row['exit_code'] != expected or not (queue / 'STOP').is_file()
                    or value['service_cleanup_confirmed'] is not (service_status == 0)):
                raise ValueError('Owned cleanup status or evidence mismatch')
        for entry in inputs + runtime_before:
            if preparation.identity(Path(entry['source'])) != {key: entry[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Baseline input changed during validation: ' + entry['source'])
        if preparation.identity(workflow)['sha256'] != report['workflow_sha256']:
            raise ValueError('Workflow changed during validation')
        report.update(status='OFFLINE_NORMAL_ANIMATION_WORKFLOW_VALIDATED', passed=True,
                      source_apks_and_preserved_tool_bytes_unchanged=True)
    except Exception as error:
        report.update(status='OFFLINE_NORMAL_ANIMATION_WORKFLOW_REJECTED', reason=type(error).__name__ + ': ' + str(error))
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
