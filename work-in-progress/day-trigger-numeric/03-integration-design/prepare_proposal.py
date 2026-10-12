#!/usr/bin/env python3
"""Pin a small integration design against the exact active 1,242-method inputs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent / 'MacroDroid-Reconstruction/project'
OUT = BASE / 'proposal-01'
SNAPSHOT = 'b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
PATHS = {
    'source/java/recovered/ui/DayTriggerValueMethods.java': 'Add only the reviewed r0 helper body.',
    'source/java-method-map.json': 'Register exactly one new method; retain every existing entry.',
    'source/ui-methods.json': 'Add the same r0 entry to the UI suite partition.',
    'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java': 'Retain existing constructors, public fields and equality; add private transient field aliases and exact getters.',
    'tests/java/DayTriggerParityCases.java': 'Add the exact 1291-case inventory, independent integer-bit expectations, scoped raw exception evidence and separate dependency coverage.',
    'tests/java/DayNumericControlHarness.java': 'Use the same cases in a small class/fixture/APK-bound control harness for actual rebuilt-Dex faults.',
    'tests/java/UiParityTests.java': 'Load the three original dependencies separately, execute Day cases, and require exact primary/dependency coverage without adding dependency method credit.',
    'tools/src/ExtractOracle.java': 'Include only declared original fixture dependencies in addition to registered methods, with duplicate/overlap/registration guards.',
    'tests/fixtures/original-dependencies.json': 'Declare exactly the three original field getters and their Day r0 consumer.',
    'tests/fixtures/original-methods.dex': 'Regenerate the test-only fixture directly from the pinned original APK.',
    'tests/fixtures/provenance.json': 'Record registered methods, dependency methods and actual fixture total/classes separately.',
    'tests/fixtures/day-numeric-mutants.json': 'Pin all thirteen reviewed source faults, required case labels and positive helper identity.',
    'ui_mutation_catalog.py': 'Add a separate exact Day catalog loader; retain all Widget catalog behavior.',
    'ui_negative_control.py': 'Retain all78 controls and add thirteen Day Java faults plus a separately recorded actual-Dex control stage.',
    'day_numeric_dex_controls.py': 'Rebuild two small actual D8/transplant faults with production helpers, check independent paths/provenance/restoration, and preserve a dedicated report.',
    'acceptance.py': 'Bind the dedicated Day Dex-control report in fresh evidence after the existing UI-control gate.',
    'tests/test_day_numeric.py': 'Add focused dependency, source-identity, catalog/required-case and count-separation rejection controls.',
    'tests/test_build.py': 'Update only the recovered-method count and explicit fixture/dependency provenance assertions.',
    'tests/test_v9.py': 'Update the exact UI method count to11 while retaining all other controls.',
}
KEEP = ['tests/java/BytecodeOracle.java', 'build.py', 'constructor_owner.py', 'test.py',
        'tests/fixtures/widget-method-mutants.json', 'tests/test_ui_mutation_catalog.py']


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    snapshot = json.loads((PROJECT / 'reports/release-input-snapshot.json').read_text())
    assert snapshot['snapshot_sha256'] == SNAPSHOT and snapshot['files'] == 81291
    canonical = json.dumps(snapshot['entries'], sort_keys=True, separators=(',', ':')).encode()
    assert hashlib.sha256(canonical).hexdigest() == SNAPSHOT
    registry = json.loads((PROJECT / 'source/java-method-map.json').read_text())
    assert len(registry) == 1242 and len({r['target'] for r in registry}) == 605
    rows = []
    for relative, purpose in PATHS.items():
        path = PROJECT / relative
        if path.exists():
            observed = identity(path)
            pin = snapshot['entries'][relative]
            assert observed == {'bytes': pin['size'], 'sha256': pin['sha256']}
        else:
            assert relative not in snapshot['entries']
            observed = None
        rows.append({'path': relative, 'baseline': observed, 'must_be_absent_if_new': observed is None, 'proposed_change': purpose})
    keep = []
    for relative in KEEP:
        path = PROJECT / relative
        observed = identity(path)
        pin = snapshot['entries'][relative]
        assert observed == {'bytes': pin['size'], 'sha256': pin['sha256']}
        keep.append({'path': relative, **observed})
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'prepare_proposal.py').write_bytes(Path(__file__).read_bytes())
    proposal = {'schema': 1, 'status': 'INACTIVE_INTEGRATION_DESIGN_NO_COMPILATION',
                'created_utc': datetime.now(timezone.utc).isoformat(),
                'active_app_source_commit': 'dbcad968c5c3e8f084205393a6c0d2d06a203c71',
                'active_input_files': 81291, 'active_snapshot_sha256': SNAPSHOT,
                'review_checkpoint_sha256': '30567165fc992e16e52ef0ba90636d13c17f7560b70c00b4fe1478cf00fbbf4f',
                'proposed_paths': rows, 'required_unchanged_inputs': keep,
                'expected_registered_methods': 1243, 'expected_registered_classes': 605,
                'expected_ui_recovered_methods': 11, 'original_fixture_dependency_methods': 3,
                'expected_total_fixture_methods': 1246, 'expected_fixture_classes': 607,
                'new_numeric_cases': 1291, 'expected_total_cases': 194780,
                'expected_ui_cases': 24465, 'existing_java_fault_controls_retained': 78,
                'new_java_fault_controls': 13, 'new_actual_rebuilt_dex_faults': 2,
                'full_source_copy_created': False, 'app_build_started': False, 'active_paths_edited': []}
    (OUT / 'proposal.json').write_text(json.dumps(proposal, indent=2) + '\n')
    print(json.dumps({'path': str(OUT / 'proposal.json'), **identity(OUT / 'proposal.json'),
                      'proposed_paths': len(rows), 'unchanged_inputs': len(keep)}, indent=2))


if __name__ == '__main__':
    main()
