#!/usr/bin/env python3
"""Derive the bounded lookup gate from the inspected numeric pipeline and new observer guards."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import shutil
import traceback

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT/'stage-02/project'
NUMERIC=PROJECT/'day_numeric_dex_controls.py'

PREAMBLE='''#!/usr/bin/env python3
"""Bind ten lookup Java faults and two actual production-D8 lookup faults.

The acceptance entry requires the complete current UI fault evidence, a positive
instruction match to the signed APK, that APK's two original getters and exact
positive restoration. The one-method compiler is also usable for explicitly
scoped private studies; it alone makes no signed packaging or ART claim.
"""
from __future__ import annotations

from datetime import datetime, timezone
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import zipfile

import build
import day_numeric_dex_controls as numeric
import ui_mutation_catalog as catalog
import ui_runtime_policy

METHOD = catalog.LOOKUP_METHOD
TARGET, SIGNATURE = METHOD.split('->', 1)
HELPER_NAME = 'recovered.ui.DayTriggerLookupMethods'
HELPER_CLASS = 'recovered/ui/DayTriggerLookupMethods.class'
# Preserve existing shared nested-class flags; do not substitute minimal study stubs.
HELPER_CLASS_SHA256 = 'df4383e951f3e897f58adc33f27847198f52cd455ccc5a9b22eb70712f66e082'
DEPENDENCY_PATH = numeric.DEPENDENCY_PATH
DEPENDENCY_SHA256 = '159061ce552e3364c113f28e72e5a4c1bc091a21153d0d5e0a793d2f773b0229'
ORIGINAL_METHOD_SHA256 = 'afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e'
GETTERS = {
    'Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;': 'f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;': '41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3',
}
JAVA_FAILURE_COUNTS = {
    'case-sensitive': 127, 'reverse-receiver': 3, 'skip-null-entry': 2, 'null-query-early-return': 3,
    'last-match': 233, 'trim-query': 1, 'indexed-loop': 369, 'extra-iteration-after-match': 233,
    'swallow-iterator-fault': 25, 'replace-injected-npe-identity': 6,
}
'''

PARTITION='''def validate_dependencies(root: Path, registry: list[dict]) -> set[str]:
    require(numeric.DEPENDENCY_PATH == DEPENDENCY_PATH and numeric.DEPENDENCY_SHA256 == DEPENDENCY_SHA256,
            'Numeric and lookup dependency declarations disagree')
    selected = numeric.validate_dependency_declaration(root, registry)
    require(selected[METHOD] == set(GETTERS) and selected[numeric.METHOD] == set(numeric.GETTERS),
            'Combined numeric/lookup dependency partitions differ')
    return selected[METHOD]
'''

RUN_COMMAND='''    def run(folder, name, argv, expected=0, timeout=120):
        folder.mkdir(parents=True, exist_ok=True)
        stdout, stderr = folder / (name + '.stdout.log'), folder / (name + '.stderr.log')
        require(not stdout.exists() and not stderr.exists(), 'Lookup command output already exists')
        started = datetime.now(timezone.utc).isoformat(); tick = time.monotonic_ns(); code = None
        witnesses = {}
        try:
            with stdout.open('xb') as out, stderr.open('xb') as err:
                for role, stream in [('stdout', out), ('stderr', err)]:
                    stat = os.fstat(stream.fileno())
                    witnesses[role] = {'device': stat.st_dev, 'inode': stat.st_ino}
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=out, stderr=err, timeout=timeout).returncode
        finally:
            finished_tick = time.monotonic_ns()
            outputs = {}
            for role, path in [('stdout', stdout), ('stderr', stderr)]:
                stat = path.stat()
                require(witnesses.get(role) == {'device': stat.st_dev, 'inode': stat.st_ino},
                        'Lookup command output path no longer names its exclusively created stream')
                outputs[role] = {'path': path.relative_to(root).as_posix(), **identity(path),
                                 'exclusive_stream_witness': witnesses[role]}
            row = {'name': name, 'argv': list(map(str, argv)), 'started_utc': started,
                   'ended_utc': datetime.now(timezone.utc).isoformat(),
                   'started_monotonic_ns': tick, 'finished_monotonic_ns': finished_tick,
                   'duration_nanoseconds': finished_tick - tick, 'timeout_seconds': timeout,
                   'returncode': code, **outputs}
            report['commands'].append(row); write_json(destination, report)
        require(code == expected, 'Lookup command failed: ' + name)
        return row
'''

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def replace_once(text,old,new):
    assert text.count(old)==1,repr(old)
    return text.replace(old,new,1)

def main():
    out=ROOT/'reports/08-gate-authoring';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-author.py');shutil.copy2(ROOT/'lookup_report_guards.py.txt',out/'lookup_report_guards.py.txt')
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat()};save(out/'result.json',result)
    try:
        assert sha(NUMERIC)=='f211cfe656674f1bae4485d98bd2619ce03f53c2f5f80eae7fa8974617d1d1bc'
        source=NUMERIC.read_text();tree=ast.parse(source);lines=source.splitlines(True)
        nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
        def function(name):
            node=nodes[name];return ''.join(lines[node.lineno-1:node.end_lineno])
        def lookup(text):
            for old,new in [('DayTriggerValueMethods','DayTriggerLookupMethods'),('DayTriggerParityCases','DayLookupParityCases'),
                            ('DayNumericControlHarness','DayLookupControlHarness'),('numericValue','findEntry'),
                            ('DAY_','LOOKUP_'),('load_day_mutations','load_lookup_mutations'),
                            ('day-numeric','day-lookup'),('day_numeric','day_lookup'),('Numeric','Lookup'),('NUMERIC','LOOKUP'),('numeric','lookup')]:
                text=text.replace(old,new)
            return text
        pieces=[PREAMBLE]
        pieces += [function(name) for name in ['require','sha','identity','write_json','require_counts']]
        pieces += [PARTITION,lookup(function('target_entry'))]
        compile_source=lookup(function('compile_target'))
        compile_source=replace_once(compile_source,"'other_original_methods_unchanged': len(old_methods) - 1, 'non_target_class_text_unchanged': True,",
            "'other_original_methods_unchanged': len(old_methods) - 1, 'non_target_class_text_unchanged': True,\n               'preservation_scope': 'One-method micro-DEX only; signed class also contains the pre-existing constant mapping and recovered r0. Signed p0 instructions are independently bound.',")
        pieces += [compile_source,lookup(function('class_pins')),(ROOT/'lookup_report_guards.py.txt').read_text()]
        java=lookup(function('validate_java_controls'))
        java=java.replace('len(selected) == 13','len(selected) == 10').replace('All thirteen actual','All ten actual')
        pieces.append(java)
        run=lookup(function('run_controls'))
        run=run.replace("'original_dependency_methods': 3, 'expected_java_faults': 13", "'original_dependency_methods': 2, 'expected_java_faults': 10")
        run=replace_once(run,"for name in ('integer-zero', 'decimal-zero'):","for name in ('case-sensitive', 'last-match'):")
        run=replace_once(run,'cases=1291, execution_paths=3','cases=371, execution_paths=3')
        run=replace_once(run,'original_instruction_count=32, rebuilt_instruction_count=25','original_instruction_count=26, rebuilt_instruction_count=23')
        begin=run.index('    def run(folder, name, argv, expected=0, timeout=120):')
        end=run.index('\n    try:\n        entry = target_entry(root)',begin)
        run=run[:begin]+RUN_COMMAND+run[end:]
        run=replace_once(run,"root / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java', *selected_original,",
            "root / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',\n                  root / catalog.DAY_HELPER_PATH, host / numeric.HELPER_CLASS, *selected_original,")
        run=replace_once(run,"entry = target_entry(root)","entry = target_entry(root)\n        numeric_entry = numeric.target_entry(root)\n        registry = json.loads((root / 'source/java-method-map.json').read_text())\n        class_mappings = [row for row in registry if row['target'] == TARGET]\n        require({row['method'] for row in class_mappings} == {SIGNATURE, numeric_entry['method'], 'requiresScheduleExactAlarm()Z'},\n                'DayTrigger class registry differs from the existing constant and two ordinary-method mappings')\n        report['signed_class_registered_methods'] = sorted(row['method'] for row in class_mappings)")
        run=replace_once(run,"positive_dex, positive_binding = compile_target(build, root, index, entry, host / HELPER_CLASS, output / 'positive-pipeline', run, java, jar)",
            "positive_dex, positive_binding = compile_target(build, root, index, entry, host / HELPER_CLASS, output / 'positive-pipeline', run, java, jar)\n        require(sha(host / numeric.HELPER_CLASS) == numeric.HELPER_CLASS_SHA256, 'Positive numeric class changed')")
        run=replace_once(run,"for name, dex in [('signed-apk', getter), ('positive-transplant', positive_dex)]:",
            "run(output, 'numeric-before-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', getter, numeric.METHOD, output / 'numeric-before-instructions.json'])\n        for name, dex in [('signed-apk', getter), ('positive-transplant', positive_dex)]:")
        run=replace_once(run,"validate_java_controls(root, java_control_records)\n        report.update(passed=True",
            "validate_java_controls(root, java_control_records)\n        run(output, 'numeric-after-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', getter, numeric.METHOD, output / 'numeric-after-instructions.json'])\n        require((output / 'numeric-before-instructions.json').read_bytes() == (output / 'numeric-after-instructions.json').read_bytes(),\n                'Signed positive numeric method changed during lookup controls')\n        report['signed_numeric_method_unchanged'] = True\n        report['micro_dex_preservation_scope'] = 'Only p0 changed in each micro-DEX. Other original methods stay original there; signed class has its complete three registered mappings.'\n        report.update(passed=True")
        pieces.append(run)
        target=PROJECT/'day_lookup_dex_controls.py';assert not target.exists();target.write_text('\n\n\n'.join(pieces)+'\n')
        ast.parse(target.read_text())
        assert sha(NUMERIC)=='f211cfe656674f1bae4485d98bd2619ce03f53c2f5f80eae7fa8974617d1d1bc'
        result.update(passed=True,status='LOOKUP_DEX_GATE_SOURCE_AUTHORED_PARSE_ONLY',path=str(target),bytes=target.stat().st_size,
                      sha256=sha(target),numeric_source_unchanged=True,actual_gate_execution=False)
    except BaseException as error:
        result.update(status='AUTHORING_FAILED_PRESERVED',error=repr(error));(out/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
