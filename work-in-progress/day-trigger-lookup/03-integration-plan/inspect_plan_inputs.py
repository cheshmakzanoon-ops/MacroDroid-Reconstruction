#!/usr/bin/env python3
"""Read frozen sources and derive a bounded integration plan; execute no app code."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tarfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path('/workspace/scratch/4130730d15aa')
NUMERIC = WORKSPACE / 'day-trigger-integration/checkpoints/04-source-acceptance-integration'
LOOKUP = WORKSPACE / 'day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls'
ACTIVE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
NUMERIC_CP = 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
LOOKUP_CP = '6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29'
LOOKUP_KEY = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;'
LOOKUP_METHOD_SHA = 'afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e'

PATHS = [
    ('source/java/recovered/ui/DayTriggerLookupMethods.java', 'new', 'Copy the proved executable helper; document and rebind any draft-comment-only edit.'),
    ('source/java-method-map.json', 'change', 'Append exactly the p0 recovery mapping, preserving every numeric baseline entry.'),
    ('source/ui-methods.json', 'change', 'Append the identical v9-ui mapping; retain exact family partition.'),
    ('test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java', 'change', 'Add getEntries/getKey only; preserve existing fields, constructors, flags and numeric aliases.'),
    ('tests/fixtures/original-dependencies.json', 'change', 'Append the two exact p0 getters, preserving the three r0 rows and disjoint consumer partitions.'),
    ('tests/fixtures/original-methods.dex', 'change', 'Re-extract the 1,244 registered bodies plus five uncredited getters from the pinned original APK.'),
    ('tests/fixtures/provenance.json', 'change', 'Bind the freshly extracted fixture, declarations and exact 1,244/5/1,249/607 counts.'),
    ('tests/java/DayLookupParityCases.java', 'new', 'Adapt all 371 exact inputs and independent identity/trace/exception observations into the UI harness.'),
    ('tests/java/DayLookupControlHarness.java', 'new', 'Provide the one-method signed/micro-DEX control runner with actual loaded-class and DEX provenance.'),
    ('tests/java/UiParityTests.java', 'change', 'Wire lookup reset, two dependency keys, identity outcome, exception observations, cases and coverage.'),
    ('tests/java/DayTriggerParityCases.java', 'change', 'Validate the combined declaration while returning only the unchanged three numeric dependencies.'),
    ('tests/fixtures/day-lookup-mutants.json', 'new', 'Retain the ten proved Java faults and required case labels with newly bound source/inventory hashes.'),
    ('day_lookup_dex_controls.py', 'new', 'Require the two actual lookup D8 faults, signed positive body/getter binding and exact restoration.'),
    ('day_numeric_dex_controls.py', 'change', 'Update only combined dependency validation/pin as required; preserve all numeric control semantics.'),
    ('ui_mutation_catalog.py', 'change', 'Append the ten lookup jobs after the unchanged first 91 jobs and bind the lookup inventory.'),
    ('ui_negative_control.py', 'change', 'Run all 101 Java faults, both numeric and both lookup DEX faults; retain exact positive restoration.'),
    ('tests/test_day_lookup.py', 'new', 'Add meaningful lookup catalog, consumer-partition, observer, coverage and provenance guard controls.'),
    ('tests/test_day_numeric.py', 'change', 'Update global inventory expectations while retaining exact three-getter numeric partition and all 35 controls.'),
    ('tests/test_build.py', 'change', 'Update full registry and fixture count/hash expectations.'),
    ('tests/test_v9.py', 'change', 'Require 12 UI methods in 11 classes; keep the unrelated 1,893 reference-file check unchanged.'),
    ('acceptance.py', 'change', 'Include the separate lookup DEX-control report in evidence; retain all 16 command gates and current bounds.'),
]
UNCHANGED = [
    'build.py', 'constructor_owner.py', 'test.py', 'release_integrity.py',
    'tests/java/BytecodeOracle.java', 'ui_runtime_policy.py',
    'tools/src/ExtractOracle.java', 'source/java/recovered/ui/DayTriggerValueMethods.java',
    'tests/java/DayNumericControlHarness.java', 'tests/fixtures/day-numeric-mutants.json',
]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def identity(path: Path) -> dict:
    s = path.stat()
    assert path.is_file() and not path.is_symlink(), str(path)
    return {'bytes': s.st_size, 'sha256': sha(path.read_bytes()), 'mode': stat.S_IMODE(s.st_mode)}

def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

def effective(path: str) -> Path:
    frozen = NUMERIC / 'project' / path
    return frozen if frozen.is_file() else ACTIVE / path

def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    out = ROOT / 'evidence'
    out.mkdir(exist_ok=False)
    assert sha((NUMERIC / 'checkpoint.json').read_bytes()) == NUMERIC_CP
    assert sha((LOOKUP / 'checkpoint.json').read_bytes()) == LOOKUP_CP
    numeric = json.loads((NUMERIC / 'checkpoint.json').read_text())
    lookup = json.loads((LOOKUP / 'checkpoint.json').read_text())
    observed = {}
    for base, rows in ((NUMERIC, numeric['files']), (LOOKUP, lookup['sourceFiles'])):
        for row in rows:
            path = base / row['path']
            value = identity(path)
            assert value['bytes'] == row['bytes'] and value['sha256'] == row['sha256'], str(path)
            observed[str(path)] = value
    assert len(numeric['source_changes']) == 19
    for row in numeric['source_changes']:
        path = NUMERIC / row['source']
        assert {k: identity(path)[k] for k in ('bytes', 'sha256')} == row['candidate']
    for base in (NUMERIC, LOOKUP):
        observed[str(base / 'checkpoint.json')] = identity(base / 'checkpoint.json')
    archive = LOOKUP / lookup['evidenceArchive']['path']
    assert {k: identity(archive)[k] for k in ('bytes', 'sha256')} == {k: lookup['evidenceArchive'][k] for k in ('bytes', 'sha256')}
    observed[str(archive)] = identity(archive)
    members = {row['path']: row for row in lookup['evidenceFiles']}
    with tarfile.open(archive, 'r:gz') as tf:
        name = 'positive/parity.json'
        raw = tf.extractfile(name).read()
        assert len(raw) == members[name]['bytes'] and sha(raw) == members[name]['sha256']
        proof = json.loads(raw)
    assert proof['passed'] is True and proof['cases'] == 371 and proof['executionPaths'] == 3
    assert proof['primaryMethod'] == LOOKUP_KEY
    assert proof['mismatchCount'] == proof['unsupportedCount'] == proof['independentExpectedFailures'] == 0
    derived_inputs = []
    remove = {'original', 'java', 'rebuilt', 'sameScopedOutcome', 'allPathsMatchIndependentExpected'}
    for row in proof['observations']:
        assert row['sameScopedOutcome'] is True and row['allPathsMatchIndependentExpected'] is True
        derived_inputs.append({key: value for key, value in row.items() if key not in remove})
    assert len(derived_inputs) == 371 and len({row['case'] for row in derived_inputs}) == 371
    save(out / 'lookup-ordered-inputs.json', derived_inputs)
    registry = json.loads(effective('source/java-method-map.json').read_text())
    ui = json.loads(effective('source/ui-methods.json').read_text())
    dependencies = json.loads(effective('tests/fixtures/original-dependencies.json').read_text())
    keys = {row['target'] + '->' + row['method'] for row in registry}
    assert len(keys) == len(registry) == 1243 and LOOKUP_KEY not in keys
    assert len(ui) == 11 and len({row['target'] for row in ui}) == 11
    numeric_key = next(row['target'] + '->' + row['method'] for row in registry if row['java_source'].endswith('DayTriggerValueMethods.java'))
    old_dependencies = dependencies['dependencies']
    assert len(old_dependencies) == 3 and all(row['consumer'] == numeric_key for row in old_dependencies)
    proposed = list(old_dependencies)
    for target, method, digest in (
        ('Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;', 'getEntries()Ljava/util/List;', 'f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e'),
        ('Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;', 'getKey()Ljava/lang/String;', '41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3'),
    ):
        proposed.append({'consumer': LOOKUP_KEY, 'target': target, 'method': method, 'original_method_sha256': digest})
    new_keys = keys | {LOOKUP_KEY}
    dep_keys = {row['target'] + '->' + row['method'] for row in proposed}
    assert len(dep_keys) == 5 and not new_keys & dep_keys
    selected = new_keys | dep_keys
    assert len(selected) == 1249 and len({key.split('->')[0] for key in selected}) == 607
    assert len({key.split('->')[0] for key in new_keys}) == 605
    plan = []
    assert len(PATHS) == 21 and len({row[0] for row in PATHS}) == 21
    for name, action, reason in PATHS:
        p = effective(name)
        if action == 'new':
            assert not p.exists(), str(p)
            baseline = None
        else:
            baseline = identity(p)
            observed[str(p)] = baseline
        plan.append({'path': name, 'proposal': action, 'reason': reason, 'baseline': baseline,
                     'baseline_source': str(p) if baseline else None, 'must_be_absent_if_new': baseline is None})
    unchanged = []
    for name in UNCHANGED:
        p = effective(name); value = identity(p); observed[str(p)] = value
        unchanged.append({'path': name, 'source': str(p), **value})
    saved = {}
    for name in ('java-all-path-parity.json', 'java-ui-three-path-parity.json'):
        p = ACTIVE / 'reports' / name; value = identity(p); observed[str(p)] = value
        saved[name] = {'input': str(p), 'identity': value, 'summary': {k: json.loads(p.read_text())[k] for k in ('passed', 'cases', 'methodsCovered')}}
    assert saved['java-all-path-parity.json']['summary'] == {'passed': True, 'cases': 193489, 'methodsCovered': 1242}
    assert saved['java-ui-three-path-parity.json']['summary'] == {'passed': True, 'cases': 23174, 'methodsCovered': 10}
    save(out / 'prospective-source-paths.json', plan)
    save(out / 'unchanged-production-inputs.json', unchanged)
    save(out / 'proposed-dependency-partitions.json', {'scope': 'Plan only; not an application fixture declaration.', 'rows': proposed})
    save(out / 'reviewed-inputs-before.json', observed)
    for path, value in observed.items():
        assert identity(Path(path)) == value, path
    save(out / 'reviewed-inputs-after.json', observed)
    for label, source in (('numeric-checkpoint.json', NUMERIC / 'checkpoint.json'), ('lookup-checkpoint.json', LOOKUP / 'checkpoint.json')):
        shutil.copy2(source, out / label)
    result = {
        'status': 'READ_ONLY_LOOKUP_INTEGRATION_PLAN_INPUTS_VERIFIED',
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(), 'elapsed_seconds': time.monotonic() - clock,
        'numeric_checkpoint_sha256': NUMERIC_CP, 'lookup_checkpoint_sha256': LOOKUP_CP,
        'verified_numeric_capsule_files': len(numeric['files']), 'verified_lookup_capsule_source_files': len(lookup['sourceFiles']),
        'reviewed_file_roles': len(observed), 'reviewed_files_unchanged': True,
        'read_archived_positive_member': {'path': 'positive/parity.json', 'bytes': len(raw), 'sha256': sha(raw)},
        'derived_input_inventory': identity(out / 'lookup-ordered-inputs.json'),
        'derivation': 'Retain the original order and all per-input fields; remove only original/java/rebuilt observations and two computed outcome booleans.',
        'actual_frozen_lookup_proof': {'cases': 371, 'paths': 3, 'new_execution_by_this_review': False,
                                     'original_instructions': 26, 'original_primary_instructions': 21, 'rebuilt_instructions': 23, 'rebuilt_primary_instructions': 18,
                                     'conditional_edges_each': 4, 'uncredited_getters': 2},
        'existing_active_reports': saved,
        'prospective_counts_only': {'registered_methods': 1244, 'recovered_target_classes': 605,
                                    'ui_methods': 12, 'ui_target_classes': 11, 'uncredited_getter_dependencies': 5,
                                    'fixture_methods': 1249, 'fixture_classes': 607,
                                    'ui_cases': 23174 + 1291 + 371, 'all_suite_cases': 193489 + 1291 + 371,
                                    'java_ui_controls': 101, 'numeric_dex_controls': 2, 'lookup_dex_controls': 2,
                                    'source_paths': len(PATHS), 'new_source_paths': sum(row[1] == 'new' for row in PATHS)},
        'application_source_written': False, 'app_execution': False, 'full_build': False,
        'new_android_execution': False, 'registration_or_apk_promoted': False,
    }
    save(out / 'result.json', result)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
