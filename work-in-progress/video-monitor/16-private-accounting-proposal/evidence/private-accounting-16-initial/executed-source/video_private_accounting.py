#!/usr/bin/env python3
"""Review-only accounting for one sealed, already executed video study.

This is deliberately not an active/fresh-run acceptance gate. It accepts exactly
the five reviewed input capsules and retains the historical raw coverage failure.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
import traceback
import types

HERE = Path(__file__).resolve().parent
PINS_SHA = '21ecda6da3a5791cd444e76821b5361ce5e7b458b74a500b00c30da73688ecdf'
VERIFIER_SHA = 'da31172a98316ca192e95720ba9eeb3d2070b729c08b1cff4743ddc5a67f69a5'
ORIGINAL_INVENTORY_SHA = 'c0904c171e0d76e9cc502ef344f34fd58b7d490344d6f7c81b335cbdc2eaa942'
REBUILT_INVENTORY_SHA = '2c8d64e83dd813cc3fbbb249b190aa55903370070d7a1a71c1e9294e75100486'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def canonical_sha(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def read_json(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, 'DUPLICATE_JSON_KEY: ' + key)
            out[key] = value
        return out
    return json.loads(path.read_text(), object_pairs_hook=unique)


def load_pins():
    path = HERE / 'private_accounting_pins.json'
    require(not path.is_symlink() and sha(path) == PINS_SHA, 'INDEPENDENT_REVIEW_PINS_CHANGED')
    value = read_json(path)
    require(value['schema'] == 'closed-video-accounting-proposal-1', 'WRONG_PIN_SCHEMA')
    return value


def safe_relative(text):
    path = PurePosixPath(text)
    require(not path.is_absolute() and bool(path.parts) and '..' not in path.parts and
            chr(92) not in text and path.as_posix() == text, 'UNSAFE_CAPSULE_PATH')
    return path


def seal(root, expected_sha):
    require(root.is_dir() and not root.is_symlink(), 'CAPSULE_DIRECTORY_REQUIRED')
    manifest = root / 'checkpoint.json'
    require(not manifest.is_symlink() and sha(manifest) == expected_sha, 'CHECKPOINT_IDENTITY_CHANGED')
    value = read_json(manifest); files = {}; allowed = {'checkpoint.json'}
    for category, prefix in [('files', ''), ('evidence_files', 'evidence/')]:
        for row in value[category]:
            relative = prefix + safe_relative(row['path']).as_posix()
            require(relative not in allowed, 'DUPLICATE_CAPSULE_FILE')
            allowed.add(relative); path = root / relative
            require(path.is_file() and not path.is_symlink(), 'REGULAR_CAPSULE_FILE_REQUIRED')
            require(type(row['bytes']) is int and path.stat().st_size == row['bytes'] and
                    sha(path) == row['sha256'], 'CAPSULE_FILE_IDENTITY_CHANGED: ' + relative)
            files[relative] = row['sha256']
    actual = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'CAPSULE_SYMLINK_REFUSED')
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    require(actual == allowed, 'EXTRA_OR_MISSING_CAPSULE_FILE')
    return value, files


def archive_hashes(path):
    result = {}
    with tarfile.open(path, 'r:gz') as stream:
        for member in stream:
            safe_relative(member.name.rstrip('/'))
            require(member.isdir() or member.isfile(), 'NONREGULAR_COMPILED_ARCHIVE_MEMBER')
            if member.isfile():
                require(member.name not in result, 'DUPLICATE_COMPILED_ARCHIVE_MEMBER')
                data = stream.extractfile(member).read()
                require(len(data) == member.size, 'SHORT_COMPILED_ARCHIVE_MEMBER')
                result[member.name] = {'bytes': len(data), 'sha256': digest(data)}
    return result


def load_proof(path):
    data = path.read_bytes()
    require(digest(data) == VERIFIER_SHA, 'REVIEWED_PROOF_CODE_CHANGED')
    module = types.ModuleType('reviewed_video_handler_proof')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


def load_payload(checkpoints, pins, jdk):
    roots = {}; actual_hashes = {}; sealed_hashes = {}
    for key, spec in pins['checkpoints'].items():
        root = checkpoints / spec['directory']
        _, files = seal(root, spec['sha256']); roots[key] = root; sealed_hashes[key] = sha(root / 'checkpoint.json')
        actual_hashes.update({key + '/' + relative: value for relative, value in files.items()})
    require(actual_hashes == pins['all_frozen_file_hashes'], 'INDEPENDENT_FROZEN_FILE_BINDINGS_CHANGED')
    run = roots['three_path'] / 'evidence/run'
    evidence = roots['dataflow'] / 'evidence/reports/handler-dataflow-04'
    proof = load_proof(roots['proof'] / 'verify_handler_dataflow.py')
    result = read_json(run / 'result.json')
    archives = {'fixed-host': archive_hashes(run / 'inputs/fixed-host-classes.tar.gz'),
                'fixed-harness': archive_hashes(run / 'inputs/fixed-harness-classes.tar.gz')}
    fixed_inventory = read_json(run / 'fixed-class-inventory.json')
    for name, family in [('host', 'fixed-host'), ('harness', 'fixed-harness')]:
        actual = [{'path': path, **row} for path, row in sorted(archives[family].items())]
        require(actual == fixed_inventory[name], 'FIXED_CLASS_ARCHIVE_INVENTORY_CHANGED')
    expected_classes = read_json(run / 'expected-class-origins.json')
    class_hashes = {}
    for row in expected_classes:
        relative = Path(row['path']).relative_to(result['private_work'])
        if relative.parts[0] in archives:
            actual = archives[relative.parts[0]][Path(*relative.parts[1:]).as_posix()]['sha256']
        else:
            require(relative.parts[0] == 'launcherclasses', 'UNEXPECTED_LOADED_CLASS_DIRECTORY')
            actual = sha(run / relative)
        require(row['class'] not in class_hashes, 'DUPLICATE_LOADED_CLASS')
        class_hashes[row['class']] = actual
    runtime_hashes = {}
    for phase in ['before', 'after']:
        folder = run / 'positive/live-runtime' / phase
        runtime_hashes[phase] = {path.name: sha(path) for path in folder.iterdir() if path.is_file() and path.name != 'runtime.json'}
    current_jdk = []
    for row in pins['jdk_inputs']:
        relative = Path(row['path']).relative_to(pins['runtime']['java.home'])
        path = jdk / relative
        require(path.is_file() and not path.is_symlink(), 'REGULAR_BOUND_JDK_INPUT_REQUIRED')
        current_jdk.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    payload = {'checkpoint_hashes': sealed_hashes, 'frozen_file_hashes': actual_hashes,
        'run_result': result, 'raw_report': read_json(run / 'positive/parity.json'),
        'restored_report': read_json(run / 'positive-restored/parity.json'),
        'method_binding': read_json(run / 'method-body-binding.json'),
        'class_origins': read_json(run / 'positive/class-origins.json'), 'expected_classes': expected_classes,
        'class_file_hashes': class_hashes,
        'runtime_before': read_json(run / 'positive/live-runtime/before/runtime.json'),
        'runtime_after': read_json(run / 'positive/live-runtime/after/runtime.json'),
        'runtime_actual_file_hashes': runtime_hashes, 'current_jdk_inputs': current_jdk,
        'original_inventory': read_json(evidence / 'original-instructions.json'),
        'rebuilt_inventory': read_json(roots['three_path'] / 'evidence/rebuilt-handler-inventory/original-instructions.json'),
        'constructor_disassemblies': {name: (evidence / ('javap-' + name + '.stdout.txt')).read_text() for name in proof.JAVAP_HASHES}}
    return payload, proof


def exact_set(values, kind, label):
    require(isinstance(values, list) and all(type(value) is kind for value in values), label + '_TYPE')
    require(values == sorted(set(values)), label + '_DUPLICATE_OR_UNORDERED')
    return set(values)


def check_coverage(report, inventory, body):
    prefix = 'original' if body == 'original' else 'rebuilt'
    coverage_key = 'instructionCoverage' if body == 'original' else 'rebuiltInstructionCoverage'
    offsets = {row['offset'] for row in inventory['instructions']}
    visited = exact_set(report[prefix + 'ExecutedOffsets'], int, prefix + '_VISITED')
    require(visited <= offsets, prefix + '_FABRICATED_OFFSET')
    edges = set()
    for row in inventory['instructions']:
        if row['opcode'].startswith('IF_'):
            edges.update([str(row['offset']) + ':' + str(row['offset'] + row['units']), str(row['offset']) + ':' + str(row['target'])])
    actual_edges = exact_set(report[prefix + 'ExecutedConditionalEdges'], str, prefix + '_EDGES')
    require(actual_edges == edges, prefix + '_MISSING_OR_FABRICATED_EDGE')
    coverage = {'instructions': len(offsets), 'visited': len(visited), 'unvisitedOffsets': sorted(offsets-visited),
        'conditionalEdges': len(edges), 'conditionalEdgesVisited': len(edges), 'unvisitedConditionalEdges': []}
    require(report[coverage_key] == coverage, prefix + '_AGGREGATE_DISAGREES_WITH_ACTUAL_SETS')
    return offsets, visited, coverage


def validate_payload(payload, pins, proof):
    require(payload['checkpoint_hashes'] == {key: value['sha256'] for key, value in pins['checkpoints'].items()}, 'CHECKPOINT_BINDINGS_CHANGED')
    require(payload['frozen_file_hashes'] == pins['all_frozen_file_hashes'], 'SOURCE_FIXTURE_PROOF_FILE_BINDING_CHANGED')
    structural = proof.structural_facts(payload['original_inventory'])
    proof.constructor_facts(payload['constructor_disassemblies'])
    require(canonical_sha(payload['original_inventory']) == ORIGINAL_INVENTORY_SHA, 'COMPLETE_ORIGINAL_INVENTORY_CHANGED')
    require(canonical_sha(payload['rebuilt_inventory']) == REBUILT_INVENTORY_SHA, 'COMPLETE_REBUILT_INVENTORY_CHANGED')
    require(payload['method_binding'] == pins['method_binding'], 'EXACT_BODY_OR_PIPELINE_BINDING_CHANGED')
    report, run = payload['raw_report'], payload['run_result']
    require(report['methodKeys'] == [pins['method']] and report['methodsCovered'] == 1 and run['method'] == pins['method'], 'WRONG_METHOD_DOMAIN')
    require(report['cases'] == 1125 and report['paths'] == 3 and report['independentExpectedResultChecks'] == 237, 'WRONG_CASE_OR_PATH_SCOPE')
    require(all(type(report[key]) is int and report[key] == 0 for key in ['failedCases', 'unsupportedExecutions', 'expectedResultFailures']), 'SEMANTIC_FAILURE_OR_UNSUPPORTED_EXECUTION')
    require(report['failures'] == [] and report['failedCaseLabels'] == [], 'HIDDEN_SEMANTIC_FAILURE')
    require(report['passed'] is False and report['fullInstructionAndConditionalCoverage'] is False and report['coverageExemptionImplemented'] is False, 'RAW_COVERAGE_FAILURE_WAS_RELABELLED')
    require(report['semanticMatch'] is True and report['noConstructorOwnerAdapterUsed'] is True and report['liveRuntimeUnchanged'] is True, 'SEMANTIC_RUNTIME_OR_ADAPTER_PREREQUISITE_FAILED')
    require(report['androidRuntime'] is False and report['registeredInActiveProject'] is False and report['signedApkBuilt'] is False and report['rebuiltDexCompared'] is True, 'SCOPE_WAS_BROADENED')
    require(run['status'] == 'THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED' and run['passed'] is False and run['raw_original_coverage_gate_passed'] is False, 'WRAPPER_RAW_STATUS_CHANGED')
    require(run['positive_semantic_match'] is True and run['all_controls_passed'] is True and run['method_only_semantic_and_control_study_complete'] is True, 'ACTUAL_COMPILED_PROOF_INCOMPLETE')
    require([row['name'] for row in run['controls']] == ['original-substituted-for-rebuilt', 'wrong-loaded-helper-hash', 'rebuilt-delay-duration'], 'ACTUAL_CONTROL_SET_CHANGED')
    require(all(row['rejected_before_parity'] is True for row in run['controls'][:2]) and run['controls'][2]['detected'] is True and run['controls'][2]['failed_cases'] == 30, 'ACTUAL_CONTROL_DETECTION_FAILED')
    require(payload['restored_report'] == report and all(value is True for key, value in run['positive_restoration'].items() if key != 'returncode') and run['positive_restoration']['returncode'] == 2, 'EXACT_POSITIVE_RESTORATION_FAILED')
    for key in ['fixed_class_inventory_unchanged', 'input_inventory_unchanged', 'frozen_baseline_unchanged', 'frozen_host_checkpoint_unchanged', 'jdk_inputs_unchanged', 'tool_jar_unchanged']:
        require(run[key] is True, 'INPUT_RESTORATION_FAILED: ' + key)
    require(payload['class_origins'] == pins['class_origins'], 'OBSERVED_CLASS_ORIGIN_CHANGED')
    expected_classes = [{key: value for key, value in row.items() if key != 'verified'} for row in pins['class_origins']['classes']]
    require(payload['expected_classes'] == expected_classes, 'EXPECTED_CLASS_ORIGIN_CHANGED')
    require(payload['class_file_hashes'] == {row['class']: row['sha256'] for row in pins['class_origins']['classes']}, 'ACTUAL_COMPILED_CLASS_BYTES_CHANGED')
    runtime = pins['runtime']
    require(payload['runtime_before'] == runtime and payload['runtime_after'] == runtime and report['liveRuntime'] == runtime, 'ACTUAL_EXECUTING_RUNTIME_CHANGED')
    require(runtime['jvmArguments'] == ['-XX:-OmitStackTraceInFastThrow', '-Xmx512m'], 'UNREVIEWED_JVM_OPTIONS')
    expected_runtime_hashes = {row['file']: row['sha256'] for row in runtime['classes']}
    expected_runtime_hashes['release'] = runtime['releaseSha256']
    require(payload['runtime_actual_file_hashes'] == {'before': expected_runtime_hashes, 'after': expected_runtime_hashes}, 'ACTUAL_JRT_BYTES_OR_RELEASE_CHANGED')
    require(payload['current_jdk_inputs'] == pins['jdk_inputs'] and run['jdk_inputs'] == pins['jdk_inputs'], 'ACTUAL_JAVA_EXECUTABLE_MODULE_OR_RELEASE_CHANGED')
    require(proof.RELEASE_SHA == runtime['releaseSha256'] and {row['class'].split('.')[-1]: row['sha256'] for row in runtime['classes']} == proof.JRT_HASHES, 'EXECUTING_JRT_DOES_NOT_MATCH_REVIEWED_CONSTRUCTOR_PROOF')
    for row in runtime['classes']:
        require(row['bootstrapLoader'] is True and row['module'] == 'java.base' and row['resource'] == 'jrt:/java.base/java/lang/' + row['file'], 'WRONG_LIVE_BOOT_CLASS_ORIGIN')
    offsets, visited, original = check_coverage(report, payload['original_inventory'], 'original')
    static = {232, 233, 235}
    require(pins['original_static_offsets'] == [232, 233, 235] and structural['handler_chain'] == [232, 233, 235], 'UNREVIEWED_STATIC_OFFSET_LIST')
    require(not visited & static, 'DYNAMIC_AND_STATIC_PARTITIONS_OVERLAP')
    require(visited | static == offsets and len(visited) == 259 and len(offsets) == 262, 'ORIGINAL_PARTITION_IS_INCOMPLETE')
    _, _, rebuilt = check_coverage(report, payload['rebuilt_inventory'], 'rebuilt')
    require(rebuilt['unvisitedOffsets'] == [235, 236] and rebuilt['visited'] == 288 and rebuilt['instructions'] == 290, 'REBUILT_RAW_COVERAGE_SCOPE_CHANGED')
    return {'status': 'PRIVATE_EXACT_ORIGINAL_ACCOUNTING_PROPOSAL_SATISFIED',
        'scope': 'Sealed already-executed study14 only; independent review is required before any active/fresh-run policy integration.',
        'proposed_accounting_satisfied': True, 'active_policy_changed': False,
        'raw_original_coverage_gate_passed': False, 'raw_report_passed': False,
        'method': pins['method'], 'cases': 1125, 'paths': 3, 'independent_expected_checks': 237,
        'original_instructions_dynamically_visited': 259, 'original_instructions_statically_infeasible': 3,
        'original_instruction_total': 262, 'original_static_offsets': [232, 233, 235],
        'original_dynamic_and_static_sets_disjoint': True, 'original_conditional_edges_dynamically_visited': 46,
        'original_conditional_edges_total': 46, 'rebuilt_raw_coverage': rebuilt,
        'rebuilt_static_accounting_applied': False, 'additional_app_executions': 0,
        'additional_dynamic_instruction_coverage': 0, 'android_executed': False, 'signed_apk_built': False,
        'assumptions': ['Exact reviewed normally linked synchronous host/JRT bytes.',
            'No asynchronous exception injection, boot-class replacement, instrumentation or external state corruption.',
            'No Android boot-library equivalence or execution claim for this video body.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoints', type=Path, required=True)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); output = args.output.resolve(); output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'CHECKING_PRIVATE_PROPOSAL', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'active_policy_changed': False, 'additional_app_executions': 0}
    try:
        pins = load_pins(); payload, proof = load_payload(args.checkpoints.resolve(), pins, args.jdk.resolve())
        result.update(validate_payload(payload, pins, proof))
        result['pins_sha256'] = PINS_SHA; result['validator_sha256'] = sha(Path(__file__))
        result['checkpoint_hashes'] = payload['checkpoint_hashes']
        result['bound_frozen_files'] = len(payload['frozen_file_hashes'])
        result['payload_canonical_sha256'] = canonical_sha(payload)
        import gzip
        with gzip.open(output / 'sealed-input-payload.json.gz', 'wb') as stream:
            stream.write((json.dumps(payload, indent=2) + '\n').encode())
        result['sealed_payload_archive_sha256'] = sha(output / 'sealed-input-payload.json.gz')
    except Exception as error:
        result['status'] = 'PRIVATE_PROPOSAL_REJECTED'; result['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
