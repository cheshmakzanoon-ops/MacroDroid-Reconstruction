#!/usr/bin/env python3
"""Compare preserved source with a fresh decode of the exact supplied original APK.

Optional, test-only audit. The original is never an application build input. This
command does not install or execute the APK. All generated files stay in build/.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
import build
from resource_verify import source_files

ORIGINAL_SHA256 = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'

def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def audit(original: Path) -> dict:
    original = original.resolve(strict=True)
    if digest(original) != ORIGINAL_SHA256:
        raise ValueError('Input is not the exact supplied MacroDroid 5.67.8 APK; no comparison performed.')
    root = build.ROOT
    work = root / 'build' / 'fresh-original-audit'
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    expected = build.index()
    seen = set()
    mismatches = []
    method_count = 0
    partition_results = []
    opaque_changes = []
    duplicate_classes = []
    with zipfile.ZipFile(original) as apk:
        if apk.testzip() is not None:
            raise ValueError('Original ZIP CRC failure')
        if len(apk.namelist()) != len(set(apk.namelist())):
            raise ValueError('Original contains duplicate ZIP entries')
        for part in json.loads((root/'source/partitions.json').read_text()):
            dex = work / (part['name'] + '.dex')
            dex.write_bytes(apk.read(part['apk_path']))
            build.dex_integrity(dex)
            target = work / part['name']
            build.java('com.android.tools.smali.baksmali.Main', 'd', '--api', '23',
                       '--use-locals', '-j', '2', '-o', target, dex,
                       log='fresh-original-' + part['name'] + '.log')
            count = 0
            for path in target.rglob('*.smali'):
                raw = path.read_bytes()
                text = raw.decode('utf-8')
                descriptor = next(line.rsplit(' ', 1)[-1] for line in text.splitlines()
                                  if line.startswith('.class '))
                key = part['name'] + ':' + descriptor
                if key in seen:
                    duplicate_classes.append(key)
                seen.add(key)
                count += 1
                method_count += len(build.methods(text))
                if key not in expected:
                    continue
                preserved = root / expected[key]['path']
                if raw != preserved.read_bytes():
                    mismatches.append(key)
            partition_results.append({'name': part['name'], 'original_dex_sha256': digest(dex),
                                      'classes': count, 'expected_classes': part['class_count']})
            print('Fresh original:', part['name'], count, 'classes', flush=True)
        with zipfile.ZipFile(root/'source/payload.zip') as payload:
            for name in payload.namelist():
                if name not in apk.namelist() or payload.read(name) != apk.read(name):
                    opaque_changes.append(name)
        compression = json.loads((root/'source/zip-compression.json').read_text())
        def signature(name: str) -> bool:
            return name == 'META-INF/MANIFEST.MF' or (name.startswith('META-INF/') and name.upper().endswith(('.RSA','.DSA','.EC','.SF')))
        names = {name for name in apk.namelist() if not signature(name)}
        compression_changes = [name for name in names & compression.keys()
                               if apk.getinfo(name).compress_type != compression[name]]
    decoded = work/'android'
    build.run(['java','-Xmx1200m','-jar',build.APKTOOL,'d','-s','--no-assets','-f',
               '-o',decoded,original], 'fresh-original-decode-resources.log')
    preserved_files = source_files(root/'source/android')
    fresh_files = source_files(decoded)
    resource_changes = [name for name in preserved_files.keys() & fresh_files.keys()
                        if preserved_files[name].read_bytes() != fresh_files[name].read_bytes()]
    build.run([build.aapt(),'dump','resources',original], 'fresh-original-resource-table.txt')
    table = (root/'reports/fresh-original-resource-table.txt').read_text()
    actual_ids = {name: rid for rid, name in re.findall(r'^    resource (0x[0-9a-f]+) ([^\s]+)',table,re.M)}
    expected_ids = {line.split(':',1)[1].split(' = ')[0]:line.split(' = ')[1].strip()
                    for line in (root/'source/android/stable-ids.txt').read_text().splitlines()}
    original_public = set(json.loads((root/'source/android/original-public-resources.json').read_text())['public_resources'])
    actual_public = set(re.findall(r'^    resource 0x[0-9a-f]+ (\S+) PUBLIC',table,re.M))
    source_hash_errors = [key for key, value in expected.items()
                          if digest(root/value['path']) != value['sha256']]
    report = {
        'original_sha256': ORIGINAL_SHA256, 'original_is_build_input': False,
        'android_runtime_executed': False, 'classes_compared': len(seen),
        'method_definitions_compared': method_count, 'partitions': partition_results,
        'changed_classes': sorted(mismatches), 'missing_classes': sorted(expected.keys()-seen),
        'extra_classes': sorted(seen-expected.keys()), 'duplicate_classes': duplicate_classes,
        'source_index_hash_mismatches': source_hash_errors,
        'resource_files_compared': len(fresh_files), 'resource_byte_changes': sorted(resource_changes),
        'missing_resource_files': sorted(preserved_files.keys()-fresh_files.keys()),
        'extra_resource_files': sorted(fresh_files.keys()-preserved_files.keys()),
        'resource_ids_compared': len(actual_ids), 'resource_ids_identical': actual_ids == expected_ids,
        'resource_visibility_identical': original_public == actual_public,
        'opaque_payload_changes': opaque_changes, 'non_signature_entries': len(names),
        'missing_payload_entries': sorted(compression.keys()-names),
        'extra_payload_entries': sorted(names-compression.keys()),
        'changed_zip_compression': sorted(compression_changes),
    }
    report['pass'] = all(not report[key] for key in [
        'changed_classes','missing_classes','extra_classes','duplicate_classes',
        'source_index_hash_mismatches','resource_byte_changes','missing_resource_files',
        'extra_resource_files','opaque_payload_changes','missing_payload_entries',
        'extra_payload_entries','changed_zip_compression']) and report['resource_ids_identical'] and report['resource_visibility_identical']
    (root/'reports/fresh-original-source-audit-v9.json').write_text(json.dumps(report,indent=2))
    if not report['pass']:
        raise RuntimeError('Fresh original-source comparison failed; see reports/fresh-original-source-audit-v9.json')
    print(json.dumps({key:value for key,value in report.items() if not isinstance(value,(list,dict))},indent=2))
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_apk', type=Path)
    args=parser.parse_args()
    build.bootstrap()
    audit(args.original_apk)

if __name__ == '__main__':
    main()
