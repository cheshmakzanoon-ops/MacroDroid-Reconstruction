#!/usr/bin/env python3
"""Actual bounded Python subprocess controls for the two source-bound producers.

These tests execute no Java, D8, APK build, application method, or Android process.
The numeric class is imported from the exact successor source. Its nested DEX
command runner is not invoked; the same class used there is exercised directly.
"""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'reports/02-producer-controls-attempt-01'
PROJECT = ROOT / 'source-successor/project'
TOOLS = ROOT / 'source/tools/day_numeric_acceptance'
BASE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
sys.path[:0] = [str(PROJECT), str(TOOLS), str(BASE)]
import day_numeric_dex_controls as numeric
import run_acceptance as wrapper


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def helper_ast(path):
    names = {'command_clock', 'command_file_stat', 'CommandStreamEvidence'}
    return ast.dump(ast.Module(body=[n for n in ast.parse(path.read_text()).body
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names], type_ignores=[]), include_attributes=False)


class ProducerControls(unittest.TestCase):
    records = []

    def directory(self, kind, suffix=''):
        folder = OUT / 'actual' / self._testMethodName / (kind + suffix)
        folder.mkdir(parents=True, exist_ok=False)
        return folder

    def invoke(self, kind, folder, code='pass', arguments=(), timeout=5):
        argv = [sys.executable, '-B', '-c', code, *map(str, arguments)]
        out, err = folder / 'probe.stdout.log', folder / 'probe.stderr.log'
        if kind == 'wrapper':
            row = wrapper.run_child(argv, folder, os.environ.copy(), out, err, timeout)
        else:
            observation = numeric.CommandStreamEvidence(folder, out, err)
            row = {'argv': argv, 'cwd': str(folder), 'timeout_seconds': timeout, 'returncode': None}
            try:
                with observation as streams:
                    row['returncode'] = subprocess.run(argv, cwd=folder, stdout=streams.handles['stdout'],
                        stderr=streams.handles['stderr'], timeout=timeout).returncode
            except BaseException as error:
                row['error'] = repr(error)
            finally:
                observation.add_to(row)
        self.records.append({'test': self._testMethodName, 'producer': kind, 'folder': str(folder), 'row': row})
        (folder / 'observation.json').write_text(json.dumps(row, indent=2) + '\n')
        return row

    def check_complete(self, row, code=0):
        self.assertEqual(code, row['returncode'])
        self.assertNotIn('error', row)
        evidence = row['stream_evidence']
        self.assertTrue(evidence['filesystem_bracket_complete'])
        self.assertNotIn('error', evidence)
        self.assertNotIn('cleanup_errors', evidence)
        self.assertLess(row['started_unix_ns'], row['ended_unix_ns'])
        self.assertLess(row['started_monotonic_ns'], row['ended_monotonic_ns'])
        self.assertLessEqual(len(evidence['after_witnesses']), 16)
        before = evidence['before_witness']['final_stat']
        after = evidence['after_witnesses'][-1]['final_stat']
        physical = []
        for receipt in [evidence['before_witness'], *evidence['streams'].values(), *evidence['after_witnesses']]:
            initial, final = receipt['initial_stat'], receipt['final_stat']
            self.assertEqual(initial['links'], 1)
            self.assertEqual(final['links'], 1)
            self.assertEqual(initial['bytes'], 0)
            self.assertEqual(initial['inode'], final['inode'])
            self.assertEqual(initial['device'], final['device'])
            physical.append((final['device'], final['inode']))
            for marker in ('open_started', 'opened', 'closing', 'closed', 'hashed'):
                self.assertLessEqual(evidence['started']['monotonic_ns'], receipt[marker]['monotonic_ns'])
                self.assertLessEqual(receipt[marker]['monotonic_ns'], evidence['finished']['monotonic_ns'])
        self.assertEqual(len(set(physical)), len(physical))
        for receipt in evidence['streams'].values():
            for phase in ('initial_stat', 'final_stat'):
                for field in ('mtime_ns', 'ctime_ns'):
                    self.assertLessEqual(before['ctime_ns'], receipt[phase][field])
                    self.assertLessEqual(receipt[phase][field], after['ctime_ns'])

    def test_both_source_producer_helpers_have_identical_full_ast(self):
        self.assertEqual(helper_ast(PROJECT / 'day_numeric_dex_controls.py'), helper_ast(TOOLS / 'run_acceptance.py'))

    def test_iso_displays_are_exact_truncations_of_the_same_integer_ns(self):
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        for module in (numeric, wrapper):
            for value in (1791798408123456000, 1791798408123456001, 1791798408123456950, 1791798408123456999):
                with patch.object(module.time, 'time_ns', return_value=value), patch.object(module.time, 'monotonic_ns', return_value=123456789):
                    row = module.command_clock()
                delta = datetime.fromisoformat(row['utc']) - epoch
                exact = (delta.days * 86400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1000
                self.assertEqual(value, row['unix_ns'])
                self.assertEqual(value // 1000 * 1000, exact)
                self.assertEqual(123456789, row['monotonic_ns'])

    def test_eight_real_empty_children_retain_actual_filesystem_clock_brackets(self):
        for kind in ('numeric', 'wrapper'):
            for index in range(4):
                with self.subTest(kind=kind, index=index):
                    row = self.invoke(kind, self.directory(kind, str(index)))
                    self.check_complete(row)
                    self.assertEqual(0, row['stdout']['bytes'])
                    self.assertEqual(0, row['stderr']['bytes'])

    def test_real_nonempty_stdout_and_stderr_keep_initial_and_final_inode(self):
        for kind in ('numeric', 'wrapper'):
            with self.subTest(kind=kind):
                folder = self.directory(kind)
                row = self.invoke(kind, folder, 'import sys; print("measured stdout"); print("measured stderr", file=sys.stderr)')
                self.check_complete(row)
                self.assertEqual(b'measured stdout\n', (folder / 'probe.stdout.log').read_bytes())
                self.assertEqual(b'measured stderr\n', (folder / 'probe.stderr.log').read_bytes())

    def test_actual_nonzero_child_status_is_retained(self):
        for kind in ('numeric', 'wrapper'):
            with self.subTest(kind=kind):
                self.check_complete(self.invoke(kind, self.directory(kind), 'raise SystemExit(7)'), 7)

    def test_preexisting_empty_stdout_rejects_before_invocation(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            path = folder / 'probe.stdout.log'; path.write_bytes(b'')
            old = path.stat().st_ino
            row = self.invoke(kind, folder, 'raise AssertionError("must not run")')
            self.assertIsNone(row['returncode'])
            self.assertIn('FileExistsError', row['error'])
            self.assertNotIn('invocation_started', row['stream_evidence'])
            self.assertEqual(old, path.stat().st_ino)
            self.assertEqual(b'', path.read_bytes())

    def test_preexisting_nonempty_stderr_rejects_without_changing_its_bytes(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            path = folder / 'probe.stderr.log'; path.write_bytes(b'retained prior stream')
            old = identity(path)
            row = self.invoke(kind, folder, 'raise AssertionError("must not run")')
            self.assertIsNone(row['returncode'])
            self.assertIn('FileExistsError', row['error'])
            self.assertEqual(old, identity(path))

    def test_preexisting_output_symlink_is_not_followed(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            target = folder / 'target.bin'; target.write_bytes(b'protected target')
            path = folder / 'probe.stdout.log'; path.symlink_to(target.name)
            row = self.invoke(kind, folder)
            self.assertIsNone(row['returncode'])
            self.assertIn('FileExistsError', row['error'])
            self.assertEqual(b'protected target', target.read_bytes())
            # Retain an inert descriptor instead of a live symlink in the proof capsule.
            link = os.readlink(path); path.unlink()
            (folder / 'symlink-description.json').write_text(json.dumps({'path': path.name, 'target': link, 'retired_after_assertions': True}) + '\n')

    def test_preexisting_before_witness_rejects_before_creating_streams(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            path = folder / 'probe.filesystem-before.log'; path.write_bytes(b'')
            row = self.invoke(kind, folder)
            self.assertIsNone(row['returncode'])
            self.assertIn('FileExistsError', row['error'])
            self.assertFalse((folder / 'probe.stdout.log').exists())

    def test_child_replaced_stdout_inode_rejects_after_actual_exit_zero(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            row = self.invoke(kind, folder, 'import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.unlink(); p.write_bytes(b"substituted")', [folder / 'probe.stdout.log'])
            self.assertEqual(0, row['returncode'])
            self.assertIn('error', row)
            self.assertTrue(row['stream_evidence']['cleanup_errors'])
            self.assertEqual(b'substituted', (folder / 'probe.stdout.log').read_bytes())

    def test_child_added_hardlink_rejects_changed_link_ownership(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            row = self.invoke(kind, folder, 'import os,sys; os.link(sys.argv[1], sys.argv[2])',
                [folder / 'probe.stdout.log', folder / 'borrowed.log'])
            self.assertEqual(0, row['returncode'])
            self.assertIn('ownership changed', row['error'])
            self.assertEqual(2, row['stream_evidence']['streams']['stdout']['final_stat']['links'])

    def test_child_past_mtime_fails_actual_witness_bracket_without_slack(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            row = self.invoke(kind, folder, 'import os,sys; os.utime(sys.argv[1], ns=(1,1))', [folder / 'probe.stdout.log'])
            self.assertEqual(0, row['returncode'])
            self.assertIn('did not bracket', row['error'])
            self.assertFalse(row['stream_evidence']['filesystem_bracket_complete'])
            self.assertEqual(16, len(row['stream_evidence']['after_witnesses']))
            self.assertEqual(1, row['stream_evidence']['streams']['stdout']['final_stat']['mtime_ns'])

    def test_child_borrowed_after_witness_is_not_reopened(self):
        for kind in ('numeric', 'wrapper'):
            folder = self.directory(kind)
            row = self.invoke(kind, folder, 'import os,sys; os.link(sys.argv[1], sys.argv[2])',
                [folder / 'probe.filesystem-before.log', folder / 'probe.filesystem-after-00.log'])
            self.assertEqual(0, row['returncode'])
            self.assertIn('FileExistsError', row['error'])
            self.assertFalse(row['stream_evidence']['filesystem_bracket_complete'])


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    source_files = [PROJECT / 'day_numeric_dex_controls.py', TOOLS / 'run_acceptance.py', Path(__file__).resolve()]
    before = {str(path): identity(path) for path in source_files}
    started = datetime.now(timezone.utc).isoformat()
    with (OUT / 'unittest.log').open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProducerControls))
    report = {'scope': __doc__, 'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
              'errors': [{'test': str(t), 'traceback': text} for t, text in result.errors],
              'failures': [{'test': str(t), 'traceback': text} for t, text in result.failures],
              'source_before': before, 'source_after': {str(path): identity(path) for path in source_files},
              'actual_process_records': ProducerControls.records,
              'old_precise_wall_clock_rejections_among_new_empty_streams': sum(
                  not row['row']['started_unix_ns'] <= receipt['final_stat']['mtime_ns'] <= row['row']['ended_unix_ns']
                  for row in ProducerControls.records if 'eight_real_empty' in row['test']
                  for receipt in row['row']['stream_evidence']['streams'].values())}
    (OUT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('passed', 'tests_run', 'old_precise_wall_clock_rejections_among_new_empty_streams')}))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
