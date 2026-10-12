#!/usr/bin/env python3
"""Verify resources of the exact inactive upload APK after all UI controls close."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--signed-proof', type=Path, required=True)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, output = args.project.resolve(), args.output.resolve()
    checkpoint = json.loads(args.checkpoint.read_text())
    proof = json.loads(args.signed_proof.read_text())
    if (proof.get('passed') is not True or proof.get('status') != 'SIGNED_THREE_PATH_ALL_54_UI_CONTROLS_PASSED' or
            proof.get('checkpoint_sha256') != sha(args.checkpoint) or len(proof.get('commands', [])) != 3 or
            any(row.get('returncode') != 0 for row in proof['commands']) or
            proof['ui_controls']['count'] != 54 or proof['ui_controls']['restoration_cases'] != 20832):
        raise RuntimeError('The full signed proof, all54 controls and positive restoration must finish first')
    apk = root / 'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    if apk.stat().st_size != proof['apk']['bytes'] or sha(apk) != proof['apk']['sha256']:
        raise RuntimeError('The signed upload APK changed')
    for row in checkpoint['files']:
        if sha(root / row['path']) != row['sha256']:
            raise RuntimeError('Frozen upload input changed: ' + row['path'])
    output.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env['JAVA_HOME'] = str(args.jdk.resolve())
    env['PATH'] = str(args.jdk.resolve() / 'bin') + os.pathsep + env.get('PATH', '')
    argv = ['python3', 'resource_verify.py', '--variant', 'hybrid']
    report = {
        'status': 'RUNNING', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Exact signed upload candidate resource/ID/ZIP/native-preservation gate; no Android execution',
        'project': str(root), 'checkpoint_sha256': sha(args.checkpoint), 'signed_proof_sha256': sha(args.signed_proof),
        'apk': proof['apk'], 'argv': argv, 'timeout_seconds': 1200,
        'runner_sha256': sha(Path(__file__)), 'resource_verifier_sha256': sha(root / 'resource_verify.py'),
        'build_script_sha256': sha(root / 'build.py'), 'android_executed': False,
    }
    (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    started = time.monotonic()
    with (output / 'stdout.txt').open('wb') as stdout, (output / 'stderr.txt').open('wb') as stderr:
        try:
            completed = subprocess.run(argv, cwd=root, env=env, stdout=stdout, stderr=stderr, timeout=1200)
            report['returncode'], report['timed_out'] = completed.returncode, False
        except subprocess.TimeoutExpired:
            report['returncode'], report['timed_out'] = 124, True
    report['elapsed_seconds'] = round(time.monotonic() - started, 3)
    report['source_files_unchanged'] = all(sha(root / row['path']) == row['sha256'] for row in checkpoint['files'])
    report['apk_unchanged'] = sha(apk) == proof['apk']['sha256'] and apk.stat().st_size == proof['apk']['bytes']
    report['proof_record_unchanged'] = sha(args.signed_proof) == report['signed_proof_sha256']
    report['scripts_unchanged'] = all([
        sha(Path(__file__)) == report['runner_sha256'],
        sha(root / 'resource_verify.py') == report['resource_verifier_sha256'],
        sha(root / 'build.py') == report['build_script_sha256'],
    ])
    report['outputs'] = {name: {'bytes': (output / name).stat().st_size, 'sha256': sha(output / name)}
                         for name in ('stdout.txt', 'stderr.txt')}
    resource = root / 'reports/hybrid-resource-parity.json'
    if resource.exists():
        report['resource_report'] = json.loads(resource.read_text())
        report['resource_report_sha256'] = sha(resource)
    report['passed'] = (report['returncode'] == 0 and all(report[key] for key in (
        'source_files_unchanged', 'apk_unchanged', 'proof_record_unchanged', 'scripts_unchanged')) and
        report.get('resource_report', {}).get('pass') is True and
        report['resource_report'].get('apk_sha256') == proof['apk']['sha256'])
    report['status'] = 'SIGNED_UPLOAD_RESOURCE_PROOF_PASSED' if report['passed'] else 'SIGNED_UPLOAD_RESOURCE_PROOF_FAILED'
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
