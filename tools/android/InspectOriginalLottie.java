/* Read-only inspection using the repository's checksum-pinned Apktool bundle. */
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

public class InspectOriginalLottie {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            throw new IllegalArgumentException("Expected original APK and new output directory");
        }
        Path output = Path.of(args[1]);
        Files.createDirectory(output);
        var targets = new LinkedHashMap<String, String>();
        targets.put("Llk9;", "LottieDrawable.smali");
        targets.put("Lcom/airbnb/lottie/LottieAnimationView;", "LottieAnimationView.smali");
        targets.put("Lvk9;", "LottieValueAnimator.smali");
        try (var apk = new ZipFile(args[0])) {
            byte[] bytes = apk.getInputStream(apk.getEntry("classes.dex")).readAllBytes();
            String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
            System.out.println("classes.dex SHA256 " + digest);
            var dex = new DexBackedDexFile(bytes, 0);
            var options = new BaksmaliOptions();
            options.localsDirective = true;
            options.debugInfo = true;
            for (int i = 0; i < dex.classCount; i++) {
                var definition = (ClassDef) dex.classSection.get(i);
                String filename = targets.remove(definition.getType());
                if (filename == null) continue;
                try (var writer = Files.newBufferedWriter(output.resolve(filename))) {
                    new ClassDefinition(options, definition).writeTo(new BaksmaliWriter(writer));
                }
                System.out.println(definition.getType() + " -> " + filename);
            }
            if (!targets.isEmpty()) throw new IllegalStateException("Missing original classes: " + targets.keySet());
        }
    }
}
