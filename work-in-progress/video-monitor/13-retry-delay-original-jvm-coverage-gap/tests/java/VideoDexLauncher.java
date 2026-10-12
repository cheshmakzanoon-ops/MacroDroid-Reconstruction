import com.google.gson.*;
import java.net.URL;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Bind the classes actually loaded before invoking the three-path method study. */
public final class VideoDexLauncher {
    private static final List<String> REQUIRED = Arrays.asList(
        "recovered.ui.VideoMonitorMethods", "BytecodeOracle", "UiParityTests", "VideoParityCases", "VideoParityStudy",
        "defpackage.VideoControl", "defpackage.VideoFile", "com.arlosoft.macrodroid.action.services.a",
        "com.arlosoft.macrodroid.action.services.BaseVideoRecordingService",
        "com.arlosoft.macrodroid.action.services.BaseVideoRecordingService$a",
        "android.content.Context", "android.os.Environment", "android.os.ParcelFileDescriptor",
        "defpackage.sz6", "defpackage.dt9", "defpackage.d31", "defpackage.u2f", "defpackage.e6d",
        "defpackage.kjf", "defpackage.jb3", "defpackage.v93", "defpackage.blg", "defpackage.qnc",
        "defpackage.rff", "defpackage.i93", "defpackage.jn6", "defpackage.at9", "defpackage.zp4",
        "defpackage.m47", "defpackage.ad4", "VideoDexStudy", "VideoDexLauncher");

    public static void main(String[] args) throws Exception {
        if (args.length != 8) throw new IllegalArgumentException("Expected origins, origin report, entry, original, rebuilt, rebuilt SHA, parity report and runtime directory");
        JsonArray declared = JsonParser.parseString(Files.readString(Paths.get(args[0]))).getAsJsonArray();
        if (declared.size() != REQUIRED.size()) throw new IllegalStateException("Incomplete class origin manifest");
        JsonArray observed = new JsonArray(); int index = 0;
        for (JsonElement value : declared) {
            JsonObject row = value.getAsJsonObject(); String name = row.get("class").getAsString();
            if (!REQUIRED.get(index++).equals(name)) throw new IllegalStateException("Unexpected class origin entry");
            Class<?> type = Class.forName(name, false, VideoDexLauncher.class.getClassLoader());
            URL resource = type.getResource("/" + name.replace('.', '/') + ".class");
            if (resource == null || !"file".equals(resource.getProtocol())) throw new IllegalStateException("Expected private class file for " + name);
            Path actual = Paths.get(resource.toURI()).toRealPath(), expected = Paths.get(row.get("path").getAsString()).toRealPath();
            if (!actual.equals(expected)) throw new IllegalStateException("Wrong loaded class origin for " + name);
            String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(actual)));
            if (!digest.equals(row.get("sha256").getAsString())) throw new IllegalStateException("Wrong loaded class hash for " + name);
            JsonObject item = new JsonObject(); item.addProperty("class", name); item.addProperty("path", actual.toString());
            item.addProperty("sha256", digest); item.addProperty("verified", true); observed.add(item);
        }
        JsonObject report = new JsonObject(); report.addProperty("passed", true); report.add("classes", observed);
        report.addProperty("scope", "Actual helper, original interpreter, unchanged frozen harness, controlled dependencies and the new three-path launcher/study");
        Files.writeString(Paths.get(args[1]), new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n", StandardOpenOption.CREATE_NEW);
        VideoDexStudy.main(Arrays.copyOfRange(args, 2, 8));
    }
}
