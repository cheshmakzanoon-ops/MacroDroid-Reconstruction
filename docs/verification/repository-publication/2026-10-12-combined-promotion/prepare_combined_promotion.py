from pathlib import Path, PurePosixPath
import difflib
import hashlib
import json
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'combined-promotion-transfer'
EXPORT.mkdir(exist_ok=True)
PROOF_COMMIT = 'c9373851d4408fb4db63c21873ac2d0bb6867270'
OPS = 'docs/verification/repository-publication/2026-10-12-combined-promotion'
desired = {}
guards = {}
origins = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()

def identity(data):
    return dict(bytes=len(data), sha256=sha(data))

def check(data, row):
    assert len(data) == row.get('bytes', row.get('size', row.get('size_bytes'))) and sha(data) == row['sha256'], row

def add(name, data, before=None, mode=0o644, origin='authored publication metadata'):
    name = safe(name)
    assert name not in desired, name
    p = REPO / name
    assert not p.is_symlink(), name
    if before is None:
        assert not p.exists(), name
    else:
        check(p.read_bytes(), before)
    desired[name] = (data, mode)
    guards[name] = before
    origins[name] = origin

def jadd(name, value, before=None):
    add(name, (json.dumps(value, indent=2) + '\n').encode(), before)

def load_bound(folder, expected):
    raw = (folder / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected
    cp = json.loads(raw)
    for row in cp['files']:
        p = folder / safe(row['path'])
        assert not p.is_symlink()
        check(p.read_bytes(), row)
    return cp, raw

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip() == PROOF_COMMIT
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO).strip()
proof = REPO / 'work-in-progress/combined-recovery/05-full-acceptance'
raw = (proof / 'checkpoint.json').read_bytes()
assert sha(raw) == 'e4cd0b6af4cf95d7131138b3ad3dab8a070042cea077a80cf83c322168457063'
cp = json.loads(raw)
assert cp['passed'] and cp['registered_methods'] == 1242 and cp['cases'] == 193489 and cp['python_tests'] == 273
old_raw = (REPO / 'project/reports/release-input-snapshot.json').read_bytes()
assert sha(old_raw) == '713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883'
old = json.loads(old_raw)
new_raw = (proof / 'project/reports/release-input-snapshot.json').read_bytes()
assert sha(new_raw) == 'ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe'
new = json.loads(new_raw)
assert old['files'] == 81245 and new['files'] == len(new['entries']) == 81291
assert new['snapshot_sha256'] == 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
delta = {name: row for name, row in new['entries'].items() if old['entries'].get(name) != row}
assert len(delta) == 63 and not set(old['entries']) - set(new['entries'])
bound = {r['path']: r for r in cp['files']}
for name, row in delta.items():
    n = 'project/' + name
    p = proof / n; data = p.read_bytes()
    check(data, row); check(data, bound[n])
    before = old['entries'].get(name)
    if before is not None:
        before = dict(bytes=before['size'], sha256=before['sha256'])
    add(n, data, before, 0o755 if p.stat().st_mode & 0o111 else 0o644, 'Combined05 exact accepted input delta')
add('project/reports/release-input-snapshot.json', new_raw, identity(old_raw), origin='Combined05 complete accepted 81,291-input inventory')

doc_folder = REPO / 'work-in-progress/combined-recovery/06-promotion-documentation'
doc_cp, doc_raw = load_bound(doc_folder, 'f0403b172d2268ae9ff99072d829871c50518c08e3c7781508f76a96f6d773c3')
prep = REPO / 'work-in-progress/combined-widget-plugin/04-fresh-source-preparation'
initial = {r['path']: r for r in json.loads((prep / 'initial-documentation/changes.json').read_text())['changes']}
table = json.loads((prep / 'documentation-table-fix.json').read_text())
doc_chain = []
for row in json.loads((doc_folder / 'changes.json').read_text())['changes']:
    name = row['path']; data = (doc_folder / name).read_bytes(); check(data, row['after'])
    before = row['before']
    if name.startswith('project/'):
        short = name[8:]; chain = initial[short]
        check((prep / 'initial-documentation' / short).read_bytes(), chain['after'])
        if short == 'UI_RECOVERY.md':
            assert table['before'] == chain['after'] and table['after'] == row['before']
        else:
            assert chain['after'] == row['before']
        check((prep / name).read_bytes(), row['before'])
        before = chain['before']
    add(name, data, before, origin='Exact closed promotion documentation with reviewed preparatory before-state chain')
    doc_chain.append(dict(path=name, current_before=before, prepared_before=row['before'], after=row['after']))

