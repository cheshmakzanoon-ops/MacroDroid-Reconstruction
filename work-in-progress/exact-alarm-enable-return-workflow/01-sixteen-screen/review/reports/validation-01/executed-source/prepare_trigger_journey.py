#!/usr/bin/env python3
"""Prepare pinned tools and APKs for the sixteen-screen exact-alarm navigation journey."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import stat
import tarfile

GUARD = 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls'
ANIMATION = 'work-in-progress/trigger-category/07-zero-animation-source'
WORKFLOW = '.github/workflows/editor-exact-alarm-enable-return.yml'
PACKAGE = 'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen'
PINS = {
    'scripts/materialize_v9.py': '99a2a50a1518bf7f960ba8bc07b9e4c25bbb882118494cc4b82d0cc87f94be0c',
    'scripts/import_v9.py': '11a1890a9e60d3905181189df6f28963c7c59b2046bc759a28b975d9b309ffa1',
    'scripts/assemble_artifact.py': 'f85a570f864ec2481dd75783b82006129755194c941b54e193c893b7ee17e97c',
    'vendor/v9/manifest.json': '11217d372fef3f4ca644ae4b10019aba69888d7944aeb5c22d7738db2a16eea3',
    'vendor/original/manifest.json': 'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684',
    'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json': 'e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152',
    'tools/android/bootstrap_android_runtime.py': '8ae2a365cc5ec5109c76967642d6ee7f6655df96287cf8feb3355444e14e4e36',
    'tools/android/android-toolchain-pins.json': '3ce2078cb52f540fd86ffdccf8577535662fee1c5274f13bcf01d8d15e3bd8b2',
    'tools/android/android_runtime_service.py': '3ac1047b8ff41aba79d1ef335e8eed260067d696460bf8322195631f09dfec57',
    'tools/android/runtime_job.py': '7babd7ebcc35e531b6b0fea9167b3436ff738e43bf0f869b44534573cb849bc8',
    'tools/android/wait_android_ready.py': '72cb3bcd56df72cd901ee724c48a44b0254235e1d7cdda6c991b985e572f34af',
    'tools/android/configure_capture_device.py': '50b93f00b68147323be46c8311ee32d3f201683a40b1825d17a02bc51ce25ec8',
    'tools/android/test_download_retry.py': 'bd5d871951fbf1e5f7aa3093c8c155b1c599d84ae008b90e1eda53bf3a60948a',
    GUARD + '/checkpoint.json': '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051',
    ANIMATION + '/checkpoint.json': '5cb124753f8acb7cf8e0ec070f1ddf2b2f9b49d99ad144dea6f2b37047258a48',
}
REPORT_SCHEMA = 7
READINESS_POLICY_SHA256 = '033014f5cfddcf41e99d41147861aaf3bf60509fbe20af01d296c4715272dc1f'
NAVIGATION_POLICY_SHA256 = '152b5356447daebaba07ddede2c851cd9affd5c5fab120be7b902cf17e1ea757'
SETTINGS_CONTRACT_SHA256 = '379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07'
APKS = [
    ('vendor/original/manifest.json', 'MacroDroid-5.67.8-original.apk', 95725918,
     '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    ('work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json', 'MacroDroid-5.67.8-day-numeric-0762aad9.apk', 94683136,
     '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'),
]
AAPT = {'bytes': 6135688, 'sha256': '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def checked_file(root, name):
    if type(name) is not str or not name:
        raise ValueError('Input path must be a nonempty string')
    relative = PurePosixPath(name)
    if (relative.is_absolute() or '..' in relative.parts or '\\' in name
            or relative.as_posix() != name):
        raise ValueError('Unsafe input path: ' + name)
    path = root / name
    if (path.is_symlink() or not path.is_file() or path.resolve() != path
            or not path.resolve().is_relative_to(root)):
        raise ValueError('Missing or unconfined input: ' + name)
    return path


GUARD_ARCHIVE = GUARD + '/evidence.tar.gz'
GUARD_LAYOUT = GUARD + '/archive-layout'
GUARD_ARCHIVE_ID = {'bytes': 13014001, 'sha256': '51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755'}
GUARD_INVENTORY_ID = {'bytes': 83303, 'sha256': 'ca355e5096b4f928196a311e7cd35bc257a250185fae1249be7eda33f8780395'}
GUARD_TRANSPORT = [
    (GUARD_LAYOUT + '/manifest.json', 1549, '8be9e7dab79ccad82db4b98e33e8418044a372a456e45907bcec0f134bce6310'),
    (GUARD_LAYOUT + '/parts/evidence.0001.part', 8388608, '550db03854608f0c565e9dd891b37fb6784338f175cfb9b329edddf2965988e6'),
    (GUARD_LAYOUT + '/parts/evidence.0002.part', 4625393, 'b72fddce277db14a84ee83c1f9cd43fe00939c24e6a56fd31c58fcfa293baf1c'),
]
PINS.update({name: digest for name, _, digest in GUARD_TRANSPORT})


def guard_transport(root):
    """Verify both fixed parts on every entry, including an existing archive."""
    checkpoint = checked_file(root, GUARD + '/checkpoint.json')
    if identity(checkpoint) != {'bytes': 39880, 'sha256': PINS[GUARD + '/checkpoint.json']}:
        raise ValueError('Pinned source checkpoint changed before archive preparation')
    rows = []
    combined = hashlib.sha256()
    total = 0
    for index, (name, size, digest) in enumerate(GUARD_TRANSPORT):
        path = checked_file(root, name)
        if stat.S_IMODE(path.stat().st_mode) != 0o644:
            raise ValueError('Pinned archive transport mode changed: ' + name)
        actual = hashlib.sha256()
        count = 0
        with path.open('rb') as stream:
            while chunk := stream.read(1024 * 1024):
                actual.update(chunk)
                count += len(chunk)
                if index:
                    combined.update(chunk)
                    total += len(chunk)
        if (count, actual.hexdigest()) != (size, digest):
            raise ValueError('Pinned archive transport changed: ' + name)
        rows.append({'path': name, 'bytes': count, 'sha256': digest, 'mode': 0o644})
    if {'bytes': total, 'sha256': combined.hexdigest()} != GUARD_ARCHIVE_ID:
        raise ValueError('Fixed archive part concatenation differs')
    manifest = json.loads(checked_file(root, GUARD_TRANSPORT[0][0]).read_bytes())
    if (manifest['format'] != 'macrodroid-multipart-artifact' or manifest['format_version'] != 1
            or manifest['filename'] != 'evidence.tar.gz' or manifest['mode'] != '100644'
            or {'bytes': manifest['size_bytes'], 'sha256': manifest['sha256']} != GUARD_ARCHIVE_ID
            or manifest['logical_repository_path'] != GUARD_ARCHIVE
            or manifest['source_checkpoint'] != {'path': GUARD + '/checkpoint.json',
                'bytes': 39880, 'sha256': PINS[GUARD + '/checkpoint.json']}
            or [(row['path'], row['size_bytes'], row['sha256'], row['mode']) for row in manifest['parts']]
                != [(name, size, digest, '100644') for name, size, digest in GUARD_TRANSPORT[1:]]):
        raise ValueError('Pinned archive manifest structure differs')
    return {'manifest': rows[0], 'parts': rows[1:], 'concatenated': dict(GUARD_ARCHIVE_ID),
            'source_checkpoint': {'path': GUARD + '/checkpoint.json', **identity(checkpoint)}}


def verify_guard_archive(root):
    """Read the exact logical archive and all 353 independently pinned members."""
    transport = guard_transport(root)
    archive = checked_file(root, GUARD_ARCHIVE)
    if (identity(archive) != GUARD_ARCHIVE_ID or stat.S_IMODE(archive.stat().st_mode) != 0o644):
        raise ValueError('Existing logical guard archive differs; refusing replacement')
    inventory_path = checked_file(root, GUARD + '/evidence-inventory.json')
    if identity(inventory_path) != GUARD_INVENTORY_ID:
        raise ValueError('Pinned guard archive member inventory changed')
    expected = json.loads(inventory_path.read_bytes())
    if (type(expected) is not list or len(expected) != 353
            or any(type(row) is not dict or set(row) != {'path', 'bytes', 'sha256', 'mode'} for row in expected)
            or len({row['path'] for row in expected}) != 353):
        raise ValueError('Guard archive member inventory is incomplete')
    observed = []
    with tarfile.open(archive, 'r|gz') as stream:
        for member in stream:
            index = len(observed)
            if index >= len(expected):
                raise ValueError('Extra guard archive member')
            row = expected[index]
            name = PurePosixPath(member.name)
            if (not member.isfile() or member.name != row['path'] or name.is_absolute()
                    or '..' in name.parts or name.as_posix() != member.name
                    or member.size != row['bytes'] or member.mode != row['mode']):
                raise ValueError('Guard archive member identity changed: ' + member.name)
            payload = stream.extractfile(member)
            if payload is None:
                raise ValueError('Missing regular guard archive member: ' + member.name)
            with payload:
                digest = hashlib.file_digest(payload, 'sha256').hexdigest()
            if digest != row['sha256']:
                raise ValueError('Guard archive member bytes changed: ' + member.name)
            observed.append(row)
    if observed != expected:
        raise ValueError('Missing guard archive member')
    return {**transport, 'logical_archive': {'path': GUARD_ARCHIVE, **GUARD_ARCHIVE_ID, 'mode': 0o644},
            'member_inventory': {'path': GUARD + '/evidence-inventory.json', **GUARD_INVENTORY_ID},
            'verified_members': len(observed)}


def prepare_guard_archive(root, output, receipt):
    """Create only a missing logical file from the fixed, already verified parts."""
    receipt.update(status='VERIFYING_SOURCE_ARCHIVE_TRANSPORT', android_executed=False,
                   logical_archive=GUARD_ARCHIVE, started_utc=datetime.now(timezone.utc).isoformat())
    receipt['transport_before'] = guard_transport(root)
    archive = root / GUARD_ARCHIVE
    receipt['logical_archive_existed'] = archive.exists() or archive.is_symlink()
    if receipt['logical_archive_existed']:
        receipt['action'] = 'VERIFIED_EXISTING_LOGICAL_ARCHIVE'
        receipt['verified'] = verify_guard_archive(root)
    else:
        temporary = output / 'source03-logical-archive.tmp'
        receipt['temporary_path'] = str(temporary.relative_to(output))
        receipt['action'] = 'ASSEMBLED_MISSING_LOGICAL_ARCHIVE'
        with temporary.open('xb') as target:
            for name, size, digest in GUARD_TRANSPORT[1:]:
                part = checked_file(root, name)
                observed = hashlib.sha256()
                length = 0
                with part.open('rb') as source:
                    while chunk := source.read(1024 * 1024):
                        target.write(chunk)
                        observed.update(chunk)
                        length += len(chunk)
                if (length, observed.hexdigest()) != (size, digest):
                    raise ValueError('Archive part changed during assembly: ' + name)
            target.flush()
            os.fchmod(target.fileno(), 0o644)
            os.fsync(target.fileno())
        if identity(temporary) != GUARD_ARCHIVE_ID:
            raise ValueError('Assembled logical guard archive differs')
        if guard_transport(root) != receipt['transport_before']:
            raise ValueError('Archive transport changed during assembly')
        # Exclusive hard-link creation cannot replace a concurrently created file.
        os.link(temporary, archive)
        temporary.unlink()
        receipt['verified'] = verify_guard_archive(root)
    receipt['transport_after'] = guard_transport(root)
    if receipt['transport_before'] != receipt['transport_after']:
        raise ValueError('Archive transport changed during preparation')
    receipt.update(status='EXACT_SOURCE_ARCHIVE_READY',
                   finished_utc=datetime.now(timezone.utc).isoformat())


def expected_inputs(root):
    """Rebuild the entire ordered inventory from pinned source, never a report.

    The workflow is bound externally to its Git revision and preserved copy.
    Its two literal helper digests bind the preparer and final verifier without
    trusting digest or membership claims from input-preflight.json.
    """
    rows = []
    destinations = set()

    def add(name, digest, size=None, destination=None):
        if (type(digest) is not str or re.fullmatch('[0-9a-f]{64}', digest) is None
                or size is not None and (type(size) is not int or size < 0)):
            raise ValueError('Invalid frozen input identity: ' + name)
        path = checked_file(root, name)
        actual = identity(path)
        if actual['sha256'] != digest or size is not None and actual['bytes'] != size:
            raise ValueError('Pinned input changed: ' + name)
        copy = destination or ('executed-inputs/' + name)
        if copy in destinations:
            raise ValueError('Duplicate frozen input destination: ' + copy)
        destinations.add(copy)
        rows.append({'path': name, 'copy': copy, **actual})

    for name, digest in PINS.items():
        add(name, digest)
    verify_guard_archive(root)
    for package, count in [(GUARD, 181), (ANIMATION, 9)]:
        checkpoint = json.loads(checked_file(root, package + '/checkpoint.json').read_text())
        files = checkpoint['files']
        if (type(files) is not list or len(files) != count
                or any(type(row) is not dict or set(row) != ({'path', 'bytes', 'sha256', 'mode'} if package == GUARD else {'path', 'bytes', 'sha256'}) for row in files)
                or len({row['path'] for row in files}) != count):
            raise ValueError('Frozen package inventory changed: ' + package)
        for row in files:
            name = package + '/' + row['path']
            if package == GUARD and (type(row['mode']) is not int
                    or stat.S_IMODE(checked_file(root, name).stat().st_mode) != row['mode']):
                raise ValueError('Frozen source payload mode changed: ' + name)
            add(name, row['sha256'], row['bytes'])
            if package == GUARD and row['path'].startswith('source/'):
                add(name, row['sha256'], row['bytes'],
                    'reviewed-source/' + row['path'][len('source/'):])
    guard_inputs = json.loads(checked_file(root, GUARD + '/reports/inputs-before.json').read_text())
    archives = {name: value for name, value in guard_inputs.items() if name.endswith('/evidence.zip')}
    if len(archives) != 2:
        raise ValueError('Exactly two pinned historical host fixtures are required')
    for name, value in archives.items():
        add(name, value['sha256'], value['bytes'])
        add(name, value['sha256'], value['bytes'], 'reviewed-source/' + name)
    for name, filename, size, digest in APKS:
        value = json.loads(checked_file(root, name).read_text())
        if (value['filename'], value['size_bytes'], value['sha256']) != (filename, size, digest):
            raise ValueError('Unexpected diagnostic APK identity: ' + name)
    workflow = checked_file(root, WORKFLOW)
    matches = re.findall(r'^          pins = (\{\n.*?^          \})$',
                         workflow.read_text(), flags=re.MULTILINE | re.DOTALL)
    if len(matches) != 1:
        raise ValueError('Exactly one literal workflow helper inventory is required')
    helper_pins = ast.literal_eval(matches[0])
    helpers = [PACKAGE + '/prepare_trigger_journey.py', PACKAGE + '/verify_trigger_journey.py']
    if type(helper_pins) is not dict or list(helper_pins) != helpers:
        raise ValueError('Workflow helper inventory changed')
    add(WORKFLOW, identity(workflow)['sha256'])
    for name in helpers:
        add(name, helper_pins[name])
    return rows


def verify_prepared_inputs(root, output, report):
    """Require exact membership and identities before executing copied code."""
    if report.get('passed') is not True or report.get('status') != 'FROZEN_EXACT_ALARM_ENABLE_RETURN_INPUTS_VERIFIED':
        raise ValueError('Successful frozen input preflight required')
    expected = expected_inputs(root)
    if type(report.get('files')) is not list or report['files'] != expected:
        raise ValueError('Prepared input inventory is not the complete independently pinned inventory')
    if (report.get('plan_sha256') != 'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211'
            or report.get('requested_scales') != '0'
            or type(report.get('requested_report_schema')) is not int
            or report['requested_report_schema'] != REPORT_SCHEMA
            or report.get('notification_readiness_policy_sha256') != READINESS_POLICY_SHA256
            or report.get('exact_alarm_enable_return_policy_sha256') != NAVIGATION_POLICY_SHA256
            or report.get('settings_contract_sha256') != SETTINGS_CONTRACT_SHA256
            or report.get('android_executed') is not False):
        raise ValueError('Frozen diagnostic plan or preparation scope changed')
    for row in expected:
        actual = {'bytes': row['bytes'], 'sha256': row['sha256']}
        if (identity(checked_file(root, row['path'])) != actual
                or identity(checked_file(output, row['copy'])) != actual):
            raise ValueError('Prepared input changed before execution: ' + row['path'])
    return expected


def prepare(root, output):
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'VERIFYING_FROZEN_INPUTS', 'passed': False, 'android_executed': False,
              'github_sha': os.environ.get('GITHUB_SHA'), 'files': [],
              'started_utc': datetime.now(timezone.utc).isoformat()}
    def copy(row):
        name = row['path']
        path = checked_file(root, name)
        actual = identity(path)
        if actual != {'bytes': row['bytes'], 'sha256': row['sha256']}:
            raise ValueError('Pinned input changed: ' + name)
        target = output / row['copy']
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(path.read_bytes())
        if identity(target) != actual or identity(path) != actual:
            raise ValueError('Input changed while copying: ' + name)
        report['files'].append(row)
    try:
        report['guard_archive_preparation'] = {}
        prepare_guard_archive(root, output, report['guard_archive_preparation'])
        for row in expected_inputs(root):
            copy(row)
        report.update(status='FROZEN_EXACT_ALARM_ENABLE_RETURN_INPUTS_VERIFIED', passed=True,
                      plan_sha256='ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211',
                      requested_scales='0', requested_report_schema=REPORT_SCHEMA,
                      notification_readiness_policy_sha256=READINESS_POLICY_SHA256,
                      exact_alarm_enable_return_policy_sha256=NAVIGATION_POLICY_SHA256,
                      settings_contract_sha256=SETTINGS_CONTRACT_SHA256,
                      full_runtime_1_to_1_established=False)
    except Exception as error:
        report.update(status='FROZEN_INPUT_PREFLIGHT_FAILED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'input-preflight.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def materialized(root, output):
    report = {'status': 'VERIFYING_MATERIALIZED_INPUTS', 'passed': False, 'android_executed': False}
    try:
        initial = json.loads((output / 'input-preflight.json').read_text())
        verify_prepared_inputs(root, output, initial)
        source = checked_file(root, 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2')
        if identity(source) != AAPT:
            raise ValueError('Preserved AAPT2 identity changed')
        target = output / 'reviewed-source/project/tools/prebuilt/linux/aapt2'
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(source.read_bytes())
        if identity(target) != AAPT:
            raise ValueError('AAPT2 copy changed')
        target.chmod(0o755)
        apk_paths = []
        for _, filename, size, digest in APKS:
            path = checked_file(root, 'workspace/artifacts/' + filename)
            if identity(path) != {'bytes': size, 'sha256': digest}:
                raise ValueError('Materialized APK identity changed: ' + filename)
            apk_paths.append(path)
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(output / 'reviewed-source/project'))
        from android_acceptance import prevalidate_pair
        report['apk_prevalidation'] = prevalidate_pair(*apk_paths)
        report.update(status='EXACT_APKS_AND_AAPT2_VERIFIED_OFFLINE', passed=True,
                      aapt2={'source': str(source.relative_to(root)), 'executed_copy': str(target.relative_to(output)), **AAPT})
    except Exception as error:
        report.update(status='MATERIALIZED_INPUT_PREFLIGHT_FAILED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        (output / 'materialized-inputs.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--materialized', action='store_true')
    args = parser.parse_args()
    function = materialized if args.materialized else prepare
    print(json.dumps(function(args.root.resolve(), args.output.resolve()), indent=2))


if __name__ == '__main__':
    main()
