#!/usr/bin/env python3
"""Read the preserved targeted run; compare templates without executing Java/D8."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path('/dev/shm/day-numeric-hosted-01')
WORK = Path('/workspace/scratch/4130730d15aa')
STUDY = WORK / 'day-trigger-integration/reports/04-targeted-numeric-attempt-02'
sys.path.insert(0, str(ROOT / 'source/tools/day_numeric_acceptance'))
import inputs
import verify


def main():
    output = ROOT / 'reports/real-command-compatibility-01'
    output.mkdir()
    report = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Read-only compatibility with existing targeted execution; path role remapping is explicit',
              'java_or_d8_executed_in_this_check': False, 'full_integrated_seventeen_command_run_executed': False,
              'signed_numeric_primary_packaging_verified': False, 'android_executed': False}
    try:
        checkpoint = WORK / 'day-trigger-integration/checkpoints/03-targeted-numeric-integration/checkpoint.json'
        inputs.require(inputs.identity(checkpoint)['sha256'] == '81f44192b6c8862938d952ec9b5b37368c9a32d7d31e0c5ca9391b3ebbe975bc',
                       'Closed targeted source checkpoint differs')
        fixed = inputs.read_json(checkpoint)
        old = inputs.read_json(STUDY / 'result.json')
        inputs.require(old['passed'] is True and old['signed_numeric_primary_packaging_verified'] is False,
                       'Old actual targeted scope differs')
        report['targeted_checkpoint'] = inputs.identity(checkpoint)
        report['targeted_result'] = {'path': str(STUDY / 'result.json'), **inputs.identity(STUDY / 'result.json')}
        report['verifier'] = inputs.identity(ROOT / 'source/tools/day_numeric_acceptance/verify.py')
        producer = WORK / 'day-trigger-integration/overlay-01/project/day_numeric_dex_controls.py'
        report['fixed_production_runner'] = {'path': str(producer), **inputs.identity(producer)}
        inputs.require(report['fixed_production_runner']['sha256'] == '2d5c58fc15dc50d74aeaf85802e5d57a785937439f6692772801a621209211e2',
                       'Frozen integrated numeric runner changed')
        future = Path('/explicit-future-project-role')
        folder = 'reports/day-numeric-dex-explicit-evidence-role'
        java = str(WORK / 'tooling/jdk21/bin/java')
        expected = verify.expected_numeric_commands(future, folder, java)
        old_jar = str(WORK / 'current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')
        new_jar = str(future / 'tools/lib/jadx-r2721.4574686-all.jar')
        report['jar_identity'] = inputs.identity(Path(old_jar))
        inputs.require(report['jar_identity']['sha256'] == '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e',
                       'The measured compiler jar differs from the fixed baseline')
        mapping = {new_jar: old_jar, str(future / folder): str(STUDY)}
        report['path_role_mapping'] = mapping
        paired = [(0, 4), (1, 5), (2, 6), (6, 34), (7, 35), (8, 36), (10, 38), (11, 39), (12, 40)]
        selected, checks = [], []
        for wanted_index, actual_index in paired:
            subdir, label, code, argv = expected[wanted_index]
            mapped = [arg.replace(str(future / folder), str(STUDY)).replace(new_jar, old_jar) for arg in argv]
            row = old['commands'][actual_index]
            inputs.require(row['name'] == label and row['returncode'] == code and row['timeout_seconds'] == 120
                           and row['argv'] == mapped, 'Preserved D8 command template differs')
            selected.append({'original_command_index': actual_index, 'unaltered_original_row': row})
            checks.append({'future_index': wanted_index, 'actual_index': actual_index, 'role': subdir + '/' + label,
                           'exact_after_declared_path_mapping': True})
        harness_pairs = [(5, 7), (9, 37), (13, 41), (14, 42), (15, 43), (16, 44)]
        classpath = ':'.join([old_jar, str(STUDY / 'hostclasses'), str(STUDY / 'harnessclasses'),
                             '/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/build/java/hostclasses',
                             '/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/tools/classes'])
        report['targeted_classpath'] = classpath
        report['classpath_scope_note'] = ('The actual small study used its new host/harness directories plus the existing compiled baseline; '
                                          'the future complete build uses only its own jar, hostclasses and tools/classes. '
                                          'These layouts are not labeled byte-identical classpaths.')
        for wanted_index, actual_index in harness_pairs:
            subdir, label, code, argv = expected[wanted_index]
            mapped = list(argv)
            mapped[5] = classpath
            mapped[-2:] = [str(STUDY / subdir / 'config.json'), str(STUDY / subdir / 'result.json')]
            row = old['commands'][actual_index]
            inputs.require(row['name'] == label and row['returncode'] == code and row['timeout_seconds'] == 120
                           and row['argv'] == mapped, 'Preserved harness policy or config/result role differs')
            selected.append({'original_command_index': actual_index, 'unaltered_original_row': row})
            checks.append({'future_index': wanted_index, 'actual_index': actual_index, 'role': subdir + '/' + label,
                           'exact_after_declared_path_and_classpath_mapping': True})
        streams = []
        physical = set()
        for selected_row in selected:
            for stream in ('stdout', 'stderr'):
                row = selected_row['unaltered_original_row'][stream]
                path = inputs.checked_identity(STUDY, row['path'], {k: row[k] for k in ('bytes', 'sha256')})
                key = (path.stat().st_dev, path.stat().st_ino)
                inputs.require(key not in physical, 'Preserved real command streams share a physical file')
                physical.add(key)
                destination = output / 'retained-actual-streams' / row['path']
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(path.read_bytes())
                streams.append(row)
        positive = inputs.read_json(STUDY / 'positive/config.json')
        configs = []
        for name in ('original-as-rebuilt-rejected', 'wrong-helper-class-rejected'):
            path = STUDY / name / 'config.json'
            actual = inputs.read_json(path)
            verify.verify_provenance_config(actual, positive, name)
            destination = output / 'retained-actual-configs' / name / 'config.json'
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(path.read_bytes())
            configs.append({'role': name, **inputs.identity(path)})
        (output / 'retained-actual-configs/positive').mkdir()
        (output / 'retained-actual-configs/positive/config.json').write_bytes((STUDY / 'positive/config.json').read_bytes())
        inputs.write_json(output / 'selected-unaltered-command-rows.json', sorted(selected, key=lambda row: row['original_command_index']))
        inputs.write_json(output / 'future-seventeen-command-policy.json', expected)
        report.update(passed=True, status='PRESERVED_TARGETED_COMMAND_TEMPLATES_AND_PROVENANCE_CONFIGS_VERIFIED',
                      pipeline_commands_verified=9, harness_commands_verified=6, real_streams_verified=len(streams),
                      provenance_configs_verified=configs, checks=checks,
                      future_signed_instruction_commands=[{'index': n, 'actual_execution_pending': True} for n in (3, 4)])
    except Exception as error:
        report['error'] = repr(error)
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        inputs.write_json(output / 'result.json', report)
    print(json.dumps({key: report.get(key) for key in ('passed', 'status', 'pipeline_commands_verified', 'harness_commands_verified', 'real_streams_verified', 'error')}, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
