from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
import traceback

from prepare_source import ROOT, JAR, identity, write

JDK = Path('/workspace/scratch/4130730d15aa/tooling/jdk21/bin')


def clock():
    return {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'unix_ns': time.time_ns(), 'monotonic_ns': time.monotonic_ns()}


def inventory(root):
    return {p.relative_to(root).as_posix(): identity(p) for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    out = ROOT / 'controls-01'
    out.mkdir(exist_ok=False)
    shutil.copyfile(Path(__file__), out / 'executed-wrapper.py')
    (out / 'tmp').mkdir()
    environment = {'PATH': str(JDK) + ':/usr/local/bin:/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
                   'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUTF8': '1', 'TMPDIR': str(out / 'tmp')}
    commands = []
    result = {'schema': 1, 'status': 'BOUNDARY_CONTROLS_RUNNING', 'passed': False, 'started': clock(),
              'application_executions': 0, 'android_runtime_executed': False, 'commands': commands}

    def run(name, argv, expected):
        folder = out / name
        folder.mkdir()
        record = {'name': name, 'argv': [str(a) for a in argv], 'cwd': str(ROOT), 'timeout_seconds': 120,
                  'environment': environment, 'expected_returncode': expected, 'started': clock()}
        write(folder / 'command.json', record)
        try:
            with (folder / 'stdout.log').open('xb') as stdout, (folder / 'stderr.log').open('xb') as stderr:
                proc = subprocess.run(record['argv'], cwd=ROOT, env=environment, timeout=120, stdout=stdout, stderr=stderr)
            record.update(returncode=proc.returncode, timed_out=False)
        except subprocess.TimeoutExpired:
            record.update(returncode=None, timed_out=True)
            raise
        finally:
            record['finished'] = clock()
            record['stdout'] = identity(folder / 'stdout.log')
            record['stderr'] = identity(folder / 'stderr.log')
            commands.append(record)
            write(folder / 'result.json', record)
        assert record['returncode'] == expected, (name, record['returncode'], expected)

    try:
        run('01-prepare', [sys.executable, '-B', ROOT / 'prepare_source.py'], 0)
        stage = ROOT / 'stage-01'
        before = inventory(stage)
        binaries = {'java': identity(JDK / 'java'), 'javac': identity(JDK / 'javac'), 'jar': identity(JAR),
                    'python': identity(Path(sys.executable).resolve())}
        write(out / 'runtime-inputs-before.json', binaries)
        write(out / 'source-inputs-before.json', before)
        run('02-java-version', [JDK / 'java', '-version'], 0)
        run('03-javac-version', [JDK / 'javac', '-version'], 0)
        classes = out / 'classes'
        classes.mkdir()
        runtime = stage / 'inputs/runtime-classes'
        cp = os.pathsep.join(str(p) for p in [JAR, runtime / 'tools/classes', runtime / 'build/java/hostclasses'])
        run('04-compile', [JDK / 'javac', '-encoding', 'UTF-8', '-cp', cp, '-d', classes,
                          stage / 'control-source/UiReportSerializationControl.java'], 0)
        actual_cp = os.pathsep.join([str(classes), cp])
        for name, mode, code in [('05-original-counterexample', 'original', 2), ('06-corrected-boundary', 'corrected', 0)]:
            run(name, [JDK / 'java', '-Xverify:all', '-cp', actual_cp, 'UiReportSerializationControl', mode,
                       stage / 'inputs', out / (mode + '-output')], code)
        original = json.loads((out / 'original-output/result.json').read_bytes())
        corrected = json.loads((out / 'corrected-output/result.json').read_bytes())
        assert original['passed'] is False and original['observerStrictEquality'] is False
        assert original['matchesOriginalClosedUiRecord'] is True and len(original['absentNullReturnIndices']) == 5
        assert corrected['passed'] is True and corrected['observerStrictEquality'] is True
        assert corrected['matchesOriginalClosedUiRecord'] is False and corrected['absentNullReturnIndices'] == []
        for value in (original, corrected):
            assert value['actualCompiledObserverMatchesClosedStandalone'] is True and value['nonNullReturnIndexPreserved'] is True
            assert value['applicationExecutions'] == value['applicationCoverageCredit'] == 0
            assert value['androidRuntime'] is False and value['completeUiHarnessExecuted'] is False
        assert inventory(stage) == before
        assert {k: identity(p) for k, p in [('java', JDK / 'java'), ('javac', JDK / 'javac'), ('jar', JAR),
                ('python', Path(sys.executable).resolve())]} == binaries
        result.update(status='ORIGINAL_FIVE_NULL_KEY_LOSS_REPRODUCED_AND_CORRECTED_WRITER_PASSED', passed=True,
                      original=original, corrected=corrected, source_input_files_unchanged=len(before),
                      runtime_inputs_unchanged=True, exact_ui_source_change_lines=1,
                      full_acceptance_executed=False, strict_finalizer_modified=False)
    except Exception as exc:
        result.update(status='BOUNDARY_CONTROL_ATTEMPT_FAILED', error_type=type(exc).__name__, error=str(exc))
        (out / 'exception.txt').write_text(traceback.format_exc())
    finally:
        result['finished'] = clock()
        write(out / 'result.json', result)
    print(json.dumps({k: result.get(k) for k in ('status', 'passed', 'source_input_files_unchanged', 'error_type', 'error')}))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
