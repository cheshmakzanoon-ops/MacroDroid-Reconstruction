#!/usr/bin/env python3
"""Read-only capsule/source/closed-evidence audit. Never executes app/tool suites."""
import ast
import datetime
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import re
import stat
import struct
import sys
import time
import traceback
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops
import yaml

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "attempt-02"
CAPSULES = [
    ("design", Path('/dev/shm/ink-indicator-fixed-sampling-design/checkpoint.json'),
     'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec'),
    ("root-design-review", Path('/dev/shm/macrodroid-indicator-design-review/checkpoint.json'),
     '92e8ceee8d6098825984de9c09993c24b287a93db4f5a7dd44991c1eb1d6e999'),
    ("incomplete-draft", Path('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/01-incomplete-runtime-draft/checkpoint.json'),
     'effbce444cd4630f0d877163ef0477c273d4d796822f0ec2357c379212585675'),
    ("implemented-offline", Path('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/02-implemented-offline-validated/checkpoint.json'),
     'd555736471dafe7cf9c93a2d32580d76ca9cd2a1f41a4ae60fc8c68deb5cdf62'),
    ("final-correction", Path('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/03-closed-synthetic-test-correction/checkpoint.json'),
     '89064abe581191cd0690eda4e739a91a9b5bae3c56cb9156533ddd78a857f7be'),
]
FINAL = CAPSULES[-1][1].parent
OLD = CAPSULES[-2][1].parent
SOURCE = FINAL / 'source'
MODULES = SOURCE / 'tools/indicator_sampling'
EXPERIMENT = FINAL / 'reports/attempt-02/host-evidence/complete-synthetic-baseline/experiment'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ident(path):
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha(raw),
            'mode': '100755' if s.st_mode & 0o111 else '100644'}


def save(name, value):
    with (OUT / name).open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def load(path):
    return json.loads(path.read_bytes())


def check_row(base, row):
    rel = Path(row['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    got = ident(base / rel)
    assert all(got[k] == row[k] for k in ('bytes', 'sha256')), str(base / rel)
    if 'mode' in row:
        mode = row['mode']
        if mode.startswith('0o'):
            mode = '100755' if int(mode, 8) & 0o111 else '100644'
        assert got['mode'] == mode, str(base / rel)
    return {'path': rel.as_posix(), **got}


def source_inventory(base):
    return [{'path': p.relative_to(base).as_posix(), **ident(p)}
            for p in sorted(base.rglob('*')) if p.is_file()]


def tests(text):
    tree = ast.parse(text)
    return {f'{c.name}.{m.name}': ast.dump(m, include_attributes=False)
            for c in tree.body if isinstance(c, ast.ClassDef)
            for m in c.body if isinstance(m, ast.FunctionDef) and m.name.startswith('test_')}


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())), element.text,
            element.tail, tuple(canonical(c) for c in element))


