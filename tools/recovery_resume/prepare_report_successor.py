#!/usr/bin/env python3
"""Prepare the exact report-only source successor; never relax verification.

The large pins file is derived mechanically from its committed predecessor.
Run on an unmodified checkout matching the declared before-identities.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

OLD_COMMIT = '39250fac022aee5551f36782bafd72cabbc33718'
SOURCE_COMMIT = '46a7e331771da1b6559cf817dc776ebc3024739f'
CAPSULE = 'work-in-progress/day-trigger-lookup/14-ui-report-null-preservation'
BEFORE = {
    'tools/day_trigger_acceptance/inputs.py': '411ecfc5fb0b6142b9a89c03a2a07a21987f68d2876a6658604462c26ec4b3c2',
    'tools/day_trigger_acceptance/pins.json': '699a393a94843446f79b46c6c74ebde118a4d16cc3f255c8aa7a9cf8885ea7a0',
    'tools/day_trigger_acceptance/README.md': '22a7fdaf4803d156461643ff1d8b6c26914f4e48fafdc526e052c7d5b61ae5f7',
    'tools/day_trigger_acceptance/runtime-files.json': 'ae4d37a41a1e9c62e57715d6dbd63a481d14d8bd0052666ffccc78c0ecc84fe7',
    '.github/workflows/day-trigger-wip-acceptance.yml': '11f32372ed4fd7ac078eaa83de407e9867d88b3112bf1bf48f49f5513310f8fc',
}

def identity(data: bytes) -> dict:
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def encoded(value: object) -> bytes:
    return json.dumps(value, indent=2).encode() + b'\n'

def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError('Expected unique source text is missing: ' + old[:100])
    return text.replace(old, new, 1)

def prepare(root: Path, output: Path) -> dict:
    root = root.resolve()
    before = {name: (root / name).read_bytes() for name in BEFORE}
    for name, data in before.items():
        if identity(data)['sha256'] != BEFORE[name]:
            raise ValueError('Unreviewed source baseline: ' + name)
    checkpoint_raw = (root / CAPSULE / 'checkpoint.json').read_bytes()
    if identity(checkpoint_raw) != {'bytes': 23328, 'sha256': 'e14ff0e88f121acfa228a349b805f59ce3d703f377718df574021b07471f7ed4'}:
        raise ValueError('Serializer source checkpoint differs')
    cp = json.loads(checkpoint_raw)
    # All capsule paths, modes and bytes must match, not only the selected Java.
    import sys
    sys.path.insert(0, str(root / 'tools/day_trigger_acceptance'))
    import inputs
    specification = {'path': CAPSULE, 'checkpoint': identity(checkpoint_raw), 'file_count': 100}
    inputs.checked_capsule(root, specification)
    old = json.loads(before['tools/day_trigger_acceptance/pins.json'])
    pins = copy.deepcopy(old)
    pins['lookup_commit'] = SOURCE_COMMIT
    pins['lookup_capsules']['successor'] = specification
    pins['lookup_final_overlay_manifest'] = identity((root / CAPSULE / 'complete-future-overlay-manifest.json').read_bytes())
    pins['future_snapshot'] = cp['future_snapshot']
    pins['future_manifest'] = cp['future_manifest']
    key = 'tests/java/UiParityTests.java'
    new_java = (root / CAPSULE / 'project' / key).read_bytes()
    old_java = (root / old['lookup_capsules']['merge']['path'] / 'project' / key).read_bytes()
    expected = old_java.replace(b'Files.writeString(reportPath,G.toJson(report));',
                               b'Files.writeString(reportPath,G.newBuilder().serializeNulls().create().toJson(report));')
    if expected == old_java or expected != new_java:
        raise ValueError('Serializer successor is not the exact one-line change')
    changed = []
    for row in pins['lookup_source_changes']:
        if row['path'] == key:
            row['candidate'] = identity(new_java)
            changed.append(row['path'])
    if changed != [key]:
        raise ValueError('Unexpected lookup source changes')
    for row in pins['lookup_payload_resolutions']:
        if row['path'] == key:
            row['capsule'] = 'successor'
    # Require the complete successor manifest to agree with every final source row.
    overlay = json.loads((root / CAPSULE / 'complete-future-overlay-manifest.json').read_bytes())
    normalized = [{'path': r['path'], 'baseline': None if r['baseline'] is None else {k:r['baseline'][k] for k in ('bytes','sha256')},
                   'candidate': {k:r['after'][k] for k in ('bytes','sha256')},
                   'must_be_absent_if_new':r['must_be_absent_if_new'], 'source':'project/'+r['path']} for r in overlay['changes']]
    if normalized != pins['lookup_source_changes']:
        raise ValueError('Twenty-one-path source manifest mismatch')
    updated = {'tools/day_trigger_acceptance/pins.json': encoded(pins)}
    text = before['tools/day_trigger_acceptance/inputs.py'].decode()
    text = replace_once(text, "('day_lookup_dex_controls.py', 'tests/test_day_lookup.py'))", "('day_lookup_dex_controls.py', 'tests/test_day_lookup.py', 'tests/java/UiParityTests.java'))")
    text = replace_once(text, 'Lookup successor must replace exactly its two reviewed files', 'Lookup successor must replace exactly its three reviewed files')
    updated['tools/day_trigger_acceptance/inputs.py'] = text.encode()
    text = before['tools/day_trigger_acceptance/README.md'].decode()
    text = text.replace(OLD_COMMIT, SOURCE_COMMIT).replace('09-lookup-recorder-successor', '14-ui-report-null-preservation')
    text = text.replace(old['lookup_capsules']['successor']['checkpoint']['sha256'], specification['checkpoint']['sha256'])
    text = text.replace(old['future_snapshot']['snapshot_sha256'], pins['future_snapshot']['snapshot_sha256'])
    text = replace_once(text,
        'Lookup selects nineteen payloads from its merge capsule and only `day_lookup_dex_controls.py` and `tests/test_day_lookup.py` from its recorder successor.',
        'Lookup selects eighteen payloads from its merge capsule and exactly `day_lookup_dex_controls.py`, `tests/test_day_lookup.py` and `tests/java/UiParityTests.java` from its report-serializer successor. The first two files are byte-identical to the preceding recorder successor; only the final UI report writer changes.')
    text += '\n## Report serializer successor\n\nRun 38248170022 remains failed: all sixteen application gates passed, but the strict finalizer rejected five missing explicit-null `returnIndex` fields. Source capsule 14 changes only the final UI report writer to `G.newBuilder().serializeNulls().create().toJson(report)`. The shared Gson configuration, observer controls, case counts, runtime producer logic, all finalizer comparisons and all original evidence remain unchanged. This job must physically rescan the 81,304-input final tree and complete a new full acceptance run before any application promotion.\n'
    updated['tools/day_trigger_acceptance/README.md'] = text.encode()
    manifest = json.loads(before['tools/day_trigger_acceptance/runtime-files.json'])
    for row in manifest['files']:
        name = 'tools/day_trigger_acceptance/' + row['path']
        row.update(identity(updated.get(name, (root / name).read_bytes())))
    updated['tools/day_trigger_acceptance/runtime-files.json'] = encoded(manifest)
    text = before['.github/workflows/day-trigger-wip-acceptance.yml'].decode()
    text = replace_once(text, BEFORE['tools/day_trigger_acceptance/runtime-files.json'], identity(updated['tools/day_trigger_acceptance/runtime-files.json'])['sha256'])
    text = replace_once(text, OLD_COMMIT, SOURCE_COMMIT)
    text = replace_once(text, 'work-in-progress/day-trigger-lookup/09-lookup-recorder-successor', CAPSULE)
    updated['.github/workflows/day-trigger-wip-acceptance.yml'] = text.encode()
    if set(updated) != set(BEFORE):
        raise ValueError('Publication scope differs')
    records = []
    for name, data in sorted(updated.items()):
        (root / name).write_bytes(data)
        records.append({'path': name, 'before': identity(before[name]), 'after': identity(data)})
    receipt = {'schema': 1, 'status': 'SOURCE_SUCCESSOR_PREPARED_NOT_ACCEPTED',
               'source_commit': SOURCE_COMMIT, 'source_checkpoint': specification,
               'changed_tooling_files': records, 'changed_application_payloads': [key],
               'application_logic_changed': False, 'strict_finalizer_unchanged': True,
               'full_runtime_1_to_1_established': False}
    output.mkdir(parents=True, exist_ok=False)
    (output / 'source-change-receipt.json').write_bytes(encoded(receipt))
    return receipt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.repository, args.output), indent=2))
