source = ROOT / 'combined-recovery/checkpoints/05-full-acceptance'
prefix = 'work-in-progress/combined-recovery/05-full-acceptance'
raw = (source / 'checkpoint.json').read_bytes()
assert sha(raw) == 'e4cd0b6af4cf95d7131138b3ad3dab8a070042cea077a80cf83c322168457063'
checkpoint = json.loads(raw)
assert checkpoint['passed'] is True and checkpoint['status'] == 'COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED'
assert checkpoint['input_files_rehashed'] == 81291 and checkpoint['registered_methods'] == 1242
assert checkpoint['cases'] == 193489 and checkpoint['python_tests'] == 273 and checkpoint['ui_fault_controls'] == 78
assert checkpoint['android_executed'] is False and checkpoint['whole_application_1_to_1_established'] is False
assert len(checkpoint['files']) == 125
for row in checkpoint['files']:
 if row['path'] == 'complete-reports.tar.gz':
  continue
 path = source / safe(row['path']); data = path.read_bytes()
 assert not path.is_symlink() and len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
 save(prefix + '/' + row['path'], data, 0o755 if path.stat().st_mode & 0o111 else 0o644)
save(prefix + '/checkpoint.json', raw)
prefixes.append(prefix)

report_record = next(row for row in checkpoint['files'] if row['path'] == 'complete-reports.tar.gz')
parts = []; stream_hash = hashlib.sha256(); total = 0
with (source / 'complete-reports.tar.gz').open('rb') as stream:
 while True:
  data = stream.read(8 * 1024 * 1024)
  if not data:
   break
  name = prefix + '/complete-reports/part-' + str(len(parts) + 1).zfill(4) + '.bin'
  save(name, data); stream_hash.update(data); total += len(data)
  parts.append(dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
assert total == report_record['bytes'] == 22556868
assert stream_hash.hexdigest() == report_record['sha256'] == 'a28998f55b333503050320465e1c977bcca11be7a81374169a810878476bca90'
report_manifest = prefix + '/complete-reports/manifest.json'
jsave(report_manifest, dict(format='macrodroid-multipart-artifact', format_version=1,
 id='combined05-complete-acceptance-reports', filename='complete-reports.tar.gz', media_type='application/gzip',
 purpose='Exact closed all-sixteen-gate host acceptance reports and all nested fault source/class artifacts.',
 size_bytes=total, sha256=stream_hash.hexdigest(), parts=parts))
manifest = json.loads((source / 'complete-reports-manifest.json').read_text())
assert manifest['file_count'] == len(manifest['files']) == 551
assert manifest['bytes'] == total and manifest['sha256'] == stream_hash.hexdigest()
expected = {row['path']: row for row in manifest['files']}; seen = set()
with tarfile.open(source / 'complete-reports.tar.gz', 'r|gz') as archive:
 for item in archive:
  if item.isdir():
   continue
  assert item.isfile()
  name = safe(item.name); assert name in expected and name not in seen
  data = archive.extractfile(item).read(); row = expected[name]
  assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
  seen.add(name)
assert seen == set(expected)

apk = json.loads((source / 'apk/manifest.json').read_text())
assert apk['size_bytes'] == 94683119 and apk['sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
assert len(apk['parts']) == 12 and apk['source_snapshot_sha256'] == checkpoint['source_snapshot_sha256']
for row in apk['parts']:
 assert row['path'].startswith(prefix + '/apk/')
 data = (REPO / safe(row['path'])).read_bytes()
 assert len(data) == row['size_bytes'] and sha(data) == row['sha256']
assembler = []
for name in (prefix + '/apk/manifest.json', report_manifest):
 run = subprocess.run(['python3', 'scripts/assemble_artifact.py', name, '--verify-only'], cwd=REPO, capture_output=True, text=True)
 assert run.returncode == 0, run.stderr
 assembler.append(dict(manifest=name, exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr))

old = json.loads((REPO / 'project/reports/release-input-snapshot.json').read_text())
new_raw = (source / 'project/reports/release-input-snapshot.json').read_bytes(); new = json.loads(new_raw)
assert old['snapshot_sha256'] == '19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183'
assert new['snapshot_sha256'] == checkpoint['source_snapshot_sha256'] == 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
assert new['files'] == len(new['entries']) == 81291 and new_raw.isascii()
changed = {name: value for name, value in new['entries'].items() if old['entries'].get(name) != value}
assert len(changed) == 63 and not set(old['entries']) - set(new['entries'])
bound = {row['path'][8:]: row for row in checkpoint['files'] if row['path'].startswith('project/') and row['path'] != 'project/reports/release-input-snapshot.json'}
assert set(bound) == set(changed)
changes = []
for name, after in changed.items():
 data = (source / 'project' / name).read_bytes()
 assert len(data) == after['size'] and sha(data) == after['sha256'] == bound[name]['sha256']
 before = old['entries'].get(name)
 path = REPO / 'project' / name
 if before is None:
  assert not path.exists()
 else:
  data = path.read_bytes(); assert len(data) == before['size'] and sha(data) == before['sha256'], name
 changes.append(dict(path='project/' + name, before=before, after=after))
jsave(prefix + '/publication-verification.json', dict(exact_checkpoint_preserved=True,
 verified_source_delta_files=63, added_inputs=46, removed_inputs=0, unchanged_prior_input_count=81245,
 exact_new_snapshot_file_sha256=sha(new_raw), new_snapshot_files=81291,
 complete_reports_verified=551, archive_recompressed=False, assembled_duplicates_created=False,
 exact_apk_parts=12, artifact_verification=assembler, source_changes=changes,
 current_source_and_apk_unchanged=True, android_executed=False, full_runtime_1_to_1_established=False))
save(prefix + '/PUBLICATION_LAYOUT.md', ('''# Complete closed acceptance publication

The original checkpoint and all 124 other listed files retain their exact bytes and modes. The original `complete-reports.tar.gz` is preserved without recompression as three ordered parts under `complete-reports/`; its 22,556,868-byte stream retains SHA-256 `a28998f55b333503050320465e1c977bcca11be7a81374169a810878476bca90`. Every one of its 551 original members was checked against `complete-reports-manifest.json`.

From the repository root, verify or reconstruct the exact report archive:

```sh
python3 scripts/assemble_artifact.py ''' + report_manifest + ''' --verify-only
python3 scripts/assemble_artifact.py ''' + report_manifest + ''' --output /path/to/complete-reports.tar.gz
```

The twelve APK parts and their literal `apk/manifest.json` paths remain unchanged. Their assembled stream is 94,683,119 bytes with SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. Both manifests were verified without creating another assembled file. Compact exact gate logs and reports are already visible under `commands/` and `reviewable/`.

All 63 changed/new build inputs match the new 81,291-entry snapshot and the current 19ea baseline delta; no input was removed. This publication preserves the closed sixteen-gate host proof and its immutable candidate. Android execution and active source/APK promotion are separate steps, and whole-application 1:1 remains unestablished.
''').encode())
receipts[prefix] = dict(checkpoint_sha256=sha(raw), original_files=125, archive_parts=3,
 full_report_members=551, apk_parts=12, input_delta=63, current_source_or_apk_changed=False)

doc_prefix = 'work-in-progress/combined-recovery/06-promotion-documentation'
docs = package('combined-recovery/checkpoints/06-promotion-documentation', doc_prefix,
 'f0403b172d2268ae9ff99072d829871c50518c08e3c7781508f76a96f6d773c3')
assert len(docs['files']) == 12 and docs['active_changes'] is False

ops = 'docs/verification/repository-publication/2026-10-12-combined-proof'
ops_rows = []
for path in [ROOT / 'prepare_combined_proof_transfer.py', ROOT / 'combined_proof_body.py',
 *[ROOT / 'normal-diagnostic-transfer' / name for name in ['manifest.json', 'blobs.json', 'preparation.json', 'activation-guards.json', 'external-preservation.json', 'verify_remote.py', 'remote-verification.json', 'checkout-observation.json']]]:
 name = 'scripts/' + path.name if path.parent == ROOT else 'closed/normal-diagnostic-transfer/' + path.name
 data = path.read_bytes(); save(ops + '/' + name, data)
 ops_rows.append(dict(path=name, source_path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops + '/checkpoint.json', dict(scope='Exact inactive proof preparation and completed reviewed-diagnostic publication/checkout',
 previous_verified_commit='3edcddd86660ea10c8aff71b651b446f86412525', files=ops_rows))
