#!/usr/bin/env python3
"""Independently replay a peer's preserved synthetic stale-evidence controls."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
PEER = ROOT.parent / 'editor-session-review'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'inputs/tools/parity_journeys'))
sys.path.insert(0, str(ROOT / 'inputs/project'))
import android_compare as proof
import post_onboarding as session
import supplied_reference_journey as adapter
import test_post_onboarding as tests


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    manifest = json.loads((ROOT / 'input-manifest.json').read_text())
    for entry in manifest['all_copied_files']:
        assert meta(ROOT / 'inputs' / entry['path']) == {key: entry[key] for key in ['bytes', 'sha256']}
    fixture = tests.SessionTests('test_exact_session_does_not_turn_shared_startup_restart_into_a_pass')
    fixture.setUp()
    try:
        positive = fixture.result()
        assert positive['editor_session_equal'] is True
    finally:
        fixture.doCleanups()
    results = []
    for name, expected_equal in [('endpoint-identity-reuse', True), ('preinput-evidence-reuse', True),
                                  ('preinput-resolved-alias-reuse', True), ('wrong-endpoint-digest-control', False)]:
        folder = PEER / 'cases' / name
        report = json.loads((folder / 'report.json').read_text())
        result = session.compare_session(folder / 'artifacts', report, adapter.load_plan(), proof)
        assert result == json.loads((folder / 'result.json').read_text())
        assert result['editor_session_equal'] is expected_equal
        results.append({'name': name, 'report': meta(folder / 'report.json'),
                        'peer_result': meta(folder / 'result.json'), 'reproduced_result': result,
                        'replayed_exactly': True, 'false_positive': expected_equal})
    output = ROOT / 'reports/01-independent-reproduction'
    output.mkdir(parents=True, exist_ok=False)
    result = {'schema': 1, 'reviewed_commit': manifest['base_commit'],
              'peer_frozen_checkpoint': {'path': str(PEER / 'checkpoints/01-read-only-guard-gaps/checkpoint.json'),
                                        **meta(PEER / 'checkpoints/01-read-only-guard-gaps/checkpoint.json')},
              'all_input_hashes_verified': True, 'positive_baseline': positive, 'cases': results,
              'android_executed': False, 'active_files_modified': False,
              'full_runtime_1_to_1_established': False}
    (output / 'independent-reproduction.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'THREE_FALSE_POSITIVES_AND_WRONG_DIGEST_REJECTION_INDEPENDENTLY_REPRODUCED',
                      'cases': [{'name': item['name'], 'status': item['reproduced_result']['status']} for item in results],
                      'android_executed': False, 'active_files_modified': False}, indent=2))


if __name__ == '__main__':
    main()
