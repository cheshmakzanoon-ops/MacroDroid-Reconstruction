"""Review the frozen numeric verifier through nine selected synthetic controls."""
from pathlib import Path
import datetime
import hashlib
import importlib
import io
import json
import os
import shutil
import stat
import sys
import time
import unittest

CAPSULE = Path('/dev/shm/day-numeric-hosted-01/checkpoints/01-hosted-wip-acceptance')
EXPECTED = '994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473'
ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/day-numeric-final-boundary-review')
ROOT.mkdir(exist_ok=False)
(ROOT / 'tmp').mkdir()
os.environ['TMPDIR'] = str(ROOT / 'tmp')
sys.dont_write_bytecode = True

def identity(path):
    value = path.lstat()
    assert stat.S_ISREG(value.st_mode)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'mode': stat.S_IMODE(value.st_mode)}

def write(name, value):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
raw = (CAPSULE / 'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
checkpoint = json.loads(raw)
assert len(checkpoint['files']) == 155
before = []
for row in checkpoint['files']:
    got = identity(CAPSULE / row['path'])
    assert got == {'bytes': row['bytes'], 'sha256': row['sha256'], 'mode': int(row['mode'], 8) & 0o777}
    before.append({'path': row['path'], **got})
write('evidence/capsule-before.json', before)
shutil.copyfile(CAPSULE / 'checkpoint.json', ROOT / 'reviewed-checkpoint.json')
for row in checkpoint['active_files']:
    source = CAPSULE / row['source']
    target = ROOT / 'reviewed-source' / row['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    target.chmod(int(row['mode'], 8) & 0o777)
    assert identity(target) == identity(source)

sys.path.insert(0, str(ROOT / 'reviewed-source/tools/day_numeric_acceptance'))
tests = importlib.import_module('test_day_numeric_acceptance')
old_teardown = tests.OwnedTemporary.tearDown
retained = []

def preserve_teardown(self):
    prefix = 'synthetic/' + self.__class__.__name__ + '/' + self._testMethodName
    observations = {'scope': 'Synthetic verifier boundary only; no Java, D8 or Android executed',
                    'original_temporary_root': str(self.root), 'files': []}
    for name in ('report', 'execution', 'prepared', 'folder', 'java', 'start', 'end'):
        if hasattr(self, name):
            value = getattr(self, name)
            observations[name] = str(value) if isinstance(value, Path) else value
    for path in sorted(self.root.rglob('*')):
        if path.is_dir():
            continue
        st = path.lstat()
        assert stat.S_ISREG(st.st_mode)
        relative = path.relative_to(self.root).as_posix()
        destination = ROOT / prefix / 'files' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        destination.chmod(stat.S_IMODE(st.st_mode))
        observations['files'].append({'path': relative, **identity(path),
                                     'device': st.st_dev, 'inode': st.st_ino, 'nlink': st.st_nlink,
                                     'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns})
    write(prefix + '/observations.json', observations)
    retained.append({'test': self.id(), 'observation_path': prefix + '/observations.json',
                     'retained_files': len(observations['files'])})
    old_teardown(self)

tests.OwnedTemporary.tearDown = preserve_teardown
names = [
    'NumericCommandControls.test_exact_seventeen_synthetic_command_rows_preserve_thirty_four_distinct_streams',
    'NumericCommandControls.test_retained_streams_cannot_make_bin_true_a_d8_command',
    'NumericCommandControls.test_missing_runtime_flag_rejects_with_unchanged_positive_streams',
    'NumericCommandControls.test_different_config_and_result_roles_reject',
    'NumericCommandControls.test_boolean_argv_element_rejects',
    'NumericCommandControls.test_physical_numeric_stream_alias_rejects_even_with_matching_hashes',
    'WrapperStreamControls.test_exact_synthetic_child_stream_roles_and_intervals_are_accepted',
    'WrapperStreamControls.test_java_version_streams_cannot_replace_acceptance_streams',
    'WrapperStreamControls.test_dot_alias_does_not_create_a_new_acceptance_stream_role',
]
suite = unittest.TestSuite(tests.__dict__[name.split('.')[0]](name.split('.')[1]) for name in names)
stream = io.StringIO()
t0 = time.perf_counter()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
elapsed = time.perf_counter() - t0
(ROOT / 'test-output.log').write_text(stream.getvalue())
after = [{'path': row['path'], **identity(CAPSULE / row['path'])} for row in checkpoint['files']]
write('evidence/capsule-after.json', after)
assert before == after and hashlib.sha256((CAPSULE / 'checkpoint.json').read_bytes()).hexdigest() == EXPECTED
outcome = {
    'schema': 1,
    'status': 'NARROW_CORRECTED_BOUNDARY_REVIEW_PASSED' if result.wasSuccessful() else 'NARROW_CORRECTED_BOUNDARY_REVIEW_FAILED',
    'passed': result.wasSuccessful(), 'started_utc': started,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Nine selected synthetic verifier regressions; not full hosted acceptance or Android evidence',
    'checkpoint_sha256': EXPECTED, 'capsule_files_rehashed_before_and_after': len(before),
    'frozen_capsule_unchanged': before == after,
    'old_counterexample_commit': '01a36663c9455a1192fedd3d1cade2c090561e59',
    'old_counterexample_checkpoint_sha256': '17528d34bb9475e7bd0e666500ff5111847aaf2e547c8c31677cd2d514f2f0d3',
    'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'skipped': len(result.skipped), 'elapsed_seconds': elapsed,
    'selected_tests': names, 'retained_synthetic_observations': retained,
    'test_adaptation': 'Only teardown copied actual synthetic artifacts before normal cleanup; production source and test methods unchanged',
    'application_source_changed': False, 'java_or_d8_executed': False, 'android_executed': False,
    'full_host_acceptance_executed': False, 'runtime_parity_established': False,
}
write('result.json', outcome)
shutil.copyfile(Path(__file__), ROOT / Path(__file__).name)
print(json.dumps(outcome))
raise SystemExit(0 if result.wasSuccessful() else 2)
