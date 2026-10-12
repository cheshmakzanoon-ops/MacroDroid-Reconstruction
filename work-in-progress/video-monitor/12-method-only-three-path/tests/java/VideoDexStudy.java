import com.google.gson.*;
import com.android.tools.smali.dexlib2.DexFileFactory;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.iface.DexFile;
import java.lang.management.ManagementFactory;
import java.net.URL;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Small original/JVM/transplanted-DEX study; the original coverage gate stays strict. */
public final class VideoDexStudy {
    static final String ORIGINAL_SHA = "940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254";
    static final String TARGET = "Lcom/arlosoft/macrodroid/action/services/a;";
    static final String METHOD = "invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;";

    static String hash(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    static JsonObject coverage(BytecodeOracle oracle) {
        String key = VideoParityCases.KEY;
        Set<Integer> visited = oracle.executed.getOrDefault(key, Collections.emptySet());
        Set<String> edges = oracle.branchEdges.getOrDefault(key, Collections.emptySet());
        List<Integer> unseen = new ArrayList<>();
        List<String> missing = new ArrayList<>();
        int offset = 0, total = 0, possible = 0;
        for (var instruction : oracle.methods.get(key).getImplementation().getInstructions()) {
            if (!visited.contains(offset)) unseen.add(offset);
            if (instruction.getOpcode().name().startsWith("IF_")) {
                possible += 2;
                int jump = offset + ((com.android.tools.smali.dexlib2.iface.instruction.OffsetInstruction) instruction).getCodeOffset();
                for (int target : new int[] {offset + instruction.getCodeUnits(), jump})
                    if (!edges.contains(offset + ":" + target)) missing.add(offset + ":" + target);
            }
            offset += instruction.getCodeUnits();
            total++;
        }
        JsonObject result = new JsonObject();
        result.addProperty("instructions", total);
        result.addProperty("visited", visited.size());
        result.add("unvisitedOffsets", UiParityTests.G.toJsonTree(unseen));
        result.addProperty("conditionalEdges", possible);
        result.addProperty("conditionalEdgesVisited", possible - missing.size());
        result.add("unvisitedConditionalEdges", UiParityTests.G.toJsonTree(missing));
        return result;
    }

    static JsonObject liveRuntime(Path output) throws Exception {
        Files.createDirectory(output);
        JsonObject result = new JsonObject();
        for (String key : List.of("java.home", "java.version", "java.runtime.version", "java.vm.version", "java.vm.name", "java.vendor"))
            result.addProperty(key, System.getProperty(key));
        result.add("jvmArguments", UiParityTests.G.toJsonTree(ManagementFactory.getRuntimeMXBean().getInputArguments()));
        JsonArray classes = new JsonArray();
        for (String name : List.of("java.lang.StringBuilder", "java.lang.AbstractStringBuilder", "java.lang.StringUTF16", "java.lang.Object")) {
            Class<?> type = Class.forName(name, false, null);
            String resourceName = "/" + name.replace('.', '/') + ".class";
            URL url = type.getResource(resourceName);
            if (type.getClassLoader() != null || !"java.base".equals(type.getModule().getName()) || url == null ||
                    !url.toString().equals("jrt:/java.base" + resourceName))
                throw new IllegalStateException("Unexpected live boot class origin: " + name);
            byte[] bytes;
            try (var input = type.getResourceAsStream(resourceName)) {
                if (input == null) throw new IllegalStateException("Missing live boot class bytes");
                bytes = input.readAllBytes();
            }
            String filename = name.substring(name.lastIndexOf('.') + 1) + ".class";
            Files.write(output.resolve(filename), bytes, StandardOpenOption.CREATE_NEW);
            JsonObject row = new JsonObject();
            row.addProperty("class", name); row.addProperty("resource", url.toString());
            row.addProperty("module", type.getModule().getName()); row.addProperty("bootstrapLoader", true);
            row.addProperty("bytes", bytes.length); row.addProperty("sha256", hash(bytes));
            row.addProperty("file", filename); classes.add(row);
        }
        result.add("classes", classes);
        byte[] release = Files.readAllBytes(Paths.get(System.getProperty("java.home"), "release"));
        Files.write(output.resolve("release"), release, StandardOpenOption.CREATE_NEW);
        result.addProperty("releaseSha256", hash(release));
        result.addProperty("scope", "Runtime evidence collected inside the JVM that executes all three paths; no static coverage accounting policy is applied.");
        Files.writeString(output.resolve("runtime.json"), UiParityTests.G.toJson(result) + "\n", StandardOpenOption.CREATE_NEW);
        return result;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 6) throw new IllegalArgumentException("Expected entry, original, rebuilt, rebuilt SHA, report and live-runtime directory");
        JsonObject entry = JsonParser.parseString(Files.readString(Paths.get(args[0]))).getAsJsonObject();
        String key = entry.get("target").getAsString() + "->" + entry.get("method").getAsString();
        if (!VideoParityCases.KEY.equals(key) || entry.has("constructor_owner_mappings"))
            throw new IllegalArgumentException("Unexpected video study entry");
        Path originalFile = Paths.get(args[1]), rebuiltFile = Paths.get(args[2]);
        if (!hash(Files.readAllBytes(originalFile)).equals(ORIGINAL_SHA)) throw new IllegalStateException("Original fixture identity differs");
        if (!args[3].matches("[0-9a-f]{64}") || !hash(Files.readAllBytes(rebuiltFile)).equals(args[3]))
            throw new IllegalStateException("Rebuilt fixture identity differs");
        DexFile dex = DexFileFactory.loadDexFile(rebuiltFile.toFile(), Opcodes.forApi(23));
        if (dex.getClasses().size() != 1 || !dex.getClasses().iterator().next().getType().equals(TARGET))
            throw new IllegalStateException("Exactly the original target class must be assembled");
        UiParityTests.registry.put(key, entry);
        UiParityTests.original = new BytecodeOracle(originalFile, UiParityTests.registry.keySet());
        UiParityTests.rebuilt = new BytecodeOracle(rebuiltFile, UiParityTests.registry.keySet());
        if (UiParityTests.original.methods.size() != 1 || UiParityTests.rebuilt.methods.size() != 1)
            throw new IllegalStateException("Exactly one selected method is required in each oracle");
        Path runtime = Paths.get(args[5]); Files.createDirectory(runtime);
        JsonObject before = liveRuntime(runtime.resolve("before"));
        VideoParityCases.run();
        JsonObject after = liveRuntime(runtime.resolve("after"));
        boolean runtimeUnchanged = before.equals(after);
        JsonObject originalCoverage = coverage(UiParityTests.original), rebuiltCoverage = coverage(UiParityTests.rebuilt);
        boolean noAdapters = UiParityTests.original.parentConstructorAdapters.isEmpty() &&
            UiParityTests.original.parentConstructorAdapterCalls.isEmpty() &&
            UiParityTests.rebuilt.parentConstructorAdapters.isEmpty() && UiParityTests.rebuilt.parentConstructorAdapterCalls.isEmpty();
        boolean semanticMatch = UiParityTests.counts.keySet().equals(UiParityTests.registry.keySet()) &&
            noAdapters && runtimeUnchanged && UiParityTests.mismatches == 0 && UiParityTests.unsupported == 0 && UiParityTests.expectedFailures == 0;
        boolean fullCoverage = originalCoverage.getAsJsonArray("unvisitedOffsets").size() == 0 &&
            originalCoverage.getAsJsonArray("unvisitedConditionalEdges").size() == 0;
        JsonObject report = new JsonObject();
        report.addProperty("passed", semanticMatch && fullCoverage);
        report.addProperty("semanticMatch", semanticMatch);
        report.addProperty("cases", UiParityTests.cases);
        report.addProperty("failedCases", UiParityTests.mismatches);
        report.addProperty("unsupportedExecutions", UiParityTests.unsupported);
        report.addProperty("independentExpectedResultChecks", UiParityTests.expectedChecks);
        report.addProperty("expectedResultFailures", UiParityTests.expectedFailures);
        report.addProperty("originalOnlyBoundaryDiscoveryExecutions", VideoParityCases.discoveryExecutions);
        report.addProperty("methodsCovered", UiParityTests.counts.size());
        report.add("methodKeys", UiParityTests.G.toJsonTree(UiParityTests.counts.keySet()));
        report.addProperty("paths", 3);
        report.addProperty("androidRuntime", false); report.addProperty("rebuiltDexCompared", true);
        report.addProperty("registeredInActiveProject", false); report.addProperty("signedApkBuilt", false);
        report.add("instructionCoverage", originalCoverage); report.add("rebuiltInstructionCoverage", rebuiltCoverage);
        report.add("originalExecutedOffsets", UiParityTests.G.toJsonTree(new TreeSet<>(UiParityTests.original.executed.getOrDefault(key, Collections.emptySet()))));
        report.add("originalExecutedConditionalEdges", UiParityTests.G.toJsonTree(new TreeSet<>(UiParityTests.original.branchEdges.getOrDefault(key, Collections.emptySet()))));
        report.add("rebuiltExecutedOffsets", UiParityTests.G.toJsonTree(new TreeSet<>(UiParityTests.rebuilt.executed.getOrDefault(key, Collections.emptySet()))));
        report.add("rebuiltExecutedConditionalEdges", UiParityTests.G.toJsonTree(new TreeSet<>(UiParityTests.rebuilt.branchEdges.getOrDefault(key, Collections.emptySet()))));
        report.addProperty("fullInstructionAndConditionalCoverage", fullCoverage);
        report.addProperty("noConstructorOwnerAdapterUsed", noAdapters);
        report.addProperty("liveRuntimeUnchanged", runtimeUnchanged); report.add("liveRuntime", before);
        report.addProperty("coverageExemptionImplemented", false);
        report.add("failures", UiParityTests.G.toJsonTree(UiParityTests.failures));
        report.add("failedCaseLabels", UiParityTests.G.toJsonTree(UiParityTests.failedLabels));
        report.add("generatedEscapedMessageExclusions", UiParityTests.G.toJsonTree(VideoParityCases.generatedEscapedMessages));
        report.addProperty("exceptionMessageScope", "The frozen 07 exact source-class observer is unchanged. All raw messages remain recorded; injected/external identity and text stay exact. Same-source-type malformed values do not distinguish cast order.");
        report.addProperty("scope", "Bounded original/JVM/method-only rebuilt DEX comparison; full raw original instruction coverage remains required. No Android service, filesystem operation, scheduler, signed APK, active registration or coverage exemption.");
        Files.writeString(Paths.get(args[4]), UiParityTests.G.toJson(report) + "\n", StandardOpenOption.CREATE_NEW);
        System.out.println("Video three-path cases=" + UiParityTests.cases + " mismatches=" + UiParityTests.mismatches +
            " unsupported=" + UiParityTests.unsupported + " expected=" + UiParityTests.expectedChecks +
            " original=" + originalCoverage.get("visited") + "/" + originalCoverage.get("instructions") +
            " rebuilt=" + rebuiltCoverage.get("visited") + "/" + rebuiltCoverage.get("instructions"));
        if (!report.get("passed").getAsBoolean()) System.exit(2);
    }
}
