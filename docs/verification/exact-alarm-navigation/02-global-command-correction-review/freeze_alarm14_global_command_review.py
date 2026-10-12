"""Freeze the bounded independent review of the corrected global command gate."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import tarfile

root = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-global-command-review')
result = json.loads((root / 'result.json').read_bytes())
assert result['status'] == 'CORRECTED_WHOLE_REPORT_REJECTS_UNPLANNED_SETTINGS_INPUT'
assert result['mutated_result_rejected'] and result['restored_comparison_exactly_equals_positive']
assert (root / 'positive-comparison.json').read_bytes() == (root / 'restored-comparison.json').read_bytes()
review = json.loads((root / 'source-review.json').read_bytes())
assert [row['reviewed_sha256'] for row in review['reviewed_files']] == [
    'ff109d74e7921404bdebd1fefa1ac4b9ea1fa02ae2dd0bb250fc9244c20e4f31',
    '8df94ea60ffd85380864b05f61eb70a7c61c140aab270aead5254d64a75a9d61']
verified = []
for container, inventory_name in [('synthetic-artifacts.tar.gz', 'artifact-members.json'),
                                  ('reviewed-source.tar.gz', 'source-files.json')]:
    rows = json.loads((root / inventory_name).read_bytes())
    expected = {row['path']: row for row in rows}
    assert len(expected) == len(rows)
    seen = set()
    with tarfile.open(root / container, 'r:gz') as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            assert not name.is_absolute() and '..' not in name.parts and name.as_posix() == member.name
            assert member.isfile() and member.name in expected and member.name not in seen
            row = expected[member.name]
            with archive.extractfile(member) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            assert member.size == row['bytes'] and member.mode == row['mode'] and digest == row['sha256']
            seen.add(member.name)
    assert seen == set(expected)
    verified.append(dict(path=container, members=len(seen), exact_member_bytes_and_modes=True))
(root / 'archive-verification.json').write_text(json.dumps(verified, indent=2) + '\n')
(root / 'README.md').write_text('''# Corrected alarm14 global-command boundary

The exact second source attempt rejects the preserved whole-report extra-input
counterexample and still accepts the intended synthetic fourteen-screen journey.
This review is separate from the immutable first-attempt false acceptance in
the sibling `01-global-input-counterexample` directory, published at commit
`811f979eda1b937917c18defef38455c49a59062`.

The reviewer executed three complete comparisons against unchanged source:
the full positive fixture, the same report with one appended
`['shell', 'input tap 20 20']` record, and exact positive restoration. The added
command has distinct streams and finite times after every terminal capture.
The new comparison rejects it with the global mutation ownership error. The
restored complete comparison equals the positive object exactly. A separate
direct readiness-verifier control also rejects nonchronological placement.

The bounded source review covered only the two production deltas recorded in
`reviewed-delta.patch`: `exact_alarm_journey.py` and `editor_journey.py`. The
gate accounts for 26 planned inputs and six install/launch/removal mutations
in exact order, claims distinct resolved stream paths and physical inodes,
and classifies other commands through a canonical finite recorder grammar.
Ordinary allowlisted evidence commands are intentionally permitted. The new
comparator call and recorded uninstall role are restricted to schema6's exact
alarm plan. This read found no further concrete blocker in those deltas.

The two archives preserve all 98 reviewed source files and all 1,418 synthetic
artifact files, with each member's bytes and mode verified. The source inventory
was unchanged after the review. The fixture uses the observed explanation
dialog and an explicitly synthetic Settings destination. No Android device,
Settings input or subprocess was executed by this review. Full new and legacy
host suites and any actual device result remain separate work. This capsule
does not activate source or workflows or establish runtime parity.
''')
(root / 'freeze_alarm14_global_command_review.py').write_bytes(Path(__file__).read_bytes())
files = []
for path in sorted(root.iterdir()):
    if path.is_dir():
        continue
    assert stat.S_ISREG(path.lstat().st_mode)
    raw = path.read_bytes()
    mode = stat.S_IMODE(path.lstat().st_mode)
    assert mode in (0o644, 0o755)
    files.append(dict(path=path.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), mode=mode))
checkpoint = dict(schema=1, created_utc=datetime.now(timezone.utc).isoformat(),
                  status=result['status'],
                  repo_target='docs/verification/exact-alarm-navigation/02-global-command-correction-review',
                  active_files=[], files=files, android_executed_here=False,
                  actual_settings_input_executed=False, reviewed_source_unchanged=True)
raw = (json.dumps(checkpoint, indent=2) + '\n').encode()
with (root / 'checkpoint.json').open('xb') as stream:
    stream.write(raw)
print(json.dumps(dict(path=str(root / 'checkpoint.json'), bytes=len(raw),
                      sha256=hashlib.sha256(raw).hexdigest(), files=len(files),
                      payload_bytes=sum(row['bytes'] for row in files))))
