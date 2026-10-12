#!/usr/bin/env python3
"""Copy the exact prior guard and newly observed Day/Time surface into a private stage."""
from pathlib import Path
import datetime, hashlib, json, shutil

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'trigger-catalog-forward/checkpoints/05-physical-identity-host-success'
BASE_SHA = '8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743'
STAGE = ROOT / 'stage-01/repository'
RAW = ROOT.parent / 'ci-run-analysis/zero12-run-38216299675-extracted/journey'

def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def copy(source, target, expected=None):
    actual = identity(source)
    if expected is not None and actual != expected: raise RuntimeError('Source identity differs: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream: stream.write(source.read_bytes())
    if identity(target) != actual: raise RuntimeError('Copied identity differs')
    return actual

def main():
    if STAGE.exists(): raise RuntimeError('Private stage already exists')
    if identity(BASE / 'checkpoint.json')['sha256'] != BASE_SHA: raise RuntimeError('Prior guard checkpoint changed')
    checkpoint = json.loads((BASE / 'checkpoint.json').read_text())
    STAGE.mkdir(parents=True)
    prior = {}
    for row in checkpoint['files']:
        if row['path'].startswith('replay-source/'):
            name = row['path'][len('replay-source/'):]
            prior[name] = copy(BASE / row['path'], STAGE / name, {key: row[key] for key in ('bytes', 'sha256')})
    old_inputs = json.loads((BASE / 'reports/inputs-before.json').read_text())
    fixtures = {name: row for name, row in old_inputs.items() if name.endswith('/evidence.zip')}
    if len(fixtures) != 2: raise RuntimeError('Expected exactly two historical evidence ZIPs')
    for name, pin in fixtures.items():
        source = ROOT.parent / 'trigger-catalog-forward/stage-05/repository' / name
        prior[name] = copy(source, STAGE / name, pin)
    report = json.loads((RAW / 'journey.json').read_text())
    if report['plan_sha256'] != '940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc':
        raise RuntimeError('Unexpected observed twelve-screen source plan')
    rows = []; destination = STAGE / 'tools/parity_journeys/fixtures/day-time-trigger'
    for run in report['runs']:
        if run['label'] not in ('original', 'candidate') or run['status'] != 'COMPLETE': raise RuntimeError('Incomplete observed source')
        shot = run['screens'][-1]
        if shot['name'] != 'after-trigger-date-category': raise RuntimeError('Unexpected source surface')
        copied = {}
        for role, item in shot['artifacts'].items():
            extension = {'hierarchy': '.xml', 'screenshot': '.png'}.get(role, '-' + role.replace('_', '-') + '.txt')
            name = run['label'] + '-date-time' + extension
            copied[role] = {'fixture': name, 'source': item['path'], **copy(RAW / item['path'], destination / name,
                                  {key: item[key] for key in ('bytes', 'sha256')})}
        if copied['hierarchy']['sha256'] != '9bb3a60891fc9194b2f9ae493e513a041a6ee2e395125c13dbeb8cef648abcd0':
            raise RuntimeError('Unexpected observed hierarchy')
        if copied['screenshot']['sha256'] != '7057b96a46d56c0e53a3b42a3475a24812b5867a753bcf81b528e9a8a6aefa92':
            raise RuntimeError('Unexpected observed full image')
        rows.append({'label': run['label'], 'apkSha256': run['apk_sha256'], 'shot': shot['name'], 'artifacts': copied})
    provenance = {'sourceRunId': 38216299675, 'sourceCommit': '6331410cfd2391389270564803623079e8355ad8',
                  'sourceJourney': identity(RAW / 'journey.json'), 'sourceComparison': identity(RAW / 'comparison.json'),
                  'sourceArchive': identity(ROOT.parent / 'ci-run-analysis/zero12-run-38216299675.zip'),
                  'scope': 'Exact observed Date/Time surfaces after the twelve-screen run; no Day/Time tile input has been observed yet.',
                  'pairedRawSurfaces': rows}
    (destination / 'source-observation.json').write_text(json.dumps(provenance, indent=2) + '\n')
    (ROOT / 'stage-01/parent-source-identities.json').write_text(json.dumps(prior, indent=2) + '\n')
    copy(BASE / 'checkpoint.json', ROOT / 'stage-01/parent-checkpoint.json')
    print(json.dumps({'status': 'PRIVATE_STAGE_PREPARED', 'parentSourceFiles': len(prior),
                      'observedSurfaceArtifacts': sum(len(row['artifacts']) for row in rows),
                      'createdUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2))

if __name__ == '__main__': main()
