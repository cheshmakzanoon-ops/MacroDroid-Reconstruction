#!/usr/bin/env python3
"""Freeze the two actually observed Settings controls and the next finite plan."""
from datetime import datetime, timezone
import copy
import hashlib
import json
from pathlib import Path
import shutil
import stat
import sys
import xml.etree.ElementTree as ET

BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
OUT = BASE / 'design-01'
PARENT = Path('/dev/shm/macrodroid-exact-alarm-navigation/source-01/repository')
CLOSED = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/05-fourteen-screen-device-analysis')
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189/extracted/journey')
TARGET = 'work-in-progress/exact-alarm-enable-return/01-observed-design'
SETTINGS = 'com.android.settings'
COMPONENT = 'com.android.settings/com.android.settings.spa.SpaActivity'
TOGGLE = {'text': 'Allow setting alarms and reminders'}
UP = {'content-desc': 'Navigate up'}
ON = 'after-exact-alarm-enable'
RETURNED = 'after-exact-alarm-return'
NUMERIC_APK = {'bytes': 94683136, 'sha256': '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'}


def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    final = path.lstat()
    assert (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) == (
        final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns)
    return {'bytes': final.st_size, 'sha256': digest}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    assert identity(CLOSED / 'checkpoint.json')['sha256'] == '57a5a23f61ae4c115db2a629c8bad8359d6f20d76612f3bd63265e8e8a2af149'
    parent_files = sorted(path for path in PARENT.rglob('*') if path.is_file())
    assert len(parent_files) == 98
    before = {str(path): identity(path) for path in parent_files}
    inputs = [CLOSED / name for name in ('checkpoint.json', 'observed-settings-controls.json',
        'analysis/independent-exact-alarm-analysis.json', 'analysis/literal-captured-comparison-replay.json',
        'analysis/observed-terminal-surfaces.json')]
    before.update({str(path): identity(path) for path in inputs})
    result = json.loads(inputs[2].read_bytes())
    assert result['analysis_passed'] is True and result['literal_evidence_valid'] is True
    assert result['diagnostic_rgba_pixel_vector'] == [0, 35] + [0] * 12
    controls = json.loads(inputs[1].read_bytes())
    assert controls['full_original_png_viewed_by_root'] is True
    terminals = json.loads(inputs[4].read_bytes())
    assert [item['label'] for item in terminals] == ['original', 'candidate']
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(PARENT / 'tools/parity_journeys'))
    import editor_journey as runner
    import exact_alarm_journey as alarm
    original_plan = alarm.expected_plan()
    assert runner.fingerprint(original_plan) == '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'
    plan = copy.deepcopy(original_plan)
    plan[-1][2] = copy.deepcopy(TOGGLE)
    plan.extend([[ON, SETTINGS, copy.deepcopy(UP), copy.deepcopy(TOGGLE)],
                 [RETURNED, runner.PACKAGE, None, copy.deepcopy(UP)]])
    assert plan[:13] == original_plan[:13] and len(plan) == 16
    assert sum(item[3] is not None for item in plan) == 15
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-collector.py')
    fixture_rows = []
    for terminal in terminals:
        for role, reference in terminal['shot']['artifacts'].items():
            source = RAW / reference['path']
            expected = {'bytes': reference['bytes'], 'sha256': reference['sha256']}
            assert identity(source) == expected
            before[str(source)] = expected
            target = OUT / 'observed-fixtures' / reference['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            assert identity(target) == expected
            fixture_rows.append({'label': terminal['label'], 'role': role,
                                 'path': target.relative_to(OUT).as_posix(), **expected})
    shot = terminals[0]['shot']
    data = (RAW / shot['artifacts']['hierarchy']['path']).read_bytes()
    assert data == (RAW / terminals[1]['shot']['artifacts']['hierarchy']['path']).read_bytes()
    off = ET.fromstring(data)
    parent_map = {child: parent for parent in off.iter() for child in parent}
    label = runner.select(off, SETTINGS, TOGGLE)
    parent = parent_map[label]
    assert parent.attrib == controls['toggle']['clickable_ancestor']
    assert parent.get('checkable') == 'true' and parent.get('checked') == 'false'
    assert runner.target(data, SETTINGS, TOGGLE, 720, 1280) == [360, 771]
    assert runner.target(data, SETTINGS, UP, 720, 1280) == [56, 104]
    on = copy.deepcopy(off)
    on_map = {child: parent for parent in on.iter() for child in parent}
    on_label = runner.select(on, SETTINGS, TOGGLE)
    on_map[on_label].set('checked', 'true')
    contract = {
        'schema': 1, 'source_run': 38240023189, 'source_artifact': 11742624179,
        'source_head': '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
        'source_candidate_apk_sha256': '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
        'owner': SETTINGS, 'component': COMPONENT, 'full_image_size': [720, 1280],
        'hierarchy_attributes': off.attrib,
        'off_hierarchy_canonical': runner.canonical(off),
        'off_hierarchy_canonical_sha256': runner.fingerprint(runner.canonical(off)),
        'predicted_on_hierarchy_canonical': runner.canonical(on),
        'predicted_on_hierarchy_canonical_sha256': runner.fingerprint(runner.canonical(on)),
        'on_hierarchy_observed': False,
        'on_prediction_derivation': 'Only the uniquely identified clickable alarm row checked attribute changes from false to true.',
        'toggle': controls['toggle'], 'navigate_up': controls['navigate_up'],
        'toggle_parent_center': [360, 771], 'navigate_up_parent_center': [56, 104],
        'observed_fixtures': fixture_rows,
        'require_initial_off_before_toggle': True,
        'require_observed_on_before_navigate_up': True,
        'permission_api_result_observed': False,
    }
    write(OUT / 'settings-contract.json', contract)
    write(OUT / 'sixteen-screen-plan.json', plan)
    design = {
        'schema': 1, 'status': 'OBSERVED_CONTROLS_AND_FINITE_PLAN_NO_NEW_ANDROID_EXECUTION',
        'parent_plan_sha256': runner.fingerprint(original_plan), 'plan_sha256': runner.fingerprint(plan),
        'report_schema': 7, 'screens_per_run': 16, 'inputs_per_run': 15,
        'new_inputs_per_run': 2, 'settings_inputs_per_run': 2, 'total_settings_inputs': 4,
        'global_inputs': 30, 'global_setup_mutations': 6,
        'new_state_order': ['observed Settings off', 'observed Settings on after one toggle', 'observed app surface after Navigate up'],
        'contract_identity': identity(OUT / 'settings-contract.json'),
        'expected_new_runtime_candidate': NUMERIC_APK,
        'runtime_candidate_manifest_commit': None,
        'candidate_manifest_must_be_fetched_and_hash_pinned_before_workflow_activation': True,
        'original_apk': {'bytes': 95725918, 'sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'},
        'new_settings_controls_were_observed_in_both_previous_apks': True,
        'permission_api_result_observed': False, 'trigger_configuration_confirmed': False,
        'macros_saved': False, 'macros_executed': False, 'new_android_actions': [],
        'active_source_or_workflow_changes': [],
        'proposed_new_sources': ['tools/parity_journeys/exact_alarm_enable_return.py',
            'tools/parity_journeys/exact_alarm_enable_return_readiness.py',
            'tools/parity_journeys/test_exact_alarm_enable_return.py',
            'tools/parity_journeys/test_exact_alarm_enable_return_readiness.py'],
        'proposed_existing_source_changes': ['tools/parity_journeys/editor_journey.py',
            'tools/parity_journeys/observed_journey.py'],
        'reused_source_behavior': ['all historical plan identities and policies',
            'literal thirteen-input fourteen-screen prefix', 'full-frame settling and first eligible readiness sequence',
            'exclusive recorded stream and command chronology checks', 'installed APK and main app PID continuity',
            'full cross-APK RGBA and hierarchy comparison without masks or tolerances'],
        'new_settings_capture_roles': ['after-exact-alarm-ok', 'after-exact-alarm-enable-before',
            'after-exact-alarm-enable', 'after-exact-alarm-return-before'],
        'unexpected_surface_behavior': 'Stop that app run and preserve partial captures; never infer or add another action.',
        'application_return_component_class_assumed': False,
        'post_return_owner': runner.PACKAGE,
        'test_plan': ['reject changed or misplaced schema7 plan/policy and foreign historical reuse',
            'reject changed full off Settings hierarchy/owner/component/PNG geometry or target ancestry',
            'require exactly one actual checked-on state after the toggle before Navigate up',
            'reject invented Settings role names, mixed capture stems and foreign owner outside four declared roles',
            'bind thirty total inputs and six setup mutations in global order with no unbound mutation',
            'reject changed coordinates, stale preconditions, PID/component replacement or raw byte mismatch',
            'retain all209 historical host controls unchanged',
            'replay the closed fourteen-screen device artifact with identical historical comparison'],
        'resource_budget_bytes': 536870912,
    }
    write(OUT / 'design.json', design)
    after = {path: identity(Path(path)) for path in before}
    assert before == after
    write(OUT / 'input-identities.json', {'inputs': before, 'all_unchanged_after': True})
    (OUT / 'README.md').write_text(f'''# Enable exact alarms and observe the return to MacroDroid

The next proposed journey has **16 screens and 15 inputs per APK**, plan `{design['plan_sha256']}`, using a distinct schema7. It extends the independently replayed fourteen-screen result from run38240023189. The first thirteen complete plan entries are unchanged; the fourteenth Settings screen now requires the observed alarm row before the next action.

## Controls actually observed

Both prior APKs show the same full Settings page in `{COMPONENT}`, identifying MacroDroid5.67.8. The enabled, clickable alarm row is checkable and unchecked. Its observed label is **Allow setting alarms and reminders**, and its clickable parent center is **(360,771)**. The observed **Navigate up** node has clickable parent center **(56,104)**. Both complete PNGs, XMLs, PID records and foreground observations are preserved with exact hashes. Root viewed the complete original PNG and read both hierarchies before defining these actions.

The runner must first acquire a fresh complete Settings observation and immediate PID/component guard. It can tap the uniquely identified unchecked row once. It must then retain a complete checked-on Settings observation before it can acquire another fresh full preinput observation and tap Navigate up. The final app surface is observation-only, with package ownership checked and no assumed activity class or next control.

`settings-contract.json` contains the complete actually observed off hierarchy. The proposed on hierarchy is a **prediction**, derived by changing only that unique row's checked attribute to true; it is explicitly not an observed result. If the actual page differs from that finite expected state, the run stops and retains the difference before any further input. The full frame is always compared between APKs, without masks, tolerances or selecting frames by cross-APK similarity.

## Evidence and command boundaries

The new adapter is scoped to the exact sixteen-entry plan and schema7. The existing fourteen-screen, thirteen-screen and older adapters and policies retain their original meanings. Settings ownership is permitted only in the four declared full-capture roles: the off screen, its pre-toggle observation, the on screen and its pre-return observation. Each of the six snapshot files must belong to the same actual label/acquisition/frame stem. Main app PID continuity, Settings component identity, exact ancestor geometry, immediate input age and complete capture chronology remain required.

The global command ledger must contain exactly **30 planned inputs**, **six install/launch setup mutations**, and **four Settings inputs** across the two ordered runs. Both new actions are visible-control taps derived again from the fresh XML, using the existing command grammar; no direct Settings/app-op mutation or programmatic permission grant is proposed. A failure cannot add, retry or reorder an action. Partial evidence is retained.

The resulting report can establish that Settings displayed the enabled state and that navigation returned to the app. It cannot by itself establish an observed AlarmManager API return value, a configured trigger or a saved/executed macro. Those remain later functional work.

## Candidate and implementation status

The next functional run is intended to use the newly host-accepted numeric candidate `{NUMERIC_APK['sha256']}` ({NUMERIC_APK['bytes']:,} bytes), with the same pinned original APK. Its immutable downloader manifest and fetched source commit are pending and must be concrete before workflow activation. The separate fixed indicator experiment keeps its earlier fixed APK pair.

This checkpoint only derives the exact plan and observed control contract, verifies the98 parent source files and closed device inputs unchanged, and preserves the two terminal observations. **No new adapter, tests, workflow, app source edit, permission input, or Android execution is claimed here.** The predicted on state has not been observed. Implementation will add two adapter modules and their tests, make narrow dispatch changes in the two existing journey modules, run all209 inherited host controls plus new boundary controls, and replay the closed fourteen-screen artifact before any new workflow activation.
''')
    rows = [{'path': path.relative_to(OUT).as_posix(), **identity(path), 'mode': '100644'}
            for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': design['status'], 'repo_target': TARGET, 'active_files': [],
        'new_android_actions': [], 'files': rows, 'file_count': len(rows),
        'payload_bytes': sum(row['bytes'] for row in rows), 'plan_sha256': design['plan_sha256']}
    write(OUT / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
        'files': len(rows), 'payload_bytes': checkpoint['payload_bytes'], 'plan_sha256': design['plan_sha256'],
        'contract': identity(OUT / 'settings-contract.json')}, indent=2))


if __name__ == '__main__':
    main()
