"""Fixed inputs and byte/identity helpers for the independent indicator study."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time

HERE = Path(__file__).resolve().parent
PARENT_COMMIT = '6331410cfd2391389270564803623079e8355ad8'
GUARD = 'work-in-progress/trigger-category/05-physical-identity-host-success/replay-source'
PACKAGE = 'com.arlosoft.macrodroid'
INTRO = PACKAGE + '/' + PACKAGE + '.intro.IntroActivity'
SERIAL = 'emulator-5560'
AVD = 'MacroDroid_API35_Disposable'
FINGERPRINT = 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys'
FIELDS = ('device', 'inode', 'mode', 'links', 'bytes', 'mtime_ns', 'ctime_ns')
ORIGINAL = {'bytes': 95725918, 'sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'}
CANDIDATE = {'bytes': 94683119, 'sha256': '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'}
MANIFESTS = {
    'original': 'vendor/original/manifest.json',
    'candidate': 'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
}
TOOL_METADATA = (
    'jdk21/release', 'android/platform-tools/source.properties',
    'android/emulator/source.properties',
    'android/system-images/android-35/google_apis/x86_64/source.properties',
    'android/system-images/android-35/google_apis/x86_64/build.prop',
    'android-user/avd/MacroDroid_API35_Disposable.ini',
    'android-user/avd/MacroDroid_API35_Disposable.avd/config.ini',
)
TOOL_BINARIES = ('jdk21/bin/java', 'jdk21/bin/javac', 'android/platform-tools/adb',
                 'android/emulator/emulator',
                 'android/emulator/qemu/linux-x86_64/qemu-system-x86_64-headless')


class Invalid(ValueError):
    pass


def require(value, message):
    if not value:
        raise Invalid(message)


def now_ns():
    return time.monotonic_ns()


def utc():
    return datetime.now(timezone.utc).isoformat()


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def file_identity(path):
    with Path(path).open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': digest}


def bytes_json(value):
    return json.dumps(value, indent=2).encode() + b'\n'


def stats(value):
    return dict(zip(FIELDS, (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                            value.st_size, value.st_mtime_ns, value.st_ctime_ns)))


def canonical_name(name):
    require(type(name) is str and name != '', 'Artifact path must be a nonempty string')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and '\\' not in name
            and path.as_posix() == name, 'Noncanonical artifact path: ' + name)
    return path


def checked_path(root, name):
    canonical_name(name)
    root = Path(root).resolve()
    path = root / name
    require(path.resolve() == path and path.is_file() and not path.is_symlink(),
            'Missing, symbolic or unconfined file: ' + name)
    return path


def json_file(path):
    return json.loads(Path(path).read_bytes())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.pending-' + str(now_ns()))
    with temp.open('xb') as stream:
        stream.write(bytes_json(value))
    temp.replace(path)


def protocol():
    value = json_file(HERE / 'protocol.json')
    require(value['kind'] == 'FIXED_INDICATOR_DIAGNOSTIC_V1', 'Wrong diagnostic protocol')
    require(value['original_apk'] == ORIGINAL and value['candidate_apk'] == CANDIDATE,
            'Fixed diagnostic APK identities changed')
    require([(s['condition'], s['apk'], s['animator_duration_scale']) for s in value['slots']] == [
        ('A', 'original', '0'), ('A', 'candidate', '0'), ('A', 'candidate', '0'), ('A', 'original', '0'),
        ('B', 'original', '1'), ('B', 'candidate', '1'), ('B', 'candidate', '1'), ('B', 'original', '1')],
        'Eight-slot condition/order changed')
    require(value['schedule']['sample_indices'] == [0, 1, 2, 3, 4]
            and value['schedule']['post_input_wait_ns'] == 2_000_000_000
            and value['schedule']['inter_observation_wait_ns'] == 1_000_000_000,
            'Fixed sampling schedule changed')
    pins = json_file(HERE / 'pins.json')
    require(identity((HERE / 'protocol.json').read_bytes()) == pins['protocol'],
            'Protocol bytes differ from their reviewed pin')
    return value


def load_parents(root):
    root = Path(root).resolve()
    pins = json_file(HERE / 'pins.json')
    require(pins['parent_commit'] == PARENT_COMMIT and len(pins['parents']) == 16,
            'The sixteen declared parent inputs changed')
    for row in pins['parents']:
        path = checked_path(root, row['path'])
        require(file_identity(path) == {k: row[k] for k in ('bytes', 'sha256')},
                'Pinned parent changed: ' + row['path'])
    tools_dir = root / GUARD / 'tools/parity_journeys'
    project = root / GUARD / 'project'
    sys.path[:0] = [str(tools_dir), str(project)]
    modules = {}
    for name, folder in [('android_compare', project), ('android_acceptance', project),
                         ('editor_journey', tools_dir), ('observed_journey', tools_dir)]:
        module = importlib.import_module(name)
        require(Path(module.__file__).resolve() == folder / (name + '.py'), 'Unexpected parent import: ' + name)
        modules[name] = module
    name = 'indicator_parent_radio'
    path = root / 'tools/android/configure_capture_device.py'
    spec = importlib.util.spec_from_file_location(name, path)
    radio = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(radio)
    modules['radio'] = radio
    return modules


def expected_environment(scale):
    return {
        'serial': SERIAL,
        'ro.build.fingerprint': FINGERPRINT,
        'ro.build.version.sdk': '35', 'ro.product.cpu.abilist': 'x86_64,arm64-v8a',
        'ro.kernel.qemu': '1', 'ro.dalvik.vm.native.bridge': 'libndk_translation.so',
        'persist.sys.locale': '', 'persist.sys.timezone': 'Etc/UTC',
        'system:font_scale': '1.0', 'global:animator_duration_scale': scale,
        'global:window_animation_scale': '0', 'global:transition_animation_scale': '0',
        'global:airplane_mode_on': '0', 'global:wifi_on': '1', 'global:mobile_data': '1',
        'global:sysui_demo_allowed': '1', 'global:sysui_tuner_demo_on': '1',
        'display_size': 'Physical size: 720x1280', 'display_density': 'Physical density: 320',
    }


def regular_one_link(value):
    return (type(value) is dict and set(value) == set(FIELDS)
            and all(type(value[k]) is int for k in FIELDS)
            and stat.S_ISREG(value['mode']) and value['links'] == 1
            and value['bytes'] >= 0 and value['inode'] > 0)


def clock_interval(start, end, label):
    require(type(start) is int and type(end) is int and 0 <= start <= end,
            'Invalid monotonic interval: ' + label)


def canonical_component(text, proof):
    values = proof.resumed_components(text)
    require(len(values) == 1, 'Exactly one resumed component is required')
    package, name = values[0].split('/', 1)
    return package + '/' + (package + name if name.startswith('.') else name)


def single_pid(text, proof):
    values = proof.live_pids(text, text)
    require(len(values) == 1, 'Exactly one main process is required')
    return values[0]


def surface_identity(xml, surface, parents):
    """Observed title/indicator and input ancestry; other XML remains measured."""
    require(surface in ('intro1', 'intro2'), 'Undeclared observation surface')
    runner = parents['editor_journey']
    root = runner.tree(xml, PACKAGE)
    filename = 'original-intro1-preinput.xml' if surface == 'intro1' else 'original-intro2.xml'
    frozen = runner.tree((HERE / 'fixtures' / filename).read_bytes(), PACKAGE)
    selectors = [{'resource-id': PACKAGE + ':id/titleText', 'text': 'MACRODROID' if surface == 'intro1' else 'TRIGGERS'},
                 {'resource-id': PACKAGE + ':id/indicator'}]
    if surface == 'intro1':
        selectors.append({'resource-id': PACKAGE + ':id/button_next', 'content-desc': 'Next'})

    def chain(tree, selector):
        node = runner.select(tree, PACKAGE, selector)
        links = {child: parent for parent in tree.iter() for child in parent}
        values = []
        while True:
            values.append((node.tag, tuple(sorted(node.attrib.items()))))
            if node not in links:
                break
            node = links[node]
        return tuple(values)

    for selector in selectors:
        require(chain(root, selector) == chain(frozen, selector),
                'Observed node/ancestor/bounds identity differs: ' + repr(selector))
    indicator = runner.select(root, PACKAGE, {'resource-id': PACKAGE + ':id/indicator'})
    require(indicator.get('bounds') == '[128,1184][592,1200]', 'Observed indicator bounds changed')
    if surface == 'intro1':
        require(runner.target(xml, PACKAGE, selectors[-1], 720, 1280) == [640, 1152],
                'Observed NEXT target changed')
    return runner.canonical(root)
