from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import subprocess
import tarfile

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
SOURCE=ROOT/'widget-art-probe/checkpoints/02-workflow-review'
EXPORT=ROOT/'widget-art02-transfer'
PREFIX='work-in-progress/widget-art/02-workflow-review'
HEAD='075cdcb5b5e7309057acdac63a097ac48dbbd545'
EXPORT.mkdir(exist_ok=True)
paths=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(name):
    p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()
def save(name,data,mode=0o644):
    name=safe(name);p=REPO/name;assert not p.is_symlink() and (not p.exists() or p.read_bytes()==data),name
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);paths.add(name)
def jsave(name,value):save(name,(json.dumps(value,indent=2)+'\n').encode())

raw=(SOURCE/'checkpoint.json').read_bytes()
assert sha(raw)=='921802a59d131ea9330d4fdbb6ae09c67f270160221a70fe875d39cb3ade1596'
cp=json.loads(raw);assert len(cp['files'])==5 and len(cp['evidence_files'])==3202
assert cp['validation']['passed'] is True and cp['android_executed'] is False
assert json.loads((SOURCE/'baseline-inputs.json').read_text())==cp['baseline_inputs']
for row in cp['baseline_inputs']['files']:
    name=safe(row['path']);data=(REPO/name).read_bytes()
    assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
    assert subprocess.check_output(['git','show',HEAD+':'+name],cwd=REPO)==data,name
workflow_name=cp['proposed_repository_path'];assert workflow_name=='.github/workflows/widget-method-probe.yml'
assert not (REPO/workflow_name).exists()
assert subprocess.run(['git','cat-file','-e',HEAD+':'+workflow_name],cwd=REPO,capture_output=True).returncode!=0
for row in cp['files']:
    p=SOURCE/safe(row['path']);data=p.read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
    save(PREFIX+'/'+row['path'],data,0o755 if p.stat().st_mode&0o111 else 0o644)
save(PREFIX+'/checkpoint.json',raw)
archive=Path(cp['evidence_bundle']['path']).read_bytes()
assert len(archive)==cp['evidence_bundle']['bytes']==1248332
assert sha(archive)==cp['evidence_bundle']['sha256']=='85020f84f11a905a9f68493d2155fef3a4a1bc2d5c8e3a8df60033bef02a3229'
expected={r['path']:r for r in cp['evidence_files']};seen=set();compact=[]
with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as t:
    for member in t.getmembers():
        if member.isdir():continue
        assert member.isfile()
        name=safe(member.name);assert name in expected and name not in seen;seen.add(name)
        data=t.extractfile(member).read();row=expected[name]
        assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
        if not name.startswith('reports/validation-01/packaged-wrapper-control-evidence/'):
            save(PREFIX+'/evidence/'+name,data,0o755 if member.mode&0o111 else 0o644);compact.append(name)
assert seen==set(expected) and len(compact)==208
part_name=PREFIX+'/evidence-archive/part-0001.part';save(part_name,archive)
jsave(PREFIX+'/evidence-archive/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,
    id='widget-art-02-workflow-review-evidence',filename='Widget-ART-02-workflow-review-evidence.tar.gz',media_type='application/gzip',
    purpose='Exact offline workflow preflight, cleanup, downloader and simulated wrapper evidence',size_bytes=len(archive),sha256=sha(archive),
    parts=[dict(path=part_name,size_bytes=len(archive),sha256=sha(archive),git_blob_sha1=oid(archive))]))
