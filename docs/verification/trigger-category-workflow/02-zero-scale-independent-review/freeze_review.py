#!/usr/bin/env python3
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
OUT = BASE / 'checkpoints/01-independent-zero12-review'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    result = json.loads((BASE / '01-closed-review/review-result.json').read_text())
    assert result['status'] == 'CLOSED_ZERO_SCALE12_REVIEW_APPROVED_FOR_SEPARATE_RUNTIME'
    paths = {'review_frozen.py': BASE / 'review_frozen.py', 'freeze_review.py': Path(__file__).resolve(),
             'review.stdout.log': BASE / '01-review.stdout.log'}
    for source in (BASE / '01-closed-review').iterdir():
        assert source.is_file()
        paths[source.name] = source
    for name, source in paths.items():
        shutil.copyfile(source, OUT / name)
        assert identity(source) == identity(OUT / name)
    (OUT / 'README.md').write_text('''# Independent review of the separate zero-scale twelve-screen workflow

The exact inactive workflow capsule was approved for a separate disposable-device run. No concrete source, argument, result-handling or provenance blocker was found in this review. Runtime equality remains pending; none of the earlier Normal03 or scale-zero failures is relabeled.

Reviewed checkpoint: `a6a279c48af61b553728eeaf05f92c8cf15e34bd5b4fdd907e193d31a63a5af0`. Reviewed generated workflow: `e3e53daf3c53c315605580aa49ff5d2ffda7c99b1dcb8014c5692dbfc22570fe`. The source lives in [the frozen zero-scale workflow](../../../../work-in-progress/trigger-category-workflow/02-zero-scale-workflow/); the separate helper checkpoint is `5cb124753f8acb7cf8e0ec070f1ddf2b2f9b49d99ad144dea6f2b37047258a48`.

The review independently verified all 12 workflow files, all nine zero-helper files, all 217 unique archive payloads covering 5,134 regular evidence paths, and all three already-published original/candidate/AAPT2 identities. The inert symlink fault was retained as metadata and was not recreated. It checked all 45 command records and retained logs; 130 capture, ten zero-helper and six downloader tests have matching individual successes and summaries. All twelve source-inventory mutations reject at both materialized and final boundaries, and all three owned-cleanup controls preserve their expected result.

The frozen preparer independently reconstructed the complete ordered set of 192 source-copy roles against the already closed private input tree. No additional APK, workspace, emulator or generated-cache copy was made. The exact candidate is the 94,683,119-byte combined APK with SHA256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`, bound to the immutable Combined05 manifest published at `c9373851d4408fb4db63c21873ac2d0bb6867270`.

The reviewed scope remains twelve full-frame stills and eleven validated inputs per APK. The final verifier requires actual zero-scale configuration and both endpoint environments, exact recorded-versus-replayed comparison objects, full pixels and hierarchies, and the frozen chronology/process guards. It requires `catalog_navigation_established=true` and `trigger_selected=false`. A recorded difference remains a difference; a successful workflow exit requires equality. The final comparison and complete evidence upload run even after an earlier step fails, and the cleanup trap addresses only the newly owned service queue and PID with a bounded wait.

The production helper delta changes the declared animation scales to zero while preserving the nineteen-command observation sequence and all existing rejection checks. The additional helper control states the exact nineteen commands independently. No app source/resource edit, screenshot mask, tolerance, cross-APK frame selection or full-runtime claim was introduced.

This was a closed evidence and code review. It executed no Android commands, rebuilt no APK, and reran no redundant suite. [review-result.json](review-result.json), [all archive member checks](all-217-archive-members.json), [all input roles](all-192-source-copy-roles.json) and [the actual review log](review.stdout.log) retain the measured result. The review source and freezer are included for reproduction.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_INDEPENDENT_ZERO12_REVIEW',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'docs/verification/trigger-category-workflow/02-zero-scale-independent-review',
                  'reviewed_checkpoint_sha256': result['reviewed_checkpoint_sha256'],
                  'active_files': [], 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'logical_bytes': sum(row['bytes'] for row in files),
                      'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
