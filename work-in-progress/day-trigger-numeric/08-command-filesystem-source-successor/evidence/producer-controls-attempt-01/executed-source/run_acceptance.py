#!/usr/bin/env python3
"""Run all sixteen gates in one owned process group and preserve actual exit status."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
import hashlib
import stat
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

import inputs
from prepare import inventory


def command_clock():
    """Record exact clocks; the ISO text is a display of this same Unix value."""
    unix_ns = time.time_ns()
    monotonic_ns = time.monotonic_ns()
    seconds, nanos = divmod(unix_ns, 1_000_000_000)
    utc = datetime.fromtimestamp(seconds, timezone.utc).replace(microsecond=nanos // 1000)
    return {'unix_ns': unix_ns, 'monotonic_ns': monotonic_ns,
            'utc': utc.isoformat(timespec='microseconds')}


def command_file_stat(value):
    return {'device': value.st_dev, 'inode': value.st_ino, 'mode': value.st_mode,
            'links': value.st_nlink, 'bytes': value.st_size,
            'mtime_ns': value.st_mtime_ns, 'ctime_ns': value.st_ctime_ns}


class CommandStreamEvidence:
    """Observe exclusive files using both clocks and actual filesystem witnesses.

    Witnesses contain no invented timestamps. Every attempted after-witness is
    retained; the first whose actual filesystem clock brackets the closed streams
    is used. The bounded wait changes no timestamp and adds no acceptance slack.
    """
    WITNESS_ATTEMPTS = 16
    WITNESS_POLL_NS = 5_000_000

    def __init__(self, root, stdout, stderr):
        self.root = Path(root).resolve()
        self.paths = {'stdout': Path(stdout), 'stderr': Path(stderr)}
        if self.paths['stdout'].parent != self.paths['stderr'].parent:
            raise RuntimeError('Command streams must share a filesystem witness directory')
        if not self.paths['stdout'].name.endswith('.stdout.log'):
            raise RuntimeError('Command stdout role differs')
        self.label = self.paths['stdout'].name[:-len('.stdout.log')]
        if self.paths['stderr'].name != self.label + '.stderr.log':
            raise RuntimeError('Command stderr role differs')
        self.folder = self.paths['stdout'].parent
        self.handles = {}
        self.value = {'schema': 2, 'started': command_clock(), 'streams': {},
                      'after_witnesses': [], 'after_witness_attempt_limit': self.WITNESS_ATTEMPTS,
                      'after_witness_poll_ns': self.WITNESS_POLL_NS,
                      'filesystem_bracket_complete': False}

    def open_file(self, path):
        name = path.relative_to(self.root).as_posix()
        row = {'path': name, 'exclusive_mode': 'xb', 'open_started': command_clock()}
        handle = path.open('xb')
        try:
            row['initial_stat'] = command_file_stat(os.fstat(handle.fileno()))
            row['initial_sha256'] = hashlib.sha256(b'').hexdigest()
            row['opened'] = command_clock()
            value = row['initial_stat']
            if not stat.S_ISREG(value['mode']) or value['links'] != 1 or value['bytes'] != 0:
                raise RuntimeError('Exclusive command file is not a new empty regular inode')
            return handle, row
        except BaseException:
            handle.close()
            raise

    def close_file(self, handle, row):
        handle.flush()
        row['closing'] = command_clock()
        row['final_stat'] = command_file_stat(os.fstat(handle.fileno()))
        handle.close()
        row['closed'] = command_clock()
        path = self.root / row['path']
        before = command_file_stat(path.stat())
        if before != row['final_stat'] or path.is_symlink():
            raise RuntimeError('Command file changed inode or metadata during closure')
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        after = command_file_stat(path.stat())
        if after != before:
            raise RuntimeError('Command file changed while hashing')
        first = row['initial_stat']
        if any(first[key] != before[key] for key in ('device', 'inode', 'mode', 'links')):
            raise RuntimeError('Exclusive command file ownership changed')
        row.update(bytes=before['bytes'], sha256=digest, hashed=command_clock())

    def witness(self, suffix):
        handle, row = self.open_file(self.folder / (self.label + '.' + suffix + '.log'))
        try:
            self.close_file(handle, row)
        finally:
            if not handle.closed:
                handle.close()
        return row

    def __enter__(self):
        try:
            self.value['before_witness'] = self.witness('filesystem-before')
            for name in ('stdout', 'stderr'):
                handle, row = self.open_file(self.paths[name])
                self.handles[name] = handle
                self.value['streams'][name] = row
            self.value['invocation_started'] = command_clock()
            return self
        except BaseException as error:
            self.value['error'] = repr(error)
            for name, handle in self.handles.items():
                if not handle.closed:
                    try:
                        self.close_file(handle, self.value['streams'][name])
                    except BaseException as cleanup_error:
                        self.value.setdefault('cleanup_errors', []).append(repr(cleanup_error))
                        if not handle.closed:
                            handle.close()
            self.value['finished'] = command_clock()
            raise

    def __exit__(self, kind, error, traceback):
        self.value['invocation_finished'] = command_clock()
        if error is not None:
            self.value['error'] = repr(error)
        cleanup_error = None
        for name in ('stderr', 'stdout'):
            handle = self.handles[name]
            try:
                self.close_file(handle, self.value['streams'][name])
            except BaseException as failure:
                self.value.setdefault('cleanup_errors', []).append(repr(failure))
                cleanup_error = failure
            finally:
                if not handle.closed:
                    handle.close()
        try:
            before = self.value['before_witness']['final_stat']
            streams = [self.value['streams'][name][phase]
                       for name in ('stdout', 'stderr') for phase in ('initial_stat', 'final_stat')]
            for index in range(self.WITNESS_ATTEMPTS):
                witness = self.witness(f'filesystem-after-{index:02d}')
                self.value['after_witnesses'].append(witness)
                after = witness['final_stat']
                complete = all(before['device'] == value['device'] == after['device']
                    and before['ctime_ns'] <= value['mtime_ns'] <= after['ctime_ns']
                    and before['ctime_ns'] <= value['ctime_ns'] <= after['ctime_ns'] for value in streams)
                if complete:
                    self.value['filesystem_bracket_complete'] = True
                    break
                if index + 1 < self.WITNESS_ATTEMPTS:
                    time.sleep(self.WITNESS_POLL_NS / 1_000_000_000)
            if not self.value['filesystem_bracket_complete']:
                raise RuntimeError('Actual filesystem witnesses did not bracket command stream timestamps')
        except BaseException as failure:
            self.value.setdefault('cleanup_errors', []).append(repr(failure))
            cleanup_error = failure
        self.value['finished'] = command_clock()
        if error is None and cleanup_error is not None:
            raise cleanup_error
        return False

    def add_to(self, row):
        for prefix, name in (('started', 'started'), ('ended', 'finished')):
            value = self.value.get(name)
            if value is not None:
                row[prefix + '_unix_ns'] = value['unix_ns']
                row[prefix + '_monotonic_ns'] = value['monotonic_ns']
                row[prefix + '_utc'] = value['utc']
        if 'finished' in self.value:
            row['duration_seconds'] = (self.value['finished']['monotonic_ns'] - self.value['started']['monotonic_ns']) / 1_000_000_000
        for name in ('stdout', 'stderr'):
            value = self.value['streams'].get(name)
            if value is not None and all(key in value for key in ('path', 'bytes', 'sha256')):
                row[name] = {key: value[key] for key in ('path', 'bytes', 'sha256')}
            else:
                row[name] = None
        row['stream_evidence'] = self.value



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
              'returncode': None, 'timed_out': False}
    observation = CommandStreamEvidence(stdout.parent, stdout, stderr)
    process = None
    try:
        with observation as streams:
            try:
                process = subprocess.Popen(command, cwd=cwd, env=env, stdout=streams.handles['stdout'],
                                           stderr=streams.handles['stderr'], start_new_session=True)
                result['owned_process_group'] = process.pid
                try:
                    result['returncode'] = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    result['timed_out'] = True
                    stop_owned_group(process)
                    result['returncode'] = process.returncode
            finally:
                if process is not None:
                    stop_owned_group(process)
    except BaseException as error:
        result['error'] = repr(error)
        if process is not None:
            result['returncode'] = process.returncode
    finally:
        observation.add_to(result)
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
    started = command_clock()
    report = {'schema': 2, 'status': 'HOST_ACCEPTANCE_NOT_COMPLETED', 'passed': False,
              'started_utc': started['utc'], 'started_unix_ns': started['unix_ns'],
              'started_monotonic_ns': started['monotonic_ns'], 'active_promoted': False,
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
        report['python_executable_identity'] = inputs.identity(Path(sys.executable).resolve(strict=True))
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
        finished = command_clock()
        report.update(finished_utc=finished['utc'], finished_unix_ns=finished['unix_ns'],
                      finished_monotonic_ns=finished['monotonic_ns'])
        inputs.write_json(output / 'execution.json', report)
        print(report['status'], flush=True)


if __name__ == '__main__':
    sys.exit(main())
