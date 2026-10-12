"""Replay the preserved session02 false positive against the narrow component fix."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'external474-worktree'
WORK = ROOT / 'component-pair-worktree'
CASE = ROOT / 'component-pair-reports/01-frozen02-false-positive'
OUT = ROOT / 'component-pair-reports/02-corrected-replay'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(WORK / 'tools/parity_journeys'), str(WORK / 'project')]
    import post_onboarding as corrected
    import android_compare as proof
    old_path = OLD / 'tools/parity_journeys/post_onboarding.py'
    assert meta(old_path.read_bytes())['sha256'] == 'da3bd4da63d5077da23cfef65adc30215ed88e62a2becd43fd7e149ff616c3c9'
    spec = importlib.util.spec_from_file_location('frozen02_session', old_path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    OUT.mkdir(parents=True, exist_ok=False)
    previous = json.loads((CASE / 'review-result.json').read_bytes())
    assert meta((CASE / 'synthetic-artifacts.zip').read_bytes()) == previous['archive']
    members = json.loads((CASE / 'synthetic-artifact-manifest.json').read_bytes())
    rows = []
    with tempfile.TemporaryDirectory(prefix='session-component-replay-') as temporary:
        folder = Path(temporary)
        with zipfile.ZipFile(CASE / 'synthetic-artifacts.zip') as archive:
            assert sorted(archive.namelist()) == sorted(row['path'] for row in members)
            for row in members:
                data = archive.read(row['path'])
                assert meta(data) == {key: row[key] for key in ('bytes', 'sha256')}
                target = folder / row['path']
                assert target.resolve().is_relative_to(folder.resolve())
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        for name in ('before', 'after'):
            report = json.loads((CASE / (name + '-report.json')).read_bytes())
            baseline = old.compare_session(folder, report, report['plan'], proof)
            result = corrected.compare_session(folder, report, report['plan'], proof)
            assert baseline['editor_session_equal']
            assert baseline == json.loads((CASE / (name + '-frozen02.json')).read_bytes())
            assert result['editor_session_equal'] == (name == 'before'), result
            assert result['evidence_identity_check']['unique_observation_files'] == 294
            if name == 'before':
                assert all(row['foreground_component_equal'] for row in result['screens'])
            else:
                assert 'observed editor activity' in result['reason']
            (OUT / (name + '-corrected.json')).write_text(json.dumps(result, indent=2) + '\n')
            rows.append({'report': name, 'frozen02_equal': baseline['editor_session_equal'],
                         'frozen02_literal_result_reproduced': True,
                         'corrected_equal': result['editor_session_equal'], 'corrected_status': result['status'],
                         'corrected_reason': result.get('reason'), 'unique_semantic_files': 294})
    result = {'schema': 1, 'status': 'PRESERVED_PAIRED_COMPONENT_FALSE_POSITIVE_NOW_REJECTED',
              'source_before': meta(old_path.read_bytes()),
              'source_after': meta((WORK / 'tools/parity_journeys/post_onboarding.py').read_bytes()),
              'archive': previous['archive'], 'archive_members_verified': len(members), 'cases': rows,
              'android_executed': False, 'active_repository_modified': False,
              'source02_unchanged': meta(old_path.read_bytes())['sha256'] == previous['frozen_source']['sha256'],
              'new_runtime_gate': 'PENDING_FRESH_CAPTURE'}
    (OUT / 'recheck-result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
