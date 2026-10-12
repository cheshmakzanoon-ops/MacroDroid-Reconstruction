#!/usr/bin/env python3
"""Preserve the actual failed job without changing its outcome or raw evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
ACTUAL = ROOT / 'hosted-run-38206308421'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    inputs = json.loads((ACTUAL / 'download-manifest.json').read_text())
    expected = {item['path']: item for item in inputs['files']}
    archive = ACTUAL / 'artifact.zip'
    if (archive.stat().st_size != 1_995_749 or
            sha(archive) != 'a860b5ca2b438db9c77e0ed362d4dcc8f2268ea29a767e931e370c29fb79afbe'):
        raise RuntimeError('Downloaded historical artifact changed')
    with zipfile.ZipFile(archive) as stream:
        members = [info for info in stream.infolist() if not info.is_dir()]
        if len(members) != len(expected):
            raise RuntimeError('Historical ZIP member count differs')
        seen = set()
        for member in members:
            item = expected[member.filename]
            data = stream.read(member)
            actual = ACTUAL / 'extracted' / member.filename
            if (member.filename in seen or len(data) != item['bytes'] or
                    hashlib.sha256(data).hexdigest() != item['sha256'] or
                    actual.is_symlink() or actual.read_bytes() != data):
                raise RuntimeError('Historical ZIP or extracted member differs')
            seen.add(member.filename)
    probe_root = ACTUAL / 'extracted/probe'
    report = json.loads((probe_root / 'probe-result.json').read_text())
    old_sha = 'c16dcf9376b1ea4de42ca51c63caeeb2ab157a5f4b89fcd0eea505182302d983'
    if (report['status'] != 'ART_WIDGET_EVIDENCE_INVALID' or
            report['evidence_error'] != 'Observed environment or state differs: avd-name' or
            report['wrapper_artifact']['sha256'] != old_sha or
            sha(probe_root / 'executed-wrapper.py') != old_sha or len(report['commands']) != 60):
        raise RuntimeError('Historical outcome or implementation is not the expected failure')
    for command in report['commands']:
        if command['returncode'] != 0 or command['timed_out'] is not False:
            raise RuntimeError('A guest/device command failed independently of the evidence parser')
        for kind in ('stdout', 'stderr'):
            item = command[kind]
            raw = probe_root / item['path']
            if raw.stat().st_size != item['bytes'] or sha(raw) != item['sha256']:
                raise RuntimeError('Command raw bytes differ')
        if not command['label'].startswith('push-') and command['stderr']['bytes']:
            raise RuntimeError('A strict command has unexpected stderr')
    for variant in ('original', 'candidate'):
        execution = report['executions'][variant]
        raw = probe_root / execution['command']['stdout']['path']
        if (execution['strict_command_passed'] is not True or
                raw.read_bytes() != report['expected_stdout'].encode() or
                sha(raw) != '5fefb35053ba679c1f0aecdac3c93094023d348310537ba2b2b11653cce9efd7'):
            raise RuntimeError('The bounded raw ART cases did not pass identically')
    raw_avd = (probe_root / '010-avd-name.stdout.txt').read_bytes()
    if raw_avd != b'MacroDroid_API35_Disposable\r\nOK\r\n':
        raise RuntimeError('Actual AVD output differs from the diagnosed response')
    runtime_predicate = raw_avd.decode().strip().splitlines() == ['MacroDroid_API35_Disposable', 'OK']
    evidence_predicate = raw_avd.decode().strip() == 'MacroDroid_API35_Disposable\nOK'
    if runtime_predicate is not True or evidence_predicate is not False:
        raise RuntimeError('The original parser disagreement was not reproduced')
    destination = ROOT / 'checkpoints/03-hosted-avd-failure'
    destination.mkdir(parents=True, exist_ok=False)
    names = ['artifact.zip', 'download-manifest.json', 'github-jobs.json', 'github-artifacts.json']
    names += [p.relative_to(ACTUAL).as_posix() for p in sorted(probe_root.iterdir()) if p.is_file()]
    names += [p.relative_to(ACTUAL).as_posix() for p in sorted((ACTUAL / 'extracted').iterdir()) if p.is_file()]
    names += ['extracted/environment/queue/responses/widget-method-art.json']
    for name in names:
        source, target = ACTUAL / name, destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(source) != sha(target):
            raise RuntimeError('Failed evidence copy changed')
    shutil.copyfile(Path(__file__), destination / 'freeze_hosted_avd_failure_03.py')
    (destination / 'README.md').write_text('''# Actual Widget Android job: preserved evidence-validator failure

Run **38206308421**, job **114670448046**, commit
`f050cfcfd70af4699f9145311b8628260c1ed17c` remains **failed**.
Its original `probe-result.json` remains `ART_WIDGET_EVIDENCE_INVALID`.
The exact downloaded GitHub artifact ZIP and every member binding are preserved.

Both real `app_process64 -Xverify:all` processes returned zero, emitted the same
379-byte eight-case stdout, and produced empty stderr. The 60 recorded device
commands returned zero without timeout. Input identities, device binary hashes,
read-only modes, environment checks and owned guest/service cleanup were retained.
This evidence is limited to eight empty-list/continuation/type-check cases. It
does not establish nonempty widget updates, rendering, or complete runtime parity.

The final host evidence check failed because the AVD console returned exactly
`MacroDroid_API35_Disposable\\r\\nOK\\r\\n`. The execution-time check split lines and
accepted that exact name and `OK`. The final evidence check compared a stripped
string with an internal LF-only separator, so its internal CR remained unequal.
The observed bytes were not rewritten. The original wrapper SHA-256 remains
`c16dcf9376b1ea4de42ca51c63caeeb2ab157a5f4b89fcd0eea505182302d983`.

A separate new parser policy and host replay must not relabel this job as passed.
A fresh Android run is required after review and publication of the correction.
''')
    files = [record(p, destination) for p in sorted(destination.rglob('*')) if p.is_file()]
    checkpoint = {
        'status': 'ACTUAL_ANDROID_JOB_FAILED_FINAL_AVD_EVIDENCE_GUARD',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': inputs['run_id'], 'job_id': inputs['job_id'], 'head_sha': inputs['head_sha'],
        'artifact_id': inputs['artifact_id'], 'source_report_status_unchanged': report['status'],
        'whole_job_passed': False, 'historical_report_relabelled': False,
        'observed_original_and_candidate_eight_case_stdout_equal': True,
        'observed_both_guest_exit_codes_zero': True, 'observed_both_guest_stderr_empty': True,
        'full_runtime_1_to_1_established': False, 'fresh_android_rerun_required': True,
        'old_wrapper_sha256': old_sha, 'original_probe_result': record(probe_root / 'probe-result.json', ACTUAL),
        'avd_stdout': record(probe_root / '010-avd-name.stdout.txt', ACTUAL),
        'old_execution_avd_predicate': runtime_predicate, 'old_evidence_avd_predicate': evidence_predicate,
        'archive': record(destination / 'artifact.zip', destination),
        'archive_members': inputs['files'], 'archive_members_hash_verified': True,
        'visible_files': files,
    }
    target = destination / 'checkpoint.json'
    target.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(target), 'sha256': sha(target), 'visible_files': len(files),
        'archive_members': len(expected), 'archive': checkpoint['archive']}, indent=2))


if __name__ == '__main__':
    main()
