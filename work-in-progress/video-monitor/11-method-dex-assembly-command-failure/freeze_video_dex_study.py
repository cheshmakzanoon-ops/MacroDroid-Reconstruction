#!/usr/bin/env python3
"""Preserve each closed method-only compiler study with its exact measured scope."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, target):
    if source.is_symlink() or not source.is_file() or target.exists():
        raise RuntimeError('Fresh regular-file copy required')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Independent copy identity differs')


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
    args = parser.parse_args(); initial = args.stage == 'initial'
    run_name = 'method-only-three-path-11' if initial else 'method-only-three-path-12'
    name = '11-method-dex-assembly-command-failure' if initial else '12-method-only-three-path'
    run = HERE / 'reports' / run_name
    result = json.loads((run / 'result.json').read_text())
    if initial:
        if result['status'] != 'METHOD_ONLY_THREE_PATH_STUDY_FAILED' or result['error'] != 'RuntimeError: assemble-one-target returned 1':
            raise RuntimeError('Actual failed assembler outcome differs')
        if [(item['label'], item['returncode']) for item in result['commands']] != [('d8-one-helper', 0), ('disassemble-one-helper', 0), ('assemble-one-target', 1)]:
            raise RuntimeError('Failed run command sequence differs')
        if (run / 'positive').exists() or (run / 'pipeline-output/rebuilt-video-monitor.dex').exists():
            raise RuntimeError('The failed wrapper must not claim target DEX or application execution')
    else:
        if result['status'] != 'THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED' or result['passed'] is not False:
            raise RuntimeError('Actual complete three-path/raw-failed-coverage outcome differs')
        for key in ['positive_semantic_match', 'method_only_semantic_and_control_study_complete', 'all_controls_passed',
                    'fixed_class_inventory_unchanged', 'input_inventory_unchanged', 'frozen_baseline_unchanged',
                    'frozen_host_checkpoint_unchanged', 'jdk_inputs_unchanged', 'tool_jar_unchanged']:
            if result[key] is not True:
                raise RuntimeError('Actual proof prerequisite failed: ' + key)
        if not all(value is True for key, value in result['positive_restoration'].items() if key != 'returncode'):
            raise RuntimeError('Exact positive restoration changed')
    destination = HERE / 'checkpoints' / name; destination.mkdir(parents=True, exist_ok=False)
    for relative in ['video_method_dex_study.py', 'video_method_negative_control.py', 'tests/java/VideoDexStudy.java', 'tests/java/VideoDexLauncher.java']:
        copy(run / 'inputs' / relative, destination / relative)
    document = 'METHOD_ONLY_DEX_INITIAL_FAILURE.md' if initial else 'METHOD_ONLY_DEX_THREE_PATH.md'
    for relative in [document, 'PRIVATE_COVERAGE_PROPOSAL.md', 'freeze_video_dex_study.py']:
        copy(HERE / relative, destination / relative)
    files = rows(destination)
    evidence = destination / 'evidence'
    for path in sorted(run.rglob('*')):
        if path.is_file():
            copy(path, evidence / 'run' / path.relative_to(run))
    precompile = HERE / 'reports/dex-launcher-compile-11'
    for path in sorted(precompile.rglob('*')):
        if path.is_file():
            copy(path, evidence / 'launcher-javac-preflight' / path.relative_to(precompile))
    prefix = 'method-only-three-path' if initial else 'method-only-three-path-final'
    for suffix in ['stdout.txt', 'stderr.txt']:
        copy(HERE / (prefix + '-' + suffix), evidence / (prefix + '-' + suffix))
    if not initial:
        prior = HERE / 'checkpoints/11-method-dex-assembly-command-failure/checkpoint.json'
        copy(prior, evidence / 'initial-wrapper-failure-checkpoint.json')
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
            item = remaining.pop(member.name); data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive member identity differs')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    value = {'status': result['status'], 'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Failed private assembler invocation before application execution.' if initial else 'Private original/JVM/method-only rebuilt DEX semantic proof; strict raw original coverage gate remains failed.',
        'study_result_sha256': sha(run / 'result.json'), 'd8_compiler_passed': True,
        'target_assembled': not initial, 'application_method_compared': not initial,
        'coverage_exemption_implemented': False, 'active_source_changed': False, 'apk_built': False, 'android_executed': False,
        'raw_original_coverage_gate_passed': False, 'raw_original_instructions_visited': 259,
        'raw_original_instructions': 262, 'original_unvisited_offsets': [232, 233, 235],
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    if not initial:
        value['positive_cases'] = 1118; value['paths'] = 3; value['semantic_mismatches'] = 0
        value['unsupported_executions'] = 0; value['independent_expected_result_checks'] = 230
        value['expected_result_failures'] = 0; value['original_conditional_edges_visited'] = 46
        value['original_conditional_edges'] = 46; value['rebuilt_coverage'] = result['rebuilt_coverage']
        value['class_origin_and_fixture_controls'] = 2; value['actual_rebuilt_dex_faults_detected'] = 1
        value['positive_entire_report_and_inputs_restored'] = True
    manifest = destination / 'checkpoint.json'; manifest.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
