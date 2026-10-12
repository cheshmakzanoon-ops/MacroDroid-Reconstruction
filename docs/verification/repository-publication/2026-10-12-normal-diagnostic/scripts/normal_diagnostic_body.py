normal_local = ROOT / 'animation-diagnostic/checkpoints/03-reviewed-workflow'
normal_prefix = 'work-in-progress/animation-diagnostic/03-reviewed-workflow'
normal = package('animation-diagnostic/checkpoints/03-reviewed-workflow', normal_prefix,
 '194ee4ddb8cbd31738f6f326b7e00365e0b0dafb99956708913cdb3327c1e172')
assert len(normal['files']) == 11 and not normal['android_executed'] and not normal['active_changes']
assert normal['workflow_sha256'] == '5bcd73aa15e5ad05de1fbcdf6252292249bf48458520bd6866477cd343af7047'
inventory = json.loads((normal_local / 'offline-evidence-manifest.json').read_text())
assert len(inventory['files']) == inventory['file_count'] == normal['evidence_files'] == 5070
assert inventory['unique_archived_payloads'] == normal['unique_archived_payloads'] == 215
payloads = {}
archive_path = normal_local / 'offline-evidence-blobs.tar.gz'
with tarfile.open(archive_path, 'r:gz') as archive:
 for item in archive:
  if item.isdir():
   continue
  assert item.isfile() and safe(item.name) == item.name and item.name not in payloads
  data = archive.extractfile(item).read()
  assert item.name == 'blobs/sha256/' + sha(data) + '.bin'
  payloads[item.name] = data
assert len(payloads) == 215
external = {}
for digest, row in inventory['exact_already_published_runtime_inputs'].items():
 path = Path(row['source']); data = path.read_bytes()
 assert not path.is_symlink() and sha(data) == row['sha256'] == digest and len(data) == row['bytes']
 if row['durable_manifest'] in ('vendor/original/manifest.json', 'artifacts/current/manifest.json'):
  raw = subprocess.check_output(['git', 'show', row['durable_commit'] + ':' + row['durable_manifest']], cwd=REPO)
  value = json.loads(raw)
  assert value['sha256'] == digest and value['size_bytes'] == len(data)
 else:
  assert row['durable_manifest'] == 'vendor/v9/manifest.json'
  found = False
  for zip_path in (ROOT / 'recovered/MacroDroid_v9_Source.zip', ROOT / 'recovered/MacroDroid_v9_Toolchain.zip'):
   if not zip_path.exists():
    continue
   with zipfile.ZipFile(zip_path) as archive:
    names = [name for name in archive.namelist() if name.endswith('/tools/prebuilt/linux/aapt2') or name == 'tools/prebuilt/linux/aapt2']
    for name in names:
     if archive.read(name) == data:
      found = True
  assert found, 'AAPT2 must match the retained durable archive bytes'
 external[digest] = dict(bytes=len(data), sha256=digest, durable_commit=row['durable_commit'], durable_manifest=row['durable_manifest'])
seen = set(); used_payloads = set(); readable = []
for row in inventory['files']:
 name = safe(row['path']); assert name not in seen; seen.add(name)
 assert type(row['mode']) is int and row['mode'] & ~0o777 == 0
 if 'archive_member' in row:
  data = payloads[row['archive_member']]; used_payloads.add(row['archive_member'])
  assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
 else:
  assert row['external_input_sha256'] in external
  assert {key: row[key] for key in ('bytes', 'sha256')} == {key: external[row['external_input_sha256']][key] for key in ('bytes', 'sha256')}
  data = None
 keep = '/' not in name or name.startswith('commands/') or (name.startswith('private-inputs/ci-normal-animation/') and name.count('/') == 2 and name.endswith('.log'))
 if keep:
  assert data is not None
  save(normal_prefix + '/review-evidence/' + name, data, row['mode'])
  readable.append(row)
assert used_payloads == set(payloads)
jsave(normal_prefix + '/publication-verification.json', dict(
 exact_frozen_checkpoint_sha256='194ee4ddb8cbd31738f6f326b7e00365e0b0dafb99956708913cdb3327c1e172',
 complete_logical_evidence_files_verified=len(seen), unique_archived_payloads_verified=len(payloads),
 exact_external_references_verified=external, reviewable_members=readable,
 all_tar_members_regular_or_directories=True, inert_symlink_controls_preserved=True,
 new_android_execution_by_publisher=False, full_runtime_1_to_1_established=False))
archive_data = archive_path.read_bytes()
jsave(normal_prefix + '/evidence-manifest.json', dict(format='macrodroid-multipart-artifact', format_version=1,
 id='normal-animation03-complete-offline-proof', filename='offline-evidence-blobs.tar.gz', media_type='application/gzip',
 purpose='Exact deduplicated frozen proof payloads; restore each of the 5,070 paths using offline-evidence-manifest.json and its durable input references.',
 size_bytes=len(archive_data), sha256=sha(archive_data), parts=[dict(path=normal_prefix + '/offline-evidence-blobs.tar.gz',
 size_bytes=len(archive_data), sha256=sha(archive_data), git_blob_sha1=oid(archive_data))]))
