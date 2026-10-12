#!/usr/bin/env python3
"""Read the retained source proof without application execution or archive rereads."""
from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
import stat
import traceback

OWN = Path('/dev/shm/macrodroid-active-numeric-independent-review')
COL = OWN / 'collection-01'
ROOT = COL / 'retained'
OUT = OWN / 'analysis-01'
PROMOTION = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-source-promotion-proposal')
PROMOTION_SHA = '0695be31f63f25952d8236d403206a2b292eef4b4e28ab7fd071c045f0401e14'
APK_SHA = '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
SNAPSHOT = 'f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545'
METHOD = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'
RUN = 'reports/acceptance-20261012T121707487120Z/'
BEFORE = {}


def read(path):
    a = path.lstat(); assert stat.S_ISREG(a.st_mode), str(path)
    data = path.read_bytes(); b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    value = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(b.st_mode)}
    if str(path) in BEFORE:
        assert BEFORE[str(path)] == value
    BEFORE[str(path)] = value
    return data


def load(relative):
    return json.loads(read(ROOT / relative))


def save(name, value):
    with (OUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def clock(value):
    assert type(value['unix_ns']) is int and type(value['monotonic_ns']) is int
    return value['unix_ns'], value['monotonic_ns']


def ordered(*values):
    points = [clock(v) for v in values]
    assert all(a[0] <= b[0] and a[1] <= b[1] for a, b in zip(points, points[1:])), points


def stream_review(row, inventory, command_start, command_end):
    assert row['exclusive_mode'] == 'xb'
    for key in ('initial_stat', 'final_stat'):
        value = row[key]
        assert all(type(value[name]) is int for name in ('device', 'inode', 'mode', 'links', 'bytes', 'mtime_ns', 'ctime_ns'))
        assert value['links'] == 1 and stat.S_ISREG(value['mode'])
    assert row['initial_stat']['bytes'] == 0
    assert row['initial_sha256'] == hashlib.sha256(b'').hexdigest()
    assert all(row['initial_stat'][name] == row['final_stat'][name] for name in ('device', 'inode', 'mode', 'links'))
    assert row['final_stat']['bytes'] == row['bytes']
    raw = inventory[row['path']]
    assert (raw['bytes'], raw['sha256']) == (row['bytes'], row['sha256'])
    ordered(command_start, row['open_started'], row['opened'], row['closing'], row['closed'], row['hashed'], command_end)
    return row['final_stat']['device'], row['final_stat']['inode']


def main():
    OUT.mkdir(exist_ok=False)
    result = {'schema': 1, 'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
              'scope': 'Independent read-only analysis of the active numeric source-build artifact',
              'builds_repeated': False, 'suites_repeated': False, 'android_repeated': False,
              'original_zip_reread': False}
    try:
        collection = json.loads(read(COL / 'result.json'))
        assert collection['passed'] is True and collection['archive_identity_unchanged'] is True
        assert collection['archive_sha256'] == '4824e07658f0e5a808a9dc0b10615b030e3d5f3d030b0fa4ff40096060a34159'
        inventory_rows = json.loads(read(COL / 'zip-member-inventory.json'))
        inventory = {row['path']: row for row in inventory_rows}
        assert len(inventory) == 1304
        bindings = json.loads(read(COL / 'retained-file-bindings.json'))
        for row in bindings:
            raw = read(COL / row['retained_path'])
            assert hashlib.sha256(raw).hexdigest() == row['retained']['sha256'] and len(raw) == row['retained']['bytes']
            if row['gzip_copy']:
                raw = gzip.decompress(raw)
            assert len(raw) == row['source']['bytes'] and hashlib.sha256(raw).hexdigest() == row['source']['sha256']
        jobs = json.loads(read(COL / 'github/github-jobs.json'))['jobs']
        source = next(row for row in jobs if row['name'] == 'source-build')
        android = next(row for row in jobs if row['name'] == 'android-cold-launch')
        assert source['id'] == 114806466819 and source['run_id'] == 38247941263
        assert source['head_sha'] == '8db1fca4f03532ee2e5a8791fde7ea18126c237f'
        assert source['conclusion'] == 'success' and android['conclusion'] == 'failure'
        for number in (4, 5, 6, 7):
            assert next(row for row in source['steps'] if row['number'] == number)['conclusion'] == 'success'
        acceptance = load('reports/acceptance-latest.json')
        assert read(ROOT / 'reports/acceptance-latest.json') == read(ROOT / (RUN + 'result.json'))
        labels = ['input-integrity', 'baseline-build', 'hybrid-build', 'baseline-code', 'hybrid-code',
                  'baseline-resources', 'hybrid-resources', 'positive-host-tests', 'reference-status',
                  'engine-negative-controls', 'ui-negative-controls', 'core-negative-controls',
                  'environment-negative-controls', 'legacy-negative-control', 'signed-source-edit',
                  'final-positive-host-tests']
        assert [row['label'] for row in acceptance['commands']] == labels
        for index, command in enumerate(acceptance['commands'], 1):
            assert command['log'] == RUN + f'{index:02d}-' + command['label'] + '.log'
            assert type(command['exit_code']) is int and command['exit_code'] == 0 and command['passed'] is True
            assert type(command['timeout_seconds']) is int
            assert command['timeout_seconds'] == (5400 if command['label'] == 'ui-negative-controls' else 1200)
            assert 0 <= command['seconds'] <= command['timeout_seconds']
            assert hashlib.sha256(read(ROOT / command['log'])).hexdigest() == command['log_sha256']
        assert acceptance['host_acceptance_passed'] is True and acceptance['source_edit_probe_skipped'] is False
        assert acceptance['input_snapshot_before'] == acceptance['input_snapshot_after'] == SNAPSHOT
        assert acceptance['input_files'] == 81298 and acceptance['build_inputs_unchanged'] is True
        assert acceptance['android_runtime_executed'] is False and acceptance['full_runtime_1_to_1_established'] is False
        assert acceptance['android_status'] == 'BLOCKED' and acceptance['android_probe_exit_code'] == 2
        for name, sha in acceptance['fresh_evidence_sha256'].items():
            assert inventory['reports/' + name]['sha256'] == sha
            assert hashlib.sha256(read(ROOT / 'reports' / name)).hexdigest() == sha
        assert len(acceptance['fresh_evidence_sha256']) == 23
        for variant, apk in acceptance['apks'].items():
            member = inventory[apk['path']]
            assert (member['bytes'], member['sha256']) == (apk['bytes'], apk['sha256'])
            build = load('reports/' + variant + '-build.json')
            assert build['sha256'] == apk['sha256'] and build['bytes'] == apk['bytes']
            assert build['original_apk_build_input'] is False and build['original_dex_build_input'] is False
        assert acceptance['apks']['hybrid']['sha256'] == APK_SHA
        assert hashlib.sha256(read(PROMOTION / 'checkpoint.json')).hexdigest() == PROMOTION_SHA
        promotion = json.loads(read(PROMOTION / 'checkpoint.json'))
        row_map = {row['path']: row for row in promotion['files']}
        for name in ('proposed/artifacts/current/manifest.json', 'proposed/project/reports/release-input-snapshot.json'):
            row = row_map[name]
            assert hashlib.sha256(read(PROMOTION / name)).hexdigest() == row['sha256']
        current = json.loads(read(PROMOTION / 'proposed/artifacts/current/manifest.json'))
        assert (current['size_bytes'], current['sha256']) == (acceptance['apks']['hybrid']['bytes'], APK_SHA)
        assert current['recovered_method_bodies'] == 1243 and current['recovered_classes'] == 605
        assert current['full_functional_parity_established'] is False
        snapshot_raw = gzip.decompress(read(ROOT / 'reports/release-input-snapshot.json.gz'))
        assert snapshot_raw == read(PROMOTION / 'proposed/project/reports/release-input-snapshot.json')
        snapshot = json.loads(snapshot_raw)
        entries = snapshot['entries']
        assert len(entries) == snapshot['files'] == 81298
        assert hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == snapshot['snapshot_sha256'] == SNAPSHOT
        source_rows = [row for row in promotion['files'] if row['path'].startswith('proposed/project/')
                       and row['path'] != 'proposed/project/reports/release-input-snapshot.json']
        assert len(source_rows) == 19
        for row in source_rows:
            name = row['path'].removeprefix('proposed/project/')
            assert entries[name] == {'size': row['bytes'], 'sha256': row['sha256']}
        assert 'day_lookup_dex_controls.py' not in entries
        overall = load('reports/java-all-path-parity.json')
        assert overall['passed'] is True and overall['cases'] == 194780
        assert overall['methodsCovered'] == overall['methodsExpected'] == 1243 and overall['paths'] == 3
        assert overall['failedCases'] == overall['unsupportedExecutions'] == 0
        assert overall['apkSha256'] == APK_SHA and overall['rebuiltDexComparedToApk'] is True
        suite_names = {'legacy': 'java-three-path-parity.json', 'core': 'java-core-three-path-parity.json',
                       'environment': 'java-environment-three-path-parity.json', 'engine': 'java-engine-three-path-parity.json',
                       'ui': 'java-ui-three-path-parity.json'}
        keys = []
        suites = {}
        for name, file in suite_names.items():
            value = load('reports/' + file)
            assert value.get('passed', value.get('pass')) is True
            assert value['paths'] == 3 and value['androidRuntime'] is False
            assert value['rebuilt_apk_sha256'] == APK_SHA and value['rebuilt_dex_compared_to_apk'] is True
            assert value['fixture_sha256'] == overall['fixtureSha256']
            assert value['cases'] == overall['suiteCases'][name]
            assert value['methodsCovered'] == len(value['methodKeys'])
            keys.extend(value['methodKeys'])
            suites[name] = {'cases': value['cases'], 'methods': value['methodsCovered']}
        assert len(keys) == len(set(keys)) == 1243 and sum(row['cases'] for row in suites.values()) == 194780
        integration = load('reports/java-integration.json')
        assert integration['methods'] == len(integration['changes']) == 1243 and integration['classes'] == 605
        assert integration['runtime_stub_classes_included'] == 0
        assert set(keys) == {row['class'] + '->' + row['method'] for row in integration['changes']}
        python_log = read(ROOT / 'reports/python-unit-tests.log').decode()
        tests = re.findall(r'^test_[^ (\n]+ \(([^)]+)\) \.\.\. ok$', python_log, re.M)
        assert len(tests) == len(set(tests)) == 308
        assert 'Ran 308 tests in 11.284s\n\nOK' in python_log
        for variant in ('baseline', 'hybrid'):
            code = load('reports/' + variant + '-roundtrip.json')
            assert code['pass'] is True and code['classes_compared'] == 71267 and code['methods_total'] == 349972
            assert all(code[name] == [] for name in ('missing', 'extra', 'unexpected_changed_methods', 'omitted_registered_changes',
                         'altered_opaque_payload', 'misaligned', 'baseline_source_hash_mismatches'))
            assert len(code['changed_classes']) == (605 if variant == 'hybrid' else 0)
            assert len(code['changed_methods']) == (1243 if variant == 'hybrid' else 0)
            resources = load('reports/' + variant + '-resource-parity.json')
            assert resources['pass'] is True and resources['files_expected'] == resources['files_actual'] == 7212
            assert resources['byte_identical'] == 7211 and len(resources['equivalent_enum_order_only']) == 1
            assert resources['resource_ids_expected'] == resources['resource_ids_actual'] == 23854
            assert len(resources['native_libraries']) == 22
            assert all(resources[name] == [] for name in ('changed_files', 'missing_files', 'extra_files', 'changed_resource_ids',
                'missing_resource_names', 'extra_resource_names', 'missing_apk_entries', 'extra_apk_entries', 'changed_zip_compression_methods'))
        ui = load('reports/java-ui-three-path-parity.json')
        baseline_ui, restored_ui = load('reports/ui-negative-baseline.json'), load('reports/ui-positive-restoration.json')
        assert baseline_ui == restored_ui
        assert {k: v for k, v in ui.items() if k not in ('fixture_sha256', 'rebuilt_apk_sha256', 'rebuilt_dex_compared_to_apk')} == restored_ui
        controls = load('reports/ui-negative-controls.json')
        assert controls['pass'] is True and controls['controlsCount'] == controls['expectedControlCount'] == len(controls['controls']) == 91
        assert controls['positiveRestorationPassed'] is True and controls['positiveRestorationExactBaseline'] is True
        assert controls['sourceFixtureAndApkUnchanged'] is True and controls['restorationCases'] == 24465
        for row in controls['controls']:
            assert row['pass'] is True and row['exitCode'] == 2 and row['failedCases'] > 0
            assert row['unsupportedExecutions'] == 0 and row['requiredCaseRejected'] is True
            assert row['sourceFixtureAndApkUnchanged'] is True and row['originalCoverageAndInventoryUnchanged'] is True
            assert inventory[row['retainedSource']]['sha256'] == row['mutantSourceSha256']
            assert inventory[row['retainedClass']]['sha256'] == row['mutantClassSha256']
        numeric = load('reports/day-numeric-dex-controls.json')
        assert numeric['schema'] == 2 and numeric['passed'] is True and numeric['androidRuntime'] is False
        assert numeric['cases'] == 1291 and numeric['execution_paths'] == 3 and numeric['signed_apk_sha256'] == APK_SHA
        assert numeric['primary_recovered_methods'] == 1 and numeric['original_dependency_methods'] == 3
        assert numeric['positive_restoration_byte_exact'] is True and numeric['provenance_controls_rejected'] == 2
        evidence = numeric['evidence_directory']
        assert read(ROOT / evidence / 'positive/result.json') == read(ROOT / evidence / 'positive-restoration/result.json')
        assert read(ROOT / evidence / 'positive-transplant-instructions.json') == read(ROOT / evidence / 'signed-apk-instructions.json')
        for name, count in [('Original', 32), ('Rebuilt', 25)]:
            cover = ui['dayNumeric' + name + 'Coverage']
            assert cover['instructionCount'] == cover['executedInstructionCount'] == count
            assert cover['requiredBranchEdges'] == cover['executedBranchEdges'] == 4 and cover['allInstructionsAndEdgesExecuted'] is True
            for method in cover['methods']:
                assert method['requiredOffsets'] == method['executedOffsets'] and method['missingOffsets'] == []
                assert method['requiredEdges'] == method['executedEdges'] and method['missingEdges'] == []
        for fault, mismatches in [('integer-zero', 509), ('decimal-zero', 406)]:
            row = next(row for row in numeric['actual_dex_faults'] if row['name'] == fault)
            detail = load(evidence + '/' + fault + '-dex-fault/result.json')
            assert row['passed'] is True and row['mismatches'] == detail['mismatchCount'] == len(detail['mismatches']) == mismatches
            assert detail['unsupportedCount'] == 0 and detail['passed'] is False
        names = ['d8-helper', 'disassemble-helper', 'assemble-target', 'signed-apk-instructions', 'positive-transplant-instructions', 'execute',
                 'd8-helper', 'disassemble-helper', 'assemble-target', 'execute',
                 'd8-helper', 'disassemble-helper', 'assemble-target', 'execute', 'execute', 'execute', 'execute']
        exits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 1, 1, 0]
        assert [row['name'] for row in numeric['commands']] == names
        report_start = {'unix_ns': numeric['started_unix_ns'], 'monotonic_ns': numeric['started_monotonic_ns']}
        report_end = {'unix_ns': numeric['finished_unix_ns'], 'monotonic_ns': numeric['finished_monotonic_ns']}
        previous = report_start
        identities = set(); witness_count = 0
        for row, code in zip(numeric['commands'], exits):
            assert type(row['returncode']) is int and row['returncode'] == code
            assert type(row['timeout_seconds']) is int and row['timeout_seconds'] == 120
            rec = row['stream_evidence']
            assert rec['schema'] == 2 and rec['filesystem_bracket_complete'] is True
            assert rec['started']['unix_ns'] == row['started_unix_ns'] and rec['finished']['unix_ns'] == row['ended_unix_ns']
            assert rec['started']['monotonic_ns'] == row['started_monotonic_ns'] and rec['finished']['monotonic_ns'] == row['ended_monotonic_ns']
            ordered(previous, rec['started'], rec['invocation_started'], rec['invocation_finished'], rec['finished'], report_end)
            assert rec['invocation_finished']['monotonic_ns'] - rec['invocation_started']['monotonic_ns'] <= 120_000_000_000
            previous = rec['finished']
            assert 1 <= len(rec['after_witnesses']) <= rec['after_witness_attempt_limit'] == 16
            assert rec['after_witness_poll_ns'] == 5_000_000
            items = [rec['before_witness'], *rec['streams'].values(), *rec['after_witnesses']]
            for item in items:
                key = stream_review(item, inventory, rec['started'], rec['finished'])
                assert key not in identities; identities.add(key)
            witness_count += 1 + len(rec['after_witnesses'])
            for stream in ('stdout', 'stderr'):
                item = rec['streams'][stream]
                assert row[stream] == {k: item[k] for k in ('path', 'bytes', 'sha256')}
                ordered(item['opened'], rec['invocation_started'], rec['invocation_finished'], item['closing'])
                low, high = rec['before_witness']['final_stat'], rec['after_witnesses'][-1]['final_stat']
                for timestamp in ('mtime_ns', 'ctime_ns'):
                    assert low[timestamp] <= item['initial_stat'][timestamp] <= item['final_stat'][timestamp] <= high[timestamp]
        edit = load('reports/full-apk-edit-probe.json')
        assert edit['pass'] is True and edit['original_release_apk_sha256'] == APK_SHA
        assert edit['negative_failed_cases'] == 113 and edit['negative_exit_code'] == 1 and edit['unsupported_executions'] == 0
        assert edit['required_pause_case_rejected'] is True and edit['release_inputs_and_apk_unchanged'] is True
        assert edit['android_runtime_executed'] is False
        historical = load('reports/release-summary-v9.json')
        assert historical['date'] == '2026-10-11' and historical['java_method_bodies'] == 1237
        result.update(passed=True, status='ACTIVE_NUMERIC_SOURCE_PROOF_AND_COMMITTED_APK_MATCH_REVIEWED',
            run_id=source['run_id'], head_sha=source['head_sha'], source_job_id=source['id'], source_job_conclusion='success',
            sibling_android_job_id=android['id'], sibling_android_job_conclusion='failure',
            gate_count=16, fresh_report_bindings=23, source_files=81298, snapshot_sha256=SNAPSHOT,
            exact_promoted_source_rows=19, fresh_hybrid_matches_committed_sha256=APK_SHA,
            host_cases=194780, registered_methods=1243, recovered_classes=605, suites=suites,
            python_named_tests=308, java_controls=91, numeric_child_commands=17,
            numeric_streams=34, numeric_filesystem_witnesses=witness_count,
            numeric_original_instructions={'primary': 25, 'dependencies': 7, 'total': 32},
            numeric_rebuilt_instructions={'primary': 18, 'dependencies': 7, 'total': 25},
            numeric_edges_each_path=4, numeric_dex_fault_mismatches={'integer-zero':509,'decimal-zero':406},
            numeric_raw_restoration_byte_exact=True, ui_restoration_json_object_exact=True,
            archive_live_inode_claim=False, raw_91_failure_bodies_reparsed=False,
            historical_summary_excluded={'date': historical['date'], 'methods': historical['java_method_bodies']},
            full_runtime_parity_established=False)
    except Exception as exc:
        result.update(status='ANALYSIS_ATTEMPT_FAILED', error=repr(exc), traceback=traceback.format_exc())
    finally:
        after = {}
        for name in list(BEFORE):
            path = Path(name); data = path.read_bytes(); value = path.stat()
            after[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(value.st_mode)}
        result['read_inputs_unchanged'] = BEFORE == after
        if BEFORE != after:
            result['passed'] = False
        save('inputs-before.json', BEFORE); save('inputs-after.json', after)
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); save('result.json', result)
        print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
