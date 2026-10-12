#!/usr/bin/env python3
"""Freeze all 58 actual expanded-harness faults with exact restoration."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
BASELINE = '02f80d76ee2fcf9d9cacf38f4b8d0fdd9c8697934daa190aa9c3450ab7cfc6ac'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, target):
    if source.is_symlink() or not source.is_file() or target.exists():
        raise RuntimeError('Fresh regular-file copy required')
    target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
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
    report_root = HERE / 'reports/compiled-faults-15-retry-delay'
    result = json.loads((report_root / 'result.json').read_text())
    if (result['status'] != 'ALL_COMPILED_FAULTS_DETECTED_EXACT_FAILED_COVERAGE_BASELINE_RESTORED' or result['passed'] is not True or
            result['controls_count'] != 58 or result['controls_detected'] != 58 or len(result['controls']) != 58 or
            result['baseline_checkpoint_sha256'] != BASELINE or not result['baseline_before']['reproduced']):
        raise RuntimeError('Actual 58-control result differs')
    restored = result['baseline_restoration']
    if not (restored['reproduced'] and restored['source_matches_frozen'] and restored['class_matches_frozen'] and
            restored['exact_frozen_parity_match'] and restored['full_original_coverage_gate_passed'] is False):
        raise RuntimeError('Exact failed-coverage baseline was not restored')
    if len(result['class_origin_controls']) != 2 or not all(item['rejected_before_parity'] for item in result['class_origin_controls']):
        raise RuntimeError('Origin controls failed')
    for key in ['fixed_class_inventory_unchanged', 'fixture_unchanged', 'frozen_checkpoint_unchanged', 'host_checkpoint_unchanged', 'authored_inputs_unchanged']:
        if result[key] is not True:
            raise RuntimeError('Input identity changed: ' + key)
    for item in result['controls']:
        if not (item['detected'] and item['compile_returncode'] == 0 and item['execution_returncode'] == 2 and item['cases'] == 1125 and
                item['failed_cases'] > 0 and item['named_failures_observed'] and item['original_coverage_unchanged'] and
                item['unsupported_executions'] == 0 and item['expected_result_failures'] == 0):
            raise RuntimeError('A control lacks actual bounded semantic detection')
    added = result['controls'][-1]
    if added['name'] != 'label-two-retry-always-suspends' or added['failed_cases'] != 4 or added['failed_case_labels'] != added['expected_failure_labels']:
        raise RuntimeError('Specific retry-delay counterexample differs')
    catalog = json.loads((report_root / 'inputs/video_method_mutants.json').read_text())
    previous = json.loads((HERE / 'video_method_mutants_final.json').read_text())
    if catalog['controls'][:-1] != previous['controls'] or len(previous['controls']) != 57:
        raise RuntimeError('Earlier 57 edits changed')
    destination = HERE / 'checkpoints/15-compiled-retry-controls'; destination.mkdir(parents=True, exist_ok=False)
    for item in result['authored_inputs']:
        source = report_root / 'inputs' / item['path']
        if sha(source) != item['sha256'] or source.stat().st_size != item['bytes']:
            raise RuntimeError('Executed input differs')
        copy(source, destination / item['path'])
    for relative in ['generate_video_retry_mutants.py', 'video_method_mutants_final.json', 'freeze_video_retry_controls.py', 'COMPILED_RETRY_CONTROL_PROOF.md']:
        copy(HERE / relative, destination / relative)
    files = rows(destination); evidence = destination / 'evidence'
    for path in sorted(report_root.rglob('*')):
        if path.is_file():
            copy(path, evidence / 'run' / path.relative_to(report_root))
    for suffix in ['stdout.txt', 'stderr.txt']:
        copy(HERE / ('retry-controls-' + suffix), evidence / ('retry-controls-' + suffix))
    for name, digest, label in [('13-retry-delay-original-jvm-coverage-gap', BASELINE, 'baseline'),
            ('10-compiled-controls', 'c8ba7485fb0a506e38c17cefdce190cd9c6c9765cf059a1b485f5f3719e14357', 'previous-57-control')]:
        path = HERE / 'checkpoints' / name / 'checkpoint.json'
        if sha(path) != digest:
            raise RuntimeError('Frozen predecessor changed')
        copy(path, evidence / (label + '-checkpoint.json'))
    evidence_files = rows(evidence)
    archive = HERE / 'checkpoints/15-compiled-retry-controls-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name); data = stream.extractfile(member).read()
            if not member.isfile() or len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive member differs')
    if remaining:
        raise RuntimeError('Archive omitted files')
    started, ended = (datetime.fromisoformat(result[key]) for key in ['started_utc', 'finished_utc'])
    value = {'status': result['status'], 'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Inactive expanded-harness compiled Java method controls; raw original coverage gate remains failed.',
        'control_gate_passed': True, 'controls': 58, 'compiled': 58, 'detected': 58,
        'previous_57_edits_unchanged': True, 'specific_retry_fault_mismatches': 4,
        'cases_per_compiled_mutant': 1125, 'paths_per_compiled_mutant': 2,
        'raw_original_coverage_gate_passed': False, 'raw_original_instructions_visited': 259,
        'raw_original_instructions': 262, 'unvisited_original_offsets': [232, 233, 235],
        'original_conditional_edges_visited': 46, 'original_conditional_edges': 46,
        'positive_source_class_and_full_report_restored': True, 'origin_controls_rejected': 2,
        'coverage_exemption_implemented': False, 'active_source_changed': False,
        'rebuilt_dex_compared': False, 'apk_built': False, 'android_executed': False,
        'measured_wall_seconds': (ended-started).total_seconds(),
        'measured_command_seconds': round(sum(row['seconds'] for row in result['commands']), 6),
        'baseline_checkpoint_sha256': BASELINE, 'study_result_sha256': sha(report_root / 'result.json'),
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    path = destination / 'checkpoint.json'; path.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'sha256': sha(path), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
