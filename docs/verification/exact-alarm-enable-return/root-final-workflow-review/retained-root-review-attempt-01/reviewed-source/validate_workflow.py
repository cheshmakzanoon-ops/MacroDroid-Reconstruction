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
    parser.add_argument('--candidate-manifest', type=Path, required=True)
    parser.add_argument('--candidate-apk', type=Path, required=True)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--original-apk', type=Path, required=True)
    parser.add_argument('--aapt2', type=Path, required=True)
    args = parser.parse_args()
    workspace, output = args.workspace.resolve(), args.output.resolve()
    home = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'OFFLINE_VALIDATION_RUNNING', 'passed': False, 'android_executed': False,
              'commands': [], 'checks': [], 'started_utc': datetime.now(timezone.utc).isoformat()}
    root = output / 'private-inputs'
    root.mkdir()
    temporary = output / 'host-temporary'; temporary.mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'GITHUB_WORKSPACE': str(root),
           'GITHUB_SHA': 'offline-control-no-git-or-android-execution', 'TMPDIR': str(temporary)}
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
        if name == preparation.WORKFLOW:
            return home / name
        if name.startswith(preparation.PACKAGE + '/'):
            return home / name[len(preparation.PACKAGE) + 1:]
        return args.checkout.resolve() / name
    try:
        workflow = home / preparation.WORKFLOW
        report['workflow_sha256'] = preparation.identity(workflow)['sha256']
        own_before = {name: preparation.identity(home / name) for name in [
            preparation.WORKFLOW, 'prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py']}
        report['helpers_before'] = own_before
        parsed = yaml.load(workflow.read_text(), Loader=yaml.BaseLoader)
        job = parsed['jobs']['editor-exact-alarm-enable-return']
        steps = job['steps']
        if parsed['permissions'] != {'contents': 'read'} or job['timeout-minutes'] != '75':
            raise ValueError('Workflow permission or timeout differs')
        if parsed['on'] != {'push': {'branches': ['main'], 'paths': [preparation.WORKFLOW,
                         preparation.PACKAGE + '/**']}, 'workflow_dispatch': ''}:
            raise ValueError('Unexpected workflow trigger scope')
        if (steps[-1].get('if') != 'always()' or steps[-1]['with']['path'] != 'ci-exact-alarm-enable-return/'
                or steps[-1]['with']['include-hidden-files'] != 'true'
                or '--disable-animations' in workflow.read_text()
                or 'exact_alarm_enable_return.py"' not in workflow.read_text()
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
        # A literal checkout contains the two committed parts, not their logical archive.
        names.remove(preparation.GUARD_ARCHIVE)
        if (args.checkout.resolve() / preparation.GUARD_ARCHIVE).exists():
            raise ValueError('Offline literal checkout unexpectedly contains a logical archive')
        inputs = []
        for name in sorted(names):
            original, target = source(name), root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, target)
            expected = preparation.identity(original)
            if preparation.identity(target) != expected:
                raise ValueError('Input copy changed')
            inputs.append({'path': name, 'source': str(original), **expected})
        save(output / 'inputs-before.json', inputs)
        row = execute('exact-frozen-preflight', ['bash', str(output / 'step-01.sh')])
        if row['exit_code']:
            raise ValueError('Exact real input preflight did not pass')
        clean = json.loads((root / 'ci-exact-alarm-enable-return/input-preflight.json').read_text())
        if not clean['passed']:
            raise ValueError('Input report disagrees')
        report['prepared_input_copies'] = len(clean['files'])
        if (clean['guard_archive_preparation']['action'] != 'ASSEMBLED_MISSING_LOGICAL_ARCHIVE'
                or clean['guard_archive_preparation']['verified']['verified_members'] != 353):
            raise ValueError('Literal multipart checkout was not fully assembled and verified')
        report['multipart_preparation'] = clean['guard_archive_preparation']
        case_input_names = {entry['path'] for entry in inputs} | {preparation.GUARD_ARCHIVE}
        report['checks'].append('Real preflight copied every declared input, including hidden workflow and exact reviewed-source dependencies')

        mutations = [
            ('changed-original-manifest', 'vendor/original/manifest.json', 'bytes'),
            ('changed-active-manifest', 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json', 'bytes'),
            ('changed-chronology-guard', preparation.GUARD + '/source/tools/parity_journeys/capture_chronology.py', 'bytes'),
            ('changed-animation-helper', preparation.ANIMATION + '/enable_still_animations.py', 'bytes'),
            ('changed-readiness-guard', preparation.GUARD + '/source/tools/parity_journeys/exact_alarm_enable_return_readiness.py', 'bytes'),
            ('changed-navigation-guard', preparation.GUARD + '/source/tools/parity_journeys/exact_alarm_enable_return.py', 'bytes'),
            ('changed-observed-dialog', preparation.GUARD + '/source/tools/parity_journeys/fixtures/exact-alarm/dialog-contract.json', 'bytes'),
            ('symlinked-runtime-input', 'tools/android/runtime_job.py', 'symlink'),
            ('changed-reviewed-finalizer', preparation.PACKAGE + '/verify_trigger_journey.py', 'bytes'),
            ('missing-archive-part-1-with-existing-logical', preparation.GUARD_TRANSPORT[1][0], 'missing'),
            ('missing-archive-part-2-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'missing'),
            ('changed-archive-part-1-with-existing-logical', preparation.GUARD_TRANSPORT[1][0], 'same-size'),
            ('truncated-archive-part-2-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'truncated'),
            ('changed-archive-manifest', preparation.GUARD_TRANSPORT[0][0], 'bytes'),
            ('symlinked-archive-part-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'symlink'),
            ('wrong-existing-logical-archive', preparation.GUARD_ARCHIVE, 'wrong-logical'),
        ]
        for label, name, mode in mutations:
            case = output / 'input-faults' / label
            case.mkdir(parents=True)
            for name_to_copy in sorted(case_input_names):
                target = case / name_to_copy
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(root / name_to_copy, target)
            path = case / name
            raw = path.read_bytes()
            path.unlink()
            if mode == 'bytes':
                path.write_bytes(raw + b'\nDELIBERATE_OFFLINE_INPUT_FAULT\n')
            elif mode == 'missing':
                pass
            elif mode == 'same-size':
                path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            elif mode == 'truncated':
                path.write_bytes(raw[:-1])
            elif mode == 'wrong-logical':
                path.write_bytes(b'DELIBERATE_WRONG_EXISTING_LOGICAL_ARCHIVE\n')
            else:
                path.symlink_to(root / name)
            row = execute(label, ['bash', str(output / 'step-01.sh')], cwd=case,
                          extra={'GITHUB_WORKSPACE': str(case)})
            if row['exit_code'] == 0:
                raise ValueError('Deliberate input fault was accepted: ' + label)
            if label in {entry[0] for entry in mutations[-7:]}:
                failed = json.loads((case / 'ci-exact-alarm-enable-return/input-preflight.json').read_bytes())
                if failed.get('passed') is not False or failed.get('files') != []:
                    raise ValueError('Archive fault reached copied-code preparation: ' + label)
                report['checks'].append({'multipart_fault': label, 'rejected_before_any_copy': True,
                                         'reason': failed.get('reason')})
            else:
                report['checks'].append(label + ': rejected')
        matching = output / 'matching-existing-logical'
        matching.mkdir()
        for name in sorted(case_input_names):
            target = matching / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(root / name, target)
        row = execute('matching-existing-logical-preflight', ['bash', str(output / 'step-01.sh')],
                      cwd=matching, extra={'GITHUB_WORKSPACE': str(matching)})
        existing = json.loads((matching / 'ci-exact-alarm-enable-return/input-preflight.json').read_bytes())
        if (row['exit_code'] or existing.get('passed') is not True
                or existing['guard_archive_preparation']['action'] != 'VERIFIED_EXISTING_LOGICAL_ARCHIVE'
                or existing['files'] != clean['files']):
            raise ValueError('Matching existing logical archive failed full preparation')
        report['checks'].append({'matching_existing_logical_archive_accepted': True,
                                 'all_parts_still_verified': True, 'copies': len(existing['files'])})
        row = execute('existing-output', ['bash', str(output / 'step-01.sh')])
        if row['exit_code'] == 0:
            raise ValueError('Existing evidence root was reused')

        # Exact frozen APKs are linked for read-only offline inspection;
        # no Android installation or extra signed build is performed.
        runtime_inputs = [
            (args.original_apk.resolve(), 'workspace/artifacts/' + preparation.APKS[0][1]),
            (args.candidate_apk.resolve(), 'workspace/artifacts/' + preparation.APKS[1][1]),
            (args.aapt2.resolve(), 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2'),
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
            runtime_before.append({'source': str(original), 'path': relative, **preparation.identity(original),
                'transport': 'READ_ONLY_HARDLINK' if original.stat().st_dev == root.stat().st_dev else 'READ_ONLY_BYTE_COPY',
                'source_device': original.stat().st_dev, 'destination_device': target.stat().st_dev})
        save(output / 'runtime-inputs-before.json', runtime_before)
        row = execute('exact-offline-apk-preflight', [sys.executable, str(home / 'prepare_trigger_journey.py'),
            '--root', str(root), '--output', str(root / 'ci-exact-alarm-enable-return'), '--materialized'], timeout=120)
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
            ('missing-navigation-policy-pin', 'omit-navigation', False, False),
            ('changed-navigation-policy-pin', 'changed-navigation', False, False),
            ('older-fourteen-plan-pin', 'older-plan', False, False),
            ('missing-settings-contract-pin', 'omit-settings-contract', False, False),
            ('changed-settings-contract-pin', 'changed-settings-contract', False, False),
        ]
        inventory_names = {entry['path'] for entry in inputs + runtime_before} | {preparation.GUARD_ARCHIVE}
        inventory_names.update('ci-exact-alarm-enable-return/' + entry['copy'] for entry in clean['files'])
        inventory_names.add('ci-exact-alarm-enable-return/input-preflight.json')
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
            case_output = case / 'ci-exact-alarm-enable-return'
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
            elif mode == 'omit-navigation':
                del declared['exact_alarm_enable_return_policy_sha256']
            elif mode == 'changed-navigation':
                declared['exact_alarm_enable_return_policy_sha256'] = '0' * 64
            elif mode == 'older-plan':
                declared['plan_sha256'] = '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'
            elif mode == 'omit-settings-contract':
                del declared['settings_contract_sha256']
            elif mode == 'changed-settings-contract':
                declared['settings_contract_sha256'] = '0' * 64
            elif mode == 'omit-reviewed':
                role = next(entry['copy'] for entry in declared['files'] if entry['copy'].startswith('reviewed-source/'))
                declared['files'] = [entry for entry in declared['files'] if entry['copy'] != role]
            replace_bytes(case_output / 'input-preflight.json', (json.dumps(declared, indent=2) + '\n').encode())
            outcomes = []
            for phase, script, suffix, report_name in [
                    ('materialized', 'prepare_trigger_journey.py', ['--materialized'], 'materialized-inputs.json'),
                    ('final', 'verify_trigger_journey.py', [], 'exact-alarm-enable-return-verification.json')]:
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
        policy_script.write_text("import copy\nimport json\nfrom pathlib import Path\nimport sys\nsys.path[:0] = [sys.argv[1], sys.argv[2], sys.argv[3]]\nimport verify_trigger_journey as verifier\nimport exact_alarm_enable_return as alarm\nimport exact_alarm_enable_return_readiness as readiness\npositive = {'schema': 7, 'plan': alarm.expected_plan(), 'plan_sha256': alarm.PLAN_SHA256,\n            alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY), readiness.POLICY_KEY: copy.deepcopy(readiness.POLICY)}\nverifier.require_workflow_policies(positive)\ncontrols = []\nfor label in ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-readiness', 'changed-readiness',\n              'missing-navigation', 'changed-navigation', 'nested-navigation', 'changed-plan', 'changed-plan-hash']:\n    value = copy.deepcopy(positive)\n    if label == 'legacy-schema': value['schema'] = 6\n    elif label == 'unregistered-schema': value['schema'] = 8\n    elif label == 'boolean-schema': value['schema'] = True\n    elif label == 'missing-readiness': del value[readiness.POLICY_KEY]\n    elif label == 'changed-readiness': value[readiness.POLICY_KEY]['max_seconds'] = 11\n    elif label == 'missing-navigation': del value[alarm.POLICY_KEY]\n    elif label == 'changed-navigation': value[alarm.POLICY_KEY]['settings_inputs_total'] = 1\n    elif label == 'nested-navigation': value['unexpected'] = {alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY)}\n    elif label == 'changed-plan': value['plan'][-1][1] = 'com.example.foreign'\n    elif label == 'changed-plan-hash': value['plan_sha256'] = '0' * 64\n    try:\n        verifier.require_workflow_policies(value)\n    except Exception as error:\n        if not any(text in str(error) for text in ['Missing or altered notification readiness policy',\n                                                  'Missing, altered or misplaced exact-alarm enable/return policy or plan']):\n            raise\n        controls.append({'label': label, 'rejected': True, 'reason': str(error)})\n    else:\n        raise AssertionError('Workflow policy substitution accepted: ' + label)\nverifier.require_workflow_policies(positive)\nresult = {'passed': True, 'android_executed': False,\n          'scope': 'Required complete plan and both policy formats only; compare separately requires complete raw evidence and every command role.',\n          'positive_and_restore': True, 'negative_controls': controls}\nPath(sys.argv[4]).write_text(json.dumps(result, indent=2) + '\\n')\nprint(json.dumps(result, indent=2))\n")
        policy_result = output / 'workflow-policy-controls.json'
        row = execute('workflow-policy-controls', [sys.executable, '-B', str(policy_script), str(home),
            str(root / 'ci-exact-alarm-enable-return/reviewed-source/tools/parity_journeys'),
            str(root / 'ci-exact-alarm-enable-return/reviewed-source/project'), str(policy_result)])
        if row['exit_code'] or json.loads(policy_result.read_text()).get('passed') is not True:
            raise ValueError('Workflow readiness policy controls failed')
        report['checks'].append(json.loads(policy_result.read_text()))

        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))
        for index, script in enumerate(host.splitlines()[1:]):
            if index == 1:
                continue  # This exact 259-test source suite is already closed; hosted still executes it.
            row = execute('packaged-host-controls-' + str(index), ['bash', '-o', 'pipefail', '-c', script], timeout=600)
            if row['exit_code']:
                raise ValueError('Packaged animation or downloader controls failed')
        closed_source = json.loads((args.guard.resolve() / 'checkpoint.json').read_bytes())
        if (closed_source['source_files'] != 102 or closed_source['android_executed'] is not False
                or closed_source['distinct_host_tests_passed'] != 259):
            raise ValueError('Closed source host-control evidence differs')
        report['source_host_controls_reused'] = {'checkpoint_sha256': preparation.PINS[preparation.GUARD + '/checkpoint.json'],
            'distinct_tests': closed_source['distinct_host_tests_passed'], 'locally_reexecuted': False,
            'hosted_workflow_still_executes_full_suite': True}
        runtime = next(step['run'] for step in steps if step['name'].startswith('Observe the sixteen declared'))
        start = runtime.index('cleanup_trigger_runtime() {')
        stop = runtime.index("trap 'exit 143' TERM") + len("trap 'exit 143' TERM")
        cleanup = runtime[start:stop]
        for label, step_status, service_status in [('clean', 0, 0), ('failed-journey', 7, 0), ('failed-service', 0, 5)]:
            case = output / 'cleanup-controls' / label
            queue = case / 'ci-exact-alarm-enable-return/environment/queue'
            queue.mkdir(parents=True)
            adb = case / 'tooling/macrodroid-exact-alarm-enable-return-tooling/android/platform-tools/adb'
            adb.parent.mkdir(parents=True)
            adb.write_text('#!/bin/sh\nprintf "SIMULATED OFFLINE DIAGNOSTIC ONLY\\n"\nexit 0\n')
            adb.chmod(0o755)
            script = output / ('cleanup-' + label + '.sh')
            script.write_text('set -euo pipefail\n' +
                "bash -c 'for ((n=0;n<200;n++)); do if test -e ci-exact-alarm-enable-return/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ " + str(service_status) + ' &\n' +
                'trigger_service_pid=$!\n' + cleanup + '\nexit ' + str(step_status) + '\n')
            row = execute('owned-cleanup-' + label, ['bash', str(script)], cwd=case,
                          extra={'RUNNER_TEMP': str(case / 'tooling')}, timeout=10)
            expected = step_status or (1 if service_status else 0)
            value = json.loads((case / 'ci-exact-alarm-enable-return/runtime-cleanup.json').read_text())
            if (row['exit_code'] != expected or not (queue / 'STOP').is_file()
                    or value['service_cleanup_confirmed'] is not (service_status == 0)):
                raise ValueError('Owned cleanup status or evidence mismatch')
        for entry in inputs + runtime_before:
            if preparation.identity(Path(entry['source'])) != {key: entry[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Baseline input changed during validation: ' + entry['source'])
        report['helpers_after'] = {name: preparation.identity(home / name) for name in own_before}
        if report['helpers_after'] != own_before:
            raise ValueError('Workflow or helper changed during validation')
        if preparation.verify_guard_archive(root) != clean['guard_archive_preparation']['verified']:
            raise ValueError('Prepared guard archive changed during validation')
        report.update(status='OFFLINE_EXACT_ALARM_ENABLE_RETURN_WORKFLOW_VALIDATED', passed=True,
                      source_apks_and_preserved_tool_bytes_unchanged=True)
    except Exception as error:
        report.update(status='OFFLINE_EXACT_ALARM_ENABLE_RETURN_WORKFLOW_REJECTED', reason=type(error).__name__ + ': ' + str(error))
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
