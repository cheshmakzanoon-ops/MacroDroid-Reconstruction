"""Independently expand the frozen lookup producer AST; run no app or compiler."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import hashlib
import json
import shutil
import stat
import subprocess

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
OUT = BASE / 'lookup-command-contract-review'
LOOKUP08 = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/04-numeric-filesystem-merge')
LOOKUP09 = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/05-lookup-recorder-successor')
DESIGN = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/06-combined-host-workflow-design')
NUMERIC = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
GIT = BASE / 'verification.git'
BASELINE = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
READS = {}

def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'mode': stat.S_IMODE(path.lstat().st_mode)}

def read(path, copy_name):
    before = identity(path)
    raw = path.read_bytes()
    assert identity(path) == before
    READS[str(path)] = before
    target = OUT / 'inputs' / copy_name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    target.chmod(before['mode'])
    return raw

def record(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def git_read(commit, path, name):
    raw = subprocess.check_output(['git', '--git-dir=' + str(GIT), 'show', commit + ':' + path])
    mode, _, oid, _ = subprocess.check_output(['git', '--git-dir=' + str(GIT), 'ls-tree', commit, '--', path]).decode().split()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == oid
    target = OUT / 'inputs' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    target.chmod(int(mode, 8) & 0o777)
    return raw, {'commit': commit, 'path': path, 'git_blob_sha1': oid, **identity(target)}

def function(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)

def literal_assignment(tree, name):
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return ast.literal_eval(node.value)

def dump(node):
    return ast.dump(node, include_attributes=False)

def expression(node, env):
    """Evaluate only immutable symbolic path/list expressions, never Python calls."""
    if isinstance(node, ast.Constant):
        assert type(node.value) in (str, int, bool, type(None))
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.Attribute):
        if node.attr == 'parent':
            return expression(node.value, env).parent
        return env[ast.unparse(node)]
    if isinstance(node, (ast.List, ast.Tuple)):
        rows = []
        for item in node.elts:
            if isinstance(item, ast.Starred):
                rows.extend(expression(item.value, env))
            else:
                rows.append(expression(item, env))
        return rows
    if isinstance(node, ast.BinOp):
        left, right = expression(node.left, env), expression(node.right, env)
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Add):
            return left + right
    raise AssertionError('Unsupported symbolic expression: ' + ast.unparse(node))

def command_calls(node):
    return sorted((n for n in ast.walk(node) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Name) and n.func.id in {'run', 'execute', 'compile_target'}),
                  key=lambda n: (n.lineno, n.col_offset))

OUT.mkdir(exist_ok=False)
for root, pin, name in [
    (LOOKUP08, '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350', 'lookup08-checkpoint.json'),
    (LOOKUP09, '87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5', 'lookup09-checkpoint.json'),
    (DESIGN, '3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f', 'design-checkpoint.json'),
]:
    raw = read(root / 'checkpoint.json', name)
    assert hashlib.sha256(raw).hexdigest() == pin

manifest = json.loads(read(LOOKUP09 / 'complete-future-overlay-manifest.json', 'complete-future-overlay-manifest.json'))
assert len(manifest['changes']) == 21
payloads, sources = {}, {}
for row in manifest['changes']:
    parent = LOOKUP09 if row['payload_source'].startswith('this-capsule/') else LOOKUP08
    source = parent / 'project' / row['path']
    raw = read(source, 'final-overlay/' + row['path'])
    assert identity(source) == row['after']
    payloads[row['path']] = raw
    sources[row['path']] = str(source)
assert set(row['path'] for row in manifest['changes'] if row['payload_source'].startswith('this-capsule/')) == {
    'day_lookup_dex_controls.py', 'tests/test_day_lookup.py'}
lookup = payloads['day_lookup_dex_controls.py'].decode()
numeric = payloads['day_numeric_dex_controls.py'].decode()
assert hashlib.sha256(lookup.encode()).hexdigest() == '0b72325dbdaf60525f07a7b72708b9096d1e585ef5e1601332ceaac9aa67c8c9'
assert hashlib.sha256(numeric.encode()).hexdigest() == '2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4'
assert read(LOOKUP09 / 'unchanged-provider/day_numeric_dex_controls.py', 'unchanged-provider.py') == numeric.encode()
previous = read(NUMERIC / 'project/day_numeric_dex_controls.py', 'numeric08-provider.py').decode()
trees = {name: ast.parse(raw) for name, raw in [('lookup', lookup), ('numeric', numeric), ('previous', previous)]}
shared = []
for name in ('command_clock', 'command_file_stat', 'CommandStreamEvidence'):
    a = next(n for n in trees['numeric'].body if getattr(n, 'name', None) == name)
    b = next(n for n in trees['previous'].body if getattr(n, 'name', None) == name)
    assert dump(a) == dump(b)
    shared.append({'name': name, 'ast_equal': True, 'source_equal': ast.get_source_segment(numeric, a) == ast.get_source_segment(previous, b)})
assert all(row['source_equal'] for row in shared)

policy_raw, policy_git = git_read(BASELINE, 'project/ui_runtime_policy.py', 'baseline-ui-runtime-policy.py')
flags = literal_assignment(ast.parse(policy_raw), 'JVM_FLAGS')
catalog = ast.parse(payloads['ui_mutation_catalog.py'])
method = literal_assignment(catalog, 'LOOKUP_METHOD')
numeric_method = literal_assignment(catalog, 'DAY_METHOD')
project = PurePosixPath('<project>')
output = project / 'reports/<lookup-evidence>'
jar = project / 'tools/lib/jadx-r2721.4574686-all.jar'
environment = {'root': project, 'output': output, 'jar': jar, 'java': '<java>',
    'cp': ':'.join(map(str, [jar, project / 'build/java/hostclasses', project / 'tools/classes'])),
    'getter': project / 'build/hybrid/classes3.dex', 'METHOD': method,
    'numeric.METHOD': numeric_method, 'ui_runtime_policy.JVM_FLAGS': flags}
driver = function(trees['lookup'], 'run_controls')
run = function(driver, 'run')
defaults = dict(zip([a.arg for a in run.args.args][-len(run.args.defaults):], map(ast.literal_eval, run.args.defaults)))
assert defaults == {'expected': 0, 'timeout': 120}
try_body = next(n for n in driver.body if isinstance(n, ast.Try)).body
execute = next(n for n in try_body if isinstance(n, ast.FunctionDef) and n.name == 'execute')
execute_call, = command_calls(execute)
pipeline = function(trees['lookup'], 'compile_target')
pipeline_calls = command_calls(pipeline)
assert len(pipeline_calls) == 3 and all(n.func.id == 'run' for n in pipeline_calls)
expanded, source_order = [], []

def row(call, env, expected=None):
    assert call.func.id == 'run' and len(call.args) in (3, 4) and not call.keywords
    folder, name, argv = [expression(value, env) for value in call.args[:3]]
    expected = expression(call.args[3], env) if len(call.args) == 4 else defaults['expected']
    result = {'directory': folder.relative_to(output).as_posix(), 'name': name,
              'expected_returncode': expected, 'timeout_seconds': defaults['timeout'],
              'argv': [str(value) for value in argv]}
    if result['directory'] == '.':
        result['directory'] = ''
    assert type(expected) is int and expected in (0, 1, 3)
    expanded.append(result)

def process(statements, env):
    for statement in statements:
        if isinstance(statement, ast.FunctionDef):
            continue
        if isinstance(statement, ast.For):
            if not command_calls(statement):
                continue
            for value in expression(statement.iter, env):
                child = dict(env)
                names = [statement.target.id] if isinstance(statement.target, ast.Name) else [n.id for n in statement.target.elts]
                for name, item in zip(names, [value] if len(names) == 1 else value):
                    child[name] = item
                process(statement.body, child)
            continue
        for call in command_calls(statement):
            source_order.append({'line': call.lineno, 'expression': ast.unparse(call)})
            if call.func.id == 'compile_target':
                folder = expression(call.args[5], env)
                child = dict(env, folder=folder)
                for name in ('compiler_input', 'dex_dir', 'smali', 'target', 'dex'):
                    assignment = next(n for n in pipeline.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
                    child[name] = expression(assignment.value, child)
                for command in pipeline_calls:
                    row(command, child)
                assert isinstance(statement, ast.Assign) and isinstance(statement.targets[0], ast.Tuple)
                env[statement.targets[0].elts[0].id] = child['dex']
            elif call.func.id == 'execute':
                name = expression(call.args[0], env)
                expected = expression(call.args[2], env) if len(call.args) == 3 else 0
                folder = output / name
                row(execute_call, dict(env, folder=folder, path=folder / 'config.json', target=folder / 'result.json', expected=expected))
            else:
                row(call, env)

process(try_body, environment)
assert len(expanded) == 19
contract = json.loads(read(DESIGN / 'evidence/reports/22-combined-host-design-source/proposed-command-and-report-contract.json', 'proposed-command-and-report-contract.json'))
assert expanded == contract['lookup_commands']
assert contract['all_actual_commands_pending'] is True and contract['symbolic_paths_are_design_only'] is True
assert sum(r['expected_returncode'] == 3 for r in expanded) == 2
assert sum(r['expected_returncode'] == 1 for r in expanded) == 2
assert len({(r['directory'], r['name']) for r in expanded}) == 19
record('source-derived-nineteen-commands.json', {'schema': 1, 'scope': 'Static symbolic AST expansion; no child command executed.',
    'commands': expanded, 'source_call_order': source_order, 'matches_frozen_design_exactly': True,
    'successful_expected_zero': 15, 'expected_fault_exits_three': 2, 'expected_provenance_exits_one': 2,
    'timeout_seconds_each': 120, 'distinct_stream_roles': 38, 'runtime_policy_git': policy_git})

cwd_contract = json.loads(read(DESIGN / 'evidence/design-extra/producer-cwd-and-finalization-contract.json', 'producer-cwd-and-finalization-contract.json'))
read(DESIGN / 'DESIGN.md', 'DESIGN.md')
producer_checks = []
for label, tree in [('lookup', trees['lookup']), ('numeric', trees['numeric'])]:
    parent = function(tree, 'run_controls')
    child = function(parent, 'run')
    subprocess_calls = [n for n in ast.walk(child) if isinstance(n, ast.Call) and ast.unparse(n.func) == 'subprocess.run']
    assert len(subprocess_calls) == 1
    call = subprocess_calls[0]
    assert ast.unparse(next(k.value for k in call.keywords if k.arg == 'cwd')) == 'root'
    assert 'root = root.resolve()' in ast.unparse(parent)
    dictionaries = [n for n in ast.walk(child) if isinstance(n, ast.Dict)]
    assert not any(isinstance(k, ast.Constant) and k.value == 'cwd' for d in dictionaries for k in d.keys)
    producer_checks.append({'producer': label, 'actual_subprocess_cwd_expression': 'root',
        'root_resolved': True, 'independently_recorded_child_cwd_field': False,
        'subprocess_call': ast.unparse(call)})
    assert cwd_contract['sources'][label]['cwd_expression'] == 'root'
    assert cwd_contract['sources'][label]['independent_cwd_field'] is False
ui = ast.parse(payloads['ui_negative_control.py'])
callers = [n for n in ast.walk(ui) if isinstance(n, ast.Call) and ast.unparse(n.func) in
           {'day_numeric_dex_controls.run_controls', 'day_lookup_dex_controls.run_controls'}]
assert len(callers) == 2 and all(ast.unparse(n.args[0]) == 'build.ROOT' for n in callers)
assert [ast.unparse(n.func) for n in sorted(callers, key=lambda n:n.lineno)] == ['day_numeric_dex_controls.run_controls','day_lookup_dex_controls.run_controls']
build_raw, build_git = git_read(BASELINE, 'project/build.py', 'baseline-build.py')
assert any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROOT' for t in n.targets)
           and ast.unparse(n.value) == 'Path(__file__).resolve().parent' for n in ast.parse(build_raw).body)
outer_raw = read(DESIGN / 'parent-tooling-source/tools/day_numeric_acceptance/run_acceptance.py', 'outer-run-acceptance.py')
outer = function(ast.parse(outer_raw), 'run_child')
assert "'cwd': str(cwd)" in ast.unparse(outer)
record('cwd-and-provider-binding.json', {'schema': 1, 'scope': 'Source-bound cwd; no independent child cwd measurement claimed.',
    'producers': producer_checks, 'shared_numeric08_provider_text_and_ast': shared,
    'ui_call_order': [ast.unparse(n) for n in sorted(callers, key=lambda n:n.lineno)],
    'build_git': build_git, 'outer_receipt_records_cwd': True})

run_text = ast.unparse(run)
for needed in ("'expected_returncode': expected", "'timed_out': isinstance(failure, subprocess.TimeoutExpired)",
               "'error_type': None if failure is None", "'error': None if failure is None",
               "row['recording_finalized'] = numeric.command_clock()",
               "row['stream_context_entered'] = 'invocation_started' in observation.value"):
    assert needed in run_text, needed
assert run_text.index('observation.add_to(row)') < run_text.index("row['recording_finalized']") < run_text.index("report['commands'].append(row)")
report_start = next(n for n in driver.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='report' for t in n.targets)).value
report_fields = {ast.literal_eval(k):v for k,v in zip(report_start.keys, report_start.values)}
assert ast.literal_eval(report_fields['schema']) == 2
assert ast.literal_eval(report_fields['command_stream_evidence_schema']) == 2
assert ast.literal_eval(report_fields['command_stream_evidence_provider']) == 'day_numeric_dex_controls.CommandStreamEvidence'
record('lookup-finalization-contract.json', {'schema': 1, 'provider': 'day_numeric_dex_controls.CommandStreamEvidence',
    'report_schema': 2, 'command_stream_evidence_schema': 2,
    'required_success_flags': {'stream_context_entered': True, 'timed_out': False, 'error_type': None, 'error': None},
    'expected_returncode_is_recorded': True,
    'finalization_after_shared_context_add_to': True,
    'failed_rows_keep_actual_finalization_without_fabricating_context_finish': True,
    'required_clock_order': ['invocation_finished','stream_evidence.finished','recording_finalized','next command start / report finish'],
    'scope': 'Source and design contract verified; no new runtime producer or acceptance execution.'})

def registry_rows(raw):
    text = raw.decode(); decoder = json.JSONDecoder(); index = text.index('[') + 1; rows = []
    while True:
        while text[index].isspace() or text[index] == ',': index += 1
        if text[index] == ']': return rows
        value, end = decoder.raw_decode(text, index); rows.append((value,text[index:end]));index=end

baseline_registry, registry_git = git_read(BASELINE, 'project/source/java-method-map.json', 'baseline-java-method-map.json')
numeric_registry = read(NUMERIC / 'project/source/java-method-map.json', 'numeric08-java-method-map.json')
stages = [registry_rows(raw) for raw in (baseline_registry,numeric_registry,payloads['source/java-method-map.json'])]
assert [len(x) for x in stages] == [1242,1243,1244]
target = method.split('->')[0]
constant = [next((v,s) for v,s in rows if v['target']==target and v['method']=='requiresScheduleExactAlarm()Z') for rows in stages]
assert constant[0] == constant[1] == constant[2]
assert stages[0] == stages[1][:-1] and stages[1] == stages[2][:-1]
class_rows = [v for v,_ in stages[2] if v['target']==target]
assert {v['method'] for v in class_rows} == {'requiresScheduleExactAlarm()Z',numeric_method.split('->')[1],method.split('->')[1]}
record('unchanged-constant-and-stage-bindings.json', {'schema':1,'payload_count':21,'lookup09_changed_payload_paths':['day_lookup_dex_controls.py','tests/test_day_lookup.py'],
    'all_twenty_one_payload_bytes_and_modes_exact':True,'registry_counts':[1242,1243,1244],
    'prior_registry_entries_order_and_raw_object_bytes_unchanged':True,'constant_mapping':constant[0][0],
    'constant_raw_object_sha256':hashlib.sha256(constant[0][1].encode()).hexdigest(),
    'baseline_registry_git':registry_git,'active_source_changed':False})

harness = payloads['tests/java/DayLookupControlHarness.java'].decode()
checks = {
    'same_local_signed_dex_for_numeric_before_and_after': expanded[3]['argv'][6:8] == expanded[-1]['argv'][6:8]
        == [str(project/'build/hybrid/classes3.dex'),numeric_method],
    'positive_signed_lookup_compared_byte_for_byte': "(output / 'signed-apk-instructions.json').read_bytes() == (output / 'positive-transplant-instructions.json').read_bytes()" in lookup,
    'numeric_before_after_compared_byte_for_byte': "(output / 'numeric-before-instructions.json').read_bytes() == (output / 'numeric-after-instructions.json').read_bytes()" in lookup,
    'apk_and_signed_dex_are_before_after_pinned': "pinned = [apk, fixture, getter, jar" in lookup and 'all(identity(Path(p)) == value for p, value in pins.items())' in lookup,
    'config_names_literal_classes3_member': "'apk_member': 'classes3.dex'" in lookup and "'apk_member': 'classes3.dex'" in numeric,
    'harness_rejects_duplicate_signed_member': 'zip.stream().filter(item -> item.getName().equals(member)).count() == 1' in harness,
    'harness_stream_hash_matches_exact_local_signed_dex': 'sha(stream).equals(sha(getterDex))' in harness,
    'harness_postchecks_all_four_dex_and_apk_roles': 'List.of("originalFixture", "rebuiltApk", "rebuiltGetterDex", "targetDex")' in harness,
    'raw_report_bound_to_exact_config_and_loaded_classes': "report.get('inputIdentities') == config" in lookup and "report.get('loadedClassOrigins') == expected" in lookup,
    'all_other_micro_class_methods_and_text_unchanged': "all(new_methods[k] == v for k, v in old_methods.items() if k != SIGNATURE)" in lookup and "new_text.replace(replacement, '<LOOKUP>', 1) == old_text.replace(old, '<LOOKUP>', 1)" in lookup,
}
assert all(checks.values()), checks
record('signed-method-source-contract.json', {'schema':1,'checks':checks,
    'required_future_combined_verifier_binding':'Both method reports and their signed getters must equal the one measured final hybrid APK and unique classes3.dex; both inspected positive primary bodies must equal that signed DEX. Recheck all final raw input identities.',
    'micro_dex_scope':'Each micro-DEX replaces only its primary method; the whole micro class is intentionally different from the signed three-mapping class.',
    'actual_combined_signed_apk_execution_performed_here':False,'actual_java_or_d8_execution_performed_here':False})

assert all(identity(Path(path)) == value for path,value in READS.items())
record('read-inputs-before-after.json', {'schema':1,'files':[{'path':p,**v} for p,v in sorted(READS.items())],
    'all_read_inputs_unchanged':True})
result = {'schema':1,'status':'STATIC_LOOKUP_COMMAND_AND_SIGNED_BINDING_REVIEW_PASSED',
    'completed_utc':datetime.now(timezone.utc).isoformat(),'nineteen_argv_exit_timeout_order_rows_exact':True,
    'shared_provider_unchanged':True,'twenty_one_frozen_payloads_exact':True,'constant_mapping_preserved_byte_for_byte':True,
    'cwd_scope_honestly_source_bound':True,'schema2_finalization_contract_consistent':True,
    'signed_method_contract_consistent':True,'concrete_blocker_found':False,
    'scope':'Independent source/design review only; no full app copy, Java, D8, child producer run, hosted tooling suite or new Android execution.',
    'future_combined_tooling_and_signed_acceptance_pending':True}
record('result.json',result)
shutil.copy2(Path(__file__), OUT / 'executed-review.py')
print(json.dumps(result))
