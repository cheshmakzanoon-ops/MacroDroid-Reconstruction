from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'dbcad-source-transfer'
EXPORT.mkdir(exist_ok=True)
paths = set()
receipts = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()

def save(name, data, mode=0o644):
    name = safe(name)
    p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    p.chmod(mode)
    paths.add(name)

def jsave(name, value):
    save(name, (json.dumps(value, indent=2) + '\n').encode())

def copy_checkpoint(source, prefix, expected_sha, list_key='files'):
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected_sha
    cp = json.loads(raw)
    for row in cp[list_key]:
        p = source / safe(row['path'])
        data = p.read_bytes()
        assert not p.is_symlink()
        assert len(data) == row.get('bytes', row.get('size_bytes')) and sha(data) == row['sha256'], row['path']
        mode = '100755' if p.stat().st_mode & 0o111 else '100644'
        if 'mode' in row:
            assert row['mode'] == mode, row['path']
        save(prefix + '/' + row['path'], data, int(mode, 8) & 0o777)
    save(prefix + '/checkpoint.json', raw)
    return cp

prefixes=[]

def package(local, target, digest, key='files'):
 cp=copy_checkpoint(ROOT/local,target,digest,key)
 prefixes.append(target)
 receipts[target]=dict(files=len(cp[key]),checkpoint_sha256=digest)
 return cp

def tar_bundle(cp,target):
 source=Path(cp['evidence_bundle']['path']);data=source.read_bytes()
 assert len(data)==cp['evidence_bundle']['bytes'] and sha(data)==cp['evidence_bundle']['sha256']
 path=target+'/evidence-archive/complete-evidence.tar.gz';save(path,data)
 jsave(target+'/evidence-archive/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,id=target.replace('/','-'),
 filename='complete-evidence.tar.gz',media_type='application/gzip',purpose='Exact closed inactive study evidence with the original checkpoint scope preserved.',
 size_bytes=len(data),sha256=sha(data),parts=[dict(path=path,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))]))
 with tarfile.open(source,'r:gz') as archive:
  members={safe(item.name):item for item in archive.getmembers() if item.isfile()}
  assert len(members)==len(cp['evidence_files'])
  assert all(item.isfile() or item.isdir() for item in archive.getmembers())
  for row in cp['evidence_files']:
   data=archive.extractfile(members[safe(row['path'])]).read()
   assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
   save(target+'/evidence/'+row['path'],data,0o755 if members[row['path']].mode & 0o111 else 0o644)
 receipts[target]['complete_archive_members']=len(cp['evidence_files'])


prefix='docs/verification/source-ci-dbcad968'
virtual=json.loads((EXPORT/'virtual-blobs.json').read_text())
virtual_by_path={row['path']:row for row in virtual}
assert len(virtual_by_path)==23
cp=package('ci-run-analysis/checkpoints/04-dbcad-source-independent-review',prefix+'/independent-review',
 'a2348b8c9692051a71e94283c0420a10993ce21ad59b84174b4b623c5c7a9df7')
