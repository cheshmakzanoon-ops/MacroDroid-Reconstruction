#!/usr/bin/env python3
"""Preserve the 57 prior mutations and add one exact label-two retry fault."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    original = HERE / 'video_method_mutants_final.json'
    if hashlib.sha256(original.read_bytes()).hexdigest() != 'c004a5aab38dedd12bb5a7eff4d0e8de739383d490b0d50198f5f8c0d47f488d':
        raise RuntimeError('Frozen prior mutation catalog changed')
    catalog = json.loads(original.read_text())
    if len(catalog['controls']) != 57:
        raise RuntimeError('Expected all prior 57 actual compiled controls')
    catalog.update(baseline_checkpoint_sha256='02f80d76ee2fcf9d9cacf38f4b8d0fdd9c8697934daa190aa9c3450ab7cfc6ac',
        baseline_study_directory='original-jvm-13-retry-delay', expected_cases=1125, expected_independent_checks=237)
    catalog['controls'].append({
        'name': 'label-two-retry-always-suspends',
        'reason': 'A synchronous return from the retry delay after a label-two resumed Exception must enter the loop and observe false recording; only the suspension singleton suspends.',
        'edits': [{'find': '            Object delayed = sz6.s(3000L, self);\n            if (delayed == suspended) return suspended;\n        } else if (label == 3) {',
                   'replace': '            Object delayed = sz6.s(3000L, self);\n            return suspended;\n        } else if (label == 3) {', 'count': 1}],
        'expected_failure_labels': ['video-label-two-retry-delay:0', 'video-label-two-retry-delay:2',
                                    'video-label-two-retry-delay:5', 'video-label-two-retry-delay:6']})
    if catalog['controls'][:-1] != json.loads(original.read_text())['controls']:
        raise RuntimeError('A prior actual mutation changed')
    output = HERE / 'video_method_mutants_retry.json'
    with output.open('x') as stream:
        json.dump(catalog, stream, indent=2); stream.write('\n')
    print(json.dumps({'path': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                      'controls': len(catalog['controls']), 'prior_57_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
