#!/usr/bin/env python3
"""Freeze actual eight-case ART success and the complete unchanged downloaded ZIP."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
ACTUAL = ROOT / 'hosted-run-38209599059'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    download = json.loads((ACTUAL / 'download-manifest.json').read_text())
    proof = json.loads((ACTUAL / 'independent-verification/result.json').read_text())
    probe = json.loads((ACTUAL / 'extracted/probe/probe-result.json').read_text())
    if (download['run_id'] != 38209599059 or download['job_id'] != 114680586735 or
            download['head_sha'] != 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514' or
            sha(ACTUAL / 'artifact.zip') != 'ad8b7f1e9e6ecc34c2b32199da0c7d777298a9a2cf8a89a464eff5779d2d1cc5' or
            proof['passed'] is not True or proof['input_preflight_files_verified'] != 19 or
            proof['hidden_workflow_copy_in_original_downloaded_zip'] is not True or
            proof['command_count_verified'] != 60 or proof['raw_command_streams_verified'] != 120 or
            proof['fresh_output_tree_matches_reviewed_owned_scope'] is not True or
            probe['status'] != 'ART_WIDGET_CASES_VERIFIED' or len(download['files']) != 7214):
        raise RuntimeError('Complete independently accepted fresh evidence required')
    for item in download['files']:
        path = ACTUAL / 'extracted' / item['path']
        if path.is_symlink() or not path.is_file() or path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise RuntimeError('Actual downloaded evidence changed')
    historical = []
    for relative, expected in (
        ('checkpoints/03-hosted-avd-failure/checkpoint.json', 'ea5a1eef38b70cb45c0079aa4f63b48b66dedecf636a10b00157b571f3969eb3'),
        ('checkpoints/06-art-pass-hidden-workflow-gap/checkpoint.json', '6f12e96586f845000f0fe5cbb2f95c8e65e83de6c46113bdf92031ff75a423e4'),
        ('hosted-run-38206308421/artifact.zip', 'a860b5ca2b438db9c77e0ed362d4dcc8f2268ea29a767e931e370c29fb79afbe'),
        ('hosted-run-38207925500/artifact.zip', '6e6124822bb17bf89b75a1683445b67c527d84ea575776bce315aff0e84a2607'),
    ):
        path = ROOT / relative
        if sha(path) != expected:
            raise RuntimeError('Historical evidence changed')
        historical.append(row(path, ROOT))
    destination = ROOT / 'checkpoints/08-hosted-complete-proof'
    destination.mkdir(parents=True, exist_ok=False)
    names = ['artifact.zip', 'download-manifest.json', 'github-jobs.json', 'github-artifacts.json',
             'download-stdout.txt', 'download-stderr.txt', 'verify-stdout.txt', 'verify-stderr.txt']
    for folder in ('extracted/probe', 'extracted/executed-inputs', 'extracted/environment',
                   'extracted/toolchain', 'independent-verification'):
        names += [path.relative_to(ACTUAL).as_posix() for path in sorted((ACTUAL / folder).rglob('*')) if path.is_file()]
    names += [path.relative_to(ACTUAL).as_posix() for path in sorted((ACTUAL / 'extracted').iterdir()) if path.is_file()]
    if len(names) != len(set(names)):
        raise RuntimeError('Duplicate visible evidence name')
    for name in names:
        source, target = ACTUAL / name, destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
            raise RuntimeError('Frozen byte copy failed')
    for name in ('download_hosted_widget_result_08.py', 'verify_hosted_widget_result_08.py', 'freeze_hosted_widget_result_08.py'):
        shutil.copyfile(ROOT / name, destination / name)
    (destination / 'README.md').write_text('''# Real Widget ART comparison with all captured inputs preserved

Actual run **38209599059**, job **114680586735**, commit
`dbbb89cf4ca65edd3d2c2b96151dadf41aaec514` completed successfully. Its original
report is `ART_WIDGET_CASES_VERIFIED`. Independent read-only verification finished
at **2026-10-12T05:53:03.213053+00:00** and accepted the complete downloaded evidence.

The unchanged original APK and inactive Widget candidate each passed these eight
real ART cases using the actual APK classes and a one-class reflection probe:

| Case | Required observation |
| --- | --- |
| Fresh empty call | Real Unit singleton identity |
| Reused label zero | Reuse completes the empty operation |
| Resumed label two | Saved empty iterator completes |
| Invalid label | Exact exception class and message |
| Label-two dead cast L$7 | ClassCastException from malformed saved state |
| Label-two dead cast L$4 | ClassCastException from malformed saved state |
| Label-two dead cast L$1 | ClassCastException from malformed saved state |
| Null list | Expected exception type |

Both guest commands returned zero with identical 379-byte stdout
(`5fefb35053ba679c1f0aecdac3c93094023d348310537ba2b2b11653cce9efd7`)
and empty stderr. Original execution took 2.264 seconds and candidate execution
took 1.935 seconds. Both used the same bound `app_process64`, `-Xverify:all`,
explicit probe-plus-one-APK classpath, a 120-second guest timeout and 150-second
host timeout. The observed device environment, executable hashes, APK/probe
hashes before and after, exact CRLF AVD checks, and owned guest/service cleanup
are retained. No Android command was issued by the independent local audit.

The exact GitHub ZIP is **4,780,068 bytes**, SHA-256
`ad8b7f1e9e6ecc34c2b32199da0c7d777298a9a2cf8a89a464eff5779d2d1cc5`.
Every one of its **7,214 file members** is hash-bound and checked against the
fresh extraction. All nineteen executed input copies are inside this original
ZIP, including `.github/workflows/widget-method-probe.yml` with the reviewed
`f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba` hash.
The full output path set equals the previously reviewed owned output set plus
that exact hidden workflow; there are no additional paths. All sixty command
records and 120 raw streams pass the unchanged reviewed ART04 verifier.
The actual job also passed all thirty-one packaged wrapper tests and all six
downloader tests. Selected raw files are directly readable here, and the exact
ZIP preserves the entire host-control and environment evidence without rewriting.

The original APK is SHA-256
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`;
the candidate is
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`;
the unchanged probe DEX is
`79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07`.

The earlier AVD-policy-failed job remains failed. The earlier successful ART06
run retains its separate failed archived-workflow audit. Their frozen manifests
and original ZIP hashes are rechecked here, and no historical report or archive
has been patched or relabelled. This new proof applies only to the eight bounded
real method cases. It does not establish nonempty widget updates, rendering,
Android service behavior, or complete application runtime 1:1 parity.
''')
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    checkpoint = {
        'status': 'ACTUAL_EIGHT_CASE_ART_AND_COMPLETE_DOWNLOADED_EVIDENCE_VERIFIED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'run_id': download['run_id'],
        'job_id': download['job_id'], 'head_sha': download['head_sha'], 'artifact_id': download['artifact_id'],
        'actual_probe_status': probe['status'], 'actual_job_success': True,
        'actual_raw_probe_independently_verified': True, 'complete_artifact_input_copy_audit_passed': True,
        'archived_input_copies': 19, 'hidden_workflow_in_downloaded_zip': True,
        'recorded_commands_verified': 60, 'raw_streams_verified': 120,
        'downloaded_zip_or_report_rewritten': False, 'historical_evidence_unchanged': historical,
        'full_runtime_1_to_1_established': False, 'nonempty_widget_behavior_verified': False,
        'widget_rendering_verified': False,
        'original_probe_result': row(ACTUAL / 'extracted/probe/probe-result.json', ACTUAL),
        'independent_verification_result': row(ACTUAL / 'independent-verification/result.json', ACTUAL),
        'archive': row(destination / 'artifact.zip', destination), 'archive_members': download['files'],
        'archive_members_hash_verified': True, 'visible_files': files,
    }
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'visible_files': len(files),
        'archive_members': len(download['files']), 'archive': checkpoint['archive']}, indent=2))


if __name__ == '__main__':
    main()
