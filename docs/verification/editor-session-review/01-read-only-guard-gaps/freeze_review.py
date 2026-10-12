from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa/editor-session-review')
DEST = ROOT / 'checkpoints/01-read-only-guard-gaps'
DEST.mkdir(parents=True, exist_ok=False)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def copy_file(path, name):
    data = path.read_bytes()
    target = DEST / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    target.chmod(path.stat().st_mode & 0o777)

for name in ['reproduce_guard_gaps.py', 'freeze_review.py', 'guard-review.json', 'existing-tests-tool-output.log']:
    copy_file(ROOT / name, name)
for source in sorted((ROOT / 'inputs').rglob('*')):
    if source.is_file():
        copy_file(source, source.relative_to(ROOT).as_posix())
for source in sorted((ROOT / 'cases').glob('*/*.json')):
    copy_file(source, source.relative_to(ROOT).as_posix())

members = []
with zipfile.ZipFile(DEST / 'complete-synthetic-evidence.zip', 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted((ROOT / 'cases').rglob('*')):
        if not path.is_file():
            continue
        assert not path.is_symlink()
        name = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        item = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = (0o100644 << 16)
        archive.writestr(item, data)
        members.append(dict(path=name, bytes=len(data), sha256=sha(data)))
with zipfile.ZipFile(DEST / 'complete-synthetic-evidence.zip') as archive:
    assert len(archive.infolist()) == len(members) == 2315
    for row in members:
        data = archive.read(row['path'])
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
(DEST / 'synthetic-members.json').write_text(json.dumps(members, indent=2) + '\n')
(DEST / 'existing-tests-execution.json').write_text(json.dumps(dict(
    command='PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/parity_journeys -p test_post_onboarding.py -v',
    working_directory='/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction',
    exit_code=0, tests=12, seconds=10.376,
    log_source='Exact stdout concatenated from initial exec and completion tool-output chunks; the test was not rerun to produce this file.',
    android_executed=False), indent=2) + '\n')
(DEST / 'README.md').write_text('''# Read-only review: stale evidence can pass the editor-session comparator

The external implementation at `934c6543dce0897975f52457717b3a70bd27ce00` was retained unchanged. Its declared home-to-editor scope is separate from startup; this review found two concrete guard failures inside that finite scope. All nine imported source/plan files are copied exactly and bound to that commit.

1. The final endpoint can reuse the starting endpoint's entire `session_identity`. The reproduction deletes all eight final endpoint command-output files, substitutes the start identity, and still receives `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY`. `checked_identity` validates command values and per-run naming but does not require distinct endpoint artifacts.
2. A later tap can reuse an earlier tap's immediate PID and foreground artifacts. The reproduction deletes the later pair, substitutes the earlier pair, and still passes. A separate case uses `./` path aliases with the same resolved file identity and also passes. `checked_transition` excludes reuse against only that transition's prior/before snapshots, not earlier inputs across the session.

The existing 12 session tests passed in 10.376 seconds. Each of the three new stale-evidence cases starts from a passing synthetic baseline and then reproduces an incorrect pass. A fourth control changes the final installed APK digest and correctly returns `REJECTED`, exercising the endpoint guard's intended failure path. The reproduction script exits successfully only when these exact vulnerable behaviors and the rejecting digest control are reproduced.

All four full synthetic reports, comparator results, mutations and 2,315 exact case artifacts are preserved in `complete-synthetic-evidence.zip`; every member was independently read back and hash checked. Compact reports/results and all pinned imported source remain directly readable. The recorded test-output file is the exact concatenation of the two tool-output chunks from the one existing-suite invocation.

No Android device was executed and no active external source was modified. These are comparator findings, not new app-parity measurements. The original actual runtime reports and failures remain unchanged. Any claimed session pass needs corrected artifact-freshness validation before it can be treated as reviewed evidence. A proposed correction should use session-wide resolved artifact identities for fresh captures, immediate input observations and the two endpoint command groups, while retaining exact bytes and the separate startup result.

The executed reproduction uses explicit task paths and requires the nine repository inputs at the pinned commit. Their complete copies under `inputs/` permit an isolated historical replay; later active fixes must not replace these frozen source bytes.
''')
rows = []
for path in sorted(DEST.rglob('*')):
    if path.is_file():
        data = path.read_bytes()
        rows.append(dict(path=path.relative_to(DEST).as_posix(), bytes=len(data), sha256=sha(data),
                         mode='100755' if path.stat().st_mode & 0o111 else '100644'))
checkpoint = dict(status='READ_ONLY_SYNTHETIC_GUARD_FALSE_POSITIVES_REPRODUCED',
                  reviewed_external_commit='934c6543dce0897975f52457717b3a70bd27ce00',
                  files=rows, complete_synthetic_archive_members=2315, existing_tests_passed=12,
                  stale_evidence_false_positive_cases=3, rejecting_digest_control_cases=1,
                  active_source_modified=False, android_executed=False, runtime_parity_established=False)
(DEST / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
raw = (DEST / 'checkpoint.json').read_bytes()
print(json.dumps(dict(path=str(DEST / 'checkpoint.json'), sha256=sha(raw), files=len(rows),
                      bytes=sum(row['bytes'] for row in rows), synthetic_members=2315)))
