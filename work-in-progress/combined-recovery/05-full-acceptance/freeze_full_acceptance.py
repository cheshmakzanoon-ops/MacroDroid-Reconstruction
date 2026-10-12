#!/usr/bin/env python3
"""Freeze the closed sixteen-gate combined source, reports and exact signed APK."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import shutil
import tarfile

from prepare_merge_overlay import identity, require, write_json
from run_combined_acceptance import verify_inputs

PIN = 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
PREPARATION_CHECKPOINT = 'da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6'
REMOTE = 'work-in-progress/combined-recovery/05-full-acceptance'
PART_BYTES = 8 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preparation-checkpoint', type=Path, required=True)
    parser.add_argument('--proof', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepared = args.preparation_checkpoint.resolve()
    proof_path = args.proof.resolve()
    require(identity(prepared / 'checkpoint.json')['sha256'] == PREPARATION_CHECKPOINT,
            'Unexpected reviewed source preparation')
    preparation_checkpoint = json.loads((prepared / 'checkpoint.json').read_text())
    for row in preparation_checkpoint['files']:
        require(identity(prepared / row['path']) == {key: row[key] for key in ('bytes', 'sha256')},
                'Reviewed source preparation changed: ' + row['path'])
    proof = json.loads(proof_path.read_text())
    require(proof['status'] == 'COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED' and proof['passed'] is True,
            'Closed complete positive acceptance required')
    require((proof['cases'], proof['registered_methods'], proof['registry_classes'], proof['python_tests'],
             proof['ui_cases'], proof['ui_methods'], proof['independent_ui_checks'], proof['ui_fault_controls'])
            == (193489, 1242, 605, 273, 23174, 10, 15326, 78), 'Combined inventory differs')
    require(proof['inputs_verified_before'] is True and proof['inputs_verified_after'] is True
            and proof['source_input_snapshot_sha256'] == PIN and proof['input_files'] == 81291,
            'Closed source identity boundaries differ')
    root = Path(proof['project'])
    pin = verify_inputs(root, PIN)
    acceptance_path = root / 'reports/acceptance-latest.json'
    require(identity(acceptance_path) == proof['acceptance'], 'Closed acceptance report changed')
    acceptance = json.loads(acceptance_path.read_text())
    require(acceptance['host_acceptance_passed'] is True and acceptance['source_edit_probe_skipped'] is False
            and len(acceptance['commands']) == 16
            and all(row['passed'] is True and row['exit_code'] == 0 for row in acceptance['commands'])
            and acceptance['input_snapshot_before'] == acceptance['input_snapshot_after'] == PIN,
            'Complete gate outcomes or source identity differ')
    for row in acceptance['commands']:
        require(identity(root / row['log'])['sha256'] == row['log_sha256'], 'Gate log changed')
    for name, digest in acceptance['fresh_evidence_sha256'].items():
        require(identity(root / 'reports' / name)['sha256'] == digest, 'Fresh report changed: ' + name)
    for variant, row in proof['apks'].items():
        require(identity(root / row['path']) == {key: row[key] for key in ('bytes', 'sha256')},
                'Signed APK changed: ' + variant)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    files = []

    def add(path, relative):
        expected = identity(path)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        require(identity(target) == expected and identity(path) == expected, 'Copy changed: ' + str(path))
        files.append({'path': relative, **expected})

    add(proof_path, 'result.json')
    add(acceptance_path, 'reviewable/acceptance-latest.json')
    for name in ('run_combined_acceptance.py', 'prepare_merge_overlay.py', 'freeze_full_acceptance.py'):
        add(Path(__file__).resolve().parent / name, name)
    for row in proof['commands']:
        log = proof_path.parent / row['log']['path']
        require(identity(log) == {key: row['log'][key] for key in ('bytes', 'sha256')}, 'Wrapper log changed')
        add(log, 'commands/' + log.name)
    for row in preparation_checkpoint['files']:
        if row['path'].startswith('project/'):
            relative = row['path'][len('project/'):]
            if relative in pin['entries']:
                require(identity(root / relative) == identity(prepared / row['path']), 'Reviewed source delta changed')
                add(root / relative, 'project/' + relative)
    add(root / 'reports/release-input-snapshot.json', 'project/reports/release-input-snapshot.json')
    for name in acceptance['fresh_evidence_sha256']:
        add(root / 'reports' / name, 'reviewable/' + name)
    add(root / 'reports/python-unit-tests.log', 'reviewable/python-unit-tests.log')
    for row in acceptance['commands']:
        add(root / row['log'], 'commands/' + Path(row['log']).name)

    reports = []
    archive = output / 'complete-reports.tar.gz'
    with tarfile.open(archive, 'w:gz', format=tarfile.PAX_FORMAT) as target:
        for path in sorted((root / 'reports').rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in {'.pyc', '.pyo'}:
                continue
            require(not path.is_symlink(), 'Report symlink is not allowed')
            relative = path.relative_to(root / 'reports').as_posix()
            raw = path.read_bytes()
            row = {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            reports.append(row)
            info = tarfile.TarInfo(relative)
            info.size, info.mode, info.mtime = len(raw), 0o644, 0
            target.addfile(info, io.BytesIO(raw))
            require(identity(path) == {key: row[key] for key in ('bytes', 'sha256')}, 'Report changed while archiving')
    with tarfile.open(archive, 'r:gz') as target:
        members = target.getmembers()
        require(len(members) == len(reports) and len({member.name for member in members}) == len(reports),
                'Complete report archive inventory differs')
        for member, row in zip(members, reports):
            require(member.isfile() and member.name == row['path'] and member.size == row['bytes']
                    and hashlib.sha256(target.extractfile(member).read()).hexdigest() == row['sha256'],
                    'Archived report differs')
    files.append({'path': archive.name, **identity(archive)})
    write_json(output / 'complete-reports-manifest.json', {
        'filename': archive.name, **identity(archive), 'files': reports, 'file_count': len(reports),
        'all_members_independently_verified': True, 'all_nested_mutant_sources_and_classes_retained': True})
    files.append({'path': 'complete-reports-manifest.json', **identity(output / 'complete-reports-manifest.json')})

    apk = proof['apks']['hybrid']
    (output / 'apk').mkdir()
    parts = []
    joined, total = hashlib.sha256(), 0
    with (root / apk['path']).open('rb') as source:
        while data := source.read(PART_BYTES):
            relative = f'apk/part-{len(parts) + 1:04d}.bin'
            path = output / relative
            path.write_bytes(data)
            expected = identity(path)
            require(expected == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}, 'APK part changed')
            files.append({'path': relative, **expected})
            parts.append({'path': REMOTE + '/' + relative, 'size_bytes': expected['bytes'],
                          'sha256': expected['sha256'],
                          'git_blob_sha1': hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest()})
            joined.update(path.read_bytes())
            total += len(data)
    require(total == apk['bytes'] and joined.hexdigest() == apk['sha256'], 'Split APK reconstruction differs')
    manifest = {'format': 'macrodroid-multipart-artifact', 'format_version': 1,
                'filename': 'MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk',
                'size_bytes': apk['bytes'], 'sha256': apk['sha256'], 'parts': parts,
                'source_snapshot_sha256': PIN, 'full_configured_host_acceptance_passed': True,
                'android_executed_for_this_candidate': False, 'whole_application_1_to_1_established': False}
    write_json(output / 'apk/manifest.json', manifest)
    files.append({'path': 'apk/manifest.json', **identity(output / 'apk/manifest.json')})
    require(verify_inputs(root, PIN) == pin, 'Source changed during freezing')
    for row in reports:
        require(identity(root / 'reports' / row['path']) == {key: row[key] for key in ('bytes', 'sha256')},
                'Closed report changed after freezing')
    readme = output / 'README.md'
    readme.write_text('''# Combined source: all sixteen acceptance gates passed

The exact combined plugin-upload and Widget candidate passed the complete
configured host acceptance suite, including signed baseline/hybrid assembly,
complete code and resource comparisons, all deliberate-fault families, the
signed source-edit experiment and final complete positive restoration.

The three-path comparison ran 193,489 cases across all 1,242 registered Java
method bodies in 605 classes, with zero mismatches or unsupported executions.
The UI group ran 23,174 cases over ten methods with 15,326 independent expected
checks. All 78 actual UI faults were detected and the full positive baseline
was restored exactly. All 273 Python tests passed. Sixteen gate logs, all 22
fresh report hashes, and 78 retained mutant source/class pairs were independently
rechecked after acceptance. Every closed report, including nested mutation
artifacts and the full input manifest, is preserved in the verified archive.

All 81,291 pinned source/tool/test inputs were independently rehashed before and
after acceptance and freezing. The source pin is
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`.
The 94,683,119-byte signed candidate SHA256 is
`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`;
its exact bytes are retained in twelve ordered, independently verified parts.
The baseline remains `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.

This is a completed local host/artifact measurement for the new combined input
pin. It is separate from previous isolated candidates and hosted/device runs.
It does not itself activate source or APKs, execute Android features, resolve
the observed old-candidate 26-pixel difference, or establish whole-app parity.
Most application logic remains editable smali and native/opaque dependencies
remain original binaries. The publisher's signing identity is unavailable.
''')
    files.append({'path': readme.name, **identity(readme)})
    checkpoint = {'status': 'COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED', 'passed': True,
                  'frozen_utc': datetime.now(timezone.utc).isoformat(),
                  'preparation_checkpoint_sha256': PREPARATION_CHECKPOINT,
                  'source_snapshot_sha256': PIN, 'input_files_rehashed': 81291,
                  'cases': 193489, 'registered_methods': 1242, 'registry_classes': 605, 'paths': 3,
                  'python_tests': 273, 'ui_cases': 23174, 'ui_methods': 10,
                  'independent_ui_checks': 15326, 'ui_fault_controls': 78,
                  'full_acceptance_executed': True, 'android_executed': False,
                  'active_source_changed': False, 'active_apk_changed': False,
                  'whole_application_1_to_1_established': False, 'apks': proof['apks'],
                  'reports': len(reports), 'fresh_report_hashes_verified': 22,
                  'files': sorted(files, key=lambda row: row['path'])}
    path = output / 'checkpoint.json'
    write_json(path, checkpoint)
    print(json.dumps({'checkpoint': str(path), **identity(path), 'files': len(files),
                      'reports': len(reports), 'apk_parts': len(parts)}, indent=2))


if __name__ == '__main__':
    main()
