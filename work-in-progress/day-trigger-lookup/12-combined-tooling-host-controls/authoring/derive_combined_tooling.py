#!/usr/bin/env python3
"""Derive the additive nine-path combined acceptance implementation."""
from pathlib import Path
import ast,copy,hashlib,json

ROOT=Path(__file__).resolve().parent
TOOLS=ROOT/'combined-host-01/repository/tools/day_trigger_acceptance'
DESIGN=ROOT/'checkpoints/06-combined-host-workflow-design/evidence/reports/22-combined-host-design-source'
FINAL=ROOT/'checkpoints/05-lookup-recorder-successor'
MERGE=ROOT/'checkpoints/04-numeric-filesystem-merge'

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def ident(path):return {'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def replace(text,old,new):
    assert text.count(old)==1,(old[:150],text.count(old))
    return text.replace(old,new,1)
def replace_fn(text,name,new):
    tree=ast.parse(text);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    lines=text.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1])+new.rstrip()+'\n'+''.join(lines[node.end_lineno:])

def main():
    pins=json.loads((TOOLS/'pins.json').read_text())
    source=json.loads((DESIGN/'two-stage-source-contract.json').read_text())
    counts=json.loads((DESIGN/'source-derived-counts.json').read_text())
    method=json.loads((DESIGN/'lookup-prior-method-proof-bindings.json').read_text())
    contract=json.loads((DESIGN/'proposed-command-and-report-contract.json').read_text())
    pins['scope']='Separate combined DayTrigger numeric and lookup WIP source acceptance; host only, no active promotion'
    pins['numeric_future_snapshot']=pins['future_snapshot'];pins['numeric_future_manifest']=pins['future_manifest']
    pins['numeric_ui_mutation_inventory']=pins['ui_mutation_inventory']
    pins['lookup_commit']='39250fac022aee5551f36782bafd72cabbc33718'
    pins['lookup_capsules']={
      'merge':{'path':'work-in-progress/day-trigger-lookup/08-numeric-filesystem-merge','checkpoint':ident(MERGE/'checkpoint.json'),'file_count':62},
      'successor':{'path':'work-in-progress/day-trigger-lookup/09-lookup-recorder-successor','checkpoint':ident(FINAL/'checkpoint.json'),'file_count':56}}
    pins['lookup_final_overlay_manifest']=ident(FINAL/'complete-future-overlay-manifest.json')
    pins['lookup_source_changes']=source['lookup_stage_changes']
    pins['lookup_payload_resolutions']=[{'path':row['path'],'source':row['source'],
      'capsule':'successor' if row['path'] in ['day_lookup_dex_controls.py','tests/test_day_lookup.py'] else 'merge'} for row in pins['lookup_source_changes']]
    pins['source_union_paths']=[row['path'] for row in source['union']]
    pins['numeric_only_files']=source['numeric_only_paths']
    pins['future_snapshot']={k:source['complete_snapshots'][2][k] for k in ('files','snapshot_sha256')}
    pins['future_manifest']=source['complete_snapshots'][2]['manifest']
    pins['fixture']=ident(ROOT/'stage-04/project/tests/fixtures/original-methods.dex')
    for key in ['registered_methods','target_classes','fixture_methods','fixture_classes','suite_cases','all_cases','python_tests']:
        pins[key]=counts[key]
    pins['original_dependency_methods']=counts['uncredited_dependencies']
    pins['ui_mutation_inventory']=json.loads((DESIGN/'proposed-ui-mutation-inventory.json').read_text())
    pins['fresh_reports']=contract['fresh_reports']
    pins['lookup_positive_pipeline']=method['positive_pipeline']
    pins['lookup_class_names']=method['runtime_class_names']
    pins['lookup_vm_null_cases']=method['vm_null_cases']
    pins['lookup_java_failure_counts']=method['java_fault_mismatch_counts']
    pins['lookup_input_inventory_sha256']=method['input_inventory_sha256']
    pins['day_trigger_class_mappings']=json.loads((DESIGN/'day-trigger-registry-and-dependencies.json').read_text())['class_mappings']
    pins['combined_dependencies']=json.loads((DESIGN/'day-trigger-registry-and-dependencies.json').read_text())['dependencies']
    pins['dependency_declaration']=ident(ROOT/'stage-04/project/tests/fixtures/original-dependencies.json')
    # Exact functions provide the source-derived cwd evidence; individual method rows do not record cwd.
    pins['method_producer_sources']={}
    for name in ['day_numeric_dex_controls.py','day_lookup_dex_controls.py','ui_negative_control.py']:
        pins['method_producer_sources'][name]=ident(ROOT/'stage-04/project'/name)
    pins['method_producer_sources']['build.py']={'bytes':20325,'sha256':'dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0'}
    save(TOOLS/'pins.json',pins)

    p=TOOLS/'inputs.py';text=p.read_text();text=replace_fn(text,'contract',(ROOT/'combined_input_contract.py.txt').read_text())
    text=text.replace("'inputs/' + role + '/' + row['path']", "'inputs/' + role + '/' + row['source']")
    p.write_text(text)

    p=TOOLS/'prepare.py';text=p.read_text()
    helper='''def apply_source_stages(project, output, pins, before, future, context):
    """Physically scan the complete tree before and after each exact source stage."""
    def scan(label, expected):
        actual = inputs.scan_inputs(project)
        inputs.compare_inputs(actual, expected)
        path = output / 'inputs' / (label + '-complete-inputs.json')
        with path.open('xb') as stream:
            stream.write(inputs.encoded(actual))
        inputs.require(inputs.identity(path) == inputs.byte_identity(inputs.encoded(expected)), 'Saved complete scan differs: ' + label)
    scan('baseline', before)
    inputs.apply_changes(project, context['numeric_root'], pins['source_changes'])
    scan('numeric', context['numeric_snapshot'])
    inputs.apply_changes(project, output / 'inputs/lookup-overlay', pins['lookup_source_changes'])
    scan('combined', future)
    return inputs.prepared_stage_records(pins, context)


'''
    text=replace(text,'def main():',helper+'def main():')
    text=replace(text,"    parser.add_argument('--overlay-repository', type=Path, required=True)","    parser.add_argument('--overlay-repository', type=Path, required=True)\n    parser.add_argument('--lookup-repository', type=Path, required=True)")
    text=replace(text,'    baseline, overlay = args.baseline_repository.resolve(), args.overlay_repository.resolve()',
                 '    baseline, overlay, lookup = args.baseline_repository.resolve(), args.overlay_repository.resolve(), args.lookup_repository.resolve()')
    text=text.replace('(baseline, overlay, job)', '(baseline, overlay, lookup, job)')
    text=replace(text,'        pins, before, future, capsule = inputs.contract(baseline, overlay)',
                 "        pins, before, future, context = inputs.contract(baseline, overlay, lookup)\n        capsule = context['numeric_root']")
    text=replace(text,"        report['overlay_checkout'] = inputs.verify_git_commit(overlay, pins['overlay_commit'])", 
                 "        report['overlay_checkout'] = inputs.verify_git_commit(overlay, pins['overlay_commit'])\n        report['lookup_checkout'] = inputs.verify_git_commit(lookup, pins['lookup_commit'])")
    text=replace(text,"        inputs.write_json(retained / 'source-changes.json', pins['source_changes'])",
                 "        inputs.write_json(retained / 'source-changes.json', pins['source_changes'])\n        inputs.write_json(retained / 'lookup-source-changes.json', pins['lookup_source_changes'])")
    text=replace(text,"        shutil.copyfile(capsule / 'checkpoint.json', retained / 'source-checkpoint.json')",
                 "        shutil.copyfile(capsule / 'checkpoint.json', retained / 'source-checkpoint.json')\n        for role in ('merge', 'successor'):\n            shutil.copyfile(context['lookup_roots'][role] / 'checkpoint.json', retained / ('lookup-' + role + '-checkpoint.json'))")
    text=replace(text,"            target = retained / 'overlay' / row['path']", "            target = retained / 'overlay' / row['source']")
    text=replace(text,"        for row in pins['baseline_repository_files']:\n            target = retained / 'baseline-tools' / row['path']",
                 "        for row in context['lookup_payloads']:\n            target = retained / 'lookup-overlay/project' / row['path']\n            target.parent.mkdir(parents=True, exist_ok=True)\n            shutil.copyfile(row['source'], target)\n            inputs.require(inputs.identity(target) == row['identity'], 'Retained lookup payload differs')\n        for row in pins['baseline_repository_files']:\n            target = retained / 'baseline-tools' / row['path']")
    text=replace(text,"        inputs.compare_inputs(inputs.scan_inputs(project), before)\n        report['baseline_complete_input_verification'] = {k: before[k] for k in ('files', 'snapshot_sha256')}\n        inputs.apply_changes(project, capsule, pins['source_changes'])\n        inputs.compare_inputs(inputs.scan_inputs(project), future)\n        report['future_complete_input_verification'] = {k: future[k] for k in ('files', 'snapshot_sha256')}",
                 "        report['source_stages'] = apply_source_stages(project, output, pins, before, future, context)")
    text=replace(text,"        report.update(status='EXACT_19_FILE_WIP_PREPARED', passed=True,\n                      complete_baseline_files_checked=81291, complete_future_files_checked=81298,\n                      source_changes_applied=19, new_files=7)",
                 "        report.update(status='EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED', passed=True,\n                      complete_baseline_files_checked=before['files'], complete_numeric_files_checked=context['numeric_snapshot']['files'],\n                      complete_future_files_checked=future['files'], numeric_source_changes_applied=19,\n                      lookup_source_changes_applied=21, distinct_final_source_paths=25, new_files=13)\n        inputs.verify_prepared_boundaries(pins, report, output, context)")
    text=replace(text,"        report['error'] = repr(error)","        report.update(passed=False, status='PREPARATION_FAILED', error=repr(error))")
    text=text.replace('Materialize a fixed baseline and apply exactly the reviewed nineteen-file overlay.',
                      'Materialize a fixed baseline; physically verify Numeric19 and then Lookup21 separately.')
    p.write_text(text)

    for name in ['run_acceptance.py','verify.py']:
        p=TOOLS/name;text=p.read_text()
        text=replace(text,"    parser.add_argument('--overlay-repository', type=Path, required=True)","    parser.add_argument('--overlay-repository', type=Path, required=True)\n    parser.add_argument('--lookup-repository', type=Path, required=True)")
        text=text.replace("'EXACT_19_FILE_WIP_PREPARED'","'EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED'")
        if name=='run_acceptance.py':
            text=replace(text,'        pins, _, expected, _ = inputs.contract(args.baseline_repository, args.overlay_repository)',
                         '        pins, _, expected, context = inputs.contract(args.baseline_repository, args.overlay_repository, args.lookup_repository)')
            text=replace(text,"        project = Path(prepared['project'])", "        inputs.verify_prepared_boundaries(pins, prepared, output, context)\n        project = Path(prepared['project'])")
        else:
            text=text.replace('(args.baseline_repository, args.overlay_repository, Path(__file__).resolve().parents[2])',
                              '(args.baseline_repository, args.overlay_repository, args.lookup_repository, Path(__file__).resolve().parents[2])')
            text=replace(text,'        pins, _, future, _ = inputs.contract(args.baseline_repository, args.overlay_repository)',
                         '        pins, _, future, context = inputs.contract(args.baseline_repository, args.overlay_repository, args.lookup_repository)')
            text=replace(text,"        inputs.verify_git_commit(args.overlay_repository, pins['overlay_commit'])",
                         "        inputs.verify_git_commit(args.overlay_repository, pins['overlay_commit'])\n        inputs.verify_git_commit(args.lookup_repository, pins['lookup_commit'])")
            text=replace(text,"        project = Path(prepared['project'])", "        inputs.verify_prepared_boundaries(pins, prepared, output, context)\n        project = Path(prepared['project'])")
        p.write_text(text)

    p=TOOLS/'verify.py';text=p.read_text()
    text=replace(text,'and len(hashes) == 23','and len(hashes) == 24')
    text=text.replace("('dependency_methods', 3)","('dependency_methods', pins['original_dependency_methods'])")
    text=text.replace("('methodsCovered', 1243), ('methodsExpected', 1243)","('methodsCovered', pins['registered_methods']), ('methodsExpected', pins['registered_methods'])")
    text=text.replace('== 1243 and set(flat)',"== pins['registered_methods'] and set(flat)")
    text=text.replace('== 1243 and set(changed)',"== pins['registered_methods'] and set(changed)")
    text=replace(text,"'dayNumericDexControlsPassed': True, 'androidRuntime': False},", "'dayNumericDexControlsPassed': True, 'dayLookupDexControlsPassed': True, 'androidRuntime': False},")
    text=replace(text,"'ALL_91_JAVA_AND_TWO_NUMERIC_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED'", "'ALL_101_JAVA_AND_FOUR_DAY_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED'")
    text=replace(text,"count(report.get(name), 91, 'UI fault control count differs')", "count(report.get(name), 101, 'UI fault control count differs')")
    text=replace(text,"count(report.get('restorationCases'), 24465, 'UI restoration omitted cases')", "count(report.get('restorationCases'), pins['suite_cases']['ui'], 'UI restoration omitted cases')")
    text=replace(text,'isinstance(rows, list) and len(rows) == 91','isinstance(rows, list) and len(rows) == 101')
    text=replace(text,"             'dayNumericInputInventorySha256', 'dayNumericOriginalCoverage')", "             'dayNumericInputInventorySha256', 'dayNumericOriginalCoverage',\n             'dayLookupRecoveredMethods', 'dayLookupOriginalDependencyMethods', 'dayLookupOriginalDependencyKeys',\n             'dayLookupInputInventorySha256', 'dayLookupOriginalCoverage', 'dayLookupGeneratedNullMessageCases',\n             'dayLookupObserverRecordControls')")
    text=replace(text,"count(row.get(field), 1243, 'Static/linkage gate omitted the numeric method')", "count(row.get(field), 1244, 'Static/linkage gate omitted a recovered DayTrigger method')")
    p.write_text(text)
    print('Derived source boundaries, final pins and narrow parent integrations; lookup verifier/tests still pending.')

if __name__=='__main__':main()
