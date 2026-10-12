#!/usr/bin/env python3
"""Read the one exact hosted ZIP; preserve compact independent binding evidence.

No APK extraction/build, Java/Android execution, or live-host stat claim occurs.
The unchanged production clock/argv predicates consume the original serialized
stat table through an explicit ZIP adapter. Byte identity is independently read
from each archive member; extracted file metadata is never substituted.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import types
import zipfile
import zlib

ZIP = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-run-38238858564/artifact.zip')
ZIP_SHA = 'a7b52e6096db27cf9854671fcd3f6d1b7c3f73f5cf0255fcb9fc6fdc5afc117c'
ROOT = Path(__file__).resolve().parent
FROZEN = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
SOURCE = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
PROJECT = 'numeric-workspace/MacroDroid_v9/'
sys.path.insert(0, str(FROZEN / 'source/tools/day_numeric_acceptance'))
import inputs
import verify as production


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def file_identity(path):
    with path.open('rb') as stream:
        return {'bytes': path.stat().st_size, 'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def save(name, value):
    target = ROOT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(json.dumps(value, indent=2).encode() + b'\n')


def copy_member(archive, name, target_name):
    raw = archive.read(name)
    path = ROOT / target_name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target:
        target.write(raw)
    return {'source_member': name, 'retained': target_name, **identity(raw)}


class RecordedZipArtifacts:
    """An explicitly archived-stat adapter, never a live filesystem replacement."""
    def __init__(self, archive, prefix, original_root, declared, start, end):
        self.archive, self.prefix, self.root = archive, prefix, Path(original_root)
        self.declared = {row['path']: row for row in declared}
        require(len(self.declared) == len(declared), 'Duplicate original stat role')
        self.rows, self.physical = {}, {}
        self.started_ns, self.ended_ns = start, end

    def bind(self, name):
        inputs.relative(name)
        row = self.declared[name]
        mode = {key: row[key] for key in ('device', 'inode', 'mode', 'links', 'bytes', 'mtime_ns', 'ctime_ns')}
        production.checked_stat(mode, 'archived:' + name)
        require(self.started_ns <= row['mtime_ns'] <= self.ended_ns
                and self.started_ns <= row['ctime_ns'] <= self.ended_ns, 'Recorded artifact outside host interval: ' + name)
        physical = (row['device'], row['inode'])
        require(physical not in self.physical or self.physical[physical] == name, 'Recorded host inode has multiple roles')
        with self.archive.open(self.prefix + name) as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        require(digest == row['sha256'] and self.archive.getinfo(self.prefix + name).file_size == row['bytes'],
                'Archived bytes differ from host-verified table: ' + name)
        self.rows[name], self.physical[physical] = row, name
        return row

    def hash(self, name, wanted):
        require(self.bind(name)['sha256'] == wanted, 'Recorded result hash differs: ' + name)

    def raw(self, name):
        self.bind(name)
        return self.archive.read(self.prefix + name)

    def json(self, name):
        return json.loads(self.raw(name))


def fixture_methods(raw):
    """Read encoded declarations directly from the actual selected original DEX."""
    require(raw[:4] == b'dex\n' and struct.unpack_from('<I', raw, 32)[0] == len(raw), 'Invalid fixture DEX header')
    require(hashlib.sha1(raw[32:]).digest() == raw[12:32]
            and zlib.adler32(raw[12:]) & 0xffffffff == struct.unpack_from('<I', raw, 8)[0], 'Fixture DEX checksum differs')
    def uleb(offset):
        value, shift = 0, 0
        while True:
            byte = raw[offset]; offset += 1
            value |= (byte & 127) << shift
            if not byte & 128:
                return value, offset
            shift += 7
            require(shift <= 28, 'Unbounded fixture ULEB128')
    string_count, strings_at, type_count, types_at, proto_count, protos_at = struct.unpack_from('<6I', raw, 56)
    strings = []
    for index in range(string_count):
        pointer = struct.unpack_from('<I', raw, strings_at + index * 4)[0]
        utf16_length, pointer = uleb(pointer)
        stop = raw.index(b'\0', pointer)
        strings.append((raw[pointer:stop], utf16_length))
    def ascii_role(index):
        # Only descriptor and method-name roles are decoded. Unrelated DEX
        # literals remain raw MUTF-8 bytes covered by the complete DEX hash.
        encoded, utf16_length = strings[index]
        decoded = encoded.decode('ascii')
        require(len(encoded) == utf16_length, 'ASCII DEX role length differs')
        return decoded
    types_ = [ascii_role(struct.unpack_from('<I', raw, types_at + index * 4)[0]) for index in range(type_count)]
    protos = []
    for index in range(proto_count):
        _, result, arguments = struct.unpack_from('<3I', raw, protos_at + index * 12)
        parameters = []
        if arguments:
            count = struct.unpack_from('<I', raw, arguments)[0]
            parameters = [types_[struct.unpack_from('<H', raw, arguments + 4 + i * 2)[0]] for i in range(count)]
        protos.append('(' + ''.join(parameters) + ')' + types_[result])
    method_count, methods_at, class_count, classes_at = struct.unpack_from('<4I', raw, 88)
    method_ids = []
    for index in range(method_count):
        owner, proto, name = struct.unpack_from('<HHI', raw, methods_at + index * 8)
        method_ids.append(types_[owner] + '->' + ascii_role(name) + protos[proto])
    declared, classes = [], []
    for index in range(class_count):
        fields = struct.unpack_from('<8I', raw, classes_at + index * 32)
        classes.append(types_[fields[0]])
        offset = fields[6]
        if not offset:
            continue
        counts = []
        for _ in range(4):
            value, offset = uleb(offset); counts.append(value)
        for _ in range(counts[0] + counts[1]):
            _, offset = uleb(offset); _, offset = uleb(offset)
        for count in counts[2:]:
            current = 0
            for _ in range(count):
                delta, offset = uleb(offset); current += delta
                _, offset = uleb(offset); code, offset = uleb(offset)
                declared.append({'key': method_ids[current], 'has_code': code != 0})
    return {'classes': classes, 'methods': declared}


def selected_numeric_validators(source):
    """Execute only exact, source-bound pure validation definitions; no producer imports."""
    tree = ast.parse(source)
    functions = {'require', 'require_counts', 'same_inputs', 'validate_report_identity',
                 'validate_positive_coverage', 'validate_observations', 'validate_positive', 'validate_fault'}
    assignments = {'METHOD', 'GETTERS', 'JAVA_FAILURE_COUNTS'}
    selected = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in functions:
            selected.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in assignments for target in node.targets):
            selected.append(node)
    catalog = types.SimpleNamespace(DAY_METHOD=production.NUMERIC_METHOD,
        DAY_INPUT_INVENTORY_SHA256='e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79')
    namespace = {'catalog': catalog, 'json': json, 'hashlib': hashlib}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<exact-selected-pure-numeric-validators>', 'exec'), namespace)
    require(functions.issubset(namespace), 'Missing selected pure validator')
    return namespace, [{'name': node.name if isinstance(node, ast.FunctionDef) else node.targets[0].id,
                        **identity(ast.get_source_segment(source, node).encode())} for node in selected]


def main():
    result = {'status': 'INCOMPLETE', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'run_id': 38238858564, 'job_id': 114776169911, 'head': '3d91187924af10457366ede7a1a8f10d3a1a6ac4',
              'android_executed_by_review': False, 'java_or_build_executed_by_review': False,
              'live_host_stat_recreated_from_archive': False, 'apk_extracted': False}
    try:
        require(file_identity(ZIP) == {'bytes': 222144520, 'sha256': ZIP_SHA}, 'Whole raw container differs')
        with zipfile.ZipFile(ZIP) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)) == 3308, 'Archive member inventory differs')
            inventory = []
            for item in archive.infolist():
                name = PurePosixPath(item.filename)
                require(not name.is_absolute() and '..' not in name.parts and name.as_posix() == item.filename
                        and not item.is_dir(), 'Unexpected or unsafe archive member')
                with archive.open(item) as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                inventory.append({'path': item.filename, 'bytes': item.file_size, 'sha256': digest,
                                  'zip_crc32': f'{item.CRC:08x}', 'compressed_bytes': item.compress_size})
            save('complete-archive-members.json', inventory)
            by_name = {row['path']: row for row in inventory}
            document = lambda name: json.loads(archive.read(name))
            pins = document('hosted-proof/inputs/pins.json')
            prepared = document('hosted-proof/preparation.json')
            execution = document('hosted-proof/execution.json')
            final = document('hosted-proof/verification.json')
            latest = document(PROJECT + 'reports/acceptance-latest.json')
            require(final['status'] == 'ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED' and final['passed'] is True,
                    'Actual final verifier is not complete')
            for field in ('active_promoted', 'android_runtime_executed', 'full_runtime_1_to_1_established', 'complete_high_level_java_kotlin_source'):
                require(final[field] is False, 'Actual scope overclaim')
            source_rows = []
            for name in [n for n in names if n.startswith('job-source/')]:
                relative = name.removeprefix('job-source/')
                actual = identity(archive.read(name))
                require(actual == file_identity(FROZEN / 'source' / relative), 'Executed job source differs from reviewed nine-path package')
                source_rows.append({'path': relative, **actual})
            require(len(source_rows) == 9, 'Actual job-source inventory differs')
            require(identity(archive.read('hosted-proof/inputs/pins.json')) == file_identity(FROZEN / 'source/tools/day_numeric_acceptance/pins.json'), 'Executed pins differ')
            require(identity(archive.read('hosted-proof/inputs/source-checkpoint.json')) == file_identity(SOURCE / 'checkpoint.json'), 'Source08 checkpoint differs')
            base = document('hosted-proof/inputs/baseline-input-snapshot.json')
            future = document('hosted-proof/inputs/future-input-snapshot.json')
            changes = document('hosted-proof/inputs/source-changes.json')
            require(len(changes) == 19 and changes == pins['source_changes'], 'Exact nineteen source roles differ')
            derived = inputs.derive(base, changes)
            require(derived == future and inputs.byte_identity(inputs.encoded(future)) == pins['future_manifest'], 'Whole future source derivation differs')
            require(identity(archive.read(PROJECT + 'reports/release-input-snapshot.json')) == pins['future_manifest'], 'Actual run manifest differs')
            overlay_rows = []
            for change in changes:
                name = 'hosted-proof/inputs/overlay/' + change['path']
                actual = identity(archive.read(name))
                require(actual == change['candidate'] == file_identity(SOURCE / change['source']), 'Actual overlay source differs: ' + change['path'])
                overlay_rows.append({'path': change['path'], **actual})
            save('complete-source-binding.json', {'baseline': {key: base[key] for key in ('files','snapshot_sha256')},
                'future': {key: future[key] for key in ('files','snapshot_sha256')}, 'future_manifest': pins['future_manifest'],
                'all_unchanged_rows_derived': True, 'actual_job_source': source_rows, 'actual_overlay': overlay_rows})
            del base, derived, future
            require(execution['preparation_sha256'] == identity(archive.read('hosted-proof/preparation.json'))['sha256'], 'Preparation changed during execution')
            require(execution['input_snapshot_before'] == execution['input_snapshot_after'] == pins['future_snapshot']
                    and execution['build_inputs_unchanged'] is True and execution['execution']['returncode'] == 0,
                    'Actual execution source/result differs')
            start, end = execution['execution']['started_unix_ns'], execution['execution']['ended_unix_ns']
            artifacts = RecordedZipArtifacts(archive, PROJECT, prepared['project'], final['verified_output_artifacts'], start, end)
            for name in artifacts.declared:
                artifacts.bind(name)
            expected_output_names = {n.removeprefix(PROJECT) for n in names if n.startswith(PROJECT + 'reports/') or n.startswith(PROJECT + 'dist/')}
            expected_output_names.remove('reports/release-input-snapshot.json')
            require(set(artifacts.declared) == expected_output_names and len(artifacts.declared) == 720, 'Host final report omits a produced report/APK')
            require(len(latest['commands']) == 16 and latest['host_acceptance_passed'] is True, 'Sixteen gate result incomplete')
            gate_rows = []
            for number, (command, expected) in enumerate(zip(latest['commands'], pins['gate_commands']), 1):
                label, argv = expected
                require(command['label'] == label and command['command'] == ['/usr/bin/python3', *argv]
                        and command['exit_code'] == 0 and command['passed'] is True
                        and command['timeout_seconds'] == (5400 if label == 'ui-negative-controls' else 1200), 'Actual gate command/outcome differs')
                require(command['log'] == f'reports/acceptance-20261012T105228709429Z/{number:02d}-{label}.log', 'Gate log role differs')
                artifacts.hash(command['log'], command['log_sha256'])
                gate_rows.append(command)
            require(artifacts.raw('reports/acceptance-latest.json') == artifacts.raw('reports/acceptance-20261012T105228709429Z/result.json'), 'Session/latest result bytes differ')
            require(set(latest['fresh_evidence_sha256']) == set(pins['fresh_reports']) and len(pins['fresh_reports']) == 23, 'Fresh report inventory differs')
            reports = {}
            for name in pins['fresh_reports']:
                artifacts.hash('reports/' + name, latest['fresh_evidence_sha256'][name])
                reports[name] = artifacts.json('reports/' + name)
            save('sixteen-gates-and-fresh-reports.json', {'gates': gate_rows, 'fresh_reports': latest['fresh_evidence_sha256']})
            apks = latest['apks']
            for variant in ('baseline','hybrid'):
                row = apks[variant]
                require({key: by_name[PROJECT + row['path']][key] for key in ('bytes','sha256')} == {key: row[key] for key in ('bytes','sha256')} == final['apks'][variant], 'Actual APK bytes differ')
            project = ROOT / 'small-source-and-class-copies'
            for name in ('source/java-method-map.json','tests/fixtures/provenance.json','tests/fixtures/original-methods.dex'):
                copy_member(archive, 'hosted-proof/inputs/overlay/' + name, 'small-source-and-class-copies/' + name)
            retained = {}
            for row in final['retained_runtime_classes']:
                source_name = 'hosted-proof/' + row['retained_path']
                require(identity(archive.read(source_name)) == row['identity'], 'Retained actual runtime class differs')
                copy_member(archive, source_name, 'small-source-and-class-copies/' + row['source_path'])
            require(len(final['retained_runtime_classes']) == 31, 'Retained positive runtime class inventory differs')
            suites = production.verify_registry_and_partition(project, pins, apks['hybrid']['sha256'], reports, artifacts)
            fixture = fixture_methods((project / 'tests/fixtures/original-methods.dex').read_bytes())
            registry = json.loads((project / 'source/java-method-map.json').read_bytes())
            registry_keys = {row['target'] + '->' + row['method'] for row in registry}
            actual_fixture = {row['key'] for row in fixture['methods']}
            dependency_keys = set(suites['ui']['dayNumericOriginalDependencyKeys'])
            require(len(fixture['classes']) == 607 and len(fixture['methods']) == len(actual_fixture) == 1246
                    and actual_fixture == registry_keys | dependency_keys and len(dependency_keys) == 3
                    and not registry_keys & dependency_keys and all(row['has_code'] for row in fixture['methods']),
                    'Actual DEX declarations do not equal registered bodies plus the three uncredited getters')
            save('actual-fixture-declarations.json', fixture)
            ui_checks = production.verify_ui_controls(project, pins, reports['ui-negative-controls.json'], suites['ui'], artifacts, ROOT / 'ui-positive-class-receipt', retained)
            require(ui_checks == final['all_ui_mutant_checks'] and len(ui_checks) == 91, 'Actual compiled fault evidence differs')
            python = production.verify_python(artifacts.raw('reports/python-unit-tests.log'), 308)
            tool_python = production.verify_python(archive.read('hosted-tool-host-tests.log'), 92)
            require(python == final['python'], 'Final verifier Python count differs')
            production.verify_other_gates(reports, apks['hybrid']['sha256'])
            numeric = reports['day-numeric-dex-controls.json']
            folder = numeric['evidence_directory']
            policy = artifacts.json('reports/ui-runtime-policy.json')
            production.verify_numeric_commands(numeric, folder, artifacts, policy['java_executable'])
            wrappers = RecordedZipArtifacts(archive, 'hosted-proof/', prepared['output'], final['verified_wrapper_streams'],
                min(row['ctime_ns'] for row in final['verified_wrapper_streams']), max(row['ctime_ns'] for row in final['verified_wrapper_streams']))
            previous = production.row_clock(execution, 'started', 'archived-wrapper')
            completion = production.row_clock(execution, 'finished', 'archived-wrapper')
            wrapper_rows = [('java-version',['java','-version'],execution['java_versions'][0],15),
                ('javac-version',['javac','-version'],execution['java_versions'][1],15),
                ('acceptance',['/usr/bin/python3','-B','acceptance.py'],execution['execution'],pins['acceptance_timeout_seconds'])]
            for label, argv, row, timeout in wrapper_rows:
                require(row['argv'] == argv and row['cwd'] == prepared['project'] and row['returncode'] == 0
                        and row['timed_out'] is False and row['timeout_seconds'] == timeout and 'error' not in row, 'Outer invocation differs')
                begin, finish = production.verify_command_stream_evidence(row, '', label, wrappers)
                production.clocks_ordered(previous, begin, 'archived outer sequence')
                production.clocks_ordered(finish, completion, 'archived wrapper completion')
                previous = finish
            require(len(wrappers.rows) == 12, 'Not all outer streams/witnesses were rechecked')
            producer_raw = archive.read('hosted-proof/inputs/overlay/day_numeric_dex_controls.py')
            validators, selected = selected_numeric_validators(producer_raw.decode())
            positive = artifacts.json(folder + '/positive/result.json')
            restored = artifacts.json(folder + '/positive-restoration/result.json')
            validators['validate_positive'](positive); validators['validate_positive'](restored)
            require(artifacts.raw(folder + '/positive/result.json') == artifacts.raw(folder + '/positive-restoration/result.json'), 'Positive raw restoration differs')
            require(numeric['positive_pipeline'] == pins['numeric_positive_pipeline'] == artifacts.json(folder + '/positive-pipeline/method-body-binding.json'), 'Actual D8/transplant positive binding differs')
            require(artifacts.raw(folder + '/signed-apk-instructions.json') == artifacts.raw(folder + '/positive-transplant-instructions.json'), 'Signed/transplanted instructions differ')
            config = artifacts.json(folder + '/positive/config.json')
            require(config == positive['inputIdentities'] and config['classPins'] == positive['loadedClassOrigins']
                    and len(config['classPins']) == 23, 'Actual numeric class/input identity differs')
            with archive.open(PROJECT + apks['hybrid']['path']) as apk_stream:
                with zipfile.ZipFile(apk_stream) as apk:
                    require(apk.namelist().count('classes3.dex') == 1, 'Signed getter partition is not unique')
                    with apk.open('classes3.dex') as stream:
                        getter_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
            require(getter_hash == config['rebuiltGetterDex']['sha256'], 'Actual signed APK getter DEX differs')
            class_rows = {row['source_path']: row for row in final['retained_runtime_classes']}
            for row in config['classPins'].values():
                name = Path(row['path']).relative_to(prepared['project']).as_posix()
                require(class_rows[name]['identity']['sha256'] == row['sha256'], 'A numeric loaded class differs from retained host bytes')
            fault_rows = []
            for fault in numeric['actual_dex_faults']:
                name = fault['name']
                bad = artifacts.json(folder + '/' + name + '-dex-fault/result.json')
                validators['validate_fault'](positive, bad, fault['required_cases'], validators['JAVA_FAILURE_COUNTS'][name], 'rebuilt')
                bad_config = artifacts.json(folder + '/' + name + '-dex-fault/config.json')
                expected_config = dict(config)
                expected_config['targetDex'] = {'path': prepared['project'] + '/' + folder + '/' + name + '-pipeline/numeric-target.dex', 'sha256': fault['pipeline']['target_dex_sha256']}
                require(bad_config == expected_config == bad['inputIdentities'] and bad['loadedClassOrigins'] == config['classPins'], 'Numeric fault changed unrelated input roles')
                artifacts.hash(folder + '/' + name + '-pipeline/numeric-target.dex', fault['pipeline']['target_dex_sha256'])
                fault_rows.append({'name': name, 'actual_failed_cases': bad['mismatchCount'], 'required_cases': fault['required_cases']})
            for name, message in [('original-as-rebuilt-rejected','Original fixture cannot masquerade as rebuilt target'),
                                  ('wrong-helper-class-rejected','Wrong input identity: class recovered.ui.DayTriggerValueMethods')]:
                production.verify_provenance_config(artifacts.json(folder + '/' + name + '/config.json'), config, name)
                require(PROJECT + folder + '/' + name + '/result.json' not in names
                        and message in artifacts.raw(folder + '/' + name + '/execute.stderr.log').decode(), 'Provenance negative did not reject before report creation')
            validators['validate_positive_coverage'](suites['ui']['dayNumericOriginalCoverage'], 32)
            validators['validate_positive_coverage'](suites['ui']['dayNumericRebuiltCoverage'], 25)
            clock_rows = []
            for group, command in [('outer', row) for _, _, row, _ in wrapper_rows] + [('numeric', row) for row in numeric['commands']]:
                evidence = command['stream_evidence']
                streams = []
                for name, receipt in evidence['streams'].items():
                    streams.append({'role': name, 'path': receipt['path'], 'bytes': receipt['bytes'],
                        'initial_ctime_minus_command_start_ns': receipt['initial_stat']['ctime_ns'] - command['started_unix_ns'],
                        'final_mtime_minus_command_start_ns': receipt['final_stat']['mtime_ns'] - command['started_unix_ns'],
                        'initial_and_final_equal': receipt['initial_stat'] == receipt['final_stat']})
                clock_rows.append({'group': group, 'argv': command['argv'], 'returncode': command['returncode'],
                    'duration_seconds': command['duration_seconds'], 'after_witness_count': len(evidence['after_witnesses']),
                    'filesystem_bracket_complete': evidence['filesystem_bracket_complete'], 'streams': streams})
            save('actual-command-clock-and-stream-replay.json', {'scope': 'Exact saved bytes and original serialized metadata through unchanged predicates; no live-host stat recreation',
                'production_verifier': identity((FROZEN / 'source/tools/day_numeric_acceptance/verify.py').read_bytes()),
                'numeric_commands': 17, 'outer_commands': 3, 'rows': clock_rows,
                'pure_numeric_validator_source': identity(producer_raw), 'selected_validators': selected,
                'actual_faults': fault_rows, 'actual_signed_getter_dex_sha256': getter_hash})
            # Keep the bounded raw relationships convenient to inspect; all other
            # source/results remain in the immutable complete container.
            selected_names = ['hosted-proof/verification.json','hosted-proof/execution.json','hosted-proof/preparation.json',
                'hosted-tool-host-tests.log','hosted-proof/inputs/source-changes.json','hosted-proof/inputs/pins.json',
                PROJECT + 'reports/acceptance-latest.json', PROJECT + 'reports/python-unit-tests.log',
                PROJECT + 'reports/day-numeric-dex-controls.json', PROJECT + 'reports/java-all-path-parity.json',
                PROJECT + 'reports/ui-negative-controls.json', PROJECT + 'reports/reference-failures-status-v9.json',
                PROJECT + 'reports/full-apk-edit-probe.json', PROJECT + 'reports/hybrid-build.json',
                PROJECT + 'reports/java-staging.json', PROJECT + 'reports/ui-runtime-policy.json']
            copies = [copy_member(archive, name, 'review-copies/' + name) for name in selected_names]
            save('review-copy-identities.json', copies)
            result.update(status='INDEPENDENT_STREAMED_HOST_EVIDENCE_BINDING_PASS', passed=True,
                zip={'bytes': 222144520, 'sha256': ZIP_SHA}, members=3308, expanded_bytes=sum(row['bytes'] for row in inventory),
                executed_job_sources=9, actual_overlay_sources=19, complete_source_snapshot=pins['future_snapshot'],
                all_report_and_apk_metadata_rows=720, gates=16, fresh_reports=23, actual_cases=194780,
                registered_methods=1243, target_classes=605, actual_fixture_methods=1246, actual_fixture_classes=607,
                uncredited_getters=3, suite_cases=pins['suite_cases'], python=python, tooling_python=tool_python,
                retained_runtime_classes=31, ui_java_faults=91, actual_numeric_dex_faults=fault_rows,
                numeric_raw_cases=1291, numeric_paths=3, actual_commands_replayed=20,
                exact_positive_restoration=True, signed_transplant_instructions_equal=True,
                apks=final['apks'], android_status=latest['android_status'], active_promoted=False,
                full_runtime_1_to_1_established=False,
                review_scope='Closed artifact/coherence and saved-metadata replay; no new build, test suite or Android run')
    except Exception as error:
        result.update(passed=False, error=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save('result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
