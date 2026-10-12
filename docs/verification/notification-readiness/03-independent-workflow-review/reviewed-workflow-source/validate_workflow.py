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
import prepare_trigger_journey as preparation


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--guard', type=Path, required=True)
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
                (preparation.GUARD, args.guard.resolve()),
                (preparation.ANIMATION, workspace / 'trigger-catalog-forward/checkpoints/07-zero-animation-source'),
                (preparation.PACKAGE, home)]:
            if name.startswith(package + '/'):
                return origin / name[len(package) + 1:]
        if name == preparation.WORKFLOW:
            return home / name
        if name == preparation.APKS[1][0]:
            return workspace / 'combined-recovery/checkpoints/05-full-acceptance/apk/manifest.json'
        return workspace / 'MacroDroid-Reconstruction' / name
    try:
        workflow = home / preparation.WORKFLOW
        report['workflow_sha256'] = preparation.identity(workflow)['sha256']
        parsed = yaml.load(workflow.read_text(), Loader=yaml.BaseLoader)
        job = parsed['jobs']['editor-day-time-readiness']
        steps = job['steps']
        if parsed['permissions'] != {'contents': 'read'} or job['timeout-minutes'] != '75':
            raise ValueError('Workflow permission or timeout differs')
        if parsed['on'] != {'push': {'branches': ['main'], 'paths': [preparation.WORKFLOW,
                         preparation.PACKAGE + '/**']}, 'workflow_dispatch': ''}:
            raise ValueError('Unexpected workflow trigger scope')
        if (steps[-1].get('if') != 'always()' or steps[-1]['with']['path'] != 'ci-day-time-readiness/'
                or steps[-1]['with']['include-hidden-files'] != 'true'
                or '--disable-animations' in workflow.read_text()
                or 'day_time_journey.py"' not in workflow.read_text()
                or 'favourite_info_journey.py"' in workflow.read_text()
                or workflow.read_text().count('--observe-notification-readiness') != 1):
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
        names.update([preparation.WORKFLOW, preparation.PACKAGE + '/prepare_trigger_journey.py',
                      preparation.PACKAGE + '/verify_trigger_journey.py'])
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
        clean = json.loads((root / 'ci-day-time-readiness/input-preflight.json').read_text())
        if not clean['passed']:
            raise ValueError('Input report disagrees')
        report['prepared_input_copies'] = len(clean['files'])
        report['checks'].append('Real preflight copied every declared input, including hidden workflow and exact reviewed-source dependencies')

        mutations = [
            ('changed-original-manifest', 'vendor/original/manifest.json', 'bytes'),
            ('changed-active-manifest', 'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json', 'bytes'),
            ('changed-chronology-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/capture_chronology.py', 'bytes'),
            ('changed-animation-helper', preparation.ANIMATION + '/enable_still_animations.py', 'bytes'),
            ('changed-readiness-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/notification_readiness.py', 'bytes'),
            ('symlinked-runtime-input', 'tools/android/runtime_job.py', 'symlink'),
            ('changed-reviewed-finalizer', preparation.PACKAGE + '/verify_trigger_journey.py', 'bytes'),
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

        # Exact frozen APKs are linked for read-only offline inspection;
        # no Android installation or extra signed build is performed.
        runtime_inputs = [
            (workspace / 'recovered/automation android app', 'workspace/artifacts/' + preparation.APKS[0][1]),
            (Path(json.loads((workspace / 'combined-recovery/reports/05-full-acceptance/result.json').read_text())['project']) / 'dist/MacroDroid-5.67.8-v9-hybrid.apk', 'workspace/artifacts/' + preparation.APKS[1][1]),
            (workspace / 'current/MacroDroid_v9/tools/prebuilt/linux/aapt2', 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2'),
        ]
        runtime_before = []
        for original, relative in runtime_inputs:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if original.stat().st_dev == root.stat().st_dev:
                os.link(original, target)
            else:
                shutil.copy2(original, target)
            if preparation.identity(target) != preparation.identity(original):
                raise ValueError('Exact offline runtime input transport changed')
            runtime_before.append({'source': str(original), 'path': relative, **preparation.identity(original)})
        save(output / 'runtime-inputs-before.json', runtime_before)
        row = execute('exact-offline-apk-preflight', [sys.executable, str(home / 'prepare_trigger_journey.py'),
            '--root', str(root), '--output', str(root / 'ci-day-time-readiness'), '--materialized'], timeout=120)
        if row['exit_code']:
            raise ValueError('Exact offline APK and AAPT2 inspection did not pass')

        # These are bounded report/data mutations, using the real materialized
        # and final verification entry points. Large, unchanged APK/fixture
        # inputs are hardlinked; every mutated file is detached first.
        inventory_cases = [
            ('omit-runtime-row', 'omit', False, False),
            ('empty-inventory', 'empty', False, False),
            ('duplicate-row', 'duplicate', False, False),
            ('reorder-rows', 'reorder', False, False),
            ('extra-row', 'extra', False, False),
            ('changed-source-and-copy-retained', 'retain', True, True),
            ('changed-source-and-copy-omitted', 'omit', True, True),
            ('changed-source-and-copy-empty', 'empty', True, True),
            ('changed-source-and-copy-rehashed', 'rehash', True, True),
            ('changed-copy-retained', 'retain', False, True),
            ('changed-copy-rehashed', 'rehash', False, True),
            ('omit-reviewed-copy-role', 'omit-reviewed', False, False),
            ('legacy-readiness-schema', 'schema-three', False, False),
            ('boolean-readiness-schema', 'schema-bool', False, False),
            ('missing-readiness-policy-pin', 'omit-policy', False, False),
            ('changed-readiness-policy-pin', 'changed-policy', False, False),
        ]
        inventory_names = {entry['path'] for entry in inputs + runtime_before}
        inventory_names.update('ci-day-time-readiness/' + entry['copy'] for entry in clean['files'])
        inventory_names.add('ci-day-time-readiness/input-preflight.json')
        fault_name = 'tools/android/bootstrap_android_runtime.py'
        fault_copy = next(entry['copy'] for entry in clean['files'] if entry['path'] == fault_name)
        fault_bytes = (root / fault_name).read_bytes() + b'\n# DELIBERATE OFFLINE INVENTORY MUTATION\n'
        def replace_bytes(path, raw):
            path.unlink()
            path.write_bytes(raw)
        for label, mode, change_source, change_copy in inventory_cases:
            case = output / 'inventory-faults' / label
            case.mkdir(parents=True)
            for name in sorted(inventory_names):
                target = case / name
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(root / name, target)
            case_output = case / 'ci-day-time-readiness'
            declared = json.loads(json.dumps(clean))
            if change_source:
                replace_bytes(case / fault_name, fault_bytes)
            if change_copy:
                replace_bytes(case_output / fault_copy, fault_bytes)
            if mode == 'omit':
                declared['files'] = [entry for entry in declared['files'] if entry['path'] != fault_name]
            elif mode == 'empty':
                declared['files'] = []
            elif mode == 'duplicate':
                declared['files'].append(dict(declared['files'][0]))
            elif mode == 'reorder':
                declared['files'][0], declared['files'][1] = declared['files'][1], declared['files'][0]
            elif mode == 'extra':
                declared['files'].append({**declared['files'][0], 'copy': 'invented-extra-role'})
            elif mode == 'rehash':
                for entry in declared['files']:
                    if entry['path'] == fault_name:
                        entry.update(bytes=len(fault_bytes), sha256=hashlib.sha256(fault_bytes).hexdigest())
            elif mode == 'schema-three':
                declared['requested_report_schema'] = 3
            elif mode == 'schema-bool':
                declared['requested_report_schema'] = True
            elif mode == 'omit-policy':
                del declared['notification_readiness_policy_sha256']
            elif mode == 'changed-policy':
                declared['notification_readiness_policy_sha256'] = '0' * 64
            elif mode == 'omit-reviewed':
                role = next(entry['copy'] for entry in declared['files'] if entry['copy'].startswith('reviewed-source/'))
                declared['files'] = [entry for entry in declared['files'] if entry['copy'] != role]
            replace_bytes(case_output / 'input-preflight.json', (json.dumps(declared, indent=2) + '\n').encode())
            outcomes = []
            for phase, script, suffix, report_name in [
                    ('materialized', 'prepare_trigger_journey.py', ['--materialized'], 'materialized-inputs.json'),
                    ('final', 'verify_trigger_journey.py', [], 'day-time-readiness-verification.json')]:
                command = execute('inventory-' + label + '-' + phase,
                    [sys.executable, str(home / script), '--root', str(case), '--output', str(case_output)] + suffix)
                value = json.loads((case_output / report_name).read_text())
                reason = value.get('reason', '')
                if (command['exit_code'] == 0 or not any(message in reason for message in [
                        'Pinned input changed:', 'not the complete independently pinned inventory',
                        'Prepared input changed before execution:',
                        'Frozen diagnostic plan or preparation scope changed'])):
                    raise ValueError('Inventory fault was not rejected at the shared input boundary: ' + label + '/' + phase)
                outcomes.append({'phase': phase, 'exit_code': command['exit_code'], 'reason': reason})
            if (case_output / 'reviewed-source/project/tools/prebuilt/linux/aapt2').exists():
                raise ValueError('Fault reached the materialized execution boundary: ' + label)
            report['checks'].append({'inventory_fault': label, 'outcomes': outcomes,
                                     'rejected_before_copied_code_or_aapt2_execution': True})

        policy_script = output / 'workflow-policy-controls.py'
        policy_script.write_text("import copy\nimport json\nfrom pathlib import Path\nimport sys\nsys.path[:0] = [sys.argv[1], sys.argv[2], sys.argv[3]]\nimport verify_trigger_journey as verifier\nimport notification_readiness as readiness\npositive = {'schema': 5, readiness.POLICY_KEY: copy.deepcopy(readiness.POLICY)}\nverifier.require_notification_policy(positive)\ncontrols = []\nfor label in ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-policy', 'changed-policy']:\n    value = copy.deepcopy(positive)\n    if label == 'legacy-schema':\n        value['schema'] = 3\n    elif label == 'unregistered-schema':\n        value['schema'] = 4\n    elif label == 'boolean-schema':\n        value['schema'] = True\n    elif label == 'missing-policy':\n        del value[readiness.POLICY_KEY]\n    else:\n        value[readiness.POLICY_KEY]['max_seconds'] = 11\n    try:\n        verifier.require_notification_policy(value)\n    except Exception as error:\n        if 'Missing or altered notification readiness policy' not in str(error):\n            raise\n        controls.append({'label': label, 'rejected': True, 'reason': str(error)})\n    else:\n        raise AssertionError('Workflow policy downgrade accepted: ' + label)\nverifier.require_notification_policy(positive)\nresult = {'passed': True, 'android_executed': False, 'scope': 'Workflow-required policy format only; complete raw evidence is independently required by compare', 'positive_and_restore': True, 'negative_controls': controls}\nPath(sys.argv[4]).write_text(json.dumps(result, indent=2) + '\\n')\nprint(json.dumps(result, indent=2))\n")
        policy_result = output / 'workflow-policy-controls.json'
        row = execute('workflow-policy-controls', [sys.executable, '-B', str(policy_script), str(home),
            str(root / 'ci-day-time-readiness/reviewed-source/tools/parity_journeys'),
            str(root / 'ci-day-time-readiness/reviewed-source/project'), str(policy_result)])
        if row['exit_code'] or json.loads(policy_result.read_text()).get('passed') is not True:
            raise ValueError('Workflow readiness policy controls failed')
        report['checks'].append(json.loads(policy_result.read_text()))

        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))
        for index, script in enumerate(host.splitlines()[1:]):
            row = execute('packaged-host-controls-' + str(index), ['bash', '-o', 'pipefail', '-c', script], timeout=300)
            if row['exit_code']:
                raise ValueError('Packaged host controls failed')
        runtime = next(step['run'] for step in steps if step['name'].startswith('Observe the thirteen declared'))
        start = runtime.index('cleanup_trigger_runtime() {')
        stop = runtime.index("trap 'exit 143' TERM") + len("trap 'exit 143' TERM")
        cleanup = runtime[start:stop]
        for label, step_status, service_status in [('clean', 0, 0), ('failed-journey', 7, 0), ('failed-service', 0, 5)]:
            case = output / 'cleanup-controls' / label
            queue = case / 'ci-day-time-readiness/environment/queue'
            queue.mkdir(parents=True)
            adb = case / 'tooling/macrodroid-day-time-readiness-tooling/android/platform-tools/adb'
            adb.parent.mkdir(parents=True)
            adb.write_text('#!/bin/sh\nprintf "SIMULATED OFFLINE DIAGNOSTIC ONLY\\n"\nexit 0\n')
            adb.chmod(0o755)
            script = output / ('cleanup-' + label + '.sh')
            script.write_text('set -euo pipefail\n' +
                "bash -c 'for ((n=0;n<200;n++)); do if test -e ci-day-time-readiness/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ " + str(service_status) + ' &\n' +
                'trigger_service_pid=$!\n' + cleanup + '\nexit ' + str(step_status) + '\n')
            row = execute('owned-cleanup-' + label, ['bash', str(script)], cwd=case,
                          extra={'RUNNER_TEMP': str(case / 'tooling')}, timeout=10)
            expected = step_status or (1 if service_status else 0)
            value = json.loads((case / 'ci-day-time-readiness/runtime-cleanup.json').read_text())
            if (row['exit_code'] != expected or not (queue / 'STOP').is_file()
                    or value['service_cleanup_confirmed'] is not (service_status == 0)):
                raise ValueError('Owned cleanup status or evidence mismatch')
        for entry in inputs + runtime_before:
            if preparation.identity(Path(entry['source'])) != {key: entry[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Baseline input changed during validation: ' + entry['source'])
        if preparation.identity(workflow)['sha256'] != report['workflow_sha256']:
            raise ValueError('Workflow changed during validation')
        report.update(status='OFFLINE_DAY_TIME_READINESS_WORKFLOW_VALIDATED', passed=True,
                      source_apks_and_preserved_tool_bytes_unchanged=True)
    except Exception as error:
        report.update(status='OFFLINE_DAY_TIME_READINESS_WORKFLOW_REJECTED', reason=type(error).__name__ + ': ' + str(error))
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
