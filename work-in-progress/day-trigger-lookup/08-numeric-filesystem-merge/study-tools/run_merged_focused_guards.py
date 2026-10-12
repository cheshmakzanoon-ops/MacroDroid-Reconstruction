#!/usr/bin/env python3
"""Run only existing numeric/catalog controls plus the new lookup guard module."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import time
import traceback
import unittest

ROOT=Path(__file__).resolve().parent;PROJECT=ROOT/'stage-03/project'
ACTIVE=Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')

def identity(path):
    with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module

def main():
    out=ROOT/'reports/17-merged-focused-guards';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-driver.py')
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'Exactly 35 numeric, 33 lookup and eight existing Widget catalog guards against the 21-path merged overlay. Numeric selector controls execute bounded real Java extraction. No full suite, APK build, application parity rerun or acceptance-level recorder execution.'}
    save(out/'result.json',result)
    try:
        view=out/'project-view';view.mkdir()
        prepared=ROOT/'reports/06-compiled-adapter-controls/preparation-inputs'
        names={p.relative_to(prepared).as_posix() for p in prepared.rglob('*') if p.is_file()}
        names.update(row['path'] for row in json.loads((PROJECT.parent/'merge-manifest.json').read_text())['changes'])
        names.update(['source/java/recovered/ui/DayTriggerValueMethods.java','tests/java/DayNumericControlHarness.java',
                      'tests/fixtures/day-numeric-mutants.json','tools/src/ExtractOracle.java','tests/test_ui_mutation_catalog.py'])
        pins={}
        for name in sorted(names):
            source=PROJECT/name if (PROJECT/name).is_file() else ACTIVE/name
            target=view/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
            assert identity(source)==identity(target);pins[str(source)]=identity(source)
        for name in ['build.py','constructor_owner.py','ui_runtime_policy.py']:
            pins[str(ACTIVE/name)]=identity(ACTIVE/name)
        save(out/'source-inputs.json',pins)
        copies={str(p):identity(p) for p in view.rglob('*') if p.is_file()};save(out/'executed-copy-inputs.json',copies)
        os.environ['TMPDIR']=str(out);os.environ['DAY_NUMERIC_TEST_COMMAND_LOG']=str(out/'extractor-commands.jsonl')
        import tempfile;tempfile.tempdir=str(out)
        sys.path[:0]=[str(view),str(ACTIVE)]
        import build
        jar=build.JAR;build.ROOT=view
        assert jar.is_file()
        import day_numeric_dex_controls as numeric, day_lookup_dex_controls as lookup
        assert Path(numeric.__file__).resolve()==(view/'day_numeric_dex_controls.py').resolve()
        assert Path(lookup.__file__).resolve()==(view/'day_lookup_dex_controls.py').resolve()
        assert identity(Path(numeric.__file__))['sha256']=='2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4'
        save(out/'loaded-runner-identities.json', {name:{'path':str(Path(module.__file__).resolve()),**identity(Path(module.__file__))} for name,module in [('numeric',numeric),('lookup',lookup)]})
        modules=[load(name,view/'tests'/(name+'.py')) for name in ['test_day_numeric','test_day_lookup','test_ui_mutation_catalog']]
        suites=[unittest.defaultTestLoader.loadTestsFromModule(module) for module in modules]
        counts={module.__name__:suite.countTestCases() for module,suite in zip(modules,suites)}
        with (out/'unittest.log').open('w') as stream:
            tick=time.monotonic();run=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite(suites));seconds=time.monotonic()-tick
        assert all(identity(Path(path))==pin for path,pin in pins.items())
        assert all(identity(Path(path))==pin for path,pin in copies.items())
        result.update(passed=run.wasSuccessful(),status='FOCUSED_GUARDS_PASSED' if run.wasSuccessful() else 'FOCUSED_GUARDS_FAILED_PRESERVED',
                      tests_run=run.testsRun,test_module_counts=counts,failures=len(run.failures),errors=len(run.errors),skipped=len(run.skipped),
                      seconds=seconds,source_inputs_and_executed_copies_unchanged=True,
                      unittest_log=identity(out/'unittest.log'),java_subprocess_log=identity(out/'extractor-commands.jsonl') if (out/'extractor-commands.jsonl').exists() else None)
        if not run.wasSuccessful():raise AssertionError('Focused test failure; see exact unittest.log')
    except BaseException as error:
        result.update(error=repr(error));(out/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result)
        print(json.dumps(result,indent=2))
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())<=256*1024*1024

if __name__=='__main__':main()
