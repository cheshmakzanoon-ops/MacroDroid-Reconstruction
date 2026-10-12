#!/usr/bin/env python3
"""Bounded independent synthetic counterexamples; no Android or source edits."""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys
import tarfile
import time
import traceback

ROOT = Path('/workspace/scratch/4130730d15aa/notification-readiness-review')
SOURCE = Path('/workspace/scratch/4130730d15aa/notification-readiness-forward/stage-01/repository')
OUTPUT = ROOT / 'reports/initial-guard-01'


def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if OUTPUT.exists(): raise RuntimeError('Use a fresh output directory')
    OUTPUT.mkdir(parents=True)
    shutil.copyfile(__file__, OUTPUT / 'probe_initial_guard.py')
    selected = sorted((SOURCE / 'tools/parity_journeys').glob('*.py')) + sorted((SOURCE / 'project').glob('*.py'))
    before = {str(p): ident(p) for p in selected}
    save(OUTPUT / 'source-identities-before.json', before)
    (OUTPUT / 'reviewed-sources').mkdir()
    for name in ('notification_readiness.py', 'editor_journey.py', 'observed_journey.py', 'test_notification_readiness.py'):
        shutil.copyfile(SOURCE / 'tools/parity_journeys' / name, OUTPUT / 'reviewed-sources' / name)
    sys.path.insert(0, str(SOURCE / 'tools/parity_journeys'))
    sys.path.insert(0, str(SOURCE / 'project'))
    import notification_readiness as ready
    import test_notification_readiness as tests
    started = time.monotonic()
    result = {'scope': 'Synthetic guard counterexamples using the real current validator; not Android, no parity credit.',
              'reviewedModule': before[str(SOURCE / 'tools/parity_journeys/notification_readiness.py')], 'cases': []}
    case = tests.ReadinessReportControls()
    try:
        case.setUp(); case.add_phases()
        original_report = copy.deepcopy(case.report)
        original_phase = tests.proof.artifact(case.folder, case.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY])
        baseline = case.fixture.result()
        save(OUTPUT / 'baseline-result.json', baseline)
        if not baseline.get('journey_equal'): raise RuntimeError('Synthetic positive prerequisite failed')
        result['baselinePassed'] = True
        # Move the complete original readiness block, keeping every byte/timing
        # and its internal order unchanged, ahead of all earlier device commands.
        phase_ref = case.report['runs'][0]['transitions'][4][ready.REFERENCE_KEY]
        phase = json.loads(tests.proof.artifact(case.folder, phase_ref))
        commands = [c for row in phase['observations'] for c in row['commands']]
        positions = [case.report['commands'].index(c) for c in commands]
        block = [case.report['commands'][i] for i in positions]
        case.report['commands'][:] = block + [c for i, c in enumerate(case.report['commands']) if i not in positions]
        changed = case.fixture.result()
        save(OUTPUT / 'whole-block-ledger-reorder-result.json', changed)
        result['cases'].append({'name': 'whole-block-ledger-reorder', 'journeyEqual': changed.get('journey_equal'),
                                'originalPositions': positions, 'newPositions': list(range(len(block))),
                                'reason': changed.get('reason')})
        case.report.clear(); case.report.update(copy.deepcopy(original_report))
        def bools(phase):
            phase['schema'] = True
            phase['observations'][0]['index'] = False
            phase['observations'][1]['index'] = True
            phase['accepted_sequence'][0] = True
        case.edit_phase(bools)
        changed = case.fixture.result()
        save(OUTPUT / 'boolean-schema-indices-result.json', changed)
        result['cases'].append({'name': 'boolean-schema-indices', 'journeyEqual': changed.get('journey_equal'),
                                'reason': changed.get('reason')})
        case.report.clear(); case.report.update(copy.deepcopy(original_report))
        reference = case.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY]
        (case.folder / reference['path']).write_bytes(original_phase)
        # Phase-only boundary: retain absent + two HOME observations but let the
        # last row wrapper continue long after its last real command completed.
        phase = json.loads(original_phase)
        phase['observations'] = phase['observations'][:3]
        phase['gaps'] = phase['gaps'][:2]
        phase['observations'][-1]['finished_monotonic'] = phase['finished_monotonic']
        phase['accepted_sequence'] = [1, 2]
        rows = phase['observations']
        command_span = rows[-1]['commands'][-1]['finished_monotonic'] - rows[1]['commands'][0]['started_monotonic']
        wrapper_span = rows[-1]['finished_monotonic'] - rows[1]['started_monotonic']
        try:
            replayed = ready.verify_phase(case.folder, phase, tests.proof)
            accepted, reason = True, None
        except Exception as error:
            accepted, reason = False, str(error)
        save(OUTPUT / 'row-wrapper-span-phase.json', phase)
        result['cases'].append({'name': 'row-wrapper-span-inflation-phase-only', 'phaseAccepted': accepted,
                                'rawHomeCommandSpanSeconds': command_span, 'rowWrapperSpanSeconds': wrapper_span,
                                'policyMinimumReadySpanSeconds': ready.POLICY['minimum_ready_span_seconds'],
                                'reason': reason, 'fullReportAcceptanceClaimed': False})
        case.report.clear(); case.report.update(copy.deepcopy(original_report))
        restored = case.fixture.result()
        save(OUTPUT / 'restored-result.json', restored)
        if restored != baseline: raise RuntimeError('Exact synthetic positive restoration failed')
        save(OUTPUT / 'synthetic-positive-report.json', case.report)
        payloads = {p.relative_to(case.folder).as_posix(): ident(p) for p in sorted(case.folder.rglob('*')) if p.is_file()}
        save(OUTPUT / 'synthetic-artifact-inventory.json', payloads)
        with tarfile.open(OUTPUT / 'synthetic-artifacts.tar.gz', 'w:gz') as archive:
            for name in payloads: archive.add(case.folder / name, arcname=name, recursive=False)
        result['syntheticArtifacts'] = {'count': len(payloads), 'archive': ident(OUTPUT / 'synthetic-artifacts.tar.gz')}
        result['exactSyntheticResultRestored'] = True
        result['status'] = 'COUNTEREXAMPLE_REVIEW_COMPLETED'
    except BaseException as error:
        result.update(status='REVIEW_EXECUTION_FAILED', error=str(error))
        (OUTPUT / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        case.doCleanups()
        after = {str(p): ident(p) for p in selected}
        save(OUTPUT / 'source-identities-after.json', after)
        result['allBoundSourceBytesUnchanged'] = before == after
        result['durationSeconds'] = time.monotonic() - started
        save(OUTPUT / 'result.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
