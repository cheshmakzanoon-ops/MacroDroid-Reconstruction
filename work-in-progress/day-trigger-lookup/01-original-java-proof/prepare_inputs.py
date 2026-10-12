#!/usr/bin/env python3
"""Capture a small, explicit set of preserved production inputs; never touch the repository."""
from pathlib import Path
import hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent / 'current/MacroDroid_v9'
INPUTS = ROOT / 'inputs'
SELECTED = {
    'Lcom/arlosoft/macrodroid/triggers/DayTrigger;': 'p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;': 'getEntries()Ljava/util/List;',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;': 'getKey()Ljava/lang/String;',
}
ACTIVE = ROOT.parent / 'MacroDroid-Reconstruction/project'


def identity(path):
    content = path.read_bytes()
    return {'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}

def copy(source, target):
    if target.exists():
        raise RuntimeError('Existing input must not be overwritten: ' + str(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert identity(source) == identity(target)

def main():
    copy(ACTIVE / 'tests/java/BytecodeOracle.java', INPUTS / 'BytecodeOracle.java')
    for name in ('build.py', 'constructor_owner.py'):
        copy(PROJECT / name, INPUTS / 'production-pipeline' / name)
    index = json.loads((PROJECT / 'source/class-index.json').read_text())
    selected = {key: row for key, row in index.items() if row['descriptor'] in SELECTED}
    assert len(selected) == len(SELECTED)
    rows = []
    method_pattern = re.compile(r'^\.method [^\n]*\n.*?^\.end method', re.M | re.S)
    for row in selected.values():
        source = PROJECT / row['path']
        target = INPUTS / 'production-pipeline' / row['path']
        copy(source, target)
        method = [m.group() for m in method_pattern.finditer(source.read_text())
                  if m.group().splitlines()[0].split()[-1] == SELECTED[row['descriptor']]]
        assert len(method) == 1
        rows.append({'descriptor': row['descriptor'], 'method': SELECTED[row['descriptor']],
                     'sourcePath': row['path'], 'sourceIdentity': identity(source),
                     'methodTextSha256': hashlib.sha256(method[0].encode()).hexdigest()})
    (INPUTS / 'production-pipeline/source/class-index-selected.json').write_text(json.dumps(selected, indent=2) + '\n')
    registry = json.loads((ACTIVE / 'source/java-method-map.json').read_text())
    assert not any(row['target'] == 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;'
                   and row['method'] == SELECTED[row['target']] for row in registry)
    pins = {'scope': 'One private, unregistered DayTrigger dictionary lookup method; source and production helpers are read-only copies.',
            'selectedOriginalMethods': sorted(rows, key=lambda row: row['descriptor']),
            'originalApk': {'path': str(ROOT.parent / 'recovered/automation android app'),
                            **identity(ROOT.parent / 'recovered/automation android app')},
            'externalToolchainJar': {'path': str(PROJECT / 'tools/lib/jadx-r2721.4574686-all.jar'),
                                    **identity(PROJECT / 'tools/lib/jadx-r2721.4574686-all.jar')},
            'externalJdkRelease': {'path': str(ROOT.parent / 'tooling/jdk21/release'),
                                  **identity(ROOT.parent / 'tooling/jdk21/release')},
            'copiedBytecodeOracle': identity(INPUTS / 'BytecodeOracle.java'),
            'copiedBuild': identity(INPUTS / 'production-pipeline/build.py'),
            'copiedConstructorOwner': identity(INPUTS / 'production-pipeline/constructor_owner.py'),
            'registrationChanged': False, 'apkChanged': False}
    (INPUTS / 'preserved-input-pins.json').write_text(json.dumps(pins, indent=2) + '\n')
    print(json.dumps({'status': 'PRIVATE_INPUTS_CAPTURED', 'originalMethods': len(rows),
                      'pins': identity(INPUTS / 'preserved-input-pins.json')}, indent=2))

if __name__ == '__main__': main()
