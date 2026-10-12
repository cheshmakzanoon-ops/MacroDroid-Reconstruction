from __future__ import annotations

import datetime
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat

ROOT = Path(__file__).resolve().parent
MERGE = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/04-numeric-filesystem-merge')
SUCCESSOR = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/05-lookup-recorder-successor')
RAW = Path('/dev/shm/macrodroid-combined-run-97322-independent-review/collection-01/retained')
DIAGNOSIS = Path('/dev/shm/macrodroid-combined-run-97322-independent-review/diagnosis-01/five-values.json')
JAR = Path('/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')
OLD_LINE = '        Files.writeString(reportPath,G.toJson(report));\n'
NEW_LINE = '        Files.writeString(reportPath,G.newBuilder().serializeNulls().create().toJson(report));\n'


def identity(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode)
    return {'bytes': after.st_size, 'sha256': digest, 'mode': stat.S_IMODE(after.st_mode)}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + '\n')


def copy(source, destination):
    before = identity(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as target, source.open('rb') as origin:
        shutil.copyfileobj(origin, target)
    destination.chmod(before['mode'])
    assert identity(destination) == before
    return before


def checkpoint_inputs(root, expected):
    result = {'checkpoint.json': identity(root / 'checkpoint.json')}
    assert result['checkpoint.json']['sha256'] == expected
    data = json.loads((root / 'checkpoint.json').read_bytes())
    for row in data['files']:
        value = identity(root / row['path'])
        assert value == {k: row[k] for k in ('bytes', 'sha256', 'mode')}, row['path']
        result[row['path']] = value
    return result


def main():
    stage = ROOT / 'stage-01'
    stage.mkdir(exist_ok=False)
    parent_inputs = {
        'merge': checkpoint_inputs(MERGE, '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350'),
        'successor': checkpoint_inputs(SUCCESSOR, '87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5'),
    }
    for name, folder in [('merge', MERGE), ('successor', SUCCESSOR)]:
        copy(folder / 'checkpoint.json', stage / 'inputs' / (name + '-checkpoint.json'))
    diagnosis = json.loads(DIAGNOSIS.read_bytes())
    assert all(diagnosis[k]['equal'] is True for k in diagnosis if k != 'observer_controls')
    assert diagnosis['observer_controls']['equal'] is False
    actual = diagnosis['observer_controls']['actual']
    expected = diagnosis['observer_controls']['expected']
    paths = [('positive', None), *[('rejectedRecords', n) for n in (0, 1, 2, 4)]]
    changed = json.loads(json.dumps(actual))
    for name, index in paths:
        a = changed[name] if index is None else changed[name][index]
        e = expected[name] if index is None else expected[name][index]
        assert 'returnIndex' not in a and e['returnIndex'] is None
        a['returnIndex'] = None
    assert changed == expected
    assert expected['rejectedRecords'][3]['returnIndex'] == 0
    copy(DIAGNOSIS, stage / 'inputs/five-values.json')
    write(stage / 'inputs/expected-observer-controls.json', expected)
    write(stage / 'inputs/actual-ui-observer-controls.json', actual)
    fixture = {'nullField': None, 'nested': {'nullField': None, 'emptyString': '', 'zero': 0, 'false': False},
               'array': [None, {'nullField': None}, [], {}], 'text': '<>&=\'"\n\t\u0000 café'}
    write(stage / 'inputs/serialization-boundary-fixture.json', fixture)
    source_dir = RAW / 'hosted-proof/inputs/lookup-overlay/project/tests/java'
    for name in ('UiParityTests.java', 'DayLookupParityCases.java', 'DayLookupControlHarness.java'):
        old = source_dir / name
        assert old.read_bytes() == (MERGE / 'project/tests/java' / name).read_bytes()
        copy(old, stage / 'inputs/source' / name)
    source = (source_dir / 'UiParityTests.java').read_text()
    assert hashlib.sha256(source.encode()).hexdigest() == 'f7e77395b4983bf786225829e6e1edfa3b997c9e947881163328196151f15b0c'
    assert source.count(OLD_LINE) == 1 and source.count(NEW_LINE) == 0
    candidate = source.replace(OLD_LINE, NEW_LINE)
    destination = stage / 'project/tests/java/UiParityTests.java'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x') as stream:
        stream.write(candidate)
    destination.chmod(0o644)
    assert candidate.replace(NEW_LINE, OLD_LINE) == source
    (stage / 'one-line-source.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True), candidate.splitlines(True),
        fromfile='parent/tests/java/UiParityTests.java', tofile='candidate/tests/java/UiParityTests.java')))
    initializer = next(line for line in source.splitlines() if 'static final Gson G =' in line)
    assert initializer == '    static final Gson G = new GsonBuilder().setPrettyPrinting().create();'
    runtime_root = RAW / 'hosted-proof/runtime-classes'
    runtime = {}
    for path in sorted(runtime_root.rglob('*.class')):
        relative = path.relative_to(runtime_root).as_posix()
        runtime[relative] = copy(path, stage / 'inputs/runtime-classes' / relative)
    assert len(runtime) == 40
    assert runtime['tools/classes/DayLookupParityCases.class']['sha256'] == 'e7df3ff6fdd46e41418ecf3589984b7242e366bf312c1ec70c97552a210e87ff'
    jar = identity(JAR)
    assert jar['bytes'] == 80076986 and jar['sha256'] == '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'
    java = '''import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Host serializer boundary only. Neither writer executes application methods. */
public final class UiReportSerializationControl {
__INITIALIZER__
    static final Gson EVIDENCE = new GsonBuilder().serializeNulls().setPrettyPrinting().create();
    static void writeOriginal(Path reportPath, JsonObject report) throws Exception {
__OLD__    }
    static void writeCorrected(Path reportPath, JsonObject report) throws Exception {
__NEW__    }
    static void require(boolean value, String message) {
        if (!value) throw new IllegalStateException(message);
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 3, "Expected mode, exact input root and fresh output root");
        String mode = args[0];
        require(mode.equals("original") || mode.equals("corrected"), "Unknown writer mode");
        Path inputs = Path.of(args[1]), output = Path.of(args[2]);
        Files.createDirectory(output);
        JsonObject expected = JsonParser.parseString(Files.readString(inputs.resolve("expected-observer-controls.json"))).getAsJsonObject();
        JsonObject oldActual = JsonParser.parseString(Files.readString(inputs.resolve("actual-ui-observer-controls.json"))).getAsJsonObject();
        var cases = DayLookupParityCases.pinnedCases();
        require(cases.size() == 371, "Pinned input count differs");
        require(DayLookupParityCases.inputInventorySha256(cases).equals("02dd119966191ad2f56937eda28e63644979080158465ffb13767710f34e32e6"), "Pinned input inventory differs");
        JsonObject generated = DayLookupParityCases.observerControls(cases);
        require(generated.equals(expected), "Actual compiled observer differs from closed standalone record");
        JsonObject report = new JsonObject();
        report.add("dayLookupObserverRecordControls", generated);
        report.add("serializationBoundaryFixture", JsonParser.parseString(Files.readString(inputs.resolve("serialization-boundary-fixture.json"))));
        Path reportPath = output.resolve("serialized-report.json");
        if (mode.equals("original")) writeOriginal(reportPath, report); else writeCorrected(reportPath, report);
        JsonObject observed = JsonParser.parseString(Files.readString(reportPath)).getAsJsonObject();
        JsonObject actual = observed.getAsJsonObject("dayLookupObserverRecordControls");
        JsonArray absentNulls = new JsonArray();
        if (!actual.getAsJsonObject("positive").has("returnIndex")) absentNulls.add("positive.returnIndex");
        for (int i : new int[]{0, 1, 2, 4})
            if (!actual.getAsJsonArray("rejectedRecords").get(i).getAsJsonObject().has("returnIndex"))
                absentNulls.add("rejectedRecords[" + i + "].returnIndex");
        JsonObject result = new JsonObject();
        result.addProperty("mode", mode);
        result.addProperty("passed", observed.equals(report));
        result.addProperty("observerStrictEquality", actual.equals(expected));
        result.addProperty("matchesOriginalClosedUiRecord", actual.equals(oldActual));
        result.addProperty("actualCompiledObserverMatchesClosedStandalone", true);
        result.addProperty("pinnedInputInventory", "02dd119966191ad2f56937eda28e63644979080158465ffb13767710f34e32e6");
        result.addProperty("pinnedInputCount", cases.size());
        result.addProperty("applicationExecutions", 0);
        result.addProperty("applicationCoverageCredit", 0);
        result.addProperty("androidRuntime", false);
        result.addProperty("completeUiHarnessExecuted", false);
        result.addProperty("strictFinalizerModified", false);
        result.add("absentNullReturnIndices", absentNulls);
        result.addProperty("nonNullReturnIndexPreserved", actual.getAsJsonArray("rejectedRecords").get(3).getAsJsonObject().get("returnIndex").getAsInt() == 0);
        result.addProperty("observerClassOrigin", DayLookupParityCases.class.getProtectionDomain().getCodeSource().getLocation().toString());
        result.addProperty("gsonClassOrigin", Gson.class.getProtectionDomain().getCodeSource().getLocation().toString());
        Files.writeString(output.resolve("expected-tree.json"), EVIDENCE.toJson(report) + "\\n");
        Files.writeString(output.resolve("result.json"), EVIDENCE.toJson(result) + "\\n");
        System.out.println("UI_REPORT_SERIALIZER mode=" + mode + " strict=" + result.get("observerStrictEquality") + " roundtrip=" + result.get("passed") + " absentNulls=" + absentNulls.size());
        if (!result.get("passed").getAsBoolean()) System.exit(2);
    }
}
'''
    java = java.replace('__INITIALIZER__', initializer).replace('__OLD__', OLD_LINE).replace('__NEW__', NEW_LINE)
    harness = stage / 'control-source/UiReportSerializationControl.java'
    harness.parent.mkdir(parents=True)
    harness.write_text(java)
    value = {'schema': 1, 'status': 'ONE_REPORT_WRITER_LINE_AUTHORED_PENDING_ACTUAL_BOUNDARY_CONTROL',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'actual_failed_run': 38248170022, 'actual_failed_head': '97322c18273818b0241fa1fa962da9d4a445afd1',
        'actual_artifact': {'bytes': 241915713, 'sha256': '3ad31b610aa01ea4b0490fe9c2238e9a919f5e38be3df923ec453e3afc117d16'},
        'parent_inputs': parent_inputs, 'parent_source': identity(source_dir / 'UiParityTests.java'),
        'candidate_source': identity(destination), 'serializer_initializer_unchanged': True,
        'only_source_change': {'old': OLD_LINE.rstrip('\n'), 'new': NEW_LINE.rstrip('\n')},
        'mechanically_extracted_boundary_harness': identity(harness),
        'runtime_classes': runtime, 'jar': {'path': str(JAR), **jar},
        'diagnosis': identity(DIAGNOSIS), 'active_source_changed': False,
        'complete_ui_harness_executed': False, 'application_execution': False, 'android_execution': False,
        'strict_finalizer_unchanged': True}
    write(stage / 'derivation.json', value)
    print(json.dumps({k: value[k] for k in ('status', 'parent_source', 'candidate_source', 'mechanically_extracted_boundary_harness')}))


if __name__ == '__main__':
    main()
