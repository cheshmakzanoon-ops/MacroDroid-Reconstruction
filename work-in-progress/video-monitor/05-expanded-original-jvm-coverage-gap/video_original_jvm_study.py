#!/usr/bin/env python3
"""Use exact already-compiled host inputs for a fresh one-method differential study."""
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
ORIGINAL_SHA = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--host-draft', required=True, type=Path)
    parser.add_argument('--original-apk', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--jdk', required=True, type=Path)
    args = parser.parse_args()
    project, output = args.project.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix='macrodroid-video-study-'))
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Original/JVM one-method proof only, reusing byte-verified compiled host inputs; no APK build or Android execution.',
        'project_read_only': str(project), 'private_work': str(private), 'registered': False,
        'android_executed': False, 'rebuilt_dex_compared': False, 'commands': []}
    inputs = []
    env = {**os.environ, 'JAVA_HOME': str(args.jdk.resolve()),
           'PATH': str(args.jdk.resolve() / 'bin') + os.pathsep + os.environ.get('PATH', '')}

    def run(label, command, allowed=(0,), timeout=300):
        command = [str(value) for value in command]
        out, err = output / (label + '.stdout.txt'), output / (label + '.stderr.txt')
        started = time.monotonic()
        with out.open('wb') as stdout, err.open('wb') as stderr:
            completed = subprocess.run(command, cwd=private, env=env, stdout=stdout, stderr=stderr, timeout=timeout)
        item = {'label': label, 'argv': command, 'returncode': completed.returncode,
            'timeout_seconds': timeout, 'seconds': round(time.monotonic() - started, 6),
            'stdout': {'path': out.name, 'sha256': sha(out)}, 'stderr': {'path': err.name, 'sha256': sha(err)}}
        report['commands'].append(item)
        save(output / 'result.json', report)
        if completed.returncode not in allowed:
            raise RuntimeError(label + ' failed with code ' + str(completed.returncode))
        return completed.returncode

    def copy(source, relative):
        target = private / 'inputs' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        digest = sha(source)
        if source.is_symlink():
            raise RuntimeError('Input symlink refused')
        shutil.copyfile(source, target)
        if sha(target) != digest:
            raise RuntimeError('Copied input differs')
        inputs.append({'path': relative, 'source': str(source), 'copy': str(target),
                      'bytes': target.stat().st_size, 'sha256': digest})
        return target

    try:
        draft_path = args.host_draft.resolve()
        draft = json.loads(draft_path.read_text())
        host_inputs = json.loads((draft_path.parent / 'inputs.json').read_text())['files']
        if draft.get('passed') is not True or draft['status'] != 'UNREGISTERED_DRAFT_COMPILED_DIFFERENTIAL_PENDING':
            raise RuntimeError('Successful draft compilation prerequisite required')
        host = Path(draft['private_work']) / 'classes'
        compiled_archive = draft_path.parent / draft['compiled_class_archive']['path']
        if sha(compiled_archive) != draft['compiled_class_archive']['sha256']:
            raise RuntimeError('Compiled host archive changed')
        archive_names = set()
        with tarfile.open(compiled_archive, 'r:gz') as stream:
            for member in stream:
                if not member.isfile():
                    continue
                data = stream.extractfile(member).read()
                relative = Path(member.name).relative_to('classes').as_posix()
                actual = host / relative
                if relative in archive_names or actual.is_symlink() or actual.read_bytes() != data:
                    raise RuntimeError('Compiled classpath differs from recorded javac output')
                archive_names.add(relative)
        if archive_names != {path.relative_to(host).as_posix() for path in host.rglob('*') if path.is_file()}:
            raise RuntimeError('Compiled host classpath has an extra or missing file')
        for item in host_inputs:
            if sha(Path(item['source'])) != item['sha256'] or sha(Path(item['private_copy'])) != item['sha256']:
                raise RuntimeError('A compiled source differs from the proposed current overlay')
        report['host_compilation'] = {'result': str(draft_path), 'result_sha256': sha(draft_path),
            'compiled_classes': len(archive_names), 'archive_sha256': sha(compiled_archive),
            'every_class_file_byte_verified': True, 'every_host_source_unchanged': True}
        apk = args.original_apk.resolve()
        if sha(apk) != ORIGINAL_SHA:
            raise RuntimeError('Original APK identity differs')
        report['original_apk'] = {'path': str(apk), 'bytes': apk.stat().st_size, 'sha256': ORIGINAL_SHA}
        jar = project / 'tools/lib/jadx-r2721.4574686-all.jar'
        report['tool_jar'] = {'path': str(jar), 'bytes': jar.stat().st_size, 'sha256': sha(jar)}
        sources = []
        for name in ('BytecodeOracle.java', 'ParityTests.java', 'UiParityTests.java', 'SceneParityCases.java',
                     'PluginParityCases.java', 'PluginUploadParityCases.java', 'WidgetParityCases.java',
                     'VideoParityCases.java', 'VideoParityStudy.java'):
            relative = 'tests/java/' + name
            source = HERE / relative if (HERE / relative).is_file() else project / relative
            sources.append(copy(source, relative))
        extractor = copy(project / 'tools/src/ExtractOracle.java', 'tools/src/ExtractOracle.java')
        entry = copy(HERE / 'proposed-method-entry.json', 'proposed-method-entry.json')
        save(output / 'inputs.json', {'files': inputs, 'mutable_hardlinks': False})
        tools = private / 'toolclasses';tools.mkdir()
        harness = private / 'harnessclasses';harness.mkdir()
        run('compile-extractor', ['javac', '-cp', jar, '-d', tools, extractor])
        run('compile-harness', ['javac', '-cp', str(jar) + os.pathsep + str(host), '-d', harness, *sources])
        fixture_root = private / 'fixture-project'
        (fixture_root / 'source').mkdir(parents=True)
        save(fixture_root / 'source/java-method-map.json', [json.loads(entry.read_text())])
        run('extract-original', ['java', '-Xmx512m', '-cp', str(jar) + os.pathsep + str(tools), 'ExtractOracle', fixture_root, apk])
        fixture = fixture_root / 'tests/fixtures/original-methods.dex'
        shutil.copyfile(fixture, output / 'original-video-monitor.dex')
        report['original_fixture'] = {'path': 'original-video-monitor.dex', 'bytes': fixture.stat().st_size, 'sha256': sha(fixture)}
        classpath = os.pathsep.join(str(path) for path in (jar, harness, host))
        code = run('original-jvm', ['java', '-XX:-OmitStackTraceInFastThrow', '-Xmx512m', '-cp', classpath,
            'VideoParityStudy', entry, fixture, output / 'parity.json'], allowed=(0, 2))
        parity = json.loads((output / 'parity.json').read_text())
        report['passed'] = code == 0 and parity['passed'] is True
        report['status'] = 'ORIGINAL_JVM_COVERAGE_PASSED' if report['passed'] else 'ORIGINAL_JVM_GATE_FAILED'
        report['parity'] = {key: value for key, value in parity.items() if key not in ('failures', 'failedCaseLabels', 'generatedEscapedMessageExclusions')}
        for item in inputs:
            if sha(Path(item['copy'])) != item['sha256'] or sha(Path(item['source'])) != item['sha256']:
                raise RuntimeError('Study input changed during execution')
        archive = output / 'compiled-harness-and-toolclasses.tar.gz'
        with tarfile.open(archive, 'w:gz') as stream:
            stream.add(harness, arcname='harnessclasses');stream.add(tools, arcname='toolclasses')
        report['compiled_harness_archive'] = {'path': archive.name, 'bytes': archive.stat().st_size, 'sha256': sha(archive)}
        report['copied_inputs_unchanged'] = True
        return 0 if report['passed'] else 2
    except Exception as error:
        report['status'] = 'STUDY_FAILED';report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps({key: value for key, value in report.items() if key != 'commands'}, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
