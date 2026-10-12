import com.google.gson.*;
import java.net.URL;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Verifies the actual loaded mutant and fixed oracle/harness classes before execution. */
public final class WidgetMutationLauncher {
    private static final List<String> REQUIRED = Arrays.asList(
        "recovered.ui.WidgetUpdateMethods", "BytecodeOracle", "UiParityTests",
        "WidgetParityCases", "WidgetParityStudy", "defpackage.WidgetControl",
        "defpackage.zhh", "defpackage.rff", "defpackage.rjb", "defpackage.rx6",
        "com.arlosoft.macrodroid.widget.custom.b");

    public static void main(String[] args) throws Exception {
        if (args.length != 5) throw new IllegalArgumentException(
            "Expected origin manifest, origin report, proposed entry, original fixture, parity report");
        JsonArray declared = JsonParser.parseString(Files.readString(Paths.get(args[0]))).getAsJsonArray();
        if (declared.size() != REQUIRED.size()) throw new IllegalStateException("Incomplete class origin manifest");
        JsonArray observed = new JsonArray();
        int index = 0;
        for (JsonElement value : declared) {
            JsonObject row = value.getAsJsonObject();
            String name = row.get("class").getAsString();
            if (!REQUIRED.get(index++).equals(name)) throw new IllegalStateException("Unexpected class origin entry");
            Class<?> type = Class.forName(name, false, WidgetMutationLauncher.class.getClassLoader());
            URL resource = type.getResource("/" + name.replace('.', '/') + ".class");
            if (resource == null || !"file".equals(resource.getProtocol()))
                throw new IllegalStateException("Expected a private class file for " + name);
            Path actual = Paths.get(resource.toURI()).toRealPath();
            Path expected = Paths.get(row.get("path").getAsString()).toRealPath();
            if (!actual.equals(expected)) throw new IllegalStateException("Wrong loaded class origin for " + name);
            String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(actual)));
            if (!digest.equals(row.get("sha256").getAsString())) throw new IllegalStateException("Wrong loaded class hash for " + name);
            JsonObject result = new JsonObject();
            result.addProperty("class", name);
            result.addProperty("path", actual.toString());
            result.addProperty("sha256", digest);
            result.addProperty("verified", true);
            observed.add(result);
        }
        JsonObject report = new JsonObject();
        report.addProperty("passed", true);
        report.addProperty("scope", "Actual loaded helper plus fixed original interpreter, case harness and selected controlled boundaries");
        report.add("classes", observed);
        Files.writeString(Paths.get(args[1]), new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        WidgetParityStudy.main(new String[]{args[2], args[3], args[4]});
    }
}
