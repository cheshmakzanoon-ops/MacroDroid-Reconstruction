from pathlib import Path
import hashlib, json, os, subprocess
expected = {'tools/indicator_sampling/README.md': {'bytes': 8924, 'sha256': 'd72b37bfe4c392f677b623e7800ae3b5679cc80d05064f684d8d39579300e19a'}, 'tools/indicator_sampling/aapt2': {'bytes': 6135688, 'sha256': '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}, 'tools/indicator_sampling/common.py': {'bytes': 9379, 'sha256': '09a2d1a5360bdb4a6e28f637012949c310f65d1885b9a7a9ef785dc12d4c4a67'}, 'tools/indicator_sampling/fixtures/candidate-intro1-preinput.xml': {'bytes': 5939, 'sha256': '9041a607c7b2fd166eb1a3580b85f7a4a6b87da5966c270454fba8eadbdd5a93'}, 'tools/indicator_sampling/fixtures/candidate-intro2.xml': {'bytes': 6689, 'sha256': '840d3f966746dea5dffe838eda7b46b0c7f48ee37b59d33cbcb28336f199dfd8'}, 'tools/indicator_sampling/fixtures/original-intro1-preinput.xml': {'bytes': 5939, 'sha256': '9041a607c7b2fd166eb1a3580b85f7a4a6b87da5966c270454fba8eadbdd5a93'}, 'tools/indicator_sampling/fixtures/original-intro2.xml': {'bytes': 6689, 'sha256': '840d3f966746dea5dffe838eda7b46b0c7f48ee37b59d33cbcb28336f199dfd8'}, 'tools/indicator_sampling/historical-coordinates.json': {'bytes': 11700, 'sha256': '7a8f88a7e79a23a3fa633f8e75c45a4060a02b86b3c24105181e2b57058da646'}, 'tools/indicator_sampling/pins.json': {'bytes': 4088, 'sha256': 'f6340442c5e26180f2eec358b887b1f7137b49210fab1f42b40422ce676518ae'}, 'tools/indicator_sampling/prepare.py': {'bytes': 16312, 'sha256': '821e08cb4c0e1f568d832588ec85d10f148a27a092ba9269d8871d9ac9cd2905'}, 'tools/indicator_sampling/protocol.json': {'bytes': 4543, 'sha256': 'edbb9647e129b2f3475f0a1b759628996d388a50ad65ee6d527ba0737432a482'}, 'tools/indicator_sampling/record.py': {'bytes': 33511, 'sha256': '2f9d81423930ec7717b6972a6b6bf46ead6e4ae54b0f7950ceabe62d4c947374'}, 'tools/indicator_sampling/test_indicator_sampling.py': {'bytes': 32837, 'sha256': 'c0358116b2eb9a91819098187e2f59ad5b2719a35ad043456f33951904ea0f17'}, 'tools/indicator_sampling/verify.py': {'bytes': 57632, 'sha256': '0ce0a496d22d257d907978db213a0a0b6fe29f8156176f4efb43858d024351e3'}}
workflow = '.github/workflows/indicator-fixed-sampling.yml'
manifest = 'tools/indicator_sampling/runtime-files.json'
output = Path('ci-indicator/owned-source')
output.mkdir()
actual = []
for name in sorted([*expected, workflow, manifest]):
    source = Path(name)
    if source.is_symlink() or not source.is_file():
        raise RuntimeError('Missing or linked executed source: ' + name)
    raw = source.read_bytes()
    target = output / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(raw)
    target.chmod(source.stat().st_mode & 0o777)
    actual.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
Path('ci-indicator/executed-source.json').write_text(json.dumps(actual, indent=2) + '\n')
def git(argv):
    result = subprocess.run(['git', *argv], capture_output=True, timeout=60, check=True)
    if result.stderr.strip():
        raise RuntimeError('Unexpected Git verification stderr')
    return result.stdout
head = git(['rev-parse', 'HEAD']).decode().strip()
parent = git(['-C', 'pinned-inputs', 'rev-parse', 'HEAD']).decode().strip()
if head != os.environ['GITHUB_SHA'] or parent != '6331410cfd2391389270564803623079e8355ad8':
    raise RuntimeError('Actual source checkout identity differs')
if git(['show', 'HEAD:' + workflow]) != Path(workflow).read_bytes():
    raise RuntimeError('Executed workflow differs from its exact checked-out commit')
required = []
for row in actual:
    if row['path'] in expected and {k: row[k] for k in ('bytes', 'sha256')} != expected[row['path']]:
        raise RuntimeError('Reviewed source changed: ' + row['path'])
    if row['path'] != manifest:
        required.append(row)
if json.loads(Path(manifest).read_text()) != required:
    raise RuntimeError('Runtime manifest omitted, changed or reordered a required source role')
Path('ci-indicator/source-checkout.json').write_text(json.dumps({'head': head, 'parent_head': parent,
    'workflow_matches_committed_blob': True, 'required_source_files': len(actual)}, indent=2) + '\n')
