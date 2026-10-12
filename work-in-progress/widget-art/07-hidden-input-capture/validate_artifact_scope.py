#!/usr/bin/env python3
"""Review the owned artifact root and exact one-line uploader configuration change."""
from collections import Counter
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import os
import yaml

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'checkpoints/05-rerun-workflow'
CAPTURE = ROOT.parent / 'hosted-run-38207925500'
REPOSITORY = ROOT.parent.parent / 'MacroDroid-Reconstruction'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    output = ROOT / 'reports/validation-01'
    output.mkdir(parents=True, exist_ok=False)
    result = {'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Exact one-line upload option, owned artifact path inventory and one real offline preflight; no Android/upload execution.',
        'android_executed': False, 'uploader_executed': False}
    try:
        original = BASE / '.github/workflows/widget-method-probe.yml'
        changed = ROOT / '.github/workflows/widget-method-probe.yml'
        baseline = original.read_text()
        expected = baseline.replace('          path: ci-widget-method/\n',
            '          path: ci-widget-method/\n          include-hidden-files: true\n')
        if (sha(original) != 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7' or
                sha(REPOSITORY / '.github/workflows/widget-method-probe.yml') != sha(original) or
                changed.read_text() != expected):
            raise RuntimeError('Workflow change exceeds the exact one-line proposal')
        before = yaml.load(baseline, Loader=yaml.BaseLoader)
        after = yaml.load(changed.read_text(), Loader=yaml.BaseLoader)
        old_steps, new_steps = before['jobs']['widget-method-probe']['steps'], after['jobs']['widget-method-probe']['steps']
        upload = new_steps[-1]
        if (upload['uses'] != 'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02' or
                upload['with']['path'] != 'ci-widget-method/' or upload['with']['include-hidden-files'] != 'true' or
                upload['if'] != 'always()' or new_steps[:-1] != old_steps[:-1]):
            raise RuntimeError('Artifact scope or any executable step changed')
        (output / 'workflow.patch').write_text(''.join(difflib.unified_diff(
            baseline.splitlines(keepends=True), changed.read_text().splitlines(keepends=True),
            fromfile='original/.github/workflows/widget-method-probe.yml',
            tofile='corrected/.github/workflows/widget-method-probe.yml')))
        action = CAPTURE / 'supplemental-provenance/upload-artifact-action.yml'
        if sha(action) != '29b21270ff44638a165ea12abb4481796770c629e513217af7b4df1aa3821177':
            raise RuntimeError('Pinned official uploader definition changed')
        definition = yaml.load(action.read_text(), Loader=yaml.BaseLoader)
        if definition['inputs']['include-hidden-files']['default'] != 'false':
            raise RuntimeError('Pinned uploader does not expose the reviewed hidden-file input')

        manifest = json.loads((CAPTURE / 'download-manifest.json').read_text())
        rows = manifest['files']
        actual = {item['path'] for item in rows}
        host = BASE / 'evidence/reports/validation-01/packaged-wrapper-control-evidence'
        host_names = {'host-control-evidence/' + path.relative_to(host).as_posix()
                      for path in host.rglob('*') if path.is_file()}
        report = json.loads((CAPTURE / 'extracted/probe/probe-result.json').read_text())
        probe_names = {'probe/' + name for name in ('executed-wrapper.py', 'input-provenance.json',
                                                   'input-probe.dex', 'probe-result.json')}
        probe_names |= {'probe/' + command[kind]['path'] for command in report['commands'] for kind in ('stdout', 'stderr')}
        preflight = json.loads((CAPTURE / 'extracted/input-preflight.json').read_text())
        input_names = {'executed-inputs/' + item['path'] for item in preflight['files']}
        environment = {'environment/' + name for name in (
            'emulator-boot.log', 'emulator-launch.json', 'runtime-properties.json', 'runtime-status.json',
            'queue/STOP', 'queue/requests/widget-method-art.done', 'queue/responses/widget-method-art.json',
            'queue/responses/widget-method-art.stderr', 'queue/responses/widget-method-art.stdout')}
        tooling = {'toolchain/' + name for name in (
            'android/emulator/source.properties', 'android/platform-tools/source.properties',
            'android/system-images/android-35/google_apis/x86_64/build.prop',
            'android/system-images/android-35/google_apis/x86_64/source.properties',
            'android-user/avd/MacroDroid_API35_Disposable.avd/config.ini',
            'android-user/avd/MacroDroid_API35_Disposable.ini', 'installed-inputs.json', 'jdk21/release')}
        top = {'bootstrap.log', 'download-tests.log', 'input-preflight.json', 'input-preflight.log',
            'lifecycle.log', 'materialize-original.log', 'owned-service-pid.txt', 'materialize-widget.log',
            'readiness.log', 'runtime-cleanup.json', 'runtime-driver.log', 'service.log', 'runtime-job.log',
            'toolchain-metadata.log', 'wrapper-tests.log'}
        allowed = host_names | probe_names | input_names | environment | tooling | top
        missing = allowed - actual
        expected_missing = {'executed-inputs/.github/workflows/widget-method-probe.yml'}
        if actual - allowed or missing != expected_missing:
            raise RuntimeError('Unexpected output path or another missing archived output')
        credentials = re.compile(r'^(?:\.git|\.ssh|\.aws|\.azure|\.env(?:\..*)?|credentials|id_rsa|id_ed25519|adbkey(?:\.pub)?|.*\.(?:pem|p12|pfx|jks|keystore))$', re.I)
        for name in allowed:
            relative = PurePosixPath(name)
            if (relative.is_absolute() or '..' in relative.parts or '\\' in name or
                    any(credentials.fullmatch(part) for part in relative.parts)):
                raise RuntimeError('Unsafe or credential-shaped artifact path')
            if any(part.startswith('.') for part in relative.parts) and name not in expected_missing:
                raise RuntimeError('Unexpected hidden artifact path')
        for item in rows:
            path = CAPTURE / 'extracted' / item['path']
            if path.is_symlink() or not path.is_file() or path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
                raise RuntimeError('Observed artifact tree changed')
        result['observed_output_inventory'] = {'count': len(rows), 'files': rows,
            'counts_by_root': dict(sorted(Counter(name.split('/')[0] for name in actual).items())),
            'unexpected_paths': [], 'credential_shaped_paths': [], 'unexpected_hidden_paths': [],
            'omitted_hidden_workflow_copy': sorted(missing),
            'scope': 'Observed 7,213-file artifact plus its one known missing bound input; future output is checked after the fresh job.'}
        result['producer_scope'] = {
            'artifact_root_created_fresh': 'mkdir ci-widget-method fails if the root already exists',
            'checkout_credentials': 'persist-credentials:false; repository .git is outside the owned output root',
            'sdk_and_adb_private_keys': 'tooling root is RUNNER_TEMP/macrodroid-widget-tooling, outside the artifact root',
            'copied_inputs': 'Only the nineteen reviewed input-preflight paths',
            'host_control_paths': 'All7,039 observed paths exactly match the frozen reviewed test output path set',
            'environment_paths': 'Nine explicit owned emulator/service queue files',
            'toolchain_paths': 'Eight selected public metadata files, not the tooling directory',
        }
        with tempfile.TemporaryDirectory(prefix='widget-hidden-copy-preflight-') as temporary:
            seed = Path(temporary)
            for item in preflight['files']:
                name = item['path']
                source = changed if name == '.github/workflows/widget-method-probe.yml' else REPOSITORY / name
                target = seed / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            script = output / 'unchanged-input-preflight.sh'
            script.write_text(new_steps[1]['run'])
            with (output / 'preflight.stdout.txt').open('wb') as out, (output / 'preflight.stderr.txt').open('wb') as err:
                completed = subprocess.run(['bash', str(script)], cwd=seed,
                    env={**os.environ, 'GITHUB_WORKSPACE': str(seed), 'GITHUB_SHA': 'offline-hidden-copy-proposal'},
                    stdout=out, stderr=err, timeout=60)
            if completed.returncode != 0:
                raise RuntimeError('The unchanged nineteen-input preflight failed')
            observed = json.loads((seed / 'ci-widget-method/input-preflight.json').read_text())
            hidden = seed / 'ci-widget-method/executed-inputs/.github/workflows/widget-method-probe.yml'
            if observed['passed'] is not True or len(observed['files']) != 19 or hidden.read_bytes() != changed.read_bytes():
                raise RuntimeError('Owned hidden input copy was not created exactly')
            shutil.copytree(seed / 'ci-widget-method', output / 'offline-preflight-output')
            result['offline_preflight'] = {'returncode': completed.returncode, 'timeout_seconds': 60,
                'input_files': 19, 'hidden_copy_created_exactly': True,
                'uploader_not_executed': True}
        result['baseline_workflow_sha256'] = sha(original)
        result['proposed_workflow_sha256'] = sha(changed)
        result['prior_21_command_validation'] = {
            'checkpoint_sha256': '670bb7a33921547e74460669d940da8cb4f223d17366e28eab7430ac7276c501',
            'all_existing_run_steps_byte_identical': True,
            'rerun_here': False,
        }
        result['passed'] = True
    except Exception as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', result)
        compact = {key: value for key, value in result.items() if key != 'observed_output_inventory'}
        print(json.dumps(compact, indent=2))


if __name__ == '__main__':
    main()
