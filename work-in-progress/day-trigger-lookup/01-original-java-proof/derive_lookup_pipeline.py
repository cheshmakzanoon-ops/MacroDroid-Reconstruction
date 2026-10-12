#!/usr/bin/env python3
"""Derive the bounded lookup study tools from the closed numeric study tools."""
from pathlib import Path
import difflib
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'day-trigger-numeric-recovery/checkpoints/01-original-java-proof'
PARENT_SHA = '6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e'


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    if identity(PARENT / 'checkpoint.json')['sha256'] != PARENT_SHA:
        raise ValueError('The frozen numeric study parent changed')
    parent = json.loads((PARENT / 'checkpoint.json').read_text())
    pins = {row['path']: {key: row[key] for key in ('bytes', 'sha256')} for row in parent['sourceFiles']}
    inputs = ROOT / 'inputs'
    inputs.mkdir(parents=True, exist_ok=True)
    changes, patch = [], ''

    def derive(name, relative, modify):
        source = PARENT / name
        if identity(source) != pins[name]:
            raise ValueError('The bound source differs: ' + name)
        target = ROOT / relative
        if target.exists():
            raise ValueError('A derived study file already exists: ' + relative)
        before = source.read_text()
        after = modify(before)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(after)
        changes.append({'parent_path': name, 'path': relative, 'before': pins[name], 'after': identity(target)})
        return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                          fromfile='numeric/' + name, tofile='lookup/' + relative))

    def prepare(text):
        start, end = text.index('SELECTED = {'), text.index('\n\ndef identity')
        text = text[:start] + '''SELECTED = {
    'Lcom/arlosoft/macrodroid/triggers/DayTrigger;': 'p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;': 'getEntries()Ljava/util/List;',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;': 'getKey()Ljava/lang/String;',
}
ACTIVE = ROOT.parent / 'MacroDroid-Reconstruction/project'
''' + text[end:]
        text = text.replace("copy(PROJECT / 'tests/java/BytecodeOracle.java'", "copy(ACTIVE / 'tests/java/BytecodeOracle.java'")
        text = text.replace("(PROJECT / 'source/java-method-map.json')", "(ACTIVE / 'source/java-method-map.json')")
        text = text.replace('DayTrigger numeric method', 'DayTrigger dictionary lookup method')
        return text

    def extract(text):
        text = text.replace('ExtractDayFixture', 'ExtractDayLookupFixture')
        start, end = text.index('        Map<String, String> wanted = Map.of('), text.index('\n        var container')
        text = text[:start] + '''        Map<String, String> wanted = Map.of(
            "Lcom/arlosoft/macrodroid/triggers/DayTrigger;", "p0(" + variables + "$Dictionary;Ljava/lang/String;)" + variables + "$DictionaryEntry;",
            variables + "$Dictionary;", "getEntries()Ljava/util/List;",
            variables + "$DictionaryEntry;", "getKey()Ljava/lang/String;");''' + text[end:]
        return text.replace('three original field getters', 'two original field getters').replace('Extracted four exact original methods', 'Extracted three exact original methods')

    def runner(text):
        for old, new in [('DayValueStudy', 'DayLookupStudy'), ('ExtractDayFixture', 'ExtractDayLookupFixture'),
                         ('DayTriggerValueMethods', 'DayTriggerLookupMethods')]:
            text = text.replace(old, new)
        # Bind the exact complete Java module image used by String/collection dependencies.
        text = text.replace("for role in ('java', 'javac'):", "for role in ('java', 'javac'):")
        anchor = "    (output / 'external-input-identities.json').write_text"
        position = text.index(anchor)
        text = text[:position] + "    external['jdkModules'] = {'path': str(JDK / 'lib/modules'), **identity(JDK / 'lib/modules')}\n" + text[position:]
        return text

    patch += derive('prepare_inputs.py', 'prepare_inputs.py', prepare)
    patch += derive('run_day_study.py', 'run_day_study.py', runner)
    patch += derive('inputs/ExtractDayFixture.java', 'inputs/ExtractDayLookupFixture.java', extract)
    for name in ('EngineRuntime.java', 'TestClock.java'):
        relative = 'inputs/host/defpackage/' + name
        patch += derive(relative, relative, lambda text: text)
    # Retain the exact shared provenance/coverage utility source for transparent derivation.
    source = PARENT / 'inputs/DayValueStudy.java'
    if identity(source) != pins['inputs/DayValueStudy.java']:
        raise ValueError('Bound provenance/coverage utility source changed')
    target = ROOT / 'parent-study-source.java.txt'
    shutil.copyfile(source, target)
    (ROOT / 'derivation.patch').write_text(patch)
    (ROOT / 'parent-source-identities.json').write_text(json.dumps({'parent_checkpoint_sha256': PARENT_SHA,
        'changes': changes, 'utility_source': identity(target), 'android_executed': False,
        'active_registration_changed': False}, indent=2) + '\n')
    print(json.dumps({'status': 'PRIVATE_LOOKUP_PIPELINE_DERIVED', 'derived_files': len(changes)}, indent=2))


if __name__ == '__main__':
    main()
