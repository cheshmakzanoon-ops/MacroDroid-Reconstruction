#!/usr/bin/env python3
"""Read-only final review of the closed sixteen-screen workflow and its evidence."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import collections
import difflib
import gzip
import hashlib
import json
import re
import shutil
import stat
import traceback

ROOT = Path('/dev/shm/macrodroid-settings-final-root-review')
A = Path('/dev/shm/settings-enable-return-workflow-01/checkpoints/01-multipart-workflow-and-offline-validation')
B = A.parent / '02-content-reference-verification'
OUT = ROOT / 'review-01'
EXPECTED = [('workflow', A, 142204, '5f64e5e87270fd1f2e5203bdc54559c50c4920102451f9761c58c2f269b72cfa', 602),
            ('reader', B, 3041, '819ce0d2b72ea9e1179ac87cc30613c72e10efb8f6eac45621ed0fe02cead92b', 12)]
PARENT = 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'

def need(value, message):
    if not value:
        raise ValueError(message)

def digest(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def read_json(p):
    return json.loads(p.read_bytes())

def write(name, value):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')

def copy(p, name):
    q = OUT / name
    q.parent.mkdir(parents=True, exist_ok=True)
    with q.open('xb') as stream:
        stream.write(p.read_bytes())

def file_identity(p):
    s = p.lstat()
    need(stat.S_ISREG(s.st_mode) and p.resolve() == p, 'Not a confined regular file: ' + str(p))
    return dict(**digest(p.read_bytes()), mode='100755' if s.st_mode & 0o111 else '100644')

def audit_capsules():
    result = []
    for label, base, size, sha, count in EXPECTED:
        raw = (base / 'checkpoint.json').read_bytes()
        need(digest(raw) == dict(bytes=size, sha256=sha), label + ' checkpoint identity')
        cp = json.loads(raw)
        rows = cp['files']
        need(len(rows) == count and len({r['path'] for r in rows}) == count, label + ' membership count')
        actual_members = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() or p.is_symlink()}
        need(actual_members == {r['path'] for r in rows} | {'checkpoint.json'}, label + ' exact membership')
        total = 0
        for r in rows:
            path = PurePosixPath(r['path'])
            need(not path.is_absolute() and '..' not in path.parts and path.as_posix() == r['path'], 'Unsafe payload path')
            actual = file_identity(base / r['path'])
            need(actual == {k:r[k] for k in ('bytes','sha256','mode')}, label + ' payload: ' + r['path'])
            result.append(dict(capsule=label, path=r['path'], **actual))
            total += r['bytes']
        need(total == cp['frozen_payload_bytes'], label + ' payload byte total')
    return result

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    copy(Path(__file__), 'executed-reviewer.py')
    report = dict(status='REVIEWING_CLOSED_SETTINGS_WORKFLOW', passed=False,
                  started_utc=datetime.now(timezone.utc).isoformat(), android_executed=False,
                  application_build_executed=False, host_suite_reexecuted=False,
                  production_verifier_reexecuted=False, full_runtime_1_to_1_established=False)
    code = 2
    try:
        before = audit_capsules()
        write('capsule-payloads-before.json', before)
        for label, base, *_ in EXPECTED:
            copy(base/'checkpoint.json', 'inputs/'+label+'-checkpoint.json')
        mapping = read_json(A/'proposed-source-files.json')
        need(len(mapping)==4, 'Exactly four reviewed execution sources')
        source_ids = {}
        for r in mapping:
            actual = file_identity(A/r['source'])
            need(actual == {k:r[k] for k in ('bytes','sha256','mode')}, 'Proposed source identity')
            source_ids[r['source']] = {k:r[k] for k in ('bytes','sha256')}
            copy(A/r['source'], 'reviewed-source/'+r['source'])
        copy(A/'proposed-source-files.json','proposed-source-files.json')
        outer = read_json(A/'review/reports/validation-01/result.json')
        actual = read_json(A/'review/reports/validation-01/validation/result.json')
        need(outer['exit_code']==0 and outer['timed_out'] is False and outer['timeout_seconds']==900,
             'Actual bounded outer validation passed')
        need(outer['input_count']==402 and outer['all_immutable_input_bytes_and_modes_unchanged'] is True,
             'Actual protected input result')
        for stream in ('stdout.txt','stderr.txt'):
            p=A/'review/reports/validation-01'/stream
            need(digest(p.read_bytes()) == {k:outer[stream][k] for k in ('bytes','sha256')}, 'Outer raw stream binding')
        need(actual['passed'] is True and actual['android_executed'] is False, 'Closed offline result flags')
        need(actual['helpers_before']==actual['helpers_after']==source_ids, 'Four executed sources unchanged')
        protected_before=(A/'review/reports/validation-01/inputs-before.json').read_bytes()
        protected_after=(A/'review/reports/validation-01/inputs-after.json').read_bytes()
        need(protected_before==protected_after and len(json.loads(protected_before))==402, '402 protected identities unchanged')
        input_faults = ['changed-original-manifest','changed-active-manifest','changed-chronology-guard',
            'changed-animation-helper','changed-readiness-guard','changed-navigation-guard','changed-observed-dialog',
            'symlinked-runtime-input','changed-reviewed-finalizer','missing-archive-part-1-with-existing-logical',
            'missing-archive-part-2-with-existing-logical','changed-archive-part-1-with-existing-logical',
            'truncated-archive-part-2-with-existing-logical','changed-archive-manifest',
            'symlinked-archive-part-with-existing-logical','wrong-existing-logical-archive']
        inventory_faults=['omit-runtime-row','empty-inventory','duplicate-row','reorder-rows','extra-row',
            'changed-source-and-copy-retained','changed-source-and-copy-omitted','changed-source-and-copy-empty',
            'changed-source-and-copy-rehashed','changed-copy-retained','changed-copy-rehashed','omit-reviewed-copy-role',
            'legacy-readiness-schema','boolean-readiness-schema','missing-readiness-policy-pin','changed-readiness-policy-pin',
            'missing-navigation-policy-pin','changed-navigation-policy-pin','older-fourteen-plan-pin',
            'missing-settings-contract-pin','changed-settings-contract-pin']
        expected=[('bash-syntax-%02d'%i,0) for i in range(1,7)]+[('exact-frozen-preflight',0)]
        expected += [(x,1) for x in input_faults]
        expected += [('matching-existing-logical-preflight',0),('existing-output',1),('exact-offline-apk-preflight',0)]
        expected += [('inventory-'+x+'-'+stage,rc) for x in inventory_faults for stage,rc in [('materialized',1),('final',2)]]
        expected += [('workflow-policy-controls',0),('packaged-host-controls-0',0),('packaged-host-controls-2',0),
                     ('owned-cleanup-clean',0),('owned-cleanup-failed-journey',7),('owned-cleanup-failed-service',1)]
        need(len(expected)==74 and [(r['label'],r['exit_code']) for r in actual['commands']]==expected, 'All 74 exact command outcomes')
        command_bindings=[]
        for r in actual['commands']:
            need(r['timed_out'] is False and r['android_executed'] is False, 'No command timeout or Android execution')
            base=A/'review/reports/validation-01/validation/commands'/r['label']
            need(read_json(base/'command.json')==r, 'Command receipt differs from closed result: '+r['label'])
            command_bindings.append(dict(command=r, stdout=digest((base/'stdout.txt').read_bytes()),
                                         stderr=digest((base/'stderr.txt').read_bytes())))
        write('literal-command-bindings.json',command_bindings)
        positive=read_json(A/'review/reports/validation-01/validation/commands/exact-frozen-preflight/stdout.txt')
        need(positive['passed'] is True and positive['android_executed'] is False and len(positive['files'])==317,
             'Full successful frozen preflight')
        need(positive['plan_sha256']=='ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211'
             and type(positive['requested_report_schema']) is int and positive['requested_report_schema']==7
             and positive['requested_scales']=='0' and positive['full_runtime_1_to_1_established'] is False,
             'Exact sixteen-screen plan schema and scope')
        need(positive['settings_contract_sha256']=='379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07',
             'Exact observed Settings contract')
        prep=actual['multipart_preparation']
        need(prep['logical_archive_existed'] is False and prep['action']=='ASSEMBLED_MISSING_LOGICAL_ARCHIVE'
             and prep['transport_before']==prep['transport_after'] and prep['verified']['verified_members']==353,
             'Literal sparse-checkout multipart assembly and unchanged transport')
        matching=read_json(A/'review/reports/validation-01/validation/commands/matching-existing-logical-preflight/stdout.txt')
        need(matching['passed'] is True and matching['guard_archive_preparation']['logical_archive_existed'] is True,
             'Matching existing logical archive still passes transport guard')
        materialized=read_json(A/'review/reports/validation-01/validation/commands/exact-offline-apk-preflight/stdout.txt')
        need(materialized['passed'] is True and materialized['android_executed'] is False, 'Read-only APK prevalidation')
        need([(r['label'],r['bytes'],r['apk_sha256']) for r in materialized['apk_prevalidation']]==[
            ('original',95725918,'84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
            ('candidate',94683136,'0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd')], 'Both fixed APK identities')
        policy=read_json(A/'review/reports/validation-01/validation/commands/workflow-policy-controls/stdout.txt')
        need(policy['passed'] is True and policy['positive_and_restore'] is True and len(policy['negative_controls'])==10
             and all(r['rejected'] is True for r in policy['negative_controls']), 'Ten policy faults and restoration')
        tests=[]
        for label,count in [('packaged-host-controls-0',6),('packaged-host-controls-2',10)]:
            raw=(A/'review/reports/validation-01/validation/commands'/label/'stdout.txt').read_text()
            names=re.findall(r'^(test_[^\s]+) ',raw,re.M)
            need(len(names)==len(set(names))==count and re.search(r'\nRan '+str(count)+r' tests in [0-9.]+s\n\nOK\n\s*$',raw),
                 'Literal named host controls: '+label)
            tests.append(dict(label=label, passed=count,names=names))
        write('additional-host-controls.json',tests)
        meta=read_json(A/'complete-evidence-index.json.metadata')
        compressed=(A/'complete-evidence-index.json.gz').read_bytes()
        raw_index=gzip.decompress(compressed)
        need(digest(compressed)==meta['compressed'] and digest(raw_index)==meta['uncompressed'], 'Exact compressed and raw index')
        index=json.loads(raw_index)
        records=index['files']; indexed={r['path']:r for r in records}
        need(len(indexed)==len(records)==16454, 'Exact indexed path count')
        regular=[r for r in records if r['kind']=='regular']; links=[r for r in records if r['kind']=='inert_symlink']
        need(len(regular)==16452 and len(links)==2 and sum(r['bytes'] for r in regular)==7114730719, 'Index regular/link/logical totals')
        declared={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in read_json(A/'checkpoint.json')['files']}
        reader=read_json(B/'corrected-reader/result.json')
        need(reader['passed'] is True and reader['status']=='COMPLETE_FROZEN_SETTINGS_EVIDENCE_VERIFIED'
             and reader['checkpoint']==dict(bytes=142204,sha256=EXPECTED[0][3]), 'Exact closed successful reader binding')
        reads={}
        for r in reader['git_reads']:
            need(r['commit']==PARENT and r['exit_code']==0 and r['timeout_seconds']==30
                 and r['stderr']==digest(b''), 'Bounded successful immutable Git read receipt')
            key=(r['commit'],r['path'])
            if key in reads: need(reads[key]==r['stdout'], 'Repeated immutable Git read identity')
            reads[key]=r['stdout']
        refs={}; multi={}; local_count=0
        for r in regular:
            ref=r['content']; expected_bytes={k:r[k] for k in ('bytes','sha256')}
            if ref['kind']=='capsule_file':
                need(declared.get(ref['path'])==expected_bytes, 'Locally frozen index reference: '+r['path'])
                local_count+=1
            elif ref['kind']=='git_blob':
                key=(ref['commit'],ref['path'])
                need(reads.get(key)==expected_bytes, 'Closed Git read/index bytes: '+r['path'])
                value=(expected_bytes,ref['git_blob_sha1'])
                if key in refs: need(refs[key]==value, 'Consistent Git identity for repeated content')
                refs[key]=value
            elif ref['kind']=='multipart_manifest':
                key=(ref['commit'],ref['path'])
                need(key in reads and reads[key]['sha256']==ref['manifest_sha256'], 'Closed multipart manifest read binding')
                if 'manifest_bytes' in ref: need(reads[key]['bytes']==ref['manifest_bytes'], 'Manifest bytes binding')
                if key in multi: need(multi[key]==expected_bytes, 'Consistent logical multipart identity')
                multi[key]=expected_bytes
            else: need(False,'Unknown reference kind')
        need(len(refs)==reader['unique_git_blob_references']==173 and len(multi)==reader['reassembled_multipart_references']==3
             and len(reader['git_reads'])==202 and local_count==1246, 'Exact reference and read counts')
        prefix='reports/validation-01/validation/private-inputs/'
        need(len({r['copy'] for r in positive['files']})==317, 'Distinct complete copy roles')
        for r in positive['files']:
            expected_bytes={k:r[k] for k in ('bytes','sha256')}
            for path in (prefix+r['path'],prefix+'ci-exact-alarm-enable-return/'+r['copy']):
                need(path in indexed and {k:indexed[path][k] for k in ('bytes','sha256')}==expected_bytes,
                     'Exact preflight source/copy indexed binding: '+path)
        faults=[]
        for label in input_faults[-7:]:
            name='reports/validation-01/validation/input-faults/'+label+'/ci-exact-alarm-enable-return/input-preflight.json'
            ref=indexed[name]['content']
            need(ref['kind']=='capsule_file','Retained transport-fault JSON')
            r=read_json(A/ref['path'])
            need(r['passed'] is False and r['files']==[] and r['android_executed'] is False, 'Transport rejected before input copying: '+label)
            faults.append(dict(label=label,status=r['status'],reason=r['reason'],copied_inputs=0))
        write('transport-failures-before-copy.json',faults)
        old=(B/'retained-failure/executed-verifier.py').read_text()
        new=(B/'corrected-reader/verify_frozen_evidence.py').read_text()
        expected_new=old.replace("key = (reference['commit'], reference['path'])", "key = ('git_blob', reference['commit'], reference['path'])",1)
        expected_new=expected_new.replace("key = (reference['commit'], reference['path'])", "key = ('multipart_manifest', reference['commit'], reference['path'])",1)
        expected_new=expected_new.replace('raw = git(*key)','raw = git(*key[1:])')
        need(new==expected_new,'Reader correction restricted to two role-qualified keys and two call argument slices')
        old_result=read_json(B/'retained-failure/result.json')
        need(old_result['passed'] is False and old_result['reason']=='ValueError: Referenced exact logical bytes differ', 'First reader failure preserved literally')
        need(read_json(B/'bindings/final-frozen-payload-rehash.json')['files']==read_json(A/'checkpoint.json')['files'], 'Reader final unchanged payload rows')
        copy(B/'corrected-reader/result.json','inputs/closed-reader-result.json')
        copy(B/'corrected-reader/derivation.patch','inputs/reader-correction.patch')
        copy(A/'closed-validation-summary.json','inputs/closed-validation-summary.json')
        write('reference-binding-review.json',dict(index=digest(raw_index), compressed=digest(compressed),
              indexed_paths=16454,regular_paths=16452,inert_symlinks=links,logical_bytes=7114730719,
              local_reference_uses=local_count, unique_git_references=len(refs),unique_multipart_references=len(multi),
              closed_reader_git_commands=202, complete_source_and_copy_roles=317,
              root_reexecuted_reader=False, limitation='Immutable Git bytes and multipart stream reconstruction were executed by the closed reviewed reader; this root pass binds its exact receipts to the independently rehashed capsules and index, without rerunning or copying large content.'))
        after=audit_capsules(); need(after==before,'All reviewed payloads unchanged after audit')
        write('capsule-payloads-after.json',after)
        activation=dict(status='ROOT_REVIEW_CLEARED_CONDITIONAL_ON_FETCHED_PUBLICATION',
            required_published_checkpoint_sha256=[EXPECTED[0][3],EXPECTED[1][3]],
            existing_helpers_to_compare=[r for r in mapping if r['target'].startswith('work-in-progress/')],
            absent_active_path_to_add=[r for r in mapping if r['target'].startswith('.github/workflows/')],
            all_other_source_apk_workflow_and_historical_paths_must_remain_unchanged=True,
            automatic_run_only=True,additional_manual_dispatch_authorized=False,
            app_or_apk_promotion_authorized=False)
        write('activation-clearance.json',activation)
        report.update(status='CLOSED_ROOT_SETTINGS_WORKFLOW_ACTIVATION_REVIEW',passed=True,
            rehashed_payloads=614,reviewed_executable_sources=4,actual_offline_commands=74,
            complete_source_and_copy_roles=317,protected_identities_unchanged=402,
            source_controls_reused=259,additional_controls_passed=16,source_and_transport_faults=16,
            inventory_faults_at_each_of_two_entry_points=21,policy_faults=10,
            root_source_review='Complete preparer, final verifier, offline validator and workflow reviewed. The fixed 16-screen journey preserves full-pixel/XML comparison and measured outcomes, observes Settings state before a guarded toggle/back, retains all bounded cleanup outcomes, and claims no universal parity.',
            initial_inline_inspection_note='Two read-only shape inspections assumed object containers where a list and an integer occurred; both inspections stopped without modifying inputs. This executed audit uses the observed schemas. No validation or application outcome was changed.')
        code=0
    except Exception as error:
        report.update(status='ROOT_SETTINGS_WORKFLOW_REVIEW_FAILED',reason=type(error).__name__+': '+str(error),traceback=traceback.format_exc())
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    write('result.json',report)
    readme='# Final root review: sixteen-screen Settings enable and return\n\n'
    readme+='This capsule contains the executed read-only audit and literal result. It adds no application change and no Android claim. The exact source workflow and reader checkpoints are retained with the review.\n\n'
    readme+='The audit checks all 614 frozen payloads before and after, the actual 74 offline commands and their raw stream identities, all 317 input-copy roles, the 402 preserved input identities, named 6+10 helper controls, and the index-to-reader publication bindings. The earlier 259 source controls and immutable-content reader are reused as closed evidence; they were not run again by this audit.\n\n'
    readme+='If the result passed, activation is limited to the single absent top-level workflow after the three existing helper paths and the required published review checkpoints are fetched and verified. The underlying original and numeric APK identities remain fixed. One automatic hosted run can then measure the full Settings journey.\n'
    with (OUT/'README.md').open('x') as stream: stream.write(readme)
    files=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): files.append(dict(path=p.relative_to(OUT).as_posix(),**file_identity(p)))
    cp=dict(schema=1,status=report['status'],passed=report['passed'],created_utc=datetime.now(timezone.utc).isoformat(),
            repo_target='docs/verification/exact-alarm-enable-return/root-final-workflow-review',
            active_files=[],android_executed=False,application_build_executed=False,full_runtime_1_to_1_established=False,
            frozen_payload_count=len(files),frozen_payload_bytes=sum(r['bytes'] for r in files),files=files)
    write('checkpoint.json',cp)
    print(json.dumps(dict(status=report['status'],checkpoint=str(OUT/'checkpoint.json'),**digest((OUT/'checkpoint.json').read_bytes()),payloads=len(files))))
    return code

if __name__=='__main__':
    raise SystemExit(main())
