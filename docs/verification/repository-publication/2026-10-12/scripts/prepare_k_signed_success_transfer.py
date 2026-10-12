from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import subprocess
import tarfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
SOURCE = ROOT / 'plugin-upload-recovery/checkpoints/04-signed-proof'
EXPORT = ROOT / 'k-signed-success-transfer'
PREFIX = 'work-in-progress/plugin-upload/04-signed-proof'
EXPORT.mkdir(exist_ok=True)
paths = set()
def sha(b): return hashlib.sha256(b).hexdigest()
def oid(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def safe(name):
    p = PurePosixPath(name); assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()
def save(name, data, mode=0o644):
    name = safe(name); p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); p.chmod(mode); paths.add(name)
def jsave(name, value): save(name, (json.dumps(value, indent=2) + '\n').encode())

raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(raw) == 'd9c1e3f02e43546b07336ded7099e8bfe0c19a97b56ab5f0b4c6b79b0f8eac48'
cp = json.loads(raw)
assert len(cp['files']) == 35 and len(cp['evidence_files']) == 445
source_rows = cp['files'] + cp['merge_patches'] + cp['study_tools'] + [cp['isolated_build_recipe']]
source_rows += [r['patch'] for r in cp['documentary_updates_after_proof']]
source_rows += [r | {'path': 'evidence-summary/' + Path(r['path']).name} for r in cp['evidence_files'] if r['path'].startswith('summary/')]
source_map = {r['path']: r for r in source_rows}
assert len(source_map) == 49
actual = {p.relative_to(SOURCE).as_posix(): p for p in SOURCE.rglob('*') if p.is_file() and 'evidence' not in p.relative_to(SOURCE).parts}
assert set(actual) == set(source_map) | {'checkpoint.json'} and len(actual) == 50
for name, row in source_map.items():
    p = actual[name]; data = p.read_bytes(); assert not p.is_symlink()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
    save(PREFIX + '/' + name, data, 0o755 if p.stat().st_mode & 0o111 else 0o644)
save(PREFIX + '/checkpoint.json', raw)
archive = Path(cp['evidence_bundle']['path']).read_bytes()
assert len(archive) == cp['evidence_bundle']['bytes'] == 17491687
assert sha(archive) == cp['evidence_bundle']['sha256'] == '1644a034c9890edb8aeb6b84e928d1032d0153887d59826be1f691445e200295'
expected = {r['path']: r for r in cp['evidence_files']}
seen = set(); compact = []; expanded_bytes = 0
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as t:
    for member in t.getmembers():
        if member.isdir(): continue
        assert member.isfile()
        name = safe(member.name); assert name in expected and name not in seen; seen.add(name)
        data = t.extractfile(member).read(); row = expected[name]
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        expanded_bytes += len(data)
        if len(data) <= 250000 or name.endswith('.java'):
            save(PREFIX + '/evidence/' + name, data, 0o755 if member.mode & 0o111 else 0o644)
            compact.append(name)
assert seen == set(expected) and len(seen) == 445 and len(compact) == 363
assert expanded_bytes == 140251467
parts = []
for i, offset in enumerate(range(0, len(archive), 8388608), 1):
    data = archive[offset:offset+8388608]; name = PREFIX + f'/evidence-archive/part-{i:04d}.part'
    save(name, data); parts.append(dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
jsave(PREFIX + '/evidence-archive/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1, id='plugin-upload-04-signed-proof-evidence',
    filename='Plugin-upload-04-signed-proof-evidence.tar.gz', media_type='application/gzip',
    purpose='Complete exact inactive K source/build/control evidence, including all generated mutant artifacts',
    size_bytes=len(archive), sha256=sha(archive), parts=parts))
assert hashlib.sha256(b''.join((REPO / r['path']).read_bytes() for r in parts)).hexdigest() == sha(archive)
assert cp['all_suite_cases'] == 191147 and cp['registered_bodies'] == 1241 and cp['paths'] == 3
assert cp['failed_cases'] == cp['unsupported_executions'] == 0 and cp['android_executed'] is False
controls = cp['negative_controls']['complete_result']
assert controls['pass'] is True and len(controls['controls']) == 54
assert controls['positiveRestorationPassed'] is True and controls['restorationCases'] == 20832
assert controls['sourceFixtureAndApkUnchanged'] is True
assert cp['signed_proof']['passed'] is True and cp['resource_proof']['returncode'] == 0 and cp['resource_proof']['timed_out'] is False
apk_path = 'work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json'
apk = json.loads((REPO / apk_path).read_text())
assert apk['size_bytes'] == cp['apk']['bytes'] == 94683177
assert apk['sha256'] == cp['apk']['sha256'] == 'e4643b554429743703bed5c1aa5e3541dbfc0705d9fd87c353bd968f348baf80'
jsave(PREFIX + '/publication-verification.json', dict(
    frozen_checkpoint_sha256=sha(raw), candidate_delta_files_verified=35, all_actual_source_capsule_files_verified=50,
    exact_archive_members_verified=445, exact_archive_expanded_bytes=expanded_bytes,
    complete_project_reports=279, actual_mutant_source_class_result_files=162,
    compact_review_files=compact, archive_manifest='evidence-archive/manifest.json',
    exact_archive_sha256=sha(archive), exact_archive_bytes=len(archive),
    unchanged_apk_manifest=apk_path, unchanged_apk_durable_commit='5024b1b46056de6a6e76a61883b469521a89ea44',
    duplicate_archive_or_apk_assembly_created=False, active_source_or_apk_changed=False, android_executed=False))
