import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.google.gson.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Exact original test-fixture extraction. Declared getter dependencies earn no
 * recovered-method credit and never become application build inputs. */
public final class ExtractOracle {
    static final String ORIGINAL_APK_SHA256 = "84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800";
    record Selection(Map<String, Set<String>> methods, Set<String> registered, Set<String> dependencies) {}
    static void require(boolean condition, String message) { if (!condition) throw new IllegalStateException(message); }
    static String signature(Method method) { return method.getName() + "(" + String.join("", method.getParameterTypes()) + ")" + method.getReturnType(); }
    static String sha(Path path) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (var stream = Files.newInputStream(path)) {
            byte[] buffer = new byte[65536]; int count;
            while ((count = stream.read(buffer)) != -1) digest.update(buffer, 0, count);
        }
        return HexFormat.of().formatHex(digest.digest());
    }
    static String key(JsonObject entry) {
        String target = entry.get("target").getAsString(), method = entry.get("method").getAsString();
        require(target.startsWith("L") && target.endsWith(";") && method.contains("(") && method.contains(")"), "Malformed original method selection");
        return target + "->" + method;
    }
    static Selection selection(JsonArray registry, JsonObject declaration) {
        Set<String> registered = new TreeSet<>(), dependencies = new TreeSet<>();
        Map<String, Set<String>> selected = new TreeMap<>();
        for (JsonElement item : registry) {
            JsonObject entry = item.getAsJsonObject();
            require(registered.add(key(entry)), "Duplicate registered original method");
            selected.computeIfAbsent(entry.get("target").getAsString(), unused -> new TreeSet<>()).add(entry.get("method").getAsString());
        }
        require(!registered.isEmpty(), "Empty original registry");
        require(declaration.keySet().equals(Set.of("schema", "purpose", "dependencies"))
                && declaration.get("schema").isJsonPrimitive()
                && declaration.get("schema").getAsJsonPrimitive().isNumber()
                && declaration.get("schema").getAsString().equals("1"), "Invalid original dependency declaration");
        for (JsonElement item : declaration.getAsJsonArray("dependencies")) {
            JsonObject entry = item.getAsJsonObject();
            require(entry.keySet().equals(Set.of("consumer", "target", "method", "original_method_sha256")), "Invalid original dependency fields");
            String selectedKey = key(entry);
            require(registered.contains(entry.get("consumer").getAsString()), "Original dependency has no registered consumer");
            require(!registered.contains(selectedKey), "Original dependency overlaps recovered registry");
            require(dependencies.add(selectedKey), "Duplicate original dependency");
            require(entry.get("original_method_sha256").getAsString().matches("[0-9a-f]{64}"), "Invalid original dependency method hash");
            require(selected.computeIfAbsent(entry.get("target").getAsString(), unused -> new TreeSet<>()).add(entry.get("method").getAsString()), "Duplicate selected original method");
        }
        return new Selection(selected, registered, dependencies);
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Expected project root and exact original APK");
        Path root = Path.of(args[0]), apk = Path.of(args[1]);
        Path registryPath = root.resolve("source/java-method-map.json"), dependencyPath = root.resolve("tests/fixtures/original-dependencies.json");
        JsonArray registry = JsonParser.parseString(Files.readString(registryPath)).getAsJsonArray();
        JsonObject declaration = JsonParser.parseString(Files.readString(dependencyPath)).getAsJsonObject();
        Selection wanted = selection(registry, declaration);
        require(sha(apk).equals(ORIGINAL_APK_SHA256), "Unexpected original APK identity");
        var container = DexFileFactory.loadDexContainer(apk.toFile(), Opcodes.forApi(23));
        List<ClassDef> classes = new ArrayList<>(); Set<String> seenClasses = new TreeSet<>(), seenMethods = new TreeSet<>();
        for (String name : container.getDexEntryNames()) {
            for (ClassDef type : container.getEntry(name).getDexFile().getClasses()) {
                Set<String> methods = wanted.methods().get(type.getType()); if (methods == null) continue;
                require(seenClasses.add(type.getType()), "Duplicate selected original class");
                List<Method> selected = new ArrayList<>();
                for (Method method : type.getMethods()) if (methods.contains(signature(method))) {
                    require(seenMethods.add(type.getType() + "->" + signature(method)), "Duplicate original method in APK");
                    selected.add(method);
                }
                require(selected.size() == methods.size(), "Missing original methods in " + type.getType());
                classes.add(new ImmutableClassDef(type.getType(), type.getAccessFlags(), type.getSuperclass(), type.getInterfaces(),
                        type.getSourceFile(), type.getAnnotations(), type.getFields(), selected));
            }
        }
        Set<String> expected = new TreeSet<>(wanted.registered()); expected.addAll(wanted.dependencies());
        require(seenClasses.equals(wanted.methods().keySet()) && seenMethods.equals(expected), "Incomplete original fixture");
        Path output = root.resolve("tests/fixtures/original-methods.dex"), temporary = output.resolveSibling(output.getFileName() + ".new");
        require(!Files.exists(temporary), "Unclosed original fixture generation exists");
        Files.createDirectories(output.getParent());
        DexPool.writeTo(temporary.toString(), new ImmutableDexFile(Opcodes.forApi(23), classes));
        Files.move(temporary, output, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
        JsonObject result = new JsonObject();
        result.addProperty("original_apk_sha256", ORIGINAL_APK_SHA256);
        result.addProperty("registry_sha256", sha(registryPath)); result.addProperty("dependency_declaration_sha256", sha(dependencyPath));
        result.addProperty("registered_methods", wanted.registered().size()); result.addProperty("dependency_methods", wanted.dependencies().size());
        result.addProperty("methods", seenMethods.size()); result.addProperty("classes", classes.size());
        result.add("dependency_keys", new Gson().toJsonTree(wanted.dependencies()));
        result.addProperty("fixture_sha256", sha(output)); result.addProperty("fixture_bytes", Files.size(output));
        result.addProperty("application_build_input", false);
        Files.createDirectories(root.resolve("reports"));
        Files.writeString(root.resolve("reports/original-fixture-extraction.json"), new GsonBuilder().setPrettyPrinting().create().toJson(result) + "\n");
        System.out.println("Test-only original fixture: classes=" + classes.size() + " methods=" + seenMethods.size()
                + " registered=" + wanted.registered().size() + " dependencies=" + wanted.dependencies().size());
    }
}
