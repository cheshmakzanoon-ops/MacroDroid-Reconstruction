from pathlib import Path
import json
jobs=json.loads(Path('/dev/shm/macrodroid-transfer-space-20261012/active-numeric-android-run-38247941263/github-jobs.json').read_bytes())['jobs']
android=next(job for job in jobs if job['id']==114806467130)
assert any('Upload' in row['name'] and row['conclusion'] == 'success' for row in android['steps'])
