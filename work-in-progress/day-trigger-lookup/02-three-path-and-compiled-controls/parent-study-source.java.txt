import com.android.tools.smali.dexlib2.iface.instruction.Instruction;
import com.android.tools.smali.dexlib2.iface.instruction.OffsetInstruction;
import com.arlosoft.macrodroid.variables.VariableValue;
import com.google.gson.*;
import recovered.ui.DayTriggerValueMethods;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Bounded, private numeric study. The instruction interpreter is not Android/ART. */
public final class DayValueStudy {
    static final String BASE = "Lcom/arlosoft/macrodroid/variables/VariableValue";
    static final String PRIMARY = "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(" + BASE + "$DictionaryEntry;)I";
    static final Set<String> GETTERS = Set.of(
        BASE + "$DictionaryEntry;->getVariable()" + BASE + ";",
        BASE + "$IntegerValue;->getIntValue()J",
        BASE + "$DecimalValue;->getDecimalValue()D");
    static final Set<String> ALL;
    static { TreeSet<String> keys = new TreeSet<>(GETTERS); keys.add(PRIMARY); ALL = Collections.unmodifiableSet(keys); }
    record Input(String name, String kind, long bits, String text) {}
    record Observed(Integer value, String exceptionClass, String rawMessage, boolean unsupported) {}
    interface Throwing { Object get() throws Throwable; }

