#!/usr/bin/env python3
"""Freeze the separate failed and successful 57-control studies without relabeling coverage."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
BASELINE = '06986104338d570dd78e4abf34f2691756f772c8f6e521769a9ebf06ea97edbe'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, target):
    if source.is_symlink() or not source.is_file() or target.exists():
        raise RuntimeError('Fresh regular-file copy required: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Independent copy failed')


def rows(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Unexpected symlink')
        if path.is_file():
            result.append({'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['initial', 'final'], required=True)
    args = parser.parse_args()
    initial = args.stage == 'initial'
    directory = 'compiled-faults-08-initial' if initial else 'compiled-faults-09-final'
    name = '08-compiled-controls-type-error' if initial else '09-compiled-controls'
    report_root = HERE / 'reports' / directory
    result = json.loads((report_root / 'result.json').read_text())
    count = 56 if initial else 57
    wanted = 'COMPILED_FAULT_CONTROL_GATE_FAILED' if initial else 'COMPILED_FAULT_CONTROLS_PASSED'
    if result['status'] != wanted or result['passed'] is not (not initial):
        raise RuntimeError('Unexpected actual final control status: ' + result['status'])
    if result['controls_count'] != 57 or result['controls_detected'] != count or len(result['controls']) != 57:
        raise RuntimeError('Actual 57-control inventory differs')
    if result['baseline_checkpoint_sha256'] != BASELINE or not result['baseline_before']['reproduced']:
        raise RuntimeError('Positive baseline identity/reproduction differs')
    restored = result['baseline_restoration']
    if not (restored['reproduced'] and restored['source_matches_frozen'] and restored['class_matches_frozen'] and
            restored['exact_frozen_parity_match'] and restored['full_original_coverage_gate_passed'] is False):
        raise RuntimeError('Exact failed-coverage baseline was not restored')
    if len(result['class_origin_controls']) != 2 or not all(item['rejected_before_parity'] for item in result['class_origin_controls']):
        raise RuntimeError('Actual class-origin controls differ')
    for field in ['fixed_class_inventory_unchanged', 'fixture_unchanged', 'frozen_checkpoint_unchanged',
                  'host_checkpoint_unchanged', 'authored_inputs_unchanged']:
        if result[field] is not True:
            raise RuntimeError('Input changed: ' + field)
    failures = [item for item in result['controls'] if not item['detected']]
    if initial:
        if len(failures) != 1 or failures[0]['name'] != 'stop-dispatcher-identity' or failures[0]['compile_returncode'] != 1:
            raise RuntimeError('The preserved initial javac failure changed')
    elif failures:
        raise RuntimeError('Final controls contain an undetected fault')
    for item in result['controls']:
        if item['detected'] and not (item['compile_returncode'] == 0 and item['execution_returncode'] == 2 and
                item['failed_cases'] > 0 and item['named_failures_observed'] and item['original_coverage_unchanged'] and
                item['unsupported_executions'] == 0 and item['expected_result_failures'] == 0):
            raise RuntimeError('A detected control lacks actual bounded semantic evidence')
    destination = HERE / 'checkpoints' / name
    destination.mkdir(parents=True, exist_ok=False)
    for item in result['authored_inputs']:
        source = report_root / 'inputs' / item['path']
        if sha(source) != item['sha256'] or source.stat().st_size != item['bytes']:
            raise RuntimeError('Executed input differs')
        copy(source, destination / item['path'])
    for relative in ['create_video_mutation_catalog.py', 'freeze_video_compiled_controls.py']:
        copy(HERE / relative, destination / relative)
    document = 'COMPILED_CONTROL_STUDY_INITIAL.md' if initial else 'COMPILED_CONTROL_STUDY_FINAL.md'
    copy(HERE / document, destination / document)
    files = rows(destination)
    evidence = destination / 'evidence'
    for path in sorted(report_root.rglob('*')):
        if path.is_file():
            copy(path, evidence / 'run' / path.relative_to(report_root))
    prefix = 'full-faults' if initial else 'final-full-faults'
    for suffix in ['stdout.txt', 'stderr.txt']:
        copy(HERE / (prefix + '-' + suffix), evidence / (prefix + '-' + suffix))
    baseline = HERE / 'checkpoints/07-cast-source-original-jvm-coverage-gap/checkpoint.json'
    if sha(baseline) != BASELINE:
        raise RuntimeError('Frozen positive checkpoint changed')
    copy(baseline, evidence / 'baseline-checkpoint.json')
    if not initial:
        copy(HERE / 'checkpoints/08-compiled-controls-type-error/checkpoint.json', evidence / 'initial-failed-control-checkpoint.json')
    evidence_files = rows(evidence)
    archive = HERE / 'checkpoints' / (name + '-evidence.tar.gz')
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive member identity differs')
    if remaining:
        raise RuntimeError('Evidence omitted from archive')
    value = {'status': result['status'], 'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Inactive compiled method-only original/JVM controls; raw original coverage gate remains failed.',
        'control_gate_passed': not initial, 'controls': 57, 'detected': count,
        'cases_per_compiled_mutant': 1118, 'paths_per_compiled_mutant': 2,
        'raw_original_coverage_gate_passed': False, 'raw_original_instructions_visited': 259,
        'raw_original_instructions': 262, 'unvisited_original_offsets': [232, 233, 235],
        'original_conditional_edges_visited': 46, 'original_conditional_edges': 46,
        'positive_source_class_and_full_report_restored': True, 'origin_controls_rejected': 2,
        'coverage_exemption_implemented': False, 'active_source_changed': False,
        'rebuilt_dex_compared': False, 'apk_built': False, 'android_executed': False,
        'baseline_checkpoint_sha256': BASELINE, 'study_result_sha256': sha(report_root / 'result.json'),
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