workflow = '.github/workflows/reconstruction.yml'
old_workflow = (REPO / workflow).read_bytes()
assert sha(old_workflow) == '71a70927a0619bfb99692adbd7db2ddb9c1236f51499c8e3ba66f0cbb20e2357'
new_workflow = (prep / 'preparation/repository-overlay' / workflow).read_bytes()
assert sha(new_workflow) == 'e60b6f3d325818c9517327d16a9735fff662f6eb16dd580e4f8d8bf6f6296602'
assert old_workflow.split(b'  android-cold-launch:', 1)[1] == new_workflow.split(b'  android-cold-launch:', 1)[1]
assert old_workflow.count(b'timeout-minutes: 90') == 1 and new_workflow.count(b'timeout-minutes: 120') == 1
add(workflow, new_workflow, identity(old_workflow), origin='Reviewed source job budget and complete nested report upload; exact Android job preserved')
workflow_diff = ''.join(difflib.unified_diff(old_workflow.decode().splitlines(True), new_workflow.decode().splitlines(True), fromfile='before/reconstruction.yml', tofile='after/reconstruction.yml'))
add(OPS + '/reconstruction-workflow.patch', workflow_diff.encode())

union = REPO / 'work-in-progress/editor-session-chronology/04-trigger05-session03-union'
ucp, uraw = load_bound(union, '9b457171561ff0de24a9219a8d5f215879bb6cc37c77637b695ae83eb0710afe')
assert ucp['full_suite_tests'] == 148 and len(ucp['inactive_union_proposals']) == 20
for row in ucp['inactive_union_proposals']:
    p = union / 'replay-source' / safe(row['path']); data = p.read_bytes(); check(data, row['after'])
    add(row['path'], data, row['before'], 0o755 if p.stat().st_mode & 0o111 else 0o644, 'Parent-approved 148-test Trigger05/session03 source union')

review_folder = ROOT / 'combined-acceptance-review/checkpoints/01-independent-full-acceptance-review'
review_cp, review_raw = load_bound(review_folder, '7eaa75bfbab27f87b2568c478b1434ed10f4b1e247b883356f46188068addac5')
assert review_cp['passed'] is True and review_cp['reviewed_capsule_sha256'] == sha(raw)
review_prefix = 'docs/verification/combined-recovery/05-full-acceptance-independent-review'
for row in review_cp['files']:
    p = review_folder / row['path']; add(review_prefix + '/' + row['path'], p.read_bytes(), mode=0o755 if p.stat().st_mode & 0o111 else 0o644, origin='Exact independent 12-file accepted proof review')
add(review_prefix + '/checkpoint.json', review_raw)

