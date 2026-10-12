#!/usr/bin/env python3
"""Freeze the actual completed fourteen-screen replay and its command receipt."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import xml.etree.ElementTree as ET

BASE = Path('/dev/shm/macrodroid-exact-alarm-navigation')
RUN = BASE / 'device-run-38240023189'
ANALYSIS = RUN / 'analysis'
RAW_ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189')
OUT = BASE / 'checkpoints/05-fourteen-screen-device-analysis'
REMOTE = 'docs/verification/android-exact-alarm-navigation-3f0ebc9'
APK_SHA = ['84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
           '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182']


def identity(path):
    first = path.lstat()
    assert stat.S_ISREG(first.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    last = path.lstat()
    assert (first.st_dev, first.st_ino, first.st_size, first.st_mtime_ns) == (
        last.st_dev, last.st_ino, last.st_size, last.st_mtime_ns), str(path)
    return {'bytes': last.st_size, 'sha256': digest}


def write(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def read(path):
    return json.loads(path.read_bytes())


def observed_control(root, key, value):
    nodes = [node for node in root.iter('node') if node.get(key) == value]
    assert len(nodes) == 1
    node = nodes[0]
    parents = {child: parent for parent in root.iter() for child in parent}
    chain = [node]
    while chain[-1] in parents and parents[chain[-1]] is not root:
        chain.append(parents[chain[-1]])
    assert parents[chain[-1]] is root
    clickable = next(item for item in chain if item.get('clickable') == 'true')
    assert clickable.get('enabled') == 'true'
    return {'selector': {key: value}, 'node': node.attrib,
            'clickable_ancestor': clickable.attrib, 'ancestor_chain': [item.attrib for item in chain]}


def main():
    result = read(ANALYSIS / 'independent-exact-alarm-analysis.json')
    assert result['status'] == 'EXACT_ALARM_DEVICE_ARTIFACT_REPLAYED' and result['analysis_passed'] is True
    assert result['raw_archive_and_all_files_unchanged'] is True and result['fixed_apks_unchanged'] is True
    assert result['journey_equal'] is False and result['literal_evidence_valid'] is True
    assert result['head_sha'] == '3f0ebc910be72beeb9d7f2443928df2df2258c7d'
    assert result['run_id'] == 38240023189 and result['artifact_id'] == 11742624179
    assert result['diagnostic_rgba_pixel_vector'] == [0, 35] + [0] * 12
    assert result['full_runtime_1_to_1_established'] is False and result['crash_free_run_established'] is False
    assert result['independently_reconstructed_input_copy_roles'] == 295
    assert [(r['status'], r['screens'], r['transitions']) for r in result['recorded_runs']] == [('COMPLETE', 14, 13)] * 2
    assert result['literal_settings_inputs'] == 0 and result['literal_permission_granted_flag'] is False
    assert result['literal_exact_alarm_ok_tapped'] is True and result['literal_settings_navigation_observed'] is True
    command = read(RUN / 'command/command.json')
    assert command['exit_code'] == 0 and command['timed_out'] is False and command['source_unchanged'] is True
    assert command['temporary_directory_removed'] is True
    for name, expected in command['streams'].items():
        assert identity(RUN / 'command' / name) == expected
    source_sha = 'fff58ac2b731a853b681cd1d02bd1060324cf8afd1b980d528495b823f27e967'
    assert identity(ANALYSIS / 'executed-replay-script.py')['sha256'] == source_sha
    assert identity(RUN / 'command/replayed-source.py')['sha256'] == source_sha
    before = read(ANALYSIS / 'raw-file-identities-before.json')
    assert before == read(ANALYSIS / 'raw-file-identities-after.json') and len(before) == 3507
    raw = RAW_ROOT / 'extracted'
    assert {p.relative_to(raw).as_posix() for p in raw.rglob('*') if p.is_file()} == set(before)
    for name, expected in before.items():
        assert identity(raw / name) == expected, name
    archive = RAW_ROOT / 'artifact.zip'
    assert identity(archive) == result['raw_archive'] == {
        'bytes': 46626337, 'sha256': 'c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04'}
    pairs = read(ANALYSIS / 'all-available-full-frame-pairs-diagnostic-only.json')
    assert len(pairs) == 14 and all(item['xml_bytes_equal'] for item in pairs)
    assert all(item['png_bytes_equal'] for i, item in enumerate(pairs) if i != 1)
    assert sum(item['changed_rgba_pixels'] for item in pairs) == 35
    assert len(pairs[1]['all_changed_rgba_pixels']) == 35
    comparison = read(ANALYSIS / 'literal-captured-comparison-replay.json')
    assert comparison['apk_sha256'] == APK_SHA
    assert comparison['global_command_observations'] == {
        'commands': 1091, 'unique_command_streams': 2182, 'planned_inputs': 26,
        'setup_mutations': 6, 'unbound_mutations': 0, 'settings_inputs': 0}
    terminals = read(ANALYSIS / 'observed-terminal-surfaces.json')
    assert len(terminals) == 2
    terminal = terminals[0]['shot']
    xml = raw / 'journey' / terminal['artifacts']['hierarchy']['path']
    png = raw / 'journey' / terminal['artifacts']['screenshot']['path']
    assert identity(xml) == {'bytes': 6919, 'sha256': '44247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e'}
    assert identity(png) == {'bytes': 88338, 'sha256': 'ac9f9f81790687fece02cbba46be83b574b31a8f3bb3f155e940a5245aac1b9c'}
    assert all(item['component'] == 'com.android.settings/com.android.settings.spa.SpaActivity'
               for item in comparison['terminal_surfaces'])
    hierarchy = ET.fromstring(xml.read_bytes())
    toggle = observed_control(hierarchy, 'text', 'Allow setting alarms and reminders')
    navigate = observed_control(hierarchy, 'content-desc', 'Navigate up')
    assert toggle['clickable_ancestor']['checkable'] == 'true'
    assert toggle['clickable_ancestor']['checked'] == 'false'
    assert toggle['clickable_ancestor']['bounds'] == '[0,688][720,855]'
    assert navigate['clickable_ancestor']['bounds'] == '[8,56][104,152]'
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'freeze-device-analysis.py')
    preserved = []
    for path in sorted(RUN.rglob('*')):
        assert not path.is_symlink()
        if not path.is_file():
            continue
        relative = path.relative_to(RUN).as_posix()
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.stat().st_dev == OUT.stat().st_dev:
            os.link(path, target)
        else:
            shutil.copy2(path, target)
        assert identity(target) == identity(path)
        preserved.append(relative)
    write(OUT / 'observed-settings-controls.json', {
        'schema': 1, 'run_id': result['run_id'], 'artifact_id': result['artifact_id'],
        'component': 'com.android.settings/com.android.settings.spa.SpaActivity',
        'full_original_png_viewed_by_root': True, 'both_terminal_png_bytes_equal': True,
        'both_terminal_xml_bytes_equal': True, 'full_image_size': [720, 1280],
        'hierarchy': terminal['artifacts']['hierarchy'], 'screenshot': terminal['artifacts']['screenshot'],
        'hierarchy_attributes': hierarchy.attrib, 'toggle': toggle, 'navigate_up': navigate,
        'toggle_parent_center': [360, 771], 'navigate_up_parent_center': [56, 104],
        'observed_toggle_checked': False, 'new_android_actions': [],
        'settings_inputs_in_this_run': 0, 'permission_granted_in_this_run': False,
        'next_work_scope': 'A separate reviewed workflow may enable the observed switch, verify its checked state, then use the observed Navigate up control and record the resulting app surface.'})
    write(OUT / 'external-evidence.json', {
        'schema': 1,
        'run_url': 'https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38240023189',
        'head_sha': result['head_sha'], 'artifact_id': result['artifact_id'],
        'zip': {'repository_path': REMOTE + '/artifact.zip', **identity(archive)},
        'raw': {'repository_path': REMOTE + '/extracted', 'files': len(before),
            'payload_bytes': sum(item['bytes'] for item in before.values()),
            'inventory_path': 'analysis/raw-file-identities-before.json',
            'inventory_identity': identity(ANALYSIS / 'raw-file-identities-before.json')},
        'extraction_receipt': {'repository_path': REMOTE + '/extracted-extraction.json',
            **identity(RAW_ROOT / 'extracted-extraction.json')},
        'workflow_checkpoint': {'repository_path': 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen/checkpoint.json',
            'sha256': '805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066'},
        'prepared_analyzer_checkpoint': {'repository_path': 'work-in-progress/exact-alarm-navigation/04-device-analyzer/checkpoint.json',
            'sha256': '008737aca46902380116db3583e736a0e15d7c9618b3cccc35d9bb9491d9e62c'},
        'raw_reverified_at_freeze': True, 'preserved_replay_and_wrapper_files': len(preserved),
        'publication_state': 'Publisher must publish and fetch-verify these external raw roles; this capsule does not itself claim remote presence.'})
    bounds = pairs[1]['bounds_exclusive']
    elapsed = (command['finished']['monotonic_ns'] - command['started']['monotonic_ns']) / 1e9
    readme = f'''# Exact-alarm Settings: completed fourteen-screen observation

Run **38240023189**, artifact **11742624179**, executed the workflow at `3f0ebc910be72beeb9d7f2443928df2df2258c7d`. Both APKs completed **14 screens and 13 inputs**. The recorded outcome is **EXACT_ALARM_NAVIGATION_FOURTEEN_SCREEN_DIFFERENCE** with valid evidence and `journey_equal: false`.

The independent replay reproduced the entire captured comparison and the entire workflow verdict, excluding only the replay's new verification timestamp. It reconstructed all **295** prepared input roles, checked all **3,507 raw files** against the single original ZIP, and verified every raw byte and both compared APKs unchanged afterwards. Its own command completed with exit code zero in **{elapsed:.3f} seconds**. The replay issued no Android action. Successful replay verifies the recorded difference; the device result remains a difference.

## Full-frame and hierarchy result

The full RGBA changed-pixel vector is `{result['diagnostic_rgba_pixel_vector']}`. All fourteen paired hierarchies are byte-identical and thirteen paired PNGs are byte-identical. The **35** differing pixels occur on `intro-2` inside exclusive bounds `{bounds}` at the page indicator. Every changed coordinate and both colors are retained. No region was masked and no pixel tolerance was used. This run does not establish the cause of the indicator variation.

The replay checked **{result['accepted_snapshot_ledgers_independently_verified']} accepted snapshot ledgers**, **{result['capture_ledgers']} capture ledgers**, **{result['recorded_frame_observations']} recorded frame observations**, **{result['unique_referenced_journey_artifacts_checked']} unique referenced artifacts**, and all **1,091 commands**. The global command check binds all **2,182 streams**, **26 planned inputs** and **six install/launch setup mutations**, with zero unbound mutations. All **209 journey**, **10 animation**, and **6 downloader** host tests have individual successful raw log entries. The nineteen zero-scale commands and owned runtime cleanup also verify.

## Exact-alarm navigation and observed Settings controls

Both APKs reached `com.android.settings/com.android.settings.spa.SpaActivity` through the previously observed **OK** button. The paired terminal PNGs are exactly 88,338 bytes with SHA-256 `ac9f9f81790687fece02cbba46be83b574b31a8f3bb3f155e940a5245aac1b9c`; the XMLs are exactly 6,919 bytes with SHA-256 `44247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e`. The root viewed the full original PNG and read both hierarchies.

The page identifies **MacroDroid 5.67.8**. Its **Allow setting alarms and reminders** row is enabled, clickable and checkable, with `checked=false`. The actual clickable ancestor bounds are `[0,688][720,855]`, giving center `(360,771)`. The visible **Navigate up** control has clickable ancestor bounds `[8,56][104,152]`, giving center `(56,104)`. Full node and ancestor attributes are retained in `observed-settings-controls.json`.

This run contains **zero Settings inputs**, no permission grant, no confirmed trigger configuration, and no saved or executed macro. A separate extension can bind these observed controls, enable the switch, verify the resulting checked state and then use Navigate up to observe the returned app surface. Those next actions have not been performed by this run or replay.

## Process observations and limits

Both notification readiness phases contain four `HOME_WITH_SAME_PID` observations and accept the first eligible sequence `[0,3]`. Both runs also record the known Fragment LB `java.lang.IllegalStateException`, followed by continuation in a replacement process. Complete raw crash and readiness evidence remains in the comparison and artifact. This is not a crash-free run, and the notification action is not established as the cause of that exception.

Full runtime 1:1 and animation timing parity remain unestablished. This evidence applies to the fourteen declared still screens and thirteen inputs with the two fixed APK identities. Historical failures and comparisons retain their original outcomes.

## Preserved files

The capsule includes every closed replay output, the exact replay source, the exact bounded command wrapper, complete command stdout/stderr and timing, full paired captures, source identities, complete verdicts and inventories. `external-evidence.json` binds the unchanged original ZIP and its complete extraction. Only the already identified ephemeral public ADB value is omitted from a clearly marked review copy of the boot log; original raw bytes remain unchanged.
'''
    (OUT / 'README.md').write_text(readme)
    rows = [{'path': p.relative_to(OUT).as_posix(), **identity(p),
             'mode': '100755' if p.stat().st_mode & 0o111 else '100644'}
            for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'EXACT_COMPLETED_FOURTEEN_SCREEN_DIFFERENCE_REPLAYED',
        'repo_target': REMOTE + '/analysis', 'active_files': [],
        'android_executed_by_analysis': False, 'device_evidence_valid': True,
        'journey_equal': False, 'full_runtime_1_to_1_established': False,
        'files': rows, 'file_count': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows),
        'raw_zip_identity': identity(archive), 'run_id': result['run_id'],
        'artifact_id': result['artifact_id'], 'head_sha': result['head_sha']}
    write(OUT / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
        'files': len(rows), 'payload_bytes': checkpoint['payload_bytes']}, indent=2))


if __name__ == '__main__':
    main()
