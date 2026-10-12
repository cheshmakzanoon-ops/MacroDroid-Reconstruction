#!/usr/bin/env python3
"""Freeze all 21 approved sources and every closed bounded proof attempt."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import difflib
import hashlib
import json
import shutil
import tarfile

ROOT=Path(__file__).resolve().parent;STAGE=ROOT/'stage-02';PROJECT=STAGE/'project'
TARGET=ROOT/'checkpoints/03-source-three-path-controls'

def identity(path):
    with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest,'mode':path.stat().st_mode&0o777}
def save(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def copy(path,name):
    target=TARGET/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target);assert identity(path)==identity(target)

def main():
    assert not TARGET.exists();TARGET.mkdir(parents=True)
    prep=json.loads((STAGE/'preparation.json').read_text());changes=[]
    approved={row['path'] for row in prep['allowed_modified_or_new_paths']}
    assert len(approved)==21
    for row in prep['copied_baseline_paths']:
        assert identity(STAGE/'baseline'/row['path'])==row['baseline']
        if row['path'] not in approved:assert identity(PROJECT/row['path'])==row['baseline']
    for row in prep['allowed_modified_or_new_paths']:
        path=PROJECT/row['path'];assert path.is_file()
        if row['baseline'] is not None:assert identity(Path(row['baseline_source']))==row['baseline']
        assert identity(path)!=row['baseline']
        if path.suffix=='.py':ast.parse(path.read_text())
        copy(path,'project/'+row['path']);changes.append({**row,'after':identity(path)})
    old=json.loads((STAGE/'baseline/source/java-method-map.json').read_text());fresh=json.loads((PROJECT/'source/java-method-map.json').read_text())
    assert len(old)==1243 and len(fresh)==1244 and fresh[:-1]==old
    old_ui=json.loads((STAGE/'baseline/source/ui-methods.json').read_text());new_ui=json.loads((PROJECT/'source/ui-methods.json').read_text())
    assert len(old_ui)==11 and len(new_ui)==12 and new_ui[:-1]==old_ui and len({row['target'] for row in new_ui})==11
    original_dependencies=json.loads((STAGE/'baseline/tests/fixtures/original-dependencies.json').read_text())['dependencies']
    dependencies=json.loads((PROJECT/'tests/fixtures/original-dependencies.json').read_text())['dependencies']
    assert len(dependencies)==5 and dependencies[:3]==original_dependencies
    fixture=identity(PROJECT/'tests/fixtures/original-methods.dex');provenance=json.loads((PROJECT/'tests/fixtures/provenance.json').read_text())
    assert fixture['sha256']==provenance['fixture_sha256'] and (provenance['methods'],provenance['registered_methods'],provenance['dependency_methods'],provenance['classes'])==(1249,1244,5,607)
    assert (PROJECT/'source/java/recovered/ui/DayTriggerValueMethods.java').read_bytes()==(STAGE/'baseline/source/java/recovered/ui/DayTriggerValueMethods.java').read_bytes()
    dayclass=[row for row in fresh if row['target']=='Lcom/arlosoft/macrodroid/triggers/DayTrigger;']
    assert len(dayclass)==3 and next(row for row in dayclass if row['method']=='requiresScheduleExactAlarm()Z')==next(row for row in old if row['target']=='Lcom/arlosoft/macrodroid/triggers/DayTrigger;' and row['method']=='requiresScheduleExactAlarm()Z')
    save(TARGET/'merge-manifest.json',{'numeric_checkpoint_sha256':prep['numeric_checkpoint_sha256'],
         'changes':changes,'scope':'Complete 21-path inactive source overlay. Full acceptance, all 101 Java controls and new signed-primary proof remain required before promotion.',
         'expected_separate_numeric_successor_overlap':['day_numeric_dex_controls.py'],
         'day_trigger_registry':dayclass,'all_prior_registry_entries_exact':True,'all_prior_ui_entries_exact':True,
         'all_three_prior_dependencies_exact':True,'numeric_executable_helper_unchanged':True,'fixture_identity':fixture})
    for name,label in [('day_numeric_dex_controls.py','numeric-dependency-only.patch'),('ui_negative_control.py','ui-negative-controls-integration.patch'),('acceptance.py','acceptance-report-inventory.patch')]:
        before=(STAGE/'baseline'/name).read_text();after=(PROJECT/name).read_text()
        (TARGET/label).write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='numeric19/'+name,tofile='lookup-overlay/'+name)))
    copy(STAGE/'preparation.json','preparation.json');copy(ROOT/'PLAN_ADDENDUM.md','PLAN_ADDENDUM.md')
    authored=['prepare_overlay.py','stage_sources.py','lookup_adapter_tail.java.txt','LookupAdapterProbe.java','CompareOriginalFixture.java',
              'run_adapter_probe.py','author_lookup_catalog.py','run_lookup_adapter_controls.py','lookup_report_guards.py.txt',
              'author_lookup_gate.py','wire_lookup_acceptance.py','run_focused_lookup_guards.py','run_lookup_micro_dex.py',
              'run_lookup_report_controls.py','freeze_adapter_checkpoint.py','freeze_complete_lookup_checkpoint.py']
    for name in authored:copy(ROOT/name,'study-tools/'+name)
    evidence=[]
    for folder,prefix in [(ROOT/'reports','reports'),(ROOT/'stage-01','failed-first-derivation-state')]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():evidence.append((path,prefix+'/'+path.relative_to(folder).as_posix()))
    for name in ['stage-02/source-slice.json','stage-02/lookup-input-inventory.compact.json']:
        evidence.append((ROOT/name,name))
    rows=[{'path':name,**identity(path)} for path,name in evidence]
    assert len({row['path'] for row in rows})==len(rows)
    save(TARGET/'evidence-files.json',rows)
    archive=TARGET/'evidence.tar.gz'
    with tarfile.open(archive,'w:gz') as tar:
        for path,name in evidence:tar.add(path,arcname=name,recursive=False)
    with tarfile.open(archive) as tar:
        members=tar.getmembers();assert len(members)==len(rows)
        for member,row in zip(members,rows):
            assert member.isfile() and member.name==row['path'] and member.size==row['bytes'] and member.mode&0o777==row['mode']
            assert hashlib.sha256(tar.extractfile(member).read()).hexdigest()==row['sha256']
    for folder in sorted((ROOT/'reports').iterdir()):
        for name in ['result.json','failure.traceback.txt','reason.json']:
            if (folder/name).is_file():copy(folder/name,'review/'+folder.name+'/'+name)
    for name in ['04-original-jvm-adapter','06-compiled-adapter-controls','10-focused-guards','12-micro-dex-three-path-corrected','14-focused-binding-followup','15-raw-report-guard-controls']:
        assert json.loads((ROOT/'reports'/name/'result.json').read_text())['passed'] is True
    micro=json.loads((ROOT/'reports/12-micro-dex-three-path-corrected/result.json').read_text())
    positive=ROOT/'reports/12-micro-dex-three-path-corrected/positive/result.json'
    helper=ROOT/'reports/04-original-jvm-adapter/hostclasses/recovered/ui/DayTriggerLookupMethods.class'
    report={
        'actual_original_jvm_ui_adapter_cases':371,'actual_compiled_java_faults':10,'actual_original_jvm_and_micro_dex_cases':371,
        'actual_dex_faults':[(row['name'],row['mismatches']) for row in micro['actual_dex_faults']],
        'original_instructions':26,'rebuilt_instructions':23,'conditional_edges_each':4,'uncredited_getter_methods':2,
        'first_91_prepared_job_prefix_unchanged':True,'actual_provenance_rejections':2,'positive_restoration':identity(positive),
        'lookup_helper_class':identity(helper),'initial_focused_tests':73,'final_lookup_focused_tests':33,
        'unique_focused_tests_by_module':{'numeric':35,'existing_widget_catalog':8,'lookup_final':33},
        'raw_report_fault_controls':16,'new_app_execution_from_report_controls':0,
        'new_signed_primary_verified':False,'full_101_ui_java_controls_executed':False,'full_four_dex_acceptance_executed':False,
        'all_suite_combined_cases_executed':False,'androidRuntime':False}
    save(TARGET/'verified-results.json',report)
    doc='''# DayTrigger.p0: complete source overlay and bounded three-path proof

This is the complete **21-path inactive lookup overlay** against frozen numeric19 checkpoint `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f`. It is ready for independent review and an explicit guarded merge with the separately authored numeric command-evidence correction. It has not been promoted to active source, built as a complete APK or signed.

## What actually passed

The actual UI adapter executed all 371 original/JVM inputs with zero mismatches, unsupported executions and independently expected failures. It preserves first matching entry identity, exact iterator/read order, null behavior and injected exception identity. All ten actual compiled Java faults were detected at the measured counts `[127, 3, 2, 3, 233, 1, 369, 233, 25, 6]`; original rows and coverage remained unchanged, and the positive report was restored byte for byte. The complete first 91 prepared jobs, including mutant source, order and required labels, remained exact. This study did not execute those 91 existing jobs again.

The separate production-D8/transplant study executed all 371 cases on original/JVM/micro-DEX paths. Original coverage is 26/26 instructions and 4/4 conditional edges; rebuilt coverage is 23/23 instructions and 4/4 edges. These totals include the two original, uncredited getters. There are no ignored offsets, static substitutions or unsupported paths. Both actual DEX faults were detected: case-sensitive comparison, 127 cases; last-match behavior, 233 cases. Original-as-rebuilt and wrong-helper identity controls failed at their intended Java provenance guards. Positive restoration was byte exact.

The micro compiler sends exactly one relocated helper class to D8, with zero host stubs. It replaces only p0 in the preserved original class and proves all other 33 original methods and non-target text unchanged **within that micro-DEX**. The two executed getters are bound to the exact existing signed APK member. The old signed p0 instruction listing differs from the new positive listing; this old APK therefore cannot satisfy the pending signed-primary gate. See PLAN_ADDENDUM.md for the preserved constant mapping and full three-entry DayTrigger registry.

The original fixture was freshly extracted from the pinned original APK. It contains 1,244 registered methods plus five uncredited getters, or 1,249 methods in 607 classes. Rebuilding the prior numeric selection from it recreated all prior 1,246-method fixture bytes exactly. All prior registry/UI entries and three numeric dependencies are unchanged; only p0 and its two getter selections were appended.

The initial focused test run passed 73 tests: 35 numeric, eight existing Widget catalog and 30 lookup guards. A small follow-up added explicit comparison of each returned control report's configuration and loaded origins with the exact command inputs. All 33 final lookup guard tests passed; the 43 unchanged earlier tests were not repeated unnecessarily. The final validator also rechecked the closed real positive and two DEX-fault reports, rejected 16 deliberately altered reports, and accepted only the specified VM-null diagnostic variant. Those report controls earned zero new app-execution/instruction credit.

## Fidelity and limits

The shared host types retain their fields, constructors, class flags, equality and numeric aliases. Only getEntries and getKey were added. The numeric executable helper source and its compiled class remain exact. The lookup helper's 991-byte class differs from the older standalone proof only through the shared nested-type metadata; its actual compiled identity and full differential results are recorded in verified-results.json.

Generated message text is omitted only for seven fixed VM-null inputs. Their raw messages, NPE type and complete event sequence are retained. Every injected exception must preserve exact message and object identity. The five observer-record faults have zero application credit. This proof concerns the declared typed-list UTF-16 inputs on the pinned host JVM; it does not establish ART Unicode behavior, exhaustive Unicode, erased malformed lists, calendar scheduling, persistence or lifecycle parity.

All sixteen acceptance commands and the 5,400-second full UI-control limit remain unchanged. The UI entry now prepares 101 Java faults, runs both existing numeric and new lookup DEX-control families, retains the 300-second per-UI/restoration limits, and requires the separate lookup DEX report. The new acceptance entry requires a real signed-positive p0 instruction match before success; the current bounded study deliberately does not bypass that requirement.

## Preserved failures and pending gates

The archive preserves the first whitespace-anchor source failure, the stale private fixture-count checker failure, and the first micro-study's retained-mutant-source path error. That first micro attempt had already passed its positive three-path run, but its overall status remains failed. The corrected driver uses a separate output directory and leaves every old artifact intact. No application helper or oracle was changed to resolve those study-tool failures.

The complete 101 Java controls, four acceptance-level DEX faults, signed primary, all-suite three-path results, full sixteen-command acceptance and Android execution are still pending. The prospective global counts are 1,244 recovered bodies, 605 target classes, 12 UI methods in 11 classes, 24,836 UI cases and 195,151 all-suite cases. Those combined case totals are projections, not results of this capsule. No new APK artifact is included or claimed.

The numeric19 dependency-only patch is preserved separately from the expected parent-owned timing/filesystem-witness successor. Neither that unfrozen successor nor any active runtime/workflow changes were absorbed. The exact before hashes in merge-manifest.json must be checked and the overlap merged deliberately before a full build.
'''
    (TARGET/'CHECKPOINT_SCOPE.md').write_text(doc)
    assert all(identity(path)=={key:row[key] for key in ['bytes','sha256','mode']} for (path,_),row in zip(evidence,rows))
    files=[{'path':path.relative_to(TARGET).as_posix(),**identity(path)} for path in sorted(TARGET.rglob('*')) if path.is_file()]
    cp={'schema':1,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'INACTIVE_COMPLETE_LOOKUP_OVERLAY_BOUNDED_THREE_PATH_CONTROLS_PASSED',
        'repo_target':'work-in-progress/day-trigger-lookup/07-source-three-path-controls','files':files,
        'numeric_baseline_checkpoint_sha256':prep['numeric_checkpoint_sha256'],
        'parent_checkpoint_sha256':'c0d1a691aeb857607b1b44ca0eb66a2a5799b8c02726b39e6acec5a0c49646f7',
        'source_path_count':21,'approved_source_path_limit':21,'evidence_file_count':len(rows),'evidence_archive':identity(archive),
        'verified_results':report,'active_source_changed':False,'full_build_or_signing':False,'new_apk':False}
    save(TARGET/'checkpoint.json',cp)
    total=sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file());assert total<=256*1024*1024
    print(json.dumps({'checkpoint':str(TARGET/'checkpoint.json'),**identity(TARGET/'checkpoint.json'),'source_paths':21,
        'files':len(files),'evidence_members':len(rows),'archive':identity(archive),'owned_bytes':total},indent=2))

if __name__=='__main__':main()
