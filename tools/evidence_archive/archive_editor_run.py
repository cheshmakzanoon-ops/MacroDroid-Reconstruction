#!/usr/bin/env python3
"""Archive one completed, same-repository main-branch editor run without executing it.
The exact artifact ZIP and extracted JSON summaries are data only. Tokens are sent
only to api.github.com; signed storage downloads use a separate unauthenticated request.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPOSITORY = 'cheshmakzanoon-ops/MacroDroid-Reconstruction'
REPOSITORY_ID = 1414876481
MAX_ARCHIVE = 64 * 1024 * 1024
MAX_EXPANDED = 256 * 1024 * 1024

class ArchiveError(ValueError):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def bounded_read(stream, limit):
    data = stream.read(limit + 1)
    if len(data) > limit:
        raise ArchiveError('Response exceeds the allowed size')
    return data


def api(path, token):
    req = urllib.request.Request('https://api.github.com/repos/' + REPOSITORY + path,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2026-03-10'})
    return urllib.request.build_opener(NoRedirect).open(req, timeout=60)


def api_json(path, token):
    with api(path, token) as response:
        return json.loads(bounded_read(response, 8 * 1024 * 1024))


def validate_run(run):
    if (run.get('repository', {}).get('id') != REPOSITORY_ID
        or run.get('head_repository', {}).get('id') != REPOSITORY_ID
        or run.get('head_branch') != 'main'
        or run.get('event') not in ('push', 'workflow_dispatch')
        or run.get('path') not in ('.github/workflows/editor-journey.yml', '.github/workflows/editor-session.yml')
        or run.get('status') != 'completed'
        or type(run.get('id')) is not int or run['id'] <= 0
        or type(run.get('run_attempt')) is not int or run['run_attempt'] <= 0
        or not re.fullmatch('[0-9a-f]{40}', run.get('head_sha', ''))):
        raise ArchiveError('Only completed, trusted main-branch editor runs may be archived')


def validate_zip(data, digest):
    if not re.fullmatch('sha256:[0-9a-f]{64}', digest or ''):
        raise ArchiveError('Artifact digest is missing')
    if len(data) > MAX_ARCHIVE or 'sha256:' + hashlib.sha256(data).hexdigest() != digest:
        raise ArchiveError('Artifact bytes differ from GitHub metadata')
    members = []
    seen = set()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        if len(infos) > 20000 or sum(i.file_size for i in infos) > MAX_EXPANDED:
            raise ArchiveError('Archive expansion exceeds the bounded evidence allowance')
        for entry in infos:
            path = PurePosixPath(entry.filename)
            mode = entry.external_attr >> 16
            if (path.is_absolute() or '..' in path.parts or '\\' in entry.filename
                or entry.filename in seen or stat.S_ISLNK(mode) or '\x00' in entry.filename
                or not entry.filename.startswith(('ci-editor/', 'tools/parity_journeys/'))):
                raise ArchiveError('Unexpected artifact member')
            seen.add(entry.filename)
            if entry.is_dir():
                continue
            if entry.file_size > 32 * 1024 * 1024:
                raise ArchiveError('Evidence member is too large')
            contents = archive.read(entry)  # ZIP CRC is checked here.
            members.append({'path': entry.filename, 'bytes': len(contents),
                            'sha256': hashlib.sha256(contents).hexdigest()})
    return members


def download_artifact(artifact_id, token):
    try:
        with api(f'/actions/artifacts/{artifact_id}/zip', token):
            raise ArchiveError('Expected the documented artifact redirect')
    except urllib.error.HTTPError as exc:
        if exc.code != 302:
            raise ArchiveError(f'Artifact API returned HTTP {exc.code}') from None
        location = exc.headers.get('Location', '')
    target = urllib.parse.urlsplit(location)
    if (target.scheme != 'https' or not target.hostname or target.username or target.password
        or not target.hostname.endswith(('.blob.core.windows.net', '.githubusercontent.com'))):
        raise ArchiveError('Unexpected signed artifact storage host')
    # No Authorization header is copied to the storage request, nor are URL tokens logged.
    request = urllib.request.Request(location)
    with urllib.request.build_opener(NoRedirect).open(request, timeout=120) as response:
        return bounded_read(response, MAX_ARCHIVE)


def archive_run(run_id, token):
    run = api_json(f'/actions/runs/{run_id}', token)
    validate_run(run)
    artifacts = api_json(f'/actions/runs/{run_id}/artifacts?per_page=100', token)
    if artifacts.get('total_count', 0) > 100:
        raise ArchiveError('Unexpected artifact count')
    expected_name = 'editor-journey-' + run['head_sha']
    matches = [a for a in artifacts['artifacts'] if a['name'] == expected_name and not a['expired']]
    if len(matches) != 1:
        raise ArchiveError('Exactly one unexpired matching evidence artifact is required')
    artifact = matches[0]
    workflow = artifact.get('workflow_run', {})
    if workflow.get('id') != run_id or workflow.get('head_sha') != run['head_sha']:
        raise ArchiveError('Artifact source does not match its run')
    if artifact['size_in_bytes'] > MAX_ARCHIVE:
        raise ArchiveError('Artifact size exceeds the Git evidence allowance')
    data = download_artifact(artifact['id'], token)
    if len(data) != artifact['size_in_bytes']:
        raise ArchiveError('Artifact byte length mismatch')
    members = validate_zip(data, artifact.get('digest'))
    destination = Path('docs/verification/editor-journey') / f'run-{run_id}-attempt-{run["run_attempt"]}'
    manifest = {'schema': 1, 'run_id': run_id, 'run_attempt': run['run_attempt'],
                'head_sha': run['head_sha'], 'run_url': run['html_url'], 'conclusion': run['conclusion'],
                'artifact_id': artifact['id'], 'artifact_bytes': len(data), 'artifact_digest': artifact['digest'],
                'members': members, 'artifact_contents_executed': False,
                'full_runtime_1_to_1_established': False}
    encoded = (json.dumps(manifest, indent=2) + '\n').encode()
    if destination.exists():
        if (destination / 'evidence.zip').read_bytes() != data or (destination / 'manifest.json').read_bytes() != encoded:
            raise ArchiveError('Refusing to overwrite a different existing run archive')
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
        staging = Path(temp) / 'ready'
        staging.mkdir()
        (staging / 'evidence.zip').write_bytes(data)
        (staging / 'manifest.json').write_bytes(encoded)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for name in ('comparison.json', 'journey.json', 'editor-session-comparison.json', 'editor-session-replay.json'):
                key = 'ci-editor/journey/' + name
                if key in archive.namelist():
                    payload = archive.read(key)
                    json.loads(payload)
                    (staging / name).write_bytes(payload)
        (staging / 'README.md').write_text(
            '# Preserved Android editor journey evidence\n\n'
            f'Run: {run_id}; source commit: `{run["head_sha"]}`.\n\n'
            'The exact GitHub artifact ZIP is committed here, with its API digest, '
            'member hashes and original JSON reports. Failed or incomplete runs are '
            'preserved without being converted into a pass. An exact recorded journey '
            'covers only its observed screens and transitions, not whole-app parity. '
            'No downloaded script is executed by the archive publisher.\n')
        staging.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', type=int, required=True)
    args = parser.parse_args()
    if args.run_id <= 0 or os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        parser.error('A positive run ID in the explicitly selected repository is required')
    token = os.environ.get('GH_TOKEN')
    if not token:
        parser.error('A scoped workflow token is required')
    try:
        path = archive_run(args.run_id, token)
        print(path)
        output = os.environ.get('GITHUB_OUTPUT')
        if output:
            with open(output, 'a') as stream:
                stream.write('archive_path=' + path.as_posix() + '\n')
    except (ArchiveError, OSError, ValueError, KeyError) as exc:
        # Never include credential-bearing download URLs in exception output.
        print('Evidence archive failed:', type(exc).__name__)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
