import com.google.gson.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Bounded study of the actual UI adapter; does not run unrelated UI cases. */
public final class LookupAdapterProbe {
    static void require(boolean value, String reason) { if (!value) throw new IllegalStateException(reason); }
    static String sha(Path file) throws Exception { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(file))); }
    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Expected config and result paths");
        JsonObject config = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        Path root = Path.of(config.get("root").getAsString());
        JsonObject origins = new JsonObject();
        for (var entry : config.getAsJsonObject("classPins").entrySet()) {
            Class<?> type = Class.forName(entry.getKey(), false, LookupAdapterProbe.class.getClassLoader());
            JsonObject pin = entry.getValue().getAsJsonObject();
            var url = type.getResource("/" + type.getName().replace('.', '/') + ".class");
            require(url != null && url.getProtocol().equals("file"), "Unexpected class origin: " + type.getName());
            Path actual = Path.of(url.toURI()).toRealPath();
            require(actual.equals(Path.of(pin.get("path").getAsString()).toRealPath()) && sha(actual).equals(pin.get("sha256").getAsString()), "Class identity mismatch: " + type.getName());
            origins.add(type.getName(), pin);
        }
        require(config.getAsJsonObject("classPins").keySet().containsAll(Set.of("LookupAdapterProbe", "UiParityTests", "DayLookupParityCases", "DayTriggerParityCases", "BytecodeOracle", "recovered.ui.DayTriggerLookupMethods", "recovered.ui.DayTriggerValueMethods", "com.arlosoft.macrodroid.variables.VariableValue", "com.arlosoft.macrodroid.variables.VariableValue$Dictionary", "com.arlosoft.macrodroid.variables.VariableValue$DictionaryEntry")), "Required class pins missing");
        Path fixture = root.resolve("tests/fixtures/original-methods.dex");
        require(sha(fixture).equals(config.get("fixtureSha256").getAsString()), "Wrong original fixture");
        for (JsonElement row : JsonParser.parseString(Files.readString(root.resolve("source/ui-methods.json"))).getAsJsonArray()) {
            JsonObject entry = row.getAsJsonObject(); String key = entry.get("target").getAsString() + "->" + entry.get("method").getAsString();
            require(UiParityTests.registry.put(key, entry) == null, "Duplicate UI registry");
        }
        require(UiParityTests.registry.size() == 12, "Wrong prospective UI registry");
        require(DayTriggerParityCases.loadDependencies(root, UiParityTests.registry.keySet()).equals(DayTriggerParityCases.GETTERS), "Numeric dependency partition changed");
        require(DayLookupParityCases.loadDependencies(root, UiParityTests.registry.keySet()).equals(DayLookupParityCases.GETTERS), "Lookup dependency partition changed");
        UiParityTests.original = new BytecodeOracle(fixture, DayLookupParityCases.ALL);
        require(UiParityTests.original.methods.keySet().equals(DayLookupParityCases.ALL), "Incomplete lookup fixture");
        require(!defpackage.EngineRuntime.active && !defpackage.TestClock.enabled, "Unexpected host hook enabled");
        DayLookupParityCases.run();
        JsonObject report = new JsonObject();
        boolean passed = UiParityTests.cases == 371 && UiParityTests.mismatches == 0 && UiParityTests.unsupported == 0
            && UiParityTests.expectedChecks == 371 && UiParityTests.expectedFailures == 0
            && UiParityTests.counts.equals(Map.of(DayLookupParityCases.KEY, 371));
        report.addProperty("passed", passed); report.addProperty("cases", UiParityTests.cases);
        report.addProperty("methodsExecuted", UiParityTests.counts.size()); report.addProperty("executionPaths", 2);
        report.addProperty("mismatches", UiParityTests.mismatches); report.addProperty("unsupported", UiParityTests.unsupported);
        report.addProperty("independentExpectedChecks", UiParityTests.expectedChecks); report.addProperty("independentExpectedFailures", UiParityTests.expectedFailures);
        report.add("failedLabels", UiParityTests.G.toJsonTree(UiParityTests.failedLabels)); report.add("failures", UiParityTests.G.toJsonTree(UiParityTests.failures));
        report.add("loadedClassOrigins", origins); report.addProperty("fixtureSha256", sha(fixture));
        if (!DayLookupParityCases.addReport(report, UiParityTests.original, null)) report.addProperty("passed", false);
        report.addProperty("scope", "Actual UI adapter over 371 original/JVM cases only. No unrelated app cases, D8, signed primary or Android execution in this command.");
        Files.writeString(Path.of(args[1]), new GsonBuilder().setPrettyPrinting().serializeNulls().create().toJson(report) + "\n");
        System.out.println("LOOKUP_ADAPTER cases=" + UiParityTests.cases + " mismatches=" + UiParityTests.mismatches + " unsupported=" + UiParityTests.unsupported);
        if (!report.get("passed").getAsBoolean()) System.exit(2);
    }
}
