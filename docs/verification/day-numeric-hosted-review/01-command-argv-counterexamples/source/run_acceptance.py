#!/usr/bin/env python3
"""Run all sixteen gates in one owned process group and preserve actual exit status."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

import inputs
from prepare import inventory


def stop_owned_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)
    # A direct child may exit before one of its owned descendants. The process
    # group was allocated by this invocation with start_new_session=True.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_child(command, cwd, env, stdout, stderr, timeout):
    result = {'argv': list(command), 'cwd': str(cwd), 'timeout_seconds': timeout,
              'returncode': None, 'timed_out': False, 'started_unix_ns': time.time_ns()}
    process = None
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=out, stderr=err, start_new_session=True)
            result['owned_process_group'] = process.pid
            try:
                result['returncode'] = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                result['timed_out'] = True
                stop_owned_group(process)
                result['returncode'] = process.returncode
    except BaseException as error:
        result['error'] = repr(error)
        if process is not None:
            stop_owned_group(process)
            result['returncode'] = process.returncode
    finally:
        if process is not None:
            stop_owned_group(process)
        result['ended_unix_ns'] = time.time_ns()
        result['stdout'] = {'path': stdout.name, **inputs.identity(stdout)} if stdout.is_file() else None
        result['stderr'] = {'path': stderr.name, **inputs.identity(stderr)} if stderr.is_file() else None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-repository', type=Path, required=True)
    parser.add_argument('--overlay-repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--runtime-manifest-sha256', required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    inputs.require(output.is_dir() and not output.is_symlink(), 'Missing owned preparation output')
    report = {'schema': 1, 'status': 'HOST_ACCEPTANCE_NOT_COMPLETED', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'active_promoted': False,
              'android_runtime_executed': False, 'full_runtime_1_to_1_established': False}
    try:
        inputs.verify_runtime_manifest(args.runtime_manifest_sha256)
        pins, _, expected, _ = inputs.contract(args.baseline_repository, args.overlay_repository)
        prepared_path = inputs.regular(output, 'preparation.json')
        prepared = inputs.read_json(prepared_path)
        inputs.require(prepared.get('passed') is True and prepared.get('status') == 'EXACT_19_FILE_WIP_PREPARED'
                       and prepared.get('output') == str(output), 'Exact preparation did not pass')
        inputs.require(prepared['runtime_source']['manifest']['sha256'] == args.runtime_manifest_sha256,
                       'Preparation has another hosted runtime manifest')
        project = Path(prepared['project'])
        inputs.compare_inputs(inputs.scan_inputs(project), expected)
        inputs.require(inventory(project / 'reports') == [{'path': 'release-input-snapshot.json', **pins['future_manifest']}]
                       and inventory(project / 'dist') == [], 'Acceptance output scope is not fresh')
        report['preparation_sha256'] = inputs.identity(prepared_path)['sha256']
        report['project'] = str(project)
        report['python_executable'] = sys.executable
        report['python_version'] = sys.version
        report['platform'] = platform.platform()
        report['input_snapshot_before'] = {k: expected[k] for k in ('files', 'snapshot_sha256')}
        env = os.environ.copy()
        env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(output / 'tmp'))
        report['environment_overrides'] = {key: env[key] for key in ('PYTHONUTF8', 'PYTHONDONTWRITEBYTECODE', 'TMPDIR')}
        report['java_versions'] = []
        for name, argv in [('java-version', ['java', '-version']), ('javac-version', ['javac', '-version'])]:
            value = run_child(argv, project, env, output / (name + '.stdout.log'), output / (name + '.stderr.log'), 15)
            report['java_versions'].append(value)
            inputs.require(type(value['returncode']) is int and value['returncode'] == 0 and value['timed_out'] is False,
                           'Java toolchain observation failed')
        inputs.write_json(output / 'execution-start.json', report)
        command = [sys.executable, '-B', 'acceptance.py']
        execution = run_child(command, project, env, output / 'acceptance.stdout.log', output / 'acceptance.stderr.log',
                              pins['acceptance_timeout_seconds'])
        report['execution'] = execution
        after = inputs.scan_inputs(project)
        report['input_snapshot_after'] = {k: after[k] for k in ('files', 'snapshot_sha256')}
        inputs.compare_inputs(after, expected)
        report['build_inputs_unchanged'] = True
        success = type(execution['returncode']) is int and execution['returncode'] == 0 and execution['timed_out'] is False and 'error' not in execution
        report.update(status='HOST_ACCEPTANCE_PROCESS_EXITED_ZERO' if success else 'HOST_ACCEPTANCE_PROCESS_FAILED', passed=success)
        return 0 if success else 2
    except BaseException as error:
        report['error'] = repr(error)
        print('HOST ACCEPTANCE WRAPPER FAILED:', error, file=sys.stderr)
        return 2
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        inputs.write_json(output / 'execution.json', report)
        print(report['status'], flush=True)


if __name__ == '__main__':
    sys.exit(main())
