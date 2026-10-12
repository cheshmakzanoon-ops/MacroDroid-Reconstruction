#!/usr/bin/env python3
"""Verify only the closed assertion correction and its derived source pins."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import shutil
import sys
import yaml

ROOT = Path(__file__).resolve().parent
NEW = ROOT / 'source'
OLD = ROOT / 'reports/attempt-02/source'
OUT = ROOT / 'reports/final-binding-04'
OUT.mkdir(parents=True, exist_ok=False)
shutil.copy2(__file__, OUT / 'verify_final_source_binding.py')
sys.dont_write_bytecode = True
sys.path.insert(0, str(NEW / 'tools/indicator_sampling'))
import common as c
import prepare


def identity(path):
    return c.file_identity(path)


rows, changed, patch = [], [], []
for path in sorted(NEW.rglob('*')):
    if not path.is_file():
        continue
    name = path.relative_to(NEW).as_posix()
    prior = OLD / name
    row = {'path': name, 'before': identity(prior), 'after': identity(path)}
    rows.append(row)
    if row['before'] != row['after']:
        changed.append(name)
        patch.extend(difflib.unified_diff(prior.read_text().splitlines(True), path.read_text().splitlines(True),
            fromfile='attempt-02/' + name, tofile='final/' + name))
test = 'tools/indicator_sampling/test_indicator_sampling.py'
manifest = 'tools/indicator_sampling/runtime-files.json'
workflow = prepare.WORKFLOW
assert changed == sorted([test, manifest, workflow]), changed
old_test, new_test = (OLD / test).read_text(), (NEW / test).read_text()
old_assertion = "self.rejected('Local APK')"
new_assertion = "self.rejected('Slot local APK read differs from its fixed input')"
assert old_test.count(old_assertion) == 1
assert old_test.replace(old_assertion, new_assertion, 1) == new_test
assert (OLD / workflow).read_text().replace(identity(OLD / test)['sha256'], identity(NEW / test)['sha256'], 1) == (NEW / workflow).read_text()
own = prepare.source_manifest(NEW)
assert len(own) == 16
data = yaml.load((NEW / workflow).read_text(), Loader=yaml.BaseLoader)
steps = data['jobs']['fixed-sampling']['steps']
python_source = steps[2]['run'].split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
tree = ast.parse(python_source)
pins = next(ast.literal_eval(node.value) for node in tree.body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == 'expected')
assert pins == dict(sorted({'tools/indicator_sampling/' + name: identity(NEW / 'tools/indicator_sampling' / name)
                           for name in prepare.OWN_FILES}.items()))
assert 'timeout 900s python3' in steps[3]['run']
assert data['jobs']['fixed-sampling']['timeout-minutes'] == '150'
for index, step in enumerate(steps):
    old_step = yaml.load((OLD / workflow).read_text(), Loader=yaml.BaseLoader)['jobs']['fixed-sampling']['steps'][index]
    if index != 2:
        assert step == old_step, index
baseline = c.json_file(ROOT / 'reports/attempt-02/host-evidence/complete-synthetic-baseline/experiment/comparison.json')
assert baseline['evidence_complete'] is True and baseline['measured_pairs'] == 92
assert len(baseline['pairs']) == 92 and len(baseline['indicator_arrays']) == 40
assert all(row['difference']['changed_pixels'] == 1 and row['xml_canonical_equal'] is False for row in baseline['pairs'])
log = (ROOT / 'reports/attempt-02/stderr.log').read_text()
successes = [line for line in log.splitlines() if line.startswith('test_') and line.endswith(' ... ok')]
failures = [line for line in log.splitlines() if line.startswith('test_') and line.endswith(' ... FAIL')]
assert len(successes) == 40 and len(failures) == 1 and 'Ran 41 tests' in log
assert 'test_changed_local_apk_identity_rejects_before_any_capture_credit' in failures[0]
result = {'status': 'FINAL_SOURCE_CHANGE_LIMITED_TO_TEST_ASSERTION_AND_DERIVED_PINS',
    'changed_paths': changed, 'all_production_source_and_fixed_inputs_unchanged': True,
    'full_host_attempt': {'tests_run': 41, 'passed': 40, 'failed_assertions': 1,
                          'timed_out': False, 'literal_status_preserved': 'FAILED'},
    'complete_recorder_produced_synthetic_dataset': {'slots': 8, 'post_input_frames': 40, 'pairs': 92,
        'every_pair_one_rgba_difference_and_unequal_canonical_xml': True,
        'independent_literal_replay_test_passed': True},
    'final_runtime_manifest': identity(NEW / manifest), 'final_workflow': identity(NEW / workflow),
    'final_fresh_full_suite_locally_reexecuted': False, 'android_executed': False,
    'production_or_workflow_timeout_changed': False, 'new_runtime_parity_credit': 0}
c.write_json(OUT / 'source-delta.json', rows)
(OUT / 'source-delta.patch').write_text(''.join(patch))
c.write_json(OUT / 'required-final-source.json', own)
c.write_json(OUT / 'actual-full-attempt-test-names.json', {'passed': successes, 'failed': failures})
c.write_json(OUT / 'result.json', result)
print(json.dumps(result, indent=2))
