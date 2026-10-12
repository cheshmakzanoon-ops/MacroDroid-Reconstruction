#!/usr/bin/env python3
"""Check the inactive integration against an existing compiled migration set.

Reads the source and generated helpers without changing either. Its reports go
to a new output directory. This is host static evidence, not Android execution.
"""
import argparse
import contextlib
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'integration/project'))
import build
import linkage_verify
import validate_migration
from constructor_owner import restore_from_preserved_source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--compiled', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, compiled, out = (path.resolve() for path in (args.source, args.compiled, args.output))
    out.mkdir(parents=True, exist_ok=False)
    build.ROOT, build.WORK, build.REPORTS = root, compiled, out
    registry = json.loads((root / 'source/java-method-map.json').read_text())
    index = build.index()
    by = {item['descriptor']: item for item in index.values()}
    originals, helpers = {}, {}
    checked = 0
    for entry in registry:
        if entry.get('constructor_owner_mappings') is not None:
            raise ValueError('Existing-set inertness check requires an unmapped registry')
        target, helper = entry['target'], entry['helper']
        if target not in originals:
            originals[target] = build.methods((root / by[target]['path']).read_text())
        if helper not in helpers:
            helpers[helper] = build.methods((compiled / 'java/smali' / (helper[1:-1] + '.smali')).read_text())
        suffix = entry['method'][entry['method'].index('('):]
        signature = entry.get('helper_descriptor', entry['helper_method'] + '(' + (target if entry['instance'] else '') + suffix[1:])
        before = helpers[helper][signature]
        after, proofs = restore_from_preserved_source(entry, before, originals[target][entry['method']], index, root)
        if after != before or proofs:
            raise ValueError('An unconfigured existing migration changed: ' + target + '->' + entry['method'])
        checked += 1
    with (out / 'static-console.log').open('w') as stream, contextlib.redirect_stdout(stream):
        static = validate_migration.verify()
        linkage = linkage_verify.verify()
    if not static['pass'] or not linkage['pass']:
        raise ValueError('An existing static gate failed')
    report = {'scope': 'Inactive constructor integration against unchanged existing migration helpers',
              'pass': True, 'android_executed': False, 'existing_methods_unchanged': checked,
              'new_constructor_corrections': 0, 'application_apk_modified': False,
              'source_input_snapshot_sha256': json.loads((root / 'reports/release-input-snapshot.json').read_text())['snapshot_sha256'],
              'migration_static_report_sha256': sha(out / 'migration-static-proof.json'),
              'migration_linkage_report_sha256': sha(out / 'migration-linkage-check.json'),
              'integration_files': {name: sha(HERE / 'integration/project' / name)
                                    for name in ['build.py', 'constructor_owner.py', 'validate_migration.py', 'linkage_verify.py']}}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