    static String sha(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }
    static String fileSha(Path path) throws Exception { return sha(Files.readAllBytes(path)); }
    static void require(boolean condition, String message) { if (!condition) throw new IllegalStateException(message); }
    static void bindClass(Class<?> type, Path expected, String hash, JsonObject bindings) throws Exception {
        var url = type.getResource("/" + type.getName().replace('.', '/') + ".class");
        require(url != null && url.getProtocol().equals("file"), "Class is not loaded from a file: " + type.getName());
        Path actual = Paths.get(url.toURI()).toRealPath();
        require(actual.equals(expected.toRealPath()), "Wrong loaded class origin: " + type.getName());
        require(fileSha(actual).equals(hash), "Wrong loaded class hash: " + type.getName());
        JsonObject item = new JsonObject(); item.addProperty("path", actual.toString()); item.addProperty("sha256", hash);
        bindings.add(type.getName(), item);
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
            case "integer" -> new VariableValue.IntegerValue(input.bits());
            case "decimal" -> new VariableValue.DecimalValue(Double.longBitsToDouble(input.bits()));
            case "string" -> new VariableValue.StringValue(input.text());
            case "boolean" -> new VariableValue.BooleanValue(input.bits() != 0);
            case "dictionary" -> new VariableValue.Dictionary();
            case "nested-entry" -> new VariableValue.DictionaryEntry(new VariableValue.IntegerValue(input.bits()));
            case "null-value" -> null;
            default -> throw new IllegalArgumentException(input.kind());
        };
        return new VariableValue.DictionaryEntry(value);
    }
    // Independent arithmetic oracle: modulo/sign interpretation for longs, exact
    // binary-double BigDecimal truncation with explicit saturation and NaN rules.
    // Neither expected-value path uses a narrowing Java numeric cast.
    static Integer expected(Input input) {
        if (input.kind().equals("null-entry")) return null;
        if (input.kind().equals("integer")) {
            BigInteger unsigned = BigInteger.valueOf(input.bits()).mod(BigInteger.ONE.shiftLeft(32));
            BigInteger signed = unsigned.testBit(31) ? unsigned.subtract(BigInteger.ONE.shiftLeft(32)) : unsigned;
            return signed.intValueExact();
        }
        if (input.kind().equals("decimal")) {
            double value = Double.longBitsToDouble(input.bits());
            if (Double.isNaN(value)) return 0;
            if (value >= 2147483647.0d) return Integer.MAX_VALUE;
            if (value <= -2147483648.0d) return Integer.MIN_VALUE;
            return new BigDecimal(value).toBigInteger().intValueExact();
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
    static List<Input> cases() {
        List<Input> out = new ArrayList<>();
        long[] integers = {0, 1, -1, 2, -2, 127, 128, 255, 256, 32767, 32768, 65535, 65536,
            2147483646L, 2147483647L, 2147483648L, 2147483649L, -2147483647L, -2147483648L,
            -2147483649L, -2147483650L, 4294967295L, 4294967296L, 4294967297L, -4294967295L,
            -4294967296L, -4294967297L, 9007199254740991L, 9007199254740992L, 9007199254740993L,
            -9007199254740991L, -9007199254740992L, -9007199254740993L, Long.MAX_VALUE, Long.MIN_VALUE};
        for (int i = 0; i < integers.length; i++) out.add(new Input("integer-boundary-" + i, "integer", integers[i], null));
        for (int bit = 0; bit < 64; bit++) {
            long value = 1L << bit;
            out.add(new Input("integer-bit-" + bit, "integer", value, null));
            out.add(new Input("integer-complement-" + bit, "integer", ~value, null));
        }
        Random random = new Random(0x567800896700008L);
        for (int i = 0; i < 384; i++) out.add(new Input("integer-seeded-" + i, "integer", random.nextLong(), null));
        double[] decimals = {0.0d, -0.0d, 0.1d, -0.1d, 0.999d, -0.999d, 1.0d, -1.0d, 1.1d, -1.1d,
            1.5d, -1.5d, 1.9d, -1.9d, 2.9d, -2.9d, 2147483646.75d, 2147483647.0d, 2147483647.75d,
            2147483648.0d, -2147483647.75d, -2147483648.0d, -2147483648.75d, 4294967296.0d,
            -4294967296.0d, 9007199254740991.0d, -9007199254740991.0d, Double.MIN_VALUE,
            -Double.MIN_VALUE, Double.MIN_NORMAL, -Double.MIN_NORMAL, Double.MAX_VALUE, -Double.MAX_VALUE,
            Double.POSITIVE_INFINITY, Double.NEGATIVE_INFINITY, Double.NaN};
        for (int i = 0; i < decimals.length; i++) out.add(new Input("decimal-boundary-" + i, "decimal", Double.doubleToRawLongBits(decimals[i]), null));
        for (double pivot : new double[]{-2147483649d, -2147483648d, -2147483647d, -2d, -1d, 0d, 1d, 2d, 2147483646d, 2147483647d, 2147483648d}) {
            double value = pivot;
            for (int i = 0; i < 8; i++) {
                value = Math.nextDown(value);
                out.add(new Input("decimal-next-down-" + Double.toHexString(pivot) + "-" + i, "decimal", Double.doubleToRawLongBits(value), null));
            }
            value = pivot;
            for (int i = 0; i < 8; i++) {
                value = Math.nextUp(value);
                out.add(new Input("decimal-next-up-" + Double.toHexString(pivot) + "-" + i, "decimal", Double.doubleToRawLongBits(value), null));
            }
        }
        long[] special = {1L, 0x8000000000000001L, 0x000fffffffffffffL, 0x800fffffffffffffL,
            0x7ff0000000000001L, 0x7ff8000000000001L, 0x7fffffffffffffffL,
            0xfff0000000000001L, 0xfff8000000000001L, 0xffffffffffffffffL};
        for (int i = 0; i < special.length; i++) out.add(new Input("decimal-special-bits-" + i, "decimal", special[i], null));
        for (int i = 0; i < 512; i++) out.add(new Input("decimal-seeded-bits-" + i, "decimal", random.nextLong(), null));
        out.add(new Input("null-entry", "null-entry", 0, null));
        out.add(new Input("null-value", "null-value", 0, null));
        out.add(new Input("string-numeric", "string", 0, "27"));
        out.add(new Input("string-decimal", "string", 0, "1.9"));
        out.add(new Input("string-empty", "string", 0, ""));
        out.add(new Input("string-null", "string", 0, null));
        out.add(new Input("boolean-false", "boolean", 0, null));
        out.add(new Input("boolean-true", "boolean", 1, null));
        out.add(new Input("dictionary", "dictionary", 0, null));
        out.add(new Input("nested-entry", "nested-entry", 91, null));
        require(out.stream().map(Input::name).distinct().count() == out.size(), "Duplicate case identifiers");
        return out;
    }
    static JsonObject coverage(BytecodeOracle oracle, Set<String> keys) {
        JsonObject output = new JsonObject(); JsonArray methods = new JsonArray();
        int total = 0, covered = 0, edgeTotal = 0, edgeCovered = 0;
        for (String key : new TreeSet<>(keys)) {
            var method = oracle.methods.get(key); require(method != null, "Coverage method missing: " + key);
            Set<Integer> required = new TreeSet<>(); Set<String> requiredEdges = new TreeSet<>(); int pc = 0;
            for (Instruction instruction : method.getImplementation().getInstructions()) {
                required.add(pc);
                if (instruction.getOpcode().name().startsWith("IF_")) {
                    requiredEdges.add(pc + ":" + (pc + instruction.getCodeUnits()));
                    requiredEdges.add(pc + ":" + (pc + ((OffsetInstruction) instruction).getCodeOffset()));
                }
                pc += instruction.getCodeUnits();
            }
            Set<Integer> actual = oracle.executed.getOrDefault(key, Set.of());
            Set<String> actualEdges = oracle.branchEdges.getOrDefault(key, Set.of());
            require(required.containsAll(actual) && requiredEdges.containsAll(actualEdges), "Unexpected coverage coordinates");
            Set<Integer> missing = new TreeSet<>(required); missing.removeAll(actual);
            Set<String> missingEdges = new TreeSet<>(requiredEdges); missingEdges.removeAll(actualEdges);
            JsonObject row = new JsonObject(); row.addProperty("key", key); row.addProperty("primaryRecovery", key.equals(PRIMARY));
            row.add("requiredOffsets", new Gson().toJsonTree(required)); row.add("executedOffsets", new Gson().toJsonTree(actual));
            row.add("missingOffsets", new Gson().toJsonTree(missing)); row.add("requiredEdges", new Gson().toJsonTree(requiredEdges));
            row.add("executedEdges", new Gson().toJsonTree(actualEdges)); row.add("missingEdges", new Gson().toJsonTree(missingEdges));
            row.addProperty("instructionCount", required.size()); row.addProperty("exceptionRegions", method.getImplementation().getTryBlocks().size());
            methods.add(row); total += required.size(); covered += actual.size(); edgeTotal += requiredEdges.size(); edgeCovered += actualEdges.size();
        }
        output.add("methods", methods); output.addProperty("instructionCount", total); output.addProperty("executedInstructionCount", covered);
        output.addProperty("requiredBranchEdges", edgeTotal); output.addProperty("executedBranchEdges", edgeCovered);
        output.addProperty("allInstructionsAndEdgesExecuted", total == covered && edgeTotal == edgeCovered);
        return output;
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Expected config.json report.json");
        JsonObject config = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        Path original = Path.of(config.get("originalDex").getAsString());
        require(fileSha(original).equals(config.get("originalDexSha256").getAsString()), "Wrong original fixture identity");
        JsonObject origins = new JsonObject();
        for (Class<?> type : List.of(DayValueStudy.class, BytecodeOracle.class, DayTriggerValueMethods.class,
                VariableValue.class, VariableValue.DictionaryEntry.class, VariableValue.IntegerValue.class,
                VariableValue.DecimalValue.class, VariableValue.StringValue.class, VariableValue.BooleanValue.class,
                VariableValue.Dictionary.class, defpackage.EngineRuntime.class, defpackage.TestClock.class)) {
            JsonObject pin = config.getAsJsonObject("classPins").getAsJsonObject(type.getName());
            require(pin != null, "Class pin missing: " + type.getName());
            bindClass(type, Path.of(pin.get("path").getAsString()), pin.get("sha256").getAsString(), origins);
        }
        require(!defpackage.EngineRuntime.active && !defpackage.TestClock.enabled, "Unexpected enabled host hook");
        BytecodeOracle reference = new BytecodeOracle(original, ALL);
        require(reference.methods.keySet().equals(ALL), "Original fixture membership mismatch");
        BytecodeOracle rebuilt = null;
        if (config.has("rebuiltDex")) {
            Path dex = Path.of(config.get("rebuiltDex").getAsString());
            require(fileSha(dex).equals(config.get("rebuiltDexSha256").getAsString()), "Wrong rebuilt fixture identity");
            require(!fileSha(dex).equals(fileSha(original)), "Original fixture cannot masquerade as rebuilt");
            rebuilt = new BytecodeOracle(original, GETTERS); rebuilt.add(dex, Set.of(PRIMARY));
            require(rebuilt.methods.keySet().equals(ALL), "Rebuilt fixture membership mismatch");
        }
        List<Input> cases = cases(); JsonArray rows = new JsonArray(); JsonArray mismatches = new JsonArray();
        int unsupported = 0, expectedFailures = 0;
        for (Input input : cases) {
            BytecodeOracle actualRebuilt = rebuilt;
            Observed old = observe(() -> reference.invoke(PRIMARY, entry(input)));
            Observed java = observe(() -> DayTriggerValueMethods.numericValue(entry(input)));
            Observed dex = rebuilt == null ? null : observe(() -> actualRebuilt.invoke(PRIMARY, entry(input)));
            JsonObject row = new JsonObject(); row.addProperty("case", input.name()); row.addProperty("kind", input.kind());
            row.addProperty("rawBitsHex", String.format(Locale.ROOT, "%016x", input.bits()));
            if (input.text() != null) row.addProperty("text", input.text());
            if (input.kind().equals("null-entry")) row.addProperty("expectedExceptionClass", "java.lang.NullPointerException");
            else row.addProperty("expected", expected(input));
            Gson gson = new GsonBuilder().serializeNulls().create();
            row.add("original", gson.toJsonTree(old)); row.add("java", gson.toJsonTree(java));
            if (dex != null) row.add("rebuilt", gson.toJsonTree(dex));
            boolean same = sameScopedOutcome(input, old, java) && (dex == null || sameScopedOutcome(input, old, dex));
            boolean correct = matchesExpected(input, old) && matchesExpected(input, java) && (dex == null || matchesExpected(input, dex));
            row.addProperty("sameScopedOutcome", same); row.addProperty("allPathsMatchIndependentExpected", correct);
            if (!same || !correct) mismatches.add(input.name());
            for (Observed output : dex == null ? List.of(old, java) : List.of(old, java, dex)) if (output.unsupported()) unsupported++;
            if (!correct) expectedFailures++;
            rows.add(row);
        }
        JsonObject report = new JsonObject();
        report.addProperty("scope", "One DayTrigger numeric method; three original field getters are dependencies. Interpreter/JVM study, not ART or calendar/lifecycle coverage.");
        report.addProperty("exceptionComparisonScope", "Only the explicit null-entry input compares the required NPE class; all raw messages are retained. Every other outcome compares the complete observed record.");
        report.addProperty("primaryMethod", PRIMARY); report.addProperty("primaryRecoveredMethods", 1); report.addProperty("originalDependencyMethods", 3);
        report.addProperty("cases", cases.size()); report.addProperty("executionPaths", rebuilt == null ? 2 : 3);
        report.addProperty("mismatchCount", mismatches.size()); report.addProperty("unsupportedCount", unsupported);
        report.addProperty("independentExpectedChecks", cases.size()); report.addProperty("independentExpectedFailures", expectedFailures);
        report.addProperty("originalDexSha256", fileSha(original)); report.add("loadedClassOrigins", origins);
        report.add("originalCoverage", coverage(reference, ALL));
        if (rebuilt != null) { report.add("rebuiltCoverage", coverage(rebuilt, ALL)); report.addProperty("rebuiltDexSha256", config.get("rebuiltDexSha256").getAsString()); }
        report.add("mismatches", mismatches); report.add("observations", rows);
        report.addProperty("passed", mismatches.size() == 0 && unsupported == 0 && expectedFailures == 0
            && report.getAsJsonObject("originalCoverage").get("allInstructionsAndEdgesExecuted").getAsBoolean()
            && (rebuilt == null || report.getAsJsonObject("rebuiltCoverage").get("allInstructionsAndEdgesExecuted").getAsBoolean()));
        Files.writeString(Path.of(args[1]), new GsonBuilder().setPrettyPrinting().serializeNulls().create().toJson(report) + "\n");
        System.out.println("DAY_VALUE_STUDY cases=" + cases.size() + " paths=" + (rebuilt == null ? 2 : 3)
            + " mismatches=" + mismatches.size() + " unsupported=" + unsupported + " expectedFailures=" + expectedFailures
            + " passed=" + report.get("passed"));
        if (!report.get("passed").getAsBoolean()) System.exit(3);
    }
}
