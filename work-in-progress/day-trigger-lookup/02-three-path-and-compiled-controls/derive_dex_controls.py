#!/usr/bin/env python3
"""Derive a bounded lookup pipeline from the exact closed numeric D8 study."""
from pathlib import Path
import difflib
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'day-trigger-numeric-recovery/checkpoints/02-three-path-and-compiled-controls'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    checkpoint_path = PARENT / 'checkpoint.json'
    if identity(checkpoint_path)['sha256'] != 'd93f08507afce1b6eebe1e3ae64338f86eb04ca01e26118bdd97f98f5d6af631':
        raise ValueError('Numeric parent checkpoint changed')
    checkpoint = json.loads(checkpoint_path.read_text())
    row = next(item for item in checkpoint['sourceFiles'] if item['path'] == 'run_day_dex_controls.py')
    parent = PARENT / row['path']
    if identity(parent) != {key: row[key] for key in ('bytes', 'sha256')}:
        raise ValueError('Numeric parent operation changed')
    original = parent.read_text()
    text = original
    replacements = {
        "CHECKPOINT_SHA = '6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e'":
            "CHECKPOINT_SHA = '4a39dd17902f68c5cba369fc927f08117ba9905556c7cf2890db8c29e46e9899'",
        "METHOD = 'r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'":
            "METHOD = 'p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;'",
        'DayTriggerValueMethods': 'DayTriggerLookupMethods',
        'DayValueStudy': 'DayLookupStudy',
        'numericValue': 'findEntry',
        'day_bound_production_build': 'day_lookup_bound_production_build',
        'Numeric method must need no constructor-owner correction': 'Lookup method must need no constructor-owner correction',
        "positive['cases'] != 1291": "positive['cases'] != 371",
        "for name, required in [('integer-zero', 'integer-boundary-1'), ('decimal-zero', 'decimal-boundary-6')]:":
            "for name, required in [('case-sensitive', 'first-duplicate-entry-identity'), ('last-match', 'empty-string-match')]:",
    }
    counts = {}
    for old, new in replacements.items():
        count = text.count(old)
        if count == 0:
            raise ValueError('Missing exact derivation anchor: ' + old)
        if old not in ('DayTriggerValueMethods', 'DayValueStudy', 'numericValue', 'day_bound_production_build') and count != 1:
            raise ValueError('Non-unique exact derivation anchor: ' + old)
        counts[old] = count
        text = text.replace(old, new)
    start = text.index("        integer = 'return (int)")
    end = text.index("        (output / 'fault-catalog.json')", start)
    fault_source = r'''        loop = """        for (DictionaryEntry entry : dictionary.getEntries()) {
            if (key.equalsIgnoreCase(entry.getKey())) return entry;
        }
        return null;"""
        faults = [
            ('case-sensitive', 'key.equalsIgnoreCase(entry.getKey())', 'key.equals(entry.getKey())', 'first-duplicate-entry-identity'),
            ('reverse-receiver', 'key.equalsIgnoreCase(entry.getKey())', 'entry.getKey().equalsIgnoreCase(key)', 'null-entry-key-is-not-a-match'),
            ('skip-null-entry', '            if (key.equalsIgnoreCase(entry.getKey())) return entry;',
             '            if (entry == null) continue;\n            if (key.equalsIgnoreCase(entry.getKey())) return entry;', 'null-first-entry'),
            ('null-query-early-return', '        for (DictionaryEntry entry : dictionary.getEntries()) {',
             '        if (key == null) return null;\n        for (DictionaryEntry entry : dictionary.getEntries()) {', 'null-query-nonempty'),
            ('last-match', loop, """        DictionaryEntry match = null;
        for (DictionaryEntry entry : dictionary.getEntries()) {
            if (key.equalsIgnoreCase(entry.getKey())) match = entry;
        }
        return match;""", 'empty-string-match'),
            ('trim-query', 'key.equalsIgnoreCase(entry.getKey())', 'key.trim().equalsIgnoreCase(entry.getKey())', 'query-whitespace-is-significant'),
            ('indexed-loop', loop, """        java.util.List<DictionaryEntry> entries = dictionary.getEntries();
        for (int i = 0; i < entries.size(); i++) {
            DictionaryEntry entry = entries.get(i);
            if (key.equalsIgnoreCase(entry.getKey())) return entry;
        }
        return null;""", 'empty'),
            ('extra-iteration-after-match', loop, """        java.util.Iterator<DictionaryEntry> entries = dictionary.getEntries().iterator();
        while (entries.hasNext()) {
            DictionaryEntry entry = entries.next();
            if (key.equalsIgnoreCase(entry.getKey())) { entries.hasNext(); return entry; }
        }
        return null;""", 'match-before-later-iterator-fault'),
            ('swallow-iterator-fault', loop, '        try {\n' + loop + '\n        } catch (RuntimeException failure) { return null; }', 'injected-iterator-state'),
            ('replace-injected-npe-identity', loop, '        try {\n' + loop + '\n        } catch (NullPointerException failure) { throw new NullPointerException(failure.getMessage()); }', 'injected-iterator-npe'),
        ]
'''
    # The raw outer template preserves Python string escapes. Each inner Java newline
    # escape must be a single backslash in the generated operation source.
    fault_source = fault_source.replace('\\\\n', '\\n')
    text = text[:start] + fault_source + text[end:]
    target = ROOT / 'run_day_dex_controls.py'
    if target.exists():
        raise ValueError('Derived operation already exists')
    target.write_text(text)
    (ROOT / 'dex-controls-derivation.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), text.splitlines(True), fromfile='numeric02/run_day_dex_controls.py',
        tofile='lookup/run_day_dex_controls.py')))
    receipt = {'parentCheckpoint': identity(checkpoint_path), 'parentOperation': identity(parent),
               'lookupBaselineCheckpoint': identity(ROOT / 'checkpoints/01-original-java-proof/checkpoint.json'),
               'replacementCounts': counts, 'compiledJavaFaultsPlanned': 10, 'compiledDexFaultsPlanned': 2,
               'derivedOperation': identity(target), 'androidExecuted': False, 'activeRegistryChanged': False}
    (ROOT / 'dex-controls-derivation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