receipts[normal_prefix].update(complete_logical_evidence_files=5070, unique_archive_payloads=215, external_inputs=3)

for local, target, digest in [
 ('normal-preflight-review/independent-03/checkpoint', 'docs/verification/normal-animation-preflight-review/02-complete-inventory-acceptance', '8f56d2a621578455d550377b6184e28dfb306902f10c052924401979580ebba8'),
 ('session-guard-forward/checkpoints/03-paired-components', 'work-in-progress/editor-session-chronology/03-paired-components', '88d3794b4343165321b14e520a8805db7cd1ebd10c97af6529f99441ec5eaa5c'),
 ('session-guard-forward/checkpoints/04-trigger05-session03-union', 'work-in-progress/editor-session-chronology/04-trigger05-session03-union', '9b457171561ff0de24a9219a8d5f215879bb6cc37c77637b695ae83eb0710afe'),
 ('tooling-validation/avd-reappearance-2026-10-12', 'docs/verification/android-environment/avd-retirement-2026-10-12/reappearance', '63d441fbab117a0a8e767cc68e1b2950438c1d9e6888dd6aa8b233cafb1f71cd'),
 ('tooling-validation/avd-payload-retirement-2026-10-12', 'docs/verification/android-environment/avd-retirement-2026-10-12/payload-retirement', '4bed6e9f9f0ed4ec324761eaba5ae926e006ce463d418dad2d0557f4c2b58e10'),
]:
 cp = package(local, target, digest)
 assert not cp.get('active_files', [])

session = ROOT / 'session-guard-forward/checkpoints/03-paired-components/reports/01-frozen02-false-positive'
members = json.loads((session / 'synthetic-artifact-manifest.json').read_text())
with zipfile.ZipFile(session / 'synthetic-artifacts.zip') as archive:
 assert len(archive.namelist()) == len(members) == 584
 assert set(archive.namelist()) == {row['path'] for row in members}
 for row in members:
  data = archive.read(safe(row['path']))
  assert len(data) == row['bytes'] and sha(data) == row['sha256']

for local, target, digest in [
 ('video-monitor-recovery/checkpoints/04-handler-dataflow-review', 'work-in-progress/video-monitor/04-handler-dataflow-review', '053ee22c427813258cc64f7363c150353ce1f5bbc8118aa12dbb9af049b8e754'),
 ('video-monitor-recovery/checkpoints/05-expanded-original-jvm-coverage-gap', 'work-in-progress/video-monitor/05-expanded-original-jvm-coverage-gap', '1e94ebcdb8644fbada96e702e4000d0268a5b1d22d5247e6a56e55c90b8ad0fe'),
]:
 cp = package(local, target, digest)
 assert cp['android_executed'] is False
 tar_bundle(cp, target)

dependency_check = json.loads((ROOT / 'normal-preflight-review/independent-03/checkpoint/repository-dependency-check.json').read_text())
for row in dependency_check['files']:
 data = (REPO / row['path']).read_bytes()
 assert len(data) == row['bytes'] and sha(data) == row['sha256']
workflow_path = '.github/workflows/editor-normal-animation.yml'
assert not (REPO / workflow_path).exists() and not (REPO / workflow_path).is_symlink()
workflow = (normal_local / workflow_path).read_bytes()
assert sha(workflow) == '5bcd73aa15e5ad05de1fbcdf6252292249bf48458520bd6866477cd343af7047'
save(workflow_path, workflow)
jsave(normal_prefix + '/activation-verification.json', dict(
 active_files=[dict(path=workflow_path, expected_prior_state='absent', bytes=len(workflow), sha256=sha(workflow))],
 required_unchanged_repository_files=dependency_check['files'],
 current_apk_sha256='9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2',
 guard_checkpoint_used='8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743',
 reviewer_checkpoint_sha256='8f56d2a621578455d550377b6184e28dfb306902f10c052924401979580ebba8',
 active_application_source_changed=False, current_apk_promoted=False,
 runtime_result_pending=True, required_order='Observe this reviewed workflow checkout before separately authorized combined application promotion'))
(EXPORT / 'activation-guards.json').write_text(json.dumps(dict(
 absent_paths=[workflow_path], unchanged_files=dependency_check['files']), indent=2) + '\n')

ops = 'docs/verification/repository-publication/2026-10-12-normal-diagnostic'
ops_rows = []
for path in [ROOT / 'prepare_normal_diagnostic_transfer.py', ROOT / 'normal_diagnostic_body.py',
 *[ROOT / 'chronology-followups-transfer' / name for name in ['manifest.json', 'blobs.json', 'preparation.json', 'external-preservation.json', 'verify_remote.py', 'remote-verification.json']]]:
 name = 'scripts/' + path.name if path.parent == ROOT else 'closed/chronology-followups-transfer/' + path.name
 data = path.read_bytes(); save(ops + '/' + name, data)
 ops_rows.append(dict(path=name, source_path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops + '/checkpoint.json', dict(scope='Exact activation preparation and completed prior publication/fetch verification',
 previous_verified_commit='5bd6aba38bc4398b1d65c37f54b13608626fdff1', files=ops_rows))
