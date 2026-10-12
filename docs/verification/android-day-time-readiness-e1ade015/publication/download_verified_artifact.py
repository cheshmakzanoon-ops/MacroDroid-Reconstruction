"""Download one authorized artifact to a new file and verify its pinned identity."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--url-file', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--bytes', type=int, required=True)
p.add_argument('--sha256', required=True)
p.add_argument('--artifact-id', type=int, required=True)
p.add_argument('--run-id', type=int, required=True)
a = p.parse_args()
url = a.url_file.read_text().strip()
a.url_file.unlink()
a.output.parent.mkdir(parents=True, exist_ok=True)
digest, count = hashlib.sha256(), 0
started = datetime.now(timezone.utc).isoformat()
with urllib.request.urlopen(url, timeout=60) as response, a.output.open('xb') as stream:
    while chunk := response.read(1024 * 1024):
        count += len(chunk)
        assert count <= a.bytes
        digest.update(chunk)
        stream.write(chunk)
assert count == a.bytes and digest.hexdigest() == a.sha256
with a.output.open('rb') as stream:
    assert hashlib.file_digest(stream, 'sha256').hexdigest() == a.sha256
result = {'schema': 1, 'status': 'EXACT_GITHUB_ARTIFACT_DOWNLOADED_AND_REHASHED',
          'artifact_id': a.artifact_id, 'run_id': a.run_id, 'archive': a.output.name,
          'bytes': count, 'sha256': digest.hexdigest(), 'started_utc': started,
          'completed_utc': datetime.now(timezone.utc).isoformat(),
          'temporary_download_url_persisted_in_evidence': False}
a.output.with_name(a.output.name + '.download.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
