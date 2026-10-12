"""Preserve the closed 41-control numeric ART archive through three exact parts."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import contextlib, hashlib, importlib.util, io, json, os, stat, subprocess, sys, tarfile

BASE=Path('/dev/shm/macrodroid-transfer-space-20261012')
SOURCE=Path('/dev/shm/macrodroid-day-numeric-art/checkpoints/04-wrapper-host-controls')
OUTPUT=BASE/'numeric-art04-archive-layout'
PREFIX='work-in-progress/day-numeric-art/04-wrapper-host-controls'
LAYOUT=PREFIX+'/archive-layout'
CP_SHA='14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb'
ARCHIVE_SHA='56e15009933932b5f197d4f985f4cd7677116b74bf5b3484a36fcbb4088ee47f'
ARCHIVE_BYTES=16898593
PARENT='88f35e5f1ff52236e8cd51fe0188eabcb4d7bec4'
GIT=['git','--git-dir='+str(BASE/'verification.git')]

def sha(raw): return hashlib.sha256(raw).hexdigest()
def safe(name):
    p=PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==name
    return name
def identity(path):
    s=path.lstat()
    assert stat.S_ISREG(s.st_mode)
    raw=path.read_bytes()
    return dict(bytes=len(raw),sha256=sha(raw),mode=stat.S_IMODE(s.st_mode))
def write(name,raw):
    p=OUTPUT/safe(name);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
    p.chmod(0o644)
def js(name,value):write(name,(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())

cp_raw=(SOURCE/'checkpoint.json').read_bytes()
assert sha(cp_raw)==CP_SHA
cp=json.loads(cp_raw)
assert len(cp['files'])==len({safe(r['path']) for r in cp['files']})==26
before={}
for row in cp['files']:
    actual=identity(SOURCE/row['path'])
    assert actual=={k:row[k] for k in ('bytes','sha256','mode')}
    before[row['path']]=actual
assert before['evidence.tar.gz']==dict(bytes=ARCHIVE_BYTES,sha256=ARCHIVE_SHA,mode=0o644)
inventory_raw=(SOURCE/'evidence-inventory.json').read_bytes()
inventory=json.loads(inventory_raw)
expected={safe(r['path']):r for r in inventory}
assert len(inventory)==len(expected)==7629
seen=set();expanded=0
with tarfile.open(SOURCE/'evidence.tar.gz','r:gz') as archive:
    for member in archive:
        assert member.isfile() and member.name in expected and member.name not in seen
        raw=archive.extractfile(member).read()
        assert dict(path=member.name,bytes=len(raw),sha256=sha(raw),mode=member.mode&0o777)==expected[member.name]
        seen.add(member.name);expanded+=len(raw)
assert len(seen)==7629 and expanded==96481154

OUTPUT.mkdir(exist_ok=False)
parts=[];combined=hashlib.sha256();total=0
with (SOURCE/'evidence.tar.gz').open('rb') as stream:
    for index in range(1,4):
        raw=stream.read(8388608)
        assert raw and len(raw)<=8388608
        name='parts/evidence.'+str(index).zfill(4)+'.part'
        write(name,raw)
        parts.append(dict(path=LAYOUT+'/'+name,size_bytes=len(raw),sha256=sha(raw),
            git_blob_sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),mode='100644'))
        combined.update(raw);total+=len(raw)
    assert not stream.read(1)
assert total==ARCHIVE_BYTES and combined.hexdigest()==ARCHIVE_SHA
assert [r['size_bytes'] for r in parts]==[8388608,8388608,121377]
js('manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,
    filename='evidence.tar.gz',size_bytes=ARCHIVE_BYTES,sha256=ARCHIVE_SHA,mode='100644',parts=parts,
    source_checkpoint=dict(path=PREFIX+'/checkpoint.json',bytes=len(cp_raw),sha256=CP_SHA),
    logical_repository_path=PREFIX+'/evidence.tar.gz',
    evidence_inventory=dict(path=PREFIX+'/evidence-inventory.json',bytes=len(inventory_raw),
                            sha256=sha(inventory_raw),members=7629)))
js('layout-addendum.json',dict(schema=1,original_checkpoint_sha256=CP_SHA,original_checkpoint_preserved=True,
    logical_path=PREFIX+'/evidence.tar.gz',logical_file=dict(bytes=ARCHIVE_BYTES,sha256=ARCHIVE_SHA,mode='100644'),
    committed_manifest=LAYOUT+'/manifest.json',parts=parts,
    all_other_25_original_payloads_committed_unchanged=True,archive_content_or_compression_changed=False,
    integration_order=['Verify the original checkpoint and the exact three part identities.',
     'Reassemble the logical evidence.tar.gz before complete-capsule verification.',
     'Verify size/SHA256, set mode 0644, and verify all 26 payloads and 7629 archived member identities.'],
    no_application_or_workflow_activation=True))
assembler=subprocess.check_output(GIT+['show',PARENT+':scripts/assemble_artifact.py'])
write('reviewed-assemble-artifact.py',assembler)
virtual=BASE/'numeric-art04-assembly-validation';virtual.mkdir(exist_ok=False)
for row in parts:
    target=virtual/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
    os.link(OUTPUT/row['path'].removeprefix(LAYOUT+'/'),target)
spec=importlib.util.spec_from_file_location('numeric_art04_exact_assembler',OUTPUT/'reviewed-assemble-artifact.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.REPOSITORY=virtual
saved=sys.argv;stdout=io.StringIO();stderr=io.StringIO()
try:
    sys.argv=['reviewed-assemble-artifact.py',str(OUTPUT/'manifest.json'),'--verify-only']
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):module.main()
finally:sys.argv=saved
assert not stderr.getvalue()
write('assembler.stdout.log',stdout.getvalue().encode());write('assembler.stderr.log',stderr.getvalue().encode())
js('verification.json',dict(status='EXACT_NUMERIC_ART04_ARCHIVE_MULTIPART_VERIFIED',passed=True,
    source_checkpoint_sha256=CP_SHA,original_payloads_verified=26,archived_members_verified=7629,
    exact_inventory_sha256=sha(inventory_raw),expanded_bytes=expanded,part_count=3,total_bytes=total,
    archive_sha256=combined.hexdigest(),part_sizes=[r['size_bytes'] for r in parts],
    no_assembled_archive_copy_created=True,
    assembler_source=dict(commit=PARENT,path='scripts/assemble_artifact.py',sha256=sha(assembler)),
    actual_entry_point='main',argv=['reviewed-assemble-artifact.py','manifest.json','--verify-only'],
    repository_override='Owned directory containing only hardlinks to the three exact parts.',
    exit_code=0,original_checkpoint_unchanged=True,application_source_changed=False,android_executed=False,
    completed_utc=datetime.now(timezone.utc).isoformat()))
readme=(
 '# Exact numeric ART 41-control archive layout\n\n'
 'The historical checkpoint '+CP_SHA+' and its 25 non-archive payloads are preserved unchanged. '
 'Its 16,898,593-byte evidence.tar.gz is represented by three exact binary parts; it was neither recompressed nor edited.\n\n'
 'The complete SHA-256 is '+ARCHIVE_SHA+'. The manifest binds canonical part paths, byte counts, SHA-256 values and Git blob identities. '
 'The original evidence-inventory.json binds all 7,629 members and their 96,481,154 total expanded bytes, which were individually rechecked here.\n\n'
 'Before validating the complete original capsule, run the existing scripts/assemble_artifact.py with '
 +LAYOUT+'/manifest.json and --output '+PREFIX+'/evidence.tar.gz, then set the output mode to 0644. '
 'Recheck the complete digest, all 26 original file identities and every archived member. '
 'The published parts resolve the logical archive; an absent assembled archive alone is not a complete materialized capsule.\n\n'
 'The fetched assembler was invoked with --verify-only against the three exact parts and created no assembled duplicate. '
 'Its exact source/stdout/stderr are retained. This transport check adds no Android or application credit. '
 'The old 41-control result stays historical: the subsequently observed schema-2.0 acceptance and its separate literal-type correction are not rewritten into it.\n')
write('README.md',readme.encode());write('executed-freezer.py',Path(__file__).read_bytes())
for name,value in before.items():assert identity(SOURCE/name)==value
assert (SOURCE/'checkpoint.json').read_bytes()==cp_raw
files=[dict(path=str(p.relative_to(OUTPUT)),**identity(p)) for p in sorted(OUTPUT.rglob('*')) if p.is_file()]
js('checkpoint.json',dict(schema=1,status='EXACT_MULTIPART_TRANSPORT_ONLY',repo_target=LAYOUT,active_files=[],
    original_checkpoint_sha256=CP_SHA,logical_archive_sha256=ARCHIVE_SHA,files=files))
print(json.dumps(dict(output=str(OUTPUT),repo_target=LAYOUT,checkpoint=identity(OUTPUT/'checkpoint.json'),
    files=len(files),manifest=identity(OUTPUT/'manifest.json'),addendum=identity(OUTPUT/'layout-addendum.json'),parts=parts,
    original_source_unchanged=True)))

