#!/usr/bin/env python3
"""Freeze the completed isolated upload proof, including executed faulty classes."""
from __future__ import annotations

import copy
import datetime
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import statistics
import tarfile


HERE = Path(__file__).resolve().parent
PROJECT = Path('/tmp/macrodroid-plugin-upload-tynqcwun/MacroDroid_v9')
DOCS = {'PLUGIN_UPLOAD_RECOVERY.md', 'UI_RECOVERY.md', 'FOLLOWON_ASSESSMENT.md'}


def sha(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def row(path: Path, name: str) -> dict:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('Expected a regular owned file: ' + str(path))
    return {'path': name, 'bytes': path.stat().st_size, 'sha256': sha(path)}


def transfer(source: Path, destination: Path, expected: str | None = None) -> dict:
    before = row(source, str(source))
    if expected is not None and before['sha256'] != expected:
        raise RuntimeError('Input hash mismatch: ' + str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copyfile(source, destination)
    after = row(destination, str(destination))
    if before['bytes'] != after['bytes'] or before['sha256'] != after['sha256']:
        raise RuntimeError('Copy mismatch: ' + str(destination))
    if source.stat().st_ino == destination.stat().st_ino and source.stat().st_dev == destination.stat().st_dev:
        raise RuntimeError('Mutable checkpoint must not use hardlinks')
    return after


def main() -> None:
    prior_path = HERE / 'checkpoints/02-original-jvm/checkpoint.json'
    prior = json.loads(prior_path.read_text())
    reports = PROJECT / 'reports'
    proof_path = reports / 'upload-signed-proof-03/result.json'
    resource_path = reports / 'upload-resource-proof-03/result.json'
    proof, resource = (json.loads(p.read_text()) for p in (proof_path, resource_path))
    controls = json.loads((reports / 'ui-negative-controls.json').read_text())
    roundtrip = json.loads((reports / 'hybrid-roundtrip.json').read_text())
    parity = json.loads((reports / 'java-all-path-parity.json').read_text())
    if (proof.get('passed') is not True or proof.get('status') != 'SIGNED_THREE_PATH_ALL_54_UI_CONTROLS_PASSED'
            or resource.get('passed') is not True or resource.get('status') != 'SIGNED_UPLOAD_RESOURCE_PROOF_PASSED'
            or proof['checkpoint_sha256'] != sha(prior_path) or resource['checkpoint_sha256'] != sha(prior_path)
            or resource['signed_proof_sha256'] != sha(proof_path)):
        raise RuntimeError('Completed source-bound signed and resource proof required')
    apk = Path(proof['apk']['path'])
    if (sha(apk) != proof['apk']['sha256'] or apk.stat().st_size != proof['apk']['bytes']
            or resource['apk'] != proof['apk'] or roundtrip.get('pass') is not True
            or roundtrip['apk_sha256'] != proof['apk']['sha256']):
        raise RuntimeError('Signed APK identity or independent roundtrip mismatch')
    if (parity.get('passed') is not True or parity['cases'] != 191147 or parity['methodsCovered'] != 1241
            or parity['methodsExpected'] != 1241 or parity['paths'] != 3
            or parity['failedCases'] != 0 or parity['unsupportedExecutions'] != 0
            or parity['exactMethodKeyPartitionVerified'] is not True
            or parity['apkSha256'] != proof['apk']['sha256']):
        raise RuntimeError('Complete exact three-path partition required')
    if (controls.get('pass') is not True or len(controls['controls']) != 54
            or controls.get('positiveRestorationPassed') is not True
            or controls.get('restorationCases') != 20832
            or controls.get('sourceFixtureAndApkUnchanged') is not True):
        raise RuntimeError('All 54 controls and clean restoration required')
    if len({r['mutation'] for r in controls['controls']}) != 54:
        raise RuntimeError('Duplicate controls')

    output = HERE / 'checkpoints/04-signed-proof'
    output.mkdir(parents=True, exist_ok=False)
    files, docs = [], []
    for old in prior['files']:
        source = PROJECT / old['path']
        if old['path'] not in DOCS and sha(source) != old['sha256']:
            raise RuntimeError('Implementation/test/fixture changed after positive proof: ' + old['path'])
        copied = transfer(source, output / old['path'])
        files.append({**old, 'sha256': copied['sha256'], 'bytes': copied['bytes'],
                      'original_jvm_checkpoint_sha256': old['sha256']})
        if old['path'] in DOCS:
            before = prior_path.parent / old['path']
            if sha(before) != old['sha256']:
                raise RuntimeError('Earlier frozen document changed')
            diff = ''.join(difflib.unified_diff(before.read_text().splitlines(True), source.read_text().splitlines(True),
                fromfile='checkpoint02/' + old['path'], tofile='checkpoint04/' + old['path']))
            patch = output / 'documentation-updates' / (old['path'] + '.patch')
            patch.parent.mkdir(parents=True, exist_ok=True)
            patch.write_text(diff)
            docs.append({'path': old['path'], 'before_sha256': old['sha256'],
                         'after_sha256': copied['sha256'], 'patch': row(patch, patch.relative_to(output).as_posix())})
    if len(files) != 35 or len(docs) != 3:
        raise RuntimeError('Unexpected source/documentation scope')
    patches = copy.deepcopy(prior['merge_patches'])
    for patch in patches:
        transfer(prior_path.parent / patch['path'], output / patch['path'], patch['sha256'])
        patch['prior_dry_run_only'] = True
        patch['integration_note'] = 'Recheck against current parent; preserve newer Widget/runtime/oracle/cleanup policies.'
    tools = []
    for name in ('run_upload_signed_build.py', 'run_upload_signed_proof.py', 'run_upload_resource_proof.py',
                 'freeze_upload_build_checkpoint.py', 'freeze_upload_final_checkpoint.py'):
        target = output / 'study-tools' / name
        transfer(HERE / name, target)
        tools.append(row(target, target.relative_to(output).as_posix()))
    recipe = output / 'isolated-build-recipe/build.py'
    transfer(PROJECT / 'build.py', recipe, proof['build_script_sha256'])

    evidence_sources = {}
    for p in sorted(reports.rglob('*')):
        if p.is_file():
            evidence_sources['reports/' + p.relative_to(reports).as_posix()] = p
    for p in sorted((PROJECT / 'build/negative-ui').rglob('*')):
        if p.is_file():
            evidence_sources['generated-ui-controls/' + p.relative_to(PROJECT / 'build/negative-ui').as_posix()] = p
    evidence_sources['prior-checkpoints/02-original-jvm.json'] = prior_path
    evidence_sources['prior-checkpoints/03-signed-build.json'] = HERE / 'checkpoints/03-signed-build/checkpoint.json'

    timing_rows = []
    for control in controls['controls']:
        if (control.get('pass') is not True or control.get('requiredCaseRejected') is not True
                or control.get('unsupportedExecutions') != 0 or control.get('exitCode') != 2
                or control.get('sourceFixtureAndApkUnchanged') is not True):
            raise RuntimeError('Fault control not correctly rejected')
        folder = PROJECT / 'build/negative-ui' / control['mutation']
        sources = list((folder / 'src').rglob('*.java'))
        classes = list((folder / 'classes').rglob('*.class'))
        if len(sources) != 1 or len(classes) != 1 or not (folder / 'result.json').is_file():
            raise RuntimeError('Missing exact executed mutant artifacts: ' + control['mutation'])
        mutant = json.loads((folder / 'result.json').read_text())
        if (control['requiredCase'] not in mutant['failedCaseLabels'] or mutant['paths'] != 3
                or mutant['unsupportedExecutions'] != 0 or mutant['cases'] != 20832):
            raise RuntimeError('Mutant evidence disagrees with control summary')
        timing_rows.append({'mutation': control['mutation'],
            'source_written_utc': datetime.datetime.fromtimestamp(sources[0].stat().st_mtime, datetime.timezone.utc).isoformat(),
            'completed_report_utc': datetime.datetime.fromtimestamp((folder / 'result.json').stat().st_mtime, datetime.timezone.utc).isoformat(),
            'observed_interval_seconds': round((folder / 'result.json').stat().st_mtime - sources[0].stat().st_mtime, 6),
            'mutated_source_sha256': sha(sources[0]), 'mutated_class_sha256': sha(classes[0]),
            'report_sha256': sha(folder / 'result.json'), 'cases': mutant['cases']})
    intervals = [r['observed_interval_seconds'] for r in timing_rows]
    timing = {'scope': 'Read-only source-write to completed-report timestamps, including javac and the full UI comparison; not per-subprocess stopwatch timing.',
        'completed_controls': 54, 'positive_restoration_cases': 20832,
        'stage_elapsed_seconds': proof['commands'][2]['elapsed_seconds'],
        'stage_measurement': 'Actual signed-proof wrapper monotonic stopwatch, including all controls and restoration.',
        'interval_min_seconds': min(intervals), 'interval_max_seconds': max(intervals),
        'interval_median_seconds': statistics.median(intervals), 'interval_sum_seconds': round(sum(intervals), 6),
        'controls': timing_rows}
    timing_path = output / 'evidence-summary/upload-control-timing-final.json'
    timing_path.parent.mkdir(parents=True)
    timing_path.write_text(json.dumps(timing, indent=2) + '\n')
    evidence_sources['summary/upload-control-timing-final.json'] = timing_path
    doc_record = output / 'evidence-summary/documentary-updates-after-proof.json'
    doc_record.write_text(json.dumps({'implementation_test_fixture_paths_unchanged': 32,
        'documentation_paths_updated_after_both_gates': docs,
        'signed_proof_sha256': sha(proof_path), 'resource_proof_sha256': sha(resource_path)}, indent=2) + '\n')
    evidence_sources['summary/documentary-updates-after-proof.json'] = doc_record
    evidence_rows = [row(p, name) for name, p in sorted(evidence_sources.items())]
    archive = HERE / 'checkpoints/04-signed-proof-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_rows:
            stream.add(evidence_sources[item['path']], arcname=item['path'], recursive=False)
    remaining = {r['path']: r for r in evidence_rows}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Evidence archive member mismatch')
    if remaining:
        raise RuntimeError('Evidence missing from archive')
    for item in evidence_rows:
        if sha(evidence_sources[item['path']]) != item['sha256']:
            raise RuntimeError('Evidence changed during freeze')
    for item in files:
        if sha(PROJECT / item['path']) != item['sha256']:
            raise RuntimeError('Candidate changed during freeze')
    if sha(apk) != proof['apk']['sha256']:
        raise RuntimeError('APK changed during freeze')

    checkpoint = copy.deepcopy(prior)
    checkpoint.update({
        'status': 'SIGNED_THREE_PATH_CODE_RESOURCE_ALL_54_CONTROLS_AND_RESTORATION_PASSED',
        'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Inactive isolated upload candidate; exact signed bounded three-path/code/resource proof. No Android execution or active/combined promotion.',
        'paths': 3, 'apk': proof['apk'], 'android_executed': False,
        'roundtrip': roundtrip, 'resources': resource['resource_report'],
        'negative_controls': {'behavioral_execution': True, 'total_ui_controls': 54, 'new_upload_controls': 17,
            'all_named_cases_rejected': True, 'unsupported_executions': 0, 'complete_result': controls,
            'actual_generated_artifact_files': 162, 'actual_generated_artifact_bytes': sum(r['bytes'] for r in evidence_rows if r['path'].startswith('generated-ui-controls/'))},
        'positive_restoration': {'passed': True, 'cases': 20832, 'paths': 3, 'source_fixture_apk_unchanged': True},
        'assembly': {'javac_passed': True, 'd8_passed': True, 'signed_apk_built': True,
            'rebuilt_dex_compared_to_apk': True, 'android_runtime_executed': False},
        'signed_proof': proof, 'resource_proof': resource,
        'source_checkpoint': {'path': str(prior_path), 'sha256': sha(prior_path)},
        'documentary_updates_after_proof': docs,
        'files': files, 'merge_patches': patches, 'study_tools': tools,
        'isolated_build_recipe': {**row(recipe, recipe.relative_to(output).as_posix()), 'merge_policy': 'Evidence only; do not overwrite parent build.py.'},
        'evidence_files': evidence_rows, 'evidence_file_count': len(evidence_rows),
        'evidence_bundle': row(archive, str(archive)), 'evidence_archive_members_hash_verified': True,
        'evidence_report': {'path': 'reports/upload-signed-proof-03/result.json', 'sha256': sha(proof_path)},
        'timing': timing, 'future_combined_candidate_requires_fresh_proof': True,
    })
    checkpoint['parent_policies_to_retain'] = [
        'build.py generated-directory cleanup', 'constructor-aware BytecodeOracle and numeric conformance',
        'Widget helper/stubs/cases and guarded constructor pipeline', 'Android recorder/runtime tests',
        'shared JVM -XX:-OmitStackTraceInFastThrow policy in all UI launchers']
    checkpoint['files_sha256'] = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    target = output / 'checkpoint.json'
    target.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(target), 'sha256': sha(target), 'candidate_files': len(files),
        'merge_patches': len(patches), 'study_tools': len(tools), 'evidence_files': len(evidence_rows),
        'evidence_bundle': checkpoint['evidence_bundle'], 'apk': checkpoint['apk'],
        'per_control_timestamp_interval': {k: v for k, v in timing.items() if k.startswith('interval_')}}, indent=2))


if __name__ == '__main__':
    main()
