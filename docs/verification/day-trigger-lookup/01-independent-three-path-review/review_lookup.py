#!/usr/bin/env python3
"""Independent bounded review of one frozen DayTrigger.p0 recovery capsule.

Read frozen sources directly; compile every host/harness class into this run;
extract the original fixture anew; send one helper class through the pinned
production transplant. No active source, cache, registry, or APK is changed.
"""
from pathlib import Path
import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
import traceback
import zipfile

WORKSPACE = Path('/workspace/scratch/4130730d15aa')
FROZEN = WORKSPACE / 'day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls'
CHECKPOINT_SHA = '6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29'
INPUTS = FROZEN / 'inputs'
JDK = WORKSPACE / 'tooling/jdk21'
HELPER = 'recovered.ui.DayTriggerLookupMethods'
TARGET = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;'
METHOD = ('p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)'
          'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;')
ORIGINAL_DEX_SHA = '261b88a32666b00ce1225c1ba03150b39f36edf0d13df5d36e05bcfd1953c568'
HELPER_CLASS_SHA = 'd0ff3559a30190eb120161faa943700d5a2e6bfeaba85cb97807c19fa219ad61'
REBUILT_DEX_SHA = 'cf79aff20187504abf4168c081b0cbd7d80ac664bce7ead175db835d8d06e596'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'bytes': Path(path).stat().st_size, 'sha256': digest.hexdigest()}


def selected_identity(row):
    return {key: row[key] for key in ('bytes', 'sha256')}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')


def hash_files(paths):
    return {str(path): identity(path) for path in paths}


