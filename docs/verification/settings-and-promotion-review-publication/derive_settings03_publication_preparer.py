"""Add one explicit multipart archive representation to the inactive publisher."""
from pathlib import Path
import difflib
import hashlib
import json

root = Path('/dev/shm/macrodroid-transfer-space-20261012')
source = root / 'prepare_standard_capsules.py'
before = source.read_text()
old = """        staged(path, prefix + '/' + row['path'])
"""
new = """        mapping = item.get('archive_mapping')
        if mapping and row['path'] == mapping['logical_path']:
            assert item['checkpoint_sha256'] == '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051'
            assert prefix == 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls'
            assert row['path'] == 'evidence.tar.gz' and row['bytes'] == 13014001
            assert row['sha256'] == '51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755'
            transport_root = Path(mapping['source'])
            manifest_raw = (transport_root / 'manifest.json').read_bytes()
            assert sha(manifest_raw) == mapping['manifest_sha256']
            transport = json.loads(manifest_raw)
            assert transport['format'] == 'macrodroid-multipart-artifact' and transport['format_version'] == 1
            assert transport['filename'] == row['path'] and transport['mode'] == '100644'
            assert transport['logical_repository_path'] == prefix + '/' + row['path']
            assert transport['source_checkpoint']['sha256'] == item['checkpoint_sha256']
            assert len(transport['parts']) == 2 and len({x['path'] for x in transport['parts']}) == 2
            checksum, byte_count = hashlib.sha256(), 0
            for index, part in enumerate(transport['parts'], 1):
                part_name = 'parts/evidence.' + str(index).zfill(4) + '.part'
                assert part['path'] == prefix + '/archive-layout/' + part_name
                part_file = transport_root / part_name
                info = part_file.lstat()
                assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
                payload = part_file.read_bytes()
                assert len(payload) == part['size_bytes'] and 0 < len(payload) <= 8388608
                assert sha(payload) == part['sha256']
                assert hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\\0' + payload).hexdigest() == part['git_blob_sha1']
                assert payload == data[byte_count:byte_count + len(payload)]
                checksum.update(payload)
                byte_count += len(payload)
            assert byte_count == row['bytes'] == transport['size_bytes']
            assert checksum.hexdigest() == row['sha256'] == transport['sha256']
        else:
            staged(path, prefix + '/' + row['path'])
"""
assert before.count(old) == 1
after = before.replace(old, new)
old_check = """                          bytes=sum(r['bytes'] for r in cp['files']), exact_bytes_and_modes_verified=True)
"""
new_check = """                          bytes=sum(r['bytes'] for r in cp['files']), exact_bytes_and_modes_verified=True)
    if item.get('archive_mapping'):
        checks[prefix]['archive_transport'] = dict(logical_path=item['archive_mapping']['logical_path'],
            direct_original_payloads=180, original_checkpoint_preserved=True,
            manifest_path=prefix + '/archive-layout/manifest.json',
            manifest_sha256=item['archive_mapping']['manifest_sha256'],
            complete_original_archive_byte_equality_verified=True,
            complete_capsule_requires_archive_reassembly=True)
"""
assert after.count(old_check) == 1
after = after.replace(old_check, new_check)
for name, data in [('prepare_settings03_capsules.py', after.encode()),
                   ('settings03-preparer-baseline.py', before.encode()),
                   ('settings03-publication-preparer.patch', ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='prepare_standard_capsules.py', tofile='prepare_settings03_capsules.py')).encode())]:
    with (root / name).open('xb') as stream:
        stream.write(data)
    (root / name).chmod(0o644)
result = dict(baseline_sha256=hashlib.sha256(before.encode()).hexdigest(),
              derived_sha256=hashlib.sha256(after.encode()).hexdigest(),
              exact_source_checkpoint='6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051',
              only_change='Verify every original payload, publish the sole exact 13,014,001-byte archive through two checksum-bound parts, and retain the original checkpoint unchanged.',
              active_source_changes=False)
with (root / 'settings03-preparer-derivation.json').open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
