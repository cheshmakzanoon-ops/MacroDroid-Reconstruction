#!/usr/bin/env python3
"""Independent byte, source-delta and literal-result review of the checkout correction."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tarfile
import traceback
import zipfile

BASE = Path('/dev/shm/macrodroid-day-lookup-checkout-fix')
CAP = BASE / 'checkpoints/01-checkout-layout-controls'
OUT = BASE / 'root-review-02'
PARENT = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls')
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/combined-run-38245093369/artifact.zip')


def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    assert (info.st_size, info.st_mtime_ns, info.st_ino, info.st_dev) == (after.st_size, after.st_mtime_ns, after.st_ino, after.st_dev)
    return {'bytes': after.st_size, 'sha256': digest, 'mode': stat.S_IMODE(after.st_mode)}


def read(path):
    return json.loads(path.read_bytes())


def save(name, value):
    with (OUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def methods(path):
    text = path.read_text()
    return {c.name + '.' + n.name: ast.get_source_segment(text, n)
            for c in ast.parse(text).body if isinstance(c, ast.ClassDef)
            for n in c.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}


def literal_successes(text, hosted=False):
    names = re.findall(r'^test_\S+ \(([^)]+)\) \.\.\. ok$', text, re.M)
    name = 'test_day_trigger_acceptance.JavaObservationFailureControls.test_zero_exit_with_evidence_error_stops_before_long_acceptance_child'
    if name in text:
        exact = ('test_zero_exit_with_evidence_error_stops_before_long_acceptance_child (' + name
                 + ') ... HOST ACCEPTANCE WRAPPER FAILED: Java toolchain observation failed\n'
                 + ('HOST_ACCEPTANCE_NOT_COMPLETED\n' if hosted else '') + 'ok\n')
        assert text.count(exact) == 1 and name not in names
        names.append(name)
    return names


def main():
    OUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-review.py')
    shutil.copytree(BASE / 'root-review-01', OUT / 'prior-review-attempt-01')
    shutil.copyfile(BASE / 'review-log-format-correction.patch', OUT / 'review-log-format-correction.patch')
    shutil.copyfile(BASE / 'review-log-format-correction.json', OUT / 'review-log-format-correction.json')
    before = {}
    result = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'android_executed': False, 'application_executed': False, 'new_tooling_suite_executed': False}
    try:
        expected = {'bytes': 14829, 'sha256': '79d1895420bedcc3a28463f55ba989ecf0c460e72d683787395caad078d7767b', 'mode': 420}
        before[str(CAP / 'checkpoint.json')] = identity(CAP / 'checkpoint.json')
        assert before[str(CAP / 'checkpoint.json')] == expected
        cp = read(CAP / 'checkpoint.json')
        assert len(cp['files']) == 66 and cp['tooling_tests_passed'] == 155
        assert cp['active_source_changed'] is False and cp['application_executions'] == 0
        assert {p.relative_to(CAP).as_posix() for p in CAP.rglob('*') if p.is_file()} == {row['path'] for row in cp['files']} | {'checkpoint.json'}
        for row in cp['files']:
            path = CAP / row['path']; before[str(path)] = identity(path)
            assert before[str(path)] == {k: row[k] for k in ('bytes', 'sha256', 'mode')}, row['path']
        before[str(PARENT / 'checkpoint.json')] = identity(PARENT / 'checkpoint.json')
        assert before[str(PARENT / 'checkpoint.json')]['sha256'] == '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88'
        assert (PARENT / 'checkpoint.json').read_bytes() == (CAP / 'review/parent-4447-checkpoint.json').read_bytes()
        source, parent = {}, {}
        for row in read(PARENT / 'checkpoint.json')['files']:
            if not row['path'].startswith('source/'):
                continue
            name = row['path'][7:]
            p = PARENT / row['path']; before[str(p)] = identity(p)
            parent[name] = before[str(p)]
            assert parent[name] == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
            assert identity(CAP / 'parent-source' / name) == parent[name]
            source[name] = identity(CAP / 'source' / name)
        assert len(source) == len(parent) == 9
        changed = sorted(name for name in source if source[name] != parent[name])
        assert changed == ['.github/workflows/day-trigger-wip-acceptance.yml', 'tools/day_trigger_acceptance/runtime-files.json', 'tools/day_trigger_acceptance/test_day_trigger_acceptance.py']
        test = 'tools/day_trigger_acceptance/test_day_trigger_acceptance.py'
        old, new = methods(CAP / 'parent-source' / test), methods(CAP / 'source' / test)
        assert len(old) == 153 and len(new) == 155 and set(old) < set(new)
        modified = [name for name in old if old[name] != new[name]]
        assert modified == ['CombinedWorkflowControls.test_workflow_runtime_pin_binds_all_seven_actual_runtime_siblings']
        assert sorted(set(new) - set(old)) == [
            'CombinedCheckoutLayoutControls.test_extra_runtime_sibling_is_rejected_even_with_allowed_checkout_metadata',
            'CombinedCheckoutLayoutControls.test_unrelated_root_and_git_style_metadata_do_not_change_the_nine_path_scope']
        manifest_name = 'tools/day_trigger_acceptance/runtime-files.json'
        runtime = read(CAP / 'source' / manifest_name)
        assert len(runtime['files']) == 7
        for row in runtime['files']:
            assert source['tools/day_trigger_acceptance/' + row['path']] == {**{k: row[k] for k in ('bytes', 'sha256')}, 'mode': 420}
        prior_runtime = read(CAP / 'parent-source' / manifest_name)
        for row in prior_runtime['files']:
            if row['path'] == 'test_day_trigger_acceptance.py':
                row.update({k: source[test][k] for k in ('bytes', 'sha256')})
        assert prior_runtime == runtime
        workflow_name = '.github/workflows/day-trigger-wip-acceptance.yml'
        prior_workflow = (CAP / 'parent-source' / workflow_name).read_text()
        assert prior_workflow.count(parent[manifest_name]['sha256']) == 1
        assert prior_workflow.replace(parent[manifest_name]['sha256'], source[manifest_name]['sha256'], 1) == (CAP / 'source' / workflow_name).read_text()
        inventory = read(CAP / 'evidence-inventory.json')
        assert len(inventory) == 4600
        expected_members = {row['path']: row for row in inventory}; assert len(expected_members) == 4600
        observed = {}
        with tarfile.open(CAP / 'evidence.tar.gz', 'r:gz') as archive:
            for member in archive:
                assert member.isfile() and member.name not in observed and member.name in expected_members
                assert not PurePosixPath(member.name).is_absolute() and '..' not in PurePosixPath(member.name).parts
                with archive.extractfile(member) as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                actual = {'bytes': member.size, 'sha256': digest, 'mode': member.mode}
                assert actual == {k: expected_members[member.name][k] for k in ('bytes', 'sha256', 'mode')}
                observed[member.name] = actual
        assert set(observed) == set(expected_members)
        attempts = []
        for role, count, exit_code in [('02-original-count-failure-reproduced', 4, 1), ('03-focused-layout-controls', 6, 0), ('04-complete-155-controls', 155, 0)]:
            root = CAP / 'reports' / role; receipt = read(root / 'result.json')
            assert receipt['passed'] is True and receipt['returncode'] == exit_code and receipt['observed_tests'] == count
            assert receipt['source_unchanged'] and receipt['entire_checkout_including_unrelated_metadata_unchanged']
            expected_source = parent if exit_code else source
            assert read(root / 'source-before.json') == read(root / 'source-after.json') == expected_source
            checkout = read(root / 'executed-checkout-before.json')
            assert checkout == read(root / 'executed-checkout-after.json') and len(checkout) == 56
            assert {name: checkout[name] for name in expected_source} == expected_source
            for name, wanted in checkout.items():
                assert observed[role + '/checkout/' + name] == wanted
            log = (root / 'stderr.log').read_text()
            successes = literal_successes(log)
            if exit_code:
                assert len(successes) == 3 and 'AssertionError: 9 != 56' in log and log.rstrip().endswith('FAILED (failures=1)')
                assert len(receipt['failed_tests']) == 1 and receipt['expected_failure_reproduced'] is True
            else:
                assert len(successes) == len(set(successes)) == count and set(successes) == set(receipt['test_names'])
                assert receipt['errors'] == receipt['failed_tests'] == [] and log.rstrip().endswith('OK')
            attempts.append({'role': role, 'tests': count, 'exit_code': exit_code, 'unchanged_checkout_files': 56})
        before[str(RAW)] = identity(RAW)
        assert before[str(RAW)] == {'bytes': 4960179, 'sha256': 'cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833', 'mode': 420}
        with zipfile.ZipFile(RAW) as archive:
            assert len(archive.infolist()) == 4355
            log = archive.read('hosted-tool-host-tests.log').decode()
            assert archive.read('hosted-tool-host-tests.log') == (CAP / 'review/actual-hosted-failure/hosted-tool-host-tests.log').read_bytes()
            assert len(literal_successes(log, hosted=True)) == 152
            assert 'AssertionError: 9 != 56' in log and log.rstrip().endswith('FAILED (failures=1)')
        save('independent-delta-and-results.json', {'changed_paths': changed, 'unchanged_production_files': 6,
            'unchanged_old_test_bodies': 152, 'modified_test': modified[0], 'new_tests': sorted(set(new)-set(old)),
            'literal_attempts': attempts, 'archive_members': 4600, 'actual_failed_hosted_tests': 153,
            'actual_failed_hosted_successes': 152, 'actual_hosted_failure_preserved': True})
        result.update(passed=True, status='THREE_PATH_CHECKOUT_LAYOUT_CORRECTION_INDEPENDENTLY_REVIEWED',
            changed_paths=changed, source_files=9, capsule_payloads=66, archive_members=4600,
            tooling_tests_passed=155, unchanged_old_test_bodies=152, unchanged_production_files=6,
            full_combined_application_acceptance_still_pending=True)
    except Exception as error:
        result.update(status='CHECKOUT_CORRECTION_REVIEW_FAILED', reason=repr(error))
        save('exception.json', {'exception': repr(error), 'traceback': traceback.format_exc()})
    finally:
        result['all_read_inputs_unchanged'] = before == {name: identity(Path(name)) for name in before}
        if result['all_read_inputs_unchanged'] is not True:
            result['passed'] = False
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save('read-input-identities.json', before); save('result.json', result)
        rows = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
        save('checkpoint.json', {'schema': 1, 'status': result['status'], 'passed': result['passed'],
            'repo_target': 'docs/verification/day-trigger-combined/checkout-correction-review', 'active_files': [],
            'reviewed_checkpoint_sha256': '79d1895420bedcc3a28463f55ba989ecf0c460e72d683787395caad078d7767b',
            'android_executed': False, 'application_executed': False, 'files': rows})
        print(json.dumps({'result': result, 'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json')}, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
