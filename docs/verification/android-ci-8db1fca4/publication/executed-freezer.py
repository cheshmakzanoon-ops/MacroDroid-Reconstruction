"""Freeze the exact active numeric APK Android run and separate host-tool artifact."""
from pathlib import Path
from datetime import datetime, timezone
import errno
import hashlib
import json
import os
import shutil
import stat
import zipfile

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
SOURCE = ROOT / 'active-numeric-android-run-38247941263'
OUTPUT = ROOT / 'active-numeric-android-raw-capsule-02'
TARGET = 'docs/verification/android-ci-8db1fca4'
OUTPUT.mkdir(exist_ok=False)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def copy(source, name):
    info = source.lstat()
    assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
    before = source.read_bytes()
    destination = OUTPUT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, destination)
    except OSError as error:
        if error.errno != errno.EXDEV:
            raise
        with source.open('rb') as original, destination.open('xb') as target:
            shutil.copyfileobj(original, target)
        destination.chmod(0o644)
    assert destination.read_bytes() == source.read_bytes() == before

def write(name, raw):
    path = OUTPUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
    path.chmod(0o644)

def write_json(name, data):
    write(name, (json.dumps(data, indent=2) + '\n').encode())

specs = [
 ('artifact.zip', 'extracted', 'extracted-extraction.json', 'extraction-receipt.json',
  11746694777, 1017412, '1fb4a6375b9eb6b416c963f1d3e6d49733c9e5884d0081887bff96bec30fea04', 424, 2282601),
 ('tooling-host-tests.zip', 'tooling-host-tests', 'tooling-host-tests-extraction.json', 'tooling-host-tests-extraction-receipt.json',
  11746409254, 1300, 'e60238918c2fedfd0372f2058db9aa1a2f6060c8c2e6cc4ddc7e3678b04d7b14', 1, 5784),
]
artifacts = []
for filename, prefix, receipt_name, published_receipt, artifact_id, size, digest, count, expanded in specs:
    receipt = json.loads((SOURCE / receipt_name).read_bytes())
    assert receipt['archive'] == dict(bytes=size, sha256=digest)
    assert receipt['artifact_id'] == artifact_id and receipt['run_id'] == 38247941263
    assert receipt['head_sha'] == '8db1fca4f03532ee2e5a8791fde7ea18126c237f'
    assert receipt['member_count'] == len(receipt['files']) == count and receipt['expanded_bytes'] == expanded
    assert receipt['all_extracted_bytes_reverified'] is True and receipt['artifact_transformations'] == []
    assert receipt['key_scan_findings'] == []
    archive_raw = (SOURCE / filename).read_bytes()
    assert len(archive_raw) == size and sha(archive_raw) == digest
    with zipfile.ZipFile(SOURCE / filename) as archive:
        assert len(archive.infolist()) == count
        for row in receipt['files']:
            source = SOURCE / prefix / row['path']
            raw = source.read_bytes()
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
            assert archive.read(row['path']) == raw
            copy(source, prefix + '/' + row['path'])
    copy(SOURCE / filename, filename)
    copy(SOURCE / (filename + '.download.json'), filename + '.download.json')
    copy(SOURCE / receipt_name, published_receipt)
    artifacts.append(dict(artifact_id=artifact_id, archive_path=filename, bytes=size, sha256=digest,
                          member_count=count, expanded_bytes=expanded, extracted_prefix=prefix,
                          extraction_receipt=published_receipt, unchanged=True))
for name in ('github-jobs.json', 'github-artifacts.json'):
    copy(SOURCE / name, name)
jobs = json.loads((SOURCE / 'github-jobs.json').read_bytes())['jobs']
android = next(job for job in jobs if job['id'] == 114806467130)
assert android['status'] == 'completed' and android['conclusion'] == 'failure'
steps = {row['number']: row for row in android['steps']}
assert steps[8]['conclusion'] == 'failure'
assert steps[9]['name'] == 'Preserve measured runtime outcomes, including failures'
assert steps[9]['status'] == 'completed' and steps[9]['conclusion'] == 'success'
copy(ROOT / 'download_verified_artifact.py', 'publication/download_verified_artifact.py')
copy(Path('/workspace/scratch/4130730d15aa/ci-run-analysis/extract_artifact.py'), 'publication/extract_artifact.py')
copy(Path(__file__), 'publication/executed-freezer.py')
write_json('manifest.json', dict(schema=1, run_id=38247941263, head_sha='8db1fca4f03532ee2e5a8791fde7ea18126c237f',
           android_job_id=114806467130, android_job_conclusion='failure', artifacts=artifacts,
           all_425_raw_member_bytes_rechecked_against_original_zip=True, raw_transformations=[],
           detailed_independent_replay='SEPARATE_ANALYSIS', source_acceptance_result='STILL_RUNNING_AT_RETAINED_JOB_OBSERVATION',
           no_runtime_parity_claim=True, frozen_utc=datetime.now(timezone.utc).isoformat()))
write('README.md', b'''# Active numeric APK Android run: preserved comparison failure

This directory preserves the complete original Android and host-tool artifacts from run **38247941263** at active source commit **8db1fca4f03532ee2e5a8791fde7ea18126c237f**. The Android job **114806467130** completed with failure at its intro/post-intro comparison and constructor-probe step; its evidence upload succeeded. The separately running source acceptance job is not assigned a completed outcome from this Android result.

The original [artifact.zip](artifact.zip) is 1,017,412 bytes, SHA-256 `1fb4a6375b9eb6b416c963f1d3e6d49733c9e5884d0081887bff96bec30fea04`. All **424** raw members (2,282,601 bytes) are preserved unchanged under [extracted/](extracted/), with their complete [extraction receipt](extraction-receipt.json). The independent tooling ZIP has one exact 5,784-byte log and its own download/extraction receipts. Both original containers and every extracted member were rechecked byte-for-byte at freezing. The recorded key-pattern scans returned no matches.

The [cold comparison](extracted/capture/cold-launch-comparison.json), [intro comparison](extracted/capture/intro-comparison.json), [post-intro comparison](extracted/capture/post-intro-comparison.json), [constructor probe](extracted/constructor-probe/probe-result.json) and complete [job metadata](github-jobs.json) remain literal primary outputs. Detailed replay and cause analysis belong in a separate additive analysis; this raw publication neither changes an acceptance rule nor claims runtime parity.

The only artifact downloads were the two independently identified ZIPs recorded here. No raw member, APK, workflow or application source was modified by this preservation step.
''')
copy(ROOT / 'derive_active_numeric_android_raw_freezer02.py', 'publication/derive-freezer02.py')
for failed_path in sorted((ROOT / 'active-numeric-android-freezer-attempt-01').iterdir()):
    copy(failed_path, 'publication/attempt-01/' + failed_path.name)
copy(ROOT / 'active-numeric-android-freezer02.patch', 'publication/freezer02.patch')
files = []
for path in sorted(OUTPUT.rglob('*')):
    if path.is_file():
        raw = path.read_bytes()
        files.append(dict(path=str(path.relative_to(OUTPUT)), bytes=len(raw), sha256=sha(raw), mode=0o644))
write_json('checkpoint.json', dict(schema=1, status='EXACT_ACTIVE_NUMERIC_ANDROID_FAILURE_RAW_PRESERVED',
           repo_target=TARGET, active_files=[], run_id=38247941263, files=files))
print(json.dumps(dict(source=str(OUTPUT), target=TARGET, files=len(files),
                     bytes=sum(row['bytes'] for row in files), checkpoint_sha256=sha((OUTPUT / 'checkpoint.json').read_bytes()))))
