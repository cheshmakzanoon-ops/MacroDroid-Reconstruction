#!/usr/bin/env python3
"""Compile a private small source overlay; no active input or APK is changed."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import time

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--jdk', required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix='macrodroid-video-host-'))
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Private javac-only source draft; original/JVM differential, rebuilt and Android proof remain pending.',
        'project_read_only': str(project), 'private_work': str(private),
        'registered': False, 'app_method_executed': False, 'apk_built': False, 'android_executed': False,
        'mutable_hardlinks': False, 'commands': []}
    inputs = []
    try:
        selected = {}
        for tree in ('source/java', 'test-support/java'):
            for root in (project, HERE):
                for path in (root / tree).rglob('*.java'):
                    selected[path.relative_to(root).as_posix()] = path
        sources = []
        for relative, source in sorted(selected.items()):
            target = private / 'inputs' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = sha(source)
            if source.is_symlink():
                raise RuntimeError('Unexpected source symlink')
            shutil.copyfile(source, target)
            if sha(target) != digest or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
                raise RuntimeError('Private byte copy failed')
            sources.append(target)
            inputs.append({'path': relative, 'source': str(source), 'private_copy': str(target),
                'origin': 'video-overlay' if source.is_relative_to(HERE) else 'combined-baseline',
                'bytes': source.stat().st_size, 'sha256': digest})
        save(output / 'inputs.json', {'files': inputs, 'every_private_copy_hash_verified': True, 'mutable_hardlinks': False})
        classes = private / 'classes'
        classes.mkdir()
        argfile = private / 'source-files.args'
        argfile.write_text(''.join('"' + str(path).replace('\\', '\\\\').replace('"', '\\"') + '"\n' for path in sources))
        command = [str(args.jdk.resolve() / 'bin/javac'), '--release', '8', '-g:none', '-Xlint:-options',
                   '-d', str(classes), '@' + str(argfile)]
        started = time.monotonic()
        with (output / 'javac.stdout.txt').open('wb') as out, (output / 'javac.stderr.txt').open('wb') as err:
            completed = subprocess.run(command, cwd=private, stdout=out, stderr=err, timeout=180)
        report['commands'].append({'argv': command, 'returncode': completed.returncode,
            'timeout_seconds': 180, 'seconds': round(time.monotonic() - started, 6),
            'stdout_sha256': sha(output / 'javac.stdout.txt'), 'stderr_sha256': sha(output / 'javac.stderr.txt')})
        if completed.returncode != 0:
            raise RuntimeError('Draft host compilation failed')
        report['source_files'] = len(sources)
        report['overlay_java_files'] = sum(item['origin'] == 'video-overlay' for item in inputs)
        report['class_files'] = len(list(classes.rglob('*.class')))
        report['all_inputs_unchanged'] = all(sha(Path(item['source'])) == item['sha256'] and
            sha(Path(item['private_copy'])) == item['sha256'] for item in inputs)
        if not report['all_inputs_unchanged']:
            raise RuntimeError('Input changed during compilation')
        archive = output / 'compiled-host-classes.tar.gz'
        with tarfile.open(archive, 'w:gz') as stream:
            stream.add(classes, arcname='classes')
        report['compiled_class_archive'] = {'path': archive.name, 'bytes': archive.stat().st_size, 'sha256': sha(archive)}
        report['status'] = 'UNREGISTERED_DRAFT_COMPILED_DIFFERENTIAL_PENDING'
        report['passed'] = True
    except Exception as error:
        report['status'] = 'DRAFT_COMPILE_FAILED'
        report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
