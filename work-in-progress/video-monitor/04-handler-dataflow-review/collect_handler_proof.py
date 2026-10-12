#!/usr/bin/env python3
"""Collect exact original operands and primary constructor sources without new app execution."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
JDK = HERE.parent / 'tooling/jdk21'
JAR = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    output = HERE / 'reports/handler-dataflow-04'
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'COLLECTING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Original instruction operands, exact installed JDK sources/classfiles, and primary Android15 source; no app execution or coverage credit.',
        'app_method_executed': False, 'android_executed': False, 'coverage_gate_changed': False,
        'commands': [], 'sources': []}
    try:
        host = output / 'host-sources';host.mkdir()
        shutil.copyfile(JDK / 'release', host / 'release')
        archive = JDK / 'lib/src.zip'
        report['installed_source_archive'] = {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)}
        with zipfile.ZipFile(archive) as source:
            for name in ('StringBuilder.java', 'AbstractStringBuilder.java', 'StringUTF16.java'):
                entry = 'java.base/java/lang/' + name
                data = source.read(entry);(host / name).write_bytes(data)
                report['sources'].append({'kind': 'installed-jdk-source', 'archive_entry': entry,
                    'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'path': 'host-sources/' + name})
        android = output / 'android15-primary';android.mkdir()

        def fetch(name):
            view = 'https://android.googlesource.com/platform/libcore/+/refs/tags/android-15.0.0_r1/ojluni/src/main/java/java/lang/' + name
            url = view + '?format=TEXT'
            started = time.monotonic()
            try:
                with urllib.request.urlopen(url, timeout=30) as response:
                    raw = response.read();code = response.status
                data = base64.b64decode(raw, validate=True)
                if code != 200 or b'package java.lang;' not in data:
                    raise RuntimeError('Unexpected primary source response')
                (android / (name + '.response-base64.txt')).write_bytes(raw)
                (android / name).write_bytes(data)
                return {'kind': 'primary-android15-tag-source', 'view_url': view, 'request_url': url,
                    'http_status': code, 'timeout_seconds': 30, 'seconds': round(time.monotonic() - started, 3),
                    'path': 'android15-primary/' + name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'response_bytes': len(raw), 'response_sha256': hashlib.sha256(raw).hexdigest(),
                    'scope': 'Pinned AOSP15 source, not a byte-for-byte extraction of the hosted Google APIs image boot library'}
            except Exception as error:
                return {'kind': 'primary-android15-tag-source', 'request_url': url, 'error': type(error).__name__ + ': ' + str(error), 'passed': False}
        with ThreadPoolExecutor(max_workers=3) as pool:
            report['sources'].extend(list(pool.map(fetch, ('StringBuilder.java', 'AbstractStringBuilder.java', 'StringUTF16.java'))))
        source = output / 'VideoHandlerInventory.java';shutil.copyfile(HERE / source.name, source)
        classes = output / 'toolclasses';classes.mkdir()
        fixture = HERE / 'reports/original-jvm-03-initial/original-video-monitor.dex'
        report['original_fixture'] = {'path': str(fixture), 'bytes': fixture.stat().st_size, 'sha256': sha(fixture)}
        def run(label, command):
            out, err = output / (label + '.stdout.txt'), output / (label + '.stderr.txt')
            started = time.monotonic()
            with out.open('wb') as stdout, err.open('wb') as stderr:
                completed = subprocess.run([str(value) for value in command], stdout=stdout, stderr=stderr, timeout=180)
            report['commands'].append({'label': label, 'argv': [str(value) for value in command],
                'returncode': completed.returncode, 'timeout_seconds': 180, 'seconds': round(time.monotonic() - started, 6),
                'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
            if completed.returncode != 0:
                raise RuntimeError(label + ' failed')
        run('compile-inventory', [JDK / 'bin/javac', '-cp', JAR, '-d', classes, source])
        run('inspect-original-and-jrt', [JDK / 'bin/java', '-cp', str(JAR) + ':' + str(classes), 'VideoHandlerInventory', fixture, output])
        for name in ('StringBuilder', 'AbstractStringBuilder', 'StringUTF16', 'Object'):
            run('javap-' + name, [JDK / 'bin/javap', '-c', '-p', '-s', output / 'jrt-classfiles' / (name + '.class')])
        report['art08_device_environment'] = json.loads((HERE.parent / 'widget-art-probe/hosted-run-38209599059/independent-verification/result.json').read_text())['device_environment']
        report['status'] = 'DATAFLOW_INPUTS_COLLECTED' if not any('error' in item for item in report['sources']) else 'DATAFLOW_INPUTS_COLLECTED_WITH_SOURCE_GAPS'
        report['files'] = [{'path': str(path.relative_to(output)), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in sorted(output.rglob('*')) if path.is_file()]
    except Exception as error:
        report['status'] = 'DATAFLOW_COLLECTION_FAILED';report['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({key: value for key, value in report.items() if key not in ('files', 'art08_device_environment')}, indent=2))


if __name__ == '__main__':
    main()
