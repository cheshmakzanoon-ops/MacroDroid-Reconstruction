#!/usr/bin/env python3
"""Compile and execute exact exception-observation controls on the bound host classpath."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import time
import traceback

HERE = Path(__file__).resolve().parent
JDK = HERE.parent / 'tooling/jdk21'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = HERE / 'reports/exception-conformance-07'
    output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix='macrodroid-video-exception-controls-'))
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Message-form/observation controls only; no app method or Android execution.',
        'app_method_executions': 0, 'original_coverage_credit_added': 0, 'commands': []}
    try:
        study_root = HERE / 'reports/original-jvm-07-cast-source'
        study = json.loads((study_root / 'result.json').read_text())
        if study['parity']['failedCases'] != 0 or study['parity']['cases'] != 1118:
            raise RuntimeError('Expected fresh narrowed-harness study required')
        harness = Path(study['private_work']) / 'harnessclasses'
        draft = json.loads(Path(study['host_compilation']['result']).read_text())
        host = Path(draft['private_work']) / 'classes'
        jar = Path(study['tool_jar']['path'])
        if sha(jar) != study['tool_jar']['sha256']:
            raise RuntimeError('Tool classpath differs')
        class_bindings = []
        for archive, directory, prefix in [(study_root / study['compiled_harness_archive']['path'], harness, 'harnessclasses/'),
            (Path(study['host_compilation']['result']).parent / draft['compiled_class_archive']['path'], host, 'classes/')]:
            members = set()
            with tarfile.open(archive, 'r:gz') as stream:
                for member in stream:
                    if member.isfile() and member.name.startswith(prefix):
                        relative = member.name[len(prefix):]; path = directory / relative
                        data = stream.extractfile(member).read()
                        if relative in members or path.is_symlink() or path.read_bytes() != data:
                            raise RuntimeError('Bound compiled class differs')
                        members.add(relative); class_bindings.append({'path': str(path), 'sha256': sha(path)})
            if members != {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}:
                raise RuntimeError('Classpath has an extra or missing class')
        (output / 'class-bindings.json').write_text(json.dumps(class_bindings, indent=2) + '\n')
        source = HERE / 'tests/java/VideoExceptionConformance.java'
        copied = output / source.name; shutil.copyfile(source, copied)
        report['source_sha256'] = sha(copied)
        report['study_result_sha256'] = sha(study_root / 'result.json')
        classes = private / 'classes'; classes.mkdir()
        cp = ':'.join(map(str, (jar, harness, host)))
        def run(label, argv):
            command = list(map(str, argv)); started = time.monotonic()
            out, err = output / (label + '.stdout.txt'), output / (label + '.stderr.txt')
            with out.open('wb') as stdout, err.open('wb') as stderr:
                completed = subprocess.run(command, stdout=stdout, stderr=stderr, cwd=private, timeout=180)
            report['commands'].append({'label': label, 'argv': command, 'returncode': completed.returncode,
                'timeout_seconds': 180, 'seconds': round(time.monotonic() - started, 6),
                'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
            if completed.returncode != 0:
                raise RuntimeError(label + ' failed')
        run('compile', [JDK / 'bin/javac', '-cp', cp, '-d', classes, copied])
        run('controls', [JDK / 'bin/java', '-XX:-OmitStackTraceInFastThrow', '-Xmx512m', '-cp', str(classes) + ':' + cp,
                         'VideoExceptionConformance', output / 'controls.json'])
        controls = json.loads((output / 'controls.json').read_text())
        if not controls['passed'] or controls['controls'] != 68 or controls['appMethodExecutions'] != 0:
            raise RuntimeError('Expected all 68 bounded observation controls')
        shutil.copyfile(classes / 'VideoExceptionConformance.class', output / 'VideoExceptionConformance.class')
        report['every_bound_class_unchanged'] = all(sha(Path(item['path'])) == item['sha256'] for item in class_bindings)
        report['source_unchanged'] = sha(source) == report['source_sha256']
        if not report['every_bound_class_unchanged'] or not report['source_unchanged']:
            raise RuntimeError('Control input changed')
        report['controls'] = 68; report['passed'] = True
        report['status'] = 'ALL_68_EXACT_EXCEPTION_OBSERVATION_CONTROLS_PASSED'
    except Exception as error:
        report['status'] = 'EXCEPTION_OBSERVATION_CONTROLS_FAILED'; report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n'); print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
