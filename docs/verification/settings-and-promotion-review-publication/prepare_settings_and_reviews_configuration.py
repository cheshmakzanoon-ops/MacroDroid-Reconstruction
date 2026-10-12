"""Bind the exact closed Settings transport and independent promotion reviews."""
from pathlib import Path
import hashlib
import json

root = Path('/dev/shm/macrodroid-transfer-space-20261012')
specs = [
('/dev/shm/macrodroid-exact-alarm-enable-return/checkpoints/03-source-and-host-controls',
 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls',
 '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051', 181),
(str(root / 'settings-source03-archive-layout'),
 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls/archive-layout',
 '4833927dff3df7213a401d40a67fdfaa2dc31fb5c6ef487616dc9dde55c700a2', 11),
('/dev/shm/macrodroid-exact-alarm-enable-return/source-review-checkpoint-01',
 'docs/verification/exact-alarm-enable-return/source-review',
 'd49cf08ea042abb8a05e05f724906bf1b4e6fa4371b016346fce4ad326859257', 24),
('/dev/shm/macrodroid-numeric-promotion-independent-review/checkpoints/01-promotion-review',
 'docs/verification/day-trigger-numeric/11-source-promotion-independent-review',
 '171694b92732192f2a509c0e8da0a509289522303c12934563f078901e88b409', 25),
('/dev/shm/macrodroid-day-lookup-checkout-fix/checkpoints/01-checkout-layout-controls',
 'work-in-progress/day-trigger-lookup/13-checkout-layout-controls',
 '79d1895420bedcc3a28463f55ba989ecf0c460e72d683787395caad078d7767b', 66),
('/dev/shm/macrodroid-day-lookup-checkout-fix/root-review-02',
 'docs/verification/day-trigger-combined/checkout-correction-review',
 'c8f60111d0ef63cd88e1bfcb65b9b5cfc919ccc56e9a9bcf7e2799a5a1c5fad0', 11),
('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/02-implemented-offline-validated',
 'work-in-progress/indicator-fixed-sampling/03-implemented-offline-validation',
 'd555736471dafe7cf9c93a2d32580d76ca9cd2a1f41a4ae60fc8c68deb5cdf62', 178),
]
capsules = []
for source, target, checkpoint, count in specs:
    raw = (Path(source) / 'checkpoint.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == checkpoint
    assert len(json.loads(raw)['files']) == count
    capsules.append(dict(source=source, target=target, checkpoint_sha256=checkpoint, files=count))
capsules[0]['archive_mapping'] = dict(logical_path='evidence.tar.gz',
    source=str(root / 'settings-source03-archive-layout'),
    manifest_sha256='8be9e7dab79ccad82db4b98e33e8418044a372a456e45907bcec0f134bce6310')
operations = [
('numeric-proposal-and-combined-failure-export/remote-verification.json', 'previous-fetched-verification.json'),
('derive_settings03_publication_preparer.py', 'derive_settings03_publication_preparer.py'),
('settings03-preparer-baseline.py', 'settings03-preparer-baseline.py'),
('settings03-publication-preparer.patch', 'settings03-publication-preparer.patch'),
('settings03-preparer-derivation.json', 'settings03-preparer-derivation.json'),
('prepare_settings_and_reviews_configuration.py', 'prepare_settings_and_reviews_configuration.py'),
]
cfg = dict(parent='636004a01b11fc7ac307abc9df022898b7738e62', capsules=capsules,
           operations_prefix='docs/verification/settings-and-promotion-review-publication',
           operations=[dict(source=str(root / src), name=dest,
                            sha256=hashlib.sha256((root / src).read_bytes()).hexdigest())
                       for src, dest in operations])
output = root / 'settings-and-promotion-reviews-configuration.json'
with output.open('x') as stream:
    stream.write(json.dumps(cfg, indent=2) + '\n')
output.chmod(0o644)
print(json.dumps(dict(configuration=str(output), capsules=len(capsules), active_paths=0)))
