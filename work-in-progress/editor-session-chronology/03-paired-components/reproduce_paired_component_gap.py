"""Preserve the final paired-component gap against the immutable session02 source."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'component-pair-reports/01-frozen02-false-positive'
WORK = ROOT / 'external474-worktree'
PIN = 'da3bd4da63d5077da23cfef65adc30215ed88e62a2becd43fd7e149ff616c3c9'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def replace_final(f, run, activity, suffix):
    data = ('topResumedActivity=com.arlosoft.macrodroid/' + activity).encode()
    shot = run['screens'][-1]
    shot['artifacts']['foreground'] = f.put(run, suffix + '-capture', data)
    shot['session_identity']['foreground']['stdout'] = f.put(run, suffix + '-endpoint', data)


def main():
    sys.dont_write_bytecode = True
    assert meta((WORK / 'tools/parity_journeys/post_onboarding.py').read_bytes())['sha256'] == PIN
    sys.path[:0] = [str(WORK / 'tools/parity_journeys'), str(WORK / 'project')]
    import test_post_onboarding as fixtures
    OUT.mkdir(parents=True, exist_ok=False)
    f = fixtures.SessionTests()
    f.setUp()
    try:
        # Use the final Activity actually observed in both preserved 934c654 captures.
        for run in f.report['runs']:
            replace_final(f, run, '.editscreen.EditMacroActivity', 'observed-final-editor')
        before_report = copy.deepcopy(f.report)
        before = f.result()
        assert before['editor_session_equal'], before
        replace_final(f, f.report['runs'][1], '.DifferentFinalActivity', 'changed-final-component')
        after = f.result()
        assert after['editor_session_equal'], after
        assert before['evidence_identity_check']['unique_observation_files'] == 294
        assert after['evidence_identity_check']['unique_observation_files'] == 294
        assert all(row['changed_pixels'] == 0 and row['hierarchy_equal'] for row in after['screens'])
        for name, obj in [('before-report.json', before_report), ('after-report.json', f.report),
                          ('before-frozen02.json', before), ('after-frozen02.json', after)]:
            (OUT / name).write_text(json.dumps(obj, indent=2) + '\n')
        members = []
        with zipfile.ZipFile(OUT / 'synthetic-artifacts.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(f.root.rglob('*')):
                if not path.is_file():
                    continue
                data = path.read_bytes()
                relative = path.relative_to(f.root).as_posix()
                info = zipfile.ZipInfo(relative, date_time=(2026, 10, 12, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
                members.append({'path': relative, **meta(data)})
        (OUT / 'synthetic-artifact-manifest.json').write_text(json.dumps(members, indent=2) + '\n')
        result = {'schema': 1, 'status': 'FROZEN02_PAIRED_FINAL_COMPONENT_FALSE_POSITIVE_REPRODUCED',
                  'frozen_source': meta((WORK / 'tools/parity_journeys/post_onboarding.py').read_bytes()),
                  'baseline_equal': before['editor_session_equal'], 'mutated_equal': after['editor_session_equal'],
                  'mutated_status': after['status'], 'unique_semantic_files': 294,
                  'full_pixel_difference_vector': [row['changed_pixels'] for row in after['screens']],
                  'all_full_hierarchies_equal': True,
                  'mutation': 'Candidate final capture AND its separate final identity foreground change to another same-package Activity; distinct fresh files and unchanged timestamps, pixels, hierarchies, PIDs and APK digests.',
                  'original_final_component': 'com.arlosoft.macrodroid/com.arlosoft.macrodroid.editscreen.EditMacroActivity',
                  'candidate_final_component': 'com.arlosoft.macrodroid/com.arlosoft.macrodroid.DifferentFinalActivity',
                  'archive': meta((OUT / 'synthetic-artifacts.zip').read_bytes()), 'archive_members': len(members),
                  'android_executed': False, 'active_repository_modified': False,
                  'startup_parity_established': False, 'full_runtime_1_to_1_established': False}
        (OUT / 'review-result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    finally:
        f.doCleanups()


if __name__ == '__main__':
    main()
