#!/usr/bin/env python3
"""Retain the unexecuted workflow derivation and closed numeric input preparation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
OUT = BASE / 'workflow-authoring-draft-01'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def main():
    numeric = json.loads((BASE / 'numeric-input-01/result.json').read_bytes())
    assert numeric['passed'] is True and numeric['all_frozen_inputs_unchanged'] is True
    assert identity(Path(numeric['artifact']['path'])) == {k: numeric['artifact'][k] for k in ('bytes', 'sha256')}
    names = ['derive_workflow.py', 'materialize_numeric_input.py', 'freeze_workflow_authoring_draft.py',
        'numeric-input-01/executed-materialize_numeric_input.py', 'numeric-input-01/manifest.json',
        'numeric-input-01/read-input-identities.json', 'numeric-input-01/result.json']
    before = {name: identity(BASE / name) for name in names}
    OUT.mkdir(exist_ok=False)
    for name in names:
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BASE / name, target)
        target.chmod(0o644)
        assert identity(target) == before[name]
    (OUT / 'README.md').write_text('''# Settings enable-and-return workflow authoring draft

This checkpoint preserves the unexecuted workflow derivation helper and one completed preparation of the exact numeric APK. It contains no active workflow and no new Android execution. The source agent is still closing the six-path, 102-file Settings adapter package; the derivation requires its exact completed checkpoint before it can generate runnable workflow files.

The proposed workflow is derived from the closed fourteen-screen workflow `805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066`. It adds the two Settings controls already frozen in the observed design, requires schema 7 and the exact sixteen-screen plan `ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211`, and preserves all radio, runtime, full-frame, notification-readiness, command-order and owned-cleanup rules. The generated finalizer is intended to require 30 paired planned inputs, six setup mutations, four Settings inputs, the captured checked-on state and the observed app return. The on-state tree remains a prediction until captured, and no AlarmManager API result, configured trigger or saved/executed macro is claimed.

The helper switches the fixed candidate input to the signed host-accepted numeric APK with SHA-256 `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`. The original APK remains `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The successful [local preparation receipt](numeric-input-01/result.json) independently checks all twelve frozen candidate parts, reassembles exactly 94,683,136 bytes, and rehashes all source parts afterward. This only creates a read-only validation input; it does not build or install the APK.

The identical APK bytes are represented by the complete twelve-part manifest at `work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json`, SHA-256 `e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152`. Those parts are being published separately; this authoring checkpoint retains the manifest and preparation evidence without duplicating the same APK. Publication receipt and source/workflow validation are still pending at this checkpoint.

The proposed local workflow validation reuses the exact closed source package's complete host-test evidence; the future hosted workflow still executes the full suite. The new helper separately checks its literal preparation, new plan/policy/contract pins and both actual APKs, and preserves the inherited input mutation and owned-cleanup controls. The draft has only been parsed. Its generated workflow, new helper hashes, test results and activation will be separate concrete checkpoints.
''')
    assert before == {name: identity(BASE / name) for name in names}
    (OUT / 'draft-source-identities.json').write_text(json.dumps(before, indent=2) + '\n')
    files = [{'path': p.relative_to(OUT).as_posix(), 'mode': '100644', **identity(p)}
             for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': 'INACTIVE_SETTINGS_WORKFLOW_AUTHORING_DRAFT_NOT_EXECUTED',
        'repo_target': 'work-in-progress/exact-alarm-enable-return-workflow/00-authoring-draft',
        'finished_utc': datetime.now(timezone.utc).isoformat(), 'files': files, 'file_count': len(files),
        'payload_bytes': sum(row['bytes'] for row in files), 'active_files': [], 'android_executed': False,
        'workflow_generated': False, 'workflow_validation_executed': False}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': checkpoint['payload_bytes']}, indent=2))


if __name__ == '__main__':
    main()
