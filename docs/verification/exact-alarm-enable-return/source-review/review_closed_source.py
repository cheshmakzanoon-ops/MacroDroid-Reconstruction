#!/usr/bin/env python3
"""Independently bind the closed Settings source, named host results and raw replay."""
import ast
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tarfile
import traceback
from datetime import datetime, timezone

BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
CAP = BASE / 'checkpoints/03-source-and-host-controls'
OUT = BASE / 'source-review-01'
PARENT = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/03-corrected-source-and-host-controls/replay-source')
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189/extracted')
ORIGINAL_REPLAY = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/05-fourteen-screen-device-analysis/analysis/literal-captured-comparison-replay.json')


def identity(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    return {'bytes': after.st_size, 'sha256': digest}


def read(path):
    return json.loads(path.read_bytes())


def write(name, value):
    with (OUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def definitions(path):
    source = path.read_text()
    return {n.name: ast.get_source_segment(source, n) for n in ast.parse(source).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


def main():
    OUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-review.py')
    before = {}
    result = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'android_executed': False, 'new_host_suite_executed': False, 'new_device_replay_executed': False}
    try:
        before[str(CAP / 'checkpoint.json')] = identity(CAP / 'checkpoint.json')
        assert before[str(CAP / 'checkpoint.json')] == {'bytes': 39880, 'sha256': '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051'}
        cp = read(CAP / 'checkpoint.json')
        assert len(cp['files']) == 181 and cp['source_files'] == 102 and cp['distinct_host_tests_passed'] == 259
        assert cp['complete_historical_schema6_verdict_unchanged'] is True and cp['android_executed'] is False
        assert {p.relative_to(CAP).as_posix() for p in CAP.rglob('*') if p.is_file()} == {r['path'] for r in cp['files']} | {'checkpoint.json'}
        for row in cp['files']:
            path = CAP / row['path']; before[str(path)] = identity(path)
            assert before[str(path)] == {k: row[k] for k in ('bytes', 'sha256')}
            assert stat.S_IMODE(path.stat().st_mode) == row['mode']
        source = {p.relative_to(CAP / 'source').as_posix(): identity(p) for p in (CAP / 'source').rglob('*') if p.is_file()}
        parent = {p.relative_to(PARENT).as_posix(): identity(p) for p in PARENT.rglob('*') if p.is_file()}
        assert len(parent) == 98 and len(source) == 102 and set(parent) <= set(source)
        before.update({str(PARENT / name): value for name, value in parent.items()})
        changed = sorted(name for name in parent if parent[name] != source[name])
        added = sorted(set(source) - set(parent))
        assert changed == ['tools/parity_journeys/editor_journey.py', 'tools/parity_journeys/observed_journey.py']
        assert added == ['tools/parity_journeys/exact_alarm_enable_return.py', 'tools/parity_journeys/exact_alarm_enable_return_readiness.py', 'tools/parity_journeys/test_exact_alarm_enable_return.py', 'tools/parity_journeys/test_exact_alarm_enable_return_readiness.py']
        preserved = read(CAP / 'reports/definition-preservation.json')
        for item in preserved['unchanged_parent_definitions']:
            name, definition = item.split(':')
            assert definitions(PARENT / name)[definition] == definitions(CAP / 'source' / name)[definition], item
        assert len(preserved['unchanged_parent_definitions']) == 37
        for name, names in preserved['changed_dispatch_definitions'].items():
            old, new = definitions(PARENT / name), definitions(CAP / 'source' / name)
            assert sorted(k for k in old if old[k] != new[k]) == names
        old_classifier = ast.parse(definitions(PARENT / 'tools/parity_journeys/exact_alarm_journey.py')['_command_kind'])
        new_classifier = ast.parse(definitions(CAP / 'source/tools/parity_journeys/exact_alarm_enable_return.py')['_command_kind'])
        assert ast.dump(old_classifier) == ast.dump(new_classifier)
        adapter = ast.parse((CAP / 'source/tools/parity_journeys/exact_alarm_enable_return.py').read_bytes())
        contract = next(ast.literal_eval(n.value) for n in adapter.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CONTRACT_BYTES' for t in n.targets))
        assert contract == (CAP / 'design/settings-contract.json').read_bytes()
        assert hashlib.sha256(contract).hexdigest() == '379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07'
        write('independent-source-boundaries.json', {'source_files': 102, 'parent_files': 98, 'unchanged': 96,
            'changed': changed, 'added': added, 'unchanged_dispatch_definitions': 37,
            'global_command_classifier_ast_unchanged': True, 'embedded_contract_exact': True})
        inv = read(CAP / 'evidence-inventory.json'); assert len(inv) == 353
        expected = {row['path']: row for row in inv}; assert len(expected) == 353
        observed, small = {}, {}
        with tarfile.open(CAP / 'evidence.tar.gz', 'r:gz') as archive:
            for member in archive:
                assert member.isfile() and not PurePosixPath(member.name).is_absolute() and '..' not in PurePosixPath(member.name).parts
                assert member.name not in observed and member.name in expected
                with archive.extractfile(member) as stream:
                    data = stream.read()
                actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                assert actual == {k: expected[member.name][k] for k in ('bytes', 'sha256')}
                assert member.mode == expected[member.name]['mode']
                observed[member.name] = actual
                if member.name.endswith(('raw-inputs-before.json.gz', 'raw-inputs-after.json.gz')):
                    small[member.name] = data
        assert set(observed) == set(expected)
        tests, results = set(), []
        for role, count in [('01-first-focused-controls', 50), ('03-parent-compatibility-controls', 209)]:
            root = CAP / 'reports/attempts' / role
            run, summary, names = read(root / 'result.json'), read(root / 'tests-result.json'), read(root / 'discovered-tests.json')
            assert run['passed'] is True and run['returncode'] == 0 and run['working_source_unchanged'] and run['executed_source_unchanged']
            assert summary['passed'] is True and summary['tests_discovered'] == summary['tests_run'] == count
            assert all(summary[key] == [] for key in ('failures', 'errors', 'skipped', 'unexpected_successes'))
            assert len(names) == len(set(names)) == count and not tests.intersection(names)
            text = (root / 'stderr.txt').read_text()
            successes = re.findall(r'^test_\S+ \(([^)]+)\) \.\.\. ok$', text, re.M)
            assert set(successes) == set(names) and len(successes) == count
            assert len(re.findall(r'^Ran ' + str(count) + r' tests in [0-9.]+s$', text, re.M)) == 1 and text.rstrip().endswith('\nOK')
            for inventory_name in ('source-before.json', 'source-after.json', 'executed-source-after.json'):
                rows = read(root / inventory_name)
                assert set(rows) == set(source)
                assert all({k: row[k] for k in ('bytes', 'sha256')} == source[name] for name, row in rows.items())
            for name, wanted in source.items():
                assert observed[role + '/repository/' + name] == wanted
            tests.update(names); results.append({'role': role, 'tests': count, 'seconds': run['seconds'], 'all_named_successes': True})
        assert len(tests) == 259 and sorted(tests) == read(CAP / 'reports/distinct-passed-tests.json')
        write('independently-bound-host-results.json', {'distinct_tests': 259, 'disjoint_attempts': results,
            'all_executed_source_bytes_exact': True, 'archived_evidence_members': len(observed)})
        raw_before = json.loads(gzip.decompress(small['04-real-fourteen-screen-replay/raw-inputs-before.json.gz']))
        raw_after = json.loads(gzip.decompress(small['04-real-fourteen-screen-replay/raw-inputs-after.json.gz']))
        assert raw_before == raw_after and len(raw_before) == 3507
        for name, wanted in raw_before.items():
            path = RAW / name; before[str(path)] = identity(path)
            assert before[str(path)] == wanted
        replay_root = CAP / 'reports/attempts/04-real-fourteen-screen-replay'
        replay = read(replay_root / 'literal-captured-comparison-replay.json')
        before[str(ORIGINAL_REPLAY)] = identity(ORIGINAL_REPLAY)
        assert replay == read(replay_root / 'expected-historical-comparison.json') == read(ORIGINAL_REPLAY)
        assert replay['status'] == 'JOURNEY_DIFFERENCE' and replay['full_runtime_1_to_1_established'] is False
        assert [row['changed_pixels'] for row in replay['screens']] == [0,35,0,0,0,0,0,0,0,0,0,0,0,0]
        assert all(row['hierarchy_equal'] for row in replay['screens'])
        assert replay['global_command_observations']['planned_inputs'] == 26 and replay['settings_inputs'] == 0
        record = read(replay_root / 'result.json')
        assert record['passed'] is True and record['returncode'] == 0 and record['complete_raw_artifact_unchanged'] is True
        assert record['android_executed_by_replay'] is False and record['source_files'] == 102
        for name, wanted in source.items():
            assert observed['04-real-fourteen-screen-replay/repository/' + name] == wanted
        write('independently-bound-historical-replay.json', {'raw_files': 3507, 'comparison_object_exact': True,
            'status': replay['status'], 'changed_pixels': [row['changed_pixels'] for row in replay['screens']],
            'commands': replay['global_command_observations']['commands'], 'planned_inputs': 26,
            'settings_inputs': 0, 'all_replay_source_bytes_exact': True})
        result.update(passed=True, status='SETTINGS_SOURCE_259_HOST_CONTROLS_AND_REAL14_REPLAY_INDEPENDENTLY_REVIEWED',
            capsule_payloads=181, archive_members=353, source_files=102, changed_parent_files=2, new_files=4,
            named_host_successes=259, unchanged_dispatch_definitions=37, historical_raw_files=3507,
            new_settings_plan_screens=16, predicted_on_previously_observed=False, full_runtime_1_to_1_established=False)
    except Exception as error:
        result.update(status='SETTINGS_SOURCE_INDEPENDENT_REVIEW_FAILED', reason=repr(error))
        write('exception.json', {'exception': repr(error), 'traceback': traceback.format_exc()})
    finally:
        after = {name: identity(Path(name)) for name in before}
        result['all_inputs_unchanged'] = before == after
        if before != after:
            result.update(passed=False, status='SETTINGS_REVIEW_INPUT_CHANGED')
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write('read-input-identities.json', before); write('result.json', result)
        print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
