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

ROOT = Path('/dev/shm/macrodroid-readiness-independent-review-02')
SOURCE = Path('/dev/shm/macrodroid-notification-readiness/stage-02/repository')
OUTPUT = ROOT / 'reports/corrected-guard-01'


def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if OUTPUT.exists(): raise RuntimeError('Use a fresh output directory')
    OUTPUT.mkdir(parents=True)
    shutil.copyfile(__file__, OUTPUT / 'probe_corrected_guard.py')
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
    result = {'scope': 'Independent replay of the closed synthetic counterexamples and precise follow-up checks against the corrected validator; not Android, no parity credit.',
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
        if changed.get('journey_equal') or 'Global command ledger is not chronological' not in changed.get('reason', ''):
            raise RuntimeError('Whole-block ledger counterexample still accepted or rejected for the wrong reason')
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
        if changed.get('journey_equal'):
            raise RuntimeError('Compound boolean mutation still accepted')
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
        if accepted or 'first eligible contiguous sequence' not in (reason or ''):
            raise RuntimeError('Short raw command span still accepted or rejected for the wrong reason')
        result['cases'].append({'name': 'row-wrapper-span-inflation-phase-only', 'phaseAccepted': accepted,
                                'rawHomeCommandSpanSeconds': command_span, 'rowWrapperSpanSeconds': wrapper_span,
                                'policyMinimumReadySpanSeconds': ready.POLICY['minimum_ready_span_seconds'],
                                'reason': reason, 'fullReportAcceptanceClaimed': False})
        case.report.clear(); case.report.update(copy.deepcopy(original_report))
        # Each primitive format fault is independent. Only its phase changes;
        # original phase bytes and complete report are restored before the next.
        for label, mutate, expected_reason in (
            ('literal-integer-phase-schema', lambda p: p.update(schema=True), 'Incomplete or altered notification readiness phase'),
            ('literal-integer-accepted-index', lambda p: p['accepted_sequence'].__setitem__(0, True), 'first eligible contiguous sequence'),
            ('literal-integer-gap-index', lambda p: p['gaps'][0].update(after_index=False), 'Invalid notification readiness fixed gap')):
            case.report.clear(); case.report.update(copy.deepcopy(original_report))
            reference = case.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY]
            (case.folder / reference['path']).write_bytes(original_phase)
            case.edit_phase(mutate)
            changed = case.fixture.result()
            save(OUTPUT / (label + '-result.json'), changed)
            if changed.get('journey_equal') or expected_reason not in changed.get('reason', ''):
                raise RuntimeError('Primitive format fault accepted or rejected for the wrong reason: ' + label)
            result['cases'].append({'name': label, 'journeyEqual': False, 'reason': changed['reason']})
        case.report.clear(); case.report.update(copy.deepcopy(original_report))
        reference = case.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY]
        (case.folder / reference['path']).write_bytes(original_phase)
        # A configured timeout can have been allocated before the later start.
        # Real endpoints still fall inside the exact same bounded phase.
        allocated = json.loads(original_phase)
        allocated['observations'][-1]['commands'][0]['timeout_seconds'] = 10
        save(OUTPUT / 'pre-start-timeout-allocation-phase.json', allocated)
        ready.verify_phase(case.folder, allocated, tests.proof)
        result['cases'].append({'name': 'pre-start-timeout-allocation', 'phaseAccepted': True,
                                'actualPhaseSeconds': allocated['seconds'], 'configuredTimeoutSeconds': 10})
        late = copy.deepcopy(allocated)
        late['observations'][-1]['commands'][-1]['finished_monotonic'] = late['finished_monotonic'] + 0.01
        save(OUTPUT / 'late-actual-command-end-phase.json', late)
        try:
            ready.verify_phase(case.folder, late, tests.proof)
        except Exception as error:
            late_reason = str(error)
        else:
            raise RuntimeError('A real command endpoint outside the phase was accepted')
        if 'actual phase bound' not in late_reason:
            raise RuntimeError('Late endpoint rejected for the wrong reason: ' + late_reason)
        result['cases'].append({'name': 'late-actual-command-end', 'phaseAccepted': False, 'reason': late_reason})
        # Moving a whole block is different from deleting the input's complete
        # ledger record while leaving every remaining record in chronological order.
        case.report['commands'].remove(case.report['runs'][0]['transitions'][4]['command'])
        missing_input = case.fixture.result()
        save(OUTPUT / 'missing-denial-ledger-entry-result.json', missing_input)
        if missing_input.get('journey_equal') or 'immediately follow their unique denial input' not in missing_input.get('reason', ''):
            raise RuntimeError('Missing input ledger binding accepted or rejected for the wrong reason')
        result['cases'].append({'name': 'missing-denial-ledger-entry', 'journeyEqual': False, 'reason': missing_input['reason']})
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
        result['status'] = 'CORRECTED_GUARD_INDEPENDENT_REVIEW_PASSED'
        result['passed'] = True
    except BaseException as error:
        result.update(status='REVIEW_EXECUTION_FAILED', passed=False, error=str(error))
        (OUTPUT / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        case.doCleanups()
        after = {str(p): ident(p) for p in selected}
        save(OUTPUT / 'source-identities-after.json', after)
        result['allBoundSourceBytesUnchanged'] = before == after
        result['durationSeconds'] = time.monotonic() - started
        save(OUTPUT / 'result.json', result)
        print(json.dumps(result, indent=2))
    if not result.get('passed') or not result['allBoundSourceBytesUnchanged']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
