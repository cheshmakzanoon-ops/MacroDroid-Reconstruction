for local, target, digest in [
 ('trigger-catalog-forward/checkpoints/05-physical-identity-host-success', 'work-in-progress/trigger-category/05-physical-identity-host-success', '8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743'),
 ('trigger-category-review/physical-guard-review', 'docs/verification/capture-order-review/03-physical-identity-acceptance', '6d3de39c65e2cfa38b7a5efb7f03c98e7bd198e560c39139f9575d26c16d7a11'),
 ('normal-preflight-review/checkpoints/01-row-omission', 'docs/verification/normal-animation-preflight-review/01-row-omission', '9e4f226a9bd0aae287ae366de637239c3e70b05a8dac71ac57a9ea174293f4f9'),
]:
 cp = package(local, target, digest)
 assert not cp.get('active_files', []) and not cp.get('active_changes', False)
 assert cp['android_executed'] is False

source = ROOT / 'animation-diagnostic/checkpoints/02-initial-workflow-controls'
target = 'work-in-progress/animation-diagnostic/02-initial-workflow-controls'
raw = (source / 'checkpoint.json').read_bytes()
assert sha(raw) == 'f1b3e4ba951e12f488cd84999cd72702ae272aa856081fc61560e09a31625589'
cp = json.loads(raw)
assert len(cp['files']) == 10 and cp['evidence_files'] == 1383
assert cp['android_executed'] is False and cp['active_changes'] is False
assert cp['status'] == 'INACTIVE_WORKFLOW_CONTROLS_PASSED_REVIEW_GAPS_PENDING'
prefixes.append(target)
archive_record = next(row for row in cp['files'] if row['path'] == 'offline-evidence.tar.gz')
for row in cp['files']:
 if row == archive_record:
  continue
 path = source / safe(row['path']); data = path.read_bytes()
 assert not path.is_symlink() and len(data) == row['bytes'] and sha(data) == row['sha256']
 save(target + '/' + row['path'], data, 0o755 if path.stat().st_mode & 0o111 else 0o644)
save(target + '/checkpoint.json', raw)

