def raw_zip(source_zip, source_dir, receipt_path, prefix, member_count):
 raw=receipt_path.read_bytes();receipt=json.loads(raw)
 assert receipt['run_id']==38214498395 and receipt['head_sha']=='dbcad968c5c3e8f084205393a6c0d2d06a203c71'
 assert receipt['member_count']==len(receipt['files'])==member_count and not receipt['key_scan_findings']
 data=source_zip.read_bytes();assert len(data)==receipt['archive']['bytes'] and sha(data)==receipt['archive']['sha256']
 archive_name=prefix+'/artifact.zip';save(archive_name,data)
 save(prefix+'/extraction-receipt.json',raw)
 jsave(prefix+'/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,
  id=prefix.replace('/','-'),filename=source_zip.name,media_type='application/zip',
  purpose='Exact unmodified hosted reconstruction evidence; preserve each recorded result and its finite scope.',
  size_bytes=len(data),sha256=sha(data),parts=[dict(path=archive_name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))],
  source_commit=receipt['head_sha'],run_id=38214498395,artifact_id=receipt['artifact_id'],whole_application_1_to_1_established=False))
 expected={r['path']:r for r in receipt['files']};seen=set();total=0
 with zipfile.ZipFile(source_zip) as archive:
  members=[m for m in archive.infolist() if not m.is_dir()]
  assert len(members)==member_count
  for member in members:
   name=safe(member.filename);assert name in expected and name not in seen
   assert (member.external_attr>>16)&0o170000!=0o120000
   data=archive.read(member);row=expected[name];assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
   p=source_dir/name;assert not p.is_symlink() and p.read_bytes()==data
   save(prefix+'/extracted/'+name,data,0o755 if p.stat().st_mode&0o111 else 0o644)
   total+=len(data);seen.add(name)
 assert seen==set(expected) and total==receipt['expanded_bytes']
 jsave(prefix+'/publication-verification.json',dict(all_members_verified=member_count,expanded_bytes=total,
  archive_sha256=receipt['archive']['sha256'],all_raw_bytes_preserved=True,recompressed=False,executed_artifacts=False))
 prefixes.append(prefix);receipts[prefix]=dict(raw_members=member_count,bytes=total,archive_sha256=receipt['archive']['sha256'])

raw_prefix='docs/verification/android-ci-dbcad968'
raw_zip(ROOT/'tooling-validation/android-cold-launch-run-38214498395.zip',
 ROOT/'tooling-validation/hosted-run-38214498395',ROOT/'tooling-validation/hosted-run-38214498395-extraction.json',raw_prefix,426)
raw_zip(ROOT/'tooling-validation/android-tools-run-38214498395.zip',
 ROOT/'tooling-validation/hosted-tools-run-38214498395',ROOT/'tooling-validation/hosted-tools-run-38214498395-extraction.json',raw_prefix+'/host-tools',1)
save(raw_prefix+'/RAW_EVIDENCE.md',b'''# Unchanged promoted-candidate Android evidence

Run 38214498395 checked out the combined reconstruction at
dbcad968c5c3e8f084205393a6c0d2d06a203c71. Its Android job reported a failed
strict intro comparison while the separate constructor allocation probe passed.
The raw 426-file capture/ART artifact and separate one-file tooling-test artifact
are preserved unchanged with their original ZIPs and exact extraction receipts.
The complete source acceptance job is a different job in this workflow.

All original member paths are under `extracted/`; tooling host evidence is under
`host-tools/`. `manifest.json` and `host-tools/manifest.json` bind exact ZIP byte
streams for `scripts/assemble_artifact.py`. Derived replay and visual measurements
are separate from these original bytes. No whole-application parity is claimed.
''')

for local,target,digest in [
 ('video-monitor-recovery/checkpoints/10-compiled-controls','work-in-progress/video-monitor/10-compiled-controls','c8ba7485fb0a506e38c17cefdce190cd9c6c9765cf059a1b485f5f3719e14357'),
 ('video-monitor-recovery/checkpoints/11-method-dex-assembly-command-failure','work-in-progress/video-monitor/11-method-dex-assembly-command-failure','10a95d413d2d866f3668bff1621bf39a9c8873829e8800b135fdec6e51215dd5'),
]:
 cp=package(local,target,digest)
 assert cp['raw_original_coverage_gate_passed'] is False and cp['android_executed'] is False
 tar_bundle(cp,target)

package('combined-cache-retirement/checkpoints/02-retirement-receipt',
 'docs/verification/storage-cleanup/combined-cache-retirement/02-retirement-receipt',
 '230fcdf1ce755c35a69881abdceebaf8c97da60a6f5c62d7d1e47330e8985296')

ops='docs/verification/repository-publication/2026-10-12-dbcad-evidence'
for p in [ROOT/'prepare_dbcad_evidence_transfer.py',ROOT/'dbcad_evidence_body.py',
 *[ROOT/'zero-trigger-transfer'/n for n in ['manifest.json','blobs.json','preparation.json','activation-guards.json','publication_guard.py','external-preservation.json','verify_remote.py','remote-verification.json','initial-workflow-observation.json']]]:
 name=('scripts/' if p.parent==ROOT else 'previous-zero-workflow-publication/')+p.name
 save(ops+'/'+name,p.read_bytes())
prefixes.append(ops)
