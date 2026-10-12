#!/usr/bin/env python3
"""Pin preserved intro drawing code and previously measured roundtrip evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


TARGETS = [
    'Lagency/tango/materialintroscreen/widgets/InkPageIndicator;',
    'Lagency/tango/materialintroscreen/MaterialIntroActivity;',
    'Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;',
    'Liz7;', 'Lmz7;', 'Lnz7;', 'Lx82;', 'Loz7;', 'Ljz7;', 'Los5;',
    'Lkz7;', 'Llz7;', 'Lv6;', 'Lcom/arlosoft/macrodroid/intro/IntroActivity;',
    'Lxdh;', 'Libg;', 'Ljc;', 'Lf13;',
]
ACTIVE_APK = '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--hosted-reports', type=Path, required=True)
    parser.add_argument('--combined-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.source, args.hosted_reports, args.combined_source, args.output = [p.resolve() for p in (
        args.source, args.hosted_reports, args.combined_source, args.output)]
    args.output.mkdir(parents=True, exist_ok=False)
    files = []
    def save(source, relative):
        expected = identity(source)
        destination = args.output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if identity(source) != expected or identity(destination) != expected:
            raise RuntimeError('Read-only source changed during capture: ' + str(source))
        files.append({'path': relative, **expected})
        return expected
    index_path = args.source / 'source/class-index.json'
    registry_path = args.source / 'source/java-method-map.json'
    index = json.loads(index_path.read_text())
    registry = json.loads(registry_path.read_text())
    before = {'index': identity(index_path), 'registry': identity(registry_path)}
    active = json.loads((args.hosted_reports / 'hybrid-roundtrip.json').read_text())
    if (active['apk_sha256'] != ACTIVE_APK or active['pass'] is not True
            or active['classes_compared'] != 71267 or active['methods_total'] != 349972
            or active['unexpected_changed_methods'] or active['baseline_source_hash_mismatches']):
        raise RuntimeError('Unexpected previously measured active APK roundtrip evidence')
    save(args.hosted_reports / 'hybrid-roundtrip.json', 'evidence/active-hosted-hybrid-roundtrip.json')
    save(args.hosted_reports / 'hybrid-resource-parity.json', 'evidence/active-hosted-hybrid-resource-parity.json')
    combined = {}
    for variant in ('baseline', 'hybrid'):
        report = json.loads((args.combined_source / 'reports' / (variant + '-roundtrip.json')).read_text())
        if not report['pass']:
            raise RuntimeError('Combined roundtrip gate has not passed')
        combined[variant] = report
        save(args.combined_source / 'reports' / (variant + '-roundtrip.json'),
             'evidence/inactive-combined-' + variant + '-roundtrip.json')
    rows = []
    for target in TARGETS:
        matches = [row for row in index.values() if row['descriptor'] == target]
        if len(matches) != 1:
            raise RuntimeError('Missing or ambiguous focused class: ' + target)
        item = matches[0]
        path = args.source / item['path']
        if identity(path)['sha256'] != item['sha256']:
            raise RuntimeError('Preserved source differs from its class index: ' + target)
        registered = [row['method'] for row in registry if row['target'] == target]
        active_changes = [row[1] for row in active['changed_methods'] if row[0] == target]
        if registered or active_changes:
            raise RuntimeError('Focused class contains a registered or measured changed method: ' + target)
        captured = save(path, 'preserved-source/' + item['path'])
        row = {'descriptor': target, 'partition': item['partition'], 'methods': item['methods'],
               'source_path': item['path'], **captured, 'registered_methods': registered,
               'active_apk_changed_methods': active_changes, 'combined_disassembly_equal': {}}
        for variant in ('baseline', 'hybrid'):
            compiled = args.combined_source / 'build' / ('verify-' + variant) / item['partition'] / (target[1:-1] + '.smali')
            # Reuse closed disassembly gates from this still-running acceptance
            # project read-only; do not compile, remove, or alter its caches.
            if compiled.read_bytes() != path.read_bytes():
                raise RuntimeError('Focused combined disassembly text differs: ' + target + ' ' + variant)
            row['combined_disassembly_equal'][variant] = identity(compiled)
        rows.append(row)
    for relative in ['source/android/res/layout/activity_material_intro.xml',
                     'reference/java/sources/com/arlosoft/macrodroid/intro/IntroActivity.java',
                     'reference/java/sources/com/arlosoft/macrodroid/intro/a.java', 'build.py']:
        save(args.source / relative, 'context/' + relative)
    after = {'index': identity(index_path), 'registry': identity(registry_path)}
    if before != after:
        raise RuntimeError('Source registry changed during audit')
    result = {
        'status': 'FOCUSED_PRESERVED_SOURCE_AUDIT_PASSED',
        'scope': '18 specified intro/dot-rendering classes, source identity and prior code-roundtrip evidence only',
        'android_executed_during_audit': False, 'new_build_executed': False,
        'rendering_difference_cause_established': False, 'pixel_comparison_rule_changed': False,
        'full_runtime_1_to_1_established': False, 'active_apk_sha256': ACTIVE_APK,
        'previous_active_hosted_run': 38202401393, 'active_hosted_commit': 'cada56c8',
        'registry_count': len(registry), 'index_identity': before['index'], 'registry_identity': before['registry'],
        'classes': rows, 'combined_apks': {v: r['apk_sha256'] for v, r in combined.items()},
        'static_observations': [
            'The indicator layout sets animationDuration=320, dotDiameter=8dp and dotGap=8dp.',
            'setSelectedPage creates a main ValueAnimator and threshold-triggered retreat/reveal subanimators.',
            'The main value-update branch writes w, triggers the threshold animator and posts an animation invalidation.',
            'The iz7 variant-zero end callback resets indicator arrays/retreat bounds through f(), then clears E; it contains no explicit invalidate call.',
            'IntroActivity adds xdh, ibg, jc and f13 as the four normal slides; all are outside the Java replacement registry.',
            'The separate manufacturer-specific intro/a.o() constant migration is not in these 18 classes.',
        ],
        'inference_limit': 'The callback structure motivates a separately declared animation-scale diagnostic. It does not prove animation scheduling or any other specific cause of the 26-pixel result.',
        'finished_utc': datetime.now(timezone.utc).isoformat(),
    }
    output = args.output / 'result.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    files.append({'path': 'result.json', **identity(output)})
    save(Path(__file__).resolve(), 'audit_preserved_source.py')
    manifest = args.output / 'checkpoint.json'
    manifest.write_text(json.dumps({'scope': result['scope'], 'files': sorted(files, key=lambda row: row['path'])}, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'classes': len(rows), 'checkpoint': str(manifest), **identity(manifest)}, indent=2))


if __name__ == '__main__':
    main()