manifest_path = 'artifacts/current/manifest.json'
old_apk_raw = (REPO / manifest_path).read_bytes()
assert sha(old_apk_raw) == '350f15eca6daf43b129fc66f4fa9e3afc6df9d607cab7ba00919943b3a139730'
old_apk = json.loads(old_apk_raw)
new_apk = json.loads((proof / 'apk/manifest.json').read_text())
assert old_apk['sha256'] == '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'
assert new_apk['sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
assert len(old_apk['parts']) == len(new_apk['parts']) == 12
parts = []
for prior, row in zip(old_apk['parts'], new_apk['parts']):
    data = (REPO / row['path']).read_bytes(); check(data, row); assert oid(data) == row['git_blob_sha1']
    add(prior['path'], data, dict(bytes=prior['size_bytes'], sha256=prior['sha256']), origin='Exact Combined05 accepted APK part; existing Git blob reused')
    parts.append(row | dict(path=prior['path']))
candidate = dict(format=old_apk['format'], format_version=1, id=old_apk['id'], filename=old_apk['filename'],
    media_type=old_apk['media_type'], purpose='Current development candidate with 1,242 recovered bodies and complete configured host acceptance; Android and whole-application parity remain separately measured.',
    source_build_filename=old_apk['source_build_filename'], recovered_method_bodies=1242, recovered_classes=605,
    full_functional_parity_established=False,
    source_checkpoint_manifest=dict(path='work-in-progress/combined-recovery/05-full-acceptance/checkpoint.json', sha256=sha(raw), commit=PROOF_COMMIT),
    source_input_snapshot=dict(path='project/reports/release-input-snapshot.json', files=81291, canonical_sha256=new['snapshot_sha256'], manifest_file_sha256=sha(new_raw)),
    origin=dict(kind='complete-sixteen-gate-combined-source-acceptance', proof_commit=PROOF_COMMIT,
        immutable_apk_manifest='work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json', immutable_apk_manifest_sha256=sha((proof/'apk/manifest.json').read_bytes()),
        independent_review_manifest=review_prefix+'/checkpoint.json', independent_review_manifest_sha256=sha(review_raw)),
    validation_at_publication=dict(configured_acceptance_gates_passed=16, original_jvm_rebuilt_cases=193489, registered_methods=1242,
        python_tests_passed=273, ui_cases=23174, independent_ui_checks=15326, actual_ui_fault_controls_passed=78,
        exact_positive_restoration_passed=True, full_configured_acceptance_executed_for_this_pin=True,
        separate_capture_guard_union_host_tests_passed=148, android_executed_for_this_candidate=False,
        post_intro_capture='pending fresh hosted candidate result', constructor_art_probe='pending fresh hosted candidate result'),
    previous_candidate=dict(commit=PROOF_COMMIT, manifest_path=manifest_path, sha256=old_apk['sha256']),
    size_bytes=new_apk['size_bytes'], sha256=new_apk['sha256'], parts=parts)
jadd(manifest_path, candidate, identity(old_apk_raw))

status_path = 'docs/TRANSFER_STATUS.md'
old_status = (REPO / status_path).read_bytes()
assert sha(old_status) == 'f9d6f799dcffaa02be5337808cb07e3d7e42f4d45afc9fded55d4a12193f81ea'
status = old_status.decode().replace('`artifacts/current/`; it is 94,683,497 bytes with SHA-256\n`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.',
    '`artifacts/current/`; it is 94,683,119 bytes with SHA-256\n`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`.')
assert status != old_status.decode()
status = status.replace('## Active plugin and runtime integration\n\nThe active overlay contains', '## Previous 1,240-body plugin and runtime integration\n\nThat overlay contained')
status = status.replace('Those new hosted outcomes remain pending at this freeze. No Widget recovery or plugin-upload body is activated by this integration, and no whole-application 1:1 claim is made.',
    'Those hosted outcomes were pending at that historical freeze; subsequent exact reports are retained separately. No Widget recovery or plugin-upload body was activated by that integration.')
status += '''
## Current combined source, artifact, and capture guards

The active overlay now contains 1,242 recovered bodies across 605 classes. Its
81,291 build/test inputs have canonical SHA-256
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`;
the complete manifest file SHA-256 is
`ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe`.
The exact delta is 46 additions and 17 changes, with no removed input. It combines
the plugin-upload and Widget implementations with their fixtures and controls.

All 16 configured clean host acceptance gates passed: 193,489 original/JVM/rebuilt
cases across all 1,242 methods, 273 Python tests, 23,174 UI cases with 15,326
independent checks, all 78 actual UI fault controls, and exact positive restoration.
The accepted APK is the current 94,683,119-byte `5f635e16…` artifact. The complete
[immutable proof](../work-in-progress/combined-recovery/05-full-acceptance/),
including all 551 reports, 22 fresh evidence hashes, 16 command logs, every retained
source/class mutant, and all twelve APK parts, was published and fetched at
`c9373851d4408fb4db63c21873ac2d0bb6867270`. The complete report archive retains its
original bytes through three verified parts and an explicit reassembly mapping.
The [independent review](verification/combined-recovery/05-full-acceptance-independent-review/)
rechecked both full input inventories, all 63 delta inputs, every report member,
all fault artifacts, and every APK part.

The reviewed Trigger05/session03 guard union is activated with its exact 148-test
host proof. It rejects stale capture order and resolved-path/physical-file reuse,
and verifies paired final activity components. The source workflow allows 120
minutes and preserves the complete nested reports tree; its Android job is
unchanged. Fresh hosted source, Android, and editor results for this promoted
candidate remain pending at this publication.

The separate normal-animation diagnostic checked out its frozen original/9108
inputs at `3edcddd86660ea10c8aff71b651b446f86412525` before this promotion.
[Run 38212813248](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38212813248)
failed to obtain stable consecutive TRIGGERS frames for both APKs with animation
scales verified as 1. Its incomplete runtime result is preserved separately;
it does not establish an outcome for the new combined candidate. Historical
26-pixel differences and earlier failure reports remain unchanged. No whole-app
1:1 runtime claim is made.
'''
add(status_path, status.encode(), identity(old_status), origin='Current measured publication status; historical sections retained')

for n in ['preparation.json','manifest.json','blobs.json','external-preservation.json','verify_remote.py','remote-verification.json']:
    p = ROOT / 'combined-proof-transfer' / n
    add(OPS + '/previous-proof-publication/' + n, p.read_bytes(), origin='Closed immutable proof Git transfer and fetched-byte verification')
add(OPS + '/previous-proof-publication/prepare_combined_proof_transfer.py', (ROOT/'prepare_combined_proof_transfer.py').read_bytes())
add(OPS + '/normal-diagnostic-checkout-observation.json', (ROOT/'normal-diagnostic-transfer/checkout-observation.json').read_bytes())
add(OPS + '/prepare_combined_promotion.py', Path(__file__).read_bytes())
jadd(OPS + '/documentation-before-state-chain.json', dict(changes=doc_chain, exact_prepared_docs_activated=True, stale_preparatory_status_not_activated=True))
jadd(OPS + '/activation.json', dict(status='COHERENT_ACCEPTED_COMBINED_SOURCE_APK_AND_REVIEWED_GUARDS',
    immutable_proof_commit=PROOF_COMMIT, source_delta=63, input_files=81291, snapshot_sha256=new['snapshot_sha256'],
    accepted_apk_sha256=new_apk['sha256'], accepted_apk_bytes=new_apk['size_bytes'],
    configured_host_gates_passed=16, registered_methods=1242, cases=193489, python_tests=273, actual_ui_fault_controls=78,
    guard_union_paths=20, guard_host_tests=148, independent_review_checkpoint_sha256=sha(review_raw),
    normal_diagnostic_prior_checkout_completed=True, android_job_source_unchanged=True,
    android_executed_for_new_candidate=False, whole_application_1_to_1_established=False,
    replacements=[dict(path=n,before=guards[n],after=identity(data),mode='100755' if mode&0o111 else '100644',origin=origins[n]) for n,(data,mode) in sorted(desired.items())]))

# Validate every replacement before touching the working tree. Unknown concurrent
# content is rejected; no checkout, hard reset, or deletion is performed.
for name, (data, mode) in desired.items():
    path = REPO / name
    if guards[name] is None:
        assert not path.exists(), name
    else:
        check(path.read_bytes(), guards[name])
for name, (data, mode) in desired.items():
    path = REPO / name; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data); path.chmod(mode)

