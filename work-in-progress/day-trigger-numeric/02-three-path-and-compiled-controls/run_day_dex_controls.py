#!/usr/bin/env python3
"""Use the unchanged production relocation/transplant helpers, then measure real faults."""
from pathlib import Path
import argparse, importlib.util, json, os, re, shutil, subprocess, sys, time, traceback, zipfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from run_day_study import identity, tree, now

INPUTS = ROOT / 'inputs'
JDK = ROOT.parent / 'tooling/jdk21'
BASELINE = ROOT / 'reports/original-java-01'
CHECKPOINT = ROOT / 'checkpoints/01-original-java-proof'
CHECKPOINT_SHA = '6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e'
TARGET = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;'
METHOD = 'r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'
HELPER = 'recovered.ui.DayTriggerValueMethods'

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output).resolve()
    if output.exists(): raise RuntimeError('Output already exists; preserve earlier attempts')
    if shutil.disk_usage(ROOT).free < 96 * 1024 * 1024: raise RuntimeError('Insufficient bounded-study headroom')
    output.mkdir(parents=True)
    result = {'startedUtc': now(), 'scope': 'Private one-method original/JVM/rebuilt-bytecode proof and actual compiled controls; no APK or active registry changes.', 'commands': []}
    shutil.copyfile(__file__, output / 'run_day_dex_controls.py')
    shutil.copyfile(ROOT / 'run_day_study.py', output / 'run_day_study.py')

    def run(folder, name, argv, expected=0, timeout=120):
        folder.mkdir(parents=True, exist_ok=True)
        item = {'name': name, 'argv': list(map(str, argv)), 'startedUtc': now(), 'timeoutSeconds': timeout}
        started = time.monotonic(); stdout = folder / (name + '.stdout.txt'); stderr = folder / (name + '.stderr.txt')
        with stdout.open('xb') as out, stderr.open('xb') as err:
            try:
                proc = subprocess.run(item['argv'], cwd=ROOT, stdout=out, stderr=err, timeout=timeout,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                item['returncode'] = proc.returncode
            except subprocess.TimeoutExpired:
                item['returncode'] = None; item['timedOut'] = True
        item.update({'finishedUtc': now(), 'durationSeconds': time.monotonic() - started,
                     'stdout': {'path': stdout.relative_to(output).as_posix(), **identity(stdout)},
                     'stderr': {'path': stderr.relative_to(output).as_posix(), **identity(stderr)}})
        result['commands'].append(item)
        (output / 'command-ledger.json').write_text(json.dumps(result['commands'], indent=2) + '\n')
        if item['returncode'] != expected: raise RuntimeError('Unexpected command result: ' + name)
        return item

    try:
        if identity(CHECKPOINT / 'checkpoint.json')['sha256'] != CHECKPOINT_SHA: raise RuntimeError('Baseline checkpoint changed')
        checkpoint = json.loads((CHECKPOINT / 'checkpoint.json').read_text())
        for row in checkpoint['sourceFiles']:
            if identity(CHECKPOINT / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise RuntimeError('Frozen source changed: ' + row['path'])
        for row in checkpoint['evidenceFiles']:
            if identity(BASELINE / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise RuntimeError('Baseline evidence changed: ' + row['path'])
        archive = checkpoint['evidenceArchive']
        if identity(CHECKPOINT / archive['path']) != {key: archive[key] for key in ('bytes', 'sha256')}:
            raise RuntimeError('Baseline archive changed')
        before = tree(INPUTS); baseline_before = tree(BASELINE)
        (output / 'input-identities-before.json').write_text(json.dumps(before, indent=2) + '\n')
        shutil.copyfile(CHECKPOINT / 'checkpoint.json', output / 'baseline-checkpoint.json')
        pins = json.loads((INPUTS / 'preserved-input-pins.json').read_text())
        external = {}
        for role in ('originalApk', 'externalToolchainJar', 'externalJdkRelease'):
            row = pins[role]; path = Path(row['path']); actual = identity(path)
            if actual != {key: row[key] for key in ('bytes', 'sha256')}: raise RuntimeError('External input changed: ' + role)
            external[role] = {'path': str(path), **actual}
        for name in ('bin/java', 'bin/javac', 'lib/server/libjvm.so', 'lib/modules'):
            path = JDK / name; external[name] = {'path': str(path), **identity(path)}
        (output / 'external-input-identities.json').write_text(json.dumps(external, indent=2) + '\n')
        jar = Path(pins['externalToolchainJar']['path']); host = BASELINE / 'hostclasses'; harness = BASELINE / 'harnessclasses'
        base_config = json.loads((BASELINE / 'study-config.json').read_text())
        sys.path.insert(0, str(INPUTS / 'production-pipeline'))
        spec = importlib.util.spec_from_file_location('day_bound_production_build', INPUTS / 'production-pipeline/build.py')
        build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
        selected = json.loads((INPUTS / 'production-pipeline/source/class-index-selected.json').read_text())
        originals = [row for row in selected.values() if row['descriptor'] == TARGET]
        if len(originals) != 1: raise RuntimeError('Target class index is not unique')
        original_path = INPUTS / 'production-pipeline' / originals[0]['path']
        original_text = original_path.read_text(); old_methods = build.methods(original_text); old = old_methods[METHOD]
        selected_pin = next(row for row in pins['selectedOriginalMethods'] if row['descriptor'] == TARGET)
        import hashlib
        text_sha = lambda text: hashlib.sha256(text.encode()).hexdigest()
        if text_sha(old) != selected_pin['methodTextSha256']: raise RuntimeError('Original primary body changed')
        entry = {'target': TARGET, 'method': METHOD, 'helper': 'Lrecovered/ui/DayTriggerValueMethods;',
                 'helper_method': 'numericValue', 'instance': False,
                 'java_source': 'source/java/recovered/ui/DayTriggerValueMethods.java'}
        (output / 'proposed-method-entry.json').write_text(json.dumps(entry, indent=2) + '\n')

        def dex_from_helper(helper_class, folder):
            folder.mkdir(parents=True)
            relocated = folder / 'relocated/recovered/ui/DayTriggerValueMethods.class'
            relocated.parent.mkdir(parents=True)
            relocated.write_bytes(build.relocate_class(helper_class.read_bytes()))
            jar_input = folder / 'inputs.jar'
            with zipfile.ZipFile(jar_input, 'x') as stream:
                item = zipfile.ZipInfo('recovered/ui/DayTriggerValueMethods.class', (1980, 1, 1, 0, 0, 0)); item.external_attr = 0o100644 << 16
                stream.writestr(item, relocated.read_bytes())
            with zipfile.ZipFile(jar_input) as stream:
                if stream.namelist() != ['recovered/ui/DayTriggerValueMethods.class'] or stream.read(stream.namelist()[0]) != relocated.read_bytes():
                    raise RuntimeError('Unexpected D8 input class')
            dexdir = folder / 'd8'; dexdir.mkdir()
            run(folder, 'd8-one-helper', [JDK / 'bin/java', '-Xmx512m', '-cp', jar, 'com.android.tools.r8.D8',
                                        '--release', '--no-desugaring', '--min-api', '23', '--output', dexdir, jar_input])
            if sorted(path.name for path in dexdir.iterdir()) != ['classes.dex']: raise RuntimeError('Unexpected D8 outputs')
            helper_dex_hash = build.dex_integrity(dexdir / 'classes.dex')
            smali = folder / 'helper-smali'
            run(folder, 'disassemble-helper', [JDK / 'bin/java', '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main',
                                               'd', '--api', '23', '--use-locals', '-o', smali, dexdir / 'classes.dex'])
            if sorted(path.relative_to(smali).as_posix() for path in smali.rglob('*.smali')) != ['recovered/ui/DayTriggerValueMethods.smali']:
                raise RuntimeError('Unexpected emitted helper classes')
            helper_method = build.methods((smali / 'recovered/ui/DayTriggerValueMethods.smali').read_text())['numericValue' + METHOD[METHOD.index('('):]]
            compiled, corrections = build.restore_from_preserved_source(entry, helper_method, old, selected, INPUTS / 'production-pipeline')
            if corrections or compiled != helper_method: raise RuntimeError('Numeric method must need no constructor-owner correction')
            body = build.ANNOT.sub('', compiled.split('\n', 1)[1].rsplit('.end method', 1)[0])
            if 'Lrecovered/' in body or 'Ldefpackage/' in body: raise RuntimeError('Runtime helper/stub reference escaped')
            replacement = old.splitlines()[0] + '\n' + ''.join(build.ANNOT.findall(old)) + body + '.end method'
            if original_text.count(old) != 1: raise RuntimeError('Primary method replacement is not unique')
            new_text = original_text.replace(old, replacement, 1); new_methods = build.methods(new_text)
            if set(new_methods) != set(old_methods) or any(new_methods[key] != value for key, value in old_methods.items() if key != METHOD):
                raise RuntimeError('A non-target method changed')
            if new_text.replace(replacement, '<PRIMARY>', 1) != original_text.replace(old, '<PRIMARY>', 1):
                raise RuntimeError('Non-target class text changed')
            target_smali = folder / 'target-smali/DayTrigger.smali'; target_smali.parent.mkdir(); target_smali.write_text(new_text)
            dex = folder / 'rebuilt-day-trigger.dex'
            run(folder, 'assemble-target', [JDK / 'bin/java', '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main',
                                            'a', '--api', '23', '-j', '2', '-o', dex, target_smali.parent])
            digest = build.dex_integrity(dex)
            binding = {'primaryMethod': TARGET + '->' + METHOD, 'originalClass': identity(original_path),
                       'originalMethodSha256': text_sha(old), 'loadedHelperClass': identity(helper_class),
                       'relocatedHelperClass': identity(relocated), 'compilerInput': identity(jar_input),
                       'compilerInputClassCount': 1, 'hostStubsSentToD8': 0, 'helperDexSha256': helper_dex_hash,
                       'compiledMethodSha256': text_sha(helper_method), 'transplantedMethodSha256': text_sha(replacement),
                       'transplantedClass': identity(target_smali), 'rebuiltDexSha256': digest,
                       'otherOriginalMethodsUnchanged': len(old_methods) - 1, 'allNonTargetClassTextUnchanged': True,
                       'constructorOwnerCorrections': [], 'productionBuild': identity(INPUTS / 'production-pipeline/build.py'),
                       'productionConstructorOwner': identity(INPUTS / 'production-pipeline/constructor_owner.py')}
            (folder / 'method-body-binding.json').write_text(json.dumps(binding, indent=2) + '\n')
            return dex, binding

        helper_class = host / 'recovered/ui/DayTriggerValueMethods.class'
        rebuilt, binding = dex_from_helper(helper_class, output / 'positive-pipeline')
        config = json.loads(json.dumps(base_config)); config.update({'rebuiltDex': str(rebuilt), 'rebuiltDexSha256': identity(rebuilt)['sha256']})

        def execute(folder, cfg, mutant_host=None, expected=0):
            folder.mkdir(parents=True, exist_ok=True)
            config_path = folder / 'config.json'; config_path.write_text(json.dumps(cfg, indent=2) + '\n')
            roots = ([mutant_host] if mutant_host else []) + [host, harness, jar]
            run(folder, 'execute-study', [JDK / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', os.pathsep.join(map(str, roots)),
                                          'DayValueStudy', config_path, folder / 'parity.json'], expected=expected)
            path = folder / 'parity.json'
            return json.loads(path.read_text()) if path.exists() else None

        positive = execute(output / 'positive', config)
        if not positive['passed'] or positive['cases'] != 1291 or positive['executionPaths'] != 3:
            raise RuntimeError('Three-path positive criteria not satisfied')
        controls = []
        wrong = json.loads(json.dumps(config)); wrong['rebuiltDex'] = wrong['originalDex']; wrong['rebuiltDexSha256'] = wrong['originalDexSha256']
        folder = output / 'controls/original-as-rebuilt'; observed = execute(folder, wrong, expected=1)
        if observed is not None or 'Original fixture cannot masquerade as rebuilt' not in (folder / 'execute-study.stderr.txt').read_text():
            raise RuntimeError('Original-as-rebuilt control did not reject for the expected reason')
        controls.append({'name': 'original-as-rebuilt', 'rejectedBeforeReport': True})
        wrong = json.loads(json.dumps(config)); wrong['classPins'][HELPER]['sha256'] = '0' * 64
        folder = output / 'controls/wrong-loaded-helper'; observed = execute(folder, wrong, expected=1)
        if observed is not None or 'Wrong loaded class hash: ' + HELPER not in (folder / 'execute-study.stderr.txt').read_text():
            raise RuntimeError('Wrong-helper control did not reject for the expected reason')
        controls.append({'name': 'wrong-loaded-helper', 'rejectedBeforeReport': True})

        source = (INPUTS / 'source/java/recovered/ui/DayTriggerValueMethods.java').read_text()
        integer = 'return (int) ((VariableValue.IntegerValue) value).getIntValue();'
        decimal = 'return (int) ((VariableValue.DecimalValue) value).getDecimalValue();'
        faults = [
            ('integer-zero', integer, 'return 0;', 'integer-boundary-1'),
            ('decimal-zero', decimal, 'return 0;', 'decimal-boundary-6'),
            ('integer-saturation', integer, 'long n = ((VariableValue.IntegerValue) value).getIntValue(); return n > Integer.MAX_VALUE ? Integer.MAX_VALUE : n < Integer.MIN_VALUE ? Integer.MIN_VALUE : (int) n;', 'integer-boundary-15'),
            ('integer-via-double', integer, 'return (int) (double) ((VariableValue.IntegerValue) value).getIntValue();', 'integer-boundary-15'),
            ('integer-via-byte', integer, 'return (byte) ((VariableValue.IntegerValue) value).getIntValue();', 'integer-boundary-6'),
            ('decimal-round', decimal, 'return (int) Math.round(((VariableValue.DecimalValue) value).getDecimalValue());', 'decimal-boundary-10'),
            ('decimal-floor', decimal, 'return (int) Math.floor(((VariableValue.DecimalValue) value).getDecimalValue());', 'decimal-boundary-3'),
            ('decimal-nan-one', decimal, 'double n = ((VariableValue.DecimalValue) value).getDecimalValue(); return Double.isNaN(n) ? 1 : (int) n;', 'decimal-boundary-35'),
            ('decimal-infinity-zero', decimal, 'double n = ((VariableValue.DecimalValue) value).getDecimalValue(); return Double.isInfinite(n) ? 0 : (int) n;', 'decimal-boundary-33'),
            ('other-minus-one', '        return 0;', '        return -1;', 'null-value'),
            ('parse-string', '        return 0;', '        if (value instanceof VariableValue.StringValue) return Integer.parseInt(((VariableValue.StringValue) value).text);\n        return 0;', 'string-numeric'),
            ('null-contained-throws', 'VariableValue value = entry.getVariable();', 'VariableValue value = entry.getVariable(); if (value == null) throw new NullPointerException("deliberate contained-null fault");', 'null-value'),
            ('null-entry-zero', 'VariableValue value = entry.getVariable();', 'if (entry == null) return 0; VariableValue value = entry.getVariable();', 'null-entry'),
        ]
        (output / 'fault-catalog.json').write_text(json.dumps([{'name': name, 'old': old_anchor, 'new': changed, 'requiredFailingCase': required}
                                                            for name, old_anchor, changed, required in faults], indent=2) + '\n')
        compiled_faults = {}; fault_results = []
        for name, old_anchor, changed, required in faults:
            if source.count(old_anchor) != 1: raise RuntimeError('Fault anchor is not unique: ' + name)
            folder = output / 'controls' / name
            mutant_source = folder / 'source/recovered/ui/DayTriggerValueMethods.java'; mutant_source.parent.mkdir(parents=True)
            mutant_source.write_text(source.replace(old_anchor, changed, 1))
            mutant_host = folder / 'hostclasses'; mutant_host.mkdir()
            run(folder, 'compile-actual-source-fault', [JDK / 'bin/javac', '--release', '8', '-g:none', '-Xlint:-options',
                                                       '-cp', host, '-d', mutant_host, mutant_source])
            mutant_class = mutant_host / 'recovered/ui/DayTriggerValueMethods.class'
            if sorted(path.relative_to(mutant_host).as_posix() for path in mutant_host.rglob('*.class')) != ['recovered/ui/DayTriggerValueMethods.class']:
                raise RuntimeError('Fault compilation emitted unexpected classes')
            cfg = json.loads(json.dumps(config)); cfg['classPins'][HELPER] = {'path': str(mutant_class), **identity(mutant_class)}
            observed = execute(folder / 'execution', cfg, mutant_host, expected=3)
            if not observed or observed['passed'] or required not in observed['mismatches'] or observed['unsupportedCount']:
                raise RuntimeError('Actual compiled fault was not detected for the required case: ' + name)
            if observed['cases'] != positive['cases'] or observed['executionPaths'] != 3:
                raise RuntimeError('Actual compiled fault omitted required cases or paths')
            for original_row, fault_row in zip(positive['observations'], observed['observations']):
                if original_row['case'] != fault_row['case'] or original_row['original'] != fault_row['original'] or original_row['rebuilt'] != fault_row['rebuilt']:
                    raise RuntimeError('Java fault changed an independent reference path: ' + name)
            fault_results.append({'name': name, 'source': identity(mutant_source), 'compiledClass': identity(mutant_class),
                                  'requiredFailingCase': required, 'mismatchCount': observed['mismatchCount'],
                                  'unsupportedCount': observed['unsupportedCount'], 'referencePathsUnchanged': True,
                                  'actualCompiledFaultDetected': True})
            compiled_faults[name] = mutant_class

        dex_controls = []
        for name, required in [('integer-zero', 'integer-boundary-1'), ('decimal-zero', 'decimal-boundary-6')]:
            dex, faulty_binding = dex_from_helper(compiled_faults[name], output / 'controls' / (name + '-rebuilt-pipeline'))
            cfg = json.loads(json.dumps(config)); cfg.update({'rebuiltDex': str(dex), 'rebuiltDexSha256': identity(dex)['sha256']})
            observed = execute(output / 'controls' / (name + '-rebuilt-execution'), cfg, expected=3)
            if not observed or observed['passed'] or required not in observed['mismatches'] or observed['unsupportedCount']:
                raise RuntimeError('Actual rebuilt-bytecode fault was not detected: ' + name)
            for original_row, fault_row in zip(positive['observations'], observed['observations']):
                if original_row['case'] != fault_row['case'] or original_row['original'] != fault_row['original'] or original_row['java'] != fault_row['java']:
                    raise RuntimeError('Rebuilt fault changed an independent reference path: ' + name)
            dex_controls.append({'name': name, 'mismatchCount': observed['mismatchCount'],
                                 'unsupportedCount': observed['unsupportedCount'], 'requiredFailingCase': required,
                                 'referencePathsUnchanged': True, 'actualCompiledRebuiltFaultDetected': True,
                                 'binding': faulty_binding})
        restored = execute(output / 'positive-restored', config)
        if restored != positive or identity(output / 'positive/parity.json') != identity(output / 'positive-restored/parity.json'):
            raise RuntimeError('Entire three-path positive report was not restored exactly')
        if tree(INPUTS) != before or tree(BASELINE) != baseline_before:
            raise RuntimeError('Immutable source or original/JVM evidence changed')
        for role, row in external.items():
            if identity(Path(row['path'])) != {key: row[key] for key in ('bytes', 'sha256')}: raise RuntimeError('External input changed: ' + role)
        result.update({'status': 'THREE_PATH_AND_COMPILED_CONTROLS_PASSED', 'passed': True,
                       'cases': positive['cases'], 'executionPaths': 3, 'mismatchCount': 0, 'unsupportedCount': 0,
                       'independentExpectedChecks': positive['independentExpectedChecks'], 'independentExpectedFailures': 0,
                       'originalCoverage': positive['originalCoverage'], 'rebuiltCoverage': positive['rebuiltCoverage'],
                       'positiveBinding': binding, 'positiveReport': identity(output / 'positive/parity.json'),
                       'originControls': controls, 'compiledJavaFaults': fault_results, 'compiledRebuiltFaults': dex_controls,
                       'allCompiledFaultsDetected': True, 'allInputBaselineAndToolBytesUnchanged': True,
                       'positiveReportRestoredExactly': True, 'activeRegistryChanged': False, 'signedApkBuilt': False, 'androidExecuted': False})
    except BaseException as error:
        result.update({'status': 'THREE_PATH_OR_CONTROL_FAILURE_RETAINED', 'passed': False, 'error': str(error)})
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        result['finishedUtc'] = now()
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({key: value for key, value in result.items() if key not in
                         ('commands', 'originalCoverage', 'rebuiltCoverage', 'compiledJavaFaults', 'compiledRebuiltFaults')}, indent=2))
    if not result['passed']: raise SystemExit(1)

if __name__ == '__main__': main()