save(PREFIX + '/PUBLICATION_LAYOUT.md', b'''# Complete signed K proof, preserved as an inactive checkpoint

All 50 actual source-capsule files are copied unchanged: the 35 candidate delta files, three narrow merge patches, five study tools, the evidence-only build recipe, three documentary patches, two evidence summaries and the frozen checkpoint itself.

The exact 17,491,687-byte evidence archive is preserved in three bounded parts under `evidence-archive/`. Every one of its 445 member sizes and SHA-256 hashes was independently verified: 279 complete project reports, 162 actual mutant source/class/result artifacts, two prior checkpoint manifests and two final summaries. All 363 members of at most 250,000 bytes, plus every authored mutant Java source, are also copied under `evidence/`; larger reports remain complete in the archive. `publication-verification.json` records the exact mapping.

The bounded signed original/JVM/rebuilt comparison passes 191,147 cases across 1,241 registered methods. Code/resource verification, all 54 fault controls and the 20,832-case clean restoration passed. The frozen reports retain their exact exception-comparison scope and source, fixture and APK identities. Actual Android execution and any future combined candidate require separate proof.

```bash
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/04-signed-proof/evidence-archive/manifest.json --verify-only
```

The exact e464 APK is already durable at commit `5024b1b46056de6a6e76a61883b469521a89ea44`, represented by `work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json`. This publication does not change active app source or APKs. The isolated build recipe remains evidence only; it must not overwrite the parent's current cleanup, constructor or runtime policies.
''')
baselines = {}
ignored_result = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
    input=b'\0'.join(p.encode() for p in sorted(paths)) + b'\0', capture_output=True)
assert ignored_result.returncode in (0,1)
ignored = [p.decode() for p in ignored_result.stdout.split(b'\0') if p]
if ignored:
    p = REPO / '.gitignore'; before=p.read_bytes(); baselines['.gitignore']=sha(before)
    addition='\n# Exact inactive K signed proof files\n'+''.join('!'+n+'\n' for n in ignored)
    p.write_bytes(before+addition.encode());paths.add('.gitignore')
p=REPO/'.gitattributes'; before=p.read_bytes(); baselines['.gitattributes']=sha(before)
p.write_bytes(before+('\n# Complete inactive K proof archive parts\n'+PREFIX+'/evidence-archive/*.part -text -diff -merge\n').encode());paths.add('.gitattributes')
known = {line.split(b' ',1)[0].decode() for line in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
rows=[];blobs=[];texts=[]
for name in sorted(paths):
    p=REPO/name;data=p.read_bytes();row=dict(path=name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data),mode='100755' if p.stat().st_mode&0o111 else '100644');rows.append(row)
    try: content=data.decode('utf-8');binary='\0' in content
    except UnicodeDecodeError: binary=True
    if row['git_blob_sha1'] in known or binary or len(data)>250000: blobs.append(row|dict(known=row['git_blob_sha1'] in known,encoding='base64'))
    else: texts.append(dict(path=name,mode=row['mode'],type='blob',content=content))
chunks=[];chunk=[]
for entry in texts:
    if chunk and len(json.dumps(chunk+[entry],ensure_ascii=False).encode())>650000:chunks.append(chunk);chunk=[]
    chunk.append(entry)
if chunk:chunks.append(chunk)
for i,entries in enumerate(chunks):(EXPORT/f'text-{i:02d}.json').write_text(json.dumps(entries,ensure_ascii=False))
for name,data in [('manifest.json',rows),('blobs.json',blobs)]:(EXPORT/name).write_text(json.dumps(data,indent=2)+'\n')
result=dict(files=len(rows),bytes=sum(r['size_bytes'] for r in rows),text_chunks=len(chunks),text_entries=len(texts),
    new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),baselines=baselines,
    complete_archive_members=445,complete_source_capsule_files=50,compact_review_files=len(compact),active_source_or_apk_changed=False)
(EXPORT/'preparation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
