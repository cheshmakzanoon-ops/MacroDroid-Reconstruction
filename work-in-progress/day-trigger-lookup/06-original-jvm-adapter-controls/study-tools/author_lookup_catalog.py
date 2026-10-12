#!/usr/bin/env python3
"""Append the ten exact measured lookup faults after the unchanged numeric prefix."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import traceback

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'stage-02/project'
BASELINE = ROOT / 'stage-02/baseline'
PROOF = Path('/workspace/scratch/4130730d15aa/day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls')
HELPER = 'source/java/recovered/ui/DayTriggerLookupMethods.java'
METHOD = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;'
INPUT_SHA = '02dd119966191ad2f56937eda28e63644979080158465ffb13767710f34e32e6'

def sha(data): return hashlib.sha256(data).hexdigest()
def save(path, value): path.write_text(json.dumps(value, indent=2) + '\n')
def replace_once(text, old, new):
    assert text.count(old) == 1, repr(old)
    return text.replace(old, new, 1)

LOADER = '''


LOOKUP_CATALOG_PATH = "tests/fixtures/day-lookup-mutants.json"
LOOKUP_CATALOG_SHA256 = "@CATALOG_SHA@"
LOOKUP_HELPER_PATH = "@HELPER@"
LOOKUP_HELPER_SHA256 = "@HELPER_SHA@"
LOOKUP_METHOD = "@METHOD@"
LOOKUP_INPUT_INVENTORY_SHA256 = "@INPUT_SHA@"


def load_lookup_mutations(root: Path) -> list[dict]:
    """Append ten lookup faults; no existing Widget or numeric job is altered."""
    data, original = (root / LOOKUP_CATALOG_PATH).read_bytes(), (root / LOOKUP_HELPER_PATH).read_bytes()
    if hashlib.sha256(data).hexdigest() != LOOKUP_CATALOG_SHA256:
        raise RuntimeError("Day lookup mutation catalog differs from its frozen bytes")
    if hashlib.sha256(original).hexdigest() != LOOKUP_HELPER_SHA256:
        raise RuntimeError("Day lookup helper differs from its measured positive source")
    catalog = json.loads(data)
    if (set(catalog) != {"schema", "method", "helper_path", "helper_sha256", "input_inventory_sha256", "controls"}
            or type(catalog.get("schema")) is not int or catalog["schema"] != 1
            or catalog.get("method") != LOOKUP_METHOD or catalog.get("helper_path") != LOOKUP_HELPER_PATH
            or catalog.get("helper_sha256") != LOOKUP_HELPER_SHA256
            or catalog.get("input_inventory_sha256") != LOOKUP_INPUT_INVENTORY_SHA256):
        raise RuntimeError("Day lookup catalog identifies another method or case inventory")
    controls = catalog.get("controls")
    if not isinstance(controls, list) or len(controls) != 10:
        raise RuntimeError("Exactly ten Day lookup mutations are required")
    jobs, names = [], set()
    for control in controls:
        if (not isinstance(control, dict)
                or set(control) != {"name", "reason", "edits", "expected_failure_labels"}
                or not isinstance(control["name"], str)
                or re.fullmatch(r"[a-z][a-z0-9-]+", control["name"]) is None
                or control["name"] in names or not isinstance(control["reason"], str) or not control["reason"]):
            raise RuntimeError("Invalid or duplicate Day lookup mutation name")
        names.add(control["name"])
        required = control["expected_failure_labels"]
        if (not isinstance(required, list) or not required or len(set(required)) != len(required)
                or any(not isinstance(label, str) or not label.startswith("day-lookup:") for label in required)):
            raise RuntimeError("Day lookup mutation must name its required observed failure")
        jobs.append({"name": "day-lookup-" + control["name"], "classname": "DayTriggerLookupMethods",
                     "source": root / LOOKUP_HELPER_PATH, "mutant": apply_edits(original.decode(), control["edits"]),
                     "required_cases": list(required), "catalog_sha256": LOOKUP_CATALOG_SHA256,
                     "reason": control["reason"], "widget": False, "day_lookup": True})
    return jobs
'''

def main():
    out = ROOT / 'reports/05-catalog-authoring'; out.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, out / 'executed-author.py')
    result = {'status':'RUNNING', 'started_utc':datetime.now(timezone.utc).isoformat(), 'passed':False}
    save(out / 'result.json',result)
    try:
        names = ('ui_mutation_catalog.py','ui_negative_control.py','tests/test_day_numeric.py','tests/test_build.py','tests/test_v9.py')
        for name in names:
            assert (PROJECT/name).read_bytes() == (BASELINE/name).read_bytes(), 'Baseline guard: '+name
            copy = out / 'before' / name; copy.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(PROJECT/name,copy)
        new = PROJECT / 'tests/fixtures/day-lookup-mutants.json'; assert not new.exists()
        with tarfile.open(PROOF/'evidence.tar.gz') as archive:
            raw = archive.extractfile('fault-catalog.json').read()
        assert len(raw)==3953 and sha(raw)=='bed429865bcc334bbd969ef9520ebfc64b46cc04a7ababd5253c08139d613140'
        (out/'original-fault-catalog.json').write_bytes(raw)
        old = json.loads(raw); assert len(old)==10
        helper = (PROJECT/HELPER).read_bytes()
        assert sha(helper)=='020256ed2d78740183aa9ac8d92e8c775db0d4fc647dfc12f1bea0a6881243e5'
        reasons = {
            'case-sensitive':'Case-insensitive matching must retain the first entry object.',
            'reverse-receiver':'The query is the receiver; null entry keys are accepted as nonmatches.',
            'skip-null-entry':'A null entry must throw when reached, after the exact iterator calls.',
            'null-query-early-return':'A null query still traverses an empty list and throws only when a key is compared.',
            'last-match':'A match returns immediately without reading a later entry.',
            'trim-query':'Query whitespace is significant.',
            'indexed-loop':'The original traverses through Iterator, with observable iterator failures and ordering.',
            'extra-iteration-after-match':'Returning a match must not perform another hasNext operation.',
            'swallow-iterator-fault':'Iterator exceptions escape with their original message and identity.',
            'replace-injected-npe-identity':'An injected NPE must escape as the same object, even if a replacement has the same message.',
        }
        controls = []
        for row in old:
            assert set(row)=={'name','old','new','requiredFailingCase'} and helper.decode().count(row['old'])==1
            controls.append({'name':row['name'],'reason':reasons[row['name']],
                             'edits':[{'find':row['old'],'replace':row['new'],'count':1}],
                             'expected_failure_labels':['day-lookup:'+row['requiredFailingCase']]})
        value = {'schema':1,'method':METHOD,'helper_path':HELPER,'helper_sha256':sha(helper),
                 'input_inventory_sha256':INPUT_SHA,'controls':controls}
        save(new,value)
        loader = LOADER
        for token,content in {'CATALOG_SHA':sha(new.read_bytes()),'HELPER':HELPER,'HELPER_SHA':sha(helper),'METHOD':METHOD,'INPUT_SHA':INPUT_SHA}.items():
            loader = loader.replace('@'+token+'@',content)
        path=PROJECT/'ui_mutation_catalog.py'; before=path.read_text(); path.write_text(before+loader)
        path=PROJECT/'ui_negative_control.py'; text=path.read_text()
        old_tail="        raise RuntimeError('All 78 existing controls and thirteen Day numeric controls are required')\n    return jobs"
        text=replace_once(text,old_tail,"        raise RuntimeError('All 78 existing controls and thirteen Day numeric controls are required')\n    jobs.extend(ui_mutation_catalog.load_lookup_mutations(build.ROOT))\n    if len(jobs)!=101 or len({job['name'] for job in jobs})!=101:\n        raise RuntimeError('All 91 existing controls and ten Day lookup controls are required')\n    return jobs")
        path.write_text(text)
        path=PROJECT/'tests/test_day_numeric.py'; text=path.read_text()
        text=replace_once(text,'self.assertEqual(len(registry), 1243)','self.assertEqual(len(registry), 1244)')
        text=replace_once(text,'self.assertEqual(len(keys | dependencies), 1246)','self.assertEqual(len(keys | dependencies), 1247)')
        text=replace_once(text,"{'registered': 1243, 'dependencies': 3, 'selected': 1246, 'classes': 607}","{'registered': 1244, 'dependencies': 5, 'selected': 1249, 'classes': 607}")
        path.write_text(text)
        path=PROJECT/'tests/test_build.py'; text=path.read_text()
        for old_count,new_count in [('len(self.registry),1243','len(self.registry),1244'),("p['methods'],1246","p['methods'],1249"),("p['registered_methods'],1243","p['registered_methods'],1244"),("p['dependency_methods'],3","p['dependency_methods'],5")]:
            text=replace_once(text,old_count,new_count)
        path.write_text(text)
        path=PROJECT/'tests/test_v9.py'; text=path.read_text()
        text=replace_once(text,'def test_exact_eleven_methods_and_classes(self):','def test_exact_twelve_methods_and_eleven_classes(self):')
        text=replace_once(text,"len({e['target'] for e in self.entries})),(11,11))","len({e['target'] for e in self.entries})),(12,11))")
        path.write_text(text)
        paths=[*names,'tests/fixtures/day-lookup-mutants.json']
        result.update(passed=True,status='LOOKUP_CATALOG_AND_COUNT_SOURCE_AUTHORED',
                      existing_loader_prefix_byte_exact=(PROJECT/'ui_mutation_catalog.py').read_bytes().startswith((BASELINE/'ui_mutation_catalog.py').read_bytes()),
                      paths={name:{'bytes':(PROJECT/name).stat().st_size,'sha256':sha((PROJECT/name).read_bytes())} for name in paths},
                      scope='Source derivation only. Prepared 91-prefix and actual mutation execution are separate following checks; full acceptance wiring remains pending.')
    except BaseException as error:
        result.update(status='AUTHORING_FAILED_PRESERVED',error=repr(error)); (out/'failure.traceback.txt').write_text(traceback.format_exc()); raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat(); save(out/'result.json',result)
        print(json.dumps(result,indent=2))

if __name__=='__main__': main()