def verify_capsule(output):
    cp = FROZEN / 'checkpoint.json'
    require(identity(cp)['sha256'] == CHECKPOINT_SHA, 'Frozen checkpoint changed')
    checkpoint = json.loads(cp.read_text())
    require(checkpoint['status'] == 'THREE_PATH_AND_COMPILED_CONTROLS_PASSED', 'Unexpected frozen scope')
    require(len(checkpoint['sourceFiles']) == 31 and len(checkpoint['evidenceFiles']) == 150,
            'Unexpected capsule membership')
    paths = [cp]
    for row in checkpoint['sourceFiles']:
        path = FROZEN / row['path']
        require(not path.is_symlink() and identity(path) == selected_identity(row), 'Frozen source changed: ' + row['path'])
        paths.append(path)
    archive = FROZEN / checkpoint['evidenceArchive']['path']
    require(identity(archive) == selected_identity(checkpoint['evidenceArchive']), 'Archive changed')
    paths.append(archive)
    expected = {row['path']: row for row in checkpoint['evidenceFiles']}
    require(len(expected) == 150, 'Duplicate manifest evidence path')
    audit = []
    with tarfile.open(archive, 'r:gz') as stream:
        members = stream.getmembers()
        require(len(members) == 150 and {m.name for m in members} == set(expected), 'Archive membership changed')
        for member in members:
            require(member.isfile() and not member.issym() and not member.islnk(), 'Non-regular archive member')
            require(not Path(member.name).is_absolute() and '..' not in Path(member.name).parts, 'Unsafe archive member')
            data = stream.extractfile(member).read()
            observed = {'bytes': len(data), 'sha256': sha(data)}
            require(observed == selected_identity(expected[member.name]), 'Archive payload changed: ' + member.name)
            audit.append({'path': member.name, 'mode': member.mode, **observed})
        parent = json.load(stream.extractfile('result.json'))
        positive = json.load(stream.extractfile('positive/parity.json'))
        restoration = stream.extractfile('positive-restored/parity.json').read()
        require(sha(restoration) == parent['positiveReport']['sha256'], 'Historical exact restoration changed')
        require(parent['passed'] and parent['cases'] == 371 and parent['executionPaths'] == 3,
                'Historical measured scope changed')
        require(len(parent['commands']) == 35, 'Historical command count changed')
        for command in parent['commands']:
            require(command['returncode'] in (0, 1, 3) and command['timeoutSeconds'] == 120,
                    'Unexpected historical command outcome/bound')
            for key in ('stdout', 'stderr'):
                row = command[key]
                require(row['path'] in expected and selected_identity(row) == selected_identity(expected[row['path']]),
                        'Historical command output binding changed')
        require([x['mismatchCount'] for x in parent['compiledJavaFaults']] == [127, 3, 2, 3, 233, 1, 369, 233, 25, 6],
                'Historical Java fault outcomes changed')
        require([x['mismatchCount'] for x in parent['compiledRebuiltFaults']] == [127, 233],
                'Historical rebuilt fault outcomes changed')
        require(all(x['unsupportedCount'] == 0 and x['referencePathsUnchanged'] for x in
                    parent['compiledJavaFaults'] + parent['compiledRebuiltFaults']), 'Historical fault reference paths changed')
    write_json(output / 'frozen-capsule-audit.json', {
        'checkpoint': {'path': str(cp), **identity(cp)}, 'sourceFilesVerified': len(checkpoint['sourceFiles']),
        'archive': {'path': str(archive), **identity(archive)}, 'archiveMembers': audit,
        'archivePayloadBytes': sum(row['bytes'] for row in audit), 'historicalCommands': 35,
        'historicalJavaFaultMismatches': [127, 3, 2, 3, 233, 1, 369, 233, 25, 6],
        'historicalRebuiltFaultMismatches': [127, 233], 'historicalExactRestorationVerified': True})
    return checkpoint, paths, positive, parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    output = Path(parser.parse_args().output).resolve()
    require(not output.exists(), 'Use a new output directory; previous attempts remain immutable')
    free = shutil.disk_usage(WORKSPACE).free
    require(free >= 96 * 1024 * 1024, 'Less than 96 MiB free; defer bounded study')
    output.mkdir(parents=True)
    started = time.monotonic()
    result = {'status': 'RUNNING', 'startedUtc': now(), 'freeBytesAtStart': free,
              'scope': 'Independent frozen-source review and fresh one-method three-path repeat; no APK build, ART, active registration, or broader coverage claim.',
              'commands': []}
    shutil.copyfile(__file__, output / 'review_lookup.py')
    env = dict(os.environ)
    suppressed = {}
    for key in ('JAVA_TOOL_OPTIONS', '_JAVA_OPTIONS', 'JDK_JAVA_OPTIONS', 'CLASSPATH'):
        if key in env:
            suppressed[key] = {'bytes': len(env[key].encode()), 'sha256': sha(env[key].encode())}
            del env[key]
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    write_json(output / 'launcher-environment-policy.json', {
        'explicitClasspathForEveryJavaInvocation': True,
        'removedInheritedJavaOptionVariables': suppressed,
        'javaPolicy': ['-Xmx512m', '-Xverify:all'],
        'vmGeneratedNullMessages': 'Seven explicitly authored VM-null cases only; retained raw and excluded by unchanged input-scoped observer. No new normalization.'})

    def run(name, argv, expected=0):
        folder = output / 'commands'
        folder.mkdir(exist_ok=True)
        stdout = folder / (name + '.stdout.txt')
        stderr = folder / (name + '.stderr.txt')
        item = {'name': name, 'argv': [str(x) for x in argv], 'cwd': str(output),
                'startedUtc': now(), 'timeoutSeconds': 120, 'expectedReturncode': expected}
        begin = time.monotonic()
        with stdout.open('xb') as out, stderr.open('xb') as err:
            try:
                proc = subprocess.run(item['argv'], cwd=output, env=env, stdout=out, stderr=err, timeout=120)
                item['returncode'] = proc.returncode
            except subprocess.TimeoutExpired:
                item['returncode'] = None
                item['timedOut'] = True
        item.update({'finishedUtc': now(), 'durationSeconds': time.monotonic() - begin,
                     'stdout': {'path': stdout.relative_to(output).as_posix(), **identity(stdout)},
                     'stderr': {'path': stderr.relative_to(output).as_posix(), **identity(stderr)}})
        result['commands'].append(item)
        write_json(output / 'command-ledger.json', result['commands'])
        require(item['returncode'] == expected, 'Unexpected command result: ' + name)

    try:
        checkpoint, protected, historical, historical_result = verify_capsule(output)
        pins = json.loads((INPUTS / 'preserved-input-pins.json').read_text())
        for role in ('originalApk', 'externalToolchainJar', 'externalJdkRelease'):
            row = pins[role]
            require(identity(Path(row['path'])) == selected_identity(row), 'Pinned external input changed: ' + role)
            protected.append(Path(row['path']))
        protected.extend(JDK / name for name in ('bin/java', 'bin/javac', 'lib/server/libjvm.so', 'lib/modules'))
        before = hash_files(protected)
        write_json(output / 'protected-inputs-before.json', before)
        jar = Path(pins['externalToolchainJar']['path'])
        host, harness = output / 'hostclasses', output / 'harnessclasses'
        host.mkdir(); harness.mkdir()
        host_sources = sorted((INPUTS / 'host').rglob('*.java')) + [INPUTS / 'source/java/recovered/ui/DayTriggerLookupMethods.java']
        run('01-java-version', [JDK / 'bin/java', '-version'])
        run('02-javac-host-helper', [JDK / 'bin/javac', '--release', '8', '-g:none', '-Xlint:-options', '-d', host, *host_sources])
        run('03-javac-harness', [JDK / 'bin/javac', '-cp', os.pathsep.join(map(str, (jar, host))), '-d', harness,
                                INPUTS / 'BytecodeOracle.java', INPUTS / 'DayLookupStudy.java', INPUTS / 'ExtractDayLookupFixture.java'])
        classpath = os.pathsep.join(map(str, (host, harness, jar)))
        original = output / 'fresh-original-selected.dex'
        run('04-extract-original-from-apk', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', classpath,
                                            'ExtractDayLookupFixture', pins['originalApk']['path'], original,
                                            output / 'fresh-original-method-inventory.json'])
        require(identity(original)['sha256'] == ORIGINAL_DEX_SHA, 'Fresh extraction differs from the reviewed actual-original fixture')
        class_pins = {}
        for root in (host, harness):
            for path in sorted(root.rglob('*.class')):
                name = path.relative_to(root).as_posix()[:-6].replace('/', '.')
                require(name not in class_pins, 'Duplicate fresh compiled class: ' + name)
                class_pins[name] = {'path': str(path), **identity(path)}
        require(len(class_pins) == 21 and set(class_pins) == set(historical['loadedClassOrigins']), 'Fresh class membership differs')
        for name, row in class_pins.items():
            require(row['sha256'] == historical['loadedClassOrigins'][name]['sha256'], 'Fresh javac class differs: ' + name)
        helper_class = host / 'recovered/ui/DayTriggerLookupMethods.class'
        require(identity(helper_class)['sha256'] == HELPER_CLASS_SHA, 'Unexpected freshly compiled helper')
        write_json(output / 'fresh-class-identities.json', class_pins)

        pipeline = INPUTS / 'production-pipeline'
        sys.path.insert(0, str(pipeline))
        spec = importlib.util.spec_from_file_location('independently_bound_lookup_production_build', pipeline / 'build.py')
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        selected = json.loads((pipeline / 'source/class-index-selected.json').read_text())
        rows = [row for row in selected.values() if row['descriptor'] == TARGET]
        require(len(rows) == 1, 'Original class selection is not unique')
        original_smali = pipeline / rows[0]['path']
        original_text = original_smali.read_text()
        original_methods = build.methods(original_text)
        old = original_methods[METHOD]
        require(sha(old.encode()) == pins['selectedOriginalMethods'][0]['methodTextSha256'], 'Original body differs')
        entry = {'target': TARGET, 'method': METHOD, 'helper': 'Lrecovered/ui/DayTriggerLookupMethods;',
                 'helper_method': 'findEntry', 'instance': False,
                 'java_source': 'source/java/recovered/ui/DayTriggerLookupMethods.java'}

        def compile_body_to_dex(compiled_class, label):
            folder = output / label
            folder.mkdir()
            relocated = build.relocate_class(compiled_class.read_bytes())
            input_jar = folder / 'one-helper.jar'
            with zipfile.ZipFile(input_jar, 'x') as stream:
                item = zipfile.ZipInfo('recovered/ui/DayTriggerLookupMethods.class', (1980, 1, 1, 0, 0, 0))
                item.external_attr = 0o100644 << 16
                stream.writestr(item, relocated)
            with zipfile.ZipFile(input_jar) as stream:
                require(stream.namelist() == ['recovered/ui/DayTriggerLookupMethods.class'], 'Host classes escaped into D8 input')
                require(stream.read(stream.namelist()[0]) == relocated, 'D8 helper bytes changed')
            dexdir = folder / 'dex'; dexdir.mkdir()
            run(label + '-d8', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', jar, 'com.android.tools.r8.D8',
                                '--release', '--no-desugaring', '--min-api', '23', '--output', dexdir, input_jar])
            require(sorted(path.name for path in dexdir.iterdir()) == ['classes.dex'], 'Unexpected D8 output membership')
            build.dex_integrity(dexdir / 'classes.dex')
            smali = folder / 'helper-smali'
            run(label + '-baksmali', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', jar,
                                      'com.android.tools.smali.baksmali.Main', 'd', '--api', '23', '--use-locals',
                                      '-o', smali, dexdir / 'classes.dex'])
            require(sorted(path.relative_to(smali).as_posix() for path in smali.rglob('*.smali')) ==
                    ['recovered/ui/DayTriggerLookupMethods.smali'], 'Unexpected D8 helper class membership')
            body_method = build.methods((smali / 'recovered/ui/DayTriggerLookupMethods.smali').read_text())['findEntry' + METHOD[METHOD.index('('):]]
            restored, corrections = build.restore_from_preserved_source(entry, body_method, old, selected, pipeline)
            require(not corrections and restored == body_method, 'Unexpected constructor/body adjustment')
            body = build.ANNOT.sub('', restored.split('\n', 1)[1].rsplit('.end method', 1)[0])
            require('Lrecovered/' not in body and 'Ldefpackage/' not in body, 'Runtime stub/helper reference escaped')
            replacement = old.splitlines()[0] + '\n' + ''.join(build.ANNOT.findall(old)) + body + '.end method'
            require(original_text.count(old) == 1, 'Nonunique original method body')
            changed = original_text.replace(old, replacement, 1)
            changed_methods = build.methods(changed)
            require(set(changed_methods) == set(original_methods), 'Method membership changed')
            require(all(changed_methods[key] == value for key, value in original_methods.items() if key != METHOD),
                    'Another original method changed')
            require(changed.replace(replacement, '<PRIMARY>', 1) == original_text.replace(old, '<PRIMARY>', 1),
                    'Non-target class text changed')
            target = folder / 'target-smali/DayTrigger.smali'; target.parent.mkdir(); target.write_text(changed)
            rebuilt = folder / 'rebuilt-day-trigger.dex'
            run(label + '-smali', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', jar,
                                   'com.android.tools.smali.smali.Main', 'a', '--api', '23', '-j', '2', '-o', rebuilt, target.parent])
            build.dex_integrity(rebuilt)
            binding = {'helperClass': identity(compiled_class), 'compilerInput': identity(input_jar),
                       'compilerInputClassCount': 1, 'hostStubClassCount': 0, 'originalMethodSha256': sha(old.encode()),
                       'compiledMethodSha256': sha(body_method.encode()), 'transplantedMethodSha256': sha(replacement.encode()),
                       'rebuiltDex': identity(rebuilt), 'otherOriginalMethodsUnchanged': len(original_methods) - 1,
                       'nonTargetClassTextUnchanged': True, 'constructorCorrections': [],
                       'productionBuild': identity(pipeline / 'build.py'),
                       'productionConstructorOwner': identity(pipeline / 'constructor_owner.py')}
            write_json(folder / 'method-body-binding.json', binding)
            return rebuilt, binding

        rebuilt, positive_binding = compile_body_to_dex(helper_class, '05-positive-pipeline')
        require(identity(rebuilt)['sha256'] == REBUILT_DEX_SHA, 'Fresh rebuilt DEX differs from frozen checkpoint')
        config = {'originalDex': str(original), 'originalDexSha256': identity(original)['sha256'],
                  'rebuiltDex': str(rebuilt), 'rebuiltDexSha256': identity(rebuilt)['sha256'], 'classPins': class_pins}

        def execute(label, cfg, extra_host=None, expected=0):
            folder = output / label; folder.mkdir()
            write_json(folder / 'config.json', cfg)
            roots = ([extra_host] if extra_host else []) + [host, harness, jar]
            run(label, [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', os.pathsep.join(map(str, roots)),
                        'DayLookupStudy', folder / 'config.json', folder / 'parity.json'], expected)
            report = folder / 'parity.json'
            return json.loads(report.read_text()) if report.exists() else None

        positive = execute('06-positive', config)
        require(positive['passed'] and positive['cases'] == 371 and positive['executionPaths'] == 3,
                'Fresh positive failed')
        require({key: value for key, value in positive.items() if key != 'loadedClassOrigins'} ==
                {key: value for key, value in historical.items() if key != 'loadedClassOrigins'},
                'Fresh complete semantic observations differ from frozen evidence')
        # The only excluded comparison above is the deliberately different absolute
        # classpath. Every loaded class byte was independently checked equal first.
        controls = []
        for label, fault, required_message in (
            ('07-wrong-original-hash', 'original', 'Wrong original fixture identity'),
            ('08-original-as-rebuilt', 'alias', 'Original fixture cannot masquerade as rebuilt'),
            ('09-wrong-helper-hash', 'helper', 'Wrong loaded class hash: ' + HELPER)):
            cfg = copy.deepcopy(config)
            if fault == 'original': cfg['originalDexSha256'] = '0' * 64
            elif fault == 'alias':
                cfg['rebuiltDex'] = cfg['originalDex']; cfg['rebuiltDexSha256'] = cfg['originalDexSha256']
            else: cfg['classPins'][HELPER]['sha256'] = '0' * 64
            report = execute(label, cfg, expected=1)
            require(report is None and required_message in (output / 'commands' / (label + '.stderr.txt')).read_text(),
                    'Origin control rejected for the wrong reason: ' + label)
            controls.append({'name': label, 'rejectedBeforeReport': True, 'reason': required_message})

        source = (INPUTS / 'source/java/recovered/ui/DayTriggerLookupMethods.java').read_text()
        anchor = 'key.equalsIgnoreCase(entry.getKey())'
        require(source.count(anchor) == 1, 'Fault source anchor not unique')
        compiled_faults = {}
        faults = []
        for label, replacement, expected_mismatches, required_case in (
            ('10-reverse-receiver', 'entry.getKey().equalsIgnoreCase(key)', 3, 'null-entry-key-is-not-a-match'),
            ('11-case-sensitive', 'key.equals(entry.getKey())', 127, 'first-duplicate-entry-identity')):
            folder = output / (label + '-compiled')
            mutant_source = folder / 'source/recovered/ui/DayTriggerLookupMethods.java'
            mutant_source.parent.mkdir(parents=True)
            mutant_source.write_text(source.replace(anchor, replacement, 1))
            mutant_host = folder / 'hostclasses'; mutant_host.mkdir()
            run(label + '-javac', [JDK / 'bin/javac', '--release', '8', '-g:none', '-Xlint:-options',
                                  '-cp', host, '-d', mutant_host, mutant_source])
            mutant_class = mutant_host / 'recovered/ui/DayTriggerLookupMethods.class'
            require(sorted(p.relative_to(mutant_host).as_posix() for p in mutant_host.rglob('*.class')) ==
                    ['recovered/ui/DayTriggerLookupMethods.class'], 'Unexpected mutant classes')
            cfg = copy.deepcopy(config)
            cfg['classPins'][HELPER] = {'path': str(mutant_class), **identity(mutant_class)}
            observed = execute(label, cfg, extra_host=mutant_host, expected=3)
            require(not observed['passed'] and observed['cases'] == 371 and observed['executionPaths'] == 3 and
                    observed['mismatchCount'] == expected_mismatches and observed['unsupportedCount'] == 0 and
                    required_case in observed['mismatches'], 'Fresh compiled Java fault not detected as expected')
            require(len(observed['observations']) == len(positive['observations']), 'Fault omitted cases')
            require(all(a['case'] == b['case'] and a['original'] == b['original'] and a['rebuilt'] == b['rebuilt']
                        for a, b in zip(positive['observations'], observed['observations'])), 'Java fault altered reference path')
            faults.append({'name': label, 'source': identity(mutant_source), 'class': identity(mutant_class),
                           'mismatchCount': expected_mismatches, 'requiredFailingCase': required_case,
                           'unchangedReferencePaths': ['original', 'rebuilt'], 'unsupportedCount': 0})
            compiled_faults[label] = mutant_class

        faulty_dex, faulty_binding = compile_body_to_dex(compiled_faults['11-case-sensitive'], '12-fault-pipeline')
        cfg = copy.deepcopy(config)
        cfg['rebuiltDex'] = str(faulty_dex); cfg['rebuiltDexSha256'] = identity(faulty_dex)['sha256']
        observed = execute('13-rebuilt-case-sensitive', cfg, expected=3)
        require(not observed['passed'] and observed['cases'] == 371 and observed['executionPaths'] == 3 and
                observed['mismatchCount'] == 127 and observed['unsupportedCount'] == 0 and
                'first-duplicate-entry-identity' in observed['mismatches'], 'Fresh rebuilt fault not detected')
        require(len(observed['observations']) == len(positive['observations']) and
                all(a['case'] == b['case'] and a['original'] == b['original'] and a['java'] == b['java']
                    for a, b in zip(positive['observations'], observed['observations'])), 'Rebuilt fault altered reference path')
        faults.append({'name': '13-rebuilt-case-sensitive', 'binding': faulty_binding, 'mismatchCount': 127,
                       'requiredFailingCase': 'first-duplicate-entry-identity',
                       'unchangedReferencePaths': ['original', 'java'], 'unsupportedCount': 0})
        restored = execute('14-positive-restored', config)
        require(restored == positive and identity(output / '06-positive/parity.json') ==
                identity(output / '14-positive-restored/parity.json'), 'Positive report not restored exactly')
        for row in class_pins.values():
            require(identity(Path(row['path'])) == selected_identity(row), 'Fresh positive class changed')
        after = hash_files(protected)
        write_json(output / 'protected-inputs-after.json', after)
        require(before == after, 'Protected source/archive/APK/tool/runtime changed')
        result.update({'status': 'INDEPENDENT_THREE_PATH_REVIEW_PASSED', 'passed': True,
                       'frozenCheckpointSha256': CHECKPOINT_SHA, 'sourceFilesVerified': 31, 'evidenceMembersVerified': 150,
                       'freshCompiledClassCount': 21, 'freshCompiledBytesEqualHistorical': True,
                       'freshOriginalFixture': identity(original), 'freshRebuiltFixture': identity(rebuilt),
                       'positiveBinding': positive_binding, 'cases': 371, 'executionPaths': 3,
                       'mismatchCount': 0, 'unsupportedCount': 0, 'independentExpectedFailures': 0,
                       'originalCoverage': positive['originalCoverage'], 'rebuiltCoverage': positive['rebuiltCoverage'],
                       'allHistoricalSemanticObservationFieldsReproducedExactly': True,
                       'freshOriginControls': controls, 'freshCompiledFaults': faults,
                       'positiveReport': identity(output / '06-positive/parity.json'),
                       'positiveReportRestoredExactly': True, 'allProtectedBytesUnchanged': True,
                       'activeSourceChanged': False, 'activeRegistryChanged': False, 'apkBuiltOrChanged': False,
                       'androidExecuted': False})
    except BaseException as error:
        result.update({'status': 'INDEPENDENT_REVIEW_FAILURE_RETAINED', 'passed': False,
                       'errorType': type(error).__name__, 'error': str(error)})
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        result['finishedUtc'] = now()
        result['durationSeconds'] = time.monotonic() - started
        result['freeBytesAtEnd'] = shutil.disk_usage(WORKSPACE).free
        result['outputPayloadBytesBeforeResult'] = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
        write_json(output / 'result.json', result)
        print(json.dumps({key: result.get(key) for key in (
            'status', 'passed', 'cases', 'executionPaths', 'mismatchCount', 'unsupportedCount',
            'durationSeconds', 'outputPayloadBytesBeforeResult', 'freeBytesAtEnd', 'error')}, indent=2))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