paths = set(desired)
baselines = {name: None if row is None else row['sha256'] for name,row in guards.items()}
ignored_result = subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(n.encode() for n in sorted(paths))+b'\0',capture_output=True)
assert ignored_result.returncode in (0,1)
ignored = [n.decode() for n in ignored_result.stdout.split(b'\0') if n]
if ignored:
    p=REPO/'.gitignore';before=p.read_bytes();baselines['.gitignore']=sha(before)
    p.write_bytes(before+('\n# Exact accepted combined source and proof\n'+''.join('!'+n+'\n' for n in ignored)).encode());paths.add('.gitignore')
p=REPO/'.gitattributes';before=p.read_bytes();baselines['.gitattributes']=sha(before)
p.write_bytes(before+('\n# Exact combined acceptance review and publication bytes\n'+review_prefix+'/** -text\n'+OPS+'/** -text\n').encode());paths.add('.gitattributes')

run=subprocess.run(['python3','scripts/assemble_artifact.py',manifest_path,'--verify-only'],cwd=REPO,capture_output=True,text=True)
assert run.returncode==0,run.stderr
check((REPO/'project/reports/release-input-snapshot.json').read_bytes(),identity(new_raw))
for name,row in delta.items():
    check((REPO/'project'/name).read_bytes(),row)
verification=dict(artifact_assembly_exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr,
    source_delta_rechecked=63,full_snapshot_file_rechecked=True,android_job_unchanged=True,
    immutable_source_and_artifact_proof_precedes_activation=True)
p=REPO/OPS/'post-application-verification.json';p.write_text(json.dumps(verification,indent=2)+'\n');paths.add(OPS+'/post-application-verification.json');baselines[OPS+'/post-application-verification.json']=None

known={line.split(b' ',1)[0].decode() for line in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
manifest=[];blobs=[];texts=[]
for name in sorted(paths):
    p=REPO/name;data=p.read_bytes();row=dict(path=name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data),mode='100755' if p.stat().st_mode&0o111 else '100644');manifest.append(row)
    try:
        content=data.decode('utf-8');binary='\0' in content
    except UnicodeDecodeError:
        binary=True
    if row['git_blob_sha1'] in known or binary or len(data)>250000:
        blobs.append(row|dict(known=row['git_blob_sha1'] in known,encoding='utf-8' if len(data)>12500000 and data.isascii() else 'base64'))
    else:
        texts.append(dict(path=name,mode=row['mode'],type='blob',content=content))
chunks=[];chunk=[]
for entry in texts:
    if chunk and len(json.dumps(chunk+[entry],ensure_ascii=False).encode())>650000:
        chunks.append(chunk);chunk=[]
    chunk.append(entry)
if chunk:chunks.append(chunk)
for i,chunk in enumerate(chunks):(EXPORT/f'text-{i:02d}.json').write_text(json.dumps(chunk,ensure_ascii=False))
for n,data in [('manifest.json',manifest),('blobs.json',blobs)]:
    (EXPORT/n).write_text(json.dumps(data,indent=2)+'\n')
result=dict(files=len(manifest),bytes=sum(r['size_bytes'] for r in manifest),text_chunks=len(chunks),text_entries=len(texts),
    new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),baselines=baselines,
    source_delta=63,active_guard_paths=20,full_snapshot_file_sha256=sha(new_raw),current_apk_sha256=new_apk['sha256'],
    active_workflow_modified=True,active_app_or_apk_modified=True,full_runtime_parity_established=False)
(EXPORT/'preparation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='baselines'}))
