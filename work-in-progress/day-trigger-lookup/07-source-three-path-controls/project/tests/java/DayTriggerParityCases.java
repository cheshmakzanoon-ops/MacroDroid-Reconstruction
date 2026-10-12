import com.android.tools.smali.dexlib2.iface.instruction.Instruction;
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
    static final String DEPENDENCIES_SHA256 = "159061ce552e3364c113f28e72e5a4c1bc091a21153d0d5e0a793d2f773b0229";
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
    static final String LOOKUP_KEY = "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;";
    static final Set<String> LOOKUP_GETTERS = Set.of(
        BASE + "$Dictionary;->getEntries()Ljava/util/List;", BASE + "$DictionaryEntry;->getKey()Ljava/lang/String;");
    static final Map<String, String> DECLARED_GETTER_HASHES = Map.ofEntries(
            Map.entry("Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;->getDecimalValue()D", "89c5a3751f7de7f7bdfaddba05f28651eb8b0b78413e4263e05c9dc795acf7ae"),
            Map.entry("Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;", "b3674d51703eb3811fc4918e739777c37de3c580bee961343b80c21e014ca5c0"),
            Map.entry("Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;->getIntValue()J", "1760568e68babc8e32459eed0352a8a20cfdbe35e02b87f2fc6dacc914399993"),
            Map.entry("Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;", "f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e"),
            Map.entry("Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;", "41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3"));
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
        require(out.size() == 1291 && inputInventorySha256(out).equals(INPUT_INVENTORY_SHA256), "Numeric case inventory changed");
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
            Set<Integer> actual = new TreeSet<>(oracle.executed.getOrDefault(key, Set.of()));
            Set<String> actualEdges = new TreeSet<>(oracle.branchEdges.getOrDefault(key, Set.of()));
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

    static void recordException(String path, Throwable error, JsonObject compared) {
        require(current != null, "Numeric exception without its current input");
        JsonObject row = inputIdentity(current); row.addProperty("path", path);
        row.addProperty("exceptionClass", error.getClass().getName()); row.addProperty("rawMessage", error.getMessage());
        row.addProperty("rawMessageWasNull", error.getMessage() == null);
        rawExceptions.add(row);
        boolean scopedNullEntry = current.kind().equals("null-entry") && error instanceof NullPointerException;
        if (!scopedNullEntry) {
            compared.addProperty("rawExceptionMessage", error.getMessage());
            compared.addProperty("rawExceptionMessageWasNull", error.getMessage() == null);
        }
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