def main():
    capsule_rows = []
    for name, path, expected in CAPSULES:
        checkpoint_id = ident(path)
        assert checkpoint_id['sha256'] == expected, name
        value = load(path)
        rows = value['files']
        assert len({r['path'] for r in rows}) == len(rows), name
        actual = [check_row(path.parent, row) for row in rows]
        capsule_rows.append({'name': name, 'checkpoint_path': str(path),
                             'checkpoint_identity': checkpoint_id,
                             'payload_count': len(actual),
                             'payload_bytes': sum(r['bytes'] for r in actual),
                             'verified_payloads': actual})
        print(f'Verified {name}: {len(actual)} exact payloads', flush=True)
    save('verified-capsule-payloads.json', capsule_rows)

    old_rows = source_inventory(OLD / 'source')
    final_rows = source_inventory(SOURCE)
    old_map = {r['path']: r for r in old_rows}
    final_map = {r['path']: r for r in final_rows}
    assert old_map.keys() == final_map.keys() and len(final_map) == 16
    changed = sorted(p for p in final_map if final_map[p] != old_map[p])
    expected_changes = ['.github/workflows/indicator-fixed-sampling.yml',
                        'tools/indicator_sampling/runtime-files.json',
                        'tools/indicator_sampling/test_indicator_sampling.py']
    assert changed == expected_changes
    test_rel = 'tools/indicator_sampling/test_indicator_sampling.py'
    before_test = (OLD / 'source' / test_rel).read_text()
    after_test = (SOURCE / test_rel).read_text()
    old_assertion = "self.rejected('Local APK')"
    new_assertion = "self.rejected('Slot local APK read differs from its fixed input')"
    assert before_test.count(old_assertion) == 1
    assert before_test.replace(old_assertion, new_assertion) == after_test
    old_tests, new_tests = tests(before_test), tests(after_test)
    assert old_tests.keys() == new_tests.keys() and len(new_tests) == 41
    changed_test = 'SyntheticTraceControls.test_changed_local_apk_identity_rejects_before_any_capture_credit'
    assert [k for k in old_tests if old_tests[k] != new_tests[k]] == [changed_test]
    runtime = load(MODULES / 'runtime-files.json')
    assert len(runtime) == 15 and len({r['path'] for r in runtime}) == 15
    assert {r['path'] for r in runtime} == final_map.keys() - {'tools/indicator_sampling/runtime-files.json'}
    for row in runtime:
        check_row(SOURCE, row)
    wf_rel = '.github/workflows/indicator-fixed-sampling.yml'
    old_wf, new_wf = (OLD/'source'/wf_rel).read_text(), (SOURCE/wf_rel).read_text()
    def metadata(row):
        return repr(test_rel) + ': ' + repr({k: row[k] for k in ('bytes', 'sha256')})
    assert old_wf.count(metadata(old_map[test_rel])) == 1
    assert old_wf.replace(metadata(old_map[test_rel]), metadata(final_map[test_rel])) == new_wf
    own_workflow = yaml.load(new_wf, Loader=yaml.BaseLoader)
    assert own_workflow['on']['push']['paths'] == [wf_rel, 'tools/indicator_sampling/**']
    assert 'workflow_dispatch' in own_workflow['on']
    job = own_workflow['jobs']['fixed-sampling']
    assert job['timeout-minutes'] == '150' and len(job['steps']) == 9
    assert job['steps'][-1]['if'] == 'always()'
    assert job['steps'][-1]['with']['include-hidden-files'] == 'true'
    save('source-delta-and-test-asts.json', {
        'old_source': old_rows, 'final_source': final_rows, 'changed_paths': changed,
        'literal_assertion_only': True, 'other_test_asts_unchanged': 40,
        'changed_test': changed_test, 'runtime_rows_exact': 15,
        'workflow_only_exact_test_metadata_replaced': True,
        'workflow_jobs': list(own_workflow['jobs']),
        'workflow_steps': [s['name'] for s in job['steps']]})

    protocol = load(MODULES / 'protocol.json')
    design_protocol = load(CAPSULES[0][1].parent / 'protocol.json')
    design_diff = []
    for key in design_protocol:
        if key in ('kind', 'scope', 'android_execution_authorized_by_this_capsule', 'active_files'):
            continue
        assert key in protocol, key
        if design_protocol[key] != protocol[key]:
            design_diff.append(key)
    assert not design_diff, design_diff
    pins = load(MODULES/'pins.json')
    parent_rows = load(CAPSULES[0][1].parent/'evidence/parent-bindings.json')['files']
    pin_map = {r['path']: r for r in pins['parents']}
    assert len(pin_map) == 16 and len(parent_rows) == 16
    for r in parent_rows:
        assert pin_map[r['path']] == {k:r[k] for k in ('path','bytes','sha256','mode')}
        check_row(Path('/dev/shm/ink-indicator-fixed-sampling-01/parent-inputs'), pin_map[r['path']])
    for side in ['original','candidate']:
        for surface in ['intro1-preinput','intro2']:
            name = f'{side}-{surface}.xml'
            assert (MODULES/'fixtures'/name).read_bytes() == (
                CAPSULES[0][1].parent/'evidence/observed-xml'/name).read_bytes()
    save('design-input-binding.json', {'protocol_semantic_top_level_fields_equal': [
        k for k in design_protocol if k not in ('kind','scope','android_execution_authorized_by_this_capsule','active_files')],
        'fixed_parent_commit': pins['parent_commit'], 'parent_rows': pins['parents'],
        'all_16_current_parent_bytes_verified': True, 'all_four_observed_xml_copies_exact': True})

    full_log = (FINAL/'reports/attempt-02/stderr.log').read_text()
    parsed = re.findall(r'^(test_\w+) \(test_indicator_sampling\.(\w+)\.(test_\w+)\) \.\.\. (ok|FAIL)$', full_log, re.M)
    assert all(name == full_name for name, cls, full_name, result in parsed)
    outcomes = {f'{cls}.{name}': result for name, cls, full_name, result in parsed}
    assert outcomes.keys() == new_tests.keys() and len(parsed) == 41
    assert [name for name, result in outcomes.items() if result != 'ok'] == [changed_test]
    assert 'Ran 41 tests in 851.940s' in full_log and 'FAILED (failures=1)' in full_log
    full_result = load(FINAL/'reports/attempt-02/result.json')
    assert full_result['returncode'] == 1 and full_result['status'] == 'FAILED'
    assert full_result['source_unchanged'] and full_result['parent_inputs_unchanged']
    assert full_result['timeout_seconds'] == 900 and full_result['timed_out'] is False
    focused_result = load(FINAL/'reports/focused-03/result.json')
    focused_log = (FINAL/'reports/focused-03/unittest.log').read_text()
    assert 'Ran 1 test in 7.576s' in focused_log and focused_log.endswith('OK\n')
    assert focused_result['tests_run'] == 1 and focused_result['failures'] == focused_result['errors'] == 0
    assert focused_result['new_recorder_capture_executed'] is False
    assert focused_result['closed_baseline_unchanged'] and focused_result['final_source_unchanged']
    assert focused_result['test_body_source'] == {k: final_map[test_rel][k] for k in ('bytes','sha256')}
    for prefix in ['closed-baseline','final-source']:
        assert (FINAL/f'reports/focused-03/{prefix}-before.json').read_bytes() == (
            FINAL/f'reports/focused-03/{prefix}-after.json').read_bytes()
    assert (FINAL/'reports/focused-03/executed-test_indicator_sampling.py').read_text() == after_test
    save('actual-named-test-outcomes.json', {
        'full_attempt_literal_status': 'FAILED', 'full_attempt_40_passed_one_assertion_failed': outcomes,
        'focused_corrected_test': changed_test, 'focused_result': focused_result,
        'distinct_passing_bodies_union': 41, 'fresh_final_full_suite_executed': False,
        'inspected_existing_logs_only': True, 'new_test_execution_by_this_review': False})

    comparison = load(EXPERIMENT/'comparison.json')
    experiment = load(EXPERIMENT/'experiment.json')
    assert experiment['deadline_ns'] - experiment['started_ns'] == 7200*10**9
    assert experiment['finished_ns'] <= experiment['deadline_ns']
    assert [s['index'] for s in comparison['slots']] == list(range(1,9))
    assert comparison['completed_slots'] == 8 and comparison['post_input_frames'] == 40
    expected_pairs = []
    for condition, slots in [('A', range(1,5)), ('B', range(5,9))]:
        for sample in range(5):
            for first, second in itertools.combinations(slots,2):
                expected_pairs.append((f'{condition}-sample-{sample}-slot-{first}-{second}',
                                       'cross-run', [first,sample], [second,sample]))
    for slot in range(1,9):
        for sample in range(4):
            expected_pairs.append((f'slot-{slot}-temporal-{sample}-{sample+1}',
                                   'temporal', [slot,sample], [slot,sample+1]))
    got_pairs = [(r['id'],r['kind'],r['first'],r['second']) for r in comparison['pairs']]
    assert got_pairs == expected_pairs, (got_pairs[-4:], expected_pairs[-4:])
    frame_names = set()
    pair_reviews = []
    for row in comparison['pairs']:
        assert row['status'] == 'MEASURED'
        first_png, second_png = EXPERIMENT/row['first_png'], EXPERIMENT/row['second_png']
        frame_names.update([row['first_png'],row['second_png']])
        raw_a, raw_b = first_png.read_bytes(), second_png.read_bytes()
        assert sha(raw_a) == row['first_png_sha256'] and sha(raw_b) == row['second_png_sha256']
        with Image.open(first_png) as tmp:
            a = tmp.convert('RGBA')
        with Image.open(second_png) as tmp:
            b = tmp.convert('RGBA')
        assert a.size == b.size == (720,1280)
        bands = ImageChops.difference(a,b).split()
        mask = bands[0]
        for band in bands[1:]:
            mask = ImageChops.lighter(mask,band)
        changed_count = 720*1280 - mask.histogram()[0]
        compressed = (EXPERIMENT/row['difference_file']).read_bytes()
        expanded = gzip.decompress(compressed)
        d = row['difference']
        assert sha(compressed) == d['sha256'] and len(compressed) == d['bytes']
        assert sha(expanded) == d['expanded_sha256'] and len(expanded) == d['expanded_bytes']
        assert len(expanded) % 12 == 0
        records = list(struct.iter_unpack('>I4s4s',expanded))
        assert len(records) == changed_count == d['changed_pixels'] == 1
        prior = -1
        for index,rgba_a,rgba_b in records:
            assert prior < index < 720*1280
            point = (index % 720, index // 720)
            assert bytes(a.getpixel(point)) == rgba_a and bytes(b.getpixel(point)) == rgba_b
            assert rgba_a != rgba_b
            prior = index
        x_a = (EXPERIMENT/row['first_xml']).read_bytes()
        x_b = (EXPERIMENT/row['second_xml']).read_bytes()
        assert sha(x_a) == row['first_xml_sha256'] and sha(x_b) == row['second_xml_sha256']
        assert (x_a == x_b) == row['xml_bytes_equal'] is False
        assert canonical(ET.fromstring(x_a)) != canonical(ET.fromstring(x_b))
        assert row['xml_canonical_equal'] is False and row['png_bytes_equal'] is False
        pair_reviews.append({'id':row['id'],'changed_pixels':changed_count,
                             'record_count':len(records),'changed_index':records[0][0],
                             'xml_bytes_equal':False,'full_xml_tuple_equal':False,
                             'lossless_values_exact':True})
    assert len(frame_names) == 40 and len(pair_reviews) == 92
    assert len(comparison['indicator_arrays']) == 40
    for row in comparison['indicator_arrays']:
        assert row['parity_weight'] == 0 and row['used_as_mask'] is False
        check_row(EXPERIMENT,row['artifact'])
        with Image.open(EXPERIMENT/row['source_png']) as im:
            rgba = im.convert('RGBA')
        assert rgba.crop(tuple(row['bounds'])).tobytes() == (EXPERIMENT/row['artifact']['path']).read_bytes()
        for p in row['historical_coordinate_values']:
            assert list(rgba.getpixel((p['x'],p['y']))) == p['rgba']
    for key in ['full_runtime_1_to_1_established','animation_parity_established','cause_established',
                'crash_free_run_established','masks_used','cross_app_frame_selection','historical_results_rewritten']:
        assert comparison[key] is False
    assert comparison['new_runtime_parity_credit'] == 0
    save('independent-synthetic-pixel-records.json', {
        'source':str(EXPERIMENT),'synthetic_only':True,'application_or_android_execution':False,
        'frames_independently_decoded':40,'pairs_independently_checked':92,
        'cross_run_pairs':60,'temporal_pairs':32,'all_full_frames_720_by_1280':True,
        'all_pairs_unequal_rgba_and_full_xml':True,'all_lossless_records_exact':True,
        'all_40_additive_arrays_and_historical_values_exact':True,
        'positive_runtime_parity_credit':0,'pair_results':pair_reviews})
    print('Independently decoded forty synthetic frames and checked all ninety-two pair records',flush=True)

    offline_root = OLD/'reports/workflow-01'
    offline = load(offline_root/'result.json')
    assert offline['status'] == 'OFFLINE_WORKFLOW_INPUTS_AND_CLEANUP_PASSED'
    assert offline['command_count'] == len(offline['commands']) == 12
    assert offline['check_count'] == len(offline['checks']) == 5
    assert [c['returncode'] for c in offline['commands']] == [0]*10 + [7,1]
    for command in offline['commands']:
        assert command['timed_out'] is False
        for kind in ('stdout','stderr'):
            check_row(offline_root,command[kind])
    save('inspected-offline-commands.json', {
        'source_result':str(offline_root/'result.json'),'command_count':12,
        'command_rows':[{k:r[k] for k in ('label','argv','returncode','timeout_seconds','timed_out')}
                        for r in offline['commands']],
        'raw_streams_independently_rehashed':24,'new_commands_executed_by_review':0,
        'checked_prior_guard_count':5,'old_workflow_source_identity':offline['workflow']})
    assert source_inventory(SOURCE) == final_rows
    for name,path,expected in CAPSULES:
        assert ident(path)['sha256'] == expected, name
    return {'status':'INDEPENDENT_IMPLEMENTATION_REVIEW_PASSED',
            'final_checkpoint_sha256':CAPSULES[-1][2],
            'final_workflow_sha256':final_map[wf_rel]['sha256'],
            'capsules_verified':len(capsule_rows),
            'capsule_payload_rows_verified':sum(r['payload_count'] for r in capsule_rows),
            'final_capsule_payloads_verified':capsule_rows[-1]['payload_count'],
            'source_paths':16,'production_paths_unchanged':13,'changed_binding_paths':changed,
            'unchanged_other_test_asts':40,'inspected_full_attempt_passes':40,
            'inspected_focused_corrected_passes':1,'distinct_passed_test_bodies':41,
            'fresh_full_suite_executed':False,'android_executed':False,'app_build_executed':False,
            'new_runtime_parity_credit':0,'independent_synthetic_pair_checks':92,
            'concrete_blockers_found':[],'source_and_capsule_identities_unchanged':True,
            'approval_scope':'Exact inactive implementation is suitable for root activation review; actual device evidence remains pending.'}


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=False)
    start = time.monotonic_ns()
    receipt = {'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'argv':sys.argv,'python':str(Path(sys.executable).resolve()),
               'collector_source_identity':ident(Path(__file__).resolve()),
               'scope':'Read-only input/source/closed-evidence analysis; no suites, app code, Android, Git or network.',
               'started_monotonic_ns':start}
    try:
        result = main()
        code = 0
    except BaseException as error:
        result = {'status':'INDEPENDENT_REVIEW_ATTEMPT_FAILED','error_type':type(error).__name__,
                  'error':str(error),'traceback':traceback.format_exc(),
                  'source_modified':False,'app_or_android_executed':False}
        traceback.print_exc()
        code = 1
    receipt.update(returncode=code,finished_monotonic_ns=time.monotonic_ns(),
                   finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save('execution.json',receipt)
    save('result.json',result)
    print(json.dumps(result,indent=2),flush=True)
    raise SystemExit(code)
