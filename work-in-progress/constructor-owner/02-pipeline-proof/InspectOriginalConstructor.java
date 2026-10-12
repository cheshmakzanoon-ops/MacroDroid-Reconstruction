/* Read-only original APK extraction with the project's pinned Apktool bundle. */
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.BaksmaliOptions;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedDexFile;
import com.android.tools.smali.dexlib2.iface.ClassDef;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.zip.ZipFile;

public class InspectOriginalConstructor {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("Expected original APK and new output directory");
        Path output = Path.of(args[1]);
        Files.createDirectory(output);
        var targets = new LinkedHashMap<String, String>();
        targets.put("Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;", "WidgetUpdateManager.smali");
        targets.put("Lzhh;", "zhh.smali");
        targets.put("Lrff;", "rff.smali");
        var options = new BaksmaliOptions();
        options.localsDirective = true;
        options.debugInfo = true;
        try (var apk = new ZipFile(args[0])) {
            var entries = apk.entries();
            while (entries.hasMoreElements()) {
                var entry = entries.nextElement();
                if (!entry.getName().matches("classes[0-9]*\\.dex")) continue;
                byte[] bytes = apk.getInputStream(entry).readAllBytes();
                var dex = new DexBackedDexFile(bytes, 0);
                boolean selected = false;
                for (int index = 0; index < dex.classCount; index++) {
                    var definition = (ClassDef) dex.classSection.get(index);
                    String filename = targets.remove(definition.getType());
                    if (filename == null) continue;
                    try (var writer = Files.newBufferedWriter(output.resolve(filename))) {
                        new ClassDefinition(options, definition).writeTo(new BaksmaliWriter(writer));
                    }
                    System.out.println(definition.getType() + " -> " + filename + " from " + entry.getName());
                    selected = true;
                }
                if (selected) System.out.println(entry.getName() + " SHA256 " +
                    HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)));
            }
        }
        if (!targets.isEmpty()) throw new IllegalStateException("Missing original classes: " + targets.keySet());
    }
}
