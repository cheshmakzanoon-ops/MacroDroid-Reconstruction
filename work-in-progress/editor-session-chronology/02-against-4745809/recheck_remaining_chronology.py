"""Preserve concrete timing/component gaps after the external file ledger fix."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'external474-reports/01-distinct-file-chronology-cases'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def earlier_endpoint(f):
    run = f.report['runs'][1]
    initial, final = run['screens'][f.start]['session_identity'], run['screens'][-1]['session_identity']
    for key in ('package_path', 'checksum', 'pid', 'foreground'):
        for stamp in ('started_monotonic', 'finished_monotonic'):
            final[key][stamp] = initial[key][stamp]


def earlier_result(f):
    run = f.report['runs'][1]
    run['screens'][-1]['session_observation'] = copy.deepcopy(run['screens'][-2]['session_observation'])


def earlier_input(f):
    first, later = f.report['runs'][1]['transitions'][f.start:f.start + 2]
    for stamp in ('started_monotonic', 'finished_monotonic'):
        later['command'][stamp] = first['command'][stamp]


def changed_component(f):
    run = f.report['runs'][1]
    run['screens'][-1]['session_identity']['foreground']['stdout'] = f.put(run, 'different-final-component', f.home())


def wrong_hash(f):
    run = f.report['runs'][1]
    run['screens'][-1]['session_identity']['checksum']['stdout'] = f.put(run, 'different-final-hash',
        ('f' * 64 + '  /data/app/test/base.apk\n').encode())


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    sys.dont_write_bytecode = True
    work = ROOT / 'external474-worktree'
    sys.path[:0] = [str(work / 'tools/parity_journeys'), str(work / 'project')]
    import test_post_onboarding as fixtures
    old_source = ROOT / 'external474-inputs/tools/parity_journeys/post_onboarding.py'
    assert meta(old_source.read_bytes())['sha256'] == '1191dedd5d233b14ad89c4978ef7f8c52ee2d0c47cc8650d21f79685f8a1b7d2'
    spec = importlib.util.spec_from_file_location('exact_external474_session', old_source)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    rows = []
    for name, mutation in (
        ('final-identity-before-final-input', earlier_endpoint),
        ('distinct-final-capture-before-final-input', earlier_result),
        ('later-input-before-earlier-input', earlier_input),
        ('final-endpoint-component-changed', changed_component),
        ('wrong-installed-hash-control', wrong_hash),
    ):
        f = fixtures.SessionTests()
        f.setUp()
        try:
            baseline_report = copy.deepcopy(f.report)
            before_old = old.compare_session(f.root, f.report, f.plan, f.proof)
            before_new = f.result()
            assert before_old['editor_session_equal'] and before_new['editor_session_equal']
            mutation(f)
            after_old = old.compare_session(f.root, f.report, f.plan, f.proof)
            after_new = f.result()
            assert after_old['editor_session_equal'] == (name != 'wrong-installed-hash-control'), (name, after_old)
            assert not after_new['editor_session_equal'], (name, after_new)
            assert after_new['evidence_identity_check']['unique_observation_files'] == 294
            case = OUT / name
            case.mkdir()
            for filename, data in (
                ('before-report.json', baseline_report), ('after-report.json', f.report),
                ('before-external474.json', before_old), ('before-proposed.json', before_new),
                ('after-external474.json', after_old), ('after-proposed.json', after_new),
            ):
                (case / filename).write_text(json.dumps(data, indent=2) + '\n')
            members = []
            with zipfile.ZipFile(case / 'synthetic-artifacts.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                for path in sorted(f.root.rglob('*')):
                    if not path.is_file():
                        continue
                    relative = path.relative_to(f.root).as_posix()
                    data = path.read_bytes()
                    info = zipfile.ZipInfo(relative, date_time=(2026, 10, 12, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, data)
                    members.append({'path': relative, **meta(data)})
            (case / 'synthetic-artifact-manifest.json').write_text(json.dumps(members, indent=2) + '\n')
            rows.append({'name': name, 'baseline_external474_accepted': True, 'baseline_proposed_accepted': True,
                         'external474_after': after_old['status'], 'external474_after_equal': after_old['editor_session_equal'],
                         'proposed_after': after_new['status'], 'proposed_reason': after_new.get('reason'),
                         'distinct_observation_files_verified': after_new['evidence_identity_check']['unique_observation_files'],
                         'synthetic_artifact_archive': meta((case / 'synthetic-artifacts.zip').read_bytes()),
                         'synthetic_artifact_members': len(members)})
            print(json.dumps(rows[-1], sort_keys=True), flush=True)
        finally:
            f.doCleanups()
    source_pins = {rel: meta((work / 'tools/parity_journeys' / rel).read_bytes())
                   for rel in ('post_onboarding.py', 'test_post_onboarding.py', 'session_evidence.py', 'test_session_evidence.py')}
    result = {'schema': 1, 'status': 'FOUR_DISTINCT_FILE_GAPS_REPRODUCED_AND_REJECTED',
              'baseline_commit': '47458097056fd023bad8b47b6464978b0d02e85c', 'baseline_source': meta(old_source.read_bytes()),
              'proposed_sources': source_pins, 'cases': rows, 'android_executed': False,
              'active_repository_modified': False, 'file_identity_ledger_relaxed': False,
              'full_runtime_1_to_1_established': False,
              'scope': 'Synthetic recorded-evidence checks; distinct files alone do not establish chronology or endpoint component continuity.'}
    (OUT / 'recheck-result.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
