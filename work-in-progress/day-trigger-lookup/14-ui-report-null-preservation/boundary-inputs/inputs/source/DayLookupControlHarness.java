import com.arlosoft.macrodroid.variables.VariableValue;
import com.google.gson.*;
import recovered.ui.DayTriggerLookupMethods;
import java.io.InputStream;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.zip.ZipFile;

/** A bounded three-path execution of the real lookup body and two APK getters.
 * The acceptance driver separately requires the standalone positive method's
 * instruction listing to equal the signed APK body. This harness alone makes
 * no packaging, ART, calendar or exhaustive Unicode claim. */
public final class DayLookupControlHarness {
    static final Gson JSON = new GsonBuilder().serializeNulls().disableHtmlEscaping().setPrettyPrinting().create();
    static void require(boolean value, String message) { if (!value) throw new IllegalStateException(message); }
    static String sha(InputStream stream) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256"); byte[] buffer = new byte[65536]; int count;
        while ((count = stream.read(buffer)) != -1) digest.update(buffer, 0, count);
        return HexFormat.of().formatHex(digest.digest());
    }
    static String sha(Path path) throws Exception { try (InputStream stream = Files.newInputStream(path)) { return sha(stream); } }
    static Path boundPath(JsonObject row, String role) throws Exception {
        require(row != null && row.keySet().containsAll(Set.of("path", "sha256")), "Missing identity: " + role);
        require(row.get("path").isJsonPrimitive() && row.getAsJsonPrimitive("path").isString()
                && row.get("sha256").isJsonPrimitive() && row.getAsJsonPrimitive("sha256").isString()
                && row.get("sha256").getAsString().matches("[0-9a-f]{64}"), "Malformed identity: " + role);
        Path path = Path.of(row.get("path").getAsString()).toRealPath();
        require(sha(path).equals(row.get("sha256").getAsString()), "Wrong input identity: " + role);
        return path;
    }
    static Set<Class<?>> requiredClasses() {
        Set<Class<?>> selected = new LinkedHashSet<>(List.of(DayLookupControlHarness.class, DayLookupParityCases.class,
            BytecodeOracle.class, DayTriggerLookupMethods.class, VariableValue.class,
            defpackage.EngineRuntime.class, defpackage.TestClock.class));
        boolean more = true;
        while (more) {
            more = false;
            for (Class<?> type : new ArrayList<>(selected)) for (Class<?> nested : type.getDeclaredClasses()) more |= selected.add(nested);
        }
        return selected;
    }
    static JsonObject bindClasses(JsonObject pins) throws Exception {
        require(pins != null, "Missing class-origin pins");
        JsonObject found = new JsonObject(); Set<String> names = new TreeSet<>();
        for (Class<?> type : requiredClasses()) {
            names.add(type.getName()); JsonObject pin = pins.getAsJsonObject(type.getName());
            Path expected = boundPath(pin, "class " + type.getName());
            var resource = type.getResource("/" + type.getName().replace('.', '/') + ".class");
            require(resource != null && resource.getProtocol().equals("file"), "Class origin is not a file: " + type.getName());
            Path actual = Path.of(resource.toURI()).toRealPath();
            require(actual.equals(expected), "Wrong loaded class origin: " + type.getName());
            JsonObject row = new JsonObject(); row.addProperty("path", actual.toString()); row.addProperty("sha256", sha(actual));
            found.add(type.getName(), row);
        }
        require(pins.keySet().equals(names), "Incomplete or extra class-origin pin inventory");
        return found;
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Expected config.json report.json");
        JsonObject config = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        require(config.keySet().equals(Set.of("schema", "originalFixture", "rebuiltApk", "rebuiltGetterDex", "targetDex", "classPins"))
                && config.get("schema").isJsonPrimitive() && config.getAsJsonPrimitive("schema").isNumber()
                && config.get("schema").toString().equals("1"), "Unknown lookup control schema or fields");
        Path fixture = boundPath(config.getAsJsonObject("originalFixture"), "original fixture");
        Path apk = boundPath(config.getAsJsonObject("rebuiltApk"), "signed APK");
        Path getterDex = boundPath(config.getAsJsonObject("rebuiltGetterDex"), "signed getter partition");
        Path targetDex = boundPath(config.getAsJsonObject("targetDex"), "standalone target DEX");
        require(!sha(fixture).equals(sha(targetDex)), "Original fixture cannot masquerade as rebuilt target");
        require(!sha(fixture).equals(sha(getterDex)), "Original fixture cannot masquerade as signed getters");
        String member = config.getAsJsonObject("rebuiltGetterDex").get("apk_member").getAsString();
        require(member.matches("classes[2-9][0-9]*\\.dex|classes\\.dex"), "Invalid signed DEX member");
        try (ZipFile zip = new ZipFile(apk.toFile())) {
            var entry = zip.getEntry(member); require(entry != null && !entry.isDirectory(), "Signed getter partition missing");
            require(zip.stream().filter(item -> item.getName().equals(member)).count() == 1, "Duplicate signed getter partition");
            try (InputStream stream = zip.getInputStream(entry)) {
                require(sha(stream).equals(sha(getterDex)), "Getter partition differs from exact signed APK");
            }
        }
        JsonObject classOrigins = bindClasses(config.getAsJsonObject("classPins"));
        require(!defpackage.EngineRuntime.active && !defpackage.TestClock.enabled, "Unexpected enabled host runtime hook");
        BytecodeOracle original = new BytecodeOracle(fixture, DayLookupParityCases.ALL);
        BytecodeOracle rebuilt = new BytecodeOracle(getterDex, DayLookupParityCases.GETTERS);
        rebuilt.add(targetDex, Set.of(DayLookupParityCases.KEY));
        require(original.methods.keySet().equals(DayLookupParityCases.ALL), "Original lookup method/dependency inventory differs");
        require(rebuilt.methods.keySet().equals(DayLookupParityCases.ALL), "Rebuilt lookup method/dependency inventory differs");
        List<DayLookupParityCases.Input> inputs = DayLookupParityCases.pinnedCases();
        JsonArray rows = new JsonArray(), mismatches = new JsonArray(); int unsupported = 0, expectedFailures = 0;
        for (DayLookupParityCases.Input input : inputs) {
            DayLookupParityCases.State oldState = new DayLookupParityCases.State(input);
            DayLookupParityCases.State javaState = new DayLookupParityCases.State(input);
            DayLookupParityCases.State rebuiltState = new DayLookupParityCases.State(input);
            var old = DayLookupParityCases.observe(oldState, () -> original.invoke(DayLookupParityCases.KEY, oldState.dictionary, input.query()));
            var java = DayLookupParityCases.observe(javaState, () -> DayTriggerLookupMethods.findEntry(javaState.dictionary, input.query()));
            var fresh = DayLookupParityCases.observe(rebuiltState, () -> rebuilt.invoke(DayLookupParityCases.KEY, rebuiltState.dictionary, input.query()));
            JsonObject row = DayLookupParityCases.inputEvidence(input);
            row.add("original", JSON.toJsonTree(old)); row.add("java", JSON.toJsonTree(java)); row.add("rebuilt", JSON.toJsonTree(fresh));
            boolean same = DayLookupParityCases.sameScopedOutcome(input, old, java) && DayLookupParityCases.sameScopedOutcome(input, old, fresh);
            boolean correct = DayLookupParityCases.matchesExpected(input, old) && DayLookupParityCases.matchesExpected(input, java) && DayLookupParityCases.matchesExpected(input, fresh);
            row.addProperty("sameScopedOutcome", same); row.addProperty("allPathsMatchIndependentExpected", correct);
            if (!same || !correct) mismatches.add("day-lookup:" + input.name());
            for (var observed : List.of(old, java, fresh)) if (observed.unsupported()) unsupported++;
            if (!correct) expectedFailures++;
            rows.add(row);
        }
        JsonObject oldCoverage = DayLookupParityCases.coverage(original, DayLookupParityCases.ALL);
        JsonObject rebuiltCoverage = DayLookupParityCases.coverage(rebuilt, DayLookupParityCases.ALL);
        require(classOrigins.equals(bindClasses(config.getAsJsonObject("classPins"))), "Loaded class bytes changed during execution");
        for (String role : List.of("originalFixture", "rebuiltApk", "rebuiltGetterDex", "targetDex")) boundPath(config.getAsJsonObject(role), role + " after execution");
        JsonObject report = new JsonObject();
        report.addProperty("schema", 1);
        report.addProperty("scope", "One lookup method with two original field-getter dependencies; actual standalone target DEX and exact signed APK getter partition. Positive signed primary equality is a separate acceptance-driver gate. No Android/ART/calendar execution or exhaustive Unicode claim.");
        report.addProperty("exceptionComparisonScope", "Only the seven exact VM-null cases omit generated diagnostic text from comparisons. All raw messages are retained; every injected exception message, object identity and ordered iterator event compares exactly.");
        report.addProperty("primaryMethod", DayLookupParityCases.KEY); report.addProperty("primaryRecoveredMethods", 1);
        report.addProperty("originalDependencyMethods", 2); report.add("dependencyKeys", JSON.toJsonTree(new TreeSet<>(DayLookupParityCases.GETTERS)));
        report.addProperty("cases", inputs.size()); report.addProperty("executionPaths", 3); report.addProperty("androidRuntime", false);
        report.addProperty("inputInventorySha256", DayLookupParityCases.inputInventorySha256(inputs));
        report.addProperty("mismatchCount", mismatches.size()); report.addProperty("unsupportedCount", unsupported);
        report.addProperty("independentExpectedChecks", inputs.size()); report.addProperty("independentExpectedFailures", expectedFailures);
        report.add("inputIdentities", config.deepCopy()); report.add("loadedClassOrigins", classOrigins);
        report.add("originalCoverage", oldCoverage); report.add("rebuiltCoverage", rebuiltCoverage);
        report.add("observerRecordControls", DayLookupParityCases.observerControls(inputs));
        report.add("generatedNullMessageCases", JSON.toJsonTree(new TreeSet<>(DayLookupParityCases.VM_NULL_CASES)));
        report.add("mismatches", mismatches); report.add("observations", rows);
        report.addProperty("passed", mismatches.isEmpty() && unsupported == 0 && expectedFailures == 0
                && oldCoverage.get("allInstructionsAndEdgesExecuted").getAsBoolean()
                && rebuiltCoverage.get("allInstructionsAndEdgesExecuted").getAsBoolean());
        Files.writeString(Path.of(args[1]), JSON.toJson(report) + "\n");
        System.out.println("DAY_LOOKUP_CONTROL cases=" + inputs.size() + " paths=3 mismatches=" + mismatches.size()
                + " unsupported=" + unsupported + " expectedFailures=" + expectedFailures + " passed=" + report.get("passed"));
        if (!report.get("passed").getAsBoolean()) System.exit(3);
    }
}
