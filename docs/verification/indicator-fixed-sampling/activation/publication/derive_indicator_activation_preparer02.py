"""Resolve the diagnostic's actual immutable manifest indirection."""
from pathlib import Path
import difflib
import hashlib
import json

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
OLD = ROOT / 'prepare_indicator_fixed_sampling_activation.py'
NEW = ROOT / 'prepare_indicator_fixed_sampling_activation02.py'
ATTEMPT = ROOT / 'indicator-activation-preparer-attempt-01'
ATTEMPT.mkdir(exist_ok=False)
old = OLD.read_bytes()
source = old.decode()

def write(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
    path.chmod(0o644)

write(ATTEMPT / 'executed-preparer.py', old)
observed = '''Traceback (most recent call last):
  File "/dev/shm/macrodroid-transfer-space-20261012/prepare_indicator_fixed_sampling_activation.py", line 124, in <module>
    assert b'5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182' in pins
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
'''
write(ATTEMPT / 'observed-execution-output.txt', observed.encode())
write(ATTEMPT / 'result.json', (json.dumps(dict(status='PUBLISHER_MANIFEST_INDIRECTION_ASSERTION_FAILURE',
    exit_code=1, source_sha256=hashlib.sha256(old).hexdigest(),
    output_provenance='Literal combined execution output retained from write_stdin session 30118.',
    explanation='The publisher expected the whole APK digest literally inside pins.json; the frozen diagnostic instead pins the complete APK manifest at an immutable parent commit.',
    active_paths_changed=False, remote_ref_changed=False, diagnostic_source_changed=False,
    export_directory_created=(ROOT/'indicator-fixed-sampling-activation-export').exists()), indent=2)+'\n').encode())
bad = "assert b'5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182' in pins\nassert b'0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd' not in pins"
assert source.count(bad) == 1
good = '''pin_object = json.loads(pins)
assert pin_object['parent_commit'] == '6331410cfd2391389270564803623079e8355ad8'
parent_rows = {row['path']: row for row in pin_object['parents']}
assert len(parent_rows) == len(pin_object['parents']) == 16

def pinned_manifest(name, expected_digest):
    row = parent_rows[name]
    assert row['sha256'] == expected_digest and git_mode(row['mode']) == '100644'
    raw = git('show', pin_object['parent_commit'] + ':' + name)
    assert len(raw) == row['bytes'] and sha(raw) == expected_digest
    assert fetched(name) == raw
    return json.loads(raw)

diagnostic_manifest = pinned_manifest(
    'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
    '459960a6afc81fc0119cd66f3a9f6be823f7947ae90cd74c902d1a8a1e010afc')
original_manifest = pinned_manifest('vendor/original/manifest.json',
    'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684')
assert diagnostic_manifest['sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
assert diagnostic_manifest['size_bytes'] == 94683119
assert original_manifest['size_bytes'] == 95725918
assert json.loads(fetched('artifacts/current/manifest.json'))['sha256'] == '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd' '''.rstrip()
new = source.replace(bad, good).replace("EXPORT = ROOT / 'indicator-fixed-sampling-activation-export'",
                                         "EXPORT = ROOT / 'indicator-fixed-sampling-activation-export-02'")
assert new != source
write(NEW, new.encode())
write(ROOT / 'indicator-activation-preparer02.patch', ''.join(difflib.unified_diff(
    source.splitlines(True), new.splitlines(True), fromfile='attempt-01/preparer.py',
    tofile='attempt-02/preparer.py')).encode())
assert OLD.read_bytes() == old
print(json.dumps(dict(status='EXACT_INDIRECT_MANIFEST_GUARD_DERIVED',
    old_source_sha256=hashlib.sha256(old).hexdigest(),
    new_source_sha256=hashlib.sha256(NEW.read_bytes()).hexdigest(),
    active_or_diagnostic_source_changed=False)))
