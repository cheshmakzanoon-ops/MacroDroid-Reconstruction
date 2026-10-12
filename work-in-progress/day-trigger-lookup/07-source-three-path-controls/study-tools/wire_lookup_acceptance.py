#!/usr/bin/env python3
"""Add lookup control ownership to the existing bounded UI acceptance entry."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import traceback

ROOT=Path(__file__).resolve().parent;PROJECT=ROOT/'stage-02/project'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def replace(text,old,new):
    assert text.count(old)==1,repr(old)
    return text.replace(old,new,1)

def main():
    out=ROOT/'reports/09-acceptance-wiring';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-author.py')
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat()};save(out/'result.json',result)
    try:
        path=PROJECT/'ui_negative_control.py'
        assert sha(path)=='c36d8e70ec459e169c82134c5252c02d410d796d053c41e125ef0d982fc721f8'
        shutil.copy2(path,out/path.name);text=path.read_text()
        text=replace(text,'import day_numeric_dex_controls\n','import day_numeric_dex_controls\nimport day_lookup_dex_controls\n')
        text=replace(text,'host/day_numeric_dex_controls.HELPER_CLASS,','host/day_numeric_dex_controls.HELPER_CLASS, host/day_lookup_dex_controls.HELPER_CLASS,')
        old="        raise RuntimeError('The current numeric method and uncredited dependency coverage are required')\n    reference_raw="
        new="""        raise RuntimeError('The current numeric method and uncredited dependency coverage are required')
    if (reference.get('dayLookupRecoveredMethods')!=1 or reference.get('dayLookupOriginalDependencyMethods')!=2
            or reference.get('dayLookupInputInventorySha256')!=ui_mutation_catalog.LOOKUP_INPUT_INVENTORY_SHA256
            or reference.get('dayLookupInstructionAndConditionalCoverage') is not True
            or reference.get('dayLookupOriginalDependencyKeys')!=sorted(day_lookup_dex_controls.GETTERS)
            or reference.get('dayLookupGeneratedNullMessageCases')!=sorted(day_lookup_dex_controls.VM_NULL_CASES)):
        raise RuntimeError('The current lookup method, exact exception scope and uncredited dependency coverage are required')
    day_lookup_dex_controls.validate_positive_coverage(reference.get('dayLookupOriginalCoverage',{}),26)
    day_lookup_dex_controls.validate_positive_coverage(reference.get('dayLookupRebuiltCoverage',{}),23)
    reference_raw="""
        text=replace(text,old,new)
        text=replace(text,"'expectedControlCount':91","'expectedControlCount':101")
        text=replace(text,"'dayNumericCatalogSha256':ui_mutation_catalog.DAY_CATALOG_SHA256}",
            "'dayNumericCatalogSha256':ui_mutation_catalog.DAY_CATALOG_SHA256,\n            'dayLookupCatalogSha256':ui_mutation_catalog.LOOKUP_CATALOG_SHA256}")
        text=replace(text,"'dayNumericInputInventorySha256','dayNumericOriginalCoverage']",
            "'dayNumericInputInventorySha256','dayNumericOriginalCoverage',\n               'dayLookupRecoveredMethods','dayLookupOriginalDependencyMethods','dayLookupOriginalDependencyKeys',\n               'dayLookupInputInventorySha256','dayLookupOriginalCoverage','dayLookupGeneratedNullMessageCases',\n               'dayLookupObserverRecordControls']")
        text=replace(text,"                raise RuntimeError('Day numeric mutation emitted another class')",
            "                raise RuntimeError('Day numeric mutation emitted another class')\n            if job.get('day_lookup') and sorted(p.relative_to(classes).as_posix() for p in classes.rglob('*') if p.is_file())!=[day_lookup_dex_controls.HELPER_CLASS]:\n                raise RuntimeError('Day lookup mutation emitted another class')")
        text=replace(text,"status='ALL_91_JAVA_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED'","status='ALL_101_JAVA_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED'")
        text=replace(text,"status='ALL_91_JAVA_AND_TWO_NUMERIC_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED')\n        result['pass']=all(row['pass'] for row in records) and len(records)==91 and numeric.get('passed') is True",
            "status='ALL_101_JAVA_AND_TWO_NUMERIC_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED')\n        save()\n        lookup=day_lookup_dex_controls.run_controls(build.ROOT,records)\n        result.update(dayLookupDexControlsPassed=lookup.get('passed') is True,\n                      dayLookupDexControlsSha256=sha(build.REPORTS/'day-lookup-dex-controls.json'),\n                      status='ALL_101_JAVA_AND_FOUR_DAY_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED')\n        result['pass']=all(row['pass'] for row in records) and len(records)==101 and numeric.get('passed') is True and lookup.get('passed') is True")
        path.write_text(text)
        path=PROJECT/'acceptance.py';assert path.read_bytes()==(ROOT/'stage-02/baseline/acceptance.py').read_bytes()
        shutil.copy2(path,out/path.name);text=path.read_text()
        text=replace(text,"'day-numeric-dex-controls.json']","'day-numeric-dex-controls.json','day-lookup-dex-controls.json']")
        path.write_text(text)
        result.update(passed=True,status='LOOKUP_ACCEPTANCE_WIRING_AUTHORED',
            paths={name:{'bytes':(PROJECT/name).stat().st_size,'sha256':sha(PROJECT/name)} for name in ['ui_negative_control.py','acceptance.py']},
            scope='Source wiring only; full 101 Java plus four DEX controls and signed-primary evidence have not been executed in this small overlay.')
    except BaseException as error:
        result.update(status='AUTHORING_FAILED_PRESERVED',error=repr(error));(out/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
