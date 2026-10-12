#!/usr/bin/env python3
"""Author the first bounded helper, dependency and identity-observer slice."""
from pathlib import Path
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'stage-01/project'
BASELINE = ROOT / 'stage-01/baseline'
LOOKUP = Path('/workspace/scratch/4130730d15aa/day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls')
KEY = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;'
METHOD_HASH = 'afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e'
HELPER = 'source/java/recovered/ui/DayTriggerLookupMethods.java'

def sha(data): return hashlib.sha256(data).hexdigest()
def save(path, value): path.write_text(json.dumps(value, indent=2) + '\n')
def replace_once(text, old, new):
    assert text.count(old) == 1, old[:100]
    return text.replace(old, new, 1)

def main():
    marker = ROOT / 'stage-01/source-slice.json'
    assert not marker.exists()
    prep = json.loads((ROOT / 'stage-01/preparation.json').read_text())
    for row in prep['copied_baseline_paths']:
        assert sha((PROJECT / row['path']).read_bytes()) == row['baseline']['sha256']
    with tarfile.open(LOOKUP / 'evidence.tar.gz', 'r:gz') as archive:
        positive = json.load(archive.extractfile('positive/parity.json'))
    omitted = {'original', 'java', 'rebuilt', 'sameScopedOutcome', 'allPathsMatchIndependentExpected'}
    inputs = [{key: value for key, value in row.items() if key not in omitted} for row in positive['observations']]
    inventory_bytes = json.dumps(inputs, separators=(',', ':'), ensure_ascii=False).encode()
    inventory_sha = sha(inventory_bytes)
    vm_nulls = sorted(row['case'] for row in inputs if row['injectedFaultAt'] is None and row['expectedExceptionClass'] == 'java.lang.NullPointerException')
    assert len(inputs) == 371 and len(vm_nulls) == 7
    (ROOT / 'stage-01/lookup-input-inventory.compact.json').write_bytes(inventory_bytes)

    helper = (LOOKUP / 'inputs' / HELPER).read_text()
    assert sha(helper.encode()) == 'd3261f820de3d197f947e65b576cb74e40153ab811dc7ed0a907dd06791b00c0'
    helper = replace_once(helper, '/** Private candidate for the original DayTrigger.p0 body; not registered. */',
                          '/** Exact recovery of the original DayTrigger.p0 method body. */')
    (PROJECT / HELPER).write_text(helper)
    entry = {'target': KEY.split('->')[0], 'method': KEY.split('->')[1],
             'helper': 'Lrecovered/ui/DayTriggerLookupMethods;', 'helper_method': 'findEntry',
             'instance': False, 'java_source': HELPER, 'proof_family': 'v9-ui', 'original_method_sha256': METHOD_HASH}
    for path, count in (('source/java-method-map.json', 1243), ('source/ui-methods.json', 11)):
        rows = json.loads((PROJECT / path).read_text()); assert len(rows) == count
        assert all(row['target'] + '->' + row['method'] != KEY for row in rows)
        rows.append(entry); save(PROJECT / path, rows)

    path = PROJECT / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java'
    source = path.read_text()
    source = replace_once(source, 'public Dictionary(List<DictionaryEntry> e,boolean a,List<String> k){entries=e;array=a;keys=k;}',
                          'public Dictionary(List<DictionaryEntry> e,boolean a,List<String> k){entries=e;array=a;keys=k;}public final List<DictionaryEntry> getEntries(){return entries;}')
    source = replace_once(source, 'public final VariableValue getVariable(){return variable;}',
                          'public final VariableValue getVariable(){return variable;}public final String getKey(){return key;}')
    path.write_text(source)

    dep_path = PROJECT / 'tests/fixtures/original-dependencies.json'
    data = json.loads(dep_path.read_text()); assert len(data['dependencies']) == 3
    additions = [
        {'consumer': KEY, 'target': 'Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;',
         'method': 'getEntries()Ljava/util/List;', 'original_method_sha256': 'f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e'},
        {'consumer': KEY, 'target': 'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;',
         'method': 'getKey()Ljava/lang/String;', 'original_method_sha256': '41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3'},
    ]
    data['dependencies'].extend(additions); save(dep_path, data); dep_sha = sha(dep_path.read_bytes())

    java_path = PROJECT / 'tests/java/DayTriggerParityCases.java'
    java = java_path.read_text()
    java = replace_once(java, 'e30552cc8ba0520bbee3a993298cb0bcaa973a9d4633649e80362d35b3eda631', dep_sha)
    start = java.index('    static Set<String> loadDependencies(')
    end = java.index('    static Observed observe(', start)
    rows = []
    for row in data['dependencies']:
        rows.append('            Map.entry(' + json.dumps(row['target'] + '->' + row['method']) + ', ' + json.dumps(row['original_method_sha256']) + ')')
    validation = '''    static final String LOOKUP_KEY = "@LOOKUP_KEY@";
    static final Set<String> LOOKUP_GETTERS = Set.of(
        BASE + "$Dictionary;->getEntries()Ljava/util/List;", BASE + "$DictionaryEntry;->getKey()Ljava/lang/String;");
    static final Map<String, String> DECLARED_GETTER_HASHES = Map.ofEntries(
@HASH_ROWS@);
    static Map<String, Set<String>> validatedDependencies(Path root, Set<String> registeredKeys) throws Exception {
        require(registeredKeys.contains(KEY) && registeredKeys.contains(LOOKUP_KEY), "Numeric or lookup primary is not registered");
        byte[] data = Files.readAllBytes(root.resolve("tests/fixtures/original-dependencies.json"));
        require(sha(data).equals(DEPENDENCIES_SHA256), "Numeric original dependency declaration changed");
        JsonObject manifest = JsonParser.parseString(new String(data, java.nio.charset.StandardCharsets.UTF_8)).getAsJsonObject();
        require(manifest.keySet().equals(Set.of("schema", "purpose", "dependencies")) && manifest.get("schema").isJsonPrimitive()
            && manifest.getAsJsonPrimitive("schema").isNumber() && manifest.get("schema").getAsString().equals("1"), "Unknown original dependency schema");
        Map<String, Set<String>> selected = new TreeMap<>(); selected.put(KEY, new TreeSet<>()); selected.put(LOOKUP_KEY, new TreeSet<>());
        Set<String> all = new TreeSet<>();
        for (JsonElement item : manifest.getAsJsonArray("dependencies")) {
            JsonObject row = item.getAsJsonObject();
            require(row.keySet().equals(Set.of("consumer", "target", "method", "original_method_sha256")), "Invalid original dependency fields");
            String key = row.get("target").getAsString() + "->" + row.get("method").getAsString();
            String consumer = row.get("consumer").getAsString();
            require(selected.containsKey(consumer) && !registeredKeys.contains(key) && all.add(key), "Registered, duplicate or misbound dependency");
            require(Objects.equals(DECLARED_GETTER_HASHES.get(key), row.get("original_method_sha256").getAsString()), "Original getter hash changed");
            selected.get(consumer).add(key);
        }
        require(selected.get(KEY).equals(GETTERS) && selected.get(LOOKUP_KEY).equals(LOOKUP_GETTERS)
            && all.equals(DECLARED_GETTER_HASHES.keySet()), "Exactly the three numeric and two lookup getters are required");
        return Map.of(KEY, Collections.unmodifiableSet(selected.get(KEY)), LOOKUP_KEY, Collections.unmodifiableSet(selected.get(LOOKUP_KEY)));
    }
    static Set<String> loadDependencies(Path root, Set<String> registeredKeys) throws Exception {
        return validatedDependencies(root, registeredKeys).get(KEY);
    }
'''.replace('@LOOKUP_KEY@', KEY).replace('@HASH_ROWS@', ',\n'.join(rows))
    java = java[:start] + validation + java[end:]; java_path.write_text(java)

    py_path = PROJECT / 'day_numeric_dex_controls.py'; py = py_path.read_text()
    py = replace_once(py, "DEPENDENCY_SHA256 = 'e30552cc8ba0520bbee3a993298cb0bcaa973a9d4633649e80362d35b3eda631'", "DEPENDENCY_SHA256 = '" + dep_sha + "'")
    start = py.index('def validate_dependencies('); end = py.index('\ndef target_entry(', start)
    py_validation = '''LOOKUP_METHOD = @LOOKUP_KEY@
LOOKUP_GETTERS = @LOOKUP_GETTERS@


def validate_dependency_declaration(root: Path, registry: list[dict]) -> dict[str, set[str]]:
    """Validate the exact global declaration before exposing either consumer partition."""
    require(sha(root / DEPENDENCY_PATH) == DEPENDENCY_SHA256, 'Original numeric dependency bytes changed')
    keys = [row['target'] + '->' + row['method'] for row in registry]
    require(len(set(keys)) == len(keys) and keys.count(METHOD) == 1 and keys.count(LOOKUP_METHOD) == 1,
            'Numeric or lookup consumer is absent or duplicated')
    data = json.loads((root / DEPENDENCY_PATH).read_text())
    require(set(data) == {'schema', 'purpose', 'dependencies'} and type(data['schema']) is int and data['schema'] == 1
            and isinstance(data['dependencies'], list), 'Invalid original dependency declaration')
    observed = {METHOD: {}, LOOKUP_METHOD: {}}
    all_keys = set()
    for row in data['dependencies']:
        require(isinstance(row, dict) and set(row) == {'consumer', 'target', 'method', 'original_method_sha256'},
                'Invalid original dependency fields')
        key = row['target'] + '->' + row['method']
        require(row['consumer'] in observed and key not in keys and key not in all_keys,
                'Original dependency credited, duplicated or misbound')
        all_keys.add(key); observed[row['consumer']][key] = row['original_method_sha256']
    require(observed == {METHOD: GETTERS, LOOKUP_METHOD: LOOKUP_GETTERS}, 'Original numeric or lookup getter selection changed')
    return {consumer: set(rows) for consumer, rows in observed.items()}


def validate_dependencies(root: Path, registry: list[dict]) -> set[str]:
    """Retain the exact three-getter numeric partition of the validated declaration."""
    return validate_dependency_declaration(root, registry)[METHOD]

'''.replace('@LOOKUP_KEY@', repr(KEY)).replace('@LOOKUP_GETTERS@', repr({row['target'] + '->' + row['method']: row['original_method_sha256'] for row in additions}))
    py = py[:start] + py_validation + py[end:]; py_path.write_text(py)

    study = (LOOKUP / 'inputs/DayLookupStudy.java').read_text()
    assert sha(study.encode()) == 'aa36382d2c5d53ad8947c56c0c8ddf758f8d903b700a449847c837581aece087'
    study = study[:study.index('    public static void main(')]
    study = replace_once(study, 'public final class DayLookupStudy', 'public final class DayLookupParityCases')
    study = replace_once(study, '/** Private typed-list lookup study. The original interpreter is not Android/ART. */',
                         '/** Exact typed-list lookup inputs and observations; bounded host evidence, not Android/ART. */')
    study = replace_once(study, 'new DictionaryEntry(input.keys()[i])', 'new DictionaryEntry(input.keys()[i], null, null)')
    study = replace_once(study, 'new Dictionary(input.mode().equals("entries-null") ? null : new TraceList(this))',
                         'new Dictionary(input.mode().equals("entries-null") ? null : new TraceList(this), false, null)')
    study = replace_once(study, '        final Dictionary dictionary;', '        final Dictionary dictionary;\n        Object returned;\n        Throwable escaped;')
    study = replace_once(study, 'if (input.faultAt() == null && "java.lang.NullPointerException".equals(input.expectedException()))', 'if (isVmNullCase(input))')
    tail = (ROOT / 'lookup_adapter_tail.java.txt').read_text().replace('@INVENTORY_SHA@', inventory_sha)
    tail = tail.replace('@VM_NULL_CASES@', ', '.join(json.dumps(name) for name in vm_nulls))
    (PROJECT / 'tests/java/DayLookupParityCases.java').write_text(study + tail)

    ui_path = PROJECT / 'tests/java/UiParityTests.java'; ui = ui_path.read_text()
    ui = replace_once(ui, 'DayTriggerParityCases.current=null;', 'DayTriggerParityCases.current=null;DayLookupParityCases.current=null;')
    ui = replace_once(ui, 'call(key,path,args); result.add("value",canonical(value));',
                     'call(key,path,args); if(key.equals(DayLookupParityCases.KEY))DayLookupParityCases.recordReturn(value,result);else result.add("value",canonical(value));')
    ui = replace_once(ui, '            if(key.equals(DayTriggerParityCases.KEY))DayTriggerParityCases.recordException(path,e,result);',
                     '            if(key.equals(DayTriggerParityCases.KEY))DayTriggerParityCases.recordException(path,e,result);\n            if(key.equals(DayLookupParityCases.KEY))DayLookupParityCases.recordException(e);')
    ui = replace_once(ui, '        if(key.equals(WidgetParityCases.KEY))WidgetParityCases.observe(args,result);',
                     '        if(key.equals(WidgetParityCases.KEY))WidgetParityCases.observe(args,result);\n        if(key.equals(DayLookupParityCases.KEY))DayLookupParityCases.observeUi(path,result);')
    ui = replace_once(ui, '        if(registry.containsKey(DayTriggerParityCases.KEY))fixtureKeys.addAll(DayTriggerParityCases.loadDependencies(root,registry.keySet()));',
                     '        if(registry.containsKey(DayTriggerParityCases.KEY))fixtureKeys.addAll(DayTriggerParityCases.loadDependencies(root,registry.keySet()));\n        if(registry.containsKey(DayLookupParityCases.KEY))fixtureKeys.addAll(DayLookupParityCases.loadDependencies(root,registry.keySet()));')
    ui = replace_once(ui, '        if(registry.containsKey(DayTriggerParityCases.KEY))DayTriggerParityCases.run();',
                     '        if(registry.containsKey(DayTriggerParityCases.KEY))DayTriggerParityCases.run();\n        if(registry.containsKey(DayLookupParityCases.KEY))DayLookupParityCases.run();')
    ui = replace_once(ui, '        if(registry.containsKey(DayTriggerParityCases.KEY)&&!DayTriggerParityCases.addReport(report,original,rebuilt))report.addProperty("passed",false);',
                     '        if(registry.containsKey(DayTriggerParityCases.KEY)&&!DayTriggerParityCases.addReport(report,original,rebuilt))report.addProperty("passed",false);\n        if(registry.containsKey(DayLookupParityCases.KEY)&&!DayLookupParityCases.addReport(report,original,rebuilt))report.addProperty("passed",false);')
    ui_path.write_text(ui)
    changed = []
    for path in sorted(PROJECT.rglob('*')):
        if not path.is_file(): continue
        relative = path.relative_to(PROJECT).as_posix(); old = BASELINE / relative
        if not old.exists() or path.read_bytes() != old.read_bytes():
            assert relative in {row['path'] for row in prep['allowed_modified_or_new_paths']}
            changed.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())})
    save(marker, {'status': 'AUTHORED_SOURCE_ADAPTER_AND_DECLARATION_SLICE_UNCOMPILED',
                  'changed_paths': changed, 'lookup_case_count': 371, 'lookup_input_inventory_sha256': inventory_sha,
                  'explicit_vm_null_cases': vm_nulls, 'dependency_sha256': dep_sha,
                  'fixture_and_provenance_still_baseline': True, 'active_source_changed': False})
    print(marker.read_text())

if __name__ == '__main__':
    main()