assert cp['active_files']==[] and cp['status']=='FROZEN_INDEPENDENT_SOURCE_CI_ALL16_REVIEW'
save(prefix+'/manifest.json',(REPO/prefix/'manifest.json').read_bytes())
paths.update(virtual_by_path)
save(prefix+'/README.md',"# Hosted reproduction of the active combined candidate\n\nSource job **114695960566** in [run 38214498395](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498395) completed successfully for commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. It passed all 16 configured acceptance gates and reproduced the exact committed baseline and hybrid APKs. The workflow's separate Android job failed its intro comparison; the overall workflow therefore remains failed.\n\n## What was independently checked\n\nThe [frozen independent review](independent-review/README.md) streamed all **1,136 original artifact members**, totaling **450,752,098 expanded bytes**, without extracting duplicate APKs or the large resource tables. It verified all 16 actual gate logs, all 22 fresh report hashes, all 78 retained mutant source/class identities and the exact complete positive restoration. The measured host totals are **193,489 original/JVM/rebuilt cases across 1,242 recovered methods**, with zero semantic mismatches or unsupported executions, and **273 Python tests**.\n\nThe complete 81,291-entry input manifest is byte-identical to the committed manifest, and its canonical digest recomputes to `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. The acceptance result reports that this input pin remained unchanged. The review binds those actual gate results and manifest bytes; it does not claim to have extracted and independently executed all source inputs again.\n\n| Output | Bytes | SHA-256 |\n| --- | ---: | --- |\n| Baseline APK | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |\n| Combined hybrid APK | 94,683,119 | `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` |\n\nThe current fresh run is `reports/acceptance-20261012T065140692696Z/`. Historical report members elsewhere in the ZIP retain their original identities and scope. The [complete member inventory](independent-review/all-1136-member-identities.json) and [independent review result](independent-review/independent-source-review.json) distinguish the actual fresh evidence from those historical files.\n\n## Exact original archive\n\nThe original GitHub artifact is **188,134,390 bytes**, with SHA-256:\n\n`da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88`\n\n[manifest.json](manifest.json) binds all 23 parts under `archive/`. The parts preserve the original ZIP byte for byte; neither the container nor its members were recompressed. Both APKs, every nested mutant source/class/report and every retained historical report are present in the archive. Compact actual reports, all gate logs, the reviewer source and the frozen provenance are also directly readable under [independent-review/](independent-review/).\n\nFrom the repository root, verify every committed part and the complete ZIP identity:\n\n```sh\npython3 scripts/assemble_artifact.py docs/verification/source-ci-dbcad968/manifest.json --verify-only\n```\n\nTo materialize an ordinary ZIP when needed:\n\n```sh\npython3 scripts/assemble_artifact.py docs/verification/source-ci-dbcad968/manifest.json --output /tmp/reconstruction-run-38214498395.zip\n```\n\nThe [GitHub metadata](github-metadata.json) binds the source job and artifact. The [publication scripts](publication/) preserve the bounded range-transfer procedure and the exact review of repository documentation changes. The download is only eligible for retirement after fetched Git blobs reconstruct its complete original identity and the independent review has closed every reader; the committed parts remain the durable source.\n\n## Runtime scope\n\nThis source job performed host, artifact and source-edit checks. It did not run the app on Android. The separately preserved [Android capture](../android-ci-dbcad968/) has an exact cold launch, a 35-pixel TRIGGERS difference and a successful bounded constructor ART probe. Its raw post-intro pair is exact, while that gate retains the failed intro prerequisite. The [scoped post-home session](../editor-journey/run-38214498414-attempt-1/analysis/) has ten exact full-frame/XML/component pairs and preserves the observed startup crashes and restarts. Neither result establishes whole-application 1:1 parity.\n".encode())
save(prefix+'/github-metadata.json',(ROOT/'tooling-validation/source-run-38214498395-api.json').read_bytes())
save(prefix+'/download-receipt.json',(ROOT/'tooling-validation/reconstruction-run-38214498395.download.json').read_bytes())
for p in [ROOT/'prepare_dbcad_source_metadata.py',ROOT/'prepare_dbcad_source_ranges.py',ROOT/'finish_dbcad_source_transfer.py',
 ROOT/'tooling-validation/download_source_38214498395.py',
 *[EXPORT/n for n in ['virtual-blobs.json','virtual-range-preparation.json','upload_virtual_ranges.js','doc-updates.json']],
 *[ROOT/'dbcad-followups-transfer'/n for n in ['manifest.json','blobs.json','preparation.json','publication_guard.py','publication-guard.json','external-preservation.json','verify_remote.py','remote-verification.json']]]:
 sub='previous-followup-publication/' if p.parent.name=='dbcad-followups-transfer' else ''
 save(prefix+'/publication/'+sub+p.name,p.read_bytes())
doc_baselines={}
for entry in json.loads((EXPORT/'doc-updates.json').read_text()):
 p=REPO/entry['path'];before=p.read_bytes()
 assert sha(before)==entry['before_sha256'] and before.decode()==entry['before_text'],entry['path']
 doc_baselines[entry['path']]=sha(before)
 p.write_bytes(entry['after_text'].encode());paths.add(entry['path'])
prefixes.append(prefix)
baselines = dict(doc_baselines)
ignored_result = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
    input=b'\0'.join(name.encode() for name in sorted(paths)) + b'\0', capture_output=True)
assert ignored_result.returncode in (0, 1)
ignored = [name.decode() for name in ignored_result.stdout.split(b'\0') if name]
if ignored:
    path = REPO / '.gitignore'
    old = path.read_bytes(); baselines['.gitignore'] = sha(old)
    path.write_bytes(old + ('\n# Exact closed runtime and guard-review evidence\n' + ''.join('!' + name + '\n' for name in ignored)).encode())
    paths.add('.gitignore')
path = REPO / '.gitattributes'
old = path.read_bytes(); baselines['.gitattributes'] = sha(old)
rules = '\n# Preserve exact raw device, protocol and synthetic evidence bytes\n'
rules += ''.join(prefix + '/** -text\n' for prefix in prefixes)
path.write_bytes(old + rules.encode()); paths.add('.gitattributes')

known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
manifest = []; blobs = []; texts = []
for name in sorted(paths):
    if name in virtual_by_path:
        v=virtual_by_path[name]
        row={key:v[key] for key in ['path','size_bytes','sha256','git_blob_sha1','mode']}
        manifest.append(row); blobs.append(v); continue
    p = REPO / name; data = p.read_bytes()
    row = dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        content = data.decode('utf-8'); binary = '\0' in content
    except UnicodeDecodeError:
        binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='utf-8' if len(data) > 12500000 and data.isascii() else 'base64'))
    else:
        texts.append(dict(path=name, mode=row['mode'], type='blob', content=content))
chunks = []; chunk = []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk); chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for index, chunk in enumerate(chunks):
    (EXPORT / f'text-{index:02d}.json').write_text(json.dumps(chunk, ensure_ascii=False))
for name, data in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (EXPORT / name).write_text(json.dumps(data, indent=2) + '\n')
result = dict(files=len(manifest), bytes=sum(row['size_bytes'] for row in manifest), text_chunks=len(chunks),
    text_entries=len(texts), new_unique_blobs=len({row['git_blob_sha1'] for row in blobs if not row['known']}),
    baselines=baselines, receipts=receipts, active_workflow_modified=False, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

