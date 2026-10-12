from __future__ import annotations

import ast
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform
import shutil
import stat
import sys
import tarfile

from run_checkout_attempt import ROOT, inventory

RAW_ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/combined-run-38245093369')
PARENT = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls')


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(path.stat().st_mode)}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def copy_file(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination); destination.chmod(stat.S_IMODE(source.stat().st_mode))
    assert identity(source) == identity(destination)


def main():
    out = ROOT / 'checkpoints/01-checkout-layout-controls'; out.mkdir(parents=True, exist_ok=False)
    current = ROOT / 'stage-01/repository'; sources = inventory(current)
    results = {name: json.loads((ROOT / 'reports' / name / 'result.json').read_bytes()) for name in (
        '01-original-count-failure', '02-original-count-failure-reproduced',
        '03-focused-layout-controls', '04-complete-155-controls')}
    assert results['01-original-count-failure']['tests_executed'] == 0
    assert all(results[name]['passed'] for name in results if name != '01-original-count-failure')
    assert results['04-complete-155-controls']['observed_tests'] == 155
    assert results['02-original-count-failure-reproduced']['returncode'] == 1
    derivation = json.loads((ROOT / 'stage-01/derivation.json').read_bytes())
    assert sources == derivation['source_after']
    for relative, row in sources.items():
        copy_file(current / relative, out / 'source' / relative)
        copy_file(PARENT / 'source' / relative, out / 'parent-source' / relative)
    for path in sorted((ROOT / 'stage-01').iterdir()):
        if path.is_file(): copy_file(path, out / 'review' / path.name)
    for name in ('prepare_successor.py', 'run_checkout_attempt.py', 'freeze_successor.py'):
        copy_file(ROOT / name, out / 'producers' / name)
    copy_file(PARENT / 'checkpoint.json', out / 'review/parent-4447-checkpoint.json')
    raw = RAW_ROOT / 'extracted'
    zip_identity = identity(RAW_ROOT / 'artifact.zip')
    assert zip_identity['bytes'] == 4960179
    assert zip_identity['sha256'] == 'cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833'
    raw_before = inventory(raw, single_link=False)
    assert len(raw_before) == 4355
    for relative in ('hosted-tool-host-tests.log', 'hosted-proof/verification.json', 'hosted-tool-source-verification.json'):
        copy_file(raw / relative, out / 'review/actual-hosted-failure' / relative)
    copy_file(Path('/dev/shm/macrodroid-day-lookup-integration/combined-hosted-run-38245093369/job-observation.json'),
              out / 'review/actual-hosted-failure/job-observation.json')
    for path in sorted(RAW_ROOT.iterdir()):
        if path.is_file() and path.suffix == '.json':
            copy_file(path, out / 'review/actual-hosted-failure' / path.name)
    with gzip.GzipFile(filename=str(out / 'review/actual-hosted-failure/raw-inventory.json.gz'), mode='wb', mtime=0) as stream:
        stream.write((json.dumps(raw_before, indent=2, sort_keys=True) + '\n').encode())
    raw_log = (raw / 'hosted-tool-host-tests.log').read_text()
    assert 'Ran 153 tests in 3.961s' in raw_log and 'AssertionError: 9 != 56' in raw_log
    assert raw_log.count('\nFAIL: ') == 1 and raw_log.rstrip().endswith('FAILED (failures=1)')
    assert json.loads((raw / 'hosted-proof/verification.json').read_bytes())['passed'] is False
    runtime = {'schema': 1, 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'python': sys.version, 'executable': sys.executable, 'resolved_executable': str(Path(sys.executable).resolve()),
               'binary': identity(Path(sys.executable).resolve()), 'platform': platform.platform(),
               'observation_phase': 'After all closed local checkout controls; argv paths are recorded in each attempt'}
    write(out / 'review/runtime-observation.json', runtime)
    write(out / 'review/closed-results.json', results)
    evidence = []
    for path in sorted((ROOT / 'reports').rglob('*')):
        if path.is_dir(): continue
        status = path.lstat(); assert stat.S_ISREG(status.st_mode) and status.st_nlink == 1, str(path)
        relative = str(path.relative_to(ROOT / 'reports'))
        evidence.append((relative, path, identity(path)))
        if path.parent.parent == ROOT / 'reports' and path.suffix in ('.json', '.log', '.txt'):
            copy_file(path, out / 'reports' / relative)
    write(out / 'evidence-inventory.json', [{'path': relative, **row} for relative, path, row in evidence])
    with (out / 'evidence.tar.gz').open('xb') as compressed:
        with gzip.GzipFile(filename='', fileobj=compressed, mode='wb', mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w|') as archive:
                for relative, path, row in evidence:
                    data = path.read_bytes(); assert identity(path) == row
                    info = tarfile.TarInfo(relative); info.mode = row['mode']; info.size = len(data); info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))
    with tarfile.open(out / 'evidence.tar.gz', 'r:gz') as archive:
        members = archive.getmembers()
        assert [row.name for row in members] == [relative for relative, path, row in evidence]
        for member, (relative, path, row) in zip(members, evidence):
            data = archive.extractfile(member).read()
            assert member.isfile() and member.mode == row['mode'] and len(data) == row['bytes']
            assert hashlib.sha256(data).hexdigest() == row['sha256']
    assert inventory(raw, single_link=False) == raw_before
    assert inventory(current) == sources
    preservation = {'schema': 1, 'actual_run_id': 38245093369, 'actual_job_id': 114796870050,
        'actual_head_sha': '59df96186fefb2bf883031c09562af08b48bde16', 'actual_artifact_id': 11744651182,
        'actual_artifact': zip_identity, 'all_4355_downloaded_raw_files_unchanged': True,
        'actual_hosted_tooling_tests': 153, 'actual_hosted_successes': 152, 'actual_hosted_failures': 1,
        'actual_hosted_failure_is_preserved_as_failure': True, 'actual_application_stages_skipped': True,
        'all_nine_original_tooling_source_bytes_equal_parent_4447': True,
        'local_original_targeted_test_failure_reproduced': True,
        'corrected_focused_tests_passed': 6, 'corrected_full_distinct_tooling_tests_passed': 155,
        'unchanged_prior_test_bodies': 152, 'new_checkout_controls': 2,
        'whole_checkout_metadata_preserved_and_not_used_as_runtime_scope': True,
        'production_inputs_prepare_run_verify_pins_readme_unchanged': True,
        'application_executions': 0, 'android_runtime_executed': False,
        'active_source_changed': False, 'active_workflow_changed': False}
    write(out / 'review/preservation.json', preservation)
    readme = '''# Combined hosted tooling: checkout scope correction

This inactive successor corrects one authored tooling test. Actual hosted run
38245093369 at59df961 executed153 tests in3.961 seconds:152 passed and exactly one
failed. The failed assertion counted every file beneath the checkout root and
expected nine; the real checkout contained56. The runtime verifier had already
accepted the seven exact runtime siblings before that unrelated whole-root count
failed. Physical source preparation and all sixteen application gates were
skipped. The later missing preparation report is a consequence of that skip.
The original job result is preserved as a failure; no APK or app parity passed.

## Exact change

Only three of the nine job paths change: test_day_trigger_acceptance.py, its
runtime-files.json byte/hash row, and the workflow's manifest hash literal. The
production inputs.py, prepare.py, run_acceptance.py, verify.py, pins.json and
README.md remain byte-for-byte identical to4447 and the actual archived runtime.
No recorder, cleanup, command argv, timeout, source-stage verification, numeric or
lookup proof, application count, or acceptance semantics is altered.

The corrected test derives the nine declared paths from the exact seven runtime
rows, manifest and workflow, requires the literal nine-path set, and validates
those regular files within the checkout. The unchanged production runtime
verifier still requires the exact complete sibling inventory. Unrelated root
documentation or Git-style metadata is outside that explicitly owned job scope;
it is preserved, not removed, masked or included in app parity.

Two new named controls copy the actual nine source files into a private checkout
with unrelated root documentation and inert Git-style metadata. That fixture is
accepted unchanged. Adding an undeclared runtime sibling is rejected by the
unchanged production runtime inventory guard. The corrected full corpus is155
distinct tests: all prior153 test identities remain, only the faulty body changed,
and two additional controls were added; the other152 test bodies are AST-exact.

## Actual closed local attempts

01 stopped before any test because the collector unnecessarily required the
immutable read-only parent's hardlinked payload to have one link. Its traceback
and exact wrapper remain. The collector now permits immutable source aliases
while requiring every newly copied executed file to have a single link. It never
mutates the parent source.

02 executes the old four workflow tests against a real56-file private layout:
nine exact old source files plus47 explicitly synthetic unrelated files. The
original9-versus56 assertion alone fails exactly, and the whole layout is retained
unchanged. This reproduces the count assumption, not the original host's unknown
metadata file contents, and is not a successful original tooling gate.

03 executes the six corrected workflow/layout tests successfully. 04 executes
the entire155-test corrected corpus successfully, including the inherited92
numeric controls and all lookup controls. Both execute in the same kind of
populated56-file private layout and verify all source and metadata bytes before
and after. Focused repeated tests are not added again to the155 distinct count.

The complete local attempts, fixtures, command streams and source snapshots are
in the exact evidence archive. The actual hosted ZIP is reused from the sole
publisher download, identified in review/preservation.json; all4355 extracted
files were rehashed unchanged. Its failure log, verifier result, source report,
job observations and raw inventory are included as review copies. The complete
raw ZIP remains a separate durable publication under
docs/verification/day-trigger-hosted-run-59df961.

This capsule proposes a fresh hosted rerun after independent review and exact
three-path publication. It does not change the active application, register a
method, build/sign an APK, execute Android, or establish full-host app acceptance.
'''
    (out / 'README.md').write_text(readme)
    direct = [{'path': str(path.relative_to(out)), **identity(path)} for path in sorted(out.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'TEST_ONLY_CHECKOUT_LAYOUT_SUCCESSOR_155_CONTROLS_PASSED_INACTIVE',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'repo_target': 'work-in-progress/day-trigger-lookup/13-checkout-layout-controls',
        'parent_checkpoint_sha256': '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88',
        'actual_failed_run_id': 38245093369, 'actual_failed_artifact': zip_identity,
        'source_files': 9, 'changed_paths': derivation['changed_paths'],
        'tooling_tests_passed': 155, 'inherited_tooling_tests': 92, 'application_executions': 0,
        'full_host_acceptance_executed': False, 'android_runtime_executed': False,
        'active_source_changed': False, 'active_workflow_changed': False,
        'runtime_manifest': identity(current / 'tools/day_trigger_acceptance/runtime-files.json'),
        'workflow': identity(current / '.github/workflows/day-trigger-wip-acceptance.yml'),
        'evidence_file_count': len(evidence), 'evidence_archive': identity(out / 'evidence.tar.gz'), 'files': direct}
    write(out / 'checkpoint.json', checkpoint)
    print(json.dumps({'path': str(out / 'checkpoint.json'), **identity(out / 'checkpoint.json'),
                      'files': len(direct), 'evidence_file_count': len(evidence), 'evidence_archive': checkpoint['evidence_archive']}))


if __name__ == '__main__':
    main()
