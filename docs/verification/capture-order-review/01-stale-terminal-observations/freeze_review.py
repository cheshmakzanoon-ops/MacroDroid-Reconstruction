from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa/trigger-category-review')
INPUTS = Path('/workspace/scratch/4130730d15aa/trigger-catalog-forward/checkpoints/02-reviewed-host-success')
DEST = ROOT / 'checkpoints/01-stale-terminal-observations'
DEST.mkdir(parents=True, exist_ok=False)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def copy_file(source, name):
    target = DEST / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    target.chmod(source.stat().st_mode & 0o777)

for source in sorted(ROOT.glob('*.py')):
    copy_file(source, source.name)
for source in [*sorted(ROOT.glob('*.json')), *sorted((ROOT / 'ten-screen').glob('*.json'))]:
    copy_file(source, source.relative_to(ROOT).as_posix())
cp_raw = (INPUTS / 'checkpoint.json').read_bytes()
assert sha(cp_raw) == '4e3d1ec8d3eec36d6db4685fef8d827c84b4c38e2c550e4a9896fba46eb90f92'
cp = json.loads(cp_raw)
for row in cp['files']:
    data = (INPUTS / row['path']).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256']
    copy_file(INPUTS / row['path'], 'inputs/' + row['path'])
copy_file(INPUTS / 'checkpoint.json', 'inputs/checkpoint.json')

members = []
with zipfile.ZipFile(DEST / 'synthetic-comparator-inputs.zip', 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for folder in [ROOT / 'synthetic-artifacts', ROOT / 'ten-screen/synthetic-artifacts']:
        for source in sorted(folder.rglob('*')):
            if not source.is_file():
                continue
            assert not source.is_symlink()
            name = source.relative_to(ROOT).as_posix()
            data = source.read_bytes()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
            members.append(dict(path=name, bytes=len(data), sha256=sha(data)))
with zipfile.ZipFile(DEST / 'synthetic-comparator-inputs.zip') as archive:
    assert len(archive.infolist()) == len(members)
    for row in members:
        data = archive.read(row['path'])
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
(DEST / 'synthetic-members.json').write_text(json.dumps(members, indent=2) + '\n')
(DEST / 'README.md').write_text('''# Read-only review: pre-input captures accepted as terminal observations

The inactive twelve-screen Trigger02 study and its unchanged existing ten-screen policy both accepted a synthetic terminal capture recorded before the final input. The exact 81-file input capsule and its checkpoint are copied under `inputs/`, matching durable commit `c1a6d71d2e290d16ea3a047d036996f79005883a` at `work-in-progress/trigger-category/02-reviewed-host-success/`.

For each sequence, the reproduction first requires a passing clean synthetic baseline. It then removes both genuine terminal acquisition ledgers and their two full observation sets: 26 files across original/candidate. It removes those two ledger references from `capture_events` and substitutes each preceding still for the terminal shot, changing only the declared screen name. The matching terminal PNG/XML therefore comes entirely from before the final input. The two false positives are:

| Sequence | Reused original/candidate observation ends | Original/candidate final input starts | Incorrect accepted scope |
| --- | --- | --- | --- |
| Twelve screens | 1056.6 / 2056.6 | 1059.4 / 2059.4 | `EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY`, surface after Date/Time tap |
| Ten screens | 1045.8 / 2045.8 | 1048.9 / 2048.9 | `EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY`, surface after OK |

The shared guard validates each acquisition's internal timing and requires its ledger to exist, but permits one accepted ledger to be used by multiple screen records. It also omits a check that the next acquisition starts after its corresponding input command finishes. The successful reproduction proves this missing relationship without changing timestamps, hashes, input arguments, prior screens, APK declarations or process guards.

Two additional controls change only the candidate final input to `input tap 1 1`; both correctly return `REJECTED` with the recorded target-command error. The scripts, complete pre-mutation and mutated report documents, removed-file inventories, final verdicts and the complete artifact set actually presented to each mutated comparator are preserved. The intentionally removed terminal file bytes are not in that final artifact set; their hashes remain in the removed-file inventories and the pinned fixture code reproduces their contents. `synthetic-comparator-inputs.zip` holds all remaining artifact files with an independently verified member inventory.

## Actual ten-screen run remains a measured difference

A separate read-only audit of the unchanged 15,156,144-byte run38205737183 ZIP verified all38 accepted acquisition ledgers were distinct, all456 observation artifact paths were distinct, and all18 actual next captures started after their input commands finished. The actual chronology therefore does not exhibit this synthetic stale-terminal defect. `actual-ten-chronology.json` records every input-to-capture interval and the exact ZIP/journey hashes. It does not rerun Android or replace the existing `JOURNEY_DIFFERENCE` verdict, including the26 TRIGGERS pixels.

No active source or workflow was modified, and neither reproduction executed Android. The Trigger02 study remains inactive. The proposed correction should reject reuse of accepted capture identities and bind each resulting capture to the completed input before it, then replay the unchanged actual ten-screen evidence. Historical failed and passing source/runtime reports must remain intact.

The executed scripts retain explicit historical study paths. The complete pinned source and report inputs are included for an isolated replay; use a fresh output directory and preserve these frozen originals.
''')
files = []
for source in sorted(DEST.rglob('*')):
    if source.is_file():
        data = source.read_bytes()
        files.append(dict(path=source.relative_to(DEST).as_posix(), bytes=len(data), sha256=sha(data),
                          mode='100755' if source.stat().st_mode & 0o111 else '100644'))
checkpoint = dict(status='TEN_AND_TWELVE_STALE_TERMINAL_FALSE_POSITIVES_REPRODUCED', files=files,
    pinned_input_checkpoint_sha256=sha(cp_raw), pinned_input_files=81,
    incorrect_acceptance_cases=2, rejecting_wrong_tap_controls=2,
    archived_synthetic_input_members=len(members), actual_ten_distinct_ledgers_verified=38,
    actual_ten_post_input_order_edges_verified=18, active_source_modified=False, android_executed=False,
    historical_actual_verdict_unchanged='JOURNEY_DIFFERENCE')
(DEST / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
print(json.dumps(dict(path=str(DEST / 'checkpoint.json'), sha256=sha((DEST / 'checkpoint.json').read_bytes()),
                      files=len(files), bytes=sum(row['bytes'] for row in files), synthetic_members=len(members))))
