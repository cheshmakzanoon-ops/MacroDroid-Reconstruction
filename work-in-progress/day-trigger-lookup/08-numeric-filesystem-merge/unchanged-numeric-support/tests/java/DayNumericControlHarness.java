import com.arlosoft.macrodroid.variables.VariableValue;
import com.google.gson.*;
import recovered.ui.DayTriggerValueMethods;
import java.io.InputStream;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.zip.ZipFile;

/** A separate, explicitly bounded three-path harness for actual numeric DEX faults.
 * It does not replace the complete UI suite or claim that a standalone target DEX
 * was packaged. The owning acceptance driver separately checks the positive target
 * instruction listing against the signed APK before accepting its control report. */
public final class DayNumericControlHarness {
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
        Path path = Path.of(row.get("path").getAsString()).toRealPath();
        require(sha(path).equals(row.get("sha256").getAsString()), "Wrong input identity: " + role);
        return path;
    }
    static Set<Class<?>> requiredClasses() {
        Set<Class<?>> selected = new LinkedHashSet<>(List.of(DayNumericControlHarness.class, DayTriggerParityCases.class,
            BytecodeOracle.class, DayTriggerValueMethods.class, VariableValue.class,
            defpackage.EngineRuntime.class, defpackage.TestClock.class));
        boolean more = true;
        while (more) {
            more = false;
            for (Class<?> type : new ArrayList<>(selected)) for (Class<?> nested : type.getDeclaredClasses()) more |= selected.add(nested);
        }
        return selected;
    }
    static JsonObject bindClasses(JsonObject pins) throws Exception {
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
        require(config.get("schema").getAsInt() == 1, "Unknown numeric control schema");
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
        BytecodeOracle original = new BytecodeOracle(fixture, DayTriggerParityCases.ALL);
        BytecodeOracle rebuilt = new BytecodeOracle(getterDex, DayTriggerParityCases.GETTERS);
        rebuilt.add(targetDex, Set.of(DayTriggerParityCases.KEY));
        require(original.methods.keySet().equals(DayTriggerParityCases.ALL), "Original numeric method/dependency inventory differs");
        require(rebuilt.methods.keySet().equals(DayTriggerParityCases.ALL), "Rebuilt numeric method/dependency inventory differs");
        List<DayTriggerParityCases.Input> inputs = DayTriggerParityCases.cases();
        JsonArray rows = new JsonArray(), mismatches = new JsonArray(); int unsupported = 0, expectedFailures = 0;
        for (DayTriggerParityCases.Input input : inputs) {
            DayTriggerParityCases.Observed old = DayTriggerParityCases.observe(() -> original.invoke(DayTriggerParityCases.KEY, DayTriggerParityCases.entry(input)));
            DayTriggerParityCases.Observed java = DayTriggerParityCases.observe(() -> DayTriggerValueMethods.numericValue(DayTriggerParityCases.entry(input)));
            DayTriggerParityCases.Observed fresh = DayTriggerParityCases.observe(() -> rebuilt.invoke(DayTriggerParityCases.KEY, DayTriggerParityCases.entry(input)));
            JsonObject row = DayTriggerParityCases.inputIdentity(input);
            if (input.kind().equals("null-entry")) row.addProperty("expectedExceptionClass", "java.lang.NullPointerException");
            else row.addProperty("expected", DayTriggerParityCases.expected(input));
            row.add("original", JSON.toJsonTree(old)); row.add("java", JSON.toJsonTree(java)); row.add("rebuilt", JSON.toJsonTree(fresh));
            boolean same = DayTriggerParityCases.sameScopedOutcome(input, old, java) && DayTriggerParityCases.sameScopedOutcome(input, old, fresh);
            boolean correct = DayTriggerParityCases.matchesExpected(input, old) && DayTriggerParityCases.matchesExpected(input, java) && DayTriggerParityCases.matchesExpected(input, fresh);
            row.addProperty("sameScopedOutcome", same); row.addProperty("allPathsMatchIndependentExpected", correct);
            if (!same || !correct) mismatches.add("day-numeric:" + input.name());
            for (var observed : List.of(old, java, fresh)) if (observed.unsupported()) unsupported++;
            if (!correct) expectedFailures++;
            rows.add(row);
        }
        JsonObject oldCoverage = DayTriggerParityCases.coverage(original, DayTriggerParityCases.ALL);
        JsonObject rebuiltCoverage = DayTriggerParityCases.coverage(rebuilt, DayTriggerParityCases.ALL);
        require(classOrigins.equals(bindClasses(config.getAsJsonObject("classPins"))), "Loaded class bytes changed during execution");
        for (String role : List.of("originalFixture", "rebuiltApk", "rebuiltGetterDex", "targetDex")) boundPath(config.getAsJsonObject(role), role + " after execution");
        JsonObject report = new JsonObject();
        report.addProperty("schema", 1); report.addProperty("scope", "One numeric method with three original field-getter dependencies. A standalone target DEX is tested; packaging equality is a separate acceptance-driver check. No Android/ART/calendar execution.");
        report.addProperty("exceptionComparisonScope", "Only the explicit null-entry NPE compares its class. Every raw exception message is retained; all other complete outcomes compare.");
        report.addProperty("primaryMethod", DayTriggerParityCases.KEY); report.addProperty("primaryRecoveredMethods", 1);
        report.addProperty("originalDependencyMethods", 3); report.add("dependencyKeys", JSON.toJsonTree(new TreeSet<>(DayTriggerParityCases.GETTERS)));
        report.addProperty("cases", inputs.size()); report.addProperty("executionPaths", 3); report.addProperty("androidRuntime", false);
        report.addProperty("inputInventorySha256", DayTriggerParityCases.inputInventorySha256(inputs));
        report.addProperty("mismatchCount", mismatches.size()); report.addProperty("unsupportedCount", unsupported);
        report.addProperty("independentExpectedChecks", inputs.size()); report.addProperty("independentExpectedFailures", expectedFailures);
        report.add("inputIdentities", config.deepCopy()); report.add("loadedClassOrigins", classOrigins);
        report.add("originalCoverage", oldCoverage); report.add("rebuiltCoverage", rebuiltCoverage);
        report.add("mismatches", mismatches); report.add("observations", rows);
        report.addProperty("passed", mismatches.isEmpty() && unsupported == 0 && expectedFailures == 0
                && oldCoverage.get("allInstructionsAndEdgesExecuted").getAsBoolean()
                && rebuiltCoverage.get("allInstructionsAndEdgesExecuted").getAsBoolean());
        Files.writeString(Path.of(args[1]), JSON.toJson(report) + "\n");
        System.out.println("DAY_NUMERIC_CONTROL cases=" + inputs.size() + " paths=3 mismatches=" + mismatches.size()
                + " unsupported=" + unsupported + " expectedFailures=" + expectedFailures + " passed=" + report.get("passed"));
        if (!report.get("passed").getAsBoolean()) System.exit(3);
    }
}
