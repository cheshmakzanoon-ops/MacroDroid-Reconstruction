#!/usr/bin/env python3
"""Freeze observed dialog inputs and the proposed one-tap fourteen-screen scope."""
import copy
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
OUT = ROOT / 'checkpoints/01-observed-input-and-design'
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388/extracted/journey')
SOURCE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
PARENT = Path('/dev/shm/macrodroid-notification-readiness/stage-02/repository/tools/parity_journeys')
PACKAGE = 'com.arlosoft.macrodroid'
SETTINGS = 'com.android.settings'
PREFIX = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'
OK = {'resource-id': 'android:id/button1', 'text': 'OK'}


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def canonical(root):
    return (root.tag, tuple(sorted(root.attrib.items())), root.text if root.text and root.text.strip() else '', root.tail if root.tail and root.tail.strip() else '', tuple(canonical(n) for n in root))


def write(name, value):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    report = json.loads((RAW / 'journey.json').read_bytes())
    assert report['schema'] == 5 and fingerprint(report['plan']) == report['plan_sha256'] == PREFIX
    assert [r['status'] for r in report['runs']] == ['COMPLETE', 'COMPLETE']
    assert [len(r['screens']) for r in report['runs']] == [13, 13]
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'prepare-design.py')
    literal = []
    for run in report['runs']:
        shot = run['screens'][-1]
        assert shot['name'] == 'after-day-time-trigger' and shot['owner'] == PACKAGE
        for role, ref in shot['artifacts'].items():
            assert identity(RAW / ref['path']) == {k: ref[k] for k in ('bytes', 'sha256')}
            dst = OUT / 'observed' / ref['path']
            dst.parent.mkdir(exist_ok=True)
            shutil.copy2(RAW / ref['path'], dst)
        tree = ET.fromstring((RAW / shot['artifacts']['hierarchy']['path']).read_bytes())
        parents = {c: p for p in tree.iter() for c in p}
        nodes = {key: [n for n in tree.iter('node') if n.get('resource-id') == key] for key in ['android:id/button1', 'android:id/button2', 'android:id/message', PACKAGE + ':id/alertTitle', PACKAGE + ':id/parentPanel']}
        assert all(len(v) == 1 for v in nodes.values())
        positive = nodes['android:id/button1'][0]
        assert all(positive.get(k) == v for k, v in {'text': 'OK', 'class': 'android.widget.Button', 'package': PACKAGE, 'clickable': 'true', 'enabled': 'true', 'bounds': '[496,761][624,857]'}.items())
        panel = nodes[PACKAGE + ':id/parentPanel'][0]
        chain, cursor = [], positive
        while cursor in parents:
            chain.append(dict(cursor.attrib))
            cursor = parents[cursor]
        literal.append({'label': run['label'], 'shot': shot, 'positive': dict(positive.attrib), 'positive_ancestor_chain': chain, 'title': dict(nodes[PACKAGE + ':id/alertTitle'][0].attrib), 'message': dict(nodes['android:id/message'][0].attrib), 'cancel': dict(nodes['android:id/button2'][0].attrib), 'canonical_panel': canonical(panel), 'canonical_panel_sha256': fingerprint(canonical(panel)), 'observed_center': [560, 809], 'subsequent_transition_count': 0})
    assert literal[0]['canonical_panel_sha256'] == literal[1]['canonical_panel_sha256']
    plan = copy.deepcopy(report['plan'])
    assert len(plan) == 13 and plan[-1][2] is None
    plan[-1][2] = OK
    plan.append(['after-exact-alarm-ok', SETTINGS, None, OK])
    assert plan[:12] == report['plan'][:12] and plan[12][3] == report['plan'][12][3]
    plan_sha = fingerprint(plan)
    assert plan_sha != '69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065'
    proposed = {'schema': 1, 'status': 'PROPOSED_NOT_EXECUTED', 'report_schema': 6, 'prefix_sha256': PREFIX, 'plan_sha256': plan_sha, 'plan': plan, 'new_input': OK, 'screen_count': 14, 'input_count': 13, 'new_input_count': 1, 'terminal_owner': SETTINGS, 'terminal_component': 'Observed stable component in the Settings package; no unobserved activity name assumed', 'full_runtime_1_to_1_established': False, 'exact_alarm_permission_granted': False, 'trigger_configuration_confirmed': False, 'macros_saved': False, 'macros_executed': False}
    write('observed-dialog-contract.json', literal)
    write('proposed-fourteen-screen-plan.json', proposed)
    # Retain complete inspected application files and bind them to the closed input manifest.
    manifest_path = SOURCE / 'reports/release-input-snapshot.json'
    manifest = json.loads(manifest_path.read_bytes())
    source_names = ['source/smali/classes3/74/DayTrigger_74d1108db13471a8.smali', 'source/smali/classes3/ef/Llob_ef0ec2c9c024726d.smali', 'source/smali/classes3/f1/Lzh_f13ce5bd058a5574.smali', 'source/android/res/values/public.xml', 'source/android/res/values/strings.xml']
    source_rows = []
    for name in source_names:
        p = SOURCE / name
        info = identity(p)
        assert manifest['entries'][name] == {'size': info['bytes'], 'sha256': info['sha256']}
        dst = OUT / 'source-inspection' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        source_rows.append({'path': name, **info})
    day, gate, listener = [(SOURCE / n).read_text() for n in source_names[:3]]
    assert re.search(r'\.method public final requiresScheduleExactAlarm\(\)Z\n.*?const/4 p0, 0x1.*?return p0\n\.end method', day, re.S)
    assert 'invoke-virtual {p2}, Landroid/app/AlarmManager;->canScheduleExactAlarms()Z' in gate
    assert 'const p1, 0x7f141194' in gate and 'const/16 v0, 0x10' in gate
    switch = re.search(r':pswitch_data_39e\n\s*\.packed-switch 0x0\n(.*?)\.end packed-switch', listener, re.S).group(1).split()
    assert switch[16] == ':pswitch_144'
    branch = listener.split('    :pswitch_144\n', 1)[1].split('    :pswitch_16a\n', 1)[0]
    assert 'android.settings.REQUEST_SCHEDULE_EXACT_ALARM' in branch and 'Landroid/content/Context;->getPackageName()' in branch and 'Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V' in branch
    write('source-inspection.json', {'schema': 1, 'scope': 'Static preserved source and resource inspection; no dynamic listener execution', 'source_manifest': identity(manifest_path), 'source_snapshot_sha256': manifest['snapshot_sha256'], 'files': source_rows, 'inspection': ['DayTrigger.requiresScheduleExactAlarm returns true', 'Llob.c checks API31 and canScheduleExactAlarms before building the required-permission dialog', 'Dialog message resource0x7f141194 maps to permission_to_set_exact_alarms_required; title0x7f141190 maps to permission_required', 'The positive OnClickListener is Lzh with discriminator16', 'Packed-switch discriminator16 maps to pswitch_144', 'That branch creates REQUEST_SCHEDULE_EXACT_ALARM with package URI derived from Activity.getPackageName and calls Activity.startActivity'], 'settings_owner_is_a_bounded_expectation': True, 'actual_destination_component_not_observed_yet': True})
    parent_rows = []
    for name in ['editor_journey.py', 'observed_journey.py', 'notification_readiness.py', 'day_time_journey.py', 'capture_chronology.py', 'test_day_time_journey.py', 'test_notification_readiness.py']:
        source = PARENT / name
        dst = OUT / 'parent-source' / name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(source, dst)
        parent_rows.append({'path': 'tools/parity_journeys/' + name, **identity(source)})
    write('parent-source-identities.json', parent_rows)
    (OUT / 'DESIGN.md').write_text('''# Exact-alarm dialog: one additional observed input

## Scope and current evidence

The completed readiness run38230072388 records both fixed APKs at the same exact-alarm permission explanation. Both terminal PNGs and XMLs are identical; their complete data and full positive-button ancestor chains are retained here. The root viewed the full terminal image. The observed OK control is `android:id/button1`, text `OK`, enabled and clickable, center `(560,809)` within bounds `[496,761][624,857]`. No later Android input has been executed by this design.

The new plan changes only the previous terminal's required selector from absent to the observed OK selector and appends one input plus one Settings observation. It contains fourteen screens and thirteen inputs. Its complete identity is in `proposed-fourteen-screen-plan.json`. The prior thirteen-screen schema5 and the historical, different fourteen-screen editor plan remain distinct and strict.

## Static source connection

The retained DayTrigger method returns true for the exact-alarm requirement. The common permission gate checks API31 and `AlarmManager.canScheduleExactAlarms`, builds the matching title/message, and installs discriminator16 of the preserved Lzh dialog listener as the positive callback. The listener's switch selects a branch that constructs `android.settings.REQUEST_SCHEDULE_EXACT_ALARM` with the current app's package URI and calls `Activity.startActivity`. The complete inspected smali and resource files are bound to the closed source manifest. This is static source evidence. The Settings package is a bounded expectation for the next capture; no destination activity class or Settings control has been observed yet.

## Exact boundaries for implementation

Add `exact_alarm_journey.py`, `exact_alarm_readiness.py`, focused tests and the observed dialog fixtures to an isolated source overlay. Modify only the common `editor_journey.py` and `observed_journey.py` dispatch and owner boundary where needed. Keep the original notification-readiness module byte-identical. The new readiness module derives from that exact algorithm, with only explicit schema6, new plan identity and plan-validator binding changes; retain its derivation patch. The new plan also requires an exact navigation policy that binds the observed dialog contract and the sole Settings terminal role.

Dispatch by complete plan identity. Do not use the number fourteen alone: the historical editor plan is `69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065`. Original schema2/3/5 reports and their historical whole-object outcomes must remain unchanged. No foreign owner is valid for them. A schema6 report must contain the exact new navigation and readiness policies, each only in its defined role; schema downgrades and extra misplaced fields reject.

The new dialog guard requires both foreground samples to be the exact AddTriggerActivity component, an app-owned hierarchy, one matching positive button, one CANCEL button, the exact title and message, and the unchanged canonical dialog panel. The observed panel contract includes all child roles, attributes, text and bounds. Validate its entire ancestor chain and require the computed center to be `(560,809)` in a720x1280 frame. Revalidate a fresh stable preinput frame and the immediate app PID and foreground before the sole OK tap. Duplicate selectors, changed words, interposed ancestors, changed owner, stale evidence and changed geometry fail before input.

Allow a Settings-owned snapshot only under the exact new fourteen-screen plan and only for its terminal acquisition labels. Capture the original MacroDroid main PID before and after every frame, requiring the already-established post-handoff PID to remain the same. Require both foreground samples to identify the same actually observed component in `com.android.settings`, and the complete UI hierarchy to belong to that owner. Record the component without guessing its class name. No Settings tap, permission grant, subsequent BACK, confirmed configuration, saved macro or executed macro is included. An unexpected owner or process disappearance remains a failed run with complete attempted evidence.

All full-frame stability, first consecutive pair, unique raw roles, monotonic command chronology, immediate input checks, installed APK identity, known notification crash observation and exact paired pixel comparison remain required. Keep the two-second post-input wait and existing bounded command/capture policy. Preserve every failed acquisition. A nonzero intro or Settings difference remains a failed exact comparison; navigation completeness does not replace equality.

## Validation and publication

Use both actual dialog XML/PNG/component sets for positive geometry checks and targeted mutations for the new trust boundaries. Exercise new Settings-owner acceptance only within the new plan and reject it under every old plan, including the old fourteen-screen plan. Exercise altered whole plans, policy/schema substitutions, missing/extra terminal inputs, stale/process/component changes and a nonzero terminal full-frame difference. Test both real recorder command generation and full synthetic paired comparison, labeling synthetic data explicitly. Re-run the packaged host corpus once after the new adapter closes, and replay the closed schema5 Android report to verify its complete verdict remains unchanged.

Freeze the inactive source overlay with all before/after hashes, new-path absence guards, exact fixtures and every executed test attempt. Then derive one separate workflow from the verified readiness workflow, pinning its original/candidate APKs, source capsule and report schema. Its fresh-input preflight, actual AAPT checks, literal verifier, complete artifact upload and owned cleanup must be reviewed before activation. The production app and compared APKs are not modified by this work. Initial owned tmpfs budget:128MiB; no full project or APK copy is needed for the design/source stage.
''')
    rows = [{'path': p.relative_to(OUT).as_posix(), **identity(p), 'mode': '100755' if p.stat().st_mode & 0o111 else '100644'} for p in sorted(OUT.rglob('*')) if p.is_file()]
    write('checkpoint.json', {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'OBSERVED_INPUT_AND_BOUNDED_DESIGN_FROZEN_NOT_EXECUTED', 'repo_target': 'work-in-progress/exact-alarm-navigation/01-observed-input-and-design', 'active_files': [], 'files': rows, 'file_count': len(rows), 'payload_bytes': sum(r['bytes'] for r in rows), 'source_inspection_only': True, 'android_executed_here': False, 'new_plan_sha256': plan_sha, 'parent_plan_sha256': PREFIX, 'parent_readiness_analysis_checkpoint_sha256': '716e3cd70c54659f1b0b84a68a875d61d8c3b1b41e864eb36756938660612439', 'full_runtime_1_to_1_established': False})
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'), 'files': len(rows), 'payload_bytes': sum(r['bytes'] for r in rows), 'new_plan_sha256': plan_sha}, indent=2))


if __name__ == '__main__':
    main()
