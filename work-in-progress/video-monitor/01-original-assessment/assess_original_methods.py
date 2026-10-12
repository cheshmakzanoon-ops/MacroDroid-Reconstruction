#!/usr/bin/env python3
"""Bind the fresh registry and inspect original DEX metadata outside active roots."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
PROJECT = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
APK = ROOT.parent / 'recovered/automation android app'
JAVA = ROOT.parent / 'tooling/jdk21/bin'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    output = ROOT / 'reports/original-inventory-01'
    output.mkdir(parents=True, exist_ok=False)
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'status': 'RUNNING',
        'scope': 'Read-only original DEX metadata and a test-only one-method fixture; no app execution or registration.',
        'android_executed': False, 'commands': [], 'source_classes': []}
    try:
        result['original_apk'] = identity(APK)
        registry = PROJECT / 'source/java-method-map.json'
        result['fresh_registry'] = identity(registry)
        if (result['original_apk']['sha256'] != '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800' or
                result['fresh_registry']['sha256'] != '73a37f1ac4148c03a1dc0df9810e899ebb8ff7bcc6f1df7c1672fd525d66a20e'):
            raise RuntimeError('Original APK or fresh registry changed')
        actual_registered = json.loads(registry.read_text())
        registered = {row['target'] + '->' + row['method'] for row in actual_registered}
        if len(registered) != 1242:
            raise RuntimeError('Expected exact 1,242-body baseline')
        metadata = json.loads((ROOT / 'remaining-method-metadata.json').read_text())
        selection = []
        aliases = []
        for index, row in enumerate(metadata['remaining']):
            owner = row['class']
            source = PROJECT / owner['path']
            if sha(source) != owner['sha256']:
                raise RuntimeError('Preserved class bytes changed')
            methods = row['methods']
            if owner['descriptor'] == 'Lcom/arlosoft/macrodroid/common/SelectableItem;':
                methods = [entry for entry in methods if entry['signature'] == 'checkAllPermissions(Z)Z']
            if not methods and 'm665SliderValueTextcf5BqRc' in row['marker']:
                signature = 'SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V'
                methods = [{'signature': signature}]
                aliases.append({'reference_marker': row['marker'], 'actual_dex_signature': signature,
                    'scope': 'Explicit decompiler name alias resolved from preserved class; no method is missing.'})
            if len(methods) != 1:
                raise RuntimeError('Marker did not select exactly one original signature')
            signature = methods[0]['signature']
            key = owner['descriptor'] + '->' + signature
            if key in registered:
                raise RuntimeError('Proposed method already has a registered replacement')
            pattern = re.compile(r'^\.method [^\n]*' + re.escape(signature) + r'\n.*?^\.end method', re.M | re.S)
            matches = list(pattern.finditer(source.read_text()))
            if len(matches) != 1:
                raise RuntimeError('Original method source is ambiguous or absent')
            body = matches[0].group(0)
            body_sha = hashlib.sha256(body.encode()).hexdigest()
            if methods[0].get('method_sha256', body_sha) != body_sha:
                raise RuntimeError('Exact method-body source hash changed')
            copy = output / 'original-methods' / ('%02d.smali' % index)
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_text(body + '\n')
            selection.append({'target': owner['descriptor'], 'method': signature,
                'reference_marker': row['marker'], 'smali_path': owner['path'],
                'smali_class_sha256': owner['sha256'], 'method_body_sha256': body_sha,
                'method_source_file': identity(copy)})
            result['source_classes'].append(identity(source))
        if len(selection) != 21:
            raise RuntimeError('Fresh remaining-marker count differs')
        selected_path = output / 'selected-methods.json'
        save(selected_path, selection)
        result['aliases'] = aliases
        jar = PROJECT / 'tools/lib/jadx-r2721.4574686-all.jar'
        result['tool_jar'] = identity(jar)
        result['inventory_source'] = identity(ROOT / 'OriginalMethodInventory.java')
        source_copy = output / 'OriginalMethodInventory.java'
        shutil.copyfile(ROOT / 'OriginalMethodInventory.java', source_copy)
        classes = output / 'classes'
        classes.mkdir()

        def run(label, argv):
            before = time.monotonic()
            with (output / (label + '.stdout.txt')).open('wb') as out, (output / (label + '.stderr.txt')).open('wb') as err:
                completed = subprocess.run([str(item) for item in argv], stdout=out, stderr=err, timeout=180)
            entry = {'argv': [str(item) for item in argv], 'returncode': completed.returncode,
                'timeout_seconds': 180, 'seconds': round(time.monotonic() - before, 6)}
            result['commands'].append(entry)
            if completed.returncode:
                raise RuntimeError('Read-only inventory command failed: ' + label)

        run('compile-inventory', [JAVA / 'javac', '-cp', jar, '-d', classes, source_copy])
        run('inspect-original-dex', [JAVA / 'java', '-Xmx768m', '-cp', str(jar) + ':' + str(classes),
            'OriginalMethodInventory', APK, selected_path, output / 'dex-method-metadata.json',
            output / 'original-video-monitor.dex'])
        observed = json.loads((output / 'dex-method-metadata.json').read_text())
        if observed['selected_methods'] != 21 or len(observed['methods']) != 21:
            raise RuntimeError('Original DEX inventory omitted a selected method')
        oracle = PROJECT / 'tests/java/BytecodeOracle.java'
        oracle_source = oracle.read_text()
        explicit = set(re.findall(r'case "([A-Z0-9_]+)"\s*:', oracle_source))
        for row in observed['methods']:
            row['unhandled_opcode_names_in_current_oracle'] = sorted(
                opcode for opcode in row['opcodes'] if opcode not in explicit and
                not opcode.startswith('INVOKE_') and not opcode.endswith('_PAYLOAD'))
            row['opcode_scan_is_not_execution_proof'] = True
        save(output / 'dex-method-metadata.json', observed)
        result['oracle_source'] = identity(oracle)
        result['fixture'] = identity(output / 'original-video-monitor.dex')
        result['fixture']['test_only_not_app_input'] = True
        result['metadata'] = identity(output / 'dex-method-metadata.json')
        if sha(APK) != result['original_apk']['sha256'] or sha(registry) != result['fresh_registry']['sha256']:
            raise RuntimeError('APK or active registry changed during read-only assessment')
        for row in result['source_classes']:
            if sha(Path(row['path'])) != row['sha256']:
                raise RuntimeError('Preserved source changed during assessment')
        result['status'] = 'EXACT_21_METHOD_ORIGINAL_DEX_METADATA_RECORDED'
        result['registered_method_count_unchanged'] = 1242
    except Exception as error:
        result['status'] = 'ASSESSMENT_FAILED'
        result['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
