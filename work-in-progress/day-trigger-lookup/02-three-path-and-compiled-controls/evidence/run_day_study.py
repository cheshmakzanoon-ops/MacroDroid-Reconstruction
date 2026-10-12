#!/usr/bin/env python3
"""Measure a fresh original/JVM study with exact source, class, tool, and fixture bindings."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess, time, traceback

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / 'inputs'
JDK = ROOT.parent / 'tooling/jdk21'

def identity(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''): h.update(block)
    return {'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def tree(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink(): raise RuntimeError('Unexpected input symlink: ' + str(path))
        if path.is_file(): result[path.relative_to(root).as_posix()] = identity(path)
    return result

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output).resolve()
    if output.exists(): raise RuntimeError('Output already exists; retain closed attempts: ' + str(output))
    if shutil.disk_usage(ROOT).free < 96 * 1024 * 1024: raise RuntimeError('Insufficient free space for bounded study')
    output.mkdir(parents=True)
    result = {'startedUtc': now(), 'scope': 'Private original/JVM study; no active registration or APK changes.', 'commands': []}
    before = tree(INPUTS)
    (output / 'input-identities-before.json').write_text(json.dumps(before, indent=2) + '\n')
    shutil.copyfile(__file__, output / 'run_day_study.py')
    pins = json.loads((INPUTS / 'preserved-input-pins.json').read_text())
    external = {}
    for role in ('originalApk', 'externalToolchainJar', 'externalJdkRelease'):
        pin = pins[role]; path = Path(pin['path']); observed = identity(path)
        if observed != {key: pin[key] for key in ('bytes', 'sha256')}: raise RuntimeError('External input changed: ' + role)
        external[role] = {'path': str(path), **observed}
    for role in ('java', 'javac'):
        path = JDK / 'bin' / role
        external[role] = {'path': str(path), **identity(path)}
    external['jdkModules'] = {'path': str(JDK / 'lib/modules'), **identity(JDK / 'lib/modules')}
    (output / 'external-input-identities.json').write_text(json.dumps(external, indent=2) + '\n')

    def run(name, argv, timeout=120, expected=0):
        started = time.monotonic(); item = {'name': name, 'argv': [str(x) for x in argv], 'startedUtc': now(), 'timeoutSeconds': timeout}
        stdout = output / (name + '.stdout.txt'); stderr = output / (name + '.stderr.txt')
        with stdout.open('wb') as out, stderr.open('wb') as err:
            try:
                proc = subprocess.run(item['argv'], cwd=ROOT, stdout=out, stderr=err, timeout=timeout,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                item['returncode'] = proc.returncode
            except subprocess.TimeoutExpired:
                item['returncode'] = None; item['timedOut'] = True
        item.update({'finishedUtc': now(), 'durationSeconds': time.monotonic() - started,
                     'stdout': {'path': stdout.name, **identity(stdout)}, 'stderr': {'path': stderr.name, **identity(stderr)}})
        result['commands'].append(item)
        (output / 'command-ledger.json').write_text(json.dumps(result['commands'], indent=2) + '\n')
        if item['returncode'] != expected: raise RuntimeError('Unexpected command result: ' + name)

    try:
        jar = Path(pins['externalToolchainJar']['path'])
        host = output / 'hostclasses'; harness = output / 'harnessclasses'
        host.mkdir(); harness.mkdir()
        run('java-version', [JDK / 'bin/java', '-version'])
        host_sources = sorted((INPUTS / 'host').rglob('*.java')) + sorted((INPUTS / 'source/java').rglob('*.java'))
        run('compile-host-helper', [JDK / 'bin/javac', '--release', '8', '-g:none', '-Xlint:-options', '-d', host, *host_sources])
        classpath = os.pathsep.join(map(str, (jar, host)))
        run('compile-study', [JDK / 'bin/javac', '-cp', classpath, '-d', harness,
                              INPUTS / 'BytecodeOracle.java', INPUTS / 'DayLookupStudy.java', INPUTS / 'ExtractDayLookupFixture.java'])
        classpath = os.pathsep.join(map(str, (jar, host, harness)))
        original = output / 'original-selected.dex'
        run('extract-original-methods', [JDK / 'bin/java', '-Xmx768m', '-cp', classpath, 'ExtractDayLookupFixture',
                                         pins['originalApk']['path'], original, output / 'original-method-inventory.json'])
        class_pins = {}
        for root in (host, harness):
            for path in sorted(root.rglob('*.class')):
                name = path.relative_to(root).as_posix()[:-6].replace('/', '.')
                if name in class_pins: raise RuntimeError('Duplicate compiled class: ' + name)
                class_pins[name] = {'path': str(path), **identity(path)}
        config = {'originalDex': str(original), 'originalDexSha256': identity(original)['sha256'], 'classPins': class_pins}
        (output / 'study-config.json').write_text(json.dumps(config, indent=2) + '\n')
        run('positive-original-java', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', classpath,
                                       'DayLookupStudy', output / 'study-config.json', output / 'positive-report.json'])
        report = json.loads((output / 'positive-report.json').read_text())
        if not report['passed']: raise RuntimeError('Positive report did not pass')
        # A wrong loaded-helper identity must reject before a report is written.
        wrong = json.loads(json.dumps(config))
        wrong['classPins']['recovered.ui.DayTriggerLookupMethods']['sha256'] = '0' * 64
        (output / 'wrong-helper-config.json').write_text(json.dumps(wrong, indent=2) + '\n')
        run('wrong-helper-origin-control', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', classpath,
                                            'DayLookupStudy', output / 'wrong-helper-config.json', output / 'wrong-helper-report.json'], expected=1)
        if (output / 'wrong-helper-report.json').exists(): raise RuntimeError('Wrong helper identity produced a report')
        if 'Wrong loaded class hash: recovered.ui.DayTriggerLookupMethods' not in (output / 'wrong-helper-origin-control.stderr.txt').read_text():
            raise RuntimeError('Origin control rejected for the wrong reason')
        run('positive-restored', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', classpath,
                                  'DayLookupStudy', output / 'study-config.json', output / 'restored-report.json'])
        if identity(output / 'positive-report.json') != identity(output / 'restored-report.json'):
            raise RuntimeError('Positive report was not restored exactly')
        for name, pin in class_pins.items():
            if identity(Path(pin['path'])) != {key: pin[key] for key in ('bytes', 'sha256')}:
                raise RuntimeError('Compiled class changed: ' + name)
        if tree(INPUTS) != before: raise RuntimeError('Input sources changed during the run')
        for role, pin in external.items():
            if identity(Path(pin['path'])) != {key: pin[key] for key in ('bytes', 'sha256')}:
                raise RuntimeError('External input changed: ' + role)
        result.update({'status': 'ORIGINAL_JAVA_STUDY_PASSED', 'passed': True,
                       'cases': report['cases'], 'executionPaths': report['executionPaths'],
                       'independentExpectedChecks': report['independentExpectedChecks'],
                       'mismatchCount': report['mismatchCount'], 'unsupportedCount': report['unsupportedCount'],
                       'originalCoverage': report['originalCoverage'], 'positiveReport': identity(output / 'positive-report.json'),
                       'originalFixture': identity(original), 'originControlRejected': True,
                       'positiveReportRestoredExactly': True, 'allInputAndCompiledBytesUnchanged': True,
                       'compiledClassCount': len(class_pins)})
    except BaseException as error:
        result.update({'status': 'STUDY_FAILED_RETAINED', 'passed': False, 'error': str(error)})
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        result['finishedUtc'] = now()
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({key: value for key, value in result.items() if key not in ('commands', 'originalCoverage')}, indent=2))
    if not result['passed']: raise SystemExit(1)

if __name__ == '__main__': main()
