#!/usr/bin/env python3
"""Create the immutable review pins for one closed, private accounting proposal."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAPSULES = {
    'three_path': ('14-method-only-three-path-retry-delay', '5174cc11e51cc333f7b75042259aee15cf4cf5ff666eb733730351ef31d7e278'),
    'cases': ('13-retry-delay-original-jvm-coverage-gap', '02f80d76ee2fcf9d9cacf38f4b8d0fdd9c8697934daa190aa9c3450ab7cfc6ac'),
    'host': ('02-draft-compile', '38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea'),
    'dataflow': ('04-handler-dataflow-review', '053ee22c427813258cc64f7363c150353ce1f5bbc8118aa12dbb9af049b8e754'),
    'proof': ('04b-pinned-handler-proof-guards', 'aade36da986f9fd683577caed650ce2a2a8b24008a92e4194931ed1ac7af0255')}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    roots = {}; files = {}
    for name, (directory, digest) in CAPSULES.items():
        root = HERE / 'checkpoints' / directory
        if sha(root / 'checkpoint.json') != digest:
            raise RuntimeError('Expected reviewed frozen checkpoint differs: ' + name)
        manifest = json.loads((root / 'checkpoint.json').read_text())
        for rows, prefix in [(manifest['files'], ''), (manifest['evidence_files'], 'evidence/')]:
            for row in rows:
                path = root / (prefix + row['path'])
                if path.is_symlink() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
                    raise RuntimeError('Frozen payload differs')
                files[name + '/' + prefix + row['path']] = row['sha256']
        roots[name] = root
    run = roots['three_path'] / 'evidence/run'
    result = json.loads((run / 'result.json').read_text())
    if result['status'] != 'THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED':
        raise RuntimeError('Closed semantic proof prerequisite differs')
    value = {'schema': 'closed-video-accounting-proposal-1',
        'scope': 'Exactly frozen study14 and reviewed original handler proof04/04b. Review-only proposal; no active policy or generic offset exception.',
        'checkpoints': {name: {'directory': directory, 'sha256': digest} for name, (directory, digest) in CAPSULES.items()},
        'all_frozen_file_hashes': files,
        'method': 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;',
        'original_static_offsets': [232, 233, 235],
        'cases': 1125, 'independent_expected_checks': 237,
        'class_origins': json.loads((run / 'positive/class-origins.json').read_text()),
        'runtime': json.loads((run / 'positive/live-runtime/before/runtime.json').read_text()),
        'jdk_inputs': result['jdk_inputs'],
        'method_binding': json.loads((run / 'method-body-binding.json').read_text())}
    path = HERE / 'private_accounting_pins.json'
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')
    print(json.dumps({'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path),
                      'frozen_files_pinned': len(files)}, indent=2))


if __name__ == '__main__':
    main()
