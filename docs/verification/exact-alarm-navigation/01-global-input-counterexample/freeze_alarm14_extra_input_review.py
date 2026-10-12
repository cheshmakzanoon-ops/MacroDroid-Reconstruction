"""Freeze the unchanged-source whole-report alarm14 extra-input counterexample."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

root = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-extra-input-review')
result = json.loads((root / 'result.json').read_bytes())
assert result['status'] == 'WHOLE_SYNTHETIC_REPORT_ACCEPTED_ONE_UNPLANNED_SETTINGS_INPUT'
assert (root / 'positive-comparison.json').read_bytes() == (root / 'extra-input-comparison.json').read_bytes()
verified = []
for container, inventory_name in [('synthetic-artifacts.tar.gz', 'artifact-members.json'),
                                  ('reviewed-source.tar.gz', 'source-files.json')]:
    expected = {row['path']: row for row in json.loads((root / inventory_name).read_bytes())}
    seen = set()
    with tarfile.open(root / container, 'r:gz') as archive:
        for member in archive:
            assert member.isfile() and member.name in expected and member.name not in seen
            row = expected[member.name]
            with archive.extractfile(member) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            assert member.size == row['bytes'] and member.mode == row['mode'] and digest == row['sha256']
            seen.add(member.name)
    assert seen == set(expected)
    verified.append(dict(path=container, members=len(seen), exact_member_bytes_and_modes=True))
(root / 'archive-verification.json').write_text(json.dumps(verified, indent=2) + '\n')
(root / 'README.md').write_text('''# Unplanned input accepted by the first alarm14 comparator

The exact first focused source attempt accepts an extra recorded Settings input
while reporting `settings_inputs: 0`. This is a whole-report counterexample using
the authored fourteen-screen fixture, not an Android execution.

The positive fixture includes all fourteen screens, the required readiness
phases, complete frame ledgers, process evidence and the exact new schema6 plan.
Its full comparator returns `EXACT_ALARM_SETTINGS_OBSERVATION_ONLY` with
`journey_equal: true`. The reviewer then appended one global command record:
`['shell', 'input tap 20 20']`, with distinct stdout/stderr artifacts and finite
chronological times after every terminal acquisition and existing command. No
screen, transition, policy, prior artifact or planned action was altered.

The complete comparison object remained byte-identical to the positive result,
including `settings_inputs: 0`. A separate direct readiness-verifier control
rejects a nonchronological placement of the appended record, showing that the
new record is not merely bypassing all global ledger inspection. That control
does not claim another whole-report replay. The original report object was
restored exactly after the two complete comparisons.

The source archive preserves all 98 exact files of the reviewed immutable
attempt. The artifact archive preserves all 1,414 synthetic evidence files,
including the added command streams. Both member inventories were checked
against every byte and mode; the source inventory was unchanged after review.
The authored fixture uses the actual observed exact-alarm explanation dialog
and an explicitly synthetic Settings destination. No Settings page was observed
on a device here, no input was executed, and no runtime parity is established.

A successor must account for all planned input records and classify the
remaining global command grammar. A command appended after the last accepted
screen cannot be ignored when the result declares that no Settings input was
used. This capsule leaves the reviewed source and previous proofs unchanged.
''')
(root / 'freeze_alarm14_extra_input_review.py').write_bytes(Path(__file__).read_bytes())
files = []
for path in sorted(root.iterdir()):
    if not path.is_file():
        continue
    raw = path.read_bytes()
    files.append(dict(path=path.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), mode='100644'))
checkpoint = dict(schema=1, created_utc=datetime.now(timezone.utc).isoformat(),
                  status=result['status'],
                  repo_target='docs/verification/exact-alarm-navigation/01-global-input-counterexample',
                  active_files=[], files=files, actual_android_or_input_executed=False,
                  first_source_attempt_unchanged=True)
raw = (json.dumps(checkpoint, indent=2) + '\n').encode()
with (root / 'checkpoint.json').open('xb') as stream:
    stream.write(raw)
print(json.dumps(dict(path=str(root / 'checkpoint.json'), bytes=len(raw),
                      sha256=hashlib.sha256(raw).hexdigest(), files=len(files),
                      payload_bytes=sum(row['bytes'] for row in files))))
