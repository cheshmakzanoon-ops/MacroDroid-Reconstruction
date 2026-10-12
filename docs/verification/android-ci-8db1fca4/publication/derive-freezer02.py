"""Preserve a publisher-only assertion failure and derive its exact-step successor."""
from pathlib import Path
import difflib
import hashlib
import json
import stat
import subprocess
import sys

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
OLD = ROOT / 'freeze_active_numeric_android_raw.py'
NEW = ROOT / 'freeze_active_numeric_android_raw02.py'
PARTIAL = ROOT / 'active-numeric-android-raw-capsule'
ATTEMPT = ROOT / 'active-numeric-android-freezer-attempt-01'
ATTEMPT.mkdir(exist_ok=False)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
    path.chmod(0o644)

def save(name, value):
    write(ATTEMPT / name, (json.dumps(value, indent=2) + '\n').encode())

old = OLD.read_bytes()
text = old.decode('utf-8')
assert text.count("OUTPUT = ROOT / 'active-numeric-android-raw-capsule'") == 1
bad = "assert any('Upload' in row['name'] and row['conclusion'] == 'success' for row in android['steps'])"
assert text.count(bad) == 1
write(ATTEMPT / 'executed-freezer.py', old)
rows = []
for path in sorted(PARTIAL.rglob('*')):
    if path.is_dir():
        continue
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode)
    raw = path.read_bytes()
    rows.append(dict(path=str(path.relative_to(PARTIAL)), bytes=len(raw),
                     sha256=digest(raw), mode=stat.S_IMODE(info.st_mode)))
save('partial-output-inventory.json', dict(root=str(PARTIAL), files=rows,
     mutation=False, original_checkpoint_present=(PARTIAL / 'checkpoint.json').exists()))

replay = ("from pathlib import Path\nimport json\n"
          "jobs=json.loads(Path(" + repr(str(ROOT / 'active-numeric-android-run-38247941263/github-jobs.json')) + ").read_bytes())['jobs']\n"
          "android=next(job for job in jobs if job['id']==114806467130)\n"
          + bad + '\n')
write(ATTEMPT / 'replay-failed-assertion.py', replay.encode())
result = subprocess.run([sys.executable, '-B', str(ATTEMPT / 'replay-failed-assertion.py')],
                        capture_output=True, check=False, timeout=10)
write(ATTEMPT / 'replay.stdout', result.stdout)
write(ATTEMPT / 'replay.stderr', result.stderr)
assert result.returncode == 1 and b'AssertionError' in result.stderr and not result.stdout
jobs = json.loads((ROOT / 'active-numeric-android-run-38247941263/github-jobs.json').read_bytes())['jobs']
android = next(job for job in jobs if job['id'] == 114806467130)
step = next(row for row in android['steps'] if row['number'] == 9)
assert step['name'] == 'Preserve measured runtime outcomes, including failures'
assert step['status'] == 'completed' and step['conclusion'] == 'success'
save('result.json', dict(status='PUBLISHER_ASSERTION_FAILURE_REPRODUCED',
     original_full_attempt=dict(exit_code=1, source_sha256=digest(old), line=85,
          exception='AssertionError', complete_raw_stderr_saved=False,
          statement='The original full invocation failed before producing a checkpoint; its complete stderr was not saved to a file.'),
     focused_replay=dict(argv=[sys.executable, '-B', str(ATTEMPT / 'replay-failed-assertion.py')],
          exit_code=result.returncode, stdout_sha256=digest(result.stdout), stderr_sha256=digest(result.stderr)),
     observed_successful_upload_step=step, raw_artifact_mutations=[], application_failure_claim=False))
write(ATTEMPT / 'README.md', b'''# Publisher-only raw-freezer assertion failure

The first full freezer stopped at line 85 because it searched for the literal substring `Upload` in a successful job step name. The actual successful step 9 is named `Preserve measured runtime outcomes, including failures`. Its source and complete partial-output inventory are retained here. The full first invocation's stderr was displayed by the execution tool but was not saved as a raw file; no reconstructed full stderr is presented.

The separate, executed focused replay retains its own actual stdout, stderr and exit code and reproduces the same assertion failure against the unchanged job metadata. The successor binds the exact observed step name, number, completion and success. This is a publication metadata correction; no raw member, application code, acceptance rule or Android outcome changes.
''')

fixed = text.replace("OUTPUT = ROOT / 'active-numeric-android-raw-capsule'",
                     "OUTPUT = ROOT / 'active-numeric-android-raw-capsule-02'")
fixed = fixed.replace(bad,
    "assert steps[9]['name'] == 'Preserve measured runtime outcomes, including failures'\n"
    "assert steps[9]['status'] == 'completed' and steps[9]['conclusion'] == 'success'")
addition = '''copy(ROOT / 'derive_active_numeric_android_raw_freezer02.py', 'publication/derive-freezer02.py')
for failed_path in sorted((ROOT / 'active-numeric-android-freezer-attempt-01').iterdir()):
    copy(failed_path, 'publication/attempt-01/' + failed_path.name)
copy(ROOT / 'active-numeric-android-freezer02.patch', 'publication/freezer02.patch')
'''
assert fixed.count('files = []\n') == 1
fixed = fixed.replace('files = []\n', addition + 'files = []\n')
write(NEW, fixed.encode())
patch = ''.join(difflib.unified_diff(text.splitlines(True), fixed.splitlines(True),
                                   fromfile='attempt-01/freezer.py', tofile='attempt-02/freezer.py'))
write(ROOT / 'active-numeric-android-freezer02.patch', patch.encode())
assert OLD.read_bytes() == old
for row in rows:
    path = PARTIAL / row['path']
    raw = path.read_bytes()
    assert len(raw) == row['bytes'] and digest(raw) == row['sha256']
print(json.dumps(dict(status='DERIVED_WITH_EXACT_METADATA_CORRECTION',
     old_source_sha256=digest(old), new_source_sha256=digest(NEW.read_bytes()),
     partial_files_unchanged=len(rows), focused_replay_exit_code=result.returncode,
     next_freezer=str(NEW))))
