#!/usr/bin/env python3
"""Small offline checks against actual immutable inputs; never run Android."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
import yaml

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
OWN = SOURCE / 'tools/indicator_sampling'
PARENT = ROOT / 'parent-inputs'
BARE = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
WORKFLOW = SOURCE / '.github/workflows/indicator-fixed-sampling.yml'
sys.path.insert(0, str(OWN))
import common as c
import prepare


def identity(path):
    return c.file_identity(path)


def inventory(root):
    return [{'path': p.relative_to(root).as_posix(), **identity(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]


parser = argparse.ArgumentParser()
parser.add_argument('attempt')
args = parser.parse_args()
output = ROOT / 'reports' / args.attempt
output.mkdir(parents=True, exist_ok=False)
shutil.copy2(__file__, output / 'validate_workflow.py')
before = inventory(SOURCE)
parents_before = inventory(PARENT)
c.write_json(output / 'source-before.json', before)
c.write_json(output / 'parents-before.json', parents_before)
report = {'schema': 1, 'status': 'OFFLINE_VALIDATION_INCOMPLETE', 'started_utc': c.utc(),
          'commands': [], 'checks': [], 'workflow': identity(WORKFLOW), 'android_executed': False,
          'apk_copy_or_materialization_performed': False,
          'scope': 'Actual read-only parent/APK/AAPT bindings and shell/import checks; cleanup uses three tiny owned simulated services.'}


def run(label, argv, cwd=ROOT, extra=None, seconds=30):
    row = {'label': label, 'argv': argv, 'cwd': str(cwd), 'timeout_seconds': seconds,
           'started_ns': time.monotonic_ns(), 'timed_out': False}
    for name in ('stdout', 'stderr'):
        row[name] = {'path': label + '.' + name}
    with (output / row['stdout']['path']).open('xb') as stdout, (output / row['stderr']['path']).open('xb') as stderr:
        try:
            child = subprocess.run(argv, cwd=cwd, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
                'TMPDIR': str(ROOT / 'tmp'), **(extra or {})}, timeout=seconds, stdout=stdout, stderr=stderr)
            row['returncode'] = child.returncode
        except subprocess.TimeoutExpired:
            row.update(returncode=None, timed_out=True)
    row['finished_ns'] = time.monotonic_ns()
    for name in ('stdout', 'stderr'):
        row[name].update(identity(output / row[name]['path']))
    report['commands'].append(row)
    c.write_json(output / 'progress.json', report)
    return row


try:
    steps = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)['jobs']['fixed-sampling']['steps']
    commands = []
    for index, step in enumerate(steps):
        if 'run' not in step:
            continue
        script = output / f'step-{index:02d}.sh'
        script.write_text(step['run'])
        c.require(run(f'bash-syntax-{index:02d}', ['bash', '-n', str(script)])['returncode'] == 0,
                  'Actual workflow shell syntax failed')
        lines = step['run'].splitlines()
        inside, body, number = False, [], 0
        for line in lines:
            if inside:
                if line == 'PY':
                    text = '\n'.join(body) + '\n'
                    ast.parse(text)
                    (output / f'step-{index:02d}-python-{number:02d}.py').write_text(text)
                    number += 1
                    body, inside = [], False
                else:
                    body.append(line)
            elif "<<'PY'" in line:
                inside = True
        c.require(not inside, 'Unterminated embedded Python block')
    report['checks'].append({'name': 'all-actual-shell-and-embedded-python-syntax', 'passed': True})
    for name in ('common.py', 'prepare.py', 'record.py', 'verify.py', 'test_indicator_sampling.py'):
        ast.parse((OWN / name).read_text())
    for name in ('prepare.py', 'record.py', 'verify.py'):
        c.require(run('cli-help-' + name[:-3], [sys.executable, '-B', str(OWN / name), '--help'])['returncode'] == 0,
                  'Actual CLI could not parse its declared entrypoint')
    required_source = prepare.source_manifest(SOURCE)
    c.require(len(required_source) == 16, 'Complete own-source count changed')
    first_python = ast.parse((output / 'step-02-python-00.py').read_text())
    embedded = next(ast.literal_eval(node.value) for node in first_python.body
                    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == 'expected')
    expected_source = {'tools/indicator_sampling/' + name: identity(OWN / name) for name in prepare.OWN_FILES}
    c.require(embedded == dict(sorted(expected_source.items())), 'Workflow embedded source pins differ')
    report['checks'].append({'name': 'complete-16-own-source-roles-and-workflow-pins', 'passed': True,
                             'entries': required_source})

    pins = c.json_file(OWN / 'pins.json')
    git_rows, paths = [], []
    for row in pins['parents']:
        paths.append({'path': row['path'], 'bytes': row['bytes'], 'sha256': row['sha256'],
                      'mode': row['mode'], 'role': 'parent'})
    for role, manifest in c.MANIFESTS.items():
        for row in c.json_file(PARENT / manifest)['parts']:
            paths.append({'path': row['path'], 'bytes': row['size_bytes'], 'sha256': row['sha256'],
                          'mode': '100644', 'role': role + '-part'})
    c.require(len(paths) == len({row['path'] for row in paths}) == 40, 'Parent input cardinality differs')
    sparse = steps[1]['with']['sparse-checkout'].splitlines()
    c.require(sparse == ['/' + row['path'] for row in paths], 'Sparse checkout omits/reorders a required parent or part')
    c.require(steps[1]['with']['ref'] == c.PARENT_COMMIT, 'Immutable parent checkout changed')
    for row in paths:
        argv = ['git', '--git-dir=' + str(BARE), 'show', c.PARENT_COMMIT + ':' + row['path']]
        begin = time.monotonic_ns()
        child = subprocess.run(argv, capture_output=True, timeout=30)
        c.require(child.returncode == 0 and not child.stderr.strip(), 'Fetched parent blob is unavailable')
        c.require(c.identity(child.stdout) == {k: row[k] for k in ('bytes', 'sha256')}, 'Fetched exact parent bytes differ')
        mode_child = subprocess.run(['git', '--git-dir=' + str(BARE), 'ls-tree', c.PARENT_COMMIT, '--', row['path']],
                                    capture_output=True, timeout=30)
        c.require(mode_child.returncode == 0 and not mode_child.stderr.strip(), 'Fetched parent mode is unavailable')
        mode_line = mode_child.stdout.decode().strip()
        c.require(mode_line.split(' ', 1)[0] == row['mode'] and mode_line.split('\t')[-1] == row['path'],
                  'Fetched parent mode/path differs')
        if row['role'] == 'parent':
            c.require(identity(PARENT / row['path']) == c.identity(child.stdout), 'Local parent copy differs from fetched commit')
        git_rows.append({**row, 'argv': argv, 'started_ns': begin, 'finished_ns': time.monotonic_ns(),
                         'returncode': child.returncode, 'git_tree_record': mode_line})
        del child
    c.write_json(output / 'all-forty-fetched-input-bindings.json', git_rows)
    report['checks'].append({'name': 'all-40-fetched-parent-and-part-bytes', 'passed': True,
                            'bytes': sum(row['bytes'] for row in paths), 'apk_parts_materialized': False})

    modules = c.load_parents(PARENT)
    apk_paths = {
        'original': Path('/workspace/scratch/4130730d15aa/recovered/automation android app'),
        'candidate': Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk'),
    }
    apks = {}
    for role, path in apk_paths.items():
        apks[role] = prepare.inspect_apk(path, role, output, modules['android_acceptance'].badging_metadata)
    c.write_json(output / 'actual-read-only-apk-inspection.json', apks)
    report['checks'].append({'name': 'both-actual-fixed-apks-full-crc-and-aapt2-badging', 'passed': True})

    runtime = steps[6]['run']
    begin = runtime.index('cleanup_indicator_runtime() {')
    end = runtime.index("trap 'exit 143' TERM") + len("trap 'exit 143' TERM")
    cleanup = runtime[begin:end]
    (output / 'exact-owned-cleanup-function.sh').write_text(cleanup + '\n')
    for label, step_status, service_status in [('clean', 0, 0), ('failed-slot', 7, 0), ('failed-service', 0, 5)]:
        case = output / 'cleanup-controls' / label
        queue = case / 'ci-indicator/environment/queue'
        queue.mkdir(parents=True)
        adb = case / 'tooling/indicator-tooling/android/platform-tools/adb'
        adb.parent.mkdir(parents=True)
        adb.write_text('#!/bin/sh\nprintf "SIMULATED OFFLINE DIAGNOSTIC ONLY\\n"\nexit 0\n')
        adb.chmod(0o755)
        script = output / ('cleanup-' + label + '.sh')
        script.write_text('set -euo pipefail\n' +
            "bash -c 'for ((n=0;n<200;n++)); do if test -e ci-indicator/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ " + str(service_status) + ' &\n' +
            'indicator_service_pid=$!\n' + cleanup + '\nexit ' + str(step_status) + '\n')
        result = run('owned-cleanup-' + label, ['bash', str(script)], cwd=case,
                     extra={'RUNNER_TEMP': str(case / 'tooling')}, seconds=10)
        expected = step_status or (1 if service_status else 0)
        value = c.json_file(case / 'ci-indicator/runtime-cleanup.json')
        c.require(result['returncode'] == expected and (queue / 'STOP').is_file()
                  and value['service_cleanup_confirmed'] is (service_status == 0),
                  'Owned cleanup failed to preserve literal service/step outcome')
    report['checks'].append({'name': 'three-actual-owned-cleanup-function-controls', 'passed': True,
                            'adb_and_android_executed': False})
    report['status'] = 'OFFLINE_WORKFLOW_INPUTS_AND_CLEANUP_PASSED'
except Exception as error:
    report['error'] = type(error).__name__ + ': ' + str(error)
    (output / 'failure.txt').write_text(traceback.format_exc())
finally:
    after, parents_after = inventory(SOURCE), inventory(PARENT)
    c.write_json(output / 'source-after.json', after)
    c.write_json(output / 'parents-after.json', parents_after)
    report.update(source_unchanged=before == after, parent_inputs_unchanged=parents_before == parents_after,
                  finished_utc=c.utc(), command_count=len(report['commands']), check_count=len(report['checks']))
    if not report['source_unchanged'] or not report['parent_inputs_unchanged']:
        report['status'] = 'OFFLINE_VALIDATION_INCOMPLETE'
    c.write_json(output / 'result.json', report)
    print(json.dumps({key: report[key] for key in ('status', 'command_count', 'check_count',
        'source_unchanged', 'parent_inputs_unchanged')} | ({'error': report['error']} if 'error' in report else {}), indent=2))