archive_path = source / 'offline-evidence.tar.gz'
parts = []; combined = hashlib.sha256(); count = 0
with archive_path.open('rb') as stream:
 while True:
  data = stream.read(8 * 1024 * 1024)
  if not data:
   break
  name = target + '/offline-evidence/complete-evidence.' + str(len(parts) + 1).zfill(2) + '.part'
  save(name, data)
  parts.append(dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
  count += len(data); combined.update(data)
assert count == archive_record['bytes'] == 102744757
assert combined.hexdigest() == archive_record['sha256'] == 'b62e9914e41608a8efe6030e3bba93bc3e8d40fa94739c678ead965d1f710885'
manifest_path = target + '/offline-evidence/manifest.json'
jsave(manifest_path, dict(format='macrodroid-multipart-artifact', format_version=1,
 id='normal-animation02-closed-offline-evidence', filename='offline-evidence.tar.gz', media_type='application/gzip',
 purpose='Exact inactive Normal02 offline proof, including the historical guard and preflight gaps. No new Android execution.',
 size_bytes=count, sha256=combined.hexdigest(), parts=parts))

inventory = json.loads((source / 'offline-evidence-manifest.json').read_text())
rows = {safe(row['path']): row for row in inventory['files']}
assert len(rows) == len(inventory['files']) == 1383
seen = set(); visible = []
with tarfile.open(archive_path, 'r|gz') as archive:
 for item in archive:
  if item.isdir():
   continue
  assert item.isfile(), item.name
  name = safe(item.name)
  assert name in rows and name not in seen, name
  data = archive.extractfile(item).read()
  row = rows[name]
  assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
  seen.add(name)
  readable = '/' not in name or name.startswith('commands/') or (name.startswith('private-inputs/ci-normal-animation/') and name.count('/') == 2 and name.endswith('.log'))
  if readable:
   save(target + '/review-evidence/' + name, data, 0o755 if item.mode & 0o111 else 0o644)
   visible.append(row)
assert seen == set(rows)
assert len(inventory['inert_symlink_controls']) == 1
assert inventory['inert_symlink_controls'][0]['restored_as_symlink'] is False
verification = subprocess.run(['python3', 'scripts/assemble_artifact.py', manifest_path, '--verify-only'], cwd=REPO, capture_output=True, text=True)
assert verification.returncode == 0, verification.stderr
jsave(target + '/offline-evidence/publication-verification.json', dict(
 exact_original_checkpoint_preserved=True, original_archive_path='offline-evidence.tar.gz',
 assembly_manifest='offline-evidence/manifest.json', archive_size_bytes=count, archive_sha256=combined.hexdigest(),
 original_archive_recompressed=False, assembled_duplicate_created=False, parts=len(parts),
 complete_original_archive_members_verified=len(seen), reviewable_members=visible,
 inert_symlinks_preserved_as_metadata_only=True, assembler_exit_code=verification.returncode,
 assembler_stdout=verification.stdout, assembler_stderr=verification.stderr,
 active_workflow_modified=False, android_executed=False, known_review_gaps_preserved=True))
save(target + '/PUBLICATION_LAYOUT.md', ('''# Exact archive publication layout

The immutable checkpoint and all nine source, inventory, and document files retain their exact bytes. The checkpoint's `offline-evidence.tar.gz` is preserved without recompression as thirteen ordered parts of at most 8 MiB under `offline-evidence/`. Its complete size is 102,744,757 bytes and SHA-256 is `b62e9914e41608a8efe6030e3bba93bc3e8d40fa94739c678ead965d1f710885`.

From the repository root, verify all parts and the complete original stream:

```sh
python3 scripts/assemble_artifact.py ''' + manifest_path + ''' --verify-only
```

To materialize the original archive, replace `--verify-only` with `--output /path/to/offline-evidence.tar.gz`. The archive's 1,383 regular files were individually checked against `offline-evidence-manifest.json`. Complete command metadata/streams and compact original reports are additionally visible under `review-evidence/`. One deliberately tested symlink remains inert metadata only; no link is recreated.

This is the initial inactive Normal02 proposal. Its measured offline commands remain preserved alongside the subsequently identified physical-alias and mutable-inventory gaps. The successful old controls do not establish that the proposal's preflight or capture guard is complete. The separate row-omission review is preserved under `docs/verification/normal-animation-preflight-review/01-row-omission/`; no Android or active workflow change was made by this publication.
''').encode())
receipts[target] = dict(files=10, exact_checkpoint_sha256=sha(raw), full_archive_bytes=count,
 full_archive_sha256=combined.hexdigest(), complete_archive_members=1383, parts=len(parts),
 source_archive_path_mapped_to_multipart_manifest=True, active_workflow_modified=False)

ops = 'docs/verification/repository-publication/2026-10-12-chronology-followups'
ops_rows = []
for path in [ROOT / 'prepare_chronology_followups_transfer.py', ROOT / 'chronology_followups_body.py',
 *[ROOT / 'closed-followups-transfer' / name for name in ['manifest.json', 'blobs.json', 'preparation.json', 'external-preservation.json', 'preserve_incoming.py', 'verify_remote.py', 'remote-verification.json']]]:
 name = 'scripts/' + path.name if path.parent == ROOT else 'closed/closed-followups-transfer/' + path.name
 data = path.read_bytes(); save(ops + '/' + name, data)
 ops_rows.append(dict(path=name, source_path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops + '/checkpoint.json', dict(scope='Exact preparation scripts and prior completed publication/fetch verification',
 previous_verified_commit='dfa130a90a271ad591dcdb86ec34ac4b6de8ddfb', files=ops_rows))
