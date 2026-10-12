#!/usr/bin/env python3
"""Read-only source derivation for a proposed combined hosted workflow.

This performs no project materialization, tests, Java execution or APK work.
All output belongs to this bounded tmpfs design study.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import collections
import copy
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import sys
import traceback

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'reports/22-combined-host-design-source'
NUMERIC = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
TOOLS = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
MERGE = ROOT / 'checkpoints/04-numeric-filesystem-merge'
FINAL = ROOT / 'checkpoints/05-lookup-recorder-successor'
PROOF = ROOT / 'checkpoints/03-source-three-path-controls'
PROJECT = ROOT / 'stage-04/project'
VIEW = ROOT / 'reports/20-lookup-recorder-focused-controls/project-view'
BASE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
PINNED = {
    NUMERIC: 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf',
    TOOLS: '815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493',
    MERGE: '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350',
    FINAL: '87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5',
    PROOF: 'd40df7530d090b6717d99e5011f1a0e5c0774297576ecc88047737301812a292',
}
READS = {}

def identity(path):
    path = Path(path)
    before = path.stat()
    assert path.is_file() and not path.is_symlink()
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.stat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    return {'bytes': after.st_size, 'sha256': digest}

def bound(path, expected=None):
    path = Path(path)
    actual = identity(path)
    if expected is not None:
        assert actual == {k: expected[k] for k in ('bytes', 'sha256')}, (str(path), actual, expected)
    READS[str(path)] = actual
    return path

def read(path, expected=None):
    return json.loads(bound(path, expected).read_bytes())

def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, bound(path))
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result

def method_names(path):
    tree = ast.parse(bound(path).read_text())
    names = [node.name + '.' + child.name for node in tree.body if isinstance(node, ast.ClassDef)
             for child in node.body if isinstance(child, ast.FunctionDef) and child.name.startswith('test_')]
    assert len(names) == len(set(names))
    return sorted(names)

def dex_defined_methods(raw):
    assert raw[:8] == b'dex\n035\x00'
    u32 = lambda p: struct.unpack_from('<I', raw, p)[0]
    def uleb(pos):
        result = shift = 0
        for _ in range(5):
            byte = raw[pos]; pos += 1
            result |= (byte & 127) << shift
            if byte < 128: return result, pos
            shift += 7
        raise ValueError('Overlong ULEB128')
    def dex_string(index):
        pos = u32(u32(0x3c) + 4 * index)
        _, pos = uleb(pos)
        return raw[pos:raw.index(0, pos)].decode('utf-8')
    def dex_type(index): return dex_string(u32(u32(0x44) + 4 * index))
    def proto(index):
        pos = u32(0x4c) + 12 * index
        returned, parameters = u32(pos + 4), u32(pos + 8)
        args = [] if not parameters else [dex_type(struct.unpack_from('<H', raw, parameters + 4 + 2 * n)[0])
                                         for n in range(u32(parameters))]
        return '(' + ''.join(args) + ')' + dex_type(returned)
    def method(index):
        pos = u32(0x5c) + 8 * index
        owner, descriptor = struct.unpack_from('<HH', raw, pos)
        return dex_type(owner) + '->' + dex_string(u32(pos + 4)) + proto(descriptor)
    keys = []
    classes = u32(0x60)
    for n in range(classes):
        pos = u32(u32(0x64) + 32 * n + 24)
        assert pos
        counts = []
        for _ in range(4):
            count, pos = uleb(pos); counts.append(count)
        for _ in range(counts[0] + counts[1]):
            _, pos = uleb(pos); _, pos = uleb(pos)
        for count in counts[2:]:
            index = 0
            for _ in range(count):
                diff, pos = uleb(pos); index += diff
                _, pos = uleb(pos); code, pos = uleb(pos)
                assert code
                keys.append(method(index))
    assert len(keys) == len(set(keys))
    return classes, sorted(keys)

def lookup_commands(project, folder, java, numeric_method, lookup_method, flags):
    output = Path(project) / folder
    jar = str(Path(project) / 'tools/lib/jadx-r2721.4574686-all.jar')
    cp = ':'.join([jar, str(Path(project) / 'build/java/hostclasses'), str(Path(project) / 'tools/classes')])
    commands = []
    def add(directory, name, code, argv):
        commands.append({'directory': directory, 'name': name, 'expected_returncode': code,
                         'timeout_seconds': 120, 'argv': list(map(str, argv))})
    def pipeline(name):
        p = output / name
        add(name, 'd8-helper', 0, [java, '-Xmx512m', '-cp', jar, 'com.android.tools.r8.D8', '--release', '--no-desugaring', '--min-api', '23', '--output', p / 'd8', p / 'inputs.jar'])
        add(name, 'disassemble-helper', 0, [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main', 'd', '--api', '23', '--use-locals', '-o', p / 'helper-smali', p / 'd8/classes.dex'])
        add(name, 'assemble-target', 0, [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main', 'a', '--api', '23', '-j', '2', '-o', p / 'lookup-target.dex', p / 'target-smali'])
    def inspect(name, dex, target):
        add('', name, 0, [java, '-Xmx512m', '-cp', cp, 'InspectMethod', dex, target, output / (name + '.json')])
    def execute(name, code):
        add(name, 'execute', code, [java, *flags, '-Xmx512m', '-cp', cp, 'DayLookupControlHarness', output / name / 'config.json', output / name / 'result.json'])
    pipeline('positive-pipeline')
    getter = Path(project) / 'build/hybrid/classes3.dex'
    inspect('numeric-before-instructions', getter, numeric_method)
    inspect('signed-apk-instructions', getter, lookup_method)
    inspect('positive-transplant-instructions', output / 'positive-pipeline/lookup-target.dex', lookup_method)
    execute('positive', 0)
    for name in ('case-sensitive', 'last-match'):
        pipeline(name + '-pipeline'); execute(name + '-dex-fault', 3)
    for name, code in [('original-as-rebuilt-rejected', 1), ('wrong-helper-class-rejected', 1), ('positive-restoration', 0)]:
        execute(name, code)
    inspect('numeric-after-instructions', getter, numeric_method)
    assert len(commands) == 19
    return commands

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, OUT / 'executed-collector.py')
    result = {'status': 'RUNNING', 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Manifest/source-only design derivation. No full tree scan/materialization, test execution, Java, D8, APK build, signing, Android, or workflow activation.'}
    try:
        capsules = {}
        for root, sha in PINNED.items():
            capsules[root] = read(root / 'checkpoint.json')
            assert READS[str(root / 'checkpoint.json')]['sha256'] == sha
        source_rows = {row['path']: row for row in capsules[TOOLS]['files'] if row['path'].startswith('source/')}
        assert len(source_rows) == 9
        for name, row in source_rows.items(): bound(TOOLS / name, row)
        tools = TOOLS / 'source/tools/day_numeric_acceptance'
        pins = read(tools / 'pins.json')
        inputs = module('inputs', tools / 'inputs.py')
        verify = module('numeric_design_verifier', tools / 'verify.py')
        base = read(BASE / 'reports/release-input-snapshot.json', pins['baseline_manifest'])
        inputs.validate_snapshot(base)
        numeric_raw = gzip.decompress(bound(NUMERIC / 'evidence/future-input-snapshot.json.gz').read_bytes())
        numeric = inputs.validate_snapshot(json.loads(numeric_raw))
        final_raw = gzip.decompress(bound(FINAL / 'future-input-snapshot.json.gz').read_bytes())
        final = inputs.validate_snapshot(json.loads(final_raw))
        assert identity_bytes(numeric_raw) == capsules[NUMERIC]['future_manifest']
        assert identity_bytes(final_raw) == capsules[FINAL]['future_manifest']
        numeric_changes = capsules[NUMERIC]['source_changes']
        assert numeric_changes == pins['source_changes'] and len(numeric_changes) == 19
        assert inputs.derive(base, numeric_changes) == numeric
        numeric_rows = {row['path']: row for row in capsules[NUMERIC]['files']}
        for row in numeric_changes: bound(NUMERIC / row['source'], numeric_rows[row['source']])
        overlay = read(FINAL / 'complete-future-overlay-manifest.json')
        lookup_changes = []
        source_resolutions = []
        for row in overlay['changes']:
            after = {k: row['after'][k] for k in ('bytes', 'sha256')}
            before = None if row['baseline'] is None else {k: row['baseline'][k] for k in ('bytes', 'sha256')}
            resolved = (FINAL if row['path'] in {'day_lookup_dex_controls.py', 'tests/test_day_lookup.py'} else MERGE) / 'project' / row['path']
            bound(resolved, after); bound(PROJECT / row['path'], after)
            source_resolutions.append({'path': row['path'], 'payload': str(resolved), 'identity': after})
            lookup_changes.append({'path': row['path'], 'baseline': before, 'candidate': after,
                                   'must_be_absent_if_new': row['must_be_absent_if_new'], 'source': 'project/' + row['path']})
        assert len(lookup_changes) == 21 and inputs.derive(numeric, lookup_changes) == final
        numeric_names = {row['path'] for row in numeric_changes}
        lookup_names = {row['path'] for row in lookup_changes}
        union = sorted(numeric_names | lookup_names)
        only = sorted(numeric_names - lookup_names)
        assert len(union) == 25 and len(only) == 4
        final_by_name = {r['path']: r for r in lookup_changes}
        union_rows = []
        for name in union:
            bound(PROJECT / name, {'bytes': final['entries'][name]['size'], 'sha256': final['entries'][name]['sha256']})
            union_rows.append({'path': name, 'baseline': base['entries'].get(name), 'after_numeric': numeric['entries'].get(name),
                              'final': final['entries'][name], 'numeric_stage': name in numeric_names, 'lookup_stage': name in lookup_names})
        assert len(set(final['entries']) - set(base['entries'])) == 13
        assert all(base['entries'][name] == final['entries'][name] for name in set(base['entries']) - set(union))
        boundaries = {'baseline_commit': pins['baseline_commit'], 'numeric_commit': pins['overlay_commit'],
                      'numeric_stage_changes': numeric_changes, 'lookup_stage_changes': lookup_changes,
                      'lookup_payload_resolutions': source_resolutions, 'union': union_rows,
                      'numeric_only_paths': [{ 'path': name, **final['entries'][name]} for name in only],
                      'complete_snapshots': [{ 'stage': label, 'files': value['files'], 'snapshot_sha256': value['snapshot_sha256'], 'manifest': raw_id}
                                             for label, value, raw_id in [('baseline',base,identity(BASE/'reports/release-input-snapshot.json')),
                                                                        ('numeric',numeric,identity_bytes(numeric_raw)),('combined',final,identity_bytes(final_raw))]],
                      'manifest_derivation_only': True, 'actual_full_tree_scans_pending': True,
                      'stage_new_files': [sum(r['baseline'] is None for r in rows) for rows in (numeric_changes, lookup_changes)],
                      'union_changed_paths': len(union), 'union_new_inputs': 13, 'untouched_baseline_entries': len(set(base['entries'])-set(union))}
        save('two-stage-source-contract.json', boundaries)
        registry = read(PROJECT / 'source/java-method-map.json')
        ui = read(PROJECT / 'source/ui-methods.json')
        provenance = read(PROJECT / 'tests/fixtures/provenance.json')
        deps = read(PROJECT / 'tests/fixtures/original-dependencies.json')['dependencies']
        keys = {row['target'] + '->' + row['method'] for row in registry}
        dep_keys = {row['target'] + '->' + row['method'] for row in deps}
        assert len(registry) == len(keys) == 1244 and len(dep_keys) == len(deps) == 5 and not keys & dep_keys
        fixture = bound(PROJECT / 'tests/fixtures/original-methods.dex')
        dex_classes, dex_keys = dex_defined_methods(fixture.read_bytes())
        assert set(dex_keys) == keys | dep_keys and dex_classes == 607 and len(dex_keys) == 1249
        assert provenance['fixture_sha256'] == identity(fixture)['sha256'] and provenance['methods'] == len(dex_keys)
        day_rows = [row for row in registry if row['target'] == 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;']
        assert len(day_rows) == 3
        save('day-trigger-registry-and-dependencies.json', {'class_mappings': day_rows, 'dependencies': deps, 'fixture': identity(fixture),
                                                          'actual_dex_defined_methods': len(dex_keys), 'actual_dex_classes': dex_classes,
                                                          'exact_registry_plus_dependency_key_set': True, 'dependency_credit': 0})
        # Catalog preparation computes source mutations only. It launches no children.
        sys.path[:0] = [str(VIEW), str(BASE)]
        import build
        bound(BASE / 'build.py'); bound(BASE / 'constructor_owner.py'); bound(BASE / 'ui_runtime_policy.py')
        build.ROOT = VIEW
        import ui_negative_control, day_numeric_dex_controls as day_numeric, day_lookup_dex_controls as day_lookup
        for path in VIEW.rglob('*'):
            if path.is_file(): bound(path)
        assert identity(Path(day_lookup.__file__)) == identity(PROJECT / 'day_lookup_dex_controls.py')
        assert identity(Path(day_numeric.__file__)) == identity(PROJECT / 'day_numeric_dex_controls.py')
        jobs = ui_negative_control.prepared_mutations()
        inventory = [{'name': job['name'], 'source': job['source'].relative_to(VIEW).as_posix(),
                      'mutant_sha256': hashlib.sha256(job['mutant'].encode()).hexdigest(),
                      'required_cases': job['required_cases'], 'widget': job.get('widget', False),
                      'day_numeric': job.get('day_numeric', False)} for job in jobs]
        assert len(inventory) == 101 and inventory[:91] == pins['ui_mutation_inventory']
        save('proposed-ui-mutation-inventory.json', inventory)
        test_changes = []
        added = 0
        for row in lookup_changes:
            if row['path'].startswith('tests/test_') and row['path'].endswith('.py'):
                current = method_names(PROJECT / row['path'])
                old = [] if row['baseline'] is None else method_names(NUMERIC / 'project' / row['path'])
                removed = sorted(set(old) - set(current))
                if removed:
                    assert row['path'] == 'tests/test_v9.py'
                    assert removed == ['UiSourceTests.test_exact_eleven_methods_and_classes']
                    assert sorted(set(current)-set(old)) == ['UiSourceTests.test_exact_twelve_methods_and_eleven_classes']
                    assert len(current) == len(old)
                added += len(current) - len(old)
                test_changes.append({'path': row['path'], 'before_count':len(old), 'after_count':len(current),
                                     'added': sorted(set(current)-set(old)), 'removed': removed,
                                     'net_count_delta':len(current)-len(old)})
        assert added == 49
        proof_members = {row['path']: row for row in read(PROOF / 'evidence-files.json')}
        retained = {}
        for name in ['positive-pipeline/method-body-binding.json', 'positive/config.json', 'positive/result.json']:
            relative = 'reports/12-micro-dex-three-path-corrected/' + name
            retained[name] = read(ROOT / relative, proof_members[relative])
        positive = retained['positive/result.json']
        assert positive['cases'] == 371 and positive['mismatchCount'] == 0 and positive['unsupportedCount'] == 0
        case_counts = dict(pins['suite_cases']); case_counts['ui'] += positive['cases']
        counts = {'scope': 'Source-derived expectations for a future combined run, not a completed full run.',
                  'registered_methods':len(registry), 'target_classes':len({r['target'] for r in registry}),
                  'ui_methods':len(ui), 'ui_classes':len({r['target'] for r in ui}),
                  'fixture_methods':len(dex_keys), 'fixture_classes':dex_classes, 'uncredited_dependencies':len(deps),
                  'suite_cases':case_counts, 'all_cases':sum(case_counts.values()),
                  'python_tests':pins['python_tests']+added, 'python_test_count_status':'Derived from parent expectation plus exact AST added-test inventory; whole-suite execution pending.',
                  'python_test_changes':test_changes, 'java_ui_faults':len(inventory), 'unchanged_parent_java_prefix':91,
                  'numeric_java_faults':13, 'lookup_java_faults':10, 'numeric_dex_faults':2, 'lookup_dex_faults':2,
                  'provenance_rejections':4, 'execution_paths_per_registered_method':3,
                  'case_count_parent':pins['all_cases'], 'added_lookup_cases':positive['cases']}
        assert counts['all_cases'] == 195151 and counts['python_tests'] == 357 and counts['target_classes'] == 605
        save('source-derived-counts.json', counts)
        save('lookup-prior-method-proof-bindings.json', {'scope': 'Actual prior method-only proof; old signed APK supplied unchanged getter dependencies, not p0. New signed primary proof remains pending.',
                 'checkpoint': identity(PROOF/'checkpoint.json'), 'positive_pipeline':retained['positive-pipeline/method-body-binding.json'],
                 'runtime_class_names':sorted(retained['positive/config.json']['classPins']),
                 'old_config_identity':identity(ROOT/'reports/12-micro-dex-three-path-corrected/positive/config.json'),
                 'raw_report_identity':identity(ROOT/'reports/12-micro-dex-three-path-corrected/positive/result.json'),
                 'input_inventory_sha256':positive['inputInventorySha256'],
                 'original_instruction_count':26,'rebuilt_instruction_count':23,'edges_per_path':4,
                 'java_fault_mismatch_counts':day_lookup.JAVA_FAILURE_COUNTS,
                 'vm_null_cases':sorted(day_lookup.VM_NULL_CASES)})
        # Extract the actual app acceptance order without invoking its main.
        main = next(n for n in ast.parse((PROJECT/'acceptance.py').read_text()).body if isinstance(n, ast.FunctionDef) and n.name=='main')
        commands = next(ast.literal_eval(n.value) for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='commands' for t in n.targets))
        commands += [('signed-source-edit',['full_apk_edit_probe.py']),('final-positive-host-tests',['test.py','--three-way'])]
        assert json.loads(json.dumps(commands)) == pins['gate_commands']
        fresh = next(ast.literal_eval(n.value) for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='names' for t in n.targets))
        fresh.append('full-apk-edit-probe.json')
        assert len(fresh)==24 and [n for n in fresh if n!='day-lookup-dex-controls.json']==pins['fresh_reports']
        numeric_cmds = [{'directory':d,'name':n,'expected_returncode':c,'timeout_seconds':120,'argv':a}
                        for d,n,c,a in verify.expected_numeric_commands('<project>', 'reports/<numeric-evidence>', '<java>')]
        lookup_cmds = lookup_commands('<project>', 'reports/<lookup-evidence>', '<java>', day_numeric.METHOD, day_lookup.METHOD, verify.JVM_FLAGS)
        save('proposed-command-and-report-contract.json', {'gate_order':commands,'gate_count':len(commands),
             'fresh_reports':fresh,'fresh_report_count':len(fresh), 'numeric_commands':numeric_cmds,'lookup_commands':lookup_cmds,
             'method_command_count':len(numeric_cmds)+len(lookup_cmds),'method_stream_count':2*(len(numeric_cmds)+len(lookup_cmds)),
             'ui_gate_timeout_seconds':5400,'other_gate_timeout_seconds':1200,'full_acceptance_timeout_seconds':pins['acceptance_timeout_seconds'],
             'hosted_job_timeout_minutes':pins['source_job_timeout_minutes'],'materialization_timeout_seconds':pins['materialize_timeout_seconds'],
             'all_actual_commands_pending':True,'symbolic_paths_are_design_only':True})
        save('ancestor-tooling-source-pins.json', {'checkpoint':identity(TOOLS/'checkpoint.json'),
                                                'files':list(source_rows.values()),'runtime_manifest':read(tools/'runtime-files.json')})
        # Demonstrate the retained boundary rejection using the already pinned utility.
        try: inputs.derive(base, lookup_changes)
        except ValueError as error: skipped_boundary = repr(error)
        else: raise AssertionError('Lookup overlay unexpectedly accepted the 1242 baseline directly')
        save('direct-baseline-rejection.json', {'scope':'Existing numeric inputs.derive exercised on manifest dictionaries only.',
                                              'direct_lookup_on_1242_baseline_rejected':True,'actual_error':skipped_boundary})
        assert all(identity(Path(path)) == pin for path,pin in READS.items())
        save('read-input-identities.json', READS)
        result.update(status='SOURCE_ONLY_COMBINED_WORKFLOW_DESIGN_FACTS_VERIFIED',passed=True,
                      source_inputs_unchanged=True,complete_manifest_rows=[base['files'],numeric['files'],final['files']],
                      distinct_final_source_paths=25,new_inputs=13,registered_methods=1244,expected_cases=195151,
                      expected_python_tests=357,prepared_java_faults=101,old_91_prefix_exact=True,
                      inspected_tooling_source_files=9,bound_read_files=len(READS),
                      tests_executed=0,application_executions=0,full_tree_materializations=0)
    except BaseException as error:
        result.update(error=repr(error));(OUT/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat()
        save('result.json',result)
        print(json.dumps(result,indent=2))
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file()) <= 256*1024*1024

def identity_bytes(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__': main()
