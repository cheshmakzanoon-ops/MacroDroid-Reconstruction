#!/usr/bin/env python3
"""Freeze closed p0 adapter evidence without claiming its pending signed gate."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import shutil
import tarfile

ROOT=Path(__file__).resolve().parent
STAGE=ROOT/'stage-02'; PROJECT=STAGE/'project'
TARGET=ROOT/'checkpoints/02-original-jvm-adapter-controls'

def identity(path):
    with path.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest,'mode':path.stat().st_mode&0o777}
def save(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def copy(path,name):
    dst=TARGET/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dst);assert identity(path)==identity(dst)

def main():
    assert not TARGET.exists();TARGET.mkdir(parents=True)
    prep=json.loads((STAGE/'preparation.json').read_text())
    assert prep['numeric_checkpoint_sha256']=='c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
    for row in prep['copied_baseline_paths']:
        assert identity(STAGE/'baseline'/row['path'])==row['baseline']
    changed=[];pending=[]
    for row in prep['allowed_modified_or_new_paths']:
        path=PROJECT/row['path']; baseline=row['baseline']
        if baseline is not None:assert identity(Path(row['baseline_source']))==baseline
        if path.is_file() and identity(path)!=baseline:
            copy(path,'project/'+row['path']);changed.append({**row,'after':identity(path)})
        else:pending.append(row['path'])
    assert len(changed)==18 and len(pending)==3
    save(TARGET/'merge-manifest.json',{'numeric_baseline':prep['numeric_checkpoint_sha256'],'changed':changed,'pending':pending,
        'scope':'Inactive partial source integration. Do not promote or merge as complete acceptance: the DEX runner, its focused tests and final acceptance wiring remain pending.'})
    before=(STAGE/'baseline/day_numeric_dex_controls.py').read_text();after=(PROJECT/'day_numeric_dex_controls.py').read_text()
    (TARGET/'numeric-dependency-only.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='numeric19/day_numeric_dex_controls.py',tofile='lookup-overlay/day_numeric_dex_controls.py')))
    copy(STAGE/'preparation.json','preparation.json')
    authored=['prepare_overlay.py','stage_sources.py','lookup_adapter_tail.java.txt','LookupAdapterProbe.java',
              'CompareOriginalFixture.java','run_adapter_probe.py','author_lookup_catalog.py','run_lookup_adapter_controls.py',
              'freeze_adapter_checkpoint.py']
    for name in authored:copy(ROOT/name,'study-tools/'+name)
    evidence=[]
    roots=[(ROOT/'reports','reports'),(ROOT/'stage-01','failed-first-derivation-state')]
    for folder,prefix in roots:
        for path in sorted(folder.rglob('*')):
            if path.is_file():evidence.append((path,prefix+'/'+path.relative_to(folder).as_posix()))
    for name in ['stage-02/source-slice.json','stage-02/lookup-input-inventory.compact.json']:
        evidence.append((ROOT/name,name))
    rows=[{'path':name,**identity(path)} for path,name in evidence]
    assert len({row['path'] for row in rows})==len(rows)
    for name in ['04-original-jvm-adapter','06-compiled-adapter-controls']:
        assert json.loads((ROOT/'reports'/name/'result.json').read_text())['passed'] is True
    assert json.loads((ROOT/'reports/07-control-harness-compile/result.json').read_text())['returncode']==0
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
        for name in ['result.json','failure.traceback.txt']:
            path=folder/name
            if path.is_file():copy(path,'review/'+folder.name+'/'+name)
    doc='''# Lookup UI adapter and compiled faults: inactive integration checkpoint

The actual shared-host lookup adapter now passes all 371 original/JVM inputs with zero mismatches, zero unsupported executions and all 371 independently expected identity/trace/exception observations. Original coverage is 26/26 instructions and 4/4 conditional edges, including two uncredited getter methods. The freshly extracted fixture contains 1,244 registered bodies plus five dependencies: 1,249 methods in 607 classes. Rebuilding the prior selection from this fixture reproduces all prior 1,246-method fixture bytes exactly.

All ten actual compiled Java lookup faults were rejected by the same UI adapter with the measured counts `[127, 3, 2, 3, 233, 1, 369, 233, 25, 6]`. Every original observation and original coverage row remained identical; the positive report was restored byte for byte. Preparing all 101 jobs confirmed that the first 91 complete ordered job dictionaries, including mutant source text and labels, were unchanged. The existing 91 jobs were prepared only in this study; their complete execution was not repeated.

The lookup helper retains the proved executable body. The shared host types preserve their existing fields, constructors and non-final nested-class flags, adding only two getters. Consequently the fresh lookup helper class is 991 bytes, SHA-256 `df4383e951f3e897f58adc33f27847198f52cd455ccc5a9b22eb70712f66e082`; its nested-type metadata differs from the older standalone helper. The numeric helper class remains byte exact at `2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211`.

The exception observer omits generated message text only for seven explicitly identified VM-null cases; all raw diagnostics are retained. Injected messages and exception object identity compare exactly, including the deliberately replaced NPE with an identical message. The five record-tampering checks retain zero application-execution/coverage credit.

## Preserved attempts and limits

The first source derivation failed an exact whitespace anchor guard; that partial private tree and complete driver/error are preserved. The first fixture-subset checker retained its old numeric count and correctly failed despite writing evidence of byte-exact restoration. The corrected private checker then passed 1,246-to-1,249 selection. Neither historical failure has been relabeled.

The new `DayLookupControlHarness` compiled successfully with no diagnostics. Its DEX/three-path execution is pending. This checkpoint contains 18 of the 21 approved source paths. The new DEX runner, focused guard tests and complete acceptance wiring are still being authored. In particular, `ui_negative_control.py` has 101 prepared jobs but its full acceptance entry still carries the inherited 91-control count until the later coherent wiring. This is an inactive work-in-progress capsule, not a ready source promotion.

There is no new signed APK, no signed primary-body equality, no full UI suite, no complete 101-control execution, no ART run and no active application change in this checkpoint. The declared typed-list UTF-16 inputs exercise the pinned host String behavior; they do not claim exhaustive Unicode, malformed erased-list behavior, scheduling or persistence parity.

The immutable numeric19 baseline is `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f`. A separate parent-owned successor is changing only numeric command-evidence timing/filesystem handling. It was not absorbed here. The included dependency-only patch and all before hashes allow an explicit guarded merge later.
'''
    (TARGET/'CHECKPOINT_SCOPE.md').write_text(doc)
    assert all(identity(path)=={k:row[k] for k in ['bytes','sha256','mode']} for (path,_),row in zip(evidence,rows))
    files=[{'path':p.relative_to(TARGET).as_posix(),**identity(p)} for p in sorted(TARGET.rglob('*')) if p.is_file()]
    cp={'schema':1,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'INACTIVE_LOOKUP_ADAPTER_AND_TEN_JAVA_FAULTS_PROVED_SIGNED_GATE_PENDING',
        'repo_target':'work-in-progress/day-trigger-lookup/06-original-jvm-adapter-controls','files':files,
        'numeric_baseline_checkpoint_sha256':prep['numeric_checkpoint_sha256'],'parent_authoring_checkpoint_sha256':'af40191de75889def9c938e631d4b085f0905cb43781d0a1d0e21259f6e02bb8',
        'source_path_count':18,'approved_source_path_limit':21,'evidence_files':len(rows),'evidence_archive':identity(archive),
        'original_jvm_cases':371,'compiled_java_faults':10,'unchanged_prepared_job_prefix':91,'active_source_changed':False,
        'signed_primary_verified':False,'full_101_java_controls_executed':False,'androidRuntime':False}
    save(TARGET/'checkpoint.json',cp)
    print(json.dumps({'checkpoint':str(TARGET/'checkpoint.json'),**identity(TARGET/'checkpoint.json'),'source_paths':18,
                      'files':len(files),'evidence_members':len(rows),'archive':identity(archive),'owned_bytes':sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())},indent=2))

if __name__=='__main__':main()
