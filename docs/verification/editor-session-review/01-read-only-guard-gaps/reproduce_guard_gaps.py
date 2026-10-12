"""Read-only review of pinned external session guards using synthetic artifacts.

This script neither executes Android nor edits repository inputs. A successful
mutation records a comparator false positive; it is not app-parity evidence.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
OUT = ROOT / 'editor-session-review'
SOURCE = REPO / 'tools/parity_journeys'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCE))
import test_post_onboarding as tests

names = ['tools/parity_journeys/post_onboarding.py',
         'tools/parity_journeys/editor_session_journey.py',
         'tools/parity_journeys/test_post_onboarding.py',
         'tools/parity_journeys/editor_journey.py',
         'tools/parity_journeys/test_editor_journey.py',
         'tools/parity_journeys/supplied_reference_journey.py',
         'tools/parity_journeys/robust_capture.py',
         'tools/parity_journeys/editor-plan.json',
         'project/android_compare.py']
inputs = {}
for name in names:
    data = (REPO / name).read_bytes()
    assert data == subprocess.check_output(['git', 'show', '934c6543dce0897975f52457717b3a70bd27ce00:' + name], cwd=REPO), name
    inputs[name] = hashlib.sha256(data).hexdigest()
    dest = OUT / 'inputs' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)

def run_case(name, mutate, expected_equal):
    fixture = tests.SessionTests('test_exact_session_does_not_turn_shared_startup_restart_into_a_pass')
    fixture.setUp()
    try:
        baseline = fixture.result()
        assert baseline['editor_session_equal'] is True, baseline
        description = mutate(fixture)
        result = fixture.result()
        assert result['editor_session_equal'] is expected_equal, (name, result)
        folder = OUT / 'cases' / name
        folder.mkdir(parents=True, exist_ok=False)
        shutil.copytree(fixture.root, folder / 'artifacts')
        (folder / 'report.json').write_text(json.dumps(fixture.report, indent=2) + '\n')
        (folder / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        record = dict(name=name, description=description, baseline_accepted=True,
                      mutated_editor_session_equal=result['editor_session_equal'],
                      mutated_status=result['status'], reason=result.get('reason'),
                      false_positive=expected_equal,
                      synthetic_only=True, android_executed=False)
        (folder / 'mutation.json').write_text(json.dumps(record, indent=2) + '\n')
        return record
    finally:
        fixture.doCleanups()

def endpoint_reuse(f):
    run = f.report['runs'][1]
    initial, final = run['screens'][f.start], run['screens'][-1]
    # The recorded final endpoint evidence is physically absent in this mutant.
    for key in ('package_path', 'checksum', 'pid', 'foreground'):
        for stream in ('stdout', 'stderr'):
            (f.root / final['session_identity'][key][stream]['path']).unlink()
    final['session_identity'] = copy.deepcopy(initial['session_identity'])
    return 'All eight final endpoint command-output files removed; final session_identity reuses the complete start identity, yet the session passes.'

def preinput_reuse(f):
    run = f.report['runs'][1]
    first, later = run['transitions'][f.start], run['transitions'][f.start + 1]
    for row in later['preinput_artifacts'].values():
        (f.root / row['path']).unlink()
    later['preinput_artifacts'] = copy.deepcopy(first['preinput_artifacts'])
    return 'A later input has no own immediate PID/foreground output files and instead reuses the prior input pair; the session passes.'

def preinput_resolved_alias_reuse(f):
    run = f.report['runs'][1]
    first, later = run['transitions'][f.start], run['transitions'][f.start + 1]
    (f.root / 'candidate-reused').mkdir()
    for key, row in list(first['preinput_artifacts'].items()):
        data = (f.root / row['path']).read_bytes()
        fresh = f.fixture.put('candidate-reused/' + key + '.txt', data)
        first['preinput_artifacts'][key] = fresh
        (f.root / later['preinput_artifacts'][key]['path']).unlink()
        aliased = copy.deepcopy(fresh)
        aliased['path'] = 'candidate-reused/./' + key + '.txt'
        later['preinput_artifacts'][key] = aliased
        assert (f.root / fresh['path']).resolve() == (f.root / aliased['path']).resolve()
    return 'The same missing-later-input evidence is reused through valid ./ aliases of the prior input files; the session passes.'

def wrong_endpoint_digest(f):
    run = f.report['runs'][1]
    final = run['screens'][-1]['session_identity']
    final['checksum']['stdout'] = f.put(run, 'review-wrong-endpoint-sha',
        ('f' * 64 + '  /data/app/test/base.apk\n').encode())
    return 'Control: a wrong final installed APK digest is rejected, confirming the synthetic baseline exercises endpoint validation.'

results = [run_case('endpoint-identity-reuse', endpoint_reuse, True),
           run_case('preinput-evidence-reuse', preinput_reuse, True),
           run_case('preinput-resolved-alias-reuse', preinput_resolved_alias_reuse, True),
           run_case('wrong-endpoint-digest-control', wrong_endpoint_digest, False)]
assert inputs == {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest() for name in names}
summary = dict(reviewed_external_commit='934c6543dce0897975f52457717b3a70bd27ce00',
               source_inputs=inputs, source_inputs_unchanged=True, cases=results,
               android_executed=False, active_files_modified=False,
               full_runtime_1_to_1_established=False)
(OUT / 'guard-review.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
