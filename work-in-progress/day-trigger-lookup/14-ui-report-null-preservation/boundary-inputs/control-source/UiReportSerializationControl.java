import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Host serializer boundary only. Neither writer executes application methods. */
public final class UiReportSerializationControl {
    static final Gson G = new GsonBuilder().setPrettyPrinting().create();
    static final Gson EVIDENCE = new GsonBuilder().serializeNulls().setPrettyPrinting().create();
    static void writeOriginal(Path reportPath, JsonObject report) throws Exception {
        Files.writeString(reportPath,G.toJson(report));
    }
    static void writeCorrected(Path reportPath, JsonObject report) throws Exception {
        Files.writeString(reportPath,G.newBuilder().serializeNulls().create().toJson(report));
    }
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
        Files.writeString(output.resolve("expected-tree.json"), EVIDENCE.toJson(report) + "\n");
        Files.writeString(output.resolve("result.json"), EVIDENCE.toJson(result) + "\n");
        System.out.println("UI_REPORT_SERIALIZER mode=" + mode + " strict=" + result.get("observerStrictEquality") + " roundtrip=" + result.get("passed") + " absentNulls=" + absentNulls.size());
        if (!result.get("passed").getAsBoolean()) System.exit(2);
    }
}
