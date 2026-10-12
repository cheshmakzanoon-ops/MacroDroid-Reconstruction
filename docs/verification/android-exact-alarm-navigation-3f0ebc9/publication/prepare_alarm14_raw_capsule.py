"""Preserve the closed Alarm14 CI container and every unchanged extracted member."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import stat
import zipfile

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
SPECS = [{'name': 'alarm14',
  'folder': 'alarm14-run-38240023189',
  'run': 38240023189,
  'artifact': 11742624179,
  'head': '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
  'bytes': 46626337,
  'sha256': 'c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04',
  'members': 3507,
  'expanded_bytes': 74601455,
  'prefix': 'docs/verification/android-exact-alarm-navigation-3f0ebc9',
  'title': 'Actual fourteen-screen exact-alarm navigation difference',
  'outcome': 'The observation and independent comparison steps failed after '
             'both fourteen-screen journeys completed. The literal reports '
             'record 35 differing pixels on intro-2, zero on the other '
             'thirteen screen pairs, and equal hierarchies. Both variants '
             'reached the Settings-owned surface after the observed '
             'explanation OK; no Settings input or permission grant occurred. '
             'Known post-crash continuations remain in the reports. These are '
             'the original reported outcomes; independent replay is preserved '
             'separately. Setup, all host controls, APK checks, runtime '
             'installation and complete evidence upload passed.'}]

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(path):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode)
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': st.st_size, 'sha256': sha, 'mode': stat.S_IMODE(st.st_mode)}

def write(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def link(source, destination):
    assert stat.S_ISREG(source.lstat().st_mode)
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, destination)
    assert identity(source) == identity(destination)

summaries = []
for spec in SPECS:
    original = BASE / spec['folder']
    archive = original / 'artifact.zip'
    assert identity(archive) | {'mode': 0o644} == {'bytes': spec['bytes'], 'sha256': spec['sha256'], 'mode': 0o644}
    receipt = json.loads((original / 'extracted-extraction.json').read_text())
    assert receipt['archive'] == {'bytes': spec['bytes'], 'sha256': spec['sha256']}
    assert (receipt['run_id'], receipt['artifact_id'], receipt['head_sha']) == (spec['run'], spec['artifact'], spec['head'])
    assert receipt['member_count'] == len(receipt['files']) == spec['members']
    assert receipt['expanded_bytes'] == spec['expanded_bytes']
    root = BASE / (spec['name'] + '-closed-raw-capsule')
    root.mkdir(exist_ok=False)
    listed = {row['path']: row for row in receipt['files']}
    assert len(listed) == spec['members']
    metadata = []
    with zipfile.ZipFile(archive) as container:
        assert len(container.infolist()) == spec['members']
        for info in container.infolist():
            path = PurePosixPath(info.filename)
            assert not info.is_dir() and not path.is_absolute() and '..' not in path.parts
            assert path.as_posix() == info.filename and '\\' not in info.filename
            assert not stat.S_ISLNK(info.external_attr >> 16)
            raw = container.read(info)
            row = listed.pop(info.filename)
            assert row == {'path': info.filename, 'bytes': len(raw), 'sha256': digest(raw)}
            source = original / 'extracted' / info.filename
            assert source.read_bytes() == raw
            link(source, root / 'extracted' / info.filename)
            metadata.append({'path': info.filename, 'bytes': len(raw), 'sha256': digest(raw),
                             'zip_mode': info.external_attr >> 16, 'zip_crc32': info.CRC,
                             'zip_timestamp': list(info.date_time),
                             'extracted_mode': stat.S_IMODE(source.lstat().st_mode)})
    assert not listed
    parts, whole, total = [], hashlib.sha256(), 0
    with archive.open('rb') as stream:
        while raw := stream.read(8 * 1024 * 1024):
            local = f'archive/part-{len(parts)+1:04d}.bin'
            target = root / local
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(raw)
            assert target.read_bytes() == raw
            parts.append({'path': spec['prefix'] + '/' + local, 'size_bytes': len(raw),
                          'sha256': digest(raw),
                          'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()})
            whole.update(raw)
            total += len(raw)
    assert total == spec['bytes'] and whole.hexdigest() == spec['sha256']
    write(root, 'manifest.json', {'format': 'macrodroid-multipart-artifact', 'format_version': 1,
          'id': spec['folder'], 'filename': archive.name, 'media_type': 'application/zip',
          'size_bytes': total, 'sha256': spec['sha256'], 'parts': parts,
          'source_commit': spec['head'], 'run_id': spec['run'], 'artifact_id': spec['artifact'],
          'purpose': 'Exact unchanged failed CI artifact; complete original bytes and all raw members retained',
          'whole_application_1_to_1_established': False})
    write(root, 'archive-member-metadata.json', {'schema': 1, 'archive_sha256': spec['sha256'],
          'all_member_bytes_equal_original_zip': True, 'files': metadata,
          'mode_note': 'Original ZIP modes remain in the exact archive; these extracted evidence copies retain their observed extraction modes.'})
    link(original / 'extracted-extraction.json', root / 'extraction-receipt.json')
    link(original / (archive.name + '.download.json'), root / 'download-receipt.json')
    for name in ['github-jobs.json', 'github-artifacts.json', 'github-run.json', 'key-scan-classification.json', 'initial-transport-observations.json', 'literal-transport-observations.json']:
        if (original / name).exists():
            link(original / name, root / name)
    for name in ['extract_artifact.py', 'download_verified_artifact.py', 'inspect_alarm14_transport.py']:
        link(original / name, root / 'publication' / name)
    shutil.copyfile(Path(__file__), root / 'publication' / Path(__file__).name)
    write(root, 'publication/reassembly-verification.json', {'run_id': spec['run'], 'archive': archive.name,
          'sha256': whole.hexdigest(), 'bytes': total, 'parts': len(parts),
          'complete_archive_reassembly_identity_verified_without_duplicate_assembly': True,
          'all_original_archive_members_equal_extracted_files': True, 'members': len(metadata),
          'completed_utc': datetime.now(timezone.utc).isoformat()})
    key_note = ('The emulator log contains one ephemeral ADB public-key line. The raw value is retained only in the original evidence; it is omitted from summaries. The extraction scan found no private-key or token pattern. '
                if spec['name'] == 'alarm14' else 'The extraction scan found no key or token pattern. ')
    (root / 'README.md').write_text(
        '# ' + spec['title'] + '\n\n' + spec['outcome'] + '\n\n'
        + f"Run [{spec['run']}](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/{spec['run']}) used exact commit `{spec['head']}`. "
        + f"Artifact `{spec['artifact']}` is {spec['bytes']:,} bytes, SHA-256 `{spec['sha256']}`. "
        + f"All {spec['members']:,} original members ({spec['expanded_bytes']:,} bytes) were compared byte-for-byte with [extracted/](extracted/) and are preserved unchanged.\n\n"
        + '## Reassemble the exact container\n\nFrom the repository root:\n\n```bash\n'
        + f"python3 scripts/assemble_artifact.py {spec['prefix']}/manifest.json --verify-only\n"
        + f"python3 scripts/assemble_artifact.py {spec['prefix']}/manifest.json\n```\n\n"
        + '[manifest.json](manifest.json) binds every repository part. [extraction-receipt.json](extraction-receipt.json) and '
        + '[archive-member-metadata.json](archive-member-metadata.json) retain all member identities and original ZIP mode metadata. '
        + 'The complete archive keeps the original ZIP bytes, timestamps and modes. '
        + key_note + '\n\n'
        + 'These files preserve an actual failed run. They do not establish full runtime parity or relabel a failed result as a success. '
        + 'No application source, APK or workflow is changed by this evidence publication.\n')
    rows = []
    for path in sorted(root.rglob('*')):
        if path.is_file():
            rows.append({'path': path.relative_to(root).as_posix(), **identity(path)})
    checkpoint = {'schema': 1, 'status': 'FROZEN_EXACT_FAILED_CI_ARTIFACT_AND_MEMBERS',
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'repo_target': spec['prefix'],
                  'scope': spec['outcome'], 'active_files': [], 'artifact_sha256': spec['sha256'],
                  'run_id': spec['run'], 'artifact_id': spec['artifact'], 'files': rows}
    write(root, 'checkpoint.json', checkpoint)
    final = identity(root / 'checkpoint.json')
    summaries.append({'source': str(root), 'target': spec['prefix'], 'checkpoint_sha256': final['sha256'],
                      'checkpoint_bytes': final['bytes'], 'files': len(rows),
                      'payload_bytes': sum(r['bytes'] for r in rows), 'parts': len(parts)})
write(BASE, 'alarm14-closed-artifact-capsules.json', summaries)
print(json.dumps(summaries))
