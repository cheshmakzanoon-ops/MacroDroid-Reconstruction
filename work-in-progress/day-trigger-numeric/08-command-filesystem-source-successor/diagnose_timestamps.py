#!/usr/bin/env python3
"""Bounded read-only replay of unchanged timestamp guards; no Java or app build."""
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-run-38232050667/extracted')
OUTPUT = ROOT / 'reports' / '01-unchanged-guard-diagnosis'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def exact_ns(text):
    delta = datetime.fromisoformat(text) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (delta.days * 86400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1000


def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    old = ROOT / 'baseline-source'
    old.mkdir(exist_ok=False)
    raw_rows = {}
    for path in sorted(RAW.rglob('*')):
        if path.is_file():
            name = path.relative_to(RAW).as_posix()
            raw_rows[name] = identity(path)
            if name.startswith('job-source/'):
                dest = old / name[len('job-source/'):]
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, dest)
    sys.path.insert(0, str(old / 'tools/day_numeric_acceptance'))
    tests = importlib.import_module('test_day_numeric_acceptance')
    verify = importlib.import_module('verify')
    runner = importlib.import_module('run_acceptance')
    tmp = ROOT / 'tmp'
    tmp.mkdir(exist_ok=False)
    tempfile.tempdir = str(tmp)
    result = {'scope': 'Unchanged guard diagnosis only; synthetic fixture replays and eight actual empty Python subprocesses. No Java/D8/build/Android.',
              'started_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
              'kernel': platform.release(), 'filesystem': 'tmpfs at /dev/shm; not the hosted Ubuntu filesystem',
              'raw_files': raw_rows, 'conversion_examples': [], 'fixtures': [], 'empty_children': []}
    for text in ['2026-10-12T09:46:48.798705+00:00', '2026-10-12T09:46:48.000001+00:00',
                 '2026-10-12T09:46:48.000002+00:00', '2026-10-12T09:46:48.000003+00:00']:
        value = verify.epoch_ns(text)
        result['conversion_examples'].append({'iso': text, 'old_epoch_ns': value, 'exact_epoch_ns': exact_ns(text),
                                              'old_error_ns': value - exact_ns(text)})
    preserved = set()
    for index in range(32):
        for label, klass in [('numeric', tests.NumericCommandControls), ('wrapper', tests.WrapperStreamControls)]:
            case = klass()
            case.setUp()
            row = {'iteration': index, 'kind': label, 'file_times': []}
            try:
                if label == 'numeric':
                    report = case.report
                    commands = report['commands']
                    row['outer_end_ns'] = case.end
                else:
                    report = case.execution
                    commands = report['java_versions'] + [report['execution']]
                    row['outer_end_ns'] = verify.epoch_ns(report['finished_utc'])
                    row['last_child_end_ns'] = commands[-1]['ended_unix_ns']
                    row['last_child_minus_outer_end_ns'] = commands[-1]['ended_unix_ns'] - row['outer_end_ns']
                for ci, command in enumerate(commands):
                    start = verify.epoch_ns(command['started_utc']) if label == 'numeric' else command['started_unix_ns']
                    end = verify.epoch_ns(command['ended_utc']) if label == 'numeric' else command['ended_unix_ns']
                    for stream in ('stdout', 'stderr'):
                        path = case.root / command[stream]['path']
                        st = path.stat()
                        row['file_times'].append({'command_index': ci, 'stream': stream, 'path': command[stream]['path'],
                            'started_ns': start, 'ended_ns': end, 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns,
                            'mtime_minus_start_ns': st.st_mtime_ns - start, 'ctime_minus_start_ns': st.st_ctime_ns - start,
                            'mtime_minus_end_ns': st.st_mtime_ns - end, 'ctime_minus_end_ns': st.st_ctime_ns - end})
                try:
                    case.check()
                    row['accepted'] = True
                except Exception as error:
                    row['accepted'] = False
                    row['error'] = repr(error)
                    if label not in preserved:
                        dest = OUTPUT / ('first-failure-' + label)
                        shutil.copytree(case.root, dest / 'files')
                        (dest / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
                        preserved.add(label)
                result['fixtures'].append(row)
            finally:
                case.tearDown()
    for index in range(8):
        folder = OUTPUT / 'actual-empty-children' / str(index)
        folder.mkdir(parents=True)
        command = [sys.executable, '-B', '-c', 'pass']
        row = runner.run_child(command, folder, os.environ.copy(), folder / 'stdout.log', folder / 'stderr.log', 5)
        row['actual_stream_stats'] = {}
        for stream in ('stdout', 'stderr'):
            st = (folder / (stream + '.log')).stat()
            row['actual_stream_stats'][stream] = {'device': st.st_dev, 'inode': st.st_ino, 'mtime_ns': st.st_mtime_ns,
                'ctime_ns': st.st_ctime_ns, 'mtime_minus_start_ns': st.st_mtime_ns - row['started_unix_ns'],
                'ctime_minus_start_ns': st.st_ctime_ns - row['started_unix_ns'],
                'within_old_child_interval': row['started_unix_ns'] <= st.st_mtime_ns <= row['ended_unix_ns']
                    and row['started_unix_ns'] <= st.st_ctime_ns <= row['ended_unix_ns']}
        result['empty_children'].append(row)
    result['raw_files_unchanged'] = all(identity(RAW / name) == expected for name, expected in raw_rows.items())
    result['baseline_source_unchanged'] = all(identity(old / name[len('job-source/'):]) == expected
        for name, expected in raw_rows.items() if name.startswith('job-source/'))
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUTPUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'scope': result['scope'], 'result': str(OUTPUT / 'result.json'),
        'fixture_failures': {label: sum(not r['accepted'] for r in result['fixtures'] if r['kind'] == label) for label in ('numeric', 'wrapper')},
        'empty_child_interval_failures': sum(not v['within_old_child_interval'] for r in result['empty_children'] for v in r['actual_stream_stats'].values()),
        'raw_files_unchanged': result['raw_files_unchanged'], 'baseline_source_unchanged': result['baseline_source_unchanged']}))


if __name__ == '__main__':
    main()
