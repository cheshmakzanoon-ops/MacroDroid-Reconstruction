#!/usr/bin/env python3
"""Retain one bounded local tooling-only validation, including every source byte."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path('/dev/shm/day-numeric-hosted-01')


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    name = sys.argv[1]
    if not re.fullmatch(r'validation-[0-9]{2}', name):
        raise ValueError('Invalid owned evidence folder')
    output = ROOT / 'reports' / name
    output.mkdir()
    (output / 'tmp').mkdir()
    sources = []
    for path in sorted((ROOT / 'source').rglob('*')):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise ValueError('Unexpected source alias')
        rel = path.relative_to(ROOT / 'source').as_posix()
        destination = output / 'executed-source' / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        sources.append({'path': rel, **identity(path)})
    (output / 'source-bindings.json').write_text(json.dumps(sources, indent=2) + '\n')
    command = ['python3', '-B', '-m', 'unittest', 'discover', '-s',
               str(ROOT / 'source/tools/day_numeric_acceptance'), '-p', 'test_*.py', '-v']
    report = {'schema': 1, 'scope': 'Hosted policy controls only; no full build, Java/D8 execution or Android execution',
              'argv': command, 'cwd': str(ROOT), 'started_utc': datetime.now(timezone.utc).isoformat(),
              'source_files': sources, 'timeout_seconds': 60, 'passed': False}
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TMPDIR=str(output / 'tmp'))
    try:
        with (output / 'host-tests.stdout.log').open('xb') as out, (output / 'host-tests.stderr.log').open('xb') as err:
            completed = subprocess.run(command, cwd=ROOT, env=env, stdout=out, stderr=err, timeout=60)
        report['returncode'] = completed.returncode
        text = (output / 'host-tests.stderr.log').read_text()
        summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
        report['individual_successes'] = len(re.findall(r' \.\.\. ok$', text, re.M))
        report['summary'] = summaries
        report['sources_unchanged'] = all(identity(ROOT / 'source' / row['path']) ==
                                          {k: row[k] for k in ('bytes', 'sha256')} for row in sources)
        report['passed'] = (completed.returncode == 0 and report['sources_unchanged'] and len(summaries) == 1
                            and int(summaries[0][0]) == report['individual_successes'] and text.rstrip().endswith('\nOK'))
    except Exception as error:
        report['error'] = repr(error)
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        report['streams'] = [{'path': name, **identity(output / name)}
                             for name in ('host-tests.stdout.log', 'host-tests.stderr.log') if (output / name).is_file()]
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report.get(k) for k in ('passed', 'returncode', 'individual_successes', 'summary', 'error')}, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
