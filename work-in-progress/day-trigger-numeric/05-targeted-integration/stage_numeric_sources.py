#!/usr/bin/env python3
"""Derive the small numeric helper/cases/dependency catalog from reviewed inputs."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / 'overlay-01/project'
FROZEN = BASE.parent / 'day-trigger-numeric-recovery/checkpoints/02-three-path-and-compiled-controls'
PRIMARY = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'


HEADER = r'''import com.android.tools.smali.dexlib2.iface.instruction.Instruction;
import com.android.tools.smali.dexlib2.iface.instruction.OffsetInstruction;
import com.arlosoft.macrodroid.variables.VariableValue;
import com.google.gson.*;
import java.math.BigInteger;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** One recovered numeric method. The three original getters are fixture dependencies,
 * not recovered methods. Host/JVM/interpreter evidence does not establish Android,
 * calendar, alarm, time-zone, persistence or lifecycle behavior. */
public final class DayTriggerParityCases {
    static final String BASE = "Lcom/arlosoft/macrodroid/variables/VariableValue";
    static final String KEY = "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(" + BASE + "$DictionaryEntry;)I";
    static final String PRIMARY = KEY;
    static final Set<String> GETTERS = Set.of(
        BASE + "$DictionaryEntry;->getVariable()" + BASE + ";",
        BASE + "$IntegerValue;->getIntValue()J",
        BASE + "$DecimalValue;->getDecimalValue()D");
    static final Set<String> ALL;
    static { TreeSet<String> keys = new TreeSet<>(GETTERS); keys.add(KEY); ALL = Collections.unmodifiableSet(keys); }
    static final String DEPENDENCIES_SHA256 = "__DEPENDENCIES_SHA256__";
    static final String INPUT_INVENTORY_SHA256 = "e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79";
    static final Gson JSON = new GsonBuilder().serializeNulls().disableHtmlEscaping().create();
    static Input current;
    static final JsonArray rawExceptions = new JsonArray();
    record Input(String name, String kind, long bits, String text) {}
    record Observed(Integer value, String exceptionClass, String rawMessage, boolean unsupported) {}
    interface Throwing { Object get() throws Throwable; }

    static void require(boolean condition, String message) { if (!condition) throw new IllegalStateException(message); }
    static String sha(byte[] bytes) {
        try { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)); }
        catch (java.security.NoSuchAlgorithmException error) { throw new AssertionError(error); }
    }
    static JsonObject inputIdentity(Input input) {
        JsonObject row = new JsonObject(); row.addProperty("case", input.name()); row.addProperty("kind", input.kind());
        row.addProperty("rawBitsHex", String.format(Locale.ROOT, "%016x", input.bits()));
        if (input.text() != null) row.addProperty("text", input.text());
        return row;
    }
    static String inputInventorySha256(List<Input> inputs) {
        JsonArray rows = new JsonArray(); for (Input input : inputs) rows.add(inputIdentity(input));
        return sha(JSON.toJson(rows).getBytes(java.nio.charset.StandardCharsets.UTF_8));
    }
    static Set<String> loadDependencies(Path root, Set<String> registeredKeys) throws Exception {
        require(registeredKeys.contains(KEY), "Numeric primary is not registered");
        byte[] data = Files.readAllBytes(root.resolve("tests/fixtures/original-dependencies.json"));
        require(sha(data).equals(DEPENDENCIES_SHA256), "Numeric original dependency declaration changed");
        JsonObject manifest = JsonParser.parseString(new String(data, java.nio.charset.StandardCharsets.UTF_8)).getAsJsonObject();
        require(manifest.get("schema").getAsInt() == 1, "Unknown original dependency schema");
        Set<String> selected = new TreeSet<>();
        for (JsonElement item : manifest.getAsJsonArray("dependencies")) {
            JsonObject row = item.getAsJsonObject(); String key = row.get("target").getAsString() + "->" + row.get("method").getAsString();
            require(row.get("consumer").getAsString().equals(KEY), "Wrong numeric dependency consumer");
            require(!registeredKeys.contains(key) && selected.add(key), "Registered or duplicate dependency");
        }
        require(selected.equals(GETTERS), "Exactly the three original numeric getters are required");
        return Collections.unmodifiableSet(selected);
    }
    static Observed observe(Throwing body) {
        try {
            Object result = body.get();
            if (!(result instanceof Integer)) return new Observed(null, "INVALID_RETURN_TYPE", String.valueOf(result), true);
            return new Observed((Integer) result, null, null, false);
        } catch (Throwable error) {
            return new Observed(null, error.getClass().getName(), error.getMessage(), error instanceof BytecodeOracle.Unsupported);
        }
    }
    static VariableValue.DictionaryEntry entry(Input input) {
        if (input.kind().equals("null-entry")) return null;
        VariableValue value = switch (input.kind()) {
            case "integer" -> new VariableValue.IntegerValue(input.bits(), null);
            case "decimal" -> new VariableValue.DecimalValue(Double.longBitsToDouble(input.bits()), null);
            case "string" -> new VariableValue.StringValue(input.text(), null);
            case "boolean" -> new VariableValue.BooleanValue(input.bits() != 0, null);
            case "dictionary" -> new VariableValue.Dictionary(new ArrayList<>(), false, null);
            case "nested-entry" -> new VariableValue.DictionaryEntry("nested", new VariableValue.IntegerValue(input.bits(), null), null);
            case "null-value" -> null;
            default -> throw new IllegalArgumentException(input.kind());
        };
        return new VariableValue.DictionaryEntry("numeric", value, null);
    }
    // Independent expected arithmetic: modular signed-integer interpretation and
    // integer-only IEEE-754 sign/exponent/significand decomposition. No floating
    // narrowing cast, Math.round/floor or recovered getter computes expectations.
    static Integer expected(Input input) {
        if (input.kind().equals("null-entry")) return null;
        if (input.kind().equals("integer")) {
            BigInteger unsigned = BigInteger.valueOf(input.bits()).mod(BigInteger.ONE.shiftLeft(32));
            return (unsigned.testBit(31) ? unsigned.subtract(BigInteger.ONE.shiftLeft(32)) : unsigned).intValueExact();
        }
        if (input.kind().equals("decimal")) {
            long bits = input.bits(), exponent = (bits >>> 52) & 0x7ffL, fraction = bits & 0x000fffffffffffffL;
            boolean negative = bits < 0;
            if (exponent == 0x7ffL) return fraction != 0 ? 0 : negative ? Integer.MIN_VALUE : Integer.MAX_VALUE;
            BigInteger significand = BigInteger.valueOf(fraction);
            if (exponent != 0) significand = significand.setBit(52);
            int shift = Math.toIntExact((exponent == 0 ? 1 : exponent) - 1023 - 52);
            BigInteger magnitude = shift >= 0 ? significand.shiftLeft(shift) : significand.shiftRight(-shift);
            BigInteger signed = negative ? magnitude.negate() : magnitude;
            if (signed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) return Integer.MAX_VALUE;
            if (signed.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) return Integer.MIN_VALUE;
            return signed.intValueExact();
        }
        return 0;
    }
    static boolean matchesExpected(Input input, Observed output) {
        if (output.unsupported()) return false;
        if (input.kind().equals("null-entry"))
            return output.value() == null && "java.lang.NullPointerException".equals(output.exceptionClass());
        return output.exceptionClass() == null && Objects.equals(expected(input), output.value());
    }
    static boolean sameScopedOutcome(Input input, Observed a, Observed b) {
        if (input.kind().equals("null-entry")) return matchesExpected(input, a) && matchesExpected(input, b);
        return a.equals(b);
    }
'''

FOOTER = r'''
    static void recordException(String path, Throwable error, JsonObject compared) {
        require(current != null, "Numeric exception without its current input");
        JsonObject row = inputIdentity(current); row.addProperty("path", path);
        row.addProperty("exceptionClass", error.getClass().getName()); row.addProperty("rawMessage", error.getMessage());
        rawExceptions.add(row);
        boolean scopedNullEntry = current.kind().equals("null-entry") && error instanceof NullPointerException;
        if (!scopedNullEntry) compared.addProperty("rawExceptionMessage", error.getMessage());
    }
    static void run() {
        List<Input> inputs = cases();
        for (Input input : inputs) {
            java.util.function.Supplier<Object[]> make = () -> { current = input; return new Object[]{entry(input)}; };
            if (input.kind().equals("null-entry")) {
                JsonObject expected = new JsonObject(); expected.addProperty("exception", "java.lang.NullPointerException");
                UiParityTests.check(KEY, "day-numeric:" + input.name(), make, UiParityTests.UNKNOWN, false, expected);
            } else UiParityTests.check(KEY, "day-numeric:" + input.name(), make, expected(input));
        }
    }
    static boolean addReport(JsonObject report, BytecodeOracle original, BytecodeOracle rebuilt) {
        JsonObject old = coverage(original, ALL), fresh = rebuilt == null ? null : coverage(rebuilt, ALL);
        report.addProperty("dayNumericRecoveredMethods", 1);
        report.addProperty("dayNumericOriginalDependencyMethods", GETTERS.size());
        report.add("dayNumericOriginalDependencyKeys", JSON.toJsonTree(new TreeSet<>(GETTERS)));
        report.addProperty("dayNumericInputInventorySha256", inputInventorySha256(cases()));
        report.add("dayNumericOriginalCoverage", old);
        if (fresh != null) report.add("dayNumericRebuiltCoverage", fresh);
        report.add("dayNumericRawExceptions", rawExceptions);
        report.addProperty("dayNumericExceptionComparisonScope", "Only the explicit null-entry NPE compares its class. Raw messages are retained. Other exceptions include their complete raw message in comparison.");
        boolean passed = old.get("allInstructionsAndEdgesExecuted").getAsBoolean()
            && old.get("instructionCount").getAsInt() == 32 && old.get("requiredBranchEdges").getAsInt() == 4
            && (fresh == null || (fresh.get("allInstructionsAndEdgesExecuted").getAsBoolean()
                && fresh.get("instructionCount").getAsInt() == 25 && fresh.get("requiredBranchEdges").getAsInt() == 4));
        report.addProperty("dayNumericInstructionAndConditionalCoverage", passed);
        return passed;
    }
}
'''


def main():
    source = (FROZEN / 'inputs/DayValueStudy.java').read_text()
    assert hashlib.sha256(source.encode()).hexdigest() == '4542b75d3ca2e5e8299fcdf218f90807e46af312531f2cdafd976b4c265a7442'
    helper = FROZEN / 'inputs/source/java/recovered/ui/DayTriggerValueMethods.java'
    assert hashlib.sha256(helper.read_bytes()).hexdigest() == 'b99984c0ca9128f9def8658d874f98d9a8e4529433d0f76f7f86e9e8299cc792'
    target_helper = OUT / 'source/java/recovered/ui/DayTriggerValueMethods.java'
    assert not target_helper.exists(); target_helper.write_bytes(helper.read_bytes())
    pins = json.loads((FROZEN / 'inputs/preserved-input-pins.json').read_text())['selectedOriginalMethods']
    primary = pins[0]
    entry = {'target': primary['descriptor'], 'method': primary['method'],
             'helper': 'Lrecovered/ui/DayTriggerValueMethods;', 'helper_method': 'numericValue',
             'instance': False, 'java_source': 'source/java/recovered/ui/DayTriggerValueMethods.java',
             'proof_family': 'v9-ui', 'original_method_sha256': primary['methodTextSha256']}
    for name in ('source/java-method-map.json', 'source/ui-methods.json'):
        path = OUT / name; rows = json.loads(path.read_text())
        assert PRIMARY not in {r['target'] + '->' + r['method'] for r in rows}
        rows.append(entry); path.write_text(json.dumps(rows, indent=2) + '\n')
    dependencies = {'schema': 1, 'purpose': 'Test-only original getter instructions; no recovered-method credit and not an application build input.',
                    'dependencies': [{'consumer': PRIMARY, 'target': row['descriptor'], 'method': row['method'],
                                      'original_method_sha256': row['methodTextSha256']} for row in pins[1:]]}
    data = (json.dumps(dependencies, indent=2) + '\n').encode()
    dependency_path = OUT / 'tests/fixtures/original-dependencies.json'
    assert not dependency_path.exists(); dependency_path.write_bytes(data)
    cases = source[source.index('    static List<Input> cases() {'):source.index('    static JsonObject coverage(')]
    cases = cases.replace('        return out;\n', '        require(out.size() == 1291 && inputInventorySha256(out).equals(INPUT_INVENTORY_SHA256), "Numeric case inventory changed");\n        return out;\n')
    coverage = source[source.index('    static JsonObject coverage('):source.index('    public static void main(')]
    coverage = coverage.replace('oracle.executed.getOrDefault(key, Set.of())', 'new TreeSet<>(oracle.executed.getOrDefault(key, Set.of()))')
    coverage = coverage.replace('oracle.branchEdges.getOrDefault(key, Set.of())', 'new TreeSet<>(oracle.branchEdges.getOrDefault(key, Set.of()))')
    java = HEADER.replace('__DEPENDENCIES_SHA256__', hashlib.sha256(data).hexdigest()) + cases + coverage + FOOTER
    path = OUT / 'tests/java/DayTriggerParityCases.java'; assert not path.exists(); path.write_text(java)
    faults = json.loads((BASE.parent / 'day-trigger-numeric-recovery/reports/three-path-controls-02/fault-catalog.json').read_text())
    # The active host StringValue field is `value`; retain that public contract.
    controls = [{'name': r['name'], 'reason': 'Measured numeric fault: ' + r['name'],
                 'edits': [{'find': r['old'], 'replace': r['new'].replace(' value).text', ' value).value'), 'count': 1}],
                 'expected_failure_labels': ['day-numeric:' + r['requiredFailingCase']]} for r in faults]
    catalog = {'schema': 1, 'method': PRIMARY, 'helper_path': entry['java_source'],
               'helper_sha256': hashlib.sha256(helper.read_bytes()).hexdigest(),
               'input_inventory_sha256': 'e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79',
               'reviewed_study_checkpoint_sha256': 'd93f08507afce1b6eebe1e3ae64338f86eb04ca01e26118bdd97f98f5d6af631',
               'host_field_adaptation': 'parse-string reads the existing public StringValue.value field; its fault and required case are unchanged.',
               'controls': controls}
    path = OUT / 'tests/fixtures/day-numeric-mutants.json'; assert not path.exists(); path.write_text(json.dumps(catalog, indent=2) + '\n')
    print(json.dumps({'registered_methods': len(json.loads((OUT / 'source/java-method-map.json').read_text())),
                      'ui_methods': len(json.loads((OUT / 'source/ui-methods.json').read_text())),
                      'dependencies': len(dependencies['dependencies']), 'catalog_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'dependency_sha256': hashlib.sha256(data).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
