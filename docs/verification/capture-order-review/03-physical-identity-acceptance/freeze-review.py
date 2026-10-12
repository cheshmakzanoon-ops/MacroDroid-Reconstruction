from pathlib import Path
import hashlib
import json

ROOT = Path('/workspace/scratch/4130730d15aa')
OUT = ROOT / 'trigger-category-review/physical-guard-review'
SOURCE = ROOT / 'trigger-catalog-forward/checkpoints/05-physical-identity-host-success'

def sha(data):
    return hashlib.sha256(data).hexdigest()

result = json.loads((OUT / 'review-result.json').read_text())
assert result['exact_source_files_verified'] == 97
assert len(result['results']) == 4
assert all(row['baseline_accepted'] and not row['mutated_accepted'] and row['status'] == 'REJECTED' for row in result['results'])
assert not result['android_executed'] and not result['active_or_frozen_source_modified']
for source, name in [
    (ROOT / 'trigger-category-review/review_physical_chronology.py', 'executed-review.py'),
    (Path(__file__), 'freeze-review.py'),
    (SOURCE / 'checkpoint.json', 'reviewed-source-checkpoint.json'),
]:
    data = source.read_bytes()
    target = OUT / name
    assert not target.exists() or target.read_bytes() == data
    target.write_bytes(data)

(OUT / 'README.md').write_text('''# Independent review of the physical capture-identity correction

The same four controls used in the preceding hardlink review were rerun against the frozen Trigger05 checkpoint, SHA-256 `8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743`. All 97 declared source/evidence files were checked against their exact bytes before and after the run. No frozen or active source was modified, and no Android command was executed.

All four genuine synthetic baselines were accepted. On both the ten-screen and twelve-screen plans, removing the real final acquisition and substituting the preceding capture was rejected for reusing an accepted ledger. On both plans, replacing a late pre-input PID artifact by a hardlink to an earlier PID artifact was rejected for reusing a physical acquisition artifact. The latter inputs retain distinct resolved paths and unchanged report fields, bytes, and hashes; the new guard also checks `(st_dev, st_ino)`.

Each case contains its full original and altered report, actual baseline and rejection result, change record, exact synthetic input ZIP, member inventory, and hardlink identity metadata. ZIP members flatten hardlinks into independent byte streams. To reproduce the physical alias, use the executed review script or recreate the exact inert identity grouping; extracting the ZIP alone does not recreate that inode relationship.

The production guard was also read: it claims both resolved paths and physical file identities for capture ledgers at initialization and for accepted frame, pre-input, command, and handoff artifact roles. The reviewer approves this narrow correction for the separately coordinated shared-guard update. This is host evidence only and does not approve any unrelated workflow preflight change or establish full runtime parity. The historical actual ten-screen 26-pixel failure remains unchanged in the parent Trigger05 replay evidence.
''')
rows = []
for path in sorted(OUT.rglob('*')):
    if path.is_dir():
        continue
    assert path.is_file() and not path.is_symlink()
    assert path.name != 'checkpoint.json'
    data = path.read_bytes()
    rows.append(dict(path=path.relative_to(OUT).as_posix(), bytes=len(data), sha256=sha(data), mode='100755' if path.stat().st_mode & 0o111 else '100644'))
checkpoint = dict(status='INDEPENDENT_FOUR_CASE_PHYSICAL_IDENTITY_REVIEW_PASSED',
    reviewed_checkpoint_sha256=result['checkpoint_sha256'], exact_source_files_verified=97,
    android_executed=False, active_files=[], approved_scope='Reviewed shared capture chronology and physical identity guard only',
    genuine_baselines_accepted=4, stale_terminal_rejections=2, physical_alias_rejections=2,
    original_and_frozen_source_unchanged=True, hardlink_metadata_required=True, files=rows)
data = (json.dumps(checkpoint, indent=2) + '\n').encode()
(OUT / 'checkpoint.json').write_bytes(data)
print(json.dumps(dict(path=str(OUT / 'checkpoint.json'), files=len(rows), bytes=sum(row['bytes'] for row in rows), checkpoint_sha256=sha(data))))
