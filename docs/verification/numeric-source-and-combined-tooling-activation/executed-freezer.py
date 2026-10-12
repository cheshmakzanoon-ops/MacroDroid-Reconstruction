"""Freeze exact guards, fetched verification, and observed automatic job metadata."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
OUTPUT = ROOT / 'numeric-and-combined-activation-receipts'
TARGET = 'docs/verification/numeric-source-and-combined-tooling-activation'
SPECS = [
 ('prepare_numeric_promotion_activation.py', 'numeric/executed-preparer.py'),
 ('prepare_combined_checkout_correction_activation.py', 'combined/executed-preparer.py'),
 ('numeric-activation-jobs-observed.json', 'numeric/observed-jobs.json'),
 ('numeric-activation-runs-observed.json', 'numeric/observed-runs.json'),
 ('combined-correction-jobs-observed.json', 'combined/observed-jobs.json'),
 ('combined-correction-runs-observed.json', 'combined/observed-runs.json'),
 ('numeric-proposal-and-combined-failure-export/precommit-guard.json', 'preceding-publications/proposal-precommit-guard.json'),
 ('numeric-proposal-and-combined-failure-export/remote-verification.json', 'preceding-publications/proposal-fetched-verification.json'),
 ('settings-and-promotion-reviews-export/precommit-guard.json', 'preceding-publications/reviews-precommit-guard.json'),
 ('settings-and-promotion-reviews-export/preparation.json', 'preceding-publications/reviews-preparation.json'),
 ('settings-and-promotion-reviews-export/remote-verification.json', 'preceding-publications/reviews-fetched-verification.json'),
 ('settings-and-promotion-reviews-export/fetched-settings03-archive-verification.json', 'preceding-publications/settings03-fetched-archive-verification.json'),
]
for prefix, folder in [('numeric-source-promotion-activation-export', 'numeric'),
                       ('combined-checkout-correction-activation-export', 'combined')]:
    for name in ('preparation.json', 'manifest.json', 'tree-elements.json', 'remote-verification.json', 'protected-trees-after.json'):
        SPECS.append((prefix + '/' + name, folder + '/' + name))
OUTPUT.mkdir(exist_ok=False)
def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), mode=0o644)
for source_name, target_name in SPECS:
    source, target = ROOT / source_name, OUTPUT / target_name
    before = identity(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    assert identity(target) == before
numeric = json.loads((OUTPUT / 'numeric/remote-verification.json').read_bytes())
combined = json.loads((OUTPUT / 'combined/remote-verification.json').read_bytes())
assert numeric['commit'] == '8db1fca4f03532ee2e5a8791fde7ea18126c237f'
assert numeric['verified_paths'] == numeric['changed_paths'] == 22
assert combined['commit'] == '97322c18273818b0241fa1fa962da9d4a445afd1'
assert combined['verified_paths'] == combined['changed_paths'] == 3
for result in (numeric, combined):
    assert result['git_mode_size_sha1_sha256_verified'] is True
    assert result['staged_bytes_and_modes_equal_fetched_git'] is True
for folder in ('numeric', 'combined'):
    proof = json.loads((OUTPUT / folder / 'protected-trees-after.json').read_bytes())
    assert proof['passed'] is True and proof['all_other_paths_unchanged'] is True
readme = '''# Numeric source promotion and separate combined-tooling correction

The reviewed numeric promotion was applied in **8db1fca4f03532ee2e5a8791fde7ea18126c237f** after its original proposal and independent review were committed and fetched back. Exactly **22** paths changed: the 19 source files, complete input snapshot, current APK manifest and reviewed root README. All 15 existing-file identities and seven required absences passed. The current manifest points to the already preserved **0762aad9** APK; all 12 fetched parts were streamed and checked before activation.

The separate checkout-layout correction was applied in **97322c18273818b0241fa1fa962da9d4a445afd1**. Exactly **three** tooling paths changed: the test file and matching runtime/workflow fingerprints. All six production tooling files and the promoted application source/APK remained byte-identical. The original failed combined run is preserved under `../day-trigger-hosted-run-59df961/`.

These are complete executed guards and fetched verification receipts, not a new acceptance result. The automatically triggered reconstruction run **38247941263** and combined run **38248170022** were in progress at the retained observations. The numeric source and Android jobs had reached materialization/runtime installation; the combined run had passed tooling controls and reached physical source preparation. No duplicate dispatch occurred. Each later result must be preserved separately before claiming a completed application or Android outcome.

Both exact preparers, complete path bindings, tree elements, Git mode/byte/hash checks, preserved-tree postconditions, prior inactive-publication receipts and original API job metadata are included. This additive evidence capsule makes no further active change.
'''
(OUTPUT / 'README.md').write_text(readme)
(OUTPUT / 'README.md').chmod(0o644)
os.link(Path(__file__), OUTPUT / 'executed-freezer.py')
files = [dict(path=str(path.relative_to(OUTPUT)), **identity(path)) for path in sorted(OUTPUT.rglob('*')) if path.is_file()]
checkpoint = dict(schema=1, repo_target=TARGET, status='EXACT_ACTIVATIONS_FETCHED_AND_VERIFIED_NEW_RUNS_PENDING',
                  active_files=[], files=files, numeric_commit=numeric['commit'], combined_tooling_commit=combined['commit'],
                  new_acceptance_or_android_result_claimed=False, created_utc=datetime.now(timezone.utc).isoformat())
(OUTPUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
(OUTPUT / 'checkpoint.json').chmod(0o644)
print(json.dumps(dict(output=str(OUTPUT), target=TARGET, checkpoint=identity(OUTPUT / 'checkpoint.json'), files=len(files))))
