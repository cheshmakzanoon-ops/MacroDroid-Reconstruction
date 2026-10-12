#!/usr/bin/env python3
"""Freeze both independent review attempts without editing the reviewed capsule."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import stat

ROOT = Path('/dev/shm/macrodroid-combined-host-tooling-review')
OUT = ROOT / 'checkpoint-01'
TARGET = 'docs/verification/day-trigger-combined/tooling-review'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def main():
    final = json.loads((ROOT / 'closed-02/result.json').read_bytes())
    first = json.loads((ROOT / 'closed-01/result.json').read_bytes())
    assert final['passed'] is True and final['all_read_inputs_unchanged'] is True
    assert first['passed'] is False and first['all_read_inputs_unchanged'] is True
    before = {str(p): identity(p) for p in ROOT.rglob('*') if p.is_file()}
    OUT.mkdir(exist_ok=False)
    for name, expected in sorted(before.items()):
        path = Path(name)
        assert stat.S_ISREG(path.lstat().st_mode)
        target = OUT / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(0o644)
        assert identity(target) == expected
    (OUT / 'initial-reader-observation.json').write_text(json.dumps({
        'schema': 1,
        'scope': 'Prior interactive read-only filename lookup, before either executed review',
        'requested_name': 'evidence-files.json',
        'literal_failure_type': 'FileNotFoundError',
        'observed_actual_name': 'evidence-inventory.json',
        'source_or_test_mutations': 0,
        'original_terminal_output_reconstructed': False,
    }, indent=2) + '\n')
    (OUT / 'README.md').write_text('''# Independent review of the combined DayTrigger host tooling

The closed combined tooling package passed this independent review at 2026-10-12 11:36:58 UTC. The exact source capsule checkpoint is `4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88`. The review covers the nine new paths declared by that capsule, including the workflow with SHA-256 `443e184bc3185593e1a8c268d60200ada2b1cdb6df2b8e551e51ae52dae0c6eb` and its exact runtime manifest `07b58ce29d4db875ef349d23aa05b8b75145ea4f7338b7dd2943db10129a0d32`.

The final [result](closed-02/result.json) verifies all 65 capsule payloads and modes, streams all 12,451 archived evidence members without extraction, and checks the 569 externally bound source/read inputs before and after. Fifty named shared recorder, filesystem-witness, input, numeric and report-verifier definitions remain byte-identical to the reviewed numeric parent.

The reviewer independently applies every baseline check before each dictionary mutation, reconstructing the complete 81,291-entry baseline, 81,298-entry numeric intermediate and 81,304-entry combined inventory. Both serialized future manifests match their exact byte and digest pins. The 19 numeric changes followed by 21 lookup changes cover 25 distinct final paths and introduce 13 release inputs. These dictionary checks do not claim a new physical full-project materialization.

The exact proposed 17 numeric and 19 lookup command vectors match the previously reviewed source-derived protocol, including order, expected exits and 120-second child limits. Sixteen acceptance gates and 24 fresh report roles are pinned. The full build is expected to exercise 195,151 three-path cases, 357 project Python tests and 1,244 registered recovered method bodies; those combined full-build results remain pending until the hosted job actually runs.

All 153 individual tooling-control successes and their exact output bytes were checked against the unchanged executed source copies. The additional boundary evidence contains exactly 11 commands: five shell-syntax checks, one successful literal workflow bootstrap and five literal bootstrap rejections. Every command's exit and both stream hashes match. The reviewer does not rerun the complete tooling suite or any Java, D8, APK build or Android action.

## Retained reviewer observations

The first [executed review](closed-01/result.json) passed the source, archive, manifest and command-vector checks, then rejected its own mistaken expectation that the boundary collector contained twelve commands. The actual closed collector has eleven. The original executed source, exception, partial outputs and unchanged-input inventory remain intact. The separate [second review](closed-02/executed-review.py) requires the exact eleven command names and order. The [correction patch](reviewer-command-count-correction.patch) changes only this reviewer expectation and its corresponding descriptive counts, plus the new output directory. No production source, tests or historical evidence was edited.

An earlier interactive reader also asked for `evidence-files.json`; the actual closed filename is `evidence-inventory.json`. The short [observation](initial-reader-observation.json) records that read-only lookup error without inventing a terminal transcript.

## Activation boundary

The nine declared active paths must all be absent in the fetched repository head. Publication of this review is separate from activation. Once the exact source capsule and this review are fetched and verified, the nine pinned paths can be added together using the existing fast-forward-only publication process. The newly activated workflow performs the full physical baseline scan, numeric stage, intermediate scan, lookup stage and combined scan before acceptance. This review contains no active application-source promotion, Android execution or universal 1:1 parity claim.
''')
    after = {name: identity(Path(name)) for name in before}
    assert before == after
    (OUT / 'freeze-source-boundaries.json').write_text(json.dumps({
        'before': before, 'after': after, 'all_source_inputs_unchanged': True,
    }, indent=2) + '\n')
    files = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file():
            files.append({'path': path.relative_to(OUT).as_posix(), 'mode': '100644', **identity(path)})
    result = {'schema': 1, 'status': 'COMBINED_HOST_TOOLING_INDEPENDENT_REVIEW_PASSED',
        'repo_target': TARGET, 'finished_utc': datetime.now(timezone.utc).isoformat(),
        'source_checkpoint_sha256': '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88',
        'files': files, 'file_count': len(files), 'payload_bytes': sum(r['bytes'] for r in files),
        'active_files': [], 'android_executed': False, 'full_host_build_executed': False,
        'full_runtime_1_to_1_established': False}
    (OUT / 'checkpoint.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': result['payload_bytes']}, indent=2))


if __name__ == '__main__':
    main()
