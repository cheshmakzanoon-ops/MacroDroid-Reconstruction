#!/usr/bin/env python3
"""Freeze the reviewed offline replay; no Android or repository mutation."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'analysis'


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    assert OUT.is_dir() and not (OUT / 'checkpoint.json').exists()
    value = json.loads((OUT / 'independent-analysis.json').read_text())
    assert value['run_id'] == 38204928419
    assert value['exact_pinned_comparator_replay_matches'] is True
    assert value['preserved_comparison']['reason'] == 'App PID changed or lacks two live samples'
    pairs = value['full_unmasked_snapshot_pairs']
    assert len(pairs) == 16 and all(p['xml_bytes_equal'] for p in pairs)
    assert sum(p['png_bytes_equal'] for p in pairs) == 5
    assert [p['changed_rgba_pixels'] for p in pairs] == [578,589,578,578,570969,578,578,578,578,578,578,0,0,0,0,0]
    for source, name in [('analysis-run-02.log', 'analysis-run-02.log'),
                         ('preliminary-pixels.json', 'preliminary-pixels.json'),
                         ('job.log', 'workflow-job.log')]:
        shutil.copyfile(ROOT / source, OUT / name)
    shutil.copyfile(Path(__file__), OUT / Path(__file__).name)
    table = '\n'.join('| ' + p['name'] + ' | ' + str(p['changed_rgba_pixels']) + ' | '
                      + ('Equal' if p['xml_bytes_equal'] else 'Different') + ' | '
                      + ('Equal' if p['png_bytes_equal'] else 'Different') + ' |' for p in pairs)
    crashes = value['fatal_exceptions_and_process_events']
    hosting = '\n'.join('| ' + p['label'] + ' | ' + p['old_pid'] + ' → ' + p['new_pid'] + ' | '
                        + p['new_process_hosting_type'] + ' | `' + p['new_process_hosting_component'] + '` |'
                        for p in crashes)
    text = f'''# External sixteen-screen editor recording: run 38204928419

Both exact installed APKs recorded all sixteen planned screens and thirty total inputs in the external plan from commit `736da1920f7dada1d0c3444032ffcf4eb8759888`. The original comparator result remains **REJECTED**, with reason `App PID changed or lacks two live samples`. This analysis reproduces that result using the unchanged pinned comparator. It separately measures the complete screenshots and raw hierarchies and retains the actual fatal exception and different process-start events. It does not convert the failed journey into a passing one.

The exact 10,973,841-byte artifact ZIP (SHA-256 `1120c0bdcff9d054a08bf3e52f733000597ca18c28a5a17230276e0fd7fad785`) and its [member manifest](../manifest.json) were published by the existing evidence archive workflow in commit `590fddb2a4703c56c5520886e68f8366d3727ceb`. All 1,784 members were independently read and checked. The replay verified {value['all_referenced_artifact_paths_verified']:,} distinct artifact paths referenced by the report, both actual installed APK identities, each captured tree and PID sample, all thirty recorded preinput guards and tap/BACK commands, and unchanged before/after environment records. The hosted job passed 33 journey host tests and six download controls before device execution; those host successes do not establish app parity.

## Full, unmasked capture pairs

| Recorded surface | Changed RGBA pixels | Full XML bytes | Full PNG bytes |
| --- | ---: | --- | --- |
{table}

All sixteen XML pairs and complete parsed trees match. The eleven differing frames retain their full pixel counts. For ten of those frames, a white system status icon differs within `[596,10,632,38)`; the TRIGGERS frame also has eleven page-dot pixels beyond those 578 status-icon pixels. The notification frame has a large background/dimming difference across its full bounds. The five final frames, including the action and constraint catalogs and final editor return, are byte-identical PNGs. Diagnostic row counts in the JSON only describe where pixels differ; no row, icon, or screenshot region is excluded from equality.

The artifact records one successful acquisition for each named screen. It does not prove consecutive full-frame stability or establish why the status icon, page dots, or notification background differed. The separate ten-screen observation policy is a later opt-in workflow and is not retroactively applied to this evidence.

## Fatal exception and different process starts

Both old main processes logged `java.lang.IllegalStateException` when the LB fragment was no longer attached to its Activity. The exact ten-frame stack matches between the two APKs; the literal messages contain different runtime fragment instance IDs and are retained unchanged. The full [lifecycle log](lifecycle.log), [original fatal block](original-fatal.txt), and [candidate fatal block](candidate-fatal.txt) remain available.

| APK | Recorded PID change | First hosting type for replacement | Recorded hosting component |
| --- | --- | --- | --- |
{hosting}

Both later capture NewHomeScreenActivity, but the original replacement first starts for the crashguard service while the candidate replacement first starts for the home activity. Those literal events differ. Full process-lifecycle equality and a crash-free run are not established. The first version of this analysis carried forward the prior run's assumption that both replacements were started as top activities. Its assertion failed on the actual original service event; that source and failure log are preserved under `analysis-attempts/01-top-activity-assumption/`. The final analyzer explicitly records and verifies the two different observed hosting events.

## Observed editor navigation

Both runs close the observed LITEAPKS dialog, enter the empty editor, display Favourite Triggers information, tap the observed `android:id/button1`, return to the editor, open the trigger catalog, return with BACK, open the action catalog, return, open the constraint catalog, and return. Every tap is bound to its raw preinput hierarchy, enabled/clickable target and geometry; all tap and BACK inputs retain the recorded foreground and live-PID checks in the derived JSON. The earlier single-OK action was therefore executed by this external run. The recording issues no macro-save or execution action, and no later creation/configuration step is inferred from viewing a catalog.

The unchanged original screenshots and XML are in `captures/`, with exact foreground and PID files for both APKs. Useful starting points are [trigger catalog](captures/original-trigger-catalog-acquisition-1.png), [action catalog](captures/original-action-catalog-acquisition-1.png), [constraint catalog](captures/original-constraint-catalog-acquisition-1.png), and [final editor](captures/original-editor-after-constraint-back-acquisition-1.png). The full pinned source and replay script accompany the analysis. Running the replay performs file verification and image/XML measurement only; it performs no device action and changes no APK.
'''
    (OUT / 'README.md').write_text(text)
    patterns = [rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', rb'(?m)^adb\.pubkey=',
                rb'(?i)authorization:\s*bearer\s+[A-Za-z0-9_-]{12,}', rb'gh[pousr]_[A-Za-z0-9]{30,}']
    for path in OUT.rglob('*'):
        if path.is_file() and path.suffix != '.png':
            data = path.read_bytes()
            assert not any(re.search(pattern, data) for pattern in patterns), path
    files = [{'path': p.relative_to(OUT).as_posix(), **meta(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    result = {'schema':1, 'status':'FROZEN_COMPLETE_OFFLINE_REPLAY_OF_FAILED_DEVICE_JOURNEY',
              'run_id':38204928419, 'head_sha':value['head_sha'], 'archive_commit':value['archive_commit'],
              'source_archive':value['archive'], 'all_archive_members_verified':1784,
              'artifact_paths_verified':value['all_referenced_artifact_paths_verified'],
              'recorded_screens_per_apk':16, 'verified_inputs_total':30,
              'original_comparator_result_preserved':True, 'full_runtime_1_to_1_established':False,
              'crash_free_run_established':False, 'full_process_lifecycle_equal_established':False,
              'files':files}
    (OUT / 'checkpoint.json').write_text(json.dumps(result, indent=2) + '\n')
    for entry in files:
        assert meta(OUT / entry['path']) == {k:entry[k] for k in ['bytes','sha256']}
    print(json.dumps({'path':str(OUT / 'checkpoint.json'), **meta(OUT / 'checkpoint.json'),
                      'files':len(files), 'analysis':meta(OUT / 'independent-analysis.json'),
                      'readme':meta(OUT / 'README.md')}, indent=2))


if __name__ == '__main__':
    main()
