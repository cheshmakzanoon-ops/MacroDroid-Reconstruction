#!/usr/bin/env python3
"""Reproduce and reject the three published stale-evidence cases without Android.

Supply post_onboarding.py from commit 934c6543. Its Git blob identity is checked
before the historical comparator is imported. Temporary synthetic artifacts are
created by the committed fixture; only compact before/after results are retained.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import test_post_onboarding as fixtures

OLD_BLOB = '639159b34062f528b2f7901954672d43ded99317'


def endpoint_reuse(f):
    run = f.report['runs'][1]
    initial, final = run['screens'][f.start], run['screens'][-1]
    for key in ('package_path', 'checksum', 'pid', 'foreground'):
        for stream in ('stdout', 'stderr'):
            (f.root / final['session_identity'][key][stream]['path']).unlink()
    final['session_identity'] = copy.deepcopy(initial['session_identity'])


def preinput_reuse(f):
    first, later = f.report['runs'][1]['transitions'][f.start:f.start + 2]
    for record in later['preinput_artifacts'].values():
        (f.root / record['path']).unlink()
    later['preinput_artifacts'] = copy.deepcopy(first['preinput_artifacts'])


def alias_reuse(f):
    first, later = f.report['runs'][1]['transitions'][f.start:f.start + 2]
    (f.root / 'candidate-reused').mkdir()
    for key, record in list(first['preinput_artifacts'].items()):
        data = (f.root / record['path']).read_bytes()
        fresh = f.fixture.put('candidate-reused/' + key + '.txt', data)
        first['preinput_artifacts'][key] = fresh
        (f.root / later['preinput_artifacts'][key]['path']).unlink()
        later['preinput_artifacts'][key] = dict(fresh, path='candidate-reused/./' + key + '.txt')


def digest_control(f):
    run = f.report['runs'][1]
    final = run['screens'][-1]['session_identity']
    final['checksum']['stdout'] = f.put(run, 'wrong-endpoint-sha',
        ('f' * 64 + '  /data/app/test/base.apk\n').encode())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--historical-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.historical_source.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != OLD_BLOB:
        parser.error('Historical comparator is not the reviewed exact source blob')
    spec = importlib.util.spec_from_file_location('reviewed_session_comparator', args.historical_source)
    historical = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(historical)
    result = {'historical_source_commit': '934c6543dce0897975f52457717b3a70bd27ce00',
              'historical_blob': blob, 'synthetic_only': True, 'android_executed': False,
              'full_runtime_1_to_1_established': False, 'cases': []}
    for name, mutate in [('endpoint-identity-reuse', endpoint_reuse),
                         ('preinput-evidence-reuse', preinput_reuse),
                         ('preinput-resolved-alias-reuse', alias_reuse),
                         ('wrong-endpoint-digest-control', digest_control)]:
        fixture = fixtures.SessionTests()
        fixture.setUp()
        try:
            def old():
                return historical.compare_session(fixture.root, fixture.report, fixture.plan, fixture.proof)
            baseline_old, baseline_new = old(), fixture.result()
            assert baseline_old['editor_session_equal'] and baseline_new['editor_session_equal']
            mutate(fixture)
            before, after = old(), fixture.result()
            expected_old = name != 'wrong-endpoint-digest-control'
            assert before['editor_session_equal'] == expected_old, (name, before)
            assert not after['editor_session_equal'], (name, after)
            result['cases'].append({'name': name, 'baseline_old_accepted': True,
                                   'baseline_new_accepted': True,
                                   'before': {k: before[k] for k in ('status', 'editor_session_equal', 'reason') if k in before},
                                   'after': {k: after[k] for k in ('status', 'editor_session_equal', 'reason') if k in after}})
        finally:
            fixture.doCleanups()
    result['all_review_cases_corrected'] = True
    result['current_sources'] = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                 for name in ('session_evidence.py', 'post_onboarding.py',
                                              'test_session_evidence.py', Path(__file__).name)}
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print('Reproduced all three historical false positives; all three now rejected; digest control rejected.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
