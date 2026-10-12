#!/usr/bin/env python3
"""Independent read-only review of the closed nine-path combined-host tooling."""
from datetime import datetime, timezone
import ast
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tarfile
import traceback

BASE = Path('/dev/shm/macrodroid-combined-host-tooling-review')
OUT = BASE / 'closed-01'
CAP = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls')
DESIGN = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/06-combined-host-workflow-design')
SOURCE = CAP / 'source'
TOOLS = SOURCE / 'tools/day_trigger_acceptance'
PARENT = DESIGN / 'parent-tooling-source/tools/day_numeric_acceptance'
PROTOCOL = DESIGN / 'evidence/reports/22-combined-host-design-source/proposed-command-and-report-contract.json'


def identity(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    return {'bytes': after.st_size, 'sha256': digest}


def read(path):
    return json.loads(path.read_bytes())


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def definitions(path):
    text = path.read_text()
    return {node.name: ast.get_source_segment(text, node) for node in ast.parse(text).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


def fingerprint_snapshot(entries):
    entries = dict(sorted(entries.items()))
    raw = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    return {'format': 1, 'files': len(entries), 'snapshot_sha256': hashlib.sha256(raw).hexdigest(), 'entries': entries}


def derive(before, changes):
    entries = copy.deepcopy(before['entries'])
    assert len({row['path'] for row in changes}) == len(changes)
    for row in changes:
        old = row['baseline']
        if old is None:
            assert row['must_be_absent_if_new'] is True and row['path'] not in entries
        else:
            assert entries[row['path']] == {'size': old['bytes'], 'sha256': old['sha256']}
    for row in changes:
        entries[row['path']] = {'size': row['candidate']['bytes'], 'sha256': row['candidate']['sha256']}
    return fingerprint_snapshot(entries)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-review.py')
    result = {'schema': 1, 'passed': False, 'status': 'REVIEW_NOT_COMPLETED',
        'started_utc': datetime.now(timezone.utc).isoformat(), 'new_android_actions': [],
        'application_build_or_test_executions': 0, 'new_full_tooling_test_executions': 0,
        'full_runtime_1_to_1_established': False}
    before = {}
    try:
        checkpoint = CAP / 'checkpoint.json'
        assert identity(checkpoint) == {'bytes': 15507, 'sha256': '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88'}
        manifest = read(checkpoint)
        assert len(manifest['files']) == 65
        assert {p.relative_to(CAP).as_posix() for p in CAP.rglob('*') if p.is_file()} == {r['path'] for r in manifest['files']} | {'checkpoint.json'}
        for row in manifest['files']:
            path = CAP / row['path']
            expected = {k: row[k] for k in ('bytes', 'sha256')}
            assert identity(path) == expected and stat.S_IMODE(path.stat().st_mode) == row['mode'], row['path']
            before[str(path)] = expected
        before[str(checkpoint)] = identity(checkpoint)
        external = read(CAP / 'review/05-source-and-workflow-boundaries-corrected/exact-read-boundaries.json')
        assert len(external) == 569
        for name, expected in external.items():
            assert identity(Path(name)) == expected, name
            before[name] = expected
        for path in [PROTOCOL, *[PARENT / n for n in ('inputs.py', 'run_acceptance.py', 'verify.py')]]:
            before[str(path)] = identity(path)
        inventory = read(CAP / 'evidence-inventory.json')
        expected_members = {row['path']: row for row in inventory['files']}
        assert len(expected_members) == inventory['file_count'] == 12451
        observed = {}
        with tarfile.open(CAP / 'evidence.tar.gz', 'r:gz') as archive:
            for member in archive:
                name = PurePosixPath(member.name)
                assert member.isfile() and not name.is_absolute() and '..' not in name.parts
                assert name.as_posix() == member.name and member.name not in observed
                assert member.mode == expected_members[member.name]['mode'], member.name
                with archive.extractfile(member) as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                observed[member.name] = {'bytes': member.size, 'sha256': digest}
        assert set(observed) == set(expected_members)
        assert all(observed[name] == {key: row[key] for key in ('bytes', 'sha256')}
                   for name, row in expected_members.items())
        write('archive-member-verification.json', {'files': len(observed),
            'payload_bytes': sum(row['bytes'] for row in observed.values()),
            'archive': identity(CAP / 'evidence.tar.gz'), 'all_members_match': True,
            'filesystem_extraction_performed': False,
            'inert_nonregular_source_descriptions': [row for row in inventory['files'] if row['source_kind'] != 'regular']})
        bindings = read(CAP / 'nine-path-bindings.json')['files']
        assert len(bindings) == 9 and all(row['active_path_must_be_absent'] is True for row in bindings)
        for row in bindings:
            assert identity(SOURCE / row['path']) == {k: row['candidate'][k] for k in ('bytes', 'sha256')}
        runtime = read(TOOLS / 'runtime-files.json')
        assert len(runtime['files']) == 7
        assert identity(TOOLS / 'runtime-files.json')['sha256'] == '07b58ce29d4db875ef349d23aa05b8b75145ea4f7338b7dd2943db10129a0d32'
        for row in runtime['files']:
            assert identity(TOOLS / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
        unchanged = {
            'inputs.py': ['require', 'pairs', 'document', 'read_json', 'encoded', 'write_json', 'byte_identity',
                'identity', 'relative', 'regular', 'checked_identity', 'metadata', 'snapshot', 'validate_snapshot',
                'input_name', 'derive', 'scan_inputs', 'compare_inputs', 'atomic_bytes', 'apply_changes', 'load_pins',
                'verify_git_commit', 'verify_runtime_manifest'],
            'run_acceptance.py': ['command_clock', 'command_file_stat', 'CommandStreamEvidence', 'stop_owned_group', 'run_child'],
            'verify.py': ['count', 'flags', 'epoch_ns', 'Artifacts', 'checked_clock', 'row_clock', 'clocks_ordered',
                'checked_stat', 'verify_file_creation', 'verify_command_stream_evidence', 'verify_execution',
                'verify_wrapper_streams', 'verify_python', 'verify_apks', 'verify_suite_scope', 'retain_class',
                'expected_numeric_commands', 'verify_numeric_commands', 'verify_java_policy', 'expected_provenance_config',
                'verify_provenance_config', 'verify_numeric'],
        }
        exact = []
        for name, names in unchanged.items():
            old, new = definitions(PARENT / name), definitions(TOOLS / name)
            for function in names:
                assert old[function] == new[function], (name, function)
                exact.append({'file': name, 'definition': function,
                              'sha256': hashlib.sha256(new[function].encode()).hexdigest()})
        assert len(exact) == 50
        write('fifty-exact-parent-definitions.json', exact)
        pins, protocol = read(TOOLS / 'pins.json'), read(PROTOCOL)
        baseline_path = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/reports/release-input-snapshot.json')
        before[str(baseline_path)] = identity(baseline_path)
        assert before[str(baseline_path)] == {'bytes': 14502990, 'sha256': 'ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe'}
        baseline = read(baseline_path)
        assert fingerprint_snapshot(baseline['entries']) == baseline
        numeric = derive(baseline, pins['source_changes'])
        combined = derive(numeric, pins['lookup_source_changes'])
        for value, expected, expected_bytes in [(numeric, pins['numeric_future_snapshot'], pins['numeric_future_manifest']),
                                                (combined, pins['future_snapshot'], pins['future_manifest'])]:
            assert {k: value[k] for k in ('files', 'snapshot_sha256')} == expected
            encoded = json.dumps(value, indent=2, ensure_ascii=True).encode()
            assert {'bytes': len(encoded), 'sha256': hashlib.sha256(encoded).hexdigest()} == expected_bytes
        assert [baseline['files'], numeric['files'], combined['files']] == [81291, 81298, 81304]
        union = {row['path'] for row in pins['source_changes']} | {row['path'] for row in pins['lookup_source_changes']}
        assert len(union) == 25 and sorted(union) == pins['source_union_paths']
        assert len(set(combined['entries']) - set(baseline['entries'])) == 13
        assert pins['all_cases'] == sum(pins['suite_cases'].values()) == 195151
        assert pins['python_tests'] == 357 and pins['registered_methods'] == 1244
        assert pins['gate_commands'] == protocol['gate_order'] and pins['fresh_reports'] == protocol['fresh_reports']
        assert len(pins['gate_commands']) == 16 and len(pins['fresh_reports']) == 24
        write('independent-two-stage-manifest-derivation.json', {
            'boundaries': [{k: item[k] for k in ('files', 'snapshot_sha256')} for item in (baseline, numeric, combined)],
            'complete_before_states_checked_before_each_dictionary_mutation': True,
            'union_paths': sorted(union), 'new_inputs': 13,
            'physical_full_project_materialization_performed': False})
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(TOOLS))
        import verify
        assert Path(verify.__file__).resolve() == TOOLS / 'verify.py'
        project, java = '/owned/review/project', '/owned/review/java'
        expanded = {}
        for role, function in [('numeric', verify.expected_numeric_commands), ('lookup', verify.expected_lookup_commands)]:
            evidence = 'day-' + role + '-dex-fixed'
            actual = function(Path(project), 'reports/' + evidence, java)
            expected = []
            for row in protocol[role + '_commands']:
                argv = [value.replace('<project>', project).replace('<java>', java)
                        .replace('<' + role + '-evidence>', evidence) for value in row['argv']]
                expected.append((row['directory'], row['name'], row['expected_returncode'], argv))
                assert row['timeout_seconds'] == 120
            assert actual == expected and len(actual) == {'numeric': 17, 'lookup': 19}[role]
            expanded[role] = actual
        write('independent-exact-command-vectors.json', expanded)
        controls = read(CAP / 'review/03-corrected-153-controls/result.json')
        assert controls['returncode'] == 0 and controls['passed'] is True and controls['observed_tests'] == 153
        assert controls['source_before'] == controls['source_after'] == controls['executed_source_after']
        for row in controls['source_before']:
            assert identity(SOURCE / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
        for name, expected in controls['logs'].items():
            assert identity(CAP / 'review/03-corrected-153-controls' / name) == expected
        stderr = (CAP / 'review/03-corrected-153-controls/stderr.log').read_text()
        summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', stderr, re.M)
        headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ', stderr, re.M)
        successes = re.findall(r'(?:\.\.\. |^)ok$', stderr, re.M)
        assert len(summaries) == 1 and int(summaries[0][0]) == len(headers) == len(successes) == 153
        assert stderr.rstrip().endswith('\nOK')
        boundary = read(CAP / 'review/05-source-and-workflow-boundaries-corrected/result.json')
        assert boundary['passed'] is True and boundary['all_bound_reads_unchanged'] is True
        assert len(boundary['commands']) == 12
        for command in boundary['commands']:
            assert command['returncode'] == command['expected_returncode'] and command['timeout_seconds'] == 15
            for role in ('stdout', 'stderr'):
                file = CAP / 'review/05-source-and-workflow-boundaries-corrected/commands' / command['name'] / (role + '.log')
                assert identity(file) == command[role]
        assert [(row['actual_exit'], row['intended_exit']) for row in boundary['actual_literal_preflight_controls']] == [(0, 0)] + [(1, 1)] * 5
        write('literal-tooling-controls-and-boundaries.json', {'tests': 153, 'individual_successes': len(successes),
            'wall_seconds': controls['elapsed_seconds'], 'unittest_seconds': float(summaries[0][1]),
            'all_nine_sources_and_execution_copy_equal': True, 'source_reads_checked': 569,
            'shell_syntax_commands': 6, 'bootstrap_positive': 1, 'bootstrap_rejections': 5,
            'commands_and_streams_hash_checked': 12, 'new_corpus_execution_performed': False})
        result.update(passed=True, status='COMBINED_HOST_TOOLING_INDEPENDENT_REVIEW_PASSED',
            capsule_files_checked=65, streamed_archive_members=12451, external_inputs_checked=569,
            exact_parent_definitions=50, command_vectors={'numeric': 17, 'lookup': 19},
            new_active_paths=9, requires_all_nine_active_paths_absent=True,
            reviewed_workflow_sha256='443e184bc3185593e1a8c268d60200ada2b1cdb6df2b8e551e51ae52dae0c6eb',
            reviewed_runtime_sha256='07b58ce29d4db875ef349d23aa05b8b75145ea4f7338b7dd2943db10129a0d32')
    except Exception as error:
        result.update(passed=False, status='COMBINED_HOST_TOOLING_REVIEW_REJECTED', error=repr(error))
        write('exception.json', {'exception': repr(error), 'traceback': traceback.format_exc()})
    finally:
        after = {name: identity(Path(name)) for name in before}
        result['all_read_inputs_unchanged'] = before == after
        if before != after:
            result.update(passed=False, status='REVIEW_INPUTS_CHANGED')
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write('read-input-identities.json', before)
        write('result.json', result)
        print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
