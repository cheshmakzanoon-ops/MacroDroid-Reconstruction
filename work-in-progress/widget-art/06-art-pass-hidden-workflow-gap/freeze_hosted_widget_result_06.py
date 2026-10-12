#!/usr/bin/env python3
"""Keep real ART success and the separate missing workflow-copy finding intact."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
ACTUAL = ROOT / 'hosted-run-38207925500'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    download = json.loads((ACTUAL / 'download-manifest.json').read_text())
    probe = json.loads((ACTUAL / 'extracted/probe/probe-result.json').read_text())
    failure = json.loads((ACTUAL / 'independent-verification/result.json').read_text())
    partial = json.loads((ACTUAL / 'probe-only-independent-verification.json').read_text())
    if (download['run_id'] != 38207925500 or
            sha(ACTUAL / 'artifact.zip') != '6e6124822bb17bf89b75a1683445b67c527d84ea575776bce315aff0e84a2607' or
            probe['status'] != 'ART_WIDGET_CASES_VERIFIED' or failure['passed'] is not False or
            'executed-inputs/.github/workflows/widget-method-probe.yml' not in failure['error'] or
            partial['passed_for_probe_scope'] is not True or
            partial['complete_artifact_input_copy_validation_passed'] is not False):
        raise RuntimeError('Recorded success and packaging failure must remain distinct')
    for item in download['files']:
        path = ACTUAL / 'extracted' / item['path']
        if path.is_symlink() or path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise RuntimeError('Actual downloaded evidence changed')
    missing = ACTUAL / 'extracted/executed-inputs/.github/workflows/widget-method-probe.yml'
    if missing.exists():
        raise RuntimeError('The missing file was inserted into the historical capture')
    supplemental = ACTUAL / 'supplemental-provenance/published-workflow.yml'
    if sha(supplemental) != 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7':
        raise RuntimeError('Supplemental exact-commit workflow differs')
    destination = ROOT / 'checkpoints/06-art-pass-hidden-workflow-gap'
    destination.mkdir(parents=True, exist_ok=False)
    names = ['artifact.zip', 'download-manifest.json', 'github-jobs.json', 'github-artifacts.json',
             'probe-only-independent-verification.json', 'verify-stdout.txt', 'verify-stderr.txt']
    for folder in ('extracted/probe', 'supplemental-provenance', 'independent-verification'):
        names += [path.relative_to(ACTUAL).as_posix() for path in sorted((ACTUAL / folder).rglob('*')) if path.is_file()]
    names += [path.relative_to(ACTUAL).as_posix() for path in sorted((ACTUAL / 'extracted').iterdir()) if path.is_file()]
    names += ['extracted/environment/queue/responses/widget-method-art.json']
    for name in names:
        source, target = ACTUAL / name, destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(source) != sha(target):
            raise RuntimeError('Evidence copy changed')
    shutil.copyfile(Path(__file__), destination / 'freeze_hosted_widget_result_06.py')
    (destination / 'README.md').write_text('''# Actual Widget ART success with a separate artifact input-copy gap

Run **38207925500**, job **114675450663**, commit
`c1a6d71d2e290d16ea3a047d036996f79005883a` completed successfully.
The actual `probe-result.json` is `ART_WIDGET_CASES_VERIFIED`. Both original and
candidate guest processes returned zero with identical eight-case stdout and
empty stderr. All 60 command identities and 120 raw streams pass an independent
recheck with the frozen, reviewed wrapper. Actual ADB CRLF output is preserved
and accepted by both exact AVD checks. Input and binary postchecks, read-only
guest files, and owned guest/service cleanup passed. No new Android commands
were executed during this local verification.

The independent complete-input-copy audit separately failed because the uploader
excluded `executed-inputs/.github/workflows/widget-method-probe.yml`. Its original
failed audit, traceback and executed verifier are retained unchanged. The exact
7,213-member downloaded ZIP also remains unchanged. No file was inserted into
its extraction to make that audit pass.

Supplemental provenance fetches the workflow at the exact published c1a6d71
commit: Git blob `5dc674dd2ce9572b5f61ae1e8ef794ef6ec81528`, 13,095 bytes,
SHA-256 `b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7`.
That exact source matches the workflow hash reported by the actual input
preflight. It is explicitly supplemental and is not represented as an archived
executed copy. The uploader's exact pinned action.yml is also preserved; its
`include-hidden-files` input defaults to false.

The next narrow workflow change enables hidden-file upload only within the
fresh owned `ci-widget-method/` output root, followed by a fresh actual run to
retain every input copy. The historical AVD-failed run remains failed; this
successful ART run keeps its separate artifact-copy limitation. Neither run
proves nonempty widget updates, rendering, or complete application runtime parity.
''')
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    result = {
        'status': 'ACTUAL_EIGHT_CASE_ART_SUCCESS_WITH_MISSING_ARCHIVED_WORKFLOW_COPY',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': download['run_id'], 'job_id': download['job_id'], 'head_sha': download['head_sha'],
        'artifact_id': download['artifact_id'], 'actual_probe_status': probe['status'],
        'actual_job_success': True, 'actual_raw_probe_independently_verified': True,
        'complete_artifact_input_copy_audit_passed': False, 'supplemental_workflow_blob_verified': True,
        'downloaded_zip_or_report_rewritten': False, 'fresh_complete_archive_run_required': True,
        'full_runtime_1_to_1_established': False,
        'original_probe_result': row(ACTUAL / 'extracted/probe/probe-result.json', ACTUAL),
        'failed_complete_copy_audit': row(ACTUAL / 'independent-verification/result.json', ACTUAL),
        'raw_probe_recheck': partial, 'archive': row(destination / 'artifact.zip', destination),
        'archive_members': download['files'], 'archive_members_hash_verified': True,
        'visible_files': files,
    }
    path = destination / 'checkpoint.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'sha256': sha(path), 'visible_files': len(files),
        'archive_members': len(download['files']), 'archive': result['archive']}, indent=2))


if __name__ == '__main__':
    main()