workflow=(SOURCE/workflow_name).read_bytes();assert sha(workflow)==cp['workflow_sha256']=='43cf0363c9382083bdeed97f33fd71cfe2905eada2f34dd9e5698900ce226149'
save(workflow_name,workflow)
jsave(PREFIX+'/publication-verification.json',dict(frozen_checkpoint_sha256=sha(raw),observed_parent=HEAD,
    source_files_verified=5,baseline_dependency_files_verified=22,new_workflow_absence_guard_verified=True,
    complete_archive_members_verified=3202,compact_review_files=compact,archive_manifest='evidence-archive/manifest.json',
    exact_archive_sha256=sha(archive),exact_archive_bytes=len(archive),active_workflow=workflow_name,
    original_apk_sha256=cp['original_apk_sha256'],candidate_apk_sha256=cp['candidate_apk_sha256'],
    prior_workflows_and_app_inputs_changed=False,android_execution_at_publication='PENDING'))
save(PREFIX+'/PUBLICATION_LAYOUT.md',b'''# Independent Widget ART workflow publication

The five declared source, workflow, documentation and validation files and the original checkpoint are preserved unchanged. The new active workflow is `.github/workflows/widget-method-probe.yml`; all 22 frozen dependency/package hashes and the new-path absence guard were checked against the observed repository head before publication. Existing workflows and active app/APK inputs remain unchanged.

The exact evidence archive preserves all 3,202 members with individually verified sizes and SHA-256 hashes. Its 208 compact files are also copied under `evidence/`; the full simulated wrapper cases remain in the archive. The original host results include nine preflight fault rejections, four cleanup controls, six downloader tests and 27 packaged wrapper tests. They are offline measurements, with actual Android execution pending at this checkpoint.

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-art/02-workflow-review/evidence-archive/manifest.json --verify-only
```

The own-path workflow trigger requests a fresh independent Android run using the original APK, the unchanged b79 Widget APK and the already published ART01 probe package. Future measured results must be retained separately; this publication does not establish whole-app parity.
''')
baselines={}
ignored_result=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(p.encode() for p in sorted(paths))+b'\0',capture_output=True)
assert ignored_result.returncode in (0,1)
ignored=[p.decode() for p in ignored_result.stdout.split(b'\0') if p]
if ignored:
    p=REPO/'.gitignore';before=p.read_bytes();baselines['.gitignore']=sha(before)
    p.write_bytes(before+('\n# Exact Widget workflow review evidence\n'+''.join('!'+n+'\n' for n in ignored)).encode());paths.add('.gitignore')
p=REPO/'.gitattributes';before=p.read_bytes();baselines['.gitattributes']=sha(before)
p.write_bytes(before+('\n# Exact Widget workflow review archive\n'+PREFIX+'/evidence-archive/*.part -text -diff -merge\n').encode());paths.add('.gitattributes')
known={line.split(b' ',1)[0].decode() for line in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
rows=[];blobs=[];texts=[]
for name in sorted(paths):
    p=REPO/name;data=p.read_bytes();row=dict(path=name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data),mode='100755' if p.stat().st_mode&0o111 else '100644');rows.append(row)
    try:content=data.decode('utf-8');binary='\0' in content
    except UnicodeDecodeError:binary=True
    if row['git_blob_sha1'] in known or binary or len(data)>250000:blobs.append(row|dict(known=row['git_blob_sha1'] in known,encoding='base64'))
    else:texts.append(dict(path=name,mode=row['mode'],type='blob',content=content))
chunks=[];chunk=[]
for entry in texts:
    if chunk and len(json.dumps(chunk+[entry],ensure_ascii=False).encode())>650000:chunks.append(chunk);chunk=[]
    chunk.append(entry)
if chunk:chunks.append(chunk)
for i,entries in enumerate(chunks):(EXPORT/f'text-{i:02d}.json').write_text(json.dumps(entries,ensure_ascii=False))
for name,data in [('manifest.json',rows),('blobs.json',blobs)]:(EXPORT/name).write_text(json.dumps(data,indent=2)+'\n')
result=dict(files=len(rows),bytes=sum(r['size_bytes'] for r in rows),text_chunks=len(chunks),text_entries=len(texts),
    new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),baselines=baselines,
    complete_archive_members=3202,compact_review_files=len(compact),active_workflows_added=1,active_app_or_apk_changed=False)
(EXPORT/'preparation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
