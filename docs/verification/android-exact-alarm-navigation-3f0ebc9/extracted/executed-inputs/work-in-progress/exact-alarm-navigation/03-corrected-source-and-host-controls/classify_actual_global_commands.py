#!/usr/bin/env python3
"""Record how the corrected finite grammar classifies the closed real command log."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import stat
import sys
import time

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
SOURCE = ROOT / 'source-01/repository'
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388/extracted/journey')
OUTPUT = ROOT / 'source-01/actual-command-grammar-corrected'
REPORT_SHA = '0d4565b26a98b4a21d4294ae895fc8ac7c3e32dc313767312e8c9d06f64b8d92'


def identity(path, relative_to):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise RuntimeError('Expected a regular input file')
    data = path.read_bytes()
    return {'path': path.relative_to(relative_to).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'mode': '100755' if info.st_mode & 0o111 else '100644'}


def inventory(folder):
    return [identity(path, folder) for path in sorted(folder.rglob('*')) if not path.is_dir()]


def write(name, value):
    with (OUTPUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    OUTPUT.mkdir(exist_ok=False)
    source_before = inventory(SOURCE)
    reviewed = json.loads((ROOT / 'source-01/attempts/02-global-command-correction/source-before.json').read_text())
    if source_before != reviewed:
        raise RuntimeError('Corrected reviewed source changed before grammar classification')
    report_path = RAW / 'journey.json'
    report_bytes = report_path.read_bytes()
    if hashlib.sha256(report_bytes).hexdigest() != REPORT_SHA:
        raise RuntimeError('Closed real report identity changed')
    report = json.loads(report_bytes)
    evidence_paths = [report_path]
    for run in report['runs']:
        evidence_paths.extend(RAW / run['installed_path'][role]['path'] for role in ('stdout', 'stderr'))
    raw_before = [identity(path, RAW) for path in evidence_paths]
    write('source-before.json', source_before)
    write('read-inputs-before.json', raw_before)
    sys.path[:0] = [str(SOURCE / 'tools/parity_journeys'), str(SOURCE / 'project')]
    import android_compare as proof
    import exact_alarm_journey as alarm
    import editor_journey as runner
    installed = [proof.installed_path(run['installed_path']['returncode'],
                  proof.artifact(RAW, run['installed_path']['stdout']).decode(),
                  proof.artifact(RAW, run['installed_path']['stderr']).decode()) for run in report['runs']]
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    rows = []
    for index, command in enumerate(report['commands']):
        rows.append({'index': index, 'argv': command['argv'],
                     'whole_command_sha256': runner.fingerprint(command),
                     'kind': alarm._command_kind(command['argv'], installed)})
    finished = time.monotonic()
    finished_utc = datetime.now(timezone.utc).isoformat()
    counts = dict(sorted(Counter(row['kind'] for row in rows).items()))
    if len(rows) != 1021 or counts != {'evidence': 991, 'input': 24, 'install': 2, 'launch': 2, 'uninstall': 2}:
        raise RuntimeError('Unexpected actual command inventory')
    write('classified-commands.json', rows)
    raw_after = [identity(path, RAW) for path in evidence_paths]
    source_after = inventory(SOURCE)
    write('read-inputs-after.json', raw_after)
    write('source-after.json', source_after)
    result = {'status': 'ALL_CLOSED_REAL_COMMANDS_CLASSIFIED' if raw_before == raw_after and source_before == source_after else 'FAILED',
              'run_id': 38230072388, 'head_sha': 'e1ade015f938339479216a1a91518e556902fce8',
              'report_sha256': REPORT_SHA, 'report_schema': report['schema'],
              'commands': len(rows), 'counts': counts,
              'started_utc': started_utc, 'finished_utc': finished_utc,
              'started_monotonic': started, 'finished_monotonic': finished,
              'seconds': finished - started,
              'read_inputs_unchanged': raw_before == raw_after, 'source_unchanged': source_before == source_after,
              'classification_only': True, 'schema6_global_ownership_verification_claimed': False,
              'new_android_execution': False, 'full_runtime_1_to_1_established': False,
              'scope': 'Classifies the exact 1,021 commands from the actual schema5 report using the corrected finite grammar. This does not fabricate the new uninstall role or a fourteenth screen.'}
    write('result.json', result)
    shutil.copy2(Path(__file__), OUTPUT / 'executed-classify-actual-global-commands.py')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'ALL_CLOSED_REAL_COMMANDS_CLASSIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
