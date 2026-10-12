#!/usr/bin/env python3
"""Freeze completed neutral compilation and review the exact indicator delta."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import stat

BASE = Path('/dev/shm/macrodroid-day-numeric-art')


def identity(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns), str(path)
    return {'bytes': b.st_size, 'sha256': digest, 'mode': stat.S_IMODE(b.st_mode)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def copy(source, target):
    expected = identity(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open('rb') as reader, target.open('xb') as writer:
        shutil.copyfileobj(reader, writer)
    target.chmod(expected['mode'])
    assert identity(target) == expected and identity(source) == expected


def freeze(root, extra):
    rows = [{'path': path.relative_to(root).as_posix(), **identity(path)}
            for path in sorted(root.rglob('*')) if path.is_file()]
    value = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
             **extra, 'payload_count': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows), 'files': rows}
    save(root / 'checkpoint.json', value)
    print(json.dumps({'checkpoint': str(root / 'checkpoint.json'), **identity(root / 'checkpoint.json'),
                      'payload_count': len(rows), 'payload_bytes': value['payload_bytes']}))


def close_compilation():
    source = BASE / 'compile-01'
    out = BASE / 'checkpoints/02-compiled-probe-and-corpus'
    out.mkdir(parents=True, exist_ok=False)
    copy(Path(__file__), out / 'executed-freezer.py')
    before = {str(p): identity(p) for p in sorted(source.rglob('*')) if p.is_file()}
    result = json.loads((source / 'result.json').read_bytes())
    assert result['passed'] is True and result['corpus_cases'] == 1291
    assert result['probe_compiled'] is True and result['all_read_inputs_unchanged'] is True
    for key in ('android_executed', 'application_build_executed', 'probe_runtime_executed', 'full_runtime_1_to_1_established'):
        assert result[key] is False
    assert result['inventory_only_jvm_execution'] is True
    assert [row['label'] for row in result['commands']] == ['java-version', 'javac-version', 'neutral-probe-javac', 'inventory-only-jvm', 'neutral-probe-d8']
    for command in result['commands']:
        assert type(command['returncode']) is int and command['returncode'] == 0 and command['timed_out'] is False
        for channel in ('stdout', 'stderr'):
            assert identity(source / 'commands' / command['label'] / (channel + '.txt')) == command[channel]
    assert (source / 'inputs-before.json').read_bytes() == (source / 'inputs-after.json').read_bytes()
    assert identity(source / 'dex/classes.dex') == {'bytes': 14108, 'sha256': '7cf6f31793b1f0546bf4927a63481a25662634b8a0ac2fa520a69900204ed3aa', 'mode': 420}
    for path in sorted(source.rglob('*')):
        if path.is_file():
            copy(path, out / 'evidence' / path.relative_to(source))
    parent = BASE / 'source-draft-02/checkpoint.json'
    assert identity(parent)['sha256'] == '707afe796307be6044a5571cc39d4480ec032d2bf3d0ad87eb9a75118959deda'
    copy(parent, out / 'source-design-checkpoint.json')
    copy(BASE / 'source-draft-02/protocol.json', out / 'source-design-protocol.json')
    after = {name: identity(Path(name)) for name in before}
    assert before == after
    save(out / 'closure-inputs-before.json', before)
    save(out / 'closure-inputs-after.json', after)
    (out / 'README.md').write_text('''# Compiled neutral numeric probe and complete input inventory

The exact neutral Java source `ab5b1b1d01ab33f66cab22c1d5a5f7c09ffdf13b8e0e335cf22f86ba5fcc6c2b` compiled successfully into one class and one DEX. The DEX is 14,108 bytes, SHA256 `7cf6f31793b1f0546bf4927a63481a25662634b8a0ac2fa520a69900204ed3aa`. Its only class is `Lrecovered/probe/DayNumericMethodProbe;`; all typed references are Java, that probe, primitive/array types or the two standard Dalvik annotations. No application or Android class definition is present.

The retained five actual commands observed Java and javac, compiled with Java 8 bytecode semantics, ran only the host input-inventory branch with verification enabled, and converted the single class with the pinned D8 compiler. Every command exited zero within its existing 30- or 120-second bound. The Java 8 compilation warning remains verbatim in stderr. No application APK was built or executed.

The host inventory emitted all 1,291 original cases in their original order. Independent Python integer-only arithmetic agreed with every Java expectation. The original compact input SHA256 remains `e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79`. Counts are 547 integer, 734 decimal and ten other inputs, including a null entry and two explicitly declared reflective invalid-heap states. The protocol/source-design capsule documents those states and the exact original method scope.

This is a neutral-probe compilation and input-corpus result. The host inventory does not load application classes. Neither APK, the actual target method, Android ART, the emulator, UI nor alarms were exercised here. Android execution and its bounded wrapper/workflow review remain pending. The historical source-design capsule retains its original uncompiled status; this successor records the later actual compilation without rewriting that history.

`evidence/` preserves the executed compiler, Java source and class, DEX, full literal stdout/stderr and command metadata, both input inventories, toolchain release metadata and all 1,291 independent expectations. Read-only closure rechecked the five commands and raw-stream identities. All source and output inputs remained unchanged through closure.
''')
    freeze(out, {'status': 'CLOSED_NEUTRAL_PROBE_COMPILATION_AND_1291_INPUTS_NO_ANDROID',
                 'repo_target': 'work-in-progress/day-numeric-art/02-compiled-probe-and-corpus',
                 'source_design_checkpoint_sha256': identity(parent)['sha256'],
                 'active_files': [], 'probe_compiled': True, 'input_cases': 1291,
                 'android_executed': False, 'application_build_executed': False,
                 'probe_runtime_executed': False, 'all_read_inputs_unchanged': True})


def indicator_review():
    source = Path('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/03-closed-synthetic-test-correction')
    previous = source.parent / '02-implemented-offline-validated'
    review = Path('/dev/shm/macrodroid-indicator-implementation-independent-review')
    out = Path('/dev/shm/macrodroid-indicator-final-root-review/review-01')
    out.mkdir(parents=True, exist_ok=False)
    copy(Path(__file__), out / 'executed-reviewer.py')
    before = {}
    def inspect(path):
        row = identity(path)
        before[str(path)] = row
        return row
    assert inspect(source / 'checkpoint.json')['sha256'] == '89064abe581191cd0690eda4e739a91a9b5bae3c56cb9156533ddd78a857f7be'
    assert inspect(review / 'checkpoint.json')['sha256'] == '3a781f2b91b06f2d7884f47030fcd30ec3601bf93ef09534571a178e7412456b'
    reviewed = json.loads((review / 'checkpoint.json').read_bytes())
    assert reviewed['review_passed'] is True and reviewed['blockers'] == []
    assert reviewed['reviewed_source_checkpoint_sha256'] == before[str(source / 'checkpoint.json')]['sha256']
    for row in reviewed['files']:
        actual = inspect(review / row['path'])
        assert {k: actual[k] for k in ('bytes', 'sha256')} == {k: row[k] for k in ('bytes', 'sha256')}
        assert actual['mode'] == (493 if row['mode'] == '100755' else 420)
    listing = source / 'proposed-source-files.json'; inspect(listing)
    rows = json.loads(listing.read_bytes())
    assert len(rows) == 16 and len({row['target'] for row in rows}) == 16
    assert sorted(p.relative_to(source / 'source').as_posix() for p in (source / 'source').rglob('*') if p.is_file()) == sorted(row['target'] for row in rows)
    changed = []
    for row in rows:
        actual = inspect(source / row['source'])
        assert {k: actual[k] for k in ('bytes', 'sha256')} == {k: row[k] for k in ('bytes', 'sha256')}
        assert actual['mode'] == (493 if row['mode'] == '100755' else 420)
        old = inspect(previous / row['source'])
        if old != actual:
            changed.append(row['target'])
    assert sorted(changed) == ['.github/workflows/indicator-fixed-sampling.yml', 'tools/indicator_sampling/runtime-files.json', 'tools/indicator_sampling/test_indicator_sampling.py']
    runtime = json.loads((source / 'source/tools/indicator_sampling/runtime-files.json').read_bytes())
    assert runtime == [{k: row['target'] if k == 'path' else row[k] for k in ('path', 'bytes', 'sha256')} for row in rows if row['target'] != 'tools/indicator_sampling/runtime-files.json']
    workflow = (source / 'source/.github/workflows/indicator-fixed-sampling.yml').read_text()
    for literal in ['timeout-minutes: 150', 'timeout 900s python3 -B -m unittest', '--timeout 900 --', 'for indicator_slot in 1 2 3 4 5 6 7 8', 'include-hidden-files: true', 'cancel-in-progress: false', "ref: 6331410cfd2391389270564803623079e8355ad8", 'trap cleanup_indicator_runtime EXIT']:
        assert literal in workflow, literal
    result = json.loads((review / 'attempt-02/result.json').read_bytes())
    assert result['concrete_blockers_found'] == [] and result['distinct_passed_test_bodies'] == 41
    assert result['fresh_full_suite_executed'] is False and result['independent_synthetic_pair_checks'] == 92
    for src, dst in [(source / 'checkpoint.json', 'implementation-checkpoint.json'), (review / 'checkpoint.json', 'independent-review-checkpoint.json'), (listing, 'proposed-source-files.json'), (source / 'source-delta.patch', 'source-delta.patch'), (source / 'closed-results.json', 'closed-results.json'), (review / 'attempt-02/result.json', 'independent-result.json'), (source / 'source/.github/workflows/indicator-fixed-sampling.yml', 'reviewed-workflow.yml')]:
        inspect(src); copy(src, out / dst)
    after = {name: identity(Path(name)) for name in before}
    assert before == after
    save(out / 'inputs-before.json', before); save(out / 'inputs-after.json', after)
    save(out / 'result.json', {'status': 'ROOT_FINAL_INDICATOR_ACTIVATION_REVIEW_PASSED',
          'source_paths': 16, 'review_payloads_rehashed': len(reviewed['files']),
          'changed_from_implemented_parent': changed, 'runtime_manifest_rows': len(runtime),
          'independent_review_no_blocker': True, 'all_read_inputs_unchanged': True,
          'android_executed': False, 'new_suite_executed': False, 'new_runtime_parity_credit': 0,
          'activation_scope': 'Only the exact sixteen paths after both implementation and reviews are fetched and verified; one automatic eight-install diagnostic; no app/APK/source promotion.'})
    (out / 'README.md').write_text('''# Root final indicator activation review

The root reviewed the complete final workflow, exact three-path correction, literal full/focused outcomes and independent implementation assessment. It independently rehashed all thirty peer-review payloads and all sixteen final source roles, checked the complete source-path set, compared every role with the implemented parent, and verified the fifteen runtime-manifest rows. All read inputs remained unchanged.

The workflow retains the mandatory full 41-control host discovery, exact immutable parent checkout, both fixed APKs, the A-then-B eight-install schedule, finite queue/slot/experiment bounds, owned runtime cleanup and complete partial-evidence upload. Its sole test change corrects an expected rejection string. The existing full run remains 40 passing / 1 failed, with the focused corrected test passing separately. No fresh full-suite result or Android behavior is invented.

The independent reviewer checked all 3,660 payload rows across five capsules and all 92 deliberately unequal synthetic pixel/XML pairs. That report, the exact implementation and this final review must be committed, pushed and fetched with matching bytes/modes before activating only the sixteen declared paths. Root finds no blocking issue for that exact diagnostic activation. The experiment retains original APK 84333011 and older candidate 5f635e16 to preserve the fixed study inputs. It grants no app promotion, runtime parity or causality credit. Actual Android evidence remains pending.
''')
    freeze(out, {'status': 'CLOSED_ROOT_FINAL_INDICATOR_ACTIVATION_REVIEW',
                 'repo_target': 'docs/verification/indicator-fixed-sampling/root-final-activation-review',
                 'source_checkpoint_sha256': before[str(source / 'checkpoint.json')]['sha256'],
                 'independent_review_checkpoint_sha256': before[str(review / 'checkpoint.json')]['sha256'],
                 'eligible_source_paths': 16, 'active_files': [], 'android_executed': False,
                 'new_suite_executed': False, 'all_read_inputs_unchanged': True})


if __name__ == '__main__':
    close_compilation()
    indicator_review()
