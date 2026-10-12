#!/usr/bin/env python3
"""Exercise the corrected assertion against the closed actual synthetic trace.

The recorder is not run again. The final test body imports the same byte-exact
production modules as the closed attempt, retaining that attempt's original
runtime-manifest context. This is a focused verifier/test assertion check, not a
new full-source workflow/preparation claim.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'reports/attempt-02'
FINAL = ROOT / 'source/tools/indicator_sampling'
OUTPUT = ROOT / 'reports/focused-03'
OUTPUT.mkdir(parents=True, exist_ok=False)
shutil.copy2(__file__, OUTPUT / 'run_focused_correction.py')
shutil.copy2(FINAL / 'test_indicator_sampling.py', OUTPUT / 'executed-test_indicator_sampling.py')
BASE = OLD / 'host-evidence/complete-synthetic-baseline'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def inventory(root):
    return [{'path': p.relative_to(root).as_posix(), **identity(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


source_before, baseline_before = inventory(ROOT / 'source'), inventory(BASE)
save(OUTPUT / 'final-source-before.json', source_before)
save(OUTPUT / 'closed-baseline-before.json', baseline_before)
old_source = OLD / 'source/tools/indicator_sampling'
binding = []
for name in ('common.py', 'prepare.py', 'record.py', 'verify.py', 'pins.json', 'protocol.json',
             'historical-coordinates.json'):
    assert identity(old_source / name) == identity(FINAL / name), name
    binding.append({'path': name, 'old_executed': identity(old_source / name), 'final': identity(FINAL / name)})
save(OUTPUT / 'unchanged-production-binding.json', binding)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['INDICATOR_PARENTS'] = str(ROOT / 'parent-inputs')
os.environ['INDICATOR_HOST_EVIDENCE'] = str(OUTPUT / 'host-evidence')
sys.dont_write_bytecode = True
sys.path[:0] = [str(old_source)]
spec = importlib.util.spec_from_file_location('indicator_final_focused_test', FINAL / 'test_indicator_sampling.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cls = module.SyntheticTraceControls


def reuse_closed_fixture(klass):
    klass.baseline = BASE
    klass.result = json.loads((BASE / 'experiment/comparison.json').read_bytes())


cls.setUpClass = classmethod(reuse_closed_fixture)
case = 'test_changed_local_apk_identity_rejects_before_any_capture_credit'
suite = unittest.TestSuite([cls(case)])
report = {'scope': 'One final corrected test body against the closed Recorder-produced synthetic trace and byte-unchanged verifier.',
          'closed_fixture': str(BASE), 'closed_fixture_runtime_manifest': identity(old_source / 'runtime-files.json'),
          'test_body_source': identity(FINAL / 'test_indicator_sampling.py'),
          'new_recorder_capture_executed': False, 'android_executed': False,
          'new_full_source_preparation_or_workflow_claimed': False,
          'setUpClass_override': 'Reuse the exact closed attempt-02 baseline only; no new device executor.',
          'started_monotonic_ns': time.monotonic_ns()}
with (OUTPUT / 'unittest.log').open('x') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
report.update(finished_monotonic_ns=time.monotonic_ns(), tests_run=result.testsRun,
              failures=len(result.failures), errors=len(result.errors))
baseline_after, source_after = inventory(BASE), inventory(ROOT / 'source')
save(OUTPUT / 'closed-baseline-after.json', baseline_after)
save(OUTPUT / 'final-source-after.json', source_after)
report['closed_baseline_unchanged'] = baseline_before == baseline_after
report['final_source_unchanged'] = source_before == source_after
report['literal_original_case_base_note'] = 'The test tearDown retains its usual ../complete-synthetic-baseline/experiment note. For this focused followup only, resolve the baseline through this wrapper\'s exact closed_fixture and complete before/after inventories.'
report['status'] = 'FOCUSED_ASSERTION_CORRECTION_PASSED' if result.wasSuccessful() and all(
    report[name] for name in ('closed_baseline_unchanged', 'final_source_unchanged')) else 'FOCUSED_ASSERTION_CORRECTION_FAILED'
save(OUTPUT / 'result.json', report)
print(json.dumps({key: report[key] for key in ('status', 'tests_run', 'failures', 'errors',
    'closed_baseline_unchanged', 'final_source_unchanged')}, indent=2))
