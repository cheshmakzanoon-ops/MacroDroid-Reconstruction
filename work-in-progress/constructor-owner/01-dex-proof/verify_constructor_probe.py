#!/usr/bin/env python3
"""Compile, transform and round-trip a standalone constructor-owner probe.

The original APK is read-only. Only the probe class enters its separate DEX; all
referenced application classes must come from the original APK in a later ART run.
This command never installs, changes or executes an Android application.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import zipfile

from constructor_owner import digest, restore_constructor_owners


ORIGINAL_SHA = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
METHOD = 'm(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = args.source.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    if sha(args.original) != ORIGINAL_SHA:
        raise ValueError('Unexpected original APK identity')
    specification = importlib.util.spec_from_file_location('probe_build_support', root / 'build.py')
    build = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(build)
    java, javac = (str(args.java_home / 'bin' / name) for name in ('java', 'javac'))
    bundle = root / 'tools/lib/jadx-r2721.4574686-all.jar'
    apktool = root / 'tools/apktool_v3.0.3-26-0a1c54f7-SNAPSHOT.jar'
    report = {'scope': 'Standalone constructor owner compilation and DEX roundtrip only',
              'android_executed': False, 'app_apk_modified': False,
              'original_apk_sha256': ORIGINAL_SHA, 'pass': False, 'commands': []}
    def save():
        (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    def run(label, argv):
        result = subprocess.run(list(map(str, argv)), capture_output=True, text=True, timeout=180)
        log = out / (label + '.log')
        log.write_text('COMMAND: ' + json.dumps(list(map(str, argv))) + '\n' + result.stdout + '\n' + result.stderr)
        report['commands'].append({'label': label, 'exit_code': result.returncode, 'log': log.name, 'log_sha256': sha(log)})
        save()
        if result.returncode:
            raise RuntimeError(label + ' failed; see ' + str(log))
        return result.stdout
    save()
    run('original-disassembly', [java, '-cp', apktool, here / 'InspectOriginalConstructor.java', args.original, out / 'original'])
    originals = {
        'WidgetUpdateManager.smali': 'source/smali/classes/67/WidgetUpdateManager_6791e8994482f6df.smali',
        'zhh.smali': 'source/smali/classes/c2/Lzhh_c22737dc2c4c675a.smali',
        'rff.smali': 'source/smali/classes7/d2/Lrff_d2448d30d4685e58.smali'}
    report['original_classes'] = []
    for name, reference in originals.items():
        actual = out / 'original' / name
        if actual.read_bytes() != (root / reference).read_bytes():
            raise ValueError('Original APK class differs from preserved source: ' + name)
        report['original_classes'].append({'source_path': reference, 'sha256': sha(actual), 'byte_identical': True})
    original = build.methods((out / 'original/WidgetUpdateManager.smali').read_text())[METHOD]
    (out / 'original-widget-method.smali').write_text(original)
    host = out / 'hostclasses'
    host.mkdir()
    sources = sorted((here / 'probe').rglob('*.java'))
    run('javac', [javac, '--release', '8', '-g:none', '-d', host, *sources])
    host_output = run('host-allocation', [java, '-cp', host, 'recovered.probe.ConstructorProbe'])
    if host_output.strip() != 'CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2':
        raise ValueError('Unexpected host probe result')
    classes = sorted((host / 'recovered').rglob('*.class'))
    if [path.relative_to(host).as_posix() for path in classes] != ['recovered/probe/ConstructorProbe.class']:
        raise ValueError('Unexpected probe runtime class set')
    inputs = out / 'probe-inputs.jar'
    with zipfile.ZipFile(inputs, 'w') as archive:
        for path in classes:
            archive.writestr(path.relative_to(host).as_posix(), build.relocate_class(path.read_bytes()))
    dex = out / 'compiled-dex'
    dex.mkdir()
    run('d8', [java, '-cp', bundle, 'com.android.tools.r8.D8', '--release', '--no-desugaring', '--min-api', '23', '--output', dex, inputs])
    smali = out / 'compiled-smali'
    run('compiled-disassembly', [java, '-cp', bundle, 'com.android.tools.smali.baksmali.Main', 'd', '--api', '23', '--use-locals', '-o', smali, dex / 'classes.dex'])
    emitted = list(smali.rglob('*.smali'))
    if len(emitted) != 1:
        raise ValueError('Compile-only classes leaked into the probe DEX')
    source = emitted[0]
    before = source.read_text()
    signature = 'allocate()Lzhh;'
    compiled = build.methods(before)[signature]
    entry = {'original_method_sha256': digest(original), 'constructor_owner_mappings': [
        {'allocated_type': 'Lzhh;', 'original_owner': 'Lrff;', 'constructor': '<init>(ILm73;)V', 'occurrences': 1}]}
    lookup = {'Lzhh;': (out / 'original/zhh.smali').read_text(), 'Lrff;': (out / 'original/rff.smali').read_text()}
    transformed, evidence = restore_constructor_owners(entry, compiled, original, lookup.__getitem__)
    rewritten = before.replace(compiled, transformed, 1)
    if rewritten.replace('Lrff;-><init>(ILm73;)V', 'Lzhh;-><init>(ILm73;)V', 1) != before:
        raise ValueError('Probe transformation changed more than one constructor owner')
    patched = out / 'patched-smali/recovered/probe/ConstructorProbe.smali'
    patched.parent.mkdir(parents=True)
    patched.write_text(rewritten)
    probe_dex = out / 'constructor-probe.dex'
    run('assemble-transformed-probe', [java, '-cp', bundle, 'com.android.tools.smali.smali.Main', 'a', '--api', '23', '-o', probe_dex, out / 'patched-smali'])
    roundtrip = out / 'roundtrip-smali'
    run('transformed-roundtrip', [java, '-cp', bundle, 'com.android.tools.smali.baksmali.Main', 'd', '--api', '23', '--use-locals', '-o', roundtrip, probe_dex])
    recovered = roundtrip / 'recovered/probe/ConstructorProbe.smali'
    if recovered.read_text() != rewritten:
        raise ValueError('Transformed probe did not survive the DEX roundtrip byte-for-byte')
    if len(list(roundtrip.rglob('*.smali'))) != 1:
        raise ValueError('Unexpected class added to transformed probe')
    report.update(pass_=True, transformations=evidence, runtime_probe_classes=1, compile_only_classes_in_dex=0,
                  probe_dex={'bytes': probe_dex.stat().st_size, 'sha256': sha(probe_dex)},
                  original_method_sha256=digest(original), allocation_type_preserved=True,
                  transformed_smali_roundtrip_byte_identical=True)
    report['pass'] = report.pop('pass_')
    save()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
