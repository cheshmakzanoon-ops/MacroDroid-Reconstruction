#!/usr/bin/env python3
"""Compile a bounded source slice and execute only the lookup adapter's 371 cases."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import traceback

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'stage-02/project'
ACTIVE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
WORKSPACE = Path('/workspace/scratch/4130730d15aa')
JDK = WORKSPACE / 'tooling/jdk21/bin'
JAR = WORKSPACE / 'current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar'
APK = WORKSPACE / 'recovered/automation android app'

def identity(path):
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}

def save(path, value): path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    out = ROOT / 'reports/04-original-jvm-adapter'
    out.mkdir(parents=True, exist_ok=False)
    result = {'status': 'RUNNING', 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'commands': [], 'full_source_copy': False, 'full_build': False, 'signed_primary_verified': False,
              'androidRuntime': False, 'active_source_changed': False}
    save(out / 'result.json', result)
    shutil.copy2(__file__, out / 'executed-driver.py')
    def run(name, argv, timeout=90):
        cmd = list(map(str, argv)); stdout, stderr = out / (name + '.stdout.log'), out / (name + '.stderr.log')
        at, tick = datetime.now(timezone.utc).isoformat(), time.monotonic(); code = None
        env = {**os.environ, 'JAVA_HOME': str(JDK.parent), 'PATH': str(JDK) + os.pathsep + os.environ.get('PATH',''),
               'TMPDIR': str(out), 'PYTHONDONTWRITEBYTECODE': '1'}
        try:
            with stdout.open('xb') as so, stderr.open('xb') as se:
                code = subprocess.run(cmd, cwd=out, stdout=so, stderr=se, timeout=timeout, env=env).returncode
        finally:
            result['commands'].append({'name': name, 'argv': cmd, 'returncode': code, 'started_utc': at,
                                       'duration_seconds': time.monotonic()-tick, 'timeout_seconds': timeout,
                                       'stdout': {'path': stdout.name, **identity(stdout)}, 'stderr': {'path': stderr.name, **identity(stderr)}})
            save(out / 'result.json', result)
        assert code == 0, name + ': ' + stderr.read_text(errors='replace')[-5000:]
    try:
        sources = [PROJECT / n for n in ('source/java/recovered/ui/DayTriggerLookupMethods.java',
            'source/java/recovered/ui/DayTriggerValueMethods.java', 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',
            'tests/java/DayLookupParityCases.java', 'tests/java/DayTriggerParityCases.java', 'tests/java/UiParityTests.java',
            'tools/src/ExtractOracle.java', 'source/java-method-map.json', 'source/ui-methods.json', 'tests/fixtures/original-dependencies.json')]
        sources += [ROOT / 'LookupAdapterProbe.java', ACTIVE / 'tests/java/BytecodeOracle.java',
                    ROOT / 'CompareOriginalFixture.java']
        pins = {str(p): identity(p) for p in sources}
        external = {str(p): identity(p) for p in (APK, JAR, JDK/'java', JDK/'javac', JDK.parent/'release')}
        assert external[str(APK)]['sha256'] == '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
        assert external[str(JAR)]['sha256'] == '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'
        save(out / 'source-inputs.json', pins); save(out / 'external-inputs.json', external)
        source_copy = out / 'executed-sources'; source_copy.mkdir()
        for index, p in enumerate(sources): shutil.copy2(p, source_copy / (str(index).zfill(2)+'-'+p.name))
        host, tools = out / 'hostclasses', out / 'harnessclasses'; host.mkdir(); tools.mkdir()
        base_host, base_tools = ACTIVE / 'build/java/hostclasses', ACTIVE / 'tools/classes'
        run('compile-helper-and-shared-host', [JDK/'javac', '--release','8','-g:none','-cp',base_host,'-d',host,
            PROJECT/'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',
            PROJECT/'source/java/recovered/ui/DayTriggerLookupMethods.java', PROJECT/'source/java/recovered/ui/DayTriggerValueMethods.java'])
        assert identity(host/'recovered/ui/DayTriggerValueMethods.class')['sha256'] == '2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211'
        cp = os.pathsep.join(map(str, [JAR, host, base_host, base_tools]))
        run('compile-oracle-adapter-and-selector', [JDK/'javac','-cp',cp,'-d',tools,
            ACTIVE/'tests/java/BytecodeOracle.java', PROJECT/'tests/java/UiParityTests.java',
            PROJECT/'tests/java/DayTriggerParityCases.java', PROJECT/'tests/java/DayLookupParityCases.java',
            PROJECT/'tools/src/ExtractOracle.java', ROOT/'LookupAdapterProbe.java',
            ROOT/'CompareOriginalFixture.java'])
        cp = os.pathsep.join(map(str, [JAR, host, tools, base_host, base_tools]))
        run('extract-original-fixture', [JDK/'java','-Xverify:all','-Xmx768m','-cp',cp,'ExtractOracle',PROJECT,APK])
        fixture = PROJECT/'tests/fixtures/original-methods.dex'
        run('recreate-prior-1246-fixture', [JDK/'java','-Xverify:all','-Xmx512m','-cp',cp,'CompareOriginalFixture',
            ROOT/'stage-02/baseline/tests/fixtures/original-methods.dex',fixture,out/'recreated-numeric-fixture.dex',out/'fixture-invariance.json'])
        extraction = json.loads((PROJECT/'reports/original-fixture-extraction.json').read_text())
        assert {k: extraction[k] for k in ('registered_methods','dependency_methods','methods','classes')} == {'registered_methods':1244,'dependency_methods':5,'methods':1249,'classes':607}
        shutil.copy2(PROJECT/'reports/original-fixture-extraction.json',out/'original-fixture-extraction.json')
        class_pins = {}
        for folder in (host, tools):
            for path in sorted(folder.rglob('*.class')):
                name = path.relative_to(folder).as_posix().removesuffix('.class').replace('/','.')
                assert name not in class_pins; class_pins[name] = {'path':str(path),**identity(path)}
        cfg = {'root':str(PROJECT),'fixtureSha256':identity(fixture)['sha256'],'classPins':class_pins}
        save(out/'config.json',cfg)
        run('execute-371-original-jvm-adapter', [JDK/'java','-Xverify:all','-XX:-OmitStackTraceInFastThrow','-cp',cp,'LookupAdapterProbe',out/'config.json',out/'adapter-parity.json'])
        parity = json.loads((out/'adapter-parity.json').read_text())
        assert parity['passed'] is True and parity['cases'] == 371 and parity['mismatches'] == parity['unsupported'] == 0
        assert parity['dayLookupInputInventorySha256'] == '02dd119966191ad2f56937eda28e63644979080158465ffb13767710f34e32e6'
        provenance_path = PROJECT/'tests/fixtures/provenance.json'; provenance=json.loads(provenance_path.read_text())
        for key in ('fixture_sha256','fixture_bytes','methods','classes','registered_methods','dependency_methods','dependency_declaration_sha256','dependency_keys'):
            provenance[key] = extraction[key]
        provenance['extraction'] = 'Fresh hash-checked ExtractOracle run from the exact original APK; all prior 1246-method numeric fixture bytes independently recreated from the new selection.'
        save(provenance_path,provenance)
        assert all(identity(Path(path)) == pin for path,pin in pins.items())
        assert all(identity(Path(path)) == pin for path,pin in external.items())
        result.update(status='LOOKUP_UI_ADAPTER_ORIGINAL_JVM_AND_FIXTURE_PASSED', passed=True,
            original_jvm_cases=371, mismatches=0, unsupported=0, independent_expected_checks=371,
            original_instructions=26, original_conditional_edges=4,
            fixture_registered_methods=1244, fixture_uncredited_dependencies=5, fixture_methods=1249, fixture_classes=607,
            all_prior_1246_fixture_bytes_recreated=True, numeric_helper_class_unchanged=True,
            lookup_helper_class=identity(host/'recovered/ui/DayTriggerLookupMethods.class'),
            lookup_helper_source=identity(PROJECT/'source/java/recovered/ui/DayTriggerLookupMethods.java'),
            source_and_external_inputs_unchanged=True, full_ui_101_controls_and_signed_proof_pending=True)
    except Exception as error:
        result.update(status='FAILED_PRESERVED',error_type=type(error).__name__,error=str(error))
        (out/'failure.traceback.txt').write_text(traceback.format_exc()); raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); save(out/'result.json',result)
        print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file()) <= 256*1024*1024

if __name__ == '__main__': main()
