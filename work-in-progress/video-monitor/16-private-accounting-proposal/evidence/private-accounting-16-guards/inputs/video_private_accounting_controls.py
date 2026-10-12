#!/usr/bin/env python3
"""Exercise private accounting guards without adding app executions or coverage."""
import argparse
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoints', type=Path, required=True)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # The entire compressed guard study is bounded well below this free-space floor.
    free = shutil.disk_usage(HERE).free
    if free < 64*1024*1024:
        raise SystemExit('Guard execution deferred: less than 64 MiB available; no output directory created.')
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'CHECKING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Pure evidence/rule guards plus rejection-before-evidence subprocesses; zero app execution or dynamic coverage credit.',
        'active_policy_changed': False, 'additional_app_executions': 0,
        'additional_original_coverage': 0, 'free_bytes_before': free, 'controls': [], 'subprocess_controls': []}
    program = HERE / 'video_private_accounting.py'; program_sha = sha(program)
    spec = importlib.util.spec_from_file_location('video_private_guard_subject', program)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    try:
        pins = module.load_pins(); payload, proof = module.load_payload(args.checkpoints.resolve(), pins, args.jdk.resolve())
        baseline = module.validate_payload(payload, pins, proof)
        result['baseline'] = baseline; result['validator_sha256'] = program_sha; result['pins_sha256'] = module.PINS_SHA
        inputs = output / 'inputs'; inputs.mkdir()
        for source in [program, HERE / 'private_accounting_pins.json', Path(__file__)]:
            shutil.copyfile(source, inputs / source.name)
        baseline_sha = module.canonical_sha(payload)
        with gzip.open(output / 'positive-payload.json.gz', 'wb') as stream:
            stream.write((json.dumps(payload, indent=2) + '\n').encode())

        def check(name, mutate, reason):
            changed = copy.deepcopy(payload); mutate(changed)
            if module.canonical_sha(changed) == baseline_sha:
                raise RuntimeError('Control did not change its payload: ' + name)
            folder = output / 'controls' / name; folder.mkdir(parents=True)
            with gzip.open(folder / 'payload.json.gz', 'wb') as stream:
                stream.write((json.dumps(changed, indent=2) + '\n').encode())
            row = {'name': name, 'expected_reason': reason, 'app_executions': 0, 'original_coverage_credit': 0,
                'payload_sha256': module.canonical_sha(changed), 'payload_archive_sha256': sha(folder / 'payload.json.gz')}
            try:
                observed = module.validate_payload(changed, pins, proof)
            except ValueError as error:
                row['rejected'] = reason in str(error); row['reason'] = str(error)
            else:
                row['rejected'] = False; row['unexpected_decision'] = observed
            save(folder / 'result.json', row); result['controls'].append(row)
            save(output / 'result.json', result)

        def change_report(p, mutate):
            mutate(p['raw_report']); p['restored_report'] = copy.deepcopy(p['raw_report'])

        def field(key, value):
            return lambda p: change_report(p, lambda r: r.__setitem__(key, value))

        def file_key(suffix):
            return 'three_path/evidence/run/' + suffix

        for name, key in [
            ('original-fixture-binding', file_key('inputs/original-video-monitor.dex')),
            ('helper-source-binding', file_key('inputs/source/java/recovered/ui/VideoMonitorMethods.java')),
            ('oracle-source-binding', file_key('inputs/tests/java/BytecodeOracle.java')),
            ('producer-source-binding', file_key('inputs/tests/java/VideoDexStudy.java')),
            ('origin-launcher-binding', file_key('inputs/tests/java/VideoDexLauncher.java')),
            ('reviewed-collector-binding', 'dataflow/evidence/reports/handler-dataflow-04/VideoHandlerInventory.java'),
            ('reviewed-proof-binding', 'proof/verify_handler_dataflow.py')]:
            if key not in payload['frozen_file_hashes']:
                raise RuntimeError('The specific guard input does not exist: ' + key)
            check(name, lambda p, k=key: p['frozen_file_hashes'].__setitem__(k, '0'*64), 'SOURCE_FIXTURE_PROOF_FILE_BINDING_CHANGED')
        check('proof-checkpoint-binding', lambda p: p['checkpoint_hashes'].__setitem__('proof', '0'*64), 'CHECKPOINT_BINDINGS_CHANGED')
        check('wrong-method-domain', field('methodKeys', ['Lwrong/Type;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;']), 'WRONG_METHOD_DOMAIN')
        check('missing-rebuilt-path', field('paths', 2), 'WRONG_CASE_OR_PATH_SCOPE')
        check('noninteger-case-count', field('cases', 1125.0), 'CASE_OR_PATH_COUNT_TYPE')
        for name, key in [('actual-mismatch', 'failedCases'), ('unsupported-execution', 'unsupportedExecutions'), ('expected-result-failure', 'expectedResultFailures')]:
            check(name, field(key, 1), 'SEMANTIC_FAILURE_OR_UNSUPPORTED_EXECUTION')
        check('hidden-failure-array', field('failures', [{'case': 'hidden'}]), 'HIDDEN_SEMANTIC_FAILURE')
        for name, key in [('raw-pass-relabelling', 'passed'), ('dynamic-coverage-relabelling', 'fullInstructionAndConditionalCoverage'), ('coverage-exemption-flag', 'coverageExemptionImplemented')]:
            check(name, field(key, True), 'RAW_COVERAGE_FAILURE_WAS_RELABELLED')
        check('constructor-adapter-use', field('noConstructorOwnerAdapterUsed', False), 'SEMANTIC_RUNTIME_OR_ADAPTER_PREREQUISITE_FAILED')
        check('runtime-identity-failed', field('liveRuntimeUnchanged', False), 'SEMANTIC_RUNTIME_OR_ADAPTER_PREREQUISITE_FAILED')
        check('invented-android-execution', field('androidRuntime', True), 'SCOPE_WAS_BROADENED')
        check('wrapper-raw-gate-relabelling', lambda p: p['run_result'].__setitem__('raw_original_coverage_gate_passed', True), 'WRAPPER_RAW_STATUS_CHANGED')
        check('actual-rebuilt-control-not-detected', lambda p: p['run_result']['controls'][2].__setitem__('detected', False), 'ACTUAL_CONTROL_DETECTION_FAILED')
        check('restoration-differs', lambda p: p['restored_report'].__setitem__('cases', 1), 'EXACT_POSITIVE_RESTORATION_FAILED')
        check('source-changed-after-run', lambda p: p['run_result'].__setitem__('input_inventory_unchanged', False), 'INPUT_RESTORATION_FAILED')
        check('actual-helper-class-changed', lambda p: p['class_file_hashes'].__setitem__('recovered.ui.VideoMonitorMethods', '0'*64), 'ACTUAL_COMPILED_CLASS_BYTES_CHANGED')
        check('actual-producer-class-changed', lambda p: p['class_file_hashes'].__setitem__('VideoDexStudy', '0'*64), 'ACTUAL_COMPILED_CLASS_BYTES_CHANGED')
        check('observed-class-origin-changed', lambda p: p['class_origins']['classes'][0].__setitem__('sha256', '0'*64), 'OBSERVED_CLASS_ORIGIN_CHANGED')
        check('original-substituted-as-rebuilt', lambda p: p['method_binding'].__setitem__('rebuilt_dex_sha256', '940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254'), 'EXACT_BODY_OR_PIPELINE_BINDING_CHANGED')

        def runtime_change(p, mutate):
            for key in ['runtime_before', 'runtime_after']:
                mutate(p[key])
            change_report(p, lambda r: r.__setitem__('liveRuntime', copy.deepcopy(p['runtime_before'])))

        check('unexpected-vm-options', lambda p: runtime_change(p, lambda r: r['jvmArguments'].append('-XX:+OmitStackTraceInFastThrow')), 'ACTUAL_EXECUTING_RUNTIME_CHANGED')
        check('wrong-live-boot-loader', lambda p: runtime_change(p, lambda r: r['classes'][0].__setitem__('bootstrapLoader', False)), 'ACTUAL_EXECUTING_RUNTIME_CHANGED')

        def rehash_jrt(p):
            runtime_change(p, lambda r: r['classes'][0].__setitem__('sha256', '0'*64))
            for phase in ['before', 'after']:
                p['runtime_actual_file_hashes'][phase]['StringBuilder.class'] = '0'*64
        check('changed-jrt-rehashed-rows', rehash_jrt, 'ACTUAL_EXECUTING_RUNTIME_CHANGED')

        def rehash_release(p):
            runtime_change(p, lambda r: r.__setitem__('releaseSha256', '0'*64))
            for phase in ['before', 'after']:
                p['runtime_actual_file_hashes'][phase]['release'] = '0'*64
        check('changed-release-rehashed-rows', rehash_release, 'ACTUAL_EXECUTING_RUNTIME_CHANGED')
        check('live-jrt-bytes-disagree-with-rows', lambda p: p['runtime_actual_file_hashes']['after'].__setitem__('Object.class', '0'*64), 'ACTUAL_JRT_BYTES_OR_RELEASE_CHANGED')
        check('current-java-executable-changed', lambda p: p['current_jdk_inputs'][0].__setitem__('sha256', '0'*64), 'ACTUAL_JAVA_EXECUTABLE_MODULE_OR_RELEASE_CHANGED')
        check('recorded-module-image-changed', lambda p: p['run_result']['jdk_inputs'][-1].__setitem__('sha256', '0'*64), 'ACTUAL_JAVA_EXECUTABLE_MODULE_OR_RELEASE_CHANGED')

        def instruction(p, offset):
            return next(row for row in p['original_inventory']['instructions'] if row['offset'] == offset)
        check('protected-divisor-becomes-zero', lambda p: instruction(p, 129).__setitem__('literal', 0), 'Instruction operands changed at 129')
        check('extra-protected-constructor-call', lambda p: instruction(p, 134).update(opcode='INVOKE_DIRECT', invokeRegisters=[0], reference='Ljava/lang/StringBuilder;-><init>()V'), 'Additional protected call')
        check('ordinary-entry-to-handler', lambda p: instruction(p, 231).__setitem__('target', 232), 'Ordinary entry into handler chain')
        check('extended-protected-interval', lambda p: p['original_inventory']['exceptionRegions'][2].__setitem__('end', 163), 'Exact Exception-only protected interval changed')
        check('extra-constructor-throw-retains-old-substrings', lambda p: p['constructor_disassemblies'].__setitem__('StringBuilder', p['constructor_disassemblies']['StringBuilder'].replace('       6: return\n', '       6: new           #999 // class java/lang/RuntimeException\n       9: athrow\n      10: return\n', 1)), 'Complete pinned constructor disassembly changed')
        check('changed-rebuilt-handler-operands', lambda p: p['rebuilt_inventory']['instructions'][-1].__setitem__('A', 31), 'COMPLETE_REBUILT_INVENTORY_CHANGED')

        def visited_change(p, operation):
            def mutate(r):
                operation(r['originalExecutedOffsets']); r['originalExecutedOffsets'].sort()
                covered = set(r['originalExecutedOffsets']); all_offsets = {row['offset'] for row in p['original_inventory']['instructions']}
                r['instructionCoverage']['visited'] = len(covered); r['instructionCoverage']['unvisitedOffsets'] = sorted(all_offsets-covered)
            change_report(p, mutate)
        check('missing-real-original-offset', lambda p: visited_change(p, lambda rows: rows.remove(0)), 'ORIGINAL_PARTITION_IS_INCOMPLETE')
        check('fabricated-original-offset', lambda p: visited_change(p, lambda rows: rows.append(99999)), 'original_FABRICATED_OFFSET')
        check('dynamic-static-overlap', lambda p: visited_change(p, lambda rows: rows.append(232)), 'DYNAMIC_AND_STATIC_PARTITIONS_OVERLAP')
        check('duplicate-visited-offset', lambda p: visited_change(p, lambda rows: rows.append(0)), 'original_VISITED_DUPLICATE_OR_UNORDERED')
        check('missing-original-edge', lambda p: change_report(p, lambda r: r['originalExecutedConditionalEdges'].pop()), 'original_MISSING_OR_FABRICATED_EDGE')
        check('fabricated-original-edge', lambda p: change_report(p, lambda r: r.__setitem__('originalExecutedConditionalEdges', sorted(r['originalExecutedConditionalEdges'] + ['99999:0']))), 'original_MISSING_OR_FABRICATED_EDGE')
        check('aggregate-disagrees-with-visited-set', lambda p: change_report(p, lambda r: r['instructionCoverage'].__setitem__('visited', 260)), 'original_AGGREGATE_DISAGREES_WITH_ACTUAL_SETS')
        check('noninteger-coverage-count', lambda p: change_report(p, lambda r: r['instructionCoverage'].__setitem__('visited', 259.0)), 'original_COUNT_TYPE')
        check('rebuilt-retry-edge-missing', lambda p: change_report(p, lambda r: r['rebuiltExecutedConditionalEdges'].remove('81:88')), 'rebuilt_MISSING_OR_FABRICATED_EDGE')

        # Real file/control subprocesses must stop at an independent identity guard.
        def subprocess_control(name, rewrite):
            folder = output / 'subprocess-controls' / name; folder.mkdir(parents=True)
            own_program = folder / program.name; shutil.copyfile(program, own_program)
            own_pins = folder / 'private_accounting_pins.json'; shutil.copyfile(HERE / own_pins.name, own_pins)
            checkpoints, expected = rewrite(folder, own_pins)
            argv = [sys.executable, '-B', str(own_program), '--checkpoints', str(checkpoints), '--jdk', str(args.jdk.resolve()), '--output', str(folder / 'verification')]
            started = time.monotonic(); out, err = folder / 'stdout.txt', folder / 'stderr.txt'
            with out.open('xb') as stdout, err.open('xb') as stderr:
                completed = subprocess.run(argv, stdout=stdout, stderr=stderr, timeout=120)
            observed = json.loads((folder / 'verification/result.json').read_text())
            row = {'name': name, 'argv': argv, 'returncode': completed.returncode, 'timeout_seconds': 120,
                'seconds': round(time.monotonic()-started, 6), 'stdout_sha256': sha(out), 'stderr_sha256': sha(err),
                'expected_reason': expected, 'actual_reason': observed.get('error'),
                'rejected': completed.returncode == 1 and observed['status'] == 'PRIVATE_PROPOSAL_REJECTED' and expected in observed.get('error', ''),
                'app_executions': 0, 'original_coverage_credit': 0, 'stopped_before_capsule_payload_traversal': True}
            save(folder / 'control-result.json', row); result['subprocess_controls'].append(row)

        def wrong_pins(folder, pin_path):
            changed = json.loads(pin_path.read_text()); changed['original_static_offsets'].append(236); save(pin_path, changed)
            return args.checkpoints.resolve(), 'INDEPENDENT_REVIEW_PINS_CHANGED'
        subprocess_control('unreviewed-static-offset-pin-file', wrong_pins)

        for label, relative in [('rehashed-original-fixture', 'evidence/run/inputs/original-video-monitor.dex'),
                ('rehashed-live-builder-bytes', 'evidence/run/positive/live-runtime/before/StringBuilder.class'),
                ('rehashed-producer-source', 'evidence/run/inputs/tests/java/VideoDexStudy.java')]:
            def rewrite(folder, pin_path, relative=relative):
                base = args.checkpoints.resolve() / pins['checkpoints']['three_path']['directory']
                target = folder / 'changed-checkpoints' / base.name; target.mkdir(parents=True)
                manifest = json.loads((base / 'checkpoint.json').read_text())
                changed = (base / relative).read_bytes() + b'\x00'
                path = target / relative; path.parent.mkdir(parents=True); path.write_bytes(changed)
                row = next(row for row in manifest['evidence_files'] if 'evidence/' + row['path'] == relative)
                row['bytes'] = len(changed); row['sha256'] = hashlib.sha256(changed).hexdigest()
                save(target / 'checkpoint.json', manifest)
                save(folder / 'mutation.json', {'scope': 'Only the changed file and rehashed manifest are needed: this control must fail at the independent manifest identity before reading any remaining payload.',
                    'changed_file': relative, 'changed_sha256': row['sha256'], 'rehashed_manifest_sha256': sha(target / 'checkpoint.json')})
                return target.parent, 'CHECKPOINT_IDENTITY_CHANGED'
            subprocess_control(label, rewrite)

        restored = module.validate_payload(payload, pins, proof)
        result['exact_positive_restoration'] = restored == baseline and module.canonical_sha(payload) == baseline_sha
        result['source_and_pins_unchanged'] = sha(program) == program_sha and sha(HERE / 'private_accounting_pins.json') == module.PINS_SHA
        result['controls_count'] = len(result['controls']); result['subprocess_controls_count'] = len(result['subprocess_controls'])
        result['all_rejected'] = all(row['rejected'] for row in result['controls'] + result['subprocess_controls'])
        result['passed'] = result['all_rejected'] and result['exact_positive_restoration'] and result['source_and_pins_unchanged']
        result['status'] = 'PRIVATE_ACCOUNTING_GUARDS_PASSED_EXACT_POSITIVE_RESTORED' if result['passed'] else 'PRIVATE_ACCOUNTING_GUARD_FAILURE'
        if not result['passed']:
            return 2
        return 0
    except Exception as error:
        result['status'] = 'PRIVATE_ACCOUNTING_CONTROL_STUDY_FAILED'; result['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc()); raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', result)
        print(json.dumps({key: value for key, value in result.items() if key not in ['controls', 'subprocess_controls']}, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
